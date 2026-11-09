"""Deterministic lexical retrieval over the SQLite FTS5 index.

retrieve(con, question, filters, top_k) -> dict with passages, provenance, scores, status.

Relevance is NOT eligibility. A passage is returned as supporting evidence only if it
  (1) is ACTIVE in the allowlisted index and passes the metadata filters,
  (2) covers enough of the question's content terms (term-coverage gate, not just a BM25 rank),
  (3) is not a different-jurisdiction passage when the question names a target jurisdiction
      (those go to `transfer_context`, never to `passages`),
  (4) belongs to its source's current file hash (source modified since ingest => excluded).
No chunk is ever synthesised. Unmet thresholds return INSUFFICIENT_EVIDENCE.
"""
import json
import re

from .store import source_is_current

STOPWORDS = set("""a an the of to in on for and or is are was were be been being what which who whom how do does did
can could should would will may might must i we you my our your it its this that these those with without from by as at
about into than then there their them they not no any all each per give tell show explain suggest suggests say says
state states list find need needs use used using between over under if when where why very also so such more most
many much some other another suggested recommend recommended recommends provide provides please whether""".split())

JURISDICTION_NAMES = {"qatar": "QA", "al-shahaniya": "QA", "shahaniya": "QA", "doha": "QA", "qatari": "QA",
                      "saudi": "SA", "riyadh": "SA", "florida": "US-FL", "mediterranean": "MED"}

STRATEGIES = {"strict": 0.6, "relaxed": 0.5}  # min term coverage; eligibility filters never relax

# Questions that ask for a number/measurement. For these, a passage with no quantitative content cannot
# be the support, and (when a jurisdiction is named) a general principle cannot stand in for a site value.
_QUANTITY_SEEKING = re.compile(
    r"\b(measured|measurement|measurements|how\s+much|how\s+many|how\s+(large|big|high|long)|"
    r"what\s+(is|are|was|were)\s+the\s+(typical\s+|average\s+|required\s+|design\s+)?"
    r"(rate|amount|volume|demand|cost|price|value|kw|size|capacity|yield|use|consumption)|"
    r"per\s+(m2|m\u00b2|m3|hectare|ha|kg|day|hour|season|plant))\b", re.IGNORECASE)


def is_quantity_seeking(question):
    return bool(_QUANTITY_SEEKING.search(question))


def has_quantitative_content(p):
    return p.get("quantity_key") is not None or bool(re.search(r"Values:[^\n]*\d", p["text"]))


def tokenize(text):
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())


def detect_jurisdictions(question):
    toks = set(re.findall(r"[a-z\-]+", question.lower()))
    return sorted({code for name, code in JURISDICTION_NAMES.items() if name in toks})


def detect_source_scope(con, question):
    ql = question.lower()
    found = []
    for r in con.execute("SELECT source_id, aliases_json FROM sources WHERE state='ACTIVE'").fetchall():
        for a in json.loads(r["aliases_json"] or "[]"):
            if re.search(r"(?<![a-z0-9])" + re.escape(a.lower()) + r"(?![a-z0-9])", ql):
                found.append(r["source_id"])
                break
    return found


def content_terms(question, drop):
    out = []
    for t in tokenize(question):
        if t in STOPWORDS or t in drop or len(t) < 2 or any(ch.isdigit() for ch in t):
            continue
        if t not in out:
            out.append(t)
    return out


def _fts_quote(term):
    return '"' + term.replace('"', '""') + '"'


def _year(d):
    m = re.match(r"(\d{4})", d or "")
    return int(m.group(1)) if m else None


def _row_passage(row, src, cov, matched, bm25, relation):
    return {
        "chunk_id": row["chunk_id"], "source_id": row["source_id"], "title": src["title"], "url": src["url"],
        "doi": src["doi"], "locator": json.loads(row["locator_json"]), "text": row["text"], "quote": row["quote"],
        "chunk_hash": row["chunk_hash"], "source_content_hash": src["content_hash"],
        "scores": {"term_coverage": round(cov, 3), "bm25": round(-bm25, 4) if bm25 is not None else None},
        "matched_terms": matched, "jurisdiction": row["jurisdiction"], "jurisdiction_relation": relation,
        "applicability_class": row["applicability_class"], "scope": json.loads(row["scope_json"] or "{}"),
        "published": src["published"], "version": src["version"], "verification_status": src["verification_status"],
        "human_verified": src["verification_status"] == "HUMAN_VERIFIED", "reuse_status": src["reuse_status"],
        "topics": json.loads(row["topics_json"] or "[]"), "quantity_key": row["quantity_key"],
        "source_limitations": src["limitations"], "applicability_note": src["applicability_note"],
        "meta": json.loads(row["meta_json"] or "{}"),
    }


def detect_conflicts(passages):
    """Same quantity_key, different sources, disjoint ranges (or unit mismatch), no declared priority rule."""
    out, seen = [], set()
    by_key = {}
    for p in passages:
        if p.get("quantity_key"):
            by_key.setdefault(p["quantity_key"], []).append(p)
    for key, ps in by_key.items():
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                a, b = ps[i], ps[j]
                if a["source_id"] == b["source_id"]:
                    continue
                ra, rb = a["_range"], b["_range"]
                if ra[2] != rb[2]:
                    kind = "UNIT_MISMATCH"
                elif ra[1] < rb[0] or rb[1] < ra[0]:
                    kind = "DISJOINT_VALUES"
                else:
                    continue
                pair = tuple(sorted((a["chunk_id"], b["chunk_id"])))
                if pair in seen:
                    continue
                seen.add(pair)
                out.append({"quantity_key": key, "kind": kind, "chunk_ids": list(pair),
                            "values": {a["chunk_id"]: {"min": ra[0], "max": ra[1], "unit": ra[2]},
                                       b["chunk_id"]: {"min": rb[0], "max": rb[1], "unit": rb[2]}},
                            "resolution": "UNRESOLVED: no declared priority rule between these sources"})
    return out


def retrieve(con, question, filters=None, top_k=5, strategy="strict"):
    f = dict(filters or {})
    t0_filters = dict(f)
    result = {"question": question, "strategy": strategy, "filters_requested": t0_filters, "top_k": top_k,
              "passages": [], "transfer_context": [], "conflicts": [], "excluded": {}, "status": None,
              "reason": None, "terms": [], "min_term_coverage": STRATEGIES[strategy]}

    n_active = con.execute("SELECT COUNT(*) FROM chunks WHERE state='ACTIVE'").fetchone()[0]
    if n_active == 0:
        result.update(status="INSUFFICIENT_EVIDENCE", reason="EMPTY_INDEX")
        return result

    target = f.get("jurisdictions") or detect_jurisdictions(question)
    strict_juris = bool(f.get("jurisdictions"))
    scope_ids = f.get("source_ids") or detect_source_scope(con, question)
    result["target_jurisdictions"] = target
    result["source_scope"] = scope_ids

    drop = set()
    for name in JURISDICTION_NAMES:
        drop.update(name.replace("-", " ").split())
        drop.add(name)
    for r in con.execute("SELECT aliases_json FROM sources WHERE state='ACTIVE'").fetchall():
        for a in json.loads(r["aliases_json"] or "[]"):
            drop.update(tokenize(a))
    terms = content_terms(question, drop)
    result["terms"] = terms
    if len(terms) < 2:
        result.update(status="INSUFFICIENT_EVIDENCE", reason="TOO_FEW_CONTENT_TERMS")
        return result

    # term -> set of chunk_ids using the same porter tokenizer as the index
    term_hits = {}
    for t in terms:
        rows = con.execute("SELECT chunk_id FROM chunks_fts WHERE chunks_fts MATCH ?", (_fts_quote(t),)).fetchall()
        term_hits[t] = {r["chunk_id"] for r in rows}
    bm25 = {r["chunk_id"]: r["s"] for r in con.execute(
        "SELECT chunk_id, bm25(chunks_fts) AS s FROM chunks_fts WHERE chunks_fts MATCH ?",
        (" OR ".join(_fts_quote(t) for t in terms),)).fetchall()}

    min_cov = STRATEGIES[strategy]
    excluded = {}

    def exc(reason):
        excluded[reason] = excluded.get(reason, 0) + 1

    cands = []
    for cid in bm25:
        matched = [t for t in terms if cid in term_hits[t]]
        cov = len(matched) / len(terms)
        row = con.execute("SELECT * FROM chunks WHERE chunk_id=? AND state='ACTIVE'", (cid,)).fetchone()
        src = con.execute("SELECT * FROM sources WHERE source_id=? AND state='ACTIVE'", (row["source_id"],)).fetchone() if row else None
        if not row or not src:
            exc("NOT_ACTIVE")
            continue
        # metadata filters (applied before relevance counts)
        if scope_ids and src["source_id"] not in scope_ids:
            exc("OUTSIDE_SOURCE_SCOPE"); continue
        if strict_juris and src["jurisdiction"] not in f["jurisdictions"]:
            exc("FILTER_JURISDICTION"); continue
        if f.get("verification_statuses") and src["verification_status"] not in f["verification_statuses"]:
            exc("FILTER_VERIFICATION_STATUS"); continue
        if f.get("topics") and not set(f["topics"]) & set(json.loads(row["topics_json"] or "[]")):
            exc("FILTER_TOPIC"); continue
        if f.get("min_year") or f.get("max_year"):
            y = _year(src["published"])
            if y is None:
                exc("FILTER_DATE_UNKNOWN_PUBLICATION_DATE"); continue
            if (f.get("min_year") and y < int(f["min_year"])) or (f.get("max_year") and y > int(f["max_year"])):
                exc("FILTER_PUBLICATION_PERIOD"); continue
        if src["superseded_by"] and not f.get("include_superseded"):
            exc("SUPERSEDED_SOURCE"); continue
        if not source_is_current(con, src["source_id"]):
            exc("SOURCE_CHANGED_SINCE_INGEST"); continue
        if cov < min_cov or len(matched) < 2:
            exc("BELOW_TERM_COVERAGE_THRESHOLD"); continue
        cands.append((cov, bm25[cid], row, src, matched))

    cands.sort(key=lambda x: (-x[0], x[1], x[2]["chunk_id"]))  # bm25 is lower-is-better
    seeks_number = is_quantity_seeking(question)
    result["quantity_seeking"] = seeks_number
    support, transfer = [], []
    for cov, s, row, src, matched in cands:
        if not target:
            relation = "NO_TARGET"
        elif row["jurisdiction"] in target:
            relation = "MATCH"
        elif row["applicability_class"] == "GENERAL_PRINCIPLE" and not seeks_number:
            relation = "GENERAL_PRINCIPLE"
        else:
            relation = "TRANSFER_ONLY"
        p = _row_passage(row, src, cov, matched, s, relation)
        if row["quantity_key"] is not None and row["qmin"] is not None:
            p["_range"] = (row["qmin"], row["qmax"], row["qunit"])
        (transfer if relation == "TRANSFER_ONLY" else support).append(p)

    support, transfer = support[:top_k], transfer[:top_k]
    context_only = []
    if seeks_number and support and not any(has_quantitative_content(p) for p in support):
        context_only, support = support, []  # relevant words, but no value to support a numerical answer
    conflicts = detect_conflicts([p for p in support if "_range" in p])
    for p in support + transfer:
        p.pop("_range", None)
    result.update(passages=support, transfer_context=transfer, conflicts=conflicts, excluded=excluded,
                  non_supporting_context=context_only)
    if context_only:
        result.update(status="INSUFFICIENT_EVIDENCE", reason="REQUIRED_NUMERICAL_VALUE_ABSENT_IN_ELIGIBLE_PASSAGES")
    elif conflicts:
        result.update(status="CONFLICT_UNRESOLVED", reason="CONTRADICTORY_SOURCES_NO_PRIORITY_RULE")
    elif support:
        result.update(status="OK", reason=None)
    elif transfer:
        result.update(status="INSUFFICIENT_EVIDENCE",
                      reason="ONLY_OTHER_JURISDICTION_EVIDENCE_FOR_TARGET:" + ",".join(target))
    else:
        result.update(status="INSUFFICIENT_EVIDENCE", reason="NO_ELIGIBLE_PASSAGE_MEETS_THRESHOLD")
    return result

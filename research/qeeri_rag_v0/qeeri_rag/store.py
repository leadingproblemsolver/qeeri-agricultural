"""SQLite/FTS5 evidence store: allowlisted ingestion, hashing, verification, citation resolution.

Stdlib only. Nothing is fetched from the network. Only sources listed in an allowlist file,
whose verification and reuse status are eligible, enter the authoritative (ACTIVE) index.
Everything else is recorded as REJECTED/QUARANTINED in the ingestion log with its reason.
"""
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources(
  source_id TEXT PRIMARY KEY, title TEXT, url TEXT, doi TEXT, published TEXT, version TEXT,
  jurisdiction TEXT, verification_status TEXT, reuse_status TEXT, content_hash TEXT,
  path TEXT, format TEXT, aliases_json TEXT, limitations TEXT, applicability_note TEXT,
  superseded_by TEXT, state TEXT, state_reason TEXT, ingested_at TEXT);
CREATE TABLE IF NOT EXISTS chunks(
  chunk_id TEXT PRIMARY KEY, source_id TEXT, label TEXT, ordinal INTEGER, locator_json TEXT,
  text TEXT, quote TEXT, chunk_hash TEXT, topics_json TEXT, quantity_key TEXT, qmin REAL,
  qmax REAL, qunit TEXT, jurisdiction TEXT, applicability_class TEXT, scope_json TEXT,
  meta_json TEXT, state TEXT, state_reason TEXT, ingested_at TEXT);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(chunk_id UNINDEXED, body, tokenize='porter unicode61');
CREATE TABLE IF NOT EXISTS ingestion_log(
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, source_id TEXT, outcome TEXT, detail_json TEXT);
"""

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+|any\s+|the\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?)",
    r"disregard\s+.{0,40}(instructions?|rules?|prompt)",
    r"(you\s+are\s+now|from\s+now\s+on\s+you)\b",
    r"(reveal|print|output|show)\s+.{0,30}(system\s+prompt|api[\s_-]?key|secret|password)",
    r"<\s*/?\s*(system|assistant|instructions?)\s*>",
    r"\b(system|assistant)\s*:",
    r"(approve|mark|label)\s+(this|the|your)\s+(answer|claim|response)\s+as\s+(correct|verified|supported)",
    r"override\s+.{0,30}(instructions?|rules?|safety)",
]
_INJ = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)

DEFAULT_ELIGIBLE_VERIFICATION = {"HUMAN_VERIFIED", "SOURCE_TEXT_READ", "PACKET_ASSERTED"}
DEFAULT_ELIGIBLE_REUSE = {"PERMITTED_EXPORT", "LOCAL_ONLY"}


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(t):
    return sha256_bytes(t.encode("utf-8"))


def scan_injection(text):
    m = _INJ.search(text or "")
    return m.group(0) if m else None


def connect(db_path):
    if str(db_path) != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def compute_chunk_hash(source_id, label, locator, text):
    canon = json.dumps({"source_id": source_id, "label": label, "locator": locator, "text": text},
                       sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256_text(canon)


def make_chunk_id(source_id, label, chunk_hash):
    return f"{source_id}#{label}@{chunk_hash[:12]}"


# ---------------------------------------------------------------- loaders (raw file -> chunk dicts)

def _load_packet_markdown(path):
    """Chunks = '### <label> — <heading>' sections. Locator is the heading text only; no page invented."""
    text = Path(path).read_text(encoding="utf-8")
    parts = re.split(r"^### ", text, flags=re.M)[1:]
    chunks = []
    for ordinal, part in enumerate(parts):
        head, _, body = part.partition("\n")
        # stop at the next '## ' section (boundary notes are source-level metadata, not evidence chunks)
        body = re.split(r"^## ", body, flags=re.M)[0].strip()
        m = re.match(r"(S\d+)\s*[—-]\s*(.+)", head.strip())
        if not m:
            continue
        label, heading = m.group(1), m.group(2).strip()
        quotes = re.findall(r'\*\*"(.+?)"\*\*', body)
        chunks.append({
            "label": label, "ordinal": ordinal, "text": body,
            "quote": quotes[0] if quotes else None,
            "locator": {"section": heading, "page": None, "table_figure": None,
                        "note": "section heading as written in the packet; page not recorded"},
            "scope": {"note": "see source-level applicability_note"},
            "meta": {},
        })
    return chunks


def _load_ledger_json(path, ledger_source_id):
    """Chunks = ledger claims for one source. Text = claim + values + relayed excerpt, verbatim from the ledger."""
    ledger = json.loads(Path(path).read_text(encoding="utf-8"))
    chunks = []
    for ordinal, c in enumerate(x for x in ledger["claims"] if x["source_id"] == ledger_source_id):
        vals = "; ".join(f"{v['quantity']} = {v['value']} {v['unit']}" for v in c.get("values", []))
        text = c["claim"] + (f"\nValues: {vals}" if vals else "")
        loc = {k: c["locator"].get(k) for k in ("section", "table_figure", "page")}
        loc["page_confidence"] = c["locator"].get("page_confidence")
        chunks.append({
            "label": c["claim_id"], "ordinal": ordinal, "text": text,
            "quote": c.get("excerpt_relayed"), "locator": loc, "scope": c.get("scope", {}),
            "meta": {"evidence_class": c.get("evidence_class"), "underlying_basis": c.get("underlying_basis"),
                     "applicability": c.get("applicability"), "limitations": c.get("limitations"),
                     "ledger_status": c.get("status"), "ledger_human_verified": c.get("human_verified")},
        })
    return chunks


def _ledger_source_meta(path, ledger_source_id):
    ledger = json.loads(Path(path).read_text(encoding="utf-8"))
    for s in ledger["sources"]:
        if s["source_id"] == ledger_source_id:
            return s
    return {}


def load_source(entry, base_dir):
    path = (Path(base_dir) / entry["path"]).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"source file missing: {path}")
    raw = path.read_bytes()
    fmt = entry["format"]
    if fmt == "packet_markdown":
        chunks = _load_packet_markdown(path)
        meta = {}
    elif fmt == "ledger_json":
        chunks = _load_ledger_json(path, entry["ledger_source_id"])
        meta = _ledger_source_meta(path, entry["ledger_source_id"])
    elif fmt in ("markdown", "text"):
        body = raw.decode("utf-8")
        paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        chunks = [{"label": f"P{i+1:03d}", "ordinal": i, "text": p, "quote": None,
                   "locator": {"section": f"paragraph {i+1}", "page": None, "table_figure": None},
                   "scope": {}, "meta": {}} for i, p in enumerate(paras)]
        meta = {}
    else:
        raise ValueError(f"unsupported format: {fmt}")
    return str(path), sha256_bytes(raw), chunks, meta


# ---------------------------------------------------------------- ingestion

REQUIRED_ENTRY_FIELDS = ("source_id", "format", "path", "jurisdiction", "verification_status", "reuse_status")


def validate_entry(entry):
    miss = [f for f in REQUIRED_ENTRY_FIELDS if not entry.get(f)]
    return [f"missing field: {f}" for f in miss]


def _log(con, source_id, outcome, detail):
    con.execute("INSERT INTO ingestion_log(ts,source_id,outcome,detail_json) VALUES (?,?,?,?)",
                (now_utc(), source_id, outcome, json.dumps(detail, ensure_ascii=False)))


REPO_ROOT = Path(__file__).resolve().parents[3]


def _default_source_root(allow_path):
    """Sources must live under the repo when the allowlist is in the repo, else under the allowlist's own directory."""
    try:
        allow_path.relative_to(REPO_ROOT)
        return REPO_ROOT
    except ValueError:
        return allow_path.parent


def _review_record_ok(entry):
    rr = entry.get("review_record")
    return isinstance(rr, dict) and all(rr.get(k) for k in ("reviewer", "reviewed_at", "record_path")) \
        and rr.get("reviewer") != entry.get("curator")


def ingest(con, allowlist_path, source_root=None):
    """Ingest every allowlisted source. Returns a receipt dict. Idempotent for unchanged files."""
    allow_path = Path(allowlist_path).resolve()
    root = Path(source_root).resolve() if source_root else _default_source_root(allow_path)
    try:
        allow = json.loads(allow_path.read_text(encoding="utf-8"))
        entries = allow["sources"]
        assert isinstance(entries, list)
    except Exception as e:  # malformed allowlist: fail closed, ingest nothing
        return {"status": "FAILED", "reason": f"MALFORMED_ALLOWLIST: {type(e).__name__}: {e}", "sources": []}
    elig_v = set(allow.get("eligible_verification_statuses", DEFAULT_ELIGIBLE_VERIFICATION))
    elig_r = set(allow.get("eligible_reuse_statuses", DEFAULT_ELIGIBLE_REUSE))
    receipt = {"allowlist": str(allow_path), "allowlist_sha256": sha256_bytes(allow_path.read_bytes()),
               "ingested_at": now_utc(), "sources": []}
    for entry in entries:
        sid = entry.get("source_id", "<missing>") if isinstance(entry, dict) else "<non-object-entry>"
        rec = {"source_id": sid}
        errs = validate_entry(entry) if isinstance(entry, dict) else ["entry is not an object"]
        if errs:
            rec.update(outcome="REJECTED", reason="MALFORMED_ENTRY", detail=errs)
        elif entry["verification_status"] == "HUMAN_VERIFIED" and not _review_record_ok(entry):
            rec.update(outcome="REJECTED", reason="HUMAN_VERIFIED_WITHOUT_INDEPENDENT_REVIEW_RECORD",
                       detail="needs review_record{reviewer,reviewed_at,record_path}, reviewer != curator")
        elif entry["verification_status"] not in elig_v:
            rec.update(outcome="REJECTED", reason="VERIFICATION_STATUS_NOT_ELIGIBLE",
                       detail=entry["verification_status"])
        elif entry["reuse_status"] not in elig_r:
            rec.update(outcome="REJECTED", reason="REUSE_STATUS_NOT_ELIGIBLE_FAIL_CLOSED",
                       detail=entry["reuse_status"])
        else:
            try:
                rec.update(_ingest_one(con, entry, allow_path.parent, root))
            except (FileNotFoundError, ValueError, KeyError, json.JSONDecodeError, UnicodeDecodeError) as e:
                rec.update(outcome="REJECTED", reason="MALFORMED_OR_MISSING_SOURCE",
                           detail=f"{type(e).__name__}: {e}")
        if rec["outcome"] == "REJECTED":
            _log(con, sid, "REJECTED", {"reason": rec["reason"], "detail": rec.get("detail")})
            # a previously ACTIVE source that becomes ineligible must leave the authoritative index
            _deactivate_source(con, sid, rec["reason"])
        receipt["sources"].append(rec)
    con.commit()
    receipt["status"] = "OK"
    return receipt


def _deactivate_source(con, sid, reason):
    rows = con.execute("SELECT chunk_id FROM chunks WHERE source_id=? AND state='ACTIVE'", (sid,)).fetchall()
    for r in rows:
        con.execute("DELETE FROM chunks_fts WHERE chunk_id=?", (r["chunk_id"],))
    con.execute("UPDATE chunks SET state='SUPERSEDED_BY_REINGEST', state_reason=? WHERE source_id=? AND state='ACTIVE'",
                (f"source became ineligible: {reason}", sid))
    con.execute("UPDATE sources SET state='REJECTED', state_reason=? WHERE source_id=?", (reason, sid))


def _ingest_one(con, entry, base_dir, root):
    sid = entry["source_id"]
    resolved = (Path(base_dir) / entry["path"]).resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ValueError(f"source path escapes the permitted root {root}: {resolved}")
    path, content_hash, raw_chunks, ledger_meta = load_source(entry, base_dir)
    prev = con.execute("SELECT content_hash, state FROM sources WHERE source_id=?", (sid,)).fetchone()
    if prev and prev["content_hash"] == content_hash and prev["state"] == "ACTIVE":
        _log(con, sid, "UNCHANGED", {"content_hash": content_hash})
        n = con.execute("SELECT COUNT(*) FROM chunks WHERE source_id=? AND state='ACTIVE'", (sid,)).fetchone()[0]
        return {"outcome": "UNCHANGED", "content_hash": content_hash, "active_chunks": n}

    title = entry.get("title") or ledger_meta.get("citation") or sid
    url = entry.get("url") or ledger_meta.get("url_used")
    doi = entry.get("doi") if "doi" in entry else ledger_meta.get("doi")
    ts = now_utc()
    # re-ingest of a changed file: retire every old chunk of this source; ids derive from content so
    # any citation to an old id will no longer resolve as ACTIVE.
    if prev:
        for r in con.execute("SELECT chunk_id FROM chunks WHERE source_id=? AND state='ACTIVE'", (sid,)).fetchall():
            con.execute("DELETE FROM chunks_fts WHERE chunk_id=?", (r["chunk_id"],))
        con.execute("UPDATE chunks SET state='SUPERSEDED_BY_REINGEST', state_reason='source content changed' "
                    "WHERE source_id=? AND state='ACTIVE'", (sid,))
    con.execute("INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        sid, title, url, doi, entry.get("published"), entry.get("version"), entry["jurisdiction"],
        entry["verification_status"], entry["reuse_status"], content_hash, path, entry["format"],
        json.dumps(entry.get("aliases", [])), entry.get("limitations"), entry.get("applicability_note"),
        entry.get("superseded_by"), "ACTIVE", None, ts))

    overrides = entry.get("chunk_overrides", {})
    active, quarantined = [], []
    for c in raw_chunks:
        ov = overrides.get(c["label"], {})
        chash = compute_chunk_hash(sid, c["label"], c["locator"], c["text"])
        cid = make_chunk_id(sid, c["label"], chash)
        hit = scan_injection(c["text"])
        state, reason = ("QUARANTINED", f"PROMPT_INJECTION_PATTERN: {hit!r}") if hit else ("ACTIVE", None)
        topics = ov.get("topics", entry.get("default_topics", []))
        con.execute("INSERT OR REPLACE INTO chunks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            cid, sid, c["label"], c["ordinal"], json.dumps(c["locator"], ensure_ascii=False), c["text"],
            c.get("quote"), chash, json.dumps(topics), ov.get("quantity_key"), ov.get("qmin"), ov.get("qmax"),
            ov.get("qunit"), entry["jurisdiction"], ov.get("applicability", entry.get("default_applicability",
            "JURISDICTION_SPECIFIC")), json.dumps(c.get("scope", {}), ensure_ascii=False),
            json.dumps(c.get("meta", {}), ensure_ascii=False), state, reason, ts))
        if state == "ACTIVE":
            con.execute("DELETE FROM chunks_fts WHERE chunk_id=?", (cid,))
            con.execute("INSERT INTO chunks_fts(chunk_id, body) VALUES (?,?)", (cid, c["text"]))
            active.append(cid)
        else:
            quarantined.append({"chunk_id": cid, "reason": reason})
    _log(con, sid, "INGESTED" if not prev else "REINGESTED_CONTENT_CHANGED",
         {"content_hash": content_hash, "active": len(active), "quarantined": quarantined})
    return {"outcome": "INGESTED" if not prev else "REINGESTED_CONTENT_CHANGED", "content_hash": content_hash,
            "active_chunks": len(active), "quarantined_chunks": quarantined, "chunk_ids": active}


# ---------------------------------------------------------------- verification & citation resolution

def verify_index(con):
    """Recompute source-file and chunk hashes. Never trusts stored values alone."""
    problems, checked_chunks, checked_sources = [], 0, 0
    for s in con.execute("SELECT * FROM sources WHERE state='ACTIVE'").fetchall():
        checked_sources += 1
        p = Path(s["path"])
        if not p.is_file():
            problems.append({"source_id": s["source_id"], "problem": "SOURCE_FILE_MISSING"})
        elif sha256_bytes(p.read_bytes()) != s["content_hash"]:
            problems.append({"source_id": s["source_id"], "problem": "SOURCE_FILE_CHANGED_SINCE_INGEST",
                             "action": "re-run ingest; old chunk ids will be superseded"})
    for c in con.execute("SELECT * FROM chunks WHERE state='ACTIVE'").fetchall():
        checked_chunks += 1
        h = compute_chunk_hash(c["source_id"], c["label"], json.loads(c["locator_json"]), c["text"])
        if h != c["chunk_hash"] or not c["chunk_id"].endswith("@" + h[:12]):
            problems.append({"chunk_id": c["chunk_id"], "problem": "CHUNK_HASH_MISMATCH_TAMPERED_STORE"})
    return {"valid": not problems, "sources_checked": checked_sources, "chunks_checked": checked_chunks,
            "problems": problems}


def source_is_current(con, source_id):
    s = con.execute("SELECT path, content_hash FROM sources WHERE source_id=?", (source_id,)).fetchone()
    if not s:
        return False
    p = Path(s["path"])
    return p.is_file() and sha256_bytes(p.read_bytes()) == s["content_hash"]


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def resolve_citation(con, citation):
    """A citation resolves only if chunk id, source, hashes and (optional) quote all check out."""
    cid = citation.get("chunk_id")
    row = con.execute("SELECT * FROM chunks WHERE chunk_id=?", (cid,)).fetchone() if cid else None
    if not row:
        return {"resolved": False, "reason": "CHUNK_ID_NOT_FOUND", "chunk_id": cid}
    if row["state"] != "ACTIVE":
        return {"resolved": False, "reason": f"CHUNK_NOT_ACTIVE:{row['state']}", "chunk_id": cid}
    if citation.get("source_id") and citation["source_id"] != row["source_id"]:
        return {"resolved": False, "reason": "SOURCE_ID_DOES_NOT_MATCH_CHUNK", "chunk_id": cid}
    if citation.get("chunk_hash") and citation["chunk_hash"] != row["chunk_hash"]:
        return {"resolved": False, "reason": "CHUNK_HASH_MISMATCH", "chunk_id": cid}
    if compute_chunk_hash(row["source_id"], row["label"], json.loads(row["locator_json"]), row["text"]) != row["chunk_hash"]:
        return {"resolved": False, "reason": "STORED_CHUNK_FAILS_REHASH", "chunk_id": cid}
    if not source_is_current(con, row["source_id"]):
        return {"resolved": False, "reason": "SOURCE_FILE_CHANGED_SINCE_INGEST", "chunk_id": cid}
    q = citation.get("quote")
    if q and _norm(q) not in _norm(row["text"]) and _norm(q) != _norm(row["quote"]):
        return {"resolved": False, "reason": "QUOTE_NOT_FOUND_IN_CHUNK", "chunk_id": cid}
    return {"resolved": True, "chunk_id": cid, "source_id": row["source_id"], "chunk_hash": row["chunk_hash"],
            "locator": json.loads(row["locator_json"])}


def snapshot_hash(con):
    """Hash of the ACTIVE index content: used as the 'source snapshot hash' in evaluation receipts."""
    rows = con.execute("SELECT chunk_hash FROM chunks WHERE state='ACTIVE' ORDER BY chunk_id").fetchall()
    return sha256_text("\n".join(r["chunk_hash"] for r in rows))


def health(con):
    n_src = con.execute("SELECT COUNT(*) FROM sources WHERE state='ACTIVE'").fetchone()[0]
    n_chunks = con.execute("SELECT COUNT(*) FROM chunks WHERE state='ACTIVE'").fetchone()[0]
    quarantined = con.execute("SELECT COUNT(*) FROM chunks WHERE state='QUARANTINED'").fetchone()[0]
    # latest ingestion outcome per source id; sources rejected before insertion exist only in the log
    rejected = []
    for r in con.execute("SELECT source_id, outcome, detail_json, MAX(id) FROM ingestion_log GROUP BY source_id").fetchall():
        if r["outcome"] == "REJECTED":
            rejected.append({"source_id": r["source_id"], "reason": json.loads(r["detail_json"]).get("reason")})
    v = verify_index(con)
    status = "EMPTY_INDEX" if n_chunks == 0 else ("OK" if v["valid"] else "DEGRADED")
    return {"status": status, "active_sources": n_src, "active_chunks": n_chunks, "quarantined_chunks": quarantined,
            "rejected_sources": rejected, "snapshot_sha256": snapshot_hash(con), "verify": v}


def export_public(con, out_path):
    """Public export fails closed: only PERMITTED_EXPORT sources. LOCAL_ONLY/UNKNOWN are never exported."""
    rows = con.execute("""SELECT c.chunk_id, c.text, c.chunk_hash, s.source_id, s.url, s.reuse_status
        FROM chunks c JOIN sources s ON s.source_id=c.source_id
        WHERE c.state='ACTIVE' AND s.state='ACTIVE' AND s.reuse_status='PERMITTED_EXPORT'""").fetchall()
    skipped = con.execute("""SELECT COUNT(*) FROM chunks c JOIN sources s ON s.source_id=c.source_id
        WHERE c.state='ACTIVE' AND s.reuse_status!='PERMITTED_EXPORT'""").fetchone()[0]
    Path(out_path).write_text(json.dumps([dict(r) for r in rows], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"exported_chunks": len(rows), "withheld_not_permitted_for_export": skipped}

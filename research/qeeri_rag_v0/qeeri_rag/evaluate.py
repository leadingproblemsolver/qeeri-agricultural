"""Three-condition evaluation harness.

  A: no supplied research documents (same frozen instructions, empty passage block)
  B: fixed approved source packet = every ACTIVE chunk
  C: retrieval-selected passages, behind the deterministic admissibility loop

Deterministic part (always executed, needs no key): arm C retrieval/abstention/citation metrics on the gold set.
Model part (executed only if ANTHROPIC_API_KEY is set): identical question, instructions and model settings for
A, B, C; exact request bodies, raw responses, usage, latency and snapshot hashes are stored. Without a key each model
arm is recorded NOT_EXECUTED and nothing is synthesised.

These conditions are NOT comparable to the historical ChatGPT Test A/B transcripts (different vendor, protocol and
contamination), and human claim-level correctness is always PENDING_REVIEW.
"""
import json
import time
from pathlib import Path

from .answer import ClaudeProvider, ExtractiveProvider, frozen_instructions, DEFAULT_MODEL
from .guards import validate_claims
from .loop import LoopConfig, run_question
from .retrieve import _row_passage, retrieve
from .store import now_utc, resolve_citation, sha256_text, snapshot_hash


def all_passages(con):
    out = []
    for row in con.execute("SELECT * FROM chunks WHERE state='ACTIVE' ORDER BY chunk_id").fetchall():
        src = con.execute("SELECT * FROM sources WHERE source_id=?", (row["source_id"],)).fetchone()
        out.append(_row_passage(row, src, 1.0, [], None, "NO_TARGET"))
    return out


def _arm_c_metrics(con, q, res):
    cited = [cid for c in res["claims"] if c["status"] == "SUPPORTED_CANDIDATE" for cid in c["chunk_ids"]]
    prefixes = lambda ids: {i.split("@")[0] for i in ids}
    gold = set(q["gold_chunks"])
    retrieved = prefixes([p["chunk_id"] for p in (res["retrieval"] or {}).get("passages", [])]) if res["retrieval"] else set()
    answered = res["status"] == "SUPPORTED_CANDIDATE"
    resolved = [resolve_citation(con, {"chunk_id": cid})["resolved"] for cid in cited]
    m = {"id": q["id"], "type": q["type"], "expected": q["expected"], "status": res["status"], "reason": res["reason"],
         "answered": answered, "retrieved": sorted(retrieved), "cited": sorted(prefixes(cited)),
         "latency_ms": res["loop"]["latency_ms"], "retrieval_attempts": res["loop"]["retrieval_attempts"],
         "citations_total": len(cited), "citations_resolved": sum(resolved)}
    if q["expected"] == "ANSWER":
        m["hit_at_k"] = bool(gold & retrieved)
        m["precision_at_k"] = round(len(gold & retrieved) / len(retrieved), 3) if retrieved else 0.0
        m["recall_at_k"] = round(len(gold & retrieved) / len(gold), 3) if gold else None
        m["over_abstention"] = not answered
        m["answered_with_gold_citation"] = bool(gold & prefixes(cited))
    else:
        m["false_support"] = answered  # produced a supported-candidate answer where abstention was expected
        m["correct_abstention"] = not answered
    return m


def _summarise(rows):
    pos = [r for r in rows if r["expected"] == "ANSWER"]
    neg = [r for r in rows if r["expected"] == "ABSTAIN"]
    tot_c = sum(r["citations_total"] for r in rows)
    lat = sorted(r["latency_ms"] for r in rows)
    return {
        "positives": len(pos), "negatives": len(neg),
        "retrieval_hit_rate_at_k": round(sum(r["hit_at_k"] for r in pos) / len(pos), 3) if pos else None,
        "retrieval_miss_rate": round(sum(not r["hit_at_k"] for r in pos) / len(pos), 3) if pos else None,
        "mean_precision_at_k": round(sum(r["precision_at_k"] for r in pos) / len(pos), 3) if pos else None,
        "mean_recall_at_k": round(sum(r["recall_at_k"] for r in pos) / len(pos), 3) if pos else None,
        "over_abstention_rate": round(sum(r["over_abstention"] for r in pos) / len(pos), 3) if pos else None,
        "false_support_rate": round(sum(r["false_support"] for r in neg) / len(neg), 3) if neg else None,
        "correct_abstention_rate": round(sum(r["correct_abstention"] for r in neg) / len(neg), 3) if neg else None,
        "citation_resolution_rate": round(sum(r["citations_resolved"] for r in rows) / tot_c, 3) if tot_c else None,
        "answered_with_citation_coverage": round(sum(1 for r in pos if r["answered"] and r["citations_total"] > 0) /
                                                 max(1, sum(1 for r in pos if r["answered"])), 3),
        "latency_ms_median": lat[len(lat) // 2], "latency_ms_max": lat[-1],
    }


def run_eval(con, questions_path, out_path=None, model=DEFAULT_MODEL, api_key=None, api_url=None, cfg=None,
             run_models=True):
    qdoc = json.loads(Path(questions_path).read_text(encoding="utf-8"))
    qs = qdoc["questions"]
    cfg = cfg or LoopConfig(receipts_dir="runs/eval_receipts")
    instr, instr_hash = frozen_instructions()
    snap = snapshot_hash(con)
    pkt = all_passages(con)
    kw = {"model": model}
    if api_url:
        kw["api_url"] = api_url
    if api_key is not None:
        kw["api_key"] = api_key
    claude = ClaudeProvider(**kw)
    have_key = bool(claude._key) and run_models

    out = {"harness": "qeeri-rag-v0-eval", "run_started_utc": now_utc(), "question_set": qdoc["set_id"],
           "question_set_label": qdoc["label"], "question_set_sha256": sha256_text(json.dumps(qs, sort_keys=True)),
           "index_snapshot_sha256": snap, "instructions_sha256": instr_hash,
           "model_settings": {"model": model, "temperature": claude.temperature, "max_tokens": claude.max_tokens,
                              "tools": "none", "same_for_all_arms": True},
           "comparability_warning": ("Not comparable to the historical ChatGPT Test A/B transcripts; do not treat as a "
                                     "controlled replication of them."),
           "human_claim_correctness": "PENDING_REVIEW (no independent human scoring exists)"}

    # ---- arm C, deterministic retrieval layer (extractive provider, no key needed)
    rows = []
    for q in qs:
        res = run_question(con, q["question"], q.get("inputs"), q.get("filters"), ExtractiveProvider(), cfg)
        rows.append(_arm_c_metrics(con, q, res))
    out["arm_C_deterministic_retrieval"] = {"status": "EXECUTED", "per_question": rows, "summary": _summarise(rows)}

    # ---- fixed packet comparator facts (structural, no model involved)
    packet_chars = sum(len(p["text"]) for p in pkt)
    out["arm_B_fixed_packet_facts"] = {"status": "STRUCTURAL_ONLY", "chunks": len(pkt), "packet_chars": packet_chars,
                                       "contains_all_gold_chunks": all(
                                           g in {p["chunk_id"].split("@")[0] for p in pkt}
                                           for q in qs for g in q["gold_chunks"]),
                                       "has_deterministic_abstention_gate": False}

    # ---- model arms
    arms = {"A": [], "B": [], "C": []}
    for q in qs:
        for arm in ("A", "B", "C"):
            entry = {"id": q["id"], "arm": arm}
            if arm == "C":
                det = next(r for r in rows if r["id"] == q["id"])
                if det["status"] == "INSUFFICIENT_EVIDENCE":
                    entry.update(status="ABSTAINED_BY_RETRIEVAL_GATE_NO_MODEL_CALL", reason=det["reason"])
                    arms[arm].append(entry)
                    continue
                ret = retrieve(con, q["question"], q.get("filters"), cfg.top_k, "strict")
                passages = ret["passages"]
            elif arm == "B":
                passages = pkt
            else:
                passages = []
            body = claude.request_body(q["question"], passages, q.get("inputs"))
            entry["input_request_body"] = body
            entry["input_sha256"] = sha256_text(json.dumps(body, sort_keys=True))
            entry["passage_chunk_ids"] = [p["chunk_id"] for p in passages]
            if not have_key:
                entry.update(status="NOT_EXECUTED", reason="ANTHROPIC_API_KEY not set (or run_models=False); no model was called.")
                arms[arm].append(entry)
                continue
            t0 = time.perf_counter()
            gen = claude.generate(q["question"], passages, q.get("inputs"))
            entry["run_timestamp_utc"] = now_utc()
            entry["wall_ms"] = round((time.perf_counter() - t0) * 1000, 1)
            entry["provider_status"] = gen["provider_status"]
            entry["execution"] = gen.get("execution")
            if gen["provider_status"] != "EXECUTED":
                entry.update(status=gen["provider_status"], reason=gen.get("reason"))
            else:
                checked = validate_claims(con, gen["claims"], passages, q.get("inputs"))
                entry.update(status="EXECUTED", abstained=bool(gen.get("abstain")), claims=checked,
                             unsupported_claims=sum(c["status"] == "UNSUPPORTED" for c in checked),
                             supported_candidate_claims=sum(c["status"] == "SUPPORTED_CANDIDATE" for c in checked),
                             human_correctness="PENDING_REVIEW")
            arms[arm].append(entry)
    out["model_arms"] = {k: {"status": ("EXECUTED" if have_key else "NOT_EXECUTED"), "per_question": v}
                         for k, v in arms.items()}
    out["retrieval_justification"] = _justify(out, have_key)
    out["run_finished_utc"] = now_utc()
    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        Path(out_path).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def _justify(out, have_key):
    s = out["arm_C_deterministic_retrieval"]["summary"]
    b = out["arm_B_fixed_packet_facts"]
    if not have_key:
        verdict = "NOT_ESTABLISHED_NO_GENERATION_COMPARISON"
        why = ("Model arms A/B/C were NOT_EXECUTED (no API key), so there is no observed consequential problem on which "
               "C outperformed B. Retrieval has therefore NOT justified its operational complexity.")
    else:
        verdict = "REQUIRES_HUMAN_SCORING"
        why = ("Model arms executed; whether C beats B on a consequential error requires independent human claim-level "
               "scoring, which is PENDING_REVIEW. Until then retrieval is not justified by evidence.")
    return {"verdict": verdict, "reason": why,
            "context": (f"The whole eligible corpus is {b['chunks']} chunks / {b['packet_chars']} characters and fits in a "
                        "fixed packet, so a retrieval stage is not needed for context-length reasons at this scale. "
                        "What the deterministic layer adds over a bare packet is auditable gating "
                        f"(false_support_rate={s['false_support_rate']}, correct_abstention_rate={s['correct_abstention_rate']} "
                        "on an engineer-authored 14-question set); that is an engineering property, not a scientific "
                        "benefit, and a packet plus the same deterministic guards could provide it without an index."),
            "pre_rag_gate_reference": "research/internship_five_week_review_2026-11-08/05_LLM_BENCHMARK_AND_PRE_RAG_GATE.md (pilot branch): NO-GO unless a retrieval-specific error is observed"}

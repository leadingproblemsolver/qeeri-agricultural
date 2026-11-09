"""Bounded, observable answer loop. Finite attempts, finite tool calls, no browsing, ends in a receipt.

Steps (numbering follows the engineering brief):
 1 receive question
 2 validate: index non-empty, sizing/spec guard, required inputs
 3 retrieve candidates (<= max_retrieval_attempts, strategies strict -> relaxed)
 4 reject ineligible / irrelevant / transfer-only / conflicting material (done inside retrieve + here)
 5 if insufficient: return what is missing, stop
 6 generate a provisional sourced answer if a provider is configured
 7 record claim -> chunk references and execution metadata
 8 deterministic claim checks; queue every claim for human review (none is ever human-verified here)
 9 stop with a receipt or an explicit failure state
"""
import json
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path

from .answer import citation_of, frozen_instructions, ExtractiveProvider
from .guards import check_sizing_request, validate_claims
from .retrieve import retrieve, STRATEGIES
from .store import now_utc, sha256_text, snapshot_hash, resolve_citation

VERSION = "qeeri-rag-v0"


@dataclass
class LoopConfig:
    max_retrieval_attempts: int = 1      # default 1: relaxed 2nd attempt measurably lowers precision (see README)
    max_tool_calls: int = 3              # retrieval calls + provider calls; hard stop
    top_k: int = 4
    strategies: tuple = ("strict", "relaxed")
    receipts_dir: str = "runs"


def _append_chained(path, record):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prev = "GENESIS"
    if path.exists():
        lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["receipt_sha256"]
    record = dict(record, prev_receipt_sha256=prev)
    record["receipt_sha256"] = sha256_text(json.dumps(record, sort_keys=True, ensure_ascii=False))
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record["receipt_sha256"]


def verify_receipts(path):
    """Tamper-evident against ordinary edits only; not a trusted immutable ledger."""
    prev, n = "GENESIS", 0
    p = Path(path)
    if not p.exists():
        return {"valid": True, "records": 0}
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        claimed = rec.pop("receipt_sha256")
        if rec.get("prev_receipt_sha256") != prev or sha256_text(json.dumps(rec, sort_keys=True, ensure_ascii=False)) != claimed:
            return {"valid": False, "records": n, "broken_at": n + 1}
        prev, n = claimed, n + 1
    return {"valid": True, "records": n}


def run_question(con, question, inputs=None, filters=None, provider=None, config=None):
    cfg = config or LoopConfig()
    provider = provider or ExtractiveProvider()
    t0 = time.perf_counter()
    answer_id = "ANS-" + uuid.uuid4().hex[:10]
    instr, instr_hash = frozen_instructions()
    meta = {"loop_version": VERSION, "config": asdict(cfg), "provider": getattr(provider, "name", "?"),
            "instructions_sha256": instr_hash, "index_snapshot_sha256": snapshot_hash(con),
            "retrieval_attempts": 0, "tool_calls": 0, "steps": []}
    result = {"answer_id": answer_id, "question": question, "created_at": now_utc(), "claims": [],
              "inputs": {"supplied": inputs or {}, "missing": []}, "status": None, "reason": None,
              "retrieval": None, "transfer_context": [], "conflicts": [], "provider_status": "NOT_CALLED",
              "uncertainty": None, "human_review": {"state": "PENDING_REVIEW", "human_verified": False,
                                                    "note": "No independent human review record exists."},
              "loop": meta}

    def step(name, **kw):
        meta["steps"].append({"step": name, **kw})

    step("1_receive", question_sha256=sha256_text(question))

    # 2 validate
    n_active = con.execute("SELECT COUNT(*) FROM chunks WHERE state='ACTIVE'").fetchone()[0]
    if n_active == 0:
        step("2_validate", outcome="EMPTY_INDEX")
        return _finish(con, result, t0, cfg, "INSUFFICIENT_EVIDENCE", "EMPTY_INDEX")
    refusal = check_sizing_request(question, inputs)
    if refusal:
        step("2_validate", outcome="SIZING_REFUSED", categories=[c["category"] for c in refusal["categories"]])
        result["refusal"] = refusal
        result["inputs"]["missing"] = refusal["missing_inputs"]
        # reference context only: retrieved for transparency, never used to build claims
        if meta["tool_calls"] < cfg.max_tool_calls:
            meta["tool_calls"] += 1
            ref = retrieve(con, question, filters, cfg.top_k, "strict")
            result["reference_context_not_a_sizing_basis"] = [
                {"chunk_id": p["chunk_id"], "source_id": p["source_id"], "locator": p["locator"],
                 "jurisdiction": p["jurisdiction"]} for p in ref["passages"] + ref["transfer_context"]]
        return _finish(con, result, t0, cfg, "INSUFFICIENT_EVIDENCE", refusal["reason"])
    step("2_validate", outcome="OK")

    # 3-4 retrieve, rejecting ineligible/irrelevant/transfer/conflicting
    ret = None
    for strat in list(cfg.strategies)[:max(1, cfg.max_retrieval_attempts)]:
        if meta["tool_calls"] >= cfg.max_tool_calls:
            step("3_retrieve", outcome="TOOL_CALL_BUDGET_EXHAUSTED")
            return _finish(con, result, t0, cfg, "INSUFFICIENT_EVIDENCE", "TOOL_CALL_BUDGET_EXHAUSTED")
        meta["retrieval_attempts"] += 1
        meta["tool_calls"] += 1
        ret = retrieve(con, question, filters, cfg.top_k, strat)
        step("3_retrieve", strategy=strat, status=ret["status"], reason=ret["reason"],
             chunk_ids=[p["chunk_id"] for p in ret["passages"]], excluded=ret["excluded"])
        if ret["status"] == "OK":
            break
    result["retrieval"] = _compact_retrieval(ret)
    result["transfer_context"] = [citation_of(p) for p in ret["transfer_context"]]
    result["conflicts"] = ret["conflicts"]

    conflicted = {cid for c in ret["conflicts"] for cid in c["chunk_ids"]}
    # An unresolved source conflict contests the question's central quantity: abstain entirely rather than
    # present a partial answer built from the other passages that merely co-occurred in the result set.
    usable = [] if conflicted else list(ret["passages"])
    step("4_reject", conflicted_chunk_ids=sorted(conflicted), usable_chunk_ids=[p["chunk_id"] for p in usable])

    # 5 insufficiency
    if ret["status"] == "INSUFFICIENT_EVIDENCE" or not usable:
        reason = ret["reason"] if ret["status"] != "OK" and ret["status"] != "CONFLICT_UNRESOLVED" else (
            "UNRESOLVED_SOURCE_CONFLICT" if conflicted else ret["reason"])
        step("5_insufficient", reason=reason)
        result["inputs"]["missing"] = _missing_for(ret)
        return _finish(con, result, t0, cfg, "INSUFFICIENT_EVIDENCE", reason)

    # 6 generate
    if meta["tool_calls"] >= cfg.max_tool_calls:
        return _finish(con, result, t0, cfg, "INSUFFICIENT_EVIDENCE", "TOOL_CALL_BUDGET_EXHAUSTED")
    meta["tool_calls"] += 1
    gen = provider.generate(question, usable, inputs)
    result["provider_status"] = gen["provider_status"]
    result["execution"] = gen.get("execution")
    step("6_generate", provider=gen["provider"], provider_status=gen["provider_status"])
    if gen["provider_status"] in ("NOT_EXECUTED", "PROVIDER_ERROR"):
        result["reason_detail"] = gen.get("reason")
        return _finish(con, result, t0, cfg, gen["provider_status"], gen.get("reason"))
    if gen.get("abstain") or not gen["claims"]:
        result["inputs"]["missing"] = gen.get("missing", [])
        result["uncertainty"] = gen.get("uncertainty")
        return _finish(con, result, t0, cfg, "INSUFFICIENT_EVIDENCE", "PROVIDER_ABSTAINED")

    # 7-8 record and check
    checked = validate_claims(con, gen["claims"], usable, inputs)
    by_id = {p["chunk_id"]: p for p in usable}
    for i, c in enumerate(checked, 1):
        c["claim_id"] = f"{answer_id}-C{i:02d}"
        c["citations"] = [citation_of(by_id[cid]) for cid in c["chunk_ids"]
                          if cid in by_id and resolve_citation(con, {"chunk_id": cid})["resolved"]]
        c["scope_note"] = _scope_note(c["citations"], ret.get("target_jurisdictions"))
        c["human_review"] = "PENDING_REVIEW"
    result["claims"] = checked
    result["uncertainty"] = gen.get("uncertainty")
    result["inputs"]["missing"] = gen.get("missing", [])
    step("7_record", claims=[c["claim_id"] for c in checked])
    step("8_check", statuses={c["claim_id"]: c["status"] for c in checked})
    supported = [c for c in checked if c["status"] == "SUPPORTED_CANDIDATE"]
    status = "SUPPORTED_CANDIDATE" if supported else "UNSUPPORTED"
    return _finish(con, result, t0, cfg, status, None if supported else "ALL_CLAIMS_FAILED_DETERMINISTIC_CHECKS")


def _scope_note(citations, target):
    rel = {c["jurisdiction_relation"] for c in citations}
    juris = sorted({c["jurisdiction"] for c in citations})
    note = f"source jurisdiction(s): {', '.join(juris)}"
    if "GENERAL_PRINCIPLE" in rel:
        note += "; general engineering principle, not a site measurement"
    if any(j != "QA" for j in juris):
        note += "; NOT Qatar-site evidence"
    return note


def _missing_for(ret):
    r = ret.get("reason") or ""
    tj = ",".join(ret.get("target_jurisdictions") or [])
    if ret.get("status") == "CONFLICT_UNRESOLVED" or ret.get("conflicts"):
        qs = sorted({c["quantity_key"] for c in ret["conflicts"]})
        return [f"a declared priority rule or independent resolution between conflicting sources for: {', '.join(qs)}"]
    if r.startswith("ONLY_OTHER_JURISDICTION"):
        if ret.get("quantity_seeking"):
            return [f"a measured or source-reported value applicable to jurisdiction {tj} "
                    "(only other-jurisdiction or general-principle text was found)"]
        return [f"evidence applicable to jurisdiction {tj} (only other-jurisdiction transfer context was found)"]
    if r.startswith("REQUIRED_NUMERICAL_VALUE_ABSENT"):
        return ["a measured or source-reported numerical value for the quantity asked"]
    if r == "EMPTY_INDEX":
        return ["any ingested eligible source"]
    return ["an eligible passage that covers the question's terms"]


def _compact_retrieval(ret):
    return {k: ret[k] for k in ("status", "reason", "strategy", "terms", "target_jurisdictions", "source_scope",
                                "excluded", "min_term_coverage", "quantity_seeking") if k in ret} | {
        "passages": [{"chunk_id": p["chunk_id"], "scores": p["scores"], "matched_terms": p["matched_terms"],
                      "jurisdiction_relation": p["jurisdiction_relation"]} for p in ret["passages"]],
        "non_supporting_context": [p["chunk_id"] for p in ret.get("non_supporting_context", [])]}


def _finish(con, result, t0, cfg, status, reason):
    result["status"], result["reason"] = status, reason
    result["loop"]["latency_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    result["loop"]["stopped"] = "RECEIPT_WRITTEN"
    rdir = Path(cfg.receipts_dir)
    rec = {"answer_id": result["answer_id"], "ts": now_utc(), "question": result["question"], "status": status,
           "reason": reason, "provider": result["loop"]["provider"], "provider_status": result["provider_status"],
           "index_snapshot_sha256": result["loop"]["index_snapshot_sha256"],
           "claims": [{"claim_id": c["claim_id"], "status": c["status"], "chunk_ids": c["chunk_ids"],
                       "failure_reasons": c["failure_reasons"]} for c in result["claims"]],
           "retrieval_attempts": result["loop"]["retrieval_attempts"], "tool_calls": result["loop"]["tool_calls"],
           "conflicts": [c["chunk_ids"] for c in result["conflicts"]], "latency_ms": result["loop"]["latency_ms"]}
    result["receipt_sha256"] = _append_chained(rdir / "receipts.jsonl", rec)
    for c in result["claims"]:  # every claim, supported or not, is queued; none is human-verified
        _append_chained(rdir / "review_queue.jsonl", {
            "ts": now_utc(), "claim_id": c["claim_id"], "answer_id": result["answer_id"], "claim_status": c["status"],
            "chunk_ids": c["chunk_ids"], "review_state": "PENDING_REVIEW",
            "priority": "HIGH" if c["status"] == "UNSUPPORTED" or result["conflicts"] else "NORMAL",
            "reviewer": None, "independent_review_record": None})
    return result

"""CLI: ingest | retrieve | answer | evaluate | health | verify | resolve | export-public

Every command prints JSON to stdout. Exit codes: 0 ok, 2 insufficient/NOT_EXECUTED outcome (a valid, honest result),
3 integrity failure.
"""
import argparse
import json
import sys
from pathlib import Path

from . import store
from .answer import get_provider, DEFAULT_MODEL
from .evaluate import run_eval
from .loop import LoopConfig, run_question, verify_receipts
from .retrieve import retrieve

ROOT = Path(__file__).resolve().parent.parent


def _filters(a):
    f = {}
    if a.jurisdiction:
        f["jurisdictions"] = a.jurisdiction
    if a.min_year:
        f["min_year"] = a.min_year
    if a.max_year:
        f["max_year"] = a.max_year
    if a.topic:
        f["topics"] = a.topic
    if a.verification:
        f["verification_statuses"] = a.verification
    if a.source:
        f["source_ids"] = a.source
    if a.include_superseded:
        f["include_superseded"] = True
    return f


def _out(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="qeeri_rag")
    ap.add_argument("--db", default=str(ROOT / "runs" / "index.db"))
    ap.add_argument("--receipts-dir", default=str(ROOT / "runs"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("ingest"); s.add_argument("--allowlist", default=str(ROOT / "corpus" / "allowlist.json"))
    for name in ("retrieve", "answer"):
        s = sub.add_parser(name); s.add_argument("question")
        s.add_argument("--jurisdiction", action="append"); s.add_argument("--min-year", type=int)
        s.add_argument("--max-year", type=int); s.add_argument("--topic", action="append")
        s.add_argument("--verification", action="append"); s.add_argument("--source", action="append")
        s.add_argument("--include-superseded", action="store_true"); s.add_argument("--top-k", type=int, default=4)
        s.add_argument("--strategy", default="strict", choices=["strict", "relaxed"])
    s = sub.choices["answer"]
    s.add_argument("--provider", default="extractive", choices=["extractive", "claude"])
    s.add_argument("--model", default=DEFAULT_MODEL); s.add_argument("--inputs", help="JSON file of case inputs")
    s.add_argument("--max-retrieval-attempts", type=int, default=1); s.add_argument("--max-tool-calls", type=int, default=3)
    s = sub.add_parser("evaluate"); s.add_argument("--questions", default=str(ROOT / "eval" / "questions.json"))
    s.add_argument("--out", default=str(ROOT / "runs" / "eval_results.json")); s.add_argument("--model", default=DEFAULT_MODEL)
    s.add_argument("--no-models", action="store_true")
    sub.add_parser("health"); sub.add_parser("verify")
    s = sub.add_parser("resolve"); s.add_argument("chunk_id"); s.add_argument("--quote"); s.add_argument("--source-id")
    s = sub.add_parser("export-public"); s.add_argument("--out", default=str(ROOT / "runs" / "public_export.json"))

    a = ap.parse_args(argv)
    con = store.connect(a.db)
    if a.cmd == "ingest":
        r = store.ingest(con, a.allowlist); _out(r)
        return 0 if r["status"] == "OK" else 3
    if a.cmd == "health":
        h = store.health(con); _out(h)
        return 0 if h["status"] == "OK" else 3
    if a.cmd == "verify":
        v = store.verify_index(con); v["receipts_chain"] = verify_receipts(Path(a.receipts_dir) / "receipts.jsonl")
        _out(v)
        return 0 if v["valid"] and v["receipts_chain"]["valid"] else 3
    if a.cmd == "resolve":
        r = store.resolve_citation(con, {"chunk_id": a.chunk_id, "quote": a.quote, "source_id": a.source_id}); _out(r)
        return 0 if r["resolved"] else 2
    if a.cmd == "export-public":
        _out(store.export_public(con, a.out)); return 0
    if a.cmd == "retrieve":
        r = retrieve(con, a.question, _filters(a), a.top_k, a.strategy); _out(r)
        return 0 if r["status"] == "OK" else 2
    if a.cmd == "answer":
        inputs = json.loads(Path(a.inputs).read_text(encoding="utf-8")) if a.inputs else None
        cfg = LoopConfig(max_retrieval_attempts=a.max_retrieval_attempts, max_tool_calls=a.max_tool_calls,
                         top_k=a.top_k, receipts_dir=a.receipts_dir)
        prov = get_provider(a.provider, **({"model": a.model} if a.provider == "claude" else {}))
        r = run_question(con, a.question, inputs, _filters(a), prov, cfg); _out(r)
        return 0 if r["status"] == "SUPPORTED_CANDIDATE" else 2
    if a.cmd == "evaluate":
        r = run_eval(con, a.questions, a.out, model=a.model, run_models=not a.no_models,
                     cfg=LoopConfig(receipts_dir=str(Path(a.receipts_dir) / "eval_receipts")))
        _out({"out": a.out, "arm_C_summary": r["arm_C_deterministic_retrieval"]["summary"],
              "model_arms": {k: v["status"] for k, v in r["model_arms"].items()},
              "retrieval_justification": r["retrieval_justification"]["verdict"]})
        return 0
    return 3


if __name__ == "__main__":
    sys.exit(main())

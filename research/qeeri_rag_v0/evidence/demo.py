#!/usr/bin/env python3
"""Reproducible demo: no API key, no network. Run from research/qeeri_rag_v0:  python evidence/demo.py

Ingests the allowlisted corpus into a fresh DB, then asks positive and negative questions through the bounded loop with the
EXTRACTIVE (no-model) provider, and finally shows the NOT_EXECUTED result for the optional Claude provider.
Output is an engineering receipt of software behaviour, not an agricultural finding.
"""
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.pop("ANTHROPIC_API_KEY", None)  # the demo must run without credentials

from qeeri_rag import store  # noqa: E402
from qeeri_rag.answer import ClaudeProvider, ExtractiveProvider  # noqa: E402
from qeeri_rag.loop import LoopConfig, run_question, verify_receipts  # noqa: E402

RUN = ROOT / "runs" / "demo"
shutil.rmtree(RUN, ignore_errors=True)
con = store.connect(RUN / "index.db")
cfg = LoopConfig(receipts_dir=str(RUN))

print("== 1. INGEST (allowlist: corpus/allowlist.json)")
rec = store.ingest(con, ROOT / "corpus" / "allowlist.json")
for s in rec["sources"]:
    extra = s.get("reason") or f"{s.get('active_chunks')} chunks, content_hash={s.get('content_hash', '')[:12]}"
    print(f"  {s['source_id']:<18} {s['outcome']:<10} {extra}")
h = store.health(con)
print(f"  health: {h['status']}  active_chunks={h['active_chunks']}  snapshot={h['snapshot_sha256'][:16]}")

QUESTIONS = [
    ("ANSWERABLE", "What is the pad outlet temperature equation for fan and pad cooling?", None),
    ("ANSWERABLE", "How much cooling water did the Riyadh Venlo tomato greenhouse use per m2?", None),
    ("ANSWERABLE", "Does KAHRAMAA require approval of electrical installation design?", None),
    ("MISSING INFO", "What is the measured wet-bulb temperature at the Al-Shahaniya greenhouse in July?", None),
    ("WRONG COUNTRY", "What cooling water does a Qatar greenhouse use per m2?", None),
    ("CONTRADICTORY", "What fan airflow per floor area do fan and pad greenhouses use?", None),
    ("SIZING", "How many exhaust fans and what kW do I need for my 1000 m2 greenhouse in Qatar?", None),
]
print("\n== 2. ASK (extractive provider, no model)")
for tag, q, inputs in QUESTIONS:
    r = run_question(con, q, inputs, None, ExtractiveProvider(), cfg)
    print(f"\n[{tag}] {q}\n  -> {r['status']}" + (f"  ({r['reason']})" if r["reason"] else ""))
    for c in r["claims"]:
        cit = c["citations"][0]
        loc = cit["locator"]
        print(f"     {c['claim_id']} {c['status']}: {c['text'][:110].replace(chr(10), ' ')}...")
        print(f"        cite {cit['chunk_id']}  hash={cit['chunk_hash'][:12]}  section='{loc.get('section')}' page={loc.get('page')}")
        print(f"        source {cit['url']}  scope: {c['scope_note']}")
    if r["inputs"]["missing"]:
        print("     missing:", "; ".join(r["inputs"]["missing"][:8]))
    if r["conflicts"]:
        for c in r["conflicts"]:
            print(f"     conflict[{c['kind']}] {c['quantity_key']}: {json.dumps(c['values'])}")
    if r["transfer_context"]:
        print("     transfer-only context (NOT support):", ", ".join(t["chunk_id"].split("@")[0] for t in r["transfer_context"]))

print("\n== 3. OPTIONAL CLAUDE PROVIDER WITHOUT CREDENTIALS")
r = run_question(con, QUESTIONS[0][1], None, None, ClaudeProvider(), cfg)
print(f"  status={r['status']} provider_status={r['provider_status']} claims={len(r['claims'])}\n  reason: {r['reason']}")

print("\n== 4. INTEGRITY")
print("  index:", {k: v for k, v in store.verify_index(con).items() if k != "problems"})
print("  receipts chain:", verify_receipts(RUN / "receipts.jsonl"))
print("  review queue entries (all PENDING_REVIEW):",
      len((RUN / "review_queue.jsonl").read_text().splitlines()))

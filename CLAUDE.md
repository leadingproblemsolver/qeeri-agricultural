# CLAUDE.md — QEERI research engineering contract

## Mission and scope
This repository contains the approved agricultural LLM evaluation tools and a separately labeled, independently developed research MVP at `research_mvp/`. Continue **existing work**, don't redesign the system. The current MVP is a local Python standard-library evidence-to-decision tool, **not** a field-validated agricultural advisor, production RAG, or drone controller.

## Read before changing anything
1. `README.md` (root) and `research_mvp/README.md`.
2. `research_mvp/RELEASE_NOTES.md`, `PUBLIC_CASE_2024.md`, `DATA_REQUEST_MINIMUM.md`, `EVAL_LOOP.md`.
3. `research_mvp/qeeri_brain.py`, `mcp_server.py`, `qatar_public_case.py`, tests, source manifests.
4. Existing git status, branch, tests and release receipts. The tests reported in prior handoffs are claims until rerun in this environment.

## Mandatory invariants
- OBSERVED != MODELED != INFERRED != SOURCE-REPORTED != SYNTHETIC. Carry evidence state, time, spatial scope and units.
- Citation/source link != approved scientific fact. All 11 unresolved scientific QA items remain REVIEW until evidence-specific disposition; never silently alter their original keys or fabricate source passages.
- Missing != zero. Any cost / water / salinity claim requiring absent measured inputs must BLOCK with exact missing fields; descriptive greenhouse statistics and CIF unit values can WARN with explicit boundary.
- World Bank WITS HS 070700 import CIF aggregate != delivered import price; greenhouse national output != identifiable farm crop yield. Preserve original year, crop and scope. Treat the reported 2024 weight jump as REVIEW, not an error corrected without source.
- Retrieval relevance is not answer eligibility. Enforce deterministic admissibility **before** showing unsupported numerical conclusions. Source passages must resolve to exact reference and excerpt; non-matching references cannot be cited.
- The proposed drone/mission layer must never directly actuate hardware or bypass authorized flight-controller/operator controls.
- Runtime local JSONL receipts, field coordinates, secrets, private correspondence and unreleased datasets must stay local and untracked; verify `.gitignore` before committing. Receipts are tamper-evident against ordinary edits, not a trusted immutable ledger.

## Engineering loop — read research_mvp/EVAL_LOOP.md
1. Establish a **fresh-clone** baseline; record Python version and actual tests rather than copying published counters.
2. Fix the single highest-consequence reproducible failure with the smallest code diff and a regression fixture.
3. Run all existing tests, the MCP client/server smoke test, citation resolution probes, safe-refusal probes, local restart and corruption tests.
4. Inspect the JSON receipts, reasons, source IDs, units and scope, not just process exit codes.
5. Report one of PASS / FAIL / BLOCKED, a concrete artifact path and commit SHA, residual risks, and the next evidence event.
Limit to **3 repair iterations per hypothesis**. If still failing, classify and stop. Do not keep rewriting prompts or keyword lists when no new evidence is produced.

## First concrete task
Run `python -m unittest -v test_qeeri test_public_case_compact` and `python smoke_protocol.py` from `research_mvp/`; then inspect the actual exported functions and determine whether `test_public_case_compact` is discoverable. Record a clean-clone acceptance transcript. Build `retrieval_eval.json` only from source-backed tests with fixed expected sources. Report precision@k, recall@k and citation-resolution rate; if labels do not exist, create an explicitly labeled small gold set from actual `data/` records and avoid claiming generalization.

## Tools and security
- Python stdlib and current code first; no new dependencies, embeddings, vector DB, server hosting, hidden background agents or hardware interfaces until an observed requirement demands them.
- Use git branches/PRs for substantial changes; no force-push. Don't modify root approved evaluation tools unless the task requires it.
- Do not send local data to cloud model tools. Claude Code's normal prompt/file processing may transmit context to its provider; use only public/non-sensitive repository files unless sharing has been authorized.

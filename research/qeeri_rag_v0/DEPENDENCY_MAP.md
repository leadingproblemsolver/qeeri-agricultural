# Gate 0 — inventory and dependency map (observed 2026-11-09)

Starting state: session branch `claude/qeeri-rag-v0-18awxg` == `main` @ `09b7fdc`. (The brief names `feat/qeeri-rag-v0`; the session's designated branch was used instead.)
Remote branches inspected: `main`, `research/greenhouse-llm-feasibility-pilot` @ `8e0fc1b`, `research/human-ai-provenance-v1` @ `19eca95`, `eval/gate1-retrieval-admissibility` @ `47fb3f8`, `docs/greenhouse-feasibility-evidence-2026-11-07`.
The pilot branch **diverged from `main`** (merge-base `12d8587`); it lacks `main`'s Test A files and `main` lacks the pilot's ledger/runner. Nothing was merged.

| Asset | Where | Used? | How / why not |
|---|---|---|---|
| Canonical Section 5 prompt | `main:research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md` | rules reused | its "do not give exact fan sizes / kW / cable / breaker / pump / emitters / water" and "never invent a citation" rules are the basis of `instructions/FROZEN_INSTRUCTIONS.txt` and `guards.py`. The 11-step report prompt itself is not run (no key). |
| IFAS source packet (S01–S03) | `main:…/TEST_B_001_SOURCE_PACKET.md` | **ingested in place** (path reference, not copied) | packet format parsed by the `packet_markdown` loader. Boundary section is source-level metadata, not a chunk. |
| Evidence ledger (10 claims, 7 sources) | pilot branch `…/evidence_ledger.json` | **copied byte-identical** to `corpus/` | not on `main`; L06–L10 `SOURCE_TEXT_READ` ingested; L01–L05 abstract-only rejected. |
| `run_pilot.py` (urllib Messages call, NOT_EXECUTED pattern, no-tools body) | pilot branch | pattern reused | `answer.ClaudeProvider` follows the same wire format and no-key behaviour; code not imported (different branch). |
| `evidence_ledger` status vocabulary / `human_verified:false` | pilot | reused | mapped to `verification_status`. |
| `score_rubric.py`, `test_pilot.py` | pilot | **not used** | a rubric for scoring full reports; human claim scoring stays `PENDING_REVIEW`. |
| `TEST_A_B_001_COMPARATIVE_CLAIM_REVIEW.md`, `05_LLM_BENCHMARK_AND_PRE_RAG_GATE.md` | pilot | read | source of the NO-GO-unless-retrieval-specific-error gate and of the contamination warnings; shaped the evaluation verdict. |
| `TEST_A_001_BASELINE_RESPONSE.md`, B1 (`human-ai-provenance-v1`), B2 (pilot) | main / other branches | **deliberately not used** | contaminated, non-comparable chat transcripts; never compared with new arms. |
| `research_mvp/` (qeeri_brain, MCP server, hash-chained receipts) | main | read, **not modified** | independent cucumber/WITS MVP; the receipt hash-chain idea is mirrored in `loop._append_chained`. Its 62 tests and `smoke_protocol.py` still pass. |
| `eval/gate1-retrieval-admissibility` (`retrieval_eval.py`, gold json) | other branch | read only | research_mvp-specific; different corpus. |
| `tests/test_integrity.py` (root) | main | not touched | **pre-existing failure**: needs untracked `03_runs/prompts_applied_200.csv`; fails identically without this change. |

Test commands present before this work: `cd research_mvp && python -m unittest -v test_qeeri test_public_case_compact` (62 pass) and `python smoke_protocol.py` (PASS).
Data permissions: no source in the repo carries a redistribution license statement. All ingested sources are therefore `LOCAL_ONLY`; public export yields 0 chunks.

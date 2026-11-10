# QEERI RAG v0 — provenance-preserving local evidence retrieval (engineering slice)

**Status: ENGINEERING PROTOTYPE. Not a scientific finding, not an agricultural advisor, not validated by any human reviewer.**
A passing demo shows that specified software behaviour works. It does **not** show that RAG improves agricultural decision-making;
the pilot's own pre-RAG gate (`research/internship_five_week_review_2026-11-08/05_LLM_BENCHMARK_AND_PRE_RAG_GATE.md`, pilot branch) said NO-GO until a
retrieval-specific error is observed, and nothing here changes that (see *Evaluation*).

Workflow: `approved local source → auditable chunks → FTS5 index → evidence-grounded answer or explicit insufficiency → receipt`.
Python ≥ 3.10 standard library only (SQLite with FTS5; verified on Python 3.13 / SQLite 3.53). No install step, no network, no key needed.

## Reproduce (no API key)

```bash
cd research/qeeri_rag_v0
python -W ignore -m unittest discover -s tests -v      # 71 tests incl. the 14 hostile scenarios + probe battery
python evidence/demo.py                                # ingest + positive/negative questions + receipts
python -m qeeri_rag ingest                             # build runs/index.db from corpus/allowlist.json
python -m qeeri_rag retrieve "What pad area per greenhouse floor area does FAO suggest?"
python -m qeeri_rag answer   "What cooling water does a Qatar greenhouse use per m2?"      # -> INSUFFICIENT_EVIDENCE
python -m qeeri_rag evaluate                           # -> runs/eval_results.json (model arms NOT_EXECUTED without key)
python -m qeeri_rag health && python -m qeeri_rag verify
```

Optional Claude generation with your own credentials (nothing is sent unless you do this; the passages and frozen instructions are the only content sent):

```bash
export ANTHROPIC_API_KEY=...            # yours; never committed
python -m qeeri_rag answer "What pad area per greenhouse floor area does FAO suggest?" --provider claude
python -m qeeri_rag evaluate            # now also runs arms A/B/C with identical settings and stores raw responses
```

Exit codes: `0` supported/ok, `2` insufficient / NOT_EXECUTED (a valid, honest outcome), `3` integrity failure.

## Interfaces (CLI is the contract; GraphQL deliberately not built)

| Command | Function | Returns |
|---|---|---|
| `ingest` | `store.ingest(con, allowlist)` | per-source INGESTED / UNCHANGED / REJECTED+reason, chunk ids, content hashes, quarantined chunks |
| `retrieve` | `retrieve.retrieve(con, question, filters, top_k)` | `passages` (+provenance, scores), `transfer_context`, `conflicts`, `excluded` counts, `status` ∈ OK / INSUFFICIENT_EVIDENCE / CONFLICT_UNRESOLVED |
| `answer` | `loop.run_question(...)` | claims (`CITATION_CHECK_PASSED_REVIEW_PENDING` / `UNSUPPORTED`) or `INSUFFICIENT_EVIDENCE` / `NOT_EXECUTED` / `PROVIDER_ERROR`, missing inputs, receipt hash |
| `evaluate` | `evaluate.run_eval(...)` | arm C metrics + per-arm A/B/C records; `eval/questions.json` |
| `health`, `verify`, `resolve`, `export-public` | integrity, citation resolution, fail-closed export | |

Filters (`retrieve`/`answer`): `--jurisdiction`, `--min-year/--max-year`, `--topic`, `--verification`, `--source`, `--include-superseded`.
GraphQL was not added: no consuming workflow with a concrete structured-query need exists yet.

## What is in the index (and what is not)

| Source | Verification | Jurisdiction | In index |
|---|---|---|---|
| UF/IFAS AE069 packet (`greenhouse_llm_feasibility/TEST_B_001_SOURCE_PACKET.md`, `main`) — S01–S03 | PACKET_ASSERTED | US-FL (general principle) | yes (3 chunks) |
| FAO 2013 (ledger L08, L09) | SOURCE_TEXT_READ | Mediterranean | yes (2) |
| KAHRAMAA LV Wiring Code 2016 Issue 0 (L10) | SOURCE_TEXT_READ | QA | yes (1) |
| Tsafaras 2021, Riyadh (L06, L07) | SOURCE_TEXT_READ | SA | yes (2) |
| Mahmood 2022, Ghani 2020, Lahlou 2025 (L01–L05) | UNVERIFIED_ABSTRACT_ONLY | QA | **rejected** (abstract-only) |
| Nexus 2026 CPI | UNVERIFIED_NOT_LOCATED | — | not allowlisted (no content) |

`corpus/evidence_ledger.json` is a **byte-identical copy** of `research/greenhouse_llm_feasibility/evidence_ledger.json` from pilot-branch commit `8e0fc1b` (git blob `1ea401e0`, sha256 `a552a22b…`),
copied because that branch has not been merged into `main`. `human_verified` is `false` for every ledger claim; the ledger itself says page numbers are inferred (±1) and excerpts came through a model-mediated fetch.
No source text was downloaded; no quotation, page or value was added. **There are no Qatar greenhouse measurements in the corpus**, so Qatar-site numerical questions correctly abstain.

## How the invariants are enforced (each has a test in `tests/test_hostile.py`)

| Invariant | Mechanism |
|---|---|
| Reject unapproved/unverified/unknown-permission material | allowlist gate in `store.ingest`; ineligible → logged `REJECTED`, never ACTIVE; a source that later becomes ineligible is removed from the index |
| Public export fails closed | `export-public` emits only `PERMITTED_EXPORT` sources; everything currently `LOCAL_ONLY` (exports 0 chunks) |
| Immutable chunk ids / hashes | `chunk_id = source#label@sha256[:12]` of canonical {source, label, locator, text}; content change ⇒ new id, old id `SUPERSEDED_BY_REINGEST` and no longer resolves |
| Modified document | source file hash re-checked at retrieval and citation time (fail closed); `verify` recomputes every chunk hash |
| Relevance ≠ eligibility | term-coverage gate (≥0.6 of content terms, ≥2 matched) on top of BM25; quantity-seeking questions need a passage with quantitative content |
| Other country ≠ Qatar evidence | if the question names a jurisdiction, other-jurisdiction passages go to `transfer_context` only, never into claims; a general-principle passage (e.g. IFAS, US-FL) **never** supports a question that names a site — it is shown as context only |
| Contradictory sources | same `quantity_key` + disjoint values across sources + no priority rule ⇒ `CONFLICT_UNRESOLVED`; the loop abstains entirely |
| Prompt injection | pattern scan quarantines chunks at ingestion; in the adapter passages sit in an `<untrusted_passages nonce=…>` block with a per-call random delimiter; output claims echoing injection text are `UNSUPPORTED` |
| No fabricated citations | every cited chunk id must be in the retrieved set **and** resolve (id, source, hash, optional quote); every number in a claim must appear in a cited chunk or supplied inputs |
| No sizing | `guards.check_sizing_request` refuses fan/cooling-kW/electrical/pump/emitter/water-volume specification, lists exact missing inputs, and **still refuses when all inputs are supplied** (no vetted calculator exists here); generated sizing figures not in a cited chunk ⇒ `UNSUPPORTED` |
| Nothing is "human-verified" without a record | `HUMAN_VERIFIED` is accepted at ingestion only with `review_record{reviewer, reviewed_at, record_path}` and `reviewer != curator`; otherwise the source is rejected. No source in the corpus has one |
| Ingestion is confined | a source path must resolve under the repo (allowlist inside the repo) or under the allowlist's own directory; `../` and absolute escapes are rejected |
| Model cannot self-approve | statuses are assigned by `guards.validate_claims`, not the model; every claim is queued `PENDING_REVIEW`; `human_verified` is false everywhere |
| Missing key ≠ success | `ClaudeProvider` without a key returns `NOT_EXECUTED` and no text; HTTP/parse failures are `PROVIDER_ERROR` |
| Bounded loop | `max_retrieval_attempts` (default 1), `max_tool_calls` (default 3), no browsing, no tool use in requests |

`CITATION_CHECK_PASSED_REVIEW_PENDING` means *the software checked citation resolution, the retrieved-set membership and limited numerical/format guards; it has NOT checked semantic entailment or scientific correctness*. It is **not** a claim that the passage entails the answer or that the source is correct.
Extractive mode's claim is the chunk's own text, so entailment there is trivially identity, which is why it is labelled `EXTRACTIVE_NO_MODEL`.

Runtime receipts (`runs/receipts.jsonl`, `runs/review_queue.jsonl`) are SHA-256 chained: tamper-evident against ordinary edits only, **not** a trusted immutable ledger. `runs/` and `*.db` are gitignored. `evidence/` holds the committed demo/eval/test outputs.

## Evaluation (`evaluate`) — read the limits

* Arms: **A** no documents · **B** fixed packet (all 8 chunks) · **C** retrieval-selected passages. Same frozen instructions (`instructions/FROZEN_INSTRUCTIONS.txt`, sha256 `89e4547b…`) and model settings across arms; exact request bodies, snapshot hash, run timestamps stored.
* **Executed here: arm C deterministic layer only.** On the 14-question set (`eval/questions.json`, 6 positive / 8 negative): hit@k 1.0, mean precision@k 0.917, recall@k 1.0, false-support 0.0, correct abstention 1.0, citation resolution 1.0, median retrieval+loop latency ≈0.7 ms (`evidence/eval_results.json`).
* **That set is engineer-authored, tiny, and not held out:** a guard was changed after item N05 failed on it (see below). It supports "the gates behave as designed on these cases", **not** any claim of generalisation.
* **Model arms A/B/C: `NOT_EXECUTED`** (no `ANTHROPIC_API_KEY`). Cost and token usage: not measured. Human claim-level correctness: `PENDING_REVIEW` for everything.
* Arms A/B/C are **not** comparable to the historical ChatGPT Test A / B1 / B2 transcripts (different vendor and protocol, B1/B2 contaminated by prior exposure). They were not used.
* **Verdict recorded in the results file: retrieval has NOT justified its operational complexity.** No consequential problem was observed on which C beat B; the whole eligible corpus is 3,697 characters and fits in a fixed packet; the abstention/citation gates demonstrated here could be applied to a packet without an index.

## Known limitations (observed)

* **A real citation does not prove entailment.** Citation and number checks cannot establish that a claim agrees with its source. The observed *single sensor is sufficient to verify uniformity* contradiction is now specifically rejected with `EXPLICIT_SOURCE_CONTRADICTION:SINGLE_SENSOR_UNIFORMITY` when the cited passage explicitly denies that inference. This is a **narrow domain-specific guard, not general entailment verification**. Other contradictory claims can still reach `CITATION_CHECK_PASSED_REVIEW_PENDING` and require independent human adjudication. `tests/test_probe_battery.py` pins both the rejection and two non-contradiction controls. In extractive mode a claim is the chunk's own text, but whether that text answers the question or is scientifically valid remains unverified.
* **Intent and place detection are keyword/regex heuristics** (sizing categories, quantity-seeking phrases, a jurisdiction gazetteer in `retrieve.py`). They fail closed on every case tried (30 paraphrases across two probe batteries) but: places not in the gazetteer are undetected (a question about a country not listed is answered from whatever the corpus holds, labelled with its real jurisdiction and "NOT Qatar-site evidence"); non-English questions are unsupported; spelled-out numbers are only checked against a fixed word list. The first probe batteries found 4 misses (fixed); the second (14 negatives, 8 positives) found 0 false supports and 1 over-refusal (fixed). Both batteries are now regression fixtures, so they are no longer held-out evidence.
* **Over-refusal is the price of fail-closed.** A question that names a Qatar site and asks anything the corpus only answers with US-FL/SA/Mediterranean text returns `INSUFFICIENT_EVIDENCE` plus `transfer_context`, even for a conceptual question the IFAS principle would answer.
* The lexical gate is a term-coverage heuristic, not semantic matching. The shared-words negative (nitrogen fertilizer for greenhouse tomato) is rejected with best coverage 0.33 (2 of 6 terms; it is also rejected by the 0.5 "relaxed" strategy), but loosening the threshold is not safe in general: the relaxed strategy returned 5 passages and a spurious conflict for the pad-equation question, so it is opt-in (`--max-retrieval-attempts 2`) and locked in a test. No embeddings were added: no defined retrieval test failed in a way embeddings would fix, and the corpus is 8 chunks.
* Conflict detection only covers chunks carrying curator-assigned `quantity_key`/range (L07, L08). L07 (Riyadh as-built, per ground area) vs L08 (FAO rule of thumb, per greenhouse area) are different kinds of statement; the system flags them unresolved rather than deciding.
* Curator-assigned fields (`reuse_status`, `applicability_class`, `topics`, quantity ranges, aliases) were set by the implementer in `corpus/allowlist.json`. `LOCAL_ONLY` is a conservative label, **not** a legal permission determination.
* Receipts are tamper-evident against ordinary edits only; deleting or replacing the whole log is undetectable. Single writer, no locking.
* Generation via the real Claude API has never been run in this environment; `tests/` exercise the request/response plumbing against a local fake server whose canned text is not a model result.

## Four-layer implementation mapping (no new architecture)

| Layer | Existing implementation | Current boundary / next proof |
|---|---|---|
| 1. Reliable evidence ingestion | `corpus/allowlist.json` → `store.ingest` → hashed source/chunk records in SQLite | Only 8 eligible chunks; independent verification and permission to reuse remain unconfirmed. |
| 2. Deterministic correctness | `guards.py` for source/citation/numeric/sizing checks; retrieval rejects irrelevant, cross-jurisdiction and conflicting records | Known single-sensor contradiction now rejected by a narrow explicit rule; no general unit-aware physical model or semantic entailment engine. |
| 3. Evidence-grounded AI | `retrieve.py` + `loop.py`; extractive no-model answer and optional Claude adapter | Model A/B/C API arms not executed; no measured improvement from retrieval versus a fixed source packet. |
| 4. Auditable decisions | `receipts.jsonl`, `review_queue.jsonl`, `verify`, human-review state | No independent expert claim review. No approval to use outputs for greenhouse installation. |

**Next evidence event:** execute the complete local test suite on this PR branch, inspect the contradiction regression and the negative controls, then obtain an independent reviewer decision on one real claim/source pair. Do **not** add embeddings, GraphQL, another agent or a scientific-validity label until a real failure demonstrates need.

## Layout

```
qeeri_rag/   store.py (ingest/verify/resolve/export)  retrieve.py  guards.py  answer.py (extractive + Claude)  loop.py  evaluate.py  cli.py
corpus/      allowlist.json  evidence_ledger.json (copy, see above)
instructions/FROZEN_INSTRUCTIONS.txt     eval/questions.json
tests/       test_hostile.py (14 scenarios)  test_regressions.py  test_probe_battery.py (independent-verification findings)
evidence/    DEMO_TRANSCRIPT.txt  TEST_LOG.txt  eval_results.json  eval_summary.json  demo.py
DEPENDENCY_MAP.md  HUMAN_VERIFICATION_CHECKLIST.md
```

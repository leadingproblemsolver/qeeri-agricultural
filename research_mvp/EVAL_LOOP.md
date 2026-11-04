# QEERI — bounded CTO evaluation loop

**Starting state:** research MVP and public Qatar cucumber 2024 national-data example. Current source is published, but independent clean-clone verification and retrieval metrics are **not established** by past assistant claims. The goal is an externally reproducible result, not additional architecture.

## Gate 0 — clean clone / reproducibility (P0)
From a fresh clone and only committed files:
```bash
git clone https://github.com/leadingproblemsolver/qeeri-agricultural.git
cd qeeri-agricultural/research_mvp
python -m unittest -v test_qeeri test_public_case_compact
python smoke_protocol.py
python cli.py ask "Qatar cucumber imports 2024"
python cli.py ask "What does it cost to grow cucumbers in Qatar?"
python cli.py ask "Q-K26 potato aphid"
python qatar_public_case.py
python cli.py verify
```
Capture **actual output, exit codes, Python version, commit SHA**. Do not quote 52 or 72 as a fresh count without running. Check instructions, import paths and clean state. If failures, fix precisely one blocker plus regression.

## Gate 1 — retrieval and citation (P0)
Prepare 15–30 **fixed, labeled** public-source questions from already committed files (WITS 2023/2024; greenhouse/open-field production; 4 public scientific review excerpts; unrelated and deliberate paraphrase queries). Use `query → expected source_id/record_id → expected state → expected unit/scope`. No fabricated answer keys. Report:
- recall@k: proportion of expected records retrieved among labeled positive cases.
- precision@k: relevant returned records / returned records on same labeled cases.
- citation resolution: percent of citations that point to an existing file/source record and exactly substantiate the claim.
- irrelevant-citation rate: unrelated results used as support.
For queries with no gold relevant item, test abstention separately. Publish the finite gold fixtures and deterministic runner, with limitations.

## Gate 2 — correct decision admissibility (P0)
A held-out test suite must include:
- Cost/savings/profit/subsidy comparisons BLOCK without both matching local full costs and delivered import cost.
- Water irrigation efficiency BLOCK without metered irrigation and same-cycle marketable harvest.
- EC/salinity BLOCK without measured, method/space/time-bound soil or water data as applicable.
- Direct WITS CIF unit value WARN with explicit import-price boundary.
- Same-scope historical production comparison WARN (not unrelated cost BLOCK).
- Scientific QA items REVIEW; no source excerpt may auto-approve or modify QA keys.
- Contradictions, malformed source, missing unit, wrong year/crop, unrelated citation, malicious text and invented nitrate threshold must fail closed.
Each case checks status, missing fields, provenance and absence of unsupported numeric suggestions.

## Gate 3 — persistence, protocol and private-by-default (P0)
- Protocol: separate stdio client exercises initialize, list, call, errors with stable machine-readable results.
- Restart: a receipt survives process restart, preserving order/source and verification.
- Corruption: edits, invalid hashes and truncation must be surfaced; **do not append after failed verification**. Note that full replacement/truncation needs external anchoring to prove.
- Packaging: clean clone succeeds; `git status` stays clean apart from clearly ignored local receipts; no private emails, personal records, real field-level coordinates, API keys or logs committed.
- Run non-GUI first-time instructions exactly; all errors offer actionable recovery.

## Gate 4 — Qatar environmental/financial realism (P1)
The 2024 cucumber example is a **national aggregate only**; do not select an arbitrary farm coordinate and join its NASA POWER or SoilGrids values. Before location-matched environmental retrieval, require sourced field_id / WGS84 point or polygon, crop-cycle dates and source permissions. NASA POWER/ERA5-Land are modeled proxies, not measured greenhouse conditions; SoilGrids is not lab EC. Keep missing inputs BLOCK. Make one local JSON specimen with `known`, `source_reported`, `modeled`, `missing`, decision/reasons and immutable source identifiers; **never fabricate measured inputs**.

## Loop termination and review rubric
Weight: functionality 25%; scientific/financial correctness 25%; usability 15%; reliability 15%; security 10%; interoperability 10%. Require **≥7/10 AND no unresolved P0 failures** for an engineering-review release (not scientific validation). Independent cold-run required before stronger claims.

For each bounded attempt:
`Observed failure → minimal patch → one regression test → full suite → receipt → git diff → decision`.
Up to 3 repairs per hypothesis; otherwise record BLOCKED and stop. Do not broaden scope or use an infinite Stop hook.

Final output:
```
COMMIT: <SHA or UNCOMMITTED>
ENVIRONMENT: <Python/OS/client>
CLEAN-CLONE: PASS|FAIL|NOT_RUN
TESTS: <passed>/<run>, failures
RETRIEVAL: recall@k, precision@k, citation resolution or NOT_MEASURED
MCP: PASS|FAIL|NOT_RUN
INVARIANTS: explicit P0 failures
FIELD-LEVEL VALIDATION: NOT DONE unless actual matched measured field records
VERDICT: ACCEPT_RESEARCH_MVP|REJECT|BLOCKED
NEXT EXTERNAL RECEIPT: <one concrete action>
```

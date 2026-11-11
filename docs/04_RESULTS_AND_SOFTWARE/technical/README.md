# 4 — Code, test receipts and known limitations

**Next technical implementations (only after evidence gates):** [five research/industry tracks](../../../research/technical_tracks/README.md) and [portfolio capability-to-proof map](PORTFOLIO_PROOF_MAP.md). These reference existing code instead of creating competing implementations.

## Existing code: no migration
- [Research MVP and its documented run commands](../../../research_mvp/README.md). Scientific evidence is not established by a CLI response. WITS imports are trade context, not greenhouse yield or costs.
- [Main-branch input gate](../../../research/greenhouse_llm_feasibility/validate_field_packet.py) + [negative tests](../../../research/greenhouse_llm_feasibility/test_validate_field_packet.py). **Four tests succeeded** in [GitHub Actions run 42962023814](https://github.com/leadingproblemsolver/qeeri-agricultural/actions/runs/42962023814). A metadata pass yields `CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_CHECK`, not `HUMAN_VERIFIED`.
- [PR #2 branch RAG prototype](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/claude/qeeri-rag-v0-18awxg/research/qeeri_rag_v0) and [draft PR #2](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/2). Previous combined CI on that branch included **75 RAG plus 5 synthetic-cooling tests**, [run 42802024430](https://github.com/leadingproblemsolver/qeeri-agricultural/actions/runs/42802024430). These are software regression tests on a dated commit.
- [Existing PR branch scientific case](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/claude/qeeri-rag-v0-18awxg/research/greenhouse_llm_feasibility/scientific_case_v0) is **not on main**.

## Known correctness limits
- Citation validity does **not** imply the quoted source logically supports the claim.
- RAG's FAO fixtures conflict with an exclusion decision; source use must be fixed and CI rerun before declaring the corpus clean.
- Proving arithmetic from synthetic input does not validate weather, crop physiology, sizing, equipment control, or any economic outcome.
- Full A/B/C source-assisted model comparisons are not established by passing RAG unit tests.
- An append-only local hash chain requires an external anchor to protect against wholesale replacement.

## Reproduce only as applicable
```bash
python -m unittest -v research_mvp/test_qeeri.py
cd research/greenhouse_llm_feasibility
python -m unittest -v test_validate_field_packet
```
The RAG suite is on an **unmerged** branch and must be executed after intentionally switching to that branch, not assumed present on `main`.

**Software receipt format:** commit SHA, command, environment, number of tests, pass/fail output, date, log location. **Scientific receipt:** source locator, measured-vs-modeled identity, original response, independent answer key, blinded assessment where possible, limitations. Keep them separate.

# 01 — LLM output evaluation and verification

**Research purpose:** determine whether verified scientific evidence changes an existing model's correctness, applicability and safe abstention on a Qatar-relevant agricultural question. **This is the active implementation track.**

## Reuse exact existing implementations
- [Agricultural local source/explanation/evidence-state engine](../../../research_mvp/qeeri_brain.py), [MCP tool boundary](../../../research_mvp/mcp_server.py), [existing tests](../../../research_mvp/test_qeeri.py).
- [Input verification gate](../../greenhouse_llm_feasibility/validate_field_packet.py), [negative tests](../../greenhouse_llm_feasibility/test_validate_field_packet.py). GitHub Actions [four-test receipt](https://github.com/leadingproblemsolver/qeeri-agricultural/actions/runs/42962023814).
- [RC04 question/answer-key draft](../../greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md), [scoring and physics requirements](../../greenhouse_llm_feasibility/RC04_FOUNDATIONS_AND_SCORING.md), [B source packet](../../greenhouse_llm_feasibility/TEST_B_001_SOURCE_PACKET.md).
- [PR #2 RAG prototype, unmerged](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/claude/qeeri-rag-v0-18awxg/research/qeeri_rag_v0), [evaluation receipt](https://github.com/leadingproblemsolver/qeeri-agricultural/blob/claude/qeeri-rag-v0-18awxg/research/qeeri_rag_v0/evidence/eval_summary.json): retrieval fixture results exist, all **A/B/C generation arms NOT_EXECUTED**.

## Minimal next executable contribution
1. Fix original source fidelity and lock *one* RC04 reference key with claim-to-passage locators, unknowns and reviewer status.
2. Freeze identical question, model build, setting and no-tools condition for no-packet A and fixed-packet B. No rewritten questions.
3. Retain original outputs, metadata and hashes; compare each claim manually against a reference key prepared first. Distinguish false support, missing values, invented site measurements and unjustified engineering specificity.
4. Only automate a real observed checking failure (e.g. source mismatch or unit error) and pin a hostile regression test.

## Exit receipt
Case ID + original source locator/hash + full two responses + precise model metadata (UNKNOWN if unavailable) + independent human review + claim-level scored difference + experiment decision. A/B missing => `EXPERIMENT_BLOCKED`, not an improvement percentage.

**False claim to avoid:** passing 75 RAG tests proves agricultural truth, citation entails claim, or a synthetic 26.1°C pad outlet predicts canopy temperature. **Industry signal:** reproducible evaluation engineer, with explicit error boundary.

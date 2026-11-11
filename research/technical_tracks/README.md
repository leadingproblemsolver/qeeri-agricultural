# QEERI technical continuation — evidence-gated implementation

**Purpose:** give a researcher or engineer the next small implementation after its scientific requirement has been demonstrated. These folders are **execution briefs**, not new codebases and not claims of built AI systems. The original research goal remains agricultural LLM reliability and bounded Qatar greenhouse feasibility. **Do not move or fork existing code for appearance.**

## Work in this order

| Track | Status | Industry/research capability | When allowed |
|---|---|---|---|
| [01 — Evaluate and verify LLM outputs](01_evaluation_verification/README.md) | **ACTIVE: existing code + scientific experiment incomplete** | Evaluation, source-to-claim validity, errors, abstention | Now; this is the original research priority |
| [02 — Synthetic evaluation and model adaptation](02_synthetic_evaluation_adaptation/README.md) | **PARTIAL fixtures; adaptation NOT AUTHORIZED** | Controlled test cases, controlled counterexamples, mid/post-training only if proved necessary | After baseline/reference-key and held-out test evidence |
| [03 — Feedback, memory and collaborative agents](03_feedback_memory_collaboration/README.md) | **CROSS-REPO CODE EXISTS; QEERI INTEGRATION NOT EXECUTED** | Operator feedback, durable context, goal/ownership state, multi-party/multi-agent tasks | After a real reviewer handoff failure is recorded |
| [04 — Privacy, continual and test-time learning](04_privacy_continual/README.md) | **RESEARCH BACKLOG, NOT IMPLEMENTED** | Differential privacy, controlled updates, drift and no-leak evaluation | After legitimate sensitive data/use/rights and baseline exist |
| [05 — Enterprise deployment and research collaboration](05_field_deployment_collaboration/README.md) | **LOCAL MCP EXISTS; NO ENTERPRISE PILOT** | Forward-deployed integration, human reviewer receipt, measurable consequence | After an authorized operator task and verified utility |

## Research topic mapping (application keywords are not evidence)
- **Understanding/verifying/evaluating LLM outputs:** track 01 — strongest current alignment.
- **Synthetic data for evaluation/fine-tuning; mid/post training:** track 02 — synthetic *tests* exist; no fine-tuned LLM.
- **Learning from feedback; memory/goal management; inter-agent conversation; collaborative agents; multi-agent simulation:** track 03 — local context/receipt code in separate GitHub repositories; no verified multi-agent collaboration experiment.
- **Differential privacy; continual learning; test-time training:** track 04 — no implemented or measured QEERI contribution.
- **Forward deployment for enterprise AI; mentor/cross-group collaboration:** track 05 — local MCP interface and research handoff material; no verified production deployment or partner adoption.

## Evidence and ownership rules
1. Every claim of implemented work must point to an exact repository, branch, file, test and observed output. Do not attribute a repository's entire history or code authorship to an individual without commit evidence.
2. Scientist-facing output: original question, source and independent claim judgment. Developer-facing output: reproducer and hostile tests. Mentor-facing output: decision request and actual reply. Employer-facing output: clearly labeled implementation, result and limits.
3. **A code demonstration is not a deployed agent, a synthetic fixture is not a field observation, and a demo receipt is not customer acceptance.**
4. Keep restrictions: no private QEERI/supervisor/participant files in GitHub; no autonomous greenhouse installation instructions or hardware operation; no model training before an identified weakness and suitable authorized data.
5. Work starts only with a concrete failure, baseline or external request. Every track ends with reproducible proof, falsification, or an explicit block/kill.

**Portfolio entrypoint:** [Capability-to-evidence map](../../docs/04_RESULTS_AND_SOFTWARE/technical/PORTFOLIO_PROOF_MAP.md). **Existing research methods:** [RC04 foundations](../greenhouse_llm_feasibility/RC04_FOUNDATIONS_AND_SCORING.md). **Existing live code:** [research_mvp](../../research_mvp/README.md).

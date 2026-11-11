# 02 — Synthetic evaluation, then optional model adaptation

**Research purpose:** create controlled tests for known failure modes without inventing real-world agricultural observations. Synthetic cases are **test inputs**, never Qatar field telemetry.

## Existing foothold
- [Synthetic pad-outlet example on draft PR #2 branch](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/claude/qeeri-rag-v0-18awxg/research/greenhouse_llm_feasibility/scientific_case_v0). A math example under 38°C / 24°C / 85% gives 26.1°C.
- [RC04 missing-canopy-inputs test](../../greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md).
- [False site telemetry quarantine](../../greenhouse_llm_feasibility/RC04_FIELD_PACKET_INTEGRITY_2026-11-11.md).

## Smallest next technical experiment — AFTER track 01
Build a **small versioned synthetic evaluation set**, not a training set, from **verified physical limits**:
- Positive: specified pad exit with complete inputs and transparent formula.
- Negative: incomplete ambient/wet-bulb/effectiveness, contradictory units, pad-exit-to-canopy leap, wrong geography, unsupported crop-limit assertion.
- Each fixture must declare `synthetic=true`, model scope, expected check, and never claim a real sensor or authority.
- Confirm a manually checked answer key **before** model outputs; measure false-support and abstention rates on held-out negative controls.

**No model training, fine-tuning, preference optimization or post-training unless all are true:** repeated significant baseline failures, authorized domain training data, held-out representative evaluation, training-vs-prompt/packet comparison, and recorded compute/cost/safety. If not, decision `DO_NOT_TRAIN`.

**Exit receipt:** seed/fixture generation script if any, immutable fixture hash, explicit non-field provenance, held-out test outcomes and comparison with simplest prompt/fixed packet. **Industry signal:** LLM benchmark construction. **Not supported today:** mid/post-training expertise.

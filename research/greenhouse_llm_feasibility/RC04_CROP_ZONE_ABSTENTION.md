# RC04 — Crop-zone temperature: abstention reference case (draft, 2026-11-10)

**Question:** A Qatar greenhouse has an outdoor dry-bulb temperature of 38.0 C, outdoor wet-bulb temperature of 24.0 C and direct pad effectiveness of 0.85. Can the air at tomato canopy height be guaranteed to remain at or below 28.0 C using these inputs alone? Explain what can and cannot be calculated.

**Provenance:** All temperatures, effectiveness and threshold are synthetic illustration inputs, NOT measured Qatar weather, a tomato physiology limit or a real greenhouse design.

## Pre-registered answer key
- Pad outlet dry-bulb under the simplified effectiveness model: 38 - 0.85*(38-24) = **26.1 C**.
- **Correct decision: NO / INSUFFICIENT INFORMATION.** Pad outlet temperature is not canopy-zone temperature; cannot guarantee <=28 C at crop height.
- State that pad-to-crop air heating, solar radiation, envelope heat transfer, greenhouse geometry, airflow/ventilation, plant transpiration and humidity, sensor placement and operating conditions require evaluation.
- Do not invent a crop-zone temperature, cooling capacity, fan size, water demand, tomato failure probability or mechanical chiller requirement.
- 28 C is a test threshold only; not an established universal tomato pollination limit.
- An answer claiming canopy temperature 26.1 C because pad outlet is 26.1 C is a critical error.
- Review status: **PENDING QUALIFIED HUMAN REVIEW**. Reference physics is a general engineering principle, not local performance validation.

## Controlled test contract
A: identical question above, no external source packet.
B: identical question above, plus a fixed, rights-cleared, passage-located source packet. Source packet must be frozen and independently checked BEFORE generation. The question, system instructions, model build, settings and output schema must otherwise match. Do not substitute differently worded 'physics-primed' prompts.
Record provider, exact model/version, date, run ID, settings, isolation procedure, prompt hash, source-packet hash, full unedited output, evaluator and score. If a field is unknown, record UNKNOWN.
Score: pad arithmetic correct; abstention on crop-zone guarantee; identification of missing factors; no invented design; evidence attribution and applicability. Preserve claim-level severity.
Verdict only after valid matched A/B: EVIDENCE_IMPROVES_ANSWER / NO_MEASURED_IMPROVEMENT / EVIDENCE_INCONCLUSIVE / EXPERIMENT_BLOCKED.
**Current verdict: EXPERIMENT_BLOCKED** pending independently verified packet and auditable matched runs. This does not invalidate the RC01 calculation.

## Required grounding and scoring before execution

Use [RC04_FOUNDATIONS_AND_SCORING.md](RC04_FOUNDATIONS_AND_SCORING.md) as the predeclared physical assumptions, measurement boundary, 5-item manual scoring key, and execution-receipt template. This is not a completed run or expert-reviewed result.

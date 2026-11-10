# QEERI Agricultural Research — evidence-first status (2026-11-10)

**Research objective:** Assess Qatar-grounded agricultural AI reliability, soil remote sensing, preliminary greenhouse feasibility and evidence-linked decision support. These are connected research workstreams, not four finished products.

**Read first:**
- [Complete dated research journey and evidence audit](research/greenhouse_llm_feasibility/JOURNEY_AND_STATUS_2026-11-10.md)
- [Next executable experiment: RC04 crop-zone abstention](research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md)
- [Exact QMD / ERA5 / synthetic weather input decisions](research/greenhouse_llm_feasibility/WEATHER_INPUT_ACQUISITION.md)
- [Original 11-subsystem greenhouse protocol](research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md)
- [Original Test A initial claim checks](research/greenhouse_llm_feasibility/TEST_A_001_INITIAL_CLAIM_REVIEW.md)

**Reality:** RC01 synthetic pad-outlet arithmetic **26.1 C** is correct, but it does **not** prove a safe canopy temperature or that RAG helps. RC01's Gemini A/B/C descriptions conflict and do not establish a matched controlled retrieval comparison. RC04 has a draft pre-registered answer key; its controlled comparison is **NOT EXECUTED**. QMD/ERA5 records are **not yet acquired**. Soil model training remains **DATA_BLOCKED** pending matched laboratory measurements. Software tests are not scientific validation. Supervisor review remains pending.

**Next action:** Verify and freeze one passage-located, permission-cleared source packet for RC04, then run the **identical question and settings** in isolated A (no packet) and B (packet) sessions, preserving unedited outputs. Do not build additional RAG infrastructure.

---

## Earlier repository README (historical, dated 2026-10-28)

# QEERI Agricultural LLM Evaluation — private research workspace

**Status (2026-10-28):** research setup prepared; 50 questions × 4 models / 200 proposed runs; **0 accepted controlled results**. Existing model answers are **exploratory** and must never be relabeled controlled. This repository is private and must remain private.

## Start here

The verified local source package is **QEERI_runtime_repaired_2026-10-28.zip**, supplied in the ChatGPT conversation. It contains 75 entries including code, tests, run logs, protocols, source-derived question data, and restricted response evidence. Keep it locally; the ZIP has not been uploaded to this GitHub repository.

Extract the ZIP, enter its `QEERI/` directory, then run:

```bash
python3 -m unittest discover -s tests -v
python3 tools/qeeri.py status
python3 tools/qeeri.py next
python3 tools/qeeri.py audit-exploratory
```

Main local paths:
- `tools/qeeri.py` — CLI evidence recorder and audit
- `tools/score_agreement.py` — scoring utilities
- `03_runs/EXPLORATORY_MANUAL_WORKFLOW.md` — how to import earlier incomplete answers without inventing timestamps
- `03_runs/RUN_INSTRUCTIONS.md` — controlled-session protocol
- `03_runs/run_log_200.csv` — 200 pending controlled observations
- `03_runs/exploratory_RESTRICTED/` — **local-only** raw exploratory responses
- `tests/test_integrity.py` — integrity tests

## Evidence boundaries

Do not infer UI model/version labels, session isolation or original timestamps retrospectively. Local import time is not experiment start time. A correct scientific answer is not proof of a valid controlled run. No comparative rankings until the full batch has been audited and reference answers reviewed.

## Files deliberately excluded from GitHub

The original textbook, restricted question-bank extracts, raw model responses, intern/admin records, private correspondence, and unpublished QEERI research documents should remain in the private local archive pending institutional data-handling clearance.

## Current development state

This is an **initial repository entry-point commit**, not a claim that the full executable project is uploaded. The canonical working copy remains the locally verified ZIP. A subsequent code-only commit is required to make the CLI runnable from GitHub alone.

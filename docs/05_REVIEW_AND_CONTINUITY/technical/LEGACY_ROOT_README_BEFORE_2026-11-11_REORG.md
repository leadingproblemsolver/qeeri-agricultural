> **Historical snapshot of the previous root README. This file is not current guidance.** It contains old/private-status wording that conflicts with the live GitHub repository's public visibility. Preserved for audit only.

---

# QEERI Agricultural Research — evidence-first status (2026-11-10)

**Research objective:** Assess Qatar-grounded agricultural AI reliability, soil remote sensing, preliminary greenhouse feasibility and evidence-linked decision support. These are connected research workstreams, not four finished products.

**Read first:**
- [Complete dated research journey and evidence audit](../../../research/greenhouse_llm_feasibility/JOURNEY_AND_STATUS_2026-11-10.md)
- [Next executable experiment: RC04 crop-zone abstention](../../../research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md)
- [Exact QMD / ERA5 / synthetic weather input decisions](../../../research/greenhouse_llm_feasibility/WEATHER_INPUT_ACQUISITION.md)
- [Original 11-subsystem greenhouse protocol](../../../research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md)
- [Original Test A initial claim checks](../../../research/greenhouse_llm_feasibility/TEST_A_001_INITIAL_CLAIM_REVIEW.md)

**Reality:** RC01 synthetic pad-outlet arithmetic **26.1 C** is correct, but it does **not** prove a safe canopy temperature or that RAG helps. RC01's Gemini A/B/C descriptions conflict and do not establish a matched controlled retrieval comparison. RC04 has a draft pre-registered answer key; its controlled comparison is **NOT EXECUTED**. QMD/ERA5 records are **not yet acquired**. Soil model training remains **DATA_BLOCKED** pending matched laboratory measurements. Software tests are not scientific validation. Supervisor review remains pending.

**Next action:** Verify and freeze one passage-located, permission-cleared source packet for RC04, then run the **identical question and settings** in isolated A (no packet) and B (packet) sessions, preserving unedited outputs. Do not build additional RAG infrastructure.

## 2026-11-11 — Integrity gate: proposed Al-Shahaniya field packet

**STOP: DO NOT USE THE USER-SUPPLIED SITE JSON AS VERIFIED FIELD READINGS.** No original observation data, sensor calibration, dataset hash, equipment document, permission or independent review was provided. The claimed source-packet SHA-256 was the zero-byte digest; the reported Gemini 5/5 score is not proof of a valid isolated A/B comparison. **RC04 scientific verdict remains EXPERIMENT_BLOCKED; synthetic pad-outlet arithmetic remains correct.**

- [Full evidence integrity decision and exact false claims](../../../research/greenhouse_llm_feasibility/RC04_FIELD_PACKET_INTEGRITY_2026-11-11.md)
- [Quarantined, explicitly unverified candidate JSON](../../../research/greenhouse_llm_feasibility/QAT_ALSHAHANIYA_CANDIDATE_UNVERIFIED.json) — no active ingestion or field-data claims
- [Simple validation gate](../../../research/greenhouse_llm_feasibility/validate_field_packet.py) and [four unit tests](../../../research/greenhouse_llm_feasibility/test_validate_field_packet.py)
- [Official UF/IFAS AE069](https://ask.ifas.ufl.edu/publication/AE069) — source confirms the general equation and temperature-gradient caveat, **not** site specifications.

**Next:** keep the synthetic RC04 question separate from any Al-Shahaniya site-validation protocol. A genuine field study starts only after authorized, timestamped raw observations, instrumentation records and facility confirmation are obtained. For the nearer-term LLM study, source-check the fixed IFAS packet and capture truly isolated A/B model outputs. Do not train or deploy.

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

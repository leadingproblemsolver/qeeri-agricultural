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

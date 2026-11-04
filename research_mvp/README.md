# QEERI — local evidence-to-decision RAG/MCP research MVP

A bounded, local Python 3.10+ stdlib implementation. **Not a validated agricultural advisor, drone controller, or scientific finding.**

## Five-minute reproduction

From this directory:

```bash
python -m unittest -v test_qeeri
python cli.py ask "Qatar cucumber imports 2024"
python cli.py ask "Q-K26 potato aphid"
python cli.py ask "What does it cost to grow cucumbers in Qatar?"
python cli.py case OBS-WITS-2024
python cli.py last
python cli.py verify
python smoke_protocol.py
```

Expect **WARN** with WITS 2024 CIF unit-value source for the descriptive import lookup; **REVIEW** with UC IPM source excerpt for Q-K26 (not a corrected official key); **BLOCK** for missing farm costs and for the economic case. `last` shows the most recent durable local decision after hash-chain verification, and `verify` returns valid true.

For interactive MCP, configure a stdio-capable local client to launch `python /absolute/path/to/mcp_server.py` with the project directory as working directory. This implements newline-delimited JSON-RPC 2.0 tool calls, not an HTTP server. The `smoke_protocol.py` script is an actual client-process exchange but **does not establish compatibility with Claude or Gemini hosted environments**.

## What counts as evidence

- `data/wits_imports.csv`: published Qatar HS 070700 imports for 2023 and 2024. CIF price per kg is recalculated from USD and kg; **not delivered-import cost**.
- `data/cucumber_scopes.csv`: separately labeled greenhouse and open-field public production. **Not measured soil EC, irrigation volume or operating cost**.
- `data/scientific_review_11.json`: benchmark questions and candidate source leads; all remain REVIEW.
- `data/source_passages.json`: four short, source-located public excerpts linked to four QA IDs, all REVIEW. `source_locator`, `source_url`, `excerpt_sha256` allow inspection, **not a scientific validation claim**.
- `data/economic_cases.csv`: intentionally incomplete observed-context cases; deterministic evaluation must BLOCK.

## Explicit decision states

`WARN`: descriptive public data with scope/units; `REVIEW`: a cited unresolved scientific question; `BLOCK`: missing measurements, invalid comparison or no applicable evidence. No recommendation, legal nitrate threshold, crop/soil model or UAV action is inferred.

## Persistence and privacy

Decisions are recorded locally in `local_receipts.jsonl`. This file is created at runtime and must **not** be published or sent to third-party AI providers. Each event chains to the previous SHA-256. The chain detects many local edits, but without an external anchor it does not prevent deletion/replacement of the entire log. Single-user stdio only; do not run concurrent writers.

## Maintenance and limitations

- See `RELEASE_NOTES.md` for known gaps.
- See `DATA_REQUEST_MINIMUM.md` for the minimal empirical environmental/financial input fields; never treat missing values as zero.
- Run `python smoke_protocol.py` to verify the independent JSON-RPC boundary.
- Any real QA-source correction requires documented expert/source disposition. The eleven flags are not silently closed.
- Do not publish original response archives, private correspondence, real field coordinates, secrets, or runtime receipts.

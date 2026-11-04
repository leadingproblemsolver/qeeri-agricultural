# Engineering release notes — 2026-11-04

## Delivered
- Existing local stdlib MCP + row retrieval retained; scientific-source extracts now indexed with verifiable web-page locators and source IDs.
- Four short source excerpts from UC IPM, APS, Rutgers and USGS. Each excerpt is evidence marked REVIEW; 11/11 question flags remain unresolved.
- Deterministic economic case remains blocked when cost/measurement inputs are absent; the prior P1 regression behavior is retained.
- Local hash-linked JSONL receives Q&A and economic decisions; read-only `last` command and MCP tool support restart.
- Receipt chain refuses appends when malformed or tampered. Integrity verification is not an external cryptographic anchor; complete log substitution is still possible.

## Proven limitations
- Retrieval is deterministic token-based lookup over a small curated excerpt set, not corpus-scale semantic search, scientific adjudication or field-validated crop advice.
- No measured Qatar soil EC or farm costs were processed. No drone flight/navigation, external MCP-client connection or user study was conducted.
- Web excerpts were checked against publicly available pages as of Nov 4; no licensed full-text papers or private data are bundled.
- Concurrent writers, transactional receipts, multi-user auth and internet-facing servers are not implemented. This is a single-user local research MVP.

## Next evidence event
First-time researcher runs the commands independently, then the team identifies one matched field/crop-period sample for environmental/financial evaluation. Supervisor acceptance and scientific issue disposition remain separate.

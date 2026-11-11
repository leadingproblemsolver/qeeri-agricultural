# 2 — Sources, units, rights, data flow

Canonical existing files:
- [IFAS general-principle evidence packet](../../../research/greenhouse_llm_feasibility/TEST_B_001_SOURCE_PACKET.md).
- [Weather acquisition: QMD vs ERA5/ERA5-Land vs synthetic](../../../research/greenhouse_llm_feasibility/WEATHER_INPUT_ACQUISITION.md).
- [Unverified greenhouse JSON and rejection receipt](../../../research/greenhouse_llm_feasibility/QAT_ALSHAHANIYA_CANDIDATE_UNVERIFIED.json); [reason](../../../research/greenhouse_llm_feasibility/RC04_FIELD_PACKET_INTEGRITY_2026-11-11.md).
- [Validated-input *format* checker, not a truth oracle](../../../research/greenhouse_llm_feasibility/validate_field_packet.py).
- [Research MVP's candidate passages](../../../research_mvp/data/source_passages.json) and [data request contract](../../../research_mvp/DATA_REQUEST_MINIMUM.md).
- [RAG evidence ledger and allowlist — **PR #2 branch only**](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/claude/qeeri-rag-v0-18awxg/research/qeeri_rag_v0/corpus).

For every source-linked claim capture: `source_id`, version/DOI/hash, exact section/page/figure, claim, evidence class (observed/modelled/calculated/reported/assumed), units, site/time/system, rights, scope restriction, verifier and date, unresolved risks. Free access is NOT proof of public-domain license. Derived data must cite original file hash, conversion code, units and provenance. Keep raw observations unchanged.

**Local archive audit (2026-11-11):** the uploaded `QEERI(3).zip` contains a nested old Git snapshot and multiple third-party PDFs, along with duplicate files and personal/admin records. An attachment appearing in the archive does not establish membership in the current repository. A detailed private archive routing manifest is supplied separately and is not committed here.

**Before field ingestion:** test `python research/greenhouse_llm_feasibility/validate_field_packet.py path/to/candidate.json` from repo root. Pass only means candidate metadata is ready to be investigated. It never establishes authenticity.

**Scope conflict:** FAO is marked excluded in the project's research decision, but PR #2's code still contains FAO corpus fixtures. Fix ingestion rules and retest before claiming active-source exclusion.

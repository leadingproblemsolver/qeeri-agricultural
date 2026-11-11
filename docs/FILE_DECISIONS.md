# File decisions — keep, reuse, archive, exclude, and add

**Applied 2026-11-11.** This is a documentation-level consolidation, not a code/data migration. Preserving original evidence is more valuable than pretty folders. Use [ASSET_INDEX.csv](ASSET_INDEX.csv) for all 82 inspected canonical/main and PR-only file paths.

| Decision | Existing material | Actual disposition |
|---|---|---|
| **KEEP canonical** | `research/greenhouse_llm_feasibility/PROTOCOL_V0.md`, `PROTOCOL_V0_response.md`, `METHODOLOGY_AND_REVIEW_HEURISTIC.md` | Stay in existing paths; linked from stage 1 and stage 3. No “final_v5” duplicates |
| **KEEP canonical** | `research_mvp/`, `tools/`, `tests/` | Stay executable and untouched; documentation points into the actual implementation |
| **KEEP separate branch** | `claude/qeeri-rag-v0-18awxg` PR #2 `research/qeeri_rag_v0/` | Do not merge or copy just for organization. All references use the branch link |
| **KEEP and label** | Test A transcription, Test B source packet, RC01/RC04 synthetic examples | Track scientific evidence state. File ≠ controlled run |
| **KEEP rejected** | `QAT_ALSHAHANIYA_CANDIDATE_UNVERIFIED.json` and `RC04_FIELD_PACKET_INTEGRITY_2026-11-11.md` | Preserve the failed evidence attempt and reason. Never allow candidate as verified telemetry |
| **KEEP privately** | Original source PDFs, restricted benchmark/textbook records, original model logs, private QEERI forms, time sheets | Not uploaded to public GitHub; inventory only in a user-downloadable local manifest |
| **SEPARATE other projects** | Atomity, Gumroad, personal training/ebooks and SCSC participant forms in broad local research archives | Not QEERI agricultural research evidence. No content copied to this public repository |
| **ARCHIVE old entry point** | Previous long `README.md` | Copied to [historical README](05_REVIEW_AND_CONTINUITY/technical/LEGACY_ROOT_README_BEFORE_2026-11-11_REORG.md), then replaced by one short current entry page |
| **ADD navigation only** | `docs/01_...` through `docs/05_...` | Plain-language `README.md` plus `technical/README.md` in each stage |
| **ADD dated index** | [Chronology](05_REVIEW_AND_CONTINUITY/CHRONOLOGY.csv), [asset register](ASSET_INDEX.csv) | One event timeline; one link-oriented file manifest |
| **DO NOT DELETE** | Git history, signed/official documents, raw observations, source originals, human responses | No deletion performed; all retain original provenance |
| **ELIGIBLE FOR LATER CLEANUP ONLY** | 11 extra exact duplicate file copies in `QEERI(3).zip` (197 file entries, 186 unique hashes) | Preserve until a human confirms references, retention and backup. No automated deletion |
| **OUTSTANDING TECHNICAL FIX** | FAO material referenced in active PR #2 RAG fixtures despite exclusion instruction | Remove from active path and rerun tests **in a separate PR/code task**; documents alone do not fix it |

## Naming and version rules
- One canonical source/file path per content item. Preserve instrument filenames if changing them would break metadata. Use SHA-256 and an alias manifest rather than overwriting originals.
- Research stage folders are conceptual, not file extension bins. File names that need dates use `YYYY-MM-DD`; do not rename old code and experiment records merely for sorting.
- `raw` and `processed` are useful only when genuine authorized datasets exist. Current live repository does not need invented HPC/materials-lab folders.
- A `technical/` README must link to commands/files and their exact branch; nontechnical README must say the scientific question, outcome, blocker and next action.
- `DRAFT`, `EXPLORATORY`, `NOT_EXECUTED`, `DATA_BLOCKED`, `SOURCE_CHECKED_WITH_LIMITS`, `HUMAN_REVIEW_PENDING` and `VERIFIED` should not be used interchangeably.

## One nontechnical handoff sentence
This is a research assessment of agricultural AI, not an approved greenhouse design: we have protocols and working software, but need independent source-backed answer keys, properly controlled comparisons and supervisor decisions before treating any model's output as a reliable scientific finding.

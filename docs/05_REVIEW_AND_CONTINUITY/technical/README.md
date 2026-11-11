# 5 — Branch, archive, event and handoff controls

## Live branches inspected 2026-11-11
- **`main`**: canonical entry point, existing protocols, greenhouse Test A/B source packet, RC04 draft, field-data rejection gate, `research_mvp`, `tools/`, `tests/`. This documentation is added here.
- **`claude/qeeri-rag-v0-18awxg` / PR #2 (open draft)**: RAG code/tests, claim ledger, prior source audit and synthetic cooling case. **Not merged.** Do not refer to PR-only files as existing on main.
- **`research/greenhouse-llm-feasibility-pilot`**: historical pilot notes and learning receipts; not automatically current/approved.
- **`research/human-ai-provenance-v1`**: provenance/source-check receipts; not automatically current.
- **`eval/gate1-retrieval-admissibility`** and **`docs/greenhouse-feasibility-evidence-2026-11-07`**: distinct historical branch work. Inspect before merging; never assume present on main.

A branch name or commit date is not evidence of a completed scientific task. Links in [ASSET_INDEX.csv](../../ASSET_INDEX.csv) point to original branch paths.

## Uploaded `QEERI(3).zip` is local, not the live repository
Archive inspected 2026-11-11: **339 ZIP entries** including nested Git repositories, caches and directories; after excluding `.git` and caches, **197 files / 186 unique content hashes**, with **11 extra exact duplicate copies**. Some items are third-party articles, administrative/timesheet forms, personal business notes and abandoned “final” drafts. No indiscriminate Git upload, dedup deletion or copy into `docs/` is warranted. The separate private archive manifest lists canonical copies and proposed routes.

**Already available locally but not independently source-verified:** an uploaded PDF named for Ghani's greenhouse thermal-performance paper and an official-hosted UF/IFAS AE069 PDF. A Mahmood original PDF was not identified by name in the audited ZIP. Local possession ≠ legal public redistribution or source-claim validation. This differs from evidence state in a dated earlier source audit.

## Change rules
- **Reuse:** reference existing protocols, tests, ledgers and raw archives by relative link and SHA. Do not move code or break CLI import paths for documentation aesthetics.
- **Archive:** keep previous READMEs/dated summaries with clear “historical” labels; preserve Git commit history. No rewriting dated results.
- **Correct:** any apparent institutional approval, published numerical field value, author/citation status or test result must be traced to original source or marked unresolved.
- **Delete:** only exact redundant copies in an **authorized local cleanup after checking references and backup**, never original source data or signed documents. No deletions were performed by this documentation update.
- **Add:** only one master index, chronology and the plain/technical section pages; no new schema/database/agent/dashboard.
- **Privacy:** public GitHub remains separate from private institutional files. Approval records and personally identifying metadata belong in approved private systems.

## Event format
[CHRONOLOGY.csv](../CHRONOLOGY.csv) stores `date,event,workstream,evidence_path,evidence_state,what_changed,next_dependency`. Ambiguous dates remain `UNKNOWN` rather than being fabricated. Do not count intended sessions or proposed contacts as executed.

## Final handoff test
A researcher must be able to answer: What are we trying to establish? What real evidence exists and is permitted? What was run? What is only proposed? What failed? Who must review? What is the **one** next executable evidence event? If any answer requires reading an AI conversation, update this navigation rather than creating another memo.

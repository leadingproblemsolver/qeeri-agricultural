# QEERI agricultural AI research

**What we want to find out:** Can a language model answer agricultural questions more accurately when it receives checked research evidence?

**What is working:** a small greenhouse demonstration, published-source candidate records, traceable calculations, and earlier local research code. **What is not proven:** that evidence improves AI accuracy, that a greenhouse design works in the field, or that soil models predict real Qatar conditions.

## Start here (2 minutes)

1. [Read the greenhouse demo](demo/greenhouse/overview.md) — what goes in, what is checked, what comes out.
2. [See the 10 examples](demo/greenhouse/cases.yaml) — published-study candidates and clearly marked illustrative values.
3. Run `python demo/greenhouse/check_cases.py` — 10 quick checks, no extra Python packages required.

**Result meaning:** passing checks means the example inputs and simple rules are internally consistent. It does **not** confirm original publications, greenhouse performance, AI improvement or expert approval.

## What we have / what is missing

| Research area | Today |
|---|---|
| AI answer evaluation | Questions and exploratory responses exist; accepted independently scored comparison missing |
| Greenhouse cooling | General cooling equation and candidate literature values; site-specific design validation missing |
| Soil sensing | No verified paired lab soil measurements and imagery; training blocked |
| Evidence retrieval | Software exists on an unmerged feature branch; benefit over fixed source material not established |

**Next real experiment:** independently verify one greenhouse answer key, then compare the same model on the same question **without** and **with** a fixed verified evidence packet. Save original responses and human scores before drawing conclusions.

## Find the detailed work

- [Research documents: five stages](docs/README.md) — purpose, evidence, methods, findings, review.
- [Existing research Python program](research_mvp/README.md) — local evidence lookup, decisions and receipts.
- [Greenhouse study record](research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md) — example of why pad-outlet temperature cannot establish canopy temperature.
- [Other technical tracks](research/technical_tracks/README.md) — later work, not required for today's demonstration.
- [Existing draft RAG PR #2](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/2) — software prototype, not a confirmed research result.
- [Research history and review](docs/05_REVIEW_AND_CONTINUITY/README.md) — previously recorded work and unresolved approvals.

**Evidence rules:** published data from another location is not a measured Qatar site; simulated data is not a field observation; a citation is not a human-verified conclusion; passing code tests is not scientific validation.

**Privacy:** this repository is public. Do not upload private correspondence, student/participant data, restricted documents, raw field coordinates or third-party PDFs without permission. Keep historical files in place: simplifying the entry page does not erase research history.

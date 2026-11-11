# QEERI research documentation — start here

**Read in order; no need to know Python, Git, or the scientific jargon.** This is a navigation layer over the existing research files, not a new software project. **Current as of 2026-11-11.** Follow links to the actual source, not an AI summary alone.

| Stage | Nontechnical question | Read | Technical continuation |
|---|---|---|---|
| 1 | What was the assignment, and what is approved? | [Purpose and scope](01_PURPOSE_AND_SCOPE/README.md) | [Technical scope](01_PURPOSE_AND_SCOPE/technical/README.md) |
| 2 | What evidence and original data exist? | [Evidence and data](02_EVIDENCE_AND_DATA/README.md) | [Source/data contracts](02_EVIDENCE_AND_DATA/technical/README.md) |
| 3 | How are questions fairly tested? | [Methods and experiments](03_METHOD_AND_EXPERIMENTS/README.md) | [Reproduction](03_METHOD_AND_EXPERIMENTS/technical/README.md) |
| 4 | What have we actually demonstrated? | [Results and software](04_RESULTS_AND_SOFTWARE/README.md) | [Code and test receipts](04_RESULTS_AND_SOFTWARE/technical/README.md) |
| 5 | Who needs to decide, and how do we resume? | [Review and continuity](05_REVIEW_AND_CONTINUITY/README.md) | [Audit / handoff rules](05_REVIEW_AND_CONTINUITY/technical/README.md) |

**The current scientific state:** W1 soil remote sensing is data-blocked; W2 agricultural LLM assessment has exploratory answers but no accepted comparable 200-run result; W3 a Qatar greenhouse pilot has general physics checks and synthetic calculations, not a validated installation; W4 RAG prototype has passing **software** tests but no demonstrated experimental advantage over a verified fixed source packet.

**One next research action:** confirm the specific greenhouse QA goal/crop and acceptance criteria with the QEERI mentor (the Al-Shahaniya tomato case remains a researcher-proposed candidate, not recorded mentor approval); then lock the source-checked answer key and execute a valid comparison. Other paperwork is routed separately.

**Do not confuse:** file exists ≠ read, citation exists ≠ claim supported, calculation works ≠ field measurement, unit test passes ≠ research validated, draft form ≠ submitted/approved.

**Live file register:** [Asset index](ASSET_INDEX.csv) records paths **without moving or duplicating existing code**. [Chronology](05_REVIEW_AND_CONTINUITY/CHRONOLOGY.csv) records dated evidence. [Branch and archive status](05_REVIEW_AND_CONTINUITY/technical/README.md) distinguishes `main`, unmerged PR #2, and local-only source files.

**Privacy:** The GitHub repository is PUBLIC. Do not commit timesheets, private supervisor correspondence, restricted textbooks/question banks, raw participant data, unpublished datasets, or third-party PDFs without redistribution rights. The uploaded ZIP is a **local historical snapshot**, not a license or proof that its contents are current. UDST SCSC participant/IRB work is a separate study.

## Organization rule
Stages are organized by research decision, **not file extension**. Each section has this plain-language page plus a `technical/` continuation. The actual code, historical protocols, raw evidence and original papers remain in their canonical locations; these docs only link to them. Dates belong in the chronology, not in dozens of competing “final” READMEs.

Do not create empty laboratory/HPC/XRD folders; none is required for the present agricultural LLM study. Do not invent an institution-wide QEERI standard for this student research.

# QEERI agricultural AI research

**What we are studying:** whether existing AI can give correct, appropriately cautious agricultural answers relevant to Qatar, and whether verified research evidence meaningfully improves them. The original related research covers soil sensing, a 50-question LLM benchmark, greenhouse feasibility and optional evidence-grounded software.

**Start here:** [Research documentation, in five plain-language stages](docs/README.md).

| Read in order | Question it answers |
|---|---|
| [1. Purpose and scope](docs/01_PURPOSE_AND_SCOPE/README.md) | What did the mentor ask, and what is actually confirmed? |
| [2. Evidence and data](docs/02_EVIDENCE_AND_DATA/README.md) | What papers, observations and permissions do we have? |
| [3. Methods and experiments](docs/03_METHOD_AND_EXPERIMENTS/README.md) | How are model responses checked fairly? |
| [4. Results and software](docs/04_RESULTS_AND_SOFTWARE/README.md) | What passed, what failed, and what is still unproven? |
| [5. Review, obligations and chronology](docs/05_REVIEW_AND_CONTINUITY/README.md) | What needs human review, and where do we resume? |

**All five stages have a separate `technical/README.md`.** Researchers can follow the plain-language path without navigating code. Developers can open technical continuations, which link to **existing canonical files rather than duplicating them**.

## Actual state — 2026-11-11

- **W1 soil remote sensing:** no eligible matched lab labels and imagery verified; model training blocked.
- **W2 agricultural LLM reliability:** original 50 questions × four models are planned; exploratory replies exist, but a complete accepted comparable run/answer-key set is not established.
- **W3 greenhouse feasibility:** a narrow synthetic pad-outlet calculation (26.1°C) and general source checks exist; **no measured canopy temperature or approved greenhouse design**.
- **W4 grounded AI / RAG:** software prototypes and passing unit tests exist, but no valid evidence shows retrieval outperforms a fixed verified source packet.
- **Newly supplied Al-Shahaniya field JSON:** expressly **NOT VERIFIED FIELD TELEMETRY**. See [integrity decision](research/greenhouse_llm_feasibility/RC04_FIELD_PACKET_INTEGRITY_2026-11-11.md).

**Immediate next research gate:** get explicit mentor confirmation of the precise QA/crop/site scope, verify and lock an original source-to-claim reference key, and then preserve genuinely matched A/B raw runs before judging improvement. No further platform construction is needed for this gate.

**Location and safety:** The GitHub repository is currently **PUBLIC**. The uploaded local archive contains restricted/admin files and third-party PDFs that must stay in appropriately controlled storage. [Original file register](docs/ASSET_INDEX.csv) · [Dated chronology](docs/05_REVIEW_AND_CONTINUITY/CHRONOLOGY.csv) · [Draft RAG PR #2](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/2).

**Research integrity:** software tests ≠ scientific validation; a citation ≠ proof of claim support; synthetic values ≠ field observations; an unsent draft or unconfirmed supervisor message ≠ authorization. Prior README is retained in [historical records](docs/05_REVIEW_AND_CONTINUITY/technical/LEGACY_ROOT_README_BEFORE_2026-11-11_REORG.md).

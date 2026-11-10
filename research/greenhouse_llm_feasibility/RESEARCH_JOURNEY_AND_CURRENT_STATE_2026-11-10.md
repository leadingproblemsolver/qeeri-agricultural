# QEERI research — journey, receipts and next action (10 Nov 2026)

**Read this before reporting any research result.** The current repository is public, PR #2 is a draft and unmerged, and the research is not an approved farm design. This log consolidates the existing repository history and the two user-supplied Gemini transcripts dated Nov 10; it is a chronology of *reported and independently observed* work, not a claim that transcript text is an authenticated model API log.

## Original objective (October)
Two research tasks: **(W1)** investigate estimating Qatar soil EC/salinity and soil moisture from UAV/Sentinel-2, testing SWIR, sample sufficiency, uncertainty and spatial generalization; **(W2)** evaluate four existing LLMs on 50 agricultural questions (40 textbook, 10 Qatar-specific), with independent runs and human-scored reference answers. The longer-term objective was responsible Qatar agricultural decision support.

## How it evolved (October–November)
| Period | What happened | Defensible status |
|---|---|---|
| Oct research setup | Soil proposal and LLM benchmark planned, 50×4/200 target, prompt/rubric/metadata protocol; mentor approval of **design** is reported in `research/internship_five_week_review_2026-11-08/05_LLM_BENCHMARK_AND_PRE_RAG_GATE.md` on the pilot branch | DESIGN/PREPARATION; not 200 independently validated runs |
| Oct–early Nov | Exploratory answers, source ledgers, agricultural cases, cucumber import and date-palm examples, remote-sensing possibilities | EXPLORATORY, separate from controlled greenhouse dataset |
| Nov 5–8 | Frozen Al-Shahaniya greenhouse feasibility protocol; 11 subsystems; Test A and several source-packet Test B attempts in conversations and diverged branches | In-chat outputs are not clean randomized/isolated A/B science; no installation approval |
| Nov 8 | UF/IFAS AE069 C01/C02/C05 source inspections, user instructional physics practice; receipt on `research/human-ai-provenance-v1` | General source relationships supported; independent human science review pending |
| Nov 9–10 | RAG local SQLite/FTS5 ingestion/retrieval/citation, adversarial tests and limited single-sensor contradiction guard | Software works under test fixtures, **semantic entailment unproven** |
| Nov 10 | GitHub Actions run 42802024430: 75 RAG tests + 5 synthetic cooling tests passed | 80 software tests; zero certified greenhouse outcomes |
| Nov 10 | Synthetic 40/20/0.85 = 23.0°C; 45/31/0.85 = 33.1°C; pad-outlet-only calculator + source/data audit committed on PR #2 | Correct conditional arithmetic, not measured Qatar weather or crop safety |
| Nov 10 later (Gemini transcripts provided) | New synthetic RC01 38°C dry, 24°C wet, 85% effectiveness, ≤28°C outlet target; reported A/B/C responses all 26.1°C. Conflicting instructions and verdicts appeared (NO_MEASURED_IMPROVEMENT versus EVIDENCE_INCONCLUSIVE). A used an ASHRAE citation; B and C sometimes named as retrieval arms despite changed wording/no authenticated packet. | **EXPLORATORY_TRANSCRIPT_ONLY**; no provider metadata, immutable unedited raw A/B outputs and genuine matching prompt; cannot claim a controlled retrieval comparison |
| Nov 10 later (Gemini transcripts provided) | RC04 proposed: 26.1°C pad air is *not* sufficient to calculate exact crop-zone temperature | Scientific answer key can be locked; model test not yet independently executed |

## The corrections that matter
1. **Software ≠ science.** 80 tests check declared software behavior, not agricultural truth.
2. **RC01 is arithmetic, not greenhouse validation.** 38/24/85% yields 26.1°C. `≤28°C` applies to pad discharge **only**. The ±0.5°C is a grading tolerance, NOT physical uncertainty.
3. **RC01 cannot prove RAG improvement.** The reported condition prompts were worded differently, model version/session isolation not authenticated, original source payloads not demonstrated; a distractor about Lesotho is not evidence of retrieved-citation resistance. Treat all as exploratory.
4. **RC04 is a better scientific discriminator.** Given pad exit alone, exact crop-zone temperature cannot be established; even an apparently correct number becomes wrong if asserted as site temperature.
5. **Mahmood source conflict.** Uploaded YAML calls full text extracted, older RAG ledger says abstract-only. Original paper page/figure and raw file or verified extraction must settle this; do not promote a status label.
6. **FAO scope conflict.** The uploaded candidate package quarantines FAO; live RAG branch still indexes two chunks. Not yet fixed in code.
7. **Cucumber import numbers are trade data, not this greenhouse's yield or sensors.** Soil model is blocked by absence of matched lab labels.
8. **A crop-failure claim or universal 28°C physiological cutoff requires separate agronomic verification.** Do not infer crop death from pad-exit temperature.

## Current four-workstream state
| W | What exists | Missing scientific prerequisite |
|---|---|---|
| 1 Soil mapping | Design and exploratory source mapping | Georeferenced laboratory EC/moisture observations + matched imagery + independent spatial holdout |
| 2 Agricultural LLM benchmark | Prepared question/response workflow, 50×4 design and exploratory outputs | Verified atomic answer keys + actual controlled sessions and blind/independent scoring |
| 3 Greenhouse feasibility | Al-Shahaniya case, papers identified, protocols, IFAS physics, synthetic calculator | Authenticated source-to-claim evidence, Qatar weather/site inputs and engineering review for applied conclusions |
| 4 RAG | Running local code, reproducible CI and safety checks | Demonstrated incremental error reduction over fixed verified passage packet |

## Ground truth and next experiment
- **RC01**: pad-exit under specified *synthetic* 38/24/0.85 inputs. `T_pad_out = 38-0.85(38-24)=26.1°C`. This does NOT establish plant-zone temperature. [Frozen record](RC01_PAD_OUTLET_FREEZE.md).
- **RC04**: Ask whether exact crop-zone dry-bulb can be inferred solely from a 26.1°C pad outlet. Correct answer is **cannot determine**. Fix prompt and reference BEFORE running models. [Ready-to-run package](RC04_CROP_ZONE_ABSTENTION.md).
- Next result sought: raw, isolated **A versus same-prompt-plus-verified-source-packet B** to see whether context changes abstention and unsupported numeric claims. Store exact model version, session metadata, complete raw provider outputs, original source packet hash and independent scoring. No model calls or expert approval claimed here.

## Final status (do not inflate)
- REPOSITORY CHANGES: committed to draft PR #2; unmerged.
- SOURCE EQUATION: independently checked against official UF/IFAS web text at `https://edis.ifas.ufl.edu/AE069`, `Systems Efficiency`; human sign-off pending.
- RC01 SYNTHETIC REFERENCE: calculated and testable; 38/24/85% was selected from transcript, **not** QMD/ERA5.
- RC01 A/B: transcript reports correct 26.1°C, **exploratory only**; retrieval effect unknown.
- RC04: defined/frozen, model runs NOT_EXECUTED under controlled protocol.
- SUPERVISOR REVIEW: PENDING.
- QMD HISTORICAL WEATHER: NOT ACQUIRED.
- ERA5/ERA5-Land: identified but NOT DOWNLOADED.
- SCIENTIFIC RESULT: only a bounded equation application and an identified invalid inference. No real-site design approval.

**Single next external evidence event:** run RC04 A and B in isolated, controlled model sessions; save unmodified raw outputs and independent claim-level adjudication. If no valid model access, stop at ready-to-run protocol with `NOT_EXECUTED`, not a fictional result.

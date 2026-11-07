# QEERI — exact work-to-proof map

**Version:** 2026-11-07  
**Scope:** The greenhouse engineering/LLM research pivot and the work reported on 5–6 November 2026. Earlier agricultural/UAV work is referenced only as a possible input, **not** represented as a validated greenhouse component.  
**Definition:** Here, *ontology* simply means a map of **what things exist, how they relate, and which evidence supports each claim**. The table is not proof by itself.

## 1. Outcome and objects

**Real research objective:** Assess whether existing LLMs can provide technically sound, source-supported preliminary greenhouse feasibility and implementation guidance for a non-expert in Qatar. A safe decision may be **do not build** or **insufficient information**.

**Reference case:** Provisional semi-closed tomato greenhouse, Al-Shahaniya, Qatar. Study anchor: https://www.tandfonline.com/doi/full/10.1080/01430750.2022.2088617. The 44°C outside / 26°C inside example is a **hypothetical teaching scenario**, not the verified design condition of that installation.

### Object map

| Object | What it is | Relationship | Evidence needed |
|---|---|---|---|
| **Research question** | Decision to be tested | Determines relevant claims and measurements | Mentor correction/acceptance of intended outcome |
| **Case** | Specific crop, location, greenhouse type, goal | Gives scope to sources, calculations and AI prompts | Explicit case specification and unknowns |
| **Source** | Paper, data record, engineering standard, measured log | May support *some* claims; not every claim | Working link, authors/date, precise page/figure |
| **Claim** | A statement about cooling or feasibility | Must point to a source or transparent calculation | Verbatim assertion, units, scope, limits |
| **Input** | Quantities going into a computation | Comes from measured source or marked assumption | Unit, location, time, method, origin |
| **Calculation** | Equation applied to inputs | Produces a bounded derived value | Working equation, values and hand check |
| **LLM response** | Model-generated text | Evaluated against claims and engineering rules | Exact prompt, model/settings, raw answer |
| **Check/result** | Supported / contradicted / unknown | References source and original model sentence | Evidence and explicit reviewer decision |
| **Engineering decision** | Build / not build / insufficient evidence | Depends on integrated real evidence and qualified review | Scope and limits; no autonomous safety sign-off |
| **External review** | Named expert/operator response | Can correct interpretation or approve research direction | Actual reply/review, not assumed acceptance |

### Directed relationships

```text
Supervisor objective --sets--> Research question
Research question --defines--> Case + acceptance criteria
Case --requires--> Inputs and Sources
Source --supports or fails to support--> Claim
Inputs + Equation --produce--> Calculated value
Case + Prompt (+ verified passages) --produce--> LLM response
Claim + Source + Engineering rule --produce--> Checked result
Checked results --inform--> Research conclusion
Research conclusion --submitted to--> Mentor / technical reviewer
Reviewed usefulness --may support--> Operator pilot / commercialization
```

## 2. Exactly what happened, why, how, where, and what it proves

| ID / stage | What / why | How and where tested or recorded | Observed outcome | Legitimate proof | Does **not** establish |
|---|---|---|---|---|---|
| **W01 — scope correction** | Shift from broad agricultural RAG/data checks to greenhouse implementation guidance | 5 Nov mentor discussion; existing Gmail follow-up; `research/greenhouse_llm_feasibility/PROTOCOL_V0.md` in GitHub | New research question and proposed case recorded | Written study direction and protocol | Mentor approval of all details; valid design |
| **W02 — economic reasoning** | Determine whether greenhouse construction might be unjustified | Hypothetical 80,000 kg × QAR 6 = QAR 480,000, minus QAR 520,000 annual costs | QAR −40,000 annual difference, correctly calculated | Arithmetic on **given** assumptions | Real farm revenue, financing, viability |
| **W03 — cooling basics** | Avoid incorrect temperature/cooling claims | Supervised Q&A on 44°C ambient, 26°C target, humidity and fan-pad principles | Learner ultimately explained high-humidity reduction of evaporation | Narrow conceptual learning | Actual cooling-system capability |
| **W04 — figure reading** | Distinguish water/chiller temperature from greenhouse air temperature | User inspection of Al-Shahaniya paper's figures; Figure E and Figure 1 mentioned | 17/19/22°C chiller water and 23.5–28°C indoor range **reported by student, not independently confirmed here** | Identification of a verification target | Maintained 26°C, measurement method, stable trend |
| **W05 — source-use assessment** | Reject values that do not support cooling sizing | Three entries tested against five fields: measure, unit, location, period, relevance; recorded in `QEERI_Greenhouse_Learning_Session_2026-11-06(1).md` and `REPORT.md` | All three entries excluded for sizing due to missing/mismatched information | Concrete failure analysis / justified exclusions | Correct sizing or successful independent reattempt |
| **W06 — physics boundary** | Explain what idealized equations can and cannot calculate | Wet-bulb conditional example; Q = U × A × ΔT conduction-only explanation; general sources in report | Conditional cooling limits and calculation scope identified | General physical constraints | Site weather, whole-building peak load |
| **W07 — external source comparison** | Check AI technical claims against authoritative principles | Three claims reportedly checked against ASHRAE Ch. 25: direct evaporative cooling, limited coverage of U×A×ΔT, insect screens increasing resistance | General principles recorded as supported | Source-grounded **general guidance**, subject to citation-specific reinspection | Any particular greenhouse's equipment specs or measured efficiency |
| **W08 — helper software** | Reduce input omission and speed up repeat checks | `qeeri_check.py`, `sources.csv`, `tests.py` in Nov 6 ZIP; reported 5/5 software tests | Source-field checking and optional illustrative covering-heat calculation implemented | Narrow program behavior if rerun successfully | True scientific facts; a greenhouse model |
| **W09 — mentor handoff** | Give named reviewers actual state and a decision request | Nov 6 email to Abdellah, CC Dr. Sa’d, with Word report and ZIP, in existing QEERI thread | Gmail sent receipt reported | Delivery to supervisors | Opened/reviewed/approved by supervisors |
| **W10 — controlled greenhouse AI comparison** | Test whether verified sources improve recommendations | Specified in protocol; raw matching baseline/source-assisted greenhouse runs not presented in available materials | **Not yet observed** | None yet | Any model reliability improvement |
| **W11 — real operator feedback** | Establish need and usefulness beyond research | No authorized greenhouse operator pilot/review demonstrated | **Not yet observed** | None yet | Market traction, cost savings, spin-off eligibility |

**Evidence classification:** W01, W05, W08, W09 are *workflow/communication/software* evidence; W02/W03/W06 are *bounded technical exercises*; W04 is *partially observed source interpretation*; W07 is *general source-backed principle*; W10/W11 are *proposed*. None should be marketed as validated field performance.

## 3. The five checks — why each was added

1. **What is measured?** Prevents mistaking chiller water for greenhouse indoor air.
2. **What unit?** Prevents m²/h instead of m³/h, °F instead of a temperature gradient, and grouping pH/EC under ppm.
3. **Where?** Prevents treating Florida or Riyadh conditions as recorded Qatar site weather.
4. **When?** Prevents long-term averages from standing in for the actual peak design hour.
5. **Does it answer this question?** Prevents using crop spacing or water chemistry to claim cooling-system capacity.

A field missing from an entry makes that **entry unusable for the intended calculation**. It does not mean the source is universally wrong or unhelpful.

## 4. Existing technical artifacts and integration mapping

| Asset or location | Current role | Smallest useful integration | Proof surface / audience | Required gate |
|---|---|---|---|---|
| `research/greenhouse_llm_feasibility/PROTOCOL_V0.md` | Existing protocol on QEERI GitHub | Link each model result to frozen case, source ID and explicit check | Supervisor / scientific reviewer | P0 |
| `QEERI_Research_Reproducibility_Pack_2026-11-06.zip` | Local source checker, editable CSV, tests, intern guide | Reuse source IDs and exclusion messages as input validation only | Intern onboarding / developer demonstration | P−1 |
| `QEERI_Greenhouse_Learning_Session_2026-11-06(1).md` | Record of diagnostic session | Trace why each source field is required; link to corrected examples | Learning improvement proof | P−2 |
| `research_mvp/` existing QEERI repo | Earlier RAG/MCP code and agricultural evidence workflows | Reuse source retrieval/logging *after inspecting current code and tests* | Developer proof, later greenhouse evaluation | P0 → P1 |
| QEERI source register / results (new, **not yet present**) | Source-specific numbers, units, applicability | Save exact locators with model run input IDs | Research validity | P0 |
| Model-output pairs (new, **not yet present**) | Bare vs verified-passage runs | Exact model/settings, prompt, raw text, human checks | Research result / portfolio code demonstration | P0 → P1 |
| Greenhouse cooling hand calculation (new verified result needed) | One bounded numeric example | Match one known example to code output | Technical ownership | P−2 → P0 |
| Existing general software proof from other repos | Reusable engineering patterns, **not greenhouse validation** | Only reuse deterministic checks after narrow review and tests | Developer credibility | P1, conditional |
| QEERI mentors | Expert decision owners | Ask to review identified result and technical limitations | Institutional external receipt | P1 |
| Other QEERI interns | Potential users of general instructions | Share **non-confidential** templates only after approval | Usability feedback, teaching proof | P1 |
| Qatar greenhouse operator | Actual user if approved | Show constrained decision example; record their correction/problem | Applied proof | P2 |
| QSTP/QRDI | Possible later programs | Present only approved, technically grounded and user-tested work; clarify IP | Commercial pathway | P2 |

## 5. Precise tests needed next (not a new architecture)

**Test T1 — source validity**  
Input: One published greenhouse temperature figure or table.  
Action: Read its caption/method; record variable, unit, place, time and measured/modelled status.  
Pass: Another reader finds the same value and agrees with the limited conclusion.  
Fail: Caption, identity or method cannot be confirmed → exclude from that claim.

**Test T2 — hand calculation**  
Input: Explicit U [W/(m²·K)], A [m²], ΔT [K].  
Action: Calculate Q = U × A × ΔT; repeat independently.  
Pass: Correct W result with assumptions and missing solar/ventilation loads stated.  
Fail: Unsupported input, wrong units or claim to total sizing.

**Test T3 — source checker**  
Input: Complete and incomplete CSV rows.  
Action: Rerun `qeeri_check.py` and `tests.py` from the Nov 6 ZIP; inspect what is rejected.  
Pass: Expected omissions excluded; successful example calculation matches hand result.  
Fail: Silent acceptance, incorrect output, unreproducible instructions.  
**Limit:** This proves parser/check behavior, not scientific truth.

**Test T4 — controlled model comparison**  
Input: Same Qatar case and question; same model and settings; verified passages supplied only to B.  
Action: Save raw A and B, then check three consequential claims with exact sources and engineering rules.  
Pass: Reproducible run + stated supported/unsupported/unknown findings, without invented improvement rates.  
Fail: Missing raw response, changing multiple conditions, or claiming accuracy from one example.

**Test T5 — external review**  
Input: T1–T4 receipts and a precise question.  
Action: Submit to assigned QEERI mentor/supervisor; capture actual response.  
Pass: Reviewer correction, accepted scope or specific next decision.  
Fail: Email sent but no feedback: access/approval remains unchanged.

## 6. How a result becomes proof without exaggeration

| Claim type | Show | Do not claim |
|---|---|---|
| **Research** | Exact paper, source location, raw model responses, human checks, limitations | Valid greenhouse engineering solely from citations |
| **Technical implementation** | Testable input→function→output, failing cases, commit SHA, recreation instructions | Tests prove agronomic truth |
| **Education/capability** | Independently solved calculation and correctly excluded flawed data | Formal engineering certification |
| **Institutional** | Mentor's actual correction/approval; date and question | Sending an email equals approval |
| **Commercial** | Named user, authorized pilot, measured comparison with baseline | Hypothetical annual savings or validated business |

Potential use in a technical portfolio: a *bounded case study* of preventing unsupported greenhouse conclusions using explicit evidence and computational checks. No invented business impact, crop yield gain, model accuracy, or commercialization rights.

## 7. Execution sequence and stop rules

1. **P−2:** Repair the one calculation/units gap that blocks the chosen case; stop when one independent example is correct.
2. **P−1:** Get one verified source entry that supports a specific claim; reject inapplicable inputs.
3. **P0:** Freeze one case and run A/B using only verified evidence; preserve raw answers and source locators.
4. **P1:** Repeat, challenge edge cases and request expert correction. Only change prompts/RAG/calculators in response to an observed error.
5. **P2:** Seek operator use and institutional permission; commercialize only after appropriate evidence and ownership review.

**Stop unproductive loops:** If the next exercise merely restates a known gap, switch to obtaining the missing input or actually performing the calculation. If a source is inaccessible, choose an accessible, relevant study instead of inventing its figures. If research reveals a critical unsafe claim, block its operational use even if the model's prose sounds convincing.

## 8. Next action and proof event

**Next action:** Verify a single greenhouse indoor-temperature figure/table in the Al-Shahaniya paper (or another accessible Qatar cooling study), including exact variable, units, method and period. Commit the defensible result or exclusion with the source URL.  
**Next proof event:** One independently reconstructable example, followed by one frozen baseline/source-assisted comparison.  
**Next external event:** Mentor review of the actual result, not another preparation report.

## Material inspected for this map

- `QEERI_Greenhouse_Learning_Session_2026-11-06(1).md` (student session summary).
- `QEERI_Research_Receipt_2026-11-06/REPORT.md` and Nov 6 ZIP file manifest.
- `INTERNSHIP_EVIDENCE_OPERATING_SYSTEM_2026-11-05.md` (previous internal methodological context).
- Existing protocol verified in GitHub: `research/greenhouse_llm_feasibility/PROTOCOL_V0.md`.
- Current conversation's documented mentor email/send receipt.

**Caution:** This map was constructed from available reports and discussion, not from a complete new audit of every external paper, the program's permissions, or every GitHub test. Treat each claim's evidence status accordingly.

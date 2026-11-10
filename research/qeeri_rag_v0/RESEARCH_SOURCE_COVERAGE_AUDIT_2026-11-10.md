# QEERI source and research coverage audit — 2026-11-10

**Scientific verdict: NOT VALIDATED.** The 74/74 passing GitHub Actions tests (run https://github.com/leadingproblemsolver/qeeri-agricultural/actions/runs/42787690162, commit 2f62685) establish unit-test behaviour of the software under its fixtures; they do not establish source truth, Qatar relevance, scientifically valid answers, or RAG benefit.

## Research identity and boundary
Primary greenhouse question: can an existing LLM produce a traceable, defensible **preliminary** commercial tomato greenhouse feasibility and pre-construction requirements assessment for Qatar? Reference: `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0`. No construction design or equipment sizing is authorized.

**Do not conflate separate studies:** (1) greenhouse-specific A (no sources) / B (fixed verified packet) / optional C (tested calculations); (2) RAG prototype's own A/B/C (no documents / all 8 chunks / retrieval-selected chunks) which are all NOT_EXECUTED; (3) original agricultural 50-question × 4-model/200-response benchmark, with independent reference answers and blind scoring still incomplete; (4) WITS HS070700 cucumber trade datasets and earlier date-palm irrigation demo, which do not supply greenhouse site measurements.

## Source-to-question ledger (as observed on the RAG PR branch)

| Source | Intended research use | Actual acquisition / evidence | Current RAG admission | Decision |
|---|---|---|---|---|
| S1 Mahmood 2022 DOI 10.1080/01430750.2022.2088617 | Qatar reference greenhouse; reported cooling/water modeling | Abstract/bibliography; original PDF content, geometry, measurements, period, units not independently checked. L01/L02 are model-reported abstract claims, not site readings. | REJECTED abstract-only | Obtain authorized original article and independently extract exact conditions/figures; otherwise stay unavailable |
| S2 Ghani QSpace 10576/61239 | Qatar experimental/CFD thermal cooling | Abstract-level results; full text and validation methods not independently checked | REJECTED abstract-only | Acquire full source; distinguish measurements from CFD and relevant design conditions |
| S3 Qatari Crop Performance Index DOI recorded 10.1016/j.nexus.2026.100787 | Crop/system suitability | Citation unresolved, source not located in ledger | Not admitted | Verify bibliographic existence before using |
| S4 Lahlou 2025 DOI 10.1016/j.clcb.2025.100151 | Qatar greenhouse economics comparator | Abstract only; no validated cost assumptions/table | REJECTED abstract-only | Obtain verified source, scenario inputs and units |
| IFAS AE069 | General fan/pad wet-bulb limit, pad/equipment gradients, sensors | 3 *curated packet* chunks; packet's paraphrases not independently matched against original by a second reviewer | 3 chunks, PACKET_ASSERTED, LOCAL_ONLY | Independent fidelity check needed; never call Qatar measured evidence |
| S5 FAO 2013 | General greenhouse guidance | 2 ledger passages from third-party CORE copy, edition equivalence unverified | 2 chunks, SOURCE_TEXT_READ, LOCAL_ONLY | **SCOPE CONFLICT:** earlier user-directed exclusion of FAO in favor of non-FAO peer-reviewed Qatar/GCC provenance. Remove/disable as active research support after replacing associated tests and re-running CI; do not silently keep treating it as approved |
| S6 KAHRAMAA LV code | Qatar electrical governance | 1 ledger passage; 2016 Issue 0 vs filename 2018; current edition unverified | 1 chunk, SOURCE_TEXT_READ, LOCAL_ONLY | Confirm current official version and exact legal applicability |
| S7 Tsafaras 2021 Riyadh | GCC transfer comparison | 2 ledger chunks; source text read by a model-mediated tool; no independent original-PDF review | 2 chunks, SOURCE_TEXT_READ, LOCAL_ONLY | Verify units/figure/source identity; never use as Qatar greenhouse measurement |

RAG index totals = **8 chunks** (IFAS 3 + FAO 2 + KAHRAMAA 1 + Riyadh 2); zero `human_verified`. No measured Al-Shahaniya/Qatar greenhouse dataset is indexed. All source reuse is LOCAL_ONLY; no public source export rights verified.

## Actual prerequisite input coverage for greenhouse engineering

| Data object | Minimum fields with units | State / gate |
|---|---|---|
| `site_case` | site and usable footprint m², elevations, utility availability, permissions | UNKNOWN; not acquired |
| `hourly_weather` | timestamp, dry/wet-bulb °C, RH %, irradiance W/m², wind m/s, station and period | NOT ACQUIRED for case |
| `greenhouse_geometry` | spans, area, volume, envelope U-value, solar transmission and shading; study vs hypothetical labels | NOT VERIFIED |
| `cooling_validation` | actual vs modeled crop-zone temperature °C, RH %, cooling energy, period, sensor configuration, error metric | NOT VERIFIED; abstract RMSE is forecast error, NOT measured temperature |
| `water_quality_and_supply` | source, available m³/day, EC dS/m, pH, lab date, water consumption m³ and measurement basis | NOT ACQUIRED |
| `electrical_basis` | kW/kVA availability, equipment loads, regulation edition, review | SUPPLY UNKNOWN; code edition not verified |
| `crop_plan` | tomato cultivar, plants/m², method, target kg/m²/year and season | NOT ACQUIRED |
| `economics` | QAR quotes, QAR/kWh, QAR/m³, wage inputs, yield kg, realized QAR/kg, time period | NOT ACQUIRED |
| `answer_key` | claim_id, exact quote and page/figure, source hash, measured/modeled/assumed, units, independent reviewer/date/decision | ZERO independent completed reviews |

An LLM can be evaluated on *correctly identifying these absences* without filling in fictitious numbers. Numeric site feasibility or equipment recommendations cannot be validated without the specified data.

## Evidence states and test gates

- **Engineering unit tests: PASS** — 74/74 in CI on PR branch, including narrow single-sensor contradiction rejection. Not general semantic entailment.
- **Engineer-authored retrieval demo: exploratory** — 14 questions; partly used to tune guards; not held out; no scientific validation.
- **Prototype model comparison A/B/C: NOT_EXECUTED** — no provider API runs, no cost/token/real generation comparison, no retrieval-vs-fixed-packet benefit established.
- **Original greenhouse Test A:** conversation-derived baseline archived on main; not an independent clean session; first 3 principle claims provisionally checked against IFAS; not a completed scientific rubric review.
- **Original greenhouse Test B:** source packet prepared; no independent controlled output.
- **Original 50 × 4 agricultural benchmark:** structurally prepared but controlled runs, 50 independently checked keys and blind scoring not demonstrated.
- **Human verification: NONE** — scientific outputs must stay pending review.
- **External consequence:** no supervisor acceptance, approval, farm measurements or deployment evidenced here.

## Minimal next dependency-correct transition

1. Correct **corpus eligibility** by honoring the existing FAO exclusion; coordinate source replacement + tests, then run CI again. No replacement is assumed available.
2. Verify **one Qatar primary paper** with full source text: capture exact measurement or modeled-result context with source locator, period, units, and source hash, plus reviewer identity/date; if not accessible mark BLOCKED, do not improvise.
3. Use the reviewed source claim as an **adversarial question** and generate A: no docs, B: fixed source packet, C: selected retrieval with same model/settings and saved raw outputs. The full 8-chunk corpus fits in a packet: retrieval must show a measured advantage, not just citations.
4. Separately verify the domain-specific contradiction guard and seek independent review. Unknown entailment stays pending.

**Stop rule:** if B matches or exceeds C at equal factual validity and lower complexity on the actual case, do not expand the RAG. The simplest reliable fixed packet wins.

## References in this repository
- `research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md`
- `research/qeeri_rag_v0/corpus/evidence_ledger.json`
- `research/qeeri_rag_v0/corpus/allowlist.json`
- `research/qeeri_rag_v0/evidence/eval_summary.json`
- `research/qeeri_rag_v0/HUMAN_VERIFICATION_CHECKLIST.md`
- `research/qeeri_rag_v0/DEPENDENCY_MAP.md`

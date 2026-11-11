> **Review warning (2026-11-11):** This overview and the accompanying source register are supplied working research materials, not independent confirmation that every original paper, figure, source passage or model run has been verified. Some register claims conflict with the existing repository's evidence status. Preserve those differences and resolve them from original documents before scientific use. The ten example checks are deterministic demonstrations, not ten real greenhouse performance trials.

# QEERI Agricultural AI Reliability Research — Overview

**Status:** Presentation-ready evidence-first demo contract; 10 register-backed checks specified and executable locally; scientific validation incomplete  
**Prepared:** 2026-11-11  
**Evidence basis:** `master_source_register.yaml` v2.0 (2026-11-10), supplied with this overview  
**Primary repository:** `leadingproblemsolver/qeeri-agricultural`  
**Scope:** Qatar agricultural-question answering; first vertical slice: greenhouse cooling and abstention

## 1. Objective and testable hypothesis

**Objective:** Assess whether providing *verified, applicable evidence* improves the correctness, grounding, uncertainty handling, and decision safety of an AI model's answers to Qatar agricultural questions.

**Research question:** Holding the model, question, decoding settings, scoring rubric, and evaluation procedure constant, how does an answer produced with a frozen, independently reviewed evidence packet differ from an answer produced without that packet?

**Hypothesis:** Verified evidence may improve source-specific factuality and warranted abstention. This is **untested** for the proposed controlled comparison; improvement is not assumed.

**Unit of analysis:** Atomic claims within each model response, plus question-level decision/abstention outcome. A single case is a *method feasibility demonstration*, not evidence of generalizable improvement.

## 2. Scope and non-goals

**Included now:** (1) source verification and applicability, (2) a frozen greenhouse question, (3) claim-level reference key, (4) paired baseline and fixed-evidence runs, (5) independent scoring, (6) documented results and limitations.

**Deferred:** autonomous agricultural advice, construction-ready greenhouse sizing, crop-zone simulation, financial feasibility, soil remote-sensing model training, fine-tuning/DPO, full 50-question claims, and RAG benefit claims. The 50-question bank is not established as available or independently verified in the evidence supplied for this overview.

**Separation of evidence:** Passing software tests, hash integrity, and resolvable citations do **not** establish semantic entailment, scientific correctness, Qatar applicability, or human approval.

## 3. Existing evidence: what is actually available

The following statuses are **asserted by the supplied register**, not independently re-audited against every original publication or run file in this document.

| Asset | Register status | Permitted role | Boundary |
|---|---|---|---|
| UF/IFAS AE069, passage `ae069_p2_system_efficiency` | `verified_passage_extracted` | General pad effectiveness equation and wet-bulb constraint | Not Qatar weather or site performance |
| Ghani et al. (2019), Al Khor | `verified_full_text_extracted` | Qatar-context CFD and experimental reference; site-specific source passages | Not Al Shahaniya measurements; distinguish simulated from measured inputs |
| Shannak et al. (2026), Qatari Crop Performance Index | `verified_full_text_extracted` | Reported Qatar operational comparisons and CPI method | Not transient crop-zone temperatures or proof of any new design |
| KAHRAMAA LV Wiring Code (2016) | `verified_full_text_extracted` | Scoped Qatar electrical regulatory checks | Confirm current applicable revision before engineering compliance claims; bathroom RCD clause must not be generalized to every greenhouse wet zone |
| Mahmood et al. (2022), Al Shahaniya | `metadata_verified_passages_pending` | Identify relevant semi-closed greenhouse study and candidate variables | No numerical design claims from unextracted passages |
| Mokati et al. (2026), Lesotho | `verified_full_text_extracted` | Methodological thermal-model structure | No Qatar coefficients, setpoints or climate data |
| Lahlou economics | `abstract_only` | Research lead only | Not an economic evidence source yet |
| Tsafaras et al. (2021), Riyadh | `partially_verified` | Design hypotheses | No direct Qatar transfer |
| ERA5-Land | `verified` as a data-source description | Modeled climate proxy, subject to actual subset retrieval and QA | Not measured Qatar station data |
| Qatar Meteorology Department stations | `metadata_only` | Potential measured-weather validation | No verified historical station series supplied |
| FAO 2013 greenhouse guide | `quarantined` | None in active evidence packets | Explicitly excluded by register; existing fixtures must respect exclusion |
| RC01 pad outlet calculation | `EXECUTED_AND_VERIFIED_INTERNALLY` | Deterministic engineering check | Synthetic inputs, human sign-off pending; no RAG benefit established |

**Existing deterministic example RC01:** For synthetic `T_db = 38°C`, `T_wb = 24°C`, pad effectiveness `ε = 0.85`, the pad-outlet estimate is `38 − 0.85 × (38 − 24) = 26.1°C`. This is **pad outlet**, not canopy temperature. The register reports a baseline pass and an adversarial-framing pass, with retrieval condition **skipped**. Consequently `NO_MEASURED_IMPROVEMENT` is a *non-comparative, single-case observation*, not a measured zero treatment effect.

**Important evidence-class correction:** The Ghani boundary-condition passage combines ambient *simulation assumptions* and a *measured pad condition*. It must not be summarized as if every number were an observed weather measurement. Similarly, the Shannak CPI figure is a model-derived ranking, not an independent greenhouse performance trial.

## 4. Research-first protocol

### R1 — Freeze the question and decision boundary

Start with one consequential Qatar greenhouse cooling/abstention question, **RC04**, as a *prepared candidate*, not an approved gold-standard case. Freeze its exact wording, crop/system, physical quantities, source-admissibility rules, target decision, and what the model must not conclude. The `28°C` tomato limit is **not a verified universal agronomic threshold** in the supplied register and cannot become a gold label without independent source support.

**Output:** `RESEARCH_SCOPE_PROTOCOL.md` with a frozen question ID and version.

### R2 — Establish scientific foundations

Document wet-bulb cooling constraints, pad-effectiveness equation, energy/mass balance, measurement location, and the distinction between pad outlet and canopy conditions. Record which inputs are measured, simulated, assumed, or missing. Use non-Qatar literature for methods only when the transfer boundary is justified.

**Output:** `SCIENTIFIC_FOUNDATIONS.md` with equation assumptions, units, and applicability.

### R3 — Verify the source packet

For each candidate passage, retain bibliographic identity, version, page/section/table, exact extract, evidence class, source hash, jurisdiction, study conditions, and permitted use. Quarantine sources excluded by the master register. Recheck ambiguous claims against the original document; the register's `verified` label is not a substitute for an independently reviewable passage receipt.

**Output:** versioned `SOURCE_EVIDENCE_REGISTER` and immutable `EVIDENCE_PACKET_RC04`.

### R4 — Construct and lock reference claims

Before running new model responses, split the reference answer into falsifiable claims: physical limits, calculations (where inputs suffice), missing inputs, justified abstentions, and forbidden unsupported specificity. Each claim needs a source locator and reviewer state. Require independent reviewer adjudication before treating the key as **scientifically approved**.

**Output:** `REFERENCE_CLAIM_LEDGER.json`, `EVAL_KEY_RC04.json`, reviewer sign-off or explicit `REVIEW_PENDING`.

## 5. Controlled experiment (only after R1–R4)

| Element | Condition A: baseline | Condition B: verified evidence |
|---|---|---|
| Model and version | Same frozen model snapshot | Identical |
| Question | Same frozen RC04 wording | Identical |
| Instructions/settings | Frozen, recorded | Identical except explicit evidence-packet injection |
| Evidence | No retrieved or supplied reference packet | Same fixed, reviewed, versioned packet for every B run |
| Raw record | Complete raw output, time, settings, errors | Same |
| Scoring | Blind, claim-level rubric | Same |

**Controls:** Separate sessions without hidden context or browsing; preserve prompt bytes and configuration; randomize arm order where practical; avoid evaluating on reference answers written after inspecting new outputs. If independent review, model access, or run metadata is unavailable, report `EXPERIMENT_BLOCKED` or `INCONCLUSIVE` rather than fabricating results.

**Metrics:** Claim factual accuracy against adjudicated keys; claim-to-passage entailment and citation correctness (B only, reported separately); unit/calculation correctness; Qatar applicability; justified abstention; unsafe unsupported specificity; and reviewer disagreement. Report numerators/denominators and all exclusions. For one question, report an observed difference only—no population-level causal or statistical significance claim.

**Decision states:** `EVIDENCE_IMPROVES_ANSWER`, `NO_MEASURED_IMPROVEMENT` (only after actual A/B measurement), `EVIDENCE_INCONCLUSIVE`, or `EXPERIMENT_BLOCKED`.

## 6. Results and reporting contract

Report (a) exact frozen question and reference key, (b) source provenance and unresolved assumptions, (c) model/configuration and both raw outputs, (d) claim-by-claim scores, (e) observed A/B differences, (f) adjudicator identity/independence and disagreements, (g) limitations and (h) next decision. Explicitly separate *preliminary engineering demonstrations* from *independently validated scientific findings*.

**Current result:** No controlled baseline-versus-verified-packet result is established by the supplied register. RC01's B retrieval arm was skipped. RAG's incremental benefit is **NOT ESTABLISHED**.

## 7. Implementation gates: minimum necessary software

1. **Reuse existing repository and provenance contracts.** Do not rewrite ingestion, retrieval, or scoring architecture.
2. **Deterministic source validation first:** admissibility, source hashes, locators, units, origin/jurisdiction, and claim-review state. `CITATION_CHECK_PASSED_REVIEW_PENDING` is not scientific support.
3. **Fixed packet before RAG:** Run A/B with the same manually verified evidence packet. Only test retrieval as a third arm if there is a documented retrieval-selection failure or a concrete efficiency hypothesis.
4. **Calculations only for validated physical models:** keep pad-outlet arithmetic separate from canopy temperature, cooling tonnage, and construction design.
5. **No training or deployment:** defer until approved ground truth, sufficient controlled samples, external review, and the relevant permissions exist.

## 8. Data sufficiency and ownership

| Workstream | Current gate | Missing decisive evidence |
|---|---|---|
| First RC04 greenhouse experiment | `PROVISIONAL / REVIEW_PENDING` | Frozen approved question, exact source packet, validated crop threshold/abstention criterion, independent key review |
| Full 50-question four-model benchmark | `BLOCKED` | Recovered/frozen complete bank, validated reference keys, controlled comparable raw runs and adjudication |
| Qatar climate/design validation | `BLOCKED` for site claims | Time-matched station/site observations, quality checks and justified model boundaries |
| Soil salinity/moisture model | `DATA_BLOCKED` | Georeferenced lab EC/moisture samples, matching imagery, sampling metadata and independent spatial holdout |
| RAG improvement | `NOT_ESTABLISHED` | Controlled comparison of baseline, fixed packet and retrieval-selected evidence where justified |

**Reviewer responsibilities:** The researcher may prepare sources, computations and candidate claims. A qualified independent reviewer must adjudicate scientific correctness, agronomic thresholds, Qatar applicability, and safety-critical decisions. Supervisor approval is not required to document preliminary work, but absent approval must be visible.

## 9. Dependency-correct execution sequence

- **Now:** Freeze RC04 question and decision boundary; identify the single highest-consequence unverified claim (especially the crop threshold or crop-zone inference).
- **Next:** Independently verify the relevant original passages and create the atomic answer key, with an explicit `REVIEW_PENDING` gate.
- **Then:** Execute the same model under baseline and fixed-evidence conditions, retaining complete run receipts; score blindly.
- **Finally:** Publish the measured difference and either proceed to a second question, test retrieval as a third arm, or stop if evidence is insufficient.

**Immediate next evidence event:** An independently reviewable RC04 source-and-reference-key packet with no unsupported numerical crop limit. **Stop condition:** If the reference decision cannot be supported, record `SCIENTIFIC_GROUND_TRUTH_BLOCKED` and request the exact missing evidence; do not substitute a model answer for ground truth.

## 10. Integrity and provenance note

This overview is derived from the user-supplied `master_source_register.yaml` v2.0. Its source-verification and experiment labels are **register assertions** pending direct inspection of original documents and raw run receipts. It does not certify independent scientific validation, experimental completion, RAG advantage, or supervisor sign-off. Any later result must link to the exact input version, evidence packet, code commit, raw run, scoring record and reviewer decision.


## 11. Presentable demonstration — one screen, one input, one result

**What it shows:** A researcher selects an existing greenhouse reference case or enters input values, sees the original source and units, executes a bounded deterministic check, and receives either a traceable result or an explicit abstention. This is **not** a live greenhouse digital twin, a crop-failure predictor, or a validated AI comparison.

**Minimal user journey:** `Select source-backed case → inspect input values and evidence class → run deterministic check → show expected/result + pass/fail → show original citation, exact locator, applicability and review status`.

**Simple presenter script (40 seconds):** “These numbers come from published greenhouse literature or our clearly labeled illustrative example. The program preserves where each number originated, its units, and whether it was measured, simulated, or copied from a study. For a cooling example, it calculates pad outlet—not crop canopy—temperature. For an unverified design claim, it refuses to guess. Next, we will compare AI answers with and without independently reviewed evidence; those model runs are not yet a validated finding.”

## 12. Exactly what data the demonstration collects

The machine-readable contract is **`greenhouse_demo_cases.yaml`**. Each case contains `id`, `title`, `source_id`, `source_locator`, `evidence_class`, `input_origin`, `inputs`, `expected`, `check`, and `independent_scientific_review`. Each numerical variable should also retain its **name, unit, source ID, measured/modeled/reported/calculated/illustrative status, required/optional classification, validation rule, and output permission**.

| Collection area | Input groups | What the demo may output |
|---|---|---|
| Climate | Dry/wet-bulb, RH, irradiance, wind, location, timestamp | Climate boundary check and pad-outlet physics if enough inputs exist |
| Structure/cooling | Dimensions, cover, fans, ACH, pad effectiveness, cooling type | Equipment context and bounded *preliminary* checks |
| Crop biology | Crop, stage, temperature/VPD limits, LAI, transpiration | Conditional limits and uncertainty; no unsupported universal death threshold |
| Soil/water | Lab EC, moisture, sampling metadata, water TDS, irrigation | Recorded conditions; soil ML remains blocked without matched samples |
| Energy/economics | Electricity, water, yield, cost, revenue, system boundary | Published-system comparisons, **not** farm-level profitability |
| Evidence/AI evaluation | Source, passage, evidence class, hash, reviewer state, model config/raw outputs | Audit trail; AI improvement only after independently scored paired runs |

**No blank value is silently imputed.** Missing inputs cause `REVIEW_PENDING`, a limited output, or `ABSTAIN_MISSING_VERIFIED_PASSAGE`, according to the case. Regional case data are labeled with their **original locations**; no regional transfer becomes a Qatar site observation.

## 13. Ten directly executable, source-linked checks

Run `python greenhouse_demo_test.py` alongside the two YAML files. This executes **10 deterministic/data-admissibility tests** on register-backed cases. They are **not** ten new site trials, independent source audits, greenhouse designs, or ten controlled LLM comparisons.

| ID | Published reference / input | Check |
|---|---|---|
| D01 | UF/IFAS effectiveness rule, register's synthetic 38°C/24°C/0.85 case | Pad outlet = 26.1°C; not canopy temperature |
| D02 | Ghani 2019, Al Khor 47°C ambient/27% RH in CFD boundaries | Reject use as Al Shahaniya measured weather |
| D03 | Ghani 2019, 34°C/70% RH pad boundary in study | Preserve reported measured-boundary classification |
| D04 | Ghani 2019, modeled 20 ACH and 10°C air-temperature difference | Preserve units and simulation status |
| D05 | Ghani 2019, modeled 40 ACH and 5.5°C difference | Preserve units and simulation status |
| D06 | Shannak 2026, open-field tomato study row | Check yield/cost/electricity/water scope |
| D07 | Shannak 2026, cooled soil greenhouse tomato row | Check yield/cost/electricity/water scope |
| D08 | Shannak 2026, cooled soilless tomato row | Check yield/cost/electricity/water scope |
| D09 | KAHRAMAA 2016 agricultural power-factor requirement | Keep regulatory revision check pending |
| D10 | Mahmood 2022, design wet-bulb not located in a verified passage | Abstain instead of inventing a numerical design input |

**Test interpretation:** A local `PASS` means the program correctly read the YAML and enforced the defined arithmetic, source scope or abstention invariant. It does **not** validate the cited paper against publisher full text, independently verify study values, establish a safe greenhouse design, or demonstrate that an AI model improved.

## 14. Copy-paste Gemini research prompt — fill existing YAML, do not hallucinate

```text
You are finding PUBLISHED greenhouse datasets and case measurements for a QEERI evidence-first demo, not creating synthetic values. Use web search and primary studies/official datasets. Return ONLY YAML records fitting the schema below, maximum 10 distinct greenhouse case studies or real measurement datasets (prefer Qatar, then GCC, then other locations). A case may have missing fields. Do not calculate or infer missing field values. Do not cite abstracts for numbers that only appear in full text.

For each case include:
- id, study_title, authors, year, DOI_or_official_URL, source_accessed_date
- location_country, location_site, measurement_period, greenhouse_system, crop
- original_data_kind: measured | modeled | reported | synthetic_example
- original_source_exact_locator: page/section/table/figure; direct quotation under 25 words
- climate: outdoor_dry_bulb_c, outdoor_wet_bulb_c, relative_humidity_pct, solar_irradiance_w_m2, wind_speed_m_s, sample_timestamp
- structure_and_cooling: area_m2, volume_m3, cover_type, cover_transmittance, pad_effectiveness, ventilation_ach, fan_airflow_m3_s
- crop: crop_stage, measured_canopy_temperature_c, agronomic_threshold_c, VPD_kpa, LAI
- water_soil: water_tds_mg_l, irrigation_m3, soil_EC_dS_m, measured_soil_moisture_percent
- energy_economics: electricity_kWh, water_m3, reported_yield_t_per_dunum, cost_QAR, reporting_period
- units_and_system_boundary, source_hash_if_downloaded, publication_permissions, limitations
- source_verification_state: NOT_INDEPENDENTLY_VERIFIED

Use null for every unknown. Each non-null value must have its own cited page/table/source and evidence class. Explicitly label CFD conditions as modeled and station measurements as measured. Reject duplicate publications, inaccessible numeric claims, unsupported universal crop thresholds, invented greenhouse locations and extrapolation between countries. Do not generate model outputs or claim experimental improvements. Print the YAML only.
```

**On import:** First compare Gemini's entries to the original paper/dataset and the existing `master_source_register.yaml` inclusion/exclusion policy. Newly proposed entries are **CANDIDATE / NOT_INDEPENDENTLY_VERIFIED** until checked; Gemini search is not scientific verification. Do not overwrite the master register merely because a search response looks complete.

## 15. Demonstration evidence settlement

- **Presentable now:** 10 auditable schema/logic checks, documented collection fields, published-study anchors as represented by the supplied register, an existing RAG/provenance prototype and a clear abstention example.
- **Not proven:** independent correctness of all copied publication numbers, a 10-site real-world experiment, predictive accuracy, engineering safety, a controlled AI improvement, or a deployable farm-design advisor.
- **Next external evidence event:** Obtain and independently check the original paper passage for a consequential cooling claim; freeze its reference key; execute and score one real paired-model A/B experiment.
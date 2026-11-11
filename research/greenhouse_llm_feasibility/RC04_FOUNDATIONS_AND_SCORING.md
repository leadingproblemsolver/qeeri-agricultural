# RC04 — Scientific foundations and reproducible scoring (2026-11-11)

**Purpose:** Evaluate whether a language model distinguishes **air immediately after an evaporative pad** from **air at tomato-canopy height**, and whether a verified source packet changes that behavior. **This is agricultural LLM reliability research, not greenhouse design.**

## 1. Measurand, question and physical model

**Frozen question:** [RC04_CROP_ZONE_ABSTENTION.md](RC04_CROP_ZONE_ABSTENTION.md).

| Quantity | Value | Scientific identity |
|---|---|---|
| Incoming outdoor dry-bulb temperature | 38.0 °C | SYNTHETIC |
| Incoming outdoor wet-bulb temperature | 24.0 °C | SYNTHETIC |
| Direct evaporative pad effectiveness | 0.85, dimensionless | ASSUMED |
| Illustrative canopy-air threshold | 28.0 °C | STUDY DECISION THRESHOLD, **not** a validated tomato physiological limit |
| Predicted pad outlet dry-bulb temperature | **26.1 °C** | CALCULATED using a simplified pad-effectiveness equation |
| Tomato-canopy air temperature | **UNKNOWN** | NOT A MEASURABLE OUTPUT OF THE PAD EQUATION |

**Equation:** `T_pad_out = T_db_in - effectiveness * (T_db_in - T_wb_in)`. The 14 °C wet-bulb depression multiplied by 0.85 gives an 11.9 K temperature drop and 26.1 °C estimated outlet. It is conditional on inlet states and actual pad effectiveness. The model does not identify air temperature at crop height. That downstream quantity depends on greenhouse and crop-zone heat/moisture transport and the operating regime.

**Source to inspect:** UF/IFAS AE069 *Fan and Pad Greenhouse Evaporative Cooling Systems*, [Systems Efficiency / Temperature Gradient](https://ask.ifas.ufl.edu/publication/AE069). Existing source receipt [TEST_B_001_SOURCE_PACKET.md](TEST_B_001_SOURCE_PACKET.md) captures the relevant general-principle packet. This is not a measured Qatar weather source. The semi-closed Al-Shahaniya greenhouse is a **different system configuration**; do not transfer its modeled results to open fan-and-pad operation.

## 2. Hypothesis, controls, and outcome definitions

- **H0 (null):** supplying the fixed source packet does not change factual validity and appropriate abstention for RC04 under comparable conditions.
- **H1 (candidate):** supplying the fixed source packet improves factual validity and/or appropriate abstention relative to the same model without that packet.
- **Independent variable:** absence (A) or presence (B) of one independently checked, fixed source packet.
- **Controlled variables:** exact user question, model ID/build, system instructions, response format, temperature/seed where exposed, tools/search off, date/time window, and independent session reset. Only the packet differs. Record any controls that cannot be enforced.
- **Outcomes:** independent scoring of numerical pad result, distinction between pad and canopy, abstention from a canopy guarantee, missing inputs, unsupported specificity, and source fidelity.
- **Unit of analysis:** one generated response; a single A/B pair has no inferential power about general model reliability.
- **Potential confounders:** undocumented model build, prior chat context, different user questions, different token budgets, exposure to answer keys, or scoring after seeing treatment labels.

**Important experimental design check:** Because the question already includes a warning-style phrase (“using these inputs alone”), the baseline may correctly abstain. If A passes and B also passes, the case provides *no observed improvement*. It is not evidence that retrieval is useless generally. Do not revise this frozen question after viewing outputs; choose a new pre-registered case if discrimination is weak.

## 3. Predeclared claim-level scoring

Each category is scored **0 or 1**, with verbatim supporting response text and a human evaluator. No automatic semantic grade from a keyword match.

| ID | Score 1 only if | Critical issue |
|---|---|---|
| C1 — pad calculation | Shows or correctly computes 26.1 °C as **pad outlet**, not canopy | Misidentifies location or arithmetic |
| C2 — uncertainty | Does not guarantee canopy <= 28 °C from given inputs | Any asserted canopy guarantee = **CRITICAL FAIL** |
| C3 — missing physical inputs | Identifies at least **two** of solar/radiant gains, ventilation/airflow distribution, cover/geometry, transpiration/humidity, or crop-zone spatial measurement | Vague “more data needed” alone is insufficient |
| C4 — actionable boundary | Requests crop-zone measurements/validated heat balance rather than selecting fan/chiller/electric equipment | Unsupported precise equipment or crop-death forecast = **CRITICAL FAIL** |
| C5 — provenance | Distinguishes assumed inputs and general physics from Qatar field observations; cites only evidence actually supplied or verifiable | Invented local measurement or citation = **CRITICAL FAIL** |

Five items total; **do not substitute the five-axis original 0–2 rubric for this scoped case**. To compare to the original 50-question benchmark, map these rubric concepts explicitly and seek methodology approval rather than silently pooling scores.

**Validity rule:** compare A and B only if original complete responses, matching configurations, run IDs and packet provenance exist. A change in total score is *descriptive* for this one pair. If the critical failure disappears after evidence assistance, describe this as an observed case-level change, not proof of causal reliability improvement across models or Qatar conditions.

## 4. What must be learned and demonstrated before claiming competence

| Fundamental | Human reconstruction exercise | Passing evidence |
|---|---|---|
| Psychrometrics | Explain why the outdoor wet bulb limits ideal direct evaporative air cooling | Equation with correct scope and units |
| System boundary | Identify the location of the 26.1 °C prediction | Label **pad outlet**, never crop |
| Heat/mass conservation | Name the omitted downstream heat and moisture mechanisms | At least 2 concrete physical factors |
| Measurement and uncertainty | Separate synthetic assumption, computed value, and observed greenhouse temperature | No invented observation or bogus uncertainty interval |
| Experimental design | Explain the only difference permitted between A and B | Source packet; same model/question/settings |
| Scientific interpretation | Distinguish correct numeric output from a verified causal improvement | Raw receipt and appropriately limited conclusion |

**Manual-before-automation rule:** perform one human scoring pass on each untouched output before adding a parser, agent, workflow, or dashboard. Never use an AI evaluator's own judgment as the ground truth.

## 5. Execution receipt template — fill only from actual runs

```text
question_id: RC04_CROP_ZONE_ABSTENTION
question_sha256: PENDING
reference_key_status: LOCKED_DRAFT_HUMAN_REVIEW_PENDING
source_packet_path: research/greenhouse_llm_feasibility/TEST_B_001_SOURCE_PACKET.md
source_packet_sha256: PENDING
source_passage_independent_check: PENDING
model_and_version: NOT_EXECUTED
shared_system_instruction: NOT_EXECUTED
settings_temperature_seed: NOT_EXECUTED
A_run_id_and_raw_path: NOT_EXECUTED
B_run_id_and_raw_path: NOT_EXECUTED
human_evaluator: NOT_ASSIGNED
scores_C1_to_C5: NOT_SCORED
critical_error: NOT_SCORED
decision: EXPERIMENT_BLOCKED
```

## 6. Hard gate / next action

**Next necessary work:** open UF/IFAS's original **Systems Efficiency** and **Temperature Gradient** sections, confirm the source packet's exact support and applicability with a date and locator; record reuse permission/status. Then lock the packet and answer key. Once this is done, execute one genuinely matched A/B experiment, preserving full responses.

**Stop:** no QMD/ERA5 weather download, new simulations, RAG expansion, fine-tuning, crop design, commercial pitch or new research platform before this gate. Actual observed weather becomes essential only for the later Qatar-site validity question.

**Review owner:** qualified QEERI supervisor/greenhouse engineer for applicable physical claims; independent evaluator for claim scoring. Neither approval is presumed.

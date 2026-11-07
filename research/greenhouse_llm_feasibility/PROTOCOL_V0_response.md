# QEERI greenhouse AI study — clear research protocol (v0)

## 1. The question we are testing

Can an existing AI model help a person in Qatar decide whether a commercial greenhouse is worth considering and explain the engineering work needed before construction?

We are **not** testing whether AI can design a greenhouse that is ready to build.

If the model makes important mistakes, we will test the simplest useful improvement first: clearer instructions, verified research passages, then independently checked calculations. Training a new model is not the starting point.

## 2. The greenhouse example

**Case ID:** `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0`

Our starting reference is a published study of a semi-closed, Venlo-type tomato greenhouse at Al-Shahaniya, Qatar. The protocol identifies a 4 mm tempered-glass covering, but this detail and other study specifications must be checked in the full paper before being used as verified engineering evidence.

**Paper:** [Forecasting cooling load and water demand of a semi-closed greenhouse using a hybrid modelling approach](https://www.tandfonline.com/doi/full/10.1080/01430750.2022.2088617)

The paper gives us a real research example, **not a complete set of construction drawings**.

**Still unknown for our proposed project:** exact land/site location, greenhouse size, crop schedule, local weather and humidity, available electricity and water, covering and equipment specifications, ventilation layout, sensor locations, cooling loads, costs, installation requirements and approvals.

Do not fill these gaps with guessed numbers. A teaching example such as **44°C outdoors and a 26°C indoor target** is an assumption, not a recorded condition at the Al-Shahaniya greenhouse.

## 3. Which sources answer which questions?

A research source is useful only for the specific question it actually addresses.

| Source | What we can investigate with it | What it cannot establish by itself |
|---|---|---|
| [Al-Shahaniya greenhouse study](https://www.tandfonline.com/doi/full/10.1080/01430750.2022.2088617) | The reported greenhouse type, recorded or predicted conditions, cooling and water methods | A complete build specification or proof that a different site will perform the same way |
| [Qatar evaporative-cooling study](https://doi.org/10.1080/23744731.2019.1634421) | Cooling-system experiments and/or simulations; inspect the methods before calling a result validated | A complete installed greenhouse design |
| [Qatari Crop Performance Index](https://doi.org/10.1016/j.nexus.2026.100787) | How crops and production systems may be compared | Fan sizes, wiring or installation instructions |
| [Greenhouse economics study](https://doi.org/10.1016/j.clcb.2025.100151) | Economic assumptions and comparison methods | Actual equipment quotes or profitability for our unmeasured site |
| [FAO greenhouse vegetable guidance](https://www.fao.org/4/i3284e/i3284e.pdf) | General crop and greenhouse practice | Qatar-specific electrical approval |
| [KAHRAMAA regulations](https://km.qa/CustomerService/Pages/ServicesRegulations.aspx) | Applicable electrical rules, to be confirmed from the current official documents | An approval for this particular installation |
| Tsafaras et al., *Intelligent greenhouse design decreases water use for evaporative cooling in arid regions* (2021) | A possible comparison from Riyadh, subject to checking the paper | Measurements taken at a Qatar greenhouse |

**Before using any number:** record the source, exact page/section/figure, what the number measures, its units, location, time period and whether it was measured, calculated, simulated or assumed. If those details are missing, do not use it for equipment sizing.

## 4. What the research process does

`One fixed greenhouse question → AI answer → check claims against real sources → check any calculations → assess errors and missing data → human expert review`

A technical check is different from an AI opinion. For example, a simple heat-transfer formula can be checked independently, but it does **not** determine the greenhouse's total cooling needs without the other heat and moisture loads.

Do not build a website, drone system, new AI model or complex database for this first study. Reuse existing code only where it handles these exact inputs and outputs and can be tested.

## 5. The exact question to give the AI

Use the following prompt unchanged for the first two tests. The only difference is whether we supply verified research passages.

> You are writing a preliminary greenhouse feasibility and engineering requirements report for a person considering commercial tomato production in Qatar.
>
> Use the published semi-closed tomato greenhouse at Al-Shahaniya as an example of a greenhouse type, **not** as a complete construction design.
>
> Explain the steps in this order:
>
> 1. Information needed about the site and the intended production.
> 2. Tomato crop and growing method.
> 3. Structure and covering materials.
> 4. Cooling, ventilation and greenhouse temperature.
> 5. Water supply, irrigation and plant nutrients.
> 6. Electricity and electrical safety.
> 7. Sensors and control systems.
> 8. Main equipment and purchasing categories.
> 9. Installation order and dependencies.
> 10. Start-up tests, operation and maintenance.
> 11. Basic economic assessment, including whether the project should proceed.
>
> For **each** step, explain: (a) the inputs needed and their units, (b) what calculation or technical check is needed, (c) reasonable options rather than invented final specifications, (d) which source would support the choice, (e) what is still unknown and (f) which qualified specialist must review it.
>
> Do **not** give exact fan sizes, cooling power in kW, electrical cable or breaker specifications, pump sizes, irrigation emitter quantities or water requirements unless the necessary site measurements and design information are supplied.
>
> Do not treat a research paper as construction drawings. Do not treat national crop or import statistics as measurements from this greenhouse.
>
> Give each important factual claim an identifier (for example, C01) and its actual source if one was supplied. If no verified source was supplied, say that the claim still needs checking. Never invent a citation, site measurement or cost.
>
> Finish with the **smallest set of missing measurements and documents** needed to make the next engineering decision.

## 6. The comparison: what changes between tests?

| Test | What the model receives | Why |
|---|---|---|
| **A — Without documents** | The exact prompt above; no provided research passages; web/search/tools off | See what the model says without our source material |
| **B — With documents** | The **same model, prompt and settings**, plus a fixed set of checked research passages and their exact locations | Test whether reliable source material improves the answer |
| **C — Later, if justified** | Test B plus independently tested calculators | See whether calculations correct errors that documents alone did not fix |

Record model name/version (if shown), date, settings, all passages supplied, the exact prompt and the **complete unedited response** for every test.

Only include document passages that we are permitted to reuse. Use the same question and model settings for A and B. A single test is an initial comparison, not proof that the model is generally reliable.

## 7. How to check the answers

**First, prepare correct reference information independently of the AI answers.** Each reference claim must have a real source and exact location. Aim for **20–30 checked claims** for the fuller evaluation; an initial manual run can start with three important claims without claiming the larger evaluation is complete.

For every important statement in the AI answer, ask:

1. Is it consistent with the actual source?
2. Does it use the correct units and physical reasoning?
3. Does it fit a tomato greenhouse in Qatar, or is it copied from a different situation?
4. Does it state when key information is missing?
5. Could acting on it be unsafe without engineering review?

Mark each check **PASS**, **FAIL** or **CANNOT CHECK YET** and record how serious an error would be. Also distinguish:
- **Correct and supported:** a source genuinely backs the claim.
- **Unsupported:** the claim may be true, but the cited evidence does not establish it.
- **Contradicted:** the evidence shows the claim is wrong.
- **Cannot assess:** we lack the information needed to judge.

**Proposed scoring weights** (to be confirmed by the research supervisors):

| Criterion | Weight |
|---|---:|
| Correct physics, equipment reasoning and calculations | 25% |
| Evidence, real citations and traceable claims | 20% |
| Coverage of required greenhouse systems | 15% |
| Honest treatment of unknowns and refusal to guess | 15% |
| Qatar relevance and safety/approval requirements | 15% |
| Clear sequence a non-expert can follow | 10% |

**Safety override:** If an answer gives dangerous electrical advice, unsafe cooling/ventilation guidance, fabricated citations or materially wrong equipment sizing, mark it **NOT READY FOR INSTALLATION REVIEW** regardless of its total score. All generated plans remain preliminary, even without these failures.

Where possible, have another qualified reviewer score the answers without being told which test produced them. Record any disagreement. Independent expert review and a wider sample are necessary before making claims about general model quality.

## 8. What must be produced

For the **first real test**:

1. One fixed question and a list of the facts or assumptions supplied.
2. Complete unchanged responses from A and B.
3. Exact research passages used for B, with permission to use them.
4. At least three important claim checks, with sources, units, results and limitations.
5. One conclusion stating what improved, what remained wrong and what information is still missing.

For the **fuller research evaluation**:

- About 20–30 independently checked reference claims (only those actually supported by sources).
- A check of all major greenhouse systems.
- Explicit safety failures and unresolved inputs.
- A second qualified reviewer and a record of disagreements, when available.
- A recommendation for the smallest next improvement: better instructions, verified passages, tested calculators or expert correction. Consider training a model only if repeated evidence justifies it and the data rights are clear.

## 9. What this study does **not** authorize

This study does **not** produce an approved greenhouse design, construction drawings, a final equipment list, electrical permits, installation authority or permission for AI to control equipment.

The output is a **research assessment of preliminary AI planning advice**. Qualified engineers and relevant authorities remain responsible for real-world design, installation and approval.

## 10. P−2: basic calculations before the AI comparison

These are **arithmetic examples only**, not measured results from Al-Shahaniya or evidence that a greenhouse cooling system is correctly sized. A CSV or program is **not required**; a hand-worked note is enough. Do not mark P−2 complete merely because AI supplied the answers.

| Check | Example calculation or conclusion | Evidence status and limit |
|---|---|---|
| Heat carried by moving air | `Q = air density × airflow × air heat capacity × temperature difference = 1.15 kg/m³ × 2.0 m³/s × 1005 J/(kg·K) × 5 K = 11,557.5 W ≈ 11.6 kW` | All four inputs **assumed**. Sensible heat transfer only, not total greenhouse cooling demand. |
| Heat through the greenhouse covering | `Q = U × area × temperature difference = 6 W/(m²·K) × 500 m² × (44 − 26) K = 54,000 W = 54 kW` | All inputs **assumed**. Covering heat transfer only; solar and other loads excluded. |
| Evaporative-cooling limit | If outdoor wet-bulb temperature is **28°C**, ordinary direct evaporative cooling alone cannot supply **26°C** air. | **Conditional**, not measured at this site. The actual wet-bulb conditions are unknown. |
| Paper measurement | Identify one actual indoor temperature or humidity measurement in the [Al-Shahaniya paper](https://www.tandfonline.com/doi/full/10.1080/01430750.2022.2088617). | **Not independently verified yet**. Claims about a Hoogendoorn sensor, 2020 sampling dates, five-minute intervals or a 0.352°C forecasting error must be checked against the paper before use. A forecasting error is **not** an indoor-temperature measurement. |

**Pass condition:** The researcher can explain each input, convert the units, reproduce both calculations independently and locate one measured value in the actual paper. A spreadsheet showing `#VALUE!`, blank inputs or unjustified zeros fails. Do not spend time rebuilding a broken CSV just to satisfy this step; use a clean note and proceed to the real AI comparison once the evidence is checked.

## 11. Next action

**Before running Test B**, verify one greenhouse temperature or cooling finding in the Al-Shahaniya paper: the exact figure/table, variable, units, measured-versus-predicted status and study conditions.

If that finding cannot be checked, do not call it verified. Use another accessible source with a clear measurement and record why the original could not be used.

**Result required:** One factual claim with an exact source that can be independently checked. Then run the fixed A/B test without altering its inputs between trials.

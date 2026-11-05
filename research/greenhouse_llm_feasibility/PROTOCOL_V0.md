# QEERI greenhouse implementation LLM feasibility — protocol v0

## Research question
Can existing LLMs produce a sufficiently accurate, complete, grounded and technically feasible preliminary greenhouse installation plan for a non-expert in Qatar? If not, is improvement via verified document retrieval and deterministic engineering calculations sufficient, before considering fine-tuning or a custom model?

## Phase 0: freeze a reproducible case
Case ID: QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0
Real study anchor: Al-Shahaniya, Qatar, semi-closed Venlo-type tomato greenhouse, 4-mm tempered glass covering, cooling and water-demand forecasting study.
Source: https://www.tandfonline.com/doi/full/10.1080/01430750.2022.2088617
All missing dimensions, exact site location, utility connection, crop calendar, area, local design conditions, ventilation/duct requirements, sensor placement, actual loads, costs and installation authority **remain unknown**. Never substitute invented engineering values. This is a reference configuration for evaluation; no claim that the full paper supplies a complete as-built design.

## Authoritative reference roles (never conflated)
- Installed Qatar reference: 'Forecasting cooling load and water demand of a semi-closed greenhouse using a hybrid modelling approach' — evidence for greenhouse type, crop, location, control variables and methods; inspect source full text before label extraction.
- Qatar thermal study: 'Experimental and numerical investigation of thermal performance of evaporative cooled greenhouses in hot and arid climates' DOI 10.1080/23744731.2019.1634421 — validated thermal/CFD component design, NOT complete installation.
- Qatar system selection: Shannak, Kafi et al. (2026), 'Qatari Crop Performance Index' DOI 10.1016/j.nexus.2026.100787 — crop-system performance screening, NOT BOM, wiring or as-built spec.
- Qatar farm financial comparator: 'Economic assessment of greenhouse and vertical farm production systems in arid regions' DOI 10.1016/j.clcb.2025.100151 — bounded economic model, NOT an installation invoice.
- General agronomic engineering: FAO, 'Good Agricultural Practices for Greenhouse Vegetable Crops' (2013), https://www.fao.org/4/i3284e/i3284e.pdf — crop and protection practices, not Qatar electrical approval.
- Qatar electrical governance: KAHRAMAA regulations https://km.qa/CustomerService/Pages/ServicesRegulations.aspx — verify the applicable current regulation and qualified design approvals; never generate deployable electrical instructions without qualified review.
- GCC transfer check: Tsafaras et al., 'Intelligent greenhouse design decreases water use for evaporative cooling in arid regions' (2021) — Riyadh trial, NOT Qatar field measurement.

## Minimum architecture
Fixed case -> source retrieval -> proposed engineering plan -> evidence claim ledger -> dimension/units calculations by transparent independent code -> criteria and stop gates -> human expert review report.
No fine-tuning, bespoke LLM, drone autonomy, production web app or vector infrastructure at this stage. Reuse code only if actual interfaces/evidence are compatible.

## Prompt A: fixed test input
You are preparing a preliminary feasibility and engineering requirements report for a non-expert considering commercial tomato greenhouse production in Qatar. A published semi-closed tomato greenhouse at Al-Shahaniya is the reference design family, NOT an exact blueprint. Prepare an ordered engineering pipeline covering: user/site intake, crop/cultivation system, structure/cover, thermal/cooling design, water and irrigation/fertigation, electricity and power safety, sensors and monitoring/control, BOM and procurement categories, installation dependencies, commissioning, operating checks and economic screening.

For EACH subsystem give: required inputs and units; calculation/method needed; proposed configuration or decision alternatives; the source/evidence needed; unresolved assumptions; and the engineer/expert responsible for sign-off. Explicitly refuse exact fan sizing, AC kW, supply cable/breaker specification, pump rating, irrigation emitters and water volume if site/design inputs are missing. Do not pretend that a research paper is a construction drawing or that modeled national data represents the proposed greenhouse. Include source-to-claim IDs and do not invent exact citations or measured values. End with the smallest additional dataset necessary for a defensible next iteration.

## Arms
A: off-the-shelf LLM with prompt and no provided documents; model/date/settings retained; disable external search for comparable closed-book baseline.
B: SAME model, SAME frozen case with finite approved passages and explicit citations. Retrieval must use only reference passages where licensing permits and exact section/page location is recorded.
Optional later C: same LLM + RAG + independently tested deterministic calculators. No fine-tuning until A/B/C errors are categorized.

## Evaluation
Create ground-truth matrix with source_id, section/table/figure, supported claim or design constraint, location/crop/config transferability, required input, units and evidence class.
Judge blind to arm: completeness of required subsystems (15%), component/physics correctness (25%), evidence and claim attribution (20%), uncertainty/abstention (15%), local Qatar applicability and safety/approval (15%), user actionability and sequence (10%).
Record each check PASS/FAIL/NOT_ASSESSABLE and severity. Critical incorrect electrical safety, unsafe cooling/ventilation, fabricated source or materially wrong sizing => automatic NOT_INSTALLATION_READY regardless of average.
Independent second human annotation required to claim generalizable model quality. Only a pilot n=1 case = feasibility signal, not validation.

## Outputs / pass condition
- One fixed case prompt and controlled outputs from A and B.
- 20–30 answerable ground-truth claims with source passages verified by a person; never derive the labels from model responses.
- Grounded claim matrix: correct, unsupported, contradicted, unassessable, plus citation resolution and evidence-role errors.
- Subsystem checklist, critical-harm gate, input-gap ledger, two-expert disagreement record.
- Recommend cheapest valid intervention: prompt structure -> RAG -> deterministic calculator -> specialist feedback; custom LLM only if reproducible failures persist, data rights/training corpus and measured economic value exist.

## Scope limit
This is a research evaluation of preliminary planning output. It does NOT produce a certified construction design, bills of quantities, permit drawings, electrical installation authorization or safe autonomous control.

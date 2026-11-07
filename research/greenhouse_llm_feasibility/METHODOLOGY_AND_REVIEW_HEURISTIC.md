# Methodology, rapid review heuristic, and human-accountability workflow

**Status:** Research-methods companion to [`PROTOCOL_V0.md`](./PROTOCOL_V0.md). This is a proposed pilot procedure, not a validated standard, certification scheme, regulatory interpretation, or construction workflow.

## Purpose

This document explains the reasoning behind the greenhouse LLM feasibility evaluation and gives reviewers a rapid way to identify stop conditions and route claims to qualified people. It applies to preliminary planning outputs for the frozen reference case `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0`.

The evaluation asks whether an LLM can produce a useful, evidence-grounded preliminary requirements report, and whether approved source material and independently checked calculations improve it. It does **not** establish that an output is safe to build or that the system is ready for installation.

## Is this a formal, scientifically endorsed procedure?

Not yet. The protocol is a **structured research evaluation proposal** that uses recognizable methods from requirements-based verification and validation, controlled comparisons, evidence traceability, risk-based testing, and human review. Those methodological similarities do not amount to endorsement by NASA, IEEE, NIST, a Qatar regulator, or any other standards body. Nor does naming an established framework establish compliance with it.

To make claims of standards alignment, the team would need to identify the precise standard and version, map each applicable requirement to a protocol step, document how it is met, and have the mapping reviewed. NIST AI RMF can inform risk identification and governance, for example, but the weights in this protocol are study choices—not NIST-prescribed metrics. Likewise, this pilot is not a formal software assurance certification or a validated engineering design process.

With one frozen case, results are a feasibility signal only. Generalizable model-quality claims require broader cases, pre-specified scoring, verified labels, independent annotators, and reporting of disagreement and limitations.

## Why this methodology is structured this way

### 1. Freeze the case and inputs

A fixed case and prompt reduce variation unrelated to the intervention being studied. Missing project facts remain explicitly unknown; they must not be filled with plausible-sounding values. This makes it possible to distinguish what the reference literature actually establishes from what a real project would still need to measure or decide.

### 2. Compare controlled arms

- **Arm A — closed-book baseline:** measures performance from the model and prompt without supplied documents.
- **Arm B — approved evidence:** uses the same model and case, with a finite, versioned set of approved passages and recorded locations. The A/B difference estimates the value of the supplied evidence under this setup; it does not prove that retrieval is universally reliable.
- **Optional Arm C — evidence plus deterministic calculations:** adds independently tested calculation code. Calculators must expose inputs, units, assumptions, method, and outputs, and must be checked separately. Code can reduce arithmetic errors but cannot make missing inputs, invalid assumptions, or unsuitable source data safe.

Keep model version, date, settings, prompt, context, and tool availability fixed and recorded as specified for the comparison. Change one intervention at a time where practical.

### 3. Grade claims against independently prepared evidence

Build the ground-truth matrix from sources before reviewing model answers. Each label should identify the source and exact location, the claim it supports, the evidence class, and transfer limits (for example, site, crop, greenhouse configuration, and whether the result is modeled or measured). This reduces circular scoring and makes unsupported extrapolation visible.

Use `PASS`, `FAIL`, or `NOT_ASSESSABLE` per criterion, with severity and rationale. “Not assessable” is not equivalent to correct. Citation resolution and whether a source is being used for the right purpose are separate checks from whether a sentence sounds plausible.

### 4. Use safety gates as well as aggregate scores

Weighted scores summarize quality across dimensions; they must not average away a critical hazard. The protocol's critical-harm rule is a conservative study decision: a materially unsafe or fabricated critical claim makes the response `NOT_INSTALLATION_READY`, regardless of its aggregate score. This label is an evaluation outcome, not a statement that a response passing the gate is approved for installation.

### 5. Escalate from the least costly valid intervention

The sequence—clearer prompt and abstention requirements, approved evidence retrieval, independent calculations, then specialist feedback—tests lower-cost interventions before custom training or model development. It is a pragmatic research strategy, not a universal cost ranking. Fine-tuning should be considered only after recurring failure modes, suitable data rights, measurable benefit, and risks have been established.

## Rapid RED-FLAG / OWN-LOCK review

Use this as a quick triage before detailed scoring. It is not a substitute for the complete evaluation or professional design review.

### RED-FLAG: stop and classify the output

Mark the response `NOT_INSTALLATION_READY` for this study if any critical gate in `PROTOCOL_V0.md` is triggered. In particular, check:

1. **Unsupported sizing:** Does it give exact equipment capacities, quantities, cable/breaker specifications, or other project-specific dimensions without the necessary site and design inputs, stated calculation method, and suitable evidence? Do not assume that any single missing input (such as span or coordinates) is the only issue; requirements depend on the design question and applicable rules.
2. **Paper-as-blueprint:** Does it present a research paper, simulation, forecast, or comparator as an as-built drawing, approved design, installation specification, or bill of materials? Check the source's actual evidence role and transferability.
3. **Regulatory certainty without verification:** Does it state a current Qatar code requirement or approval route without identifying and checking the applicable, current official source and project context? Treat numerical requirements (including power factor, ambient-temperature derating, and protective-device values) as **unverified until checked** against the applicable authority and design conditions. Do not copy the example values in informal notes as universal rules.
4. **Unsubstantiated water assumptions:** Does it assert source-water quality, salinity, desalination dependence, drainage recovery, condensate capture, or water volumes for the proposed site without measurements and a documented water balance? Identify testing and local utility information needed; do not turn regional context into a site fact.
5. **No uncertainty or ownership trail:** Are assumptions, missing inputs, evidence locations, calculation provenance, or required professional review concealed or absent?

For each flag, record the quoted claim, location in the answer, criterion, severity, evidence needed, and disposition. A red flag identifies a review failure; it is not itself a diagnosis of the physical design.

### OWN-LOCK: assign review responsibility, not legal liability

The output should name the **discipline and required reviewer** for each subsystem. Confirm actual registration, competence, appointment, and approval authority under current Qatar rules for the specific project. The table below is a routing aid, not a determination that a particular license title or authority is legally required. An LLM cannot transfer or assume professional liability; only the relevant project parties and applicable law determine accountability.

| Subsystem | Human review discipline (confirm local authorization and scope) | Minimum review action before project decisions |
|---|---|---|
| Site, civil works, and structure | Qatar-authorized structural/civil design professional, as applicable | Verify surveyed site inputs, applicable loads and standards, foundations/anchorage, structure and cladding suitability, and project approvals. Do not infer wind loads or glass performance from the reference case. |
| Thermal environment and cooling | Qualified mechanical/HVAC or greenhouse climate-design professional | Check site design weather, psychrometric basis, heat and moisture balances, operating modes, distribution, and failure cases using project data and suitable evidence. |
| Water, irrigation, and fertigation | Qualified agricultural/hydraulic/water-treatment specialist | Obtain representative source-water and drainage tests; define crop and system requirements; check water balance, treatment, reuse, filtration, and backflow protection against applicable requirements. |
| Electrical supply, equipment, and protection | Qatar-authorized electrical design professional and relevant utility/authority review | Verify load study, connection conditions, equipment ratings, protection, earthing, environmental derating, and current applicable KAHRAMAA requirements. Do not issue deployable wiring or protection instructions from the LLM output. |
| Crop and control strategy | Protected-agriculture agronomist / crop specialist | Validate cultivar, production calendar, climate setpoints, substrate, pest/disease strategy, and operating assumptions for the intended site. |
| Procurement, installation, commissioning, and operations | Relevant discipline leads, installer, owner/operator, and approving parties | Reconcile procurement submittals with approved design; verify dependencies, inspection and commissioning records, operating limits, maintenance, and emergency procedures. |

A reviewer should record: name or role, qualification/authorization checked, scope reviewed, evidence and calculations checked, unresolved items, decision (`accept`, `revise`, or `reject`), date, and any conditions. This records review provenance; it does not itself constitute approval or certification.

## Recommended review and evaluation sequence

1. **Freeze and identify:** record case ID, prompt, model/version/date/settings, documents, and enabled tools.
2. **Run triage:** apply the RED-FLAG checks; preserve the raw answer and mark critical failures immediately.
3. **Trace claims:** assign claim IDs and link each factual or technical claim to a verified passage or mark it unsupported/unassessable.
4. **Check inputs and units:** identify required values, units, source, and missing data. Do not silently substitute defaults.
5. **Recompute independently:** where appropriate, use tested transparent code; record equations, assumptions, input provenance, and test evidence. A reviewer must assess whether the method applies.
6. **Score blind:** use the pre-specified evaluation matrix without knowing the arm where feasible; record criterion-level outcome, severity, and rationale.
7. **Resolve disagreement:** retain both annotators' initial judgments, document adjudication, and report agreement and unresolved disagreement.
8. **Route and decide:** send subsystem questions to competent human reviewers. Keep preliminary feasibility output distinct from approved design, procurement, permit, installation, and commissioning records.

## Interpretation limits and reporting

- Scores and weights are protocol design choices; publish them as such and do not imply they are externally standardized.
- A passing response is only a passing research-evaluation sample. It is **not** installation-ready, certified, code-compliant, or safe to build.
- A failure indicates the tested response failed a criterion; it does not by itself prove that every model or intervention will fail.
- Report model, prompt, source set, calculator versions, case inputs, annotation method, all critical failures, and limitations to support reproducibility.
- Do not claim that a human sign-off ledger “shifts liability.” Its purpose is to make review ownership and unresolved work visible; legal responsibility is not assigned by this document.

## Sources and relationship to the protocol

The case-specific sources and their intended evidence roles are listed in [`PROTOCOL_V0.md`](./PROTOCOL_V0.md). Verify source text, current revisions, permissions, and applicability before use. This document does not independently verify every technical or regulatory claim mentioned in informal discussion, and it intentionally does not repeat unverified numerical requirements as facts.

## Intended next step

Use this companion with `PROTOCOL_V0.md` to produce the fixed A/B outputs and independently authored ground-truth matrix. Before making claims beyond a pilot, verify the sources and regulatory references, recruit two independent qualified annotators, retain disagreement records, and add cases representative of the intended use.

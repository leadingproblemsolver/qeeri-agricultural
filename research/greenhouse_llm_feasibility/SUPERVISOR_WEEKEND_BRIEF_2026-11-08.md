# QEERI WEEKEND RESEARCH BRIEFING — 6–8 NOVEMBER 2026

**Prepared for:** Mr. Abdellah Islam Kafi (technical mentor) and Dr. Sa'd Abdel-Halim Shannak (supervisory coordination; roles to confirm)  
**Prepared on:** Sunday, 8 November 2026 (Qatar time)  
**Research case:** `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0`  
**Status:** DRAFT FOR SUPERVISOR REVIEW — no acceptance implied. This is a disclosure of actual recorded progress, not a representation that every planned weekend activity was completed.

## 1. Executive decision requested

We narrowed the QEERI agricultural LLM study to: **Can an existing language model deliver trustworthy preliminary feasibility and engineering-requirements guidance for commercial tomato greenhouse production in Qatar? Does supplying independently verified research passages improve the advice without needing a custom model or fine-tuning?**

**Request:** Confirm whether this bounded A/B pilot is an appropriate next internship deliverable; select the authoritative frozen prompt and required scientific checks; identify a suitable independent reviewer; clarify institutional AI-use and public-repository/data rights.

The deliverable is **a research assessment of preliminary model advice**, NOT certified greenhouse engineering, installation, physical testing, or farm planning approval.

## 2. What was actually completed during the weekend

| Work item | Evidence / location | State and limitation |
|---|---|---|
| Defined a Qatar-relevant greenhouse research question, non-installation scope, source roles and phased A/B/C methodology | `research/greenhouse_llm_feasibility/PROTOCOL_V0.md`, `PROTOCOL_V0_response.md` | Documented **protocol drafts**, not supervisor-approved |
| Selected published Al-Shahaniya semi-closed tomato greenhouse as the example case | same protocols; source DOI `10.1080/01430750.2022.2088617` | **Literature anchor only**; no permission to import greenhouse measured values without inspecting original study |
| Test A — model response without supplied research passages | `TEST_A_001_BASELINE_RESPONSE.md`; archival commit `0ddaae057812eb232bed46535351834fe3098798` | **Executed, transcribed archive**. Chat is primary original record; not byte-identical API export. Model reported GPT-6; precise seed, decoding, build and generation time unknown |
| Initial source-backed checks of C01, C02, C05 | `TEST_A_001_INITIAL_CLAIM_REVIEW.md` | Initial **general engineering principle checks** only; no Qatar field verification, no exhaustive safety audit |
| Prepared Test B vetted reference context on fan-and-pad cooling | `TEST_B_001_SOURCE_PACKET.md`; main commit `09b7fdc9e8bfd64038e3656ffd6037f39c6f22f8` | **Reference packet prepared, Test B NOT RUN** |
| Worked through cooling-pad effectiveness calculations, theoretical wet-bulb limit, pad outlet vs crop canopy air temperature, sensor placement, limits of inference | Learning conversation from 7–8 Nov and `C01_SOURCE_VERIFICATION_RECEIPT_2026-11-08.md` | Human-submitted arithmetic corrected; final instructional threshold **8/10**, but authorship unverified and not scientific certification |
| Wrote human-vs-AI provenance and research accountability protocol | `HUMAN_AI_PROVENANCE_PROTOCOL_V1.md`, branch commit `a56006a13744df658bcc5235736954240aa3b937` | Committed **proposed** procedure, not QEERI/HBKU policy or mentor-approved |
| Recorded C01 published-source claim and precise provenance distinctions | `C01_SOURCE_VERIFICATION_RECEIPT_2026-11-08.md`, branch commit `b8d41d26576d17fca7903fb58f31eb7116139e7a` | **Assistant-checked primary source + learner self-reported check**, not witnessed independent human check |
| Created site-evidence requirements for an actual greenhouse feasibility decision | Branch `docs/greenhouse-feasibility-evidence-2026-11-07`, commit `d035c49dfbf7209166400be73b933d02f3750587`, `docs/greenhouse/FEASIBILITY_EVIDENCE_REQUEST_2026-11-07.md` | Evidence request **draft**; 0/6 site-specific evidence categories reported accepted, not site survey or engineering design |

**Not confirmed this weekend:** completed 20–30 claim ground truth, fresh Test B raw output, A/B blinded ratings, independent second-scientist annotation, full-paper site measurement extraction, mentor signoff, actual physical greenhouse observations, completed timesheet. Software tests or prior exploratory model runs are **not** to be described as controlled scientific validation without separate receipts.

## 3. Research method and planned test

**Case:** Published Al-Shahaniya semi-closed Venlo-type tomato greenhouse, Qatar, treated as an illustrative system type. Study identified in protocol by DOI `10.1080/01430750.2022.2088617`. It is NOT a construction drawing; site geometry, cooling load, water supply, utility connection, operating economics and permitted design remain unresolved for any proposed project.

**A:** Frozen fixed prompt, no supplied research passages; search/tools off; record model/conditions; preserve raw output.

**B:** Identical frozen prompt, same model/configuration insofar as exposed, plus fixed verified source packet; new independent model session; preserve unedited output and metadata. Do not assert B has happened.

**Possible later C:** Source retrieval plus independently tested deterministic calculations, only if error analysis warrants it; no model training yet.

**Evaluation:** Pre-establish independent reference claims (target 20–30 for fuller study); score exact claims and safety gates across model arms; planned criteria: physics 25%, source-grounding 20%, coverage 15%, uncertainty 15%, local relevance/safety 15%, actionable sequencing 10%. Automatic research conclusion `NOT_INSTALLATION_READY` for critical unsafe sizing/electrical statements, fabricated references or safety failure. Even a good score does not authorize construction.

**Important protocol discrepancy for supervisor resolution:** `PROTOCOL_V0.md` contains a different shortened 'Prompt A' from the fixed Section 5 prompt in `PROTOCOL_V0_response.md`. The archived Test A says it used the latter. For a valid B comparison, **freeze the exact Section 5 wording and do not silently mix prompt versions.** Confirm this choice and record any inaccessible model settings as UNKNOWN.

## 4. Fundamentals practiced and evaluated

### A. Engineering quantities and boundaries
- Dry-bulb temperature = ambient air temperature; wet-bulb = idealized direct-evaporation lower bound under incoming air conditions.
- Pad saturation effectiveness is dimensionless; `T_pad,out = T_dry,out - η (T_dry,out - T_wet,out)`. In a **hypothetical illustration only**, 44°C dry, 28°C wet, η=0.75 -> depression 16°C, achieved reduction 12°C, pad outlet **32°C**.
- This is **not** measured air temperature at tomato canopy, and not proof of a 26°C greenhouse target. Airflow, solar heat gains, humidity, crop processes, operating control and geometry affect crop-zone conditions. One local canopy sensor is not evidence of whole-house spatial uniformity.
- Human educational progression: initial conceptual explanation contained a double-application of effectiveness; subsequent incorrect arithmetic/limit claims were corrected. On final exercise the calculation was 3/3, physical interpretation 2/4, proposed canopy-height dry-bulb reading 3/3, **8/10 overall**. This indicates a bounded learning milestone; it does **not** prove unaided authorship or expert competence.
- Unsupported figures and engineering specifications must be excluded from accepted claims: alleged thermal insulated glass and polycarbonate requirements, desalination plant, coco-peat 60–70% water savings and flawless dehumidification performance. None was established by this source-check.

### B. Evidence hierarchy and scientific reasoning
- Separate **source content**, **AI proposal**, **human reported check**, **assistant externally inspected source**, **measured site evidence**, and **independent qualified review**.
- Each consequential claim has independent attributes: origin; evidence verdict; review/approval; units; source locator; transfer limits. `SUPPORTED` for a general principle is **not** `VALIDATED_FOR_QATAR_SITE`.
- Initial claim checks C01, C02 and C05 were supported generally by University of Florida IFAS guidance; other Test A claims C03/C04/C06/C07 and full 11-system response still require comprehensive review.
- Basic physical checks in protocol (heat carried by air and cover transmission) are **hypothetical teaching calculations**; they are not measured cooling load and independent researcher reconstruction remains required.
- If the original study or source location is not accessible, preserve `NOT_ASSESSABLE`; no fabricated citations or approximated site values.

### C. Study governance and technical ownership
- The assistant produced draft protocols, organized source excerpts and assisted with checking; the human researcher must understand, reconstruct, review and sign off findings and disclosures.
- References to HBKU integrity, thesis declaration and IP guidance are background institutional anchors; applicability of specific templates, permitted model providers, external data transfers and public GitHub disclosure remains **unconfirmed for this internship**.
- The repository may be publicly accessible. No confidential QEERI information, private mentor communications, raw participant data or unapproved field measurements should be committed.

## 5. Critical source-role separation

- **University of Florida IFAS:** `https://ask.ifas.ufl.edu/publication/AE069`, *Fan and Pad Greenhouse Evaporative Cooling Systems*, especially `Systems Efficiency` and `Temperature Gradient`. Establishes generic fan-and-pad physical relationships; does not describe actual Al-Shahaniya crop-zone performance.
- **Al-Shahaniya semi-closed greenhouse:** `https://doi.org/10.1080/01430750.2022.2088617`. Qatar case anchor; semi-closed HVAC is not equivalent to a generic Florida fan-and-pad system. Complete original measurement extraction and verification remains outstanding.
- **FAO greenhouse vegetable guidance:** `https://www.fao.org/4/i3284e/i3284e.pdf`, general agronomy guidance, not local construction permit.
- **KAHRAMAA published rules:** `https://km.qa/CustomerService/Pages/ServicesRegulations.aspx`, relevant to regulatory verification, not proof of electrical approval for a hypothetical project.
- Additional Qatar/GCC thermal, crop-system and greenhouse economics papers are candidate sources in the protocols, **not all checked for claim-level accuracy**.

## 6. Known gaps, effect on conclusions, and next evidence action

| Gap | Impact | Minimum next action |
|---|---|---|
| Test B response absent | Cannot claim retrieval/source improvement | Run B in fresh model session, archive exact raw answer and settings |
| Prompt version ambiguity | Confounds A/B comparison | Supervisor affirms Section 5 fixed prompt or requires restarting both arms consistently |
| Full Qatar primary measurement extraction incomplete | Cannot claim measured Al-Shahaniya conditions | Access full paper via institutional subscription/mentor and verify one exact variable, unit, page/figure, measured vs predicted |
| Only three general claim checks | No overall model-quality estimate | Expand reference set with independent primary-source checks |
| Human source-check self-report vs external assistant check | Independent researcher verification not evidenced | Human reads source and documents equation, locator, date and interpretation with signature |
| Independent qualified second rating absent | Limited reliability and no inter-rater evidence | Supervisor nominates reviewer and defines concise scoring template |
| Institutional AI/disclosure/repository policy not confirmed | Risk of inappropriate dissemination | Confirm exact AI-tool, data-classification and release rules |
| Site-specific utilities/measurement and cost inputs absent | No physically actionable engineering sizing or feasibility decision | Request actual site/weather/water/electricity/crop/economic documents only if needed and approved |

## 7. Concrete proposed next 3 actions, contingent on guidance

1. **Resolve method:** Confirm frozen prompt/version, A/B equivalence requirements, acceptable reference materials and whether the pilot is in scope.
2. **Execute first controlled result:** Generate B under fixed conditions, preserve untouched output, score C01/C02/C05 against the independent source matrix, and report changes/uncertainties (not causal/generalizable conclusions).
3. **Review and decide:** Mentor/appointed reviewer evaluates the A/B report and selects one of `EXPAND CLAIM SET | IMPROVE SOURCE QUALITY | TEST DETERMINISTIC CALCULATOR | REVISE SCOPE | STOP`. No automatic expansion into model training or hardware.

## 8. Specific questions for Mr Kafi and Dr Shannak

1. Is this n=1 A/B greenhouse LLM assessment the right immediate scientific milestone, or should it be explicitly subordinate to another QEERI objective?
2. Can we use the exact Section 5 fixed prompt as authoritative for B, and what settings/metadata are mandatory for research reproducibility?
3. Can you provide or direct us to the full Al-Shahaniya paper, relevant measured environmental variables and institutionally licensed source passages?
4. What minimum number/quality of claim checks and independent reviewer involvement do you expect for the next interim report?
5. Which critical greenhouse engineering claims should be prioritized first for scientific and safety relevance?
6. What is the applicable policy for external commercial LLMs, AI disclosure, repository privacy, IP and publication? Is the current public repository appropriate?
7. What date and format would be most useful for the next review, and should this brief be incorporated into the internship progress log/timesheet?

## 9. Evidence links and reproducibility index

**Main repository:** https://github.com/leadingproblemsolver/qeeri-agricultural

**Core archived protocol and experiment:**
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/main/research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/main/research/greenhouse_llm_feasibility/PROTOCOL_V0.md
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/main/research/greenhouse_llm_feasibility/TEST_A_001_BASELINE_RESPONSE.md
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/main/research/greenhouse_llm_feasibility/TEST_A_001_INITIAL_CLAIM_REVIEW.md
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/main/research/greenhouse_llm_feasibility/TEST_B_001_SOURCE_PACKET.md

**Provenance branch (not merged):** `research/human-ai-provenance-v1`
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/research/human-ai-provenance-v1/research/greenhouse_llm_feasibility/HUMAN_AI_PROVENANCE_PROTOCOL_V1.md
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/research/human-ai-provenance-v1/research/greenhouse_llm_feasibility/C01_SOURCE_VERIFICATION_RECEIPT_2026-11-08.md

**Site-data requirements branch (not merged):**
- https://github.com/leadingproblemsolver/qeeri-agricultural/blob/docs/greenhouse-feasibility-evidence-2026-11-07/docs/greenhouse/FEASIBILITY_EVIDENCE_REQUEST_2026-11-07.md

## 10. Final settlement

**What changed:** A bounded experimental question, frozen prompt candidate, first baseline response, three initial claim checks, a prepared evidence packet, a narrow human fundamentals pass and an explicit human–AI provenance scheme are documented with GitHub receipts.

**What did not change:** No controlled Test B result, no comprehensive scientific validation, no recorded independent expert approval, no verified Qatar site design or completed institutional permissions.

**Who changed behavior/access:** GitHub records are available for technical inspection; **no mentor or independent reviewer response is verified**.

**Next external evidence event:** Supervisor responds to 7 specific decisions above, then a completed archived Test B and an independently judged claim-level comparison.

# QEERI Human–AI Provenance and Research Accountability Protocol — v1

**Status:** Proposed research-team operational procedure; **NOT** a certified HBKU/QF policy or supervisor-approved protocol.  
**Date:** 2026-11-07  
**Scope:** `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0` and Test A / Test B of the greenhouse LLM feasibility evaluation.  
**Research responsibility:** Human researcher; qualified scientific and engineering sign-off remains separate.

## 1. Institutional baseline versus project controls

### Identified institutional references (verify latest applicability with supervisor)
- HBKU Research Misconduct Policy, RE EC.03.009, effective 2025-08-28: covers HBKU-affiliated research, including trainees; addresses fabrication, falsification, plagiarism and research integrity. https://www.hbku.edu.qa/sites/default/files/250828_Final_President%20Approved_Research_Misconduct_Policy.pdf
- HBKU Dissertation/Thesis/Project Formatting and Submission Guidelines (2025), declaration section: disclose AI use and consult supervisor/college/program about acceptability **for theses/projects governed by those guidelines**. Not automatically imposed as an internship form. https://www.hbku.edu.qa/sites/default/files/thesis_formatting_and_submission_guidelines_-_english.pdf
- HBKU IP Policy AC-F-11.V01 incorporating QF policy: institutional IP ownership and disclosure may apply; determine contractual permissions before public release. https://www.hbku.edu.qa/sites/default/files/intellectual_property_policy.pdf

**Unknown / requires written direction:** QEERI-specific AI use policy and declaration format; allowed AI vendors and research-data transfer; whether public repository content is approved for release; institutional ownership and publication/embargo rights; specific reviewer and sign-off requirements. The links above are not proof those permissions have been granted.

### Additional local safeguards (our procedure, not quoted institutional rules)
Preserve raw model data, identify all AI assistance, check primary sources, label derived calculations, retain decision rights with humans, restrict confidential data and require qualified review before engineering advice.

## 2. Human versus AI attribution

| Stage | AI contribution (record explicitly) | Human obligation (record actual evidence) | Sign-off authority |
|---|---|---|---|
| Question/case | Prompt drafting, alternatives | Freeze purpose and scope; authorize changes | Researcher / supervisor for protocol |
| Literature | Discovery, summary, extracted candidate claims | Open original, verify page/section, date, units, contextual applicability, license | Researcher; domain expert if scientific judgment |
| Answer A/B | Model generation; cannot be an authoritative source | Preserve exact prompts, contexts, raw outputs, tools/settings, time and session separation | Human evaluator |
| Claim check | Suggest counterexamples/checks | Independently verify against primary evidence; annotate whether supported/contradicted/unassessable | Human evaluator, then independent reviewer |
| Calculation | Suggest formula/code | Derive/check units, boundary conditions, manually test at least one known/edge case, document assumptions | Relevant engineer where safety-critical |
| Code | Generate snippets/tests and proposed fixes | Reconstruct execution, run tests, inspect diffs, negative/hostile tests, report actual commit and failures | Human developer and reviewer |
| Report | Draft summaries/tables | Verify claims, acknowledge use, resolve discrepancies, approve final wording | Named responsible human |
| Installation recommendation | Identify missing data/alternatives | Prohibit unmeasured sizing and obtain regulated approvals | Qualified greenhouse/HVAC/structural/water/electrical specialists |

## 3. Separate three independent layers for every claim

1. **Origin:** `HUMAN_AUTHORED | AI_GENERATED | SOURCE_EXCERPT | DERIVED_CALCULATION | MEASURED_DATA | UNKNOWN`. Origin is not truth.
2. **Evidence verdict:** `UNVERIFIED | SUPPORTED | CONTRADICTED | NOT_ASSESSABLE`. Requires actual check; do not infer from origin.
3. **Review status:** `NOT_REVIEWED | HUMAN_CHECKED | REPRODUCED | SPECIALIST_REVIEWED | ACCEPTED_FOR_SCOPE | REJECTED`. Scope-specific approval only; no automatic promotion.

Additionally record `release_scope = PRIVATE | PUBLIC_REDACTED | PUBLIC_APPROVED`; default **PRIVATE** for all raw records unless use and distribution rights verified. Metadata may be public only if de-identified and approved.

**Invariant:** AI cannot self-certify a human check, scientific validation or regulator authorization. Source citations with no checked passage/location remain UNVERIFIED. Test pass count is software evidence only, not scientific accuracy.

## 4. Minimal claim ledger — one row per consequential claim

| Field | Meaning |
|---|---|
| claim_id | Stable ID, never silently renumber |
| exact_claim | Literal text or exact scoped paraphrase |
| origin | One of the origin values above |
| artifact_id, path, version/SHA | Raw provenance; where claim came from |
| model/provider/build | Literal reported identifier; UNKNOWN if not exposed |
| prompt_id, context_packet_id | Frozen IDs and integrity hashes |
| timestamp, session, tool/search setting | What is actually known, not inferred |
| primary_source_id, URL/DOI, page/section | Original authoritative record and checked location |
| evidence_excerpt_or_locator | Short permitted excerpt or detailed locator; no invented quotation |
| applicability | Crop, site, season, units, measured/modelled/general principle |
| check_method, checker, date, result | Reproducible human verification |
| limitations and severity | What claim does not establish; safety issue |
| review_decision, reviewer, date | Blank until actual review |
| visibility/rights | PUBLIC only after approval |

## 5. Frozen A/B experiment — evidence flow

`Fixed case + identical prompt + same model/settings` -> **A** (no supplied reference packet) and **B** (verified fixed packet) -> immutable raw answers -> *independently pre-established* ground-truth matrix -> claim-by-claim human scoring -> safety gates -> result -> supervisor review.

- **A** raw artifact: `TEST_A_001_BASELINE_RESPONSE.md`. Provenance and completeness must be inspected, not presumed.
- **B** packet: `TEST_B_001_SOURCE_PACKET.md`; as of this protocol **Test B NOT RUN**. A source packet is NOT a model output.
- For B: use fresh separate session, same frozen prompt and model/settings as far as exposed; only supplied verified passages change. Record exact input/output and context. If unable to match settings, mark comparison confounded; don't claim causal improvement.
- Human-led reference matrix: target 20–30 checkable claims with precise original-source locators. Existing three Test A claim checks are *initial*, not independent validation.
- Score the declared criteria in `PROTOCOL_V0.md` and record blind review where possible; second independent human annotation is needed before broader model-quality claims.
- **Critical stop:** invented design numbers, unsafe electrical/safety/cooling advice, forged source or transfer of published greenhouse measurements as project measurements => `NOT_INSTALLATION_READY`.

## 6. Example recorded claims — do not overstate

| ID | Claim | Origin | Evidence | Current permissible verdict |
|---|---|---|---|---|
| C01 | Evaporative cooling depends on outdoor wet-bulb conditions and effectiveness | AI-generated Test A (reported; see raw artifact) | UF/IFAS AE069 section 'Systems Efficiency', examined during initial review | SUPPORTED as general engineering principle; Qatar site unmeasured; HUMAN_CHECKED initial |
| C02 | Dry-bulb temperature alone cannot establish cooling demand | AI-generated Test A (reported) | UF/IFAS AE069 temperature gradients / ventilation principles | SUPPORTED generally; site capacity NOT_ASSESSABLE |
| C05 | One temperature sensor cannot demonstrate spatial uniformity | AI-generated Test A (reported) | UF/IFAS AE069 temperature-gradient and controls sections | SUPPORTED as general principle, no Al-Shahaniya field verification |
| C-SITE | This proposed project has enough water, electricity, or heat rejection | Not established | No matched measured project data | UNVERIFIED / BLOCKED; **do not invent** |
| C-B | References improve Test B accuracy compared with A | Not observed | B not executed | NOT_ASSESSABLE |

The project uses a published Al-Shahaniya case as a **type reference**, not as project measurements, construction drawings or permit specifications.

## 7. Submission disclosure template (adapt only after mentor approval)

> **AI assistance disclosure (proposed):** AI tools assisted with drafting protocol language, generating candidate engineering responses, suggesting source searches, and/or generating code as documented in the provenance ledger. Model-produced text is preserved separately from human-established reference claims and original-source verification. The human researcher takes responsibility for the reported methods, checks and limitations. No site-specific engineering capacities, field measurements, scientific approval or external expert sign-off are claimed without evidence. Relevant model identifiers, prompts, run conditions and contributions are recorded in the experiment artifacts.

Do not mark a disclosure as supervisor-approved without a recorded reply.

## 8. Release/security and personal accountability gate

- Public repo **does not prove** institutional authorization. Do not add internship records, private email, unpublished data, exact private field coordinates, confidential quotations, full copyrighted articles, API keys, or unapproved research materials.
- Maintain a private audit log for raw sessions and human identities if necessary; publish only authorized, minimal evidence metadata.
- For each assistant-created commit: human inspect complete diff, ensure factual evidence states, run reproducibility checks, document what was actually executed. Agent commit is not proof of human authorship or review.
- Before any external publication, obtain supervisor/institutional confirmation of permitted AI use, data classification and IP/release rights.

## 9. Next concrete action and termination

1. **Human** confirms Test A response and metadata correspond to the original frozen run.
2. **AI-assisted execution** of Test B in a fresh session with the approved fixed packet; preserve untouched response + settings; do NOT call it verified.
3. **Human** checks the identical claims in both outputs against actual source passages and fills the ledger.
4. **Independent reviewer / mentor** accepts, rejects or requests revisions to a narrow finding.
5. Emit: `A_RAW | B_RAW | GROUND_TRUTH | SCORING | SAFETY_VERDICT | DISCLOSURE | REVIEW_DECISION`. If any is missing, report precisely `INCOMPLETE` and what's absent.

**Current external decision:** No QEERI or HBKU specialist sign-off has been established on this provenance protocol. Next research transition is the unrun Test B and subsequent human check; next governance transition is mentor review of the AI disclosure/release policy.

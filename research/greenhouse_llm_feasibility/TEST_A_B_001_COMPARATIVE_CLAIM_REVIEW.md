# TEST A/B — P0 comparative claim review and pre-RAG decision (8 Nov 2026)

**State: REVIEWED AVAILABLE EVIDENCE / NOT A CONTROLLED COMPARATIVE RESULT / RAG P1 BLOCKED.**

## 1. Actual records (do not conflate)
- **A — chat baseline:** `main:research/greenhouse_llm_feasibility/TEST_A_001_BASELINE_RESPONSE.md`. Transcribed from original conversation, not byte-identical export. GPT-6 reported; model build/temperature/seed unknown; no research sources supplied.
- **B1 — evidence-assisted response, recorded as 7 Nov:** `research/human-ai-provenance-v1:research/greenhouse_llm_feasibility/TEST_B_001_BASELINE_WITH_SOURCES.md`. Produced in same conversation and web used for source retrieval. Frozen Section 5 prompt and source packet declared. Not a fresh independent session.
- **B2 — evidence-assisted response, recorded as 8 Nov:** `research/greenhouse-llm-feasibility-pilot:research/greenhouse_llm_feasibility/TEST_B_001_BASELINE_WITH_SOURCES.md`. Pre-generation local time 08:20:47 +03, reported GPT-6; generated in ongoing conversation already exposed to A and claim review; retrieval via GitHub before generation. Not cleanly independent.
- **Earlier API experiment scaffold:** `runs/ARM_A_RUN.json`, `runs/ARM_B_RUN.json`, `runs/RESULTS.json` on this branch explicitly record `NOT_EXECUTED` owing to missing `ANTHROPIC_API_KEY`. These refer to a *separate planned Claude API pair*, not the completed chat A and B observations. Do NOT rewrite those JSON statuses to imply ChatGPT output was generated through the Python harness.

## 2. Strict first claim comparison — manual, descriptive (no numeric scoring)

| Claim | Arm A output | Arm B2 output | Independent evidence & permissible conclusion |
|---|---|---|---|
| C01: pad wet-bulb/effectiveness | General statement with no supplied research citation; refuses precise supply temperature | Gives pad temperature equation and cites supplied UF/IFAS AE069 S01, distinguishes pad outlet vs canopy | **Source-supported general principle**. More explicit citation in B, but correctness improvement not causally proven. |
| C02: greenhouse cooling demand cannot be inferred from outside temperature alone | Describes solar, sensible/latent loads, airflow and unknown site conditions | Addresses gradients and cites IFAS S02; notes site heat balance still required | Both express the broad engineering constraint; B's S02 supports a **spatial gradient**, not a full Qatar total-load calculation. |
| C05: one sensor cannot show uniform crop-zone temperature | States single temperature sensor cannot show greenhouse uniformity | Links spatial variation and sensors to IFAS S02/S03; requests representative multi-location measurement | Both contain an appropriate limitation; supplied citation does not create a measured site result. |
| Scope/safety | Withholds fan/electrical/pump sizing and construction decision | Also withholds unsupported capacities and construction decision | No observed categorical critical safety failure in these selected statements. NOT a full eleven-system safety review. |

**Observed:** source packet helped B present clearer source-to-claim attribution on selected statements. **NOT observed:** quantified increase in correctness, independent blinded scoring, reduction of hallucinations over repeated trials, or an empirical benefit requiring RAG.

## 3. Protocol and evidence contamination audit

1. Two different frozen prompts exist (`PROTOCOL_V0.md` shortened prompt vs `PROTOCOL_V0_response.md` Section 5). Archived ChatGPT comparison declares Section 5; separate Python/Claude framework has its own `prompt_A.txt`. Never compare different protocols or vendors as the same A/B trial.
2. Both observed B responses were generated in **ongoing chats** with prior exposure; not isolated. Neither supports a clean experimental estimate of source-grounding benefit.
3. Exact model build, sampling settings and reproducible session snapshots are unavailable; A archive is a transcription.
4. B1 and B2 share a filename on **different branches**; preserve separate provenance and immutable identifiers. Do not overwrite one with the other.
5. Three source-backed claims are insufficient for a general scientific conclusion; local greenhouse climatic measurements, second human evaluator and full reference matrix absent.

## 4. P0 GO/NO-GO decision

**Question:** Is there enough observed, attributable failure to justify building RAG now?

**Decision: NO-GO to RAG implementation as of this review.** Reason: no clean scored A/B comparison demonstrates an unsolved **retrieval** failure; static allowed source packets already support the selected cooling claims, while physical calculations/field-data gaps cannot be cured by adding a vector store. This is a **bounded research gate**, not a claim RAG can never help.

### Smallest dependency-correct next experiment (not new infrastructure)

1. **Freeze canonical case and record immutable metadata:** Use one agreed prompt (for ChatGPT pilot, Section 5 of `PROTOCOL_V0_response.md`); source packet `TEST_B_001_SOURCE_PACKET.md`; identify A/B outputs by branch/file/hash and report known deviations.
2. **Pre-register 3–5 independently checked consequential claims** (C01, C02, C05 plus one unsupported or stale fact if an original primary source is accessible). Record source locator, scope and safety severity before scoring.
3. **Blind-score archived A and B descriptively now**, separately marking `CORRECT`, `SUPPORTED`, `UNSUPPORTED`, `UNASSESSABLE` and any citation-resolution mistakes. This cannot by itself erase contamination.
4. If comparative inference is requested, **run two clean separate sessions** (same model/configuration and prompt, tools OFF during generation; B additionally receives fixed verified excerpts). Preserve raw outputs and exact context. If settings unavailable, declare confounding rather than claiming causal benefit.
5. **Pre-RAG discriminator:** find at least one repeated consequential error caused by *missing/dynamic source evidence* that a fixed approved packet cannot efficiently solve. Demonstrate retrieval of relevant passage versus irrelevant/wrong-jurisdiction/absent-passage negative controls; measure false support and abstention. If no such error, use static verified context + human review, not RAG.

### P1 RAG acceptance criteria (future; not claimed achieved)
- Primary-source eligibility and permitted reuse established; independent claim reference accepted.
- Relevant passage retrieved in positive tests; wrong country, wrong time, misleading lexical match and no-answer controls do NOT generate false support.
- Every output claim cites a passage that actually entails it; abstains on unavailable inputs.
- Outperforms the **simpler source-packet baseline** on a predefined consequential error with acceptable latency/cost and no safety regression.
- Supervisor has confirmed research scope, repository exposure/IP constraints and reviewer.

## 5. Evidence settlement
- **New in reality:** documented exact distinction between A, two actual B chat outputs and separate unexecuted API scaffold; initial selected-claim comparison and a defensible P0 NO-GO-to-RAG verdict.
- **Unchanged:** no controlled repeat, independent blinded human judgement or scored model-quality improvement.
- **Next irreversible event:** supervisor accepts canonical protocol and review threshold, or two clean controlled runs plus human claim-level scoring are recorded.

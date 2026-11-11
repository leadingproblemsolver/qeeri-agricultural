# 3 — How to answer the research question

A good experiment compares what the model says **before and after receiving verified evidence**, while changing nothing else of significance.

## The simplest fair comparison
1. Choose one consequential question and define what a correct and appropriately cautious answer would look like **before new outputs**.
2. Verify the evidence packet with original source passages.
3. Run **A** without that packet and **B** with it; retain complete original answers and what model/settings were used. If those conditions cannot be kept comparable, label them exploratory.
4. Independently check each claim for correctness, source support, Qatar applicability, missing inputs and unsafe overconfidence.
5. Report the difference *or* report that the experiment was blocked. Do not call n=1 proof of general improvement.

**Original larger benchmark:** 50 questions (40 general / 10 Qatar) × 4 providers was planned. Original controlled run evidence and the full reference-key status must be audited before treating “200 answers” as accepted.

**RC01:** synthetic 38°C dry bulb, 24°C wet bulb and 85% pad effectiveness give **26.1°C at pad outlet**. It is a valid worked calculation, **not** proof of safe canopy temperature and not a trustworthy RAG comparison. Prior Gemini summaries conflict about whether any fair source condition ran.

**RC04:** ask whether the canopy can be guaranteed at or below 28°C from only those inputs. Correct conclusion: **no, insufficient information**; no crop-zone guarantee. The source-backed key is under human review and valid matched A/B model outputs are not established.

Read [RC04 question/key](../../research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md) and [foundation/scoring](../../research/greenhouse_llm_feasibility/RC04_FOUNDATIONS_AND_SCORING.md).

**What you do next:** finalize the exact source-to-claim check and independent review slot; then produce a raw A/B receipt only if isolation and authorized model access are available. No additional prompts or model-training work are needed for documentation.

[Technical continuation](technical/README.md)

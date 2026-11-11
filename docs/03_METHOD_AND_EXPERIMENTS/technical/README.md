# 3 — Experimental procedure and reproducibility contracts

Use original paths; do not clone a second pipeline:
- [Full greenhouse protocol](../../../research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md)
- [Existing A transcript, not a byte-identical provider export](../../../research/greenhouse_llm_feasibility/TEST_A_001_BASELINE_RESPONSE.md)
- [Test A claim review](../../../research/greenhouse_llm_feasibility/TEST_A_001_INITIAL_CLAIM_REVIEW.md)
- [B evidence packet — file presence is not an executed model run](../../../research/greenhouse_llm_feasibility/TEST_B_001_SOURCE_PACKET.md)
- [RC04 frozen question and incomplete comparative receipt](../../../research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md)
- [RC04 source/physics and 5-item scoped scoring](../../../research/greenhouse_llm_feasibility/RC04_FOUNDATIONS_AND_SCORING.md)
- [Original benchmark recorder](../../../tools/qeeri.py) and [score agreement utility](../../../tools/score_agreement.py)
- [RAG evidence and test implementation — unmerged branch](https://github.com/leadingproblemsolver/qeeri-agricultural/tree/claude/qeeri-rag-v0-18awxg/research/qeeri_rag_v0)

**Eligibility filter for a controlled run:** exact unchanged question and system prompt, same provider/model build and actual accessible settings, no tools/search/personalization variations, isolated sessions, model start/end timestamps actually observed or marked unknown, exact supplied packet and hash, full unedited response, source rights, independent reference key prepared before outputs, human scorer with traceable rationale. Mark `EXPLORATORY` / `CONTAMINATED` / `INCOMPLETE` / `NOT_EXECUTED` when any critical contract is missing. Do not retrospectively invent model versions, seeds, timestamps or human judgments.

**RC04 minimum valid answer:** calculated pad outlet=26.1°C under synthetic assumptions; canopy<=28°C is `NOT_ASSESSABLE`, identify missing heat/moisture transport inputs; never prescribe equipment. Five provisional C1–C5 criteria are **scoped to RC04**, not automatically the original five-axis 0–2 benchmark rubric.

**Report a valid A/B comparison only when actual matched A and B responses are saved.** The fabricated-sounding `e3b0c442...` packet hash in a user-supplied receipt is the SHA-256 of an empty file, not the source packet. “5/5” self-scoring and provider labels from prose are not independent run evidence.

**Manual before automation:** calculate and verify source claims by hand once; then automate only the failure mode demonstrated by real trial evidence. No training until the simpler interventions have been compared fairly.

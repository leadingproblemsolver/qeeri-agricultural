# P0 closed; next research gate is whether RAG is warranted

## P0: stop regenerating finished preparatory material
- **COMPLETED preparation:** 50-question research set (40 agronomy textbook-derived, 10 Qatar-specific), prompt/protocol, five-axis 0–2 rubric, model choices ChatGPT/Claude/Gemini/DeepSeek, an offline execution/check framework.
- **Approval received 25 Oct:** Dr. Sa’d approved the 50-question design/rubric, manual independent browser route and metadata protocol.
- **NOT established:** 200 valid independently collected responses; 50 supervisor-verified answer keys; complete blind grades; comparative rankings. The P0 *asset set* is done, not the empirical research phase.
- Keep prior approximately 30 exploratory answers separated from controlled outputs. Freeze manifest instead of revising question counts due to recency or focus drift.
- The greenhouse Test A archive and 8 Nov in-chat Test B are a bounded pilot. Test B must be cleanly rerun before causal-style comparisons; prior exposure is documented.

## Decision before further RAG implementation
**Question:** Which observed failure would require retrieval, rather than cleaner prompting, source packet, an external deterministic calculator, or a human expert?
1. Define representative question and consequential failure: unsupported crop/greenhouse claim, outdated citation, wrong conversion, missing required inputs, misplaced confidence.
2. Freeze benchmark cases and source eligibility. Ensure source permission and independently reference-checked answer.
3. Compare fair baselines in clean sessions: no source; concise permitted source packet; retrieval only if a non-retrieval baseline leaves an evidence-availability gap; deterministic calculation when the error is arithmetic.
4. For a retrieval trial, test **positive AND negative controls**: relevant snippet at top, irrelevant lexical match, wrong country/time, contradictory source, missing value, forbidden publication. Record retrieval hit/false-support rates and abstention.
5. Human reviewer judges citation-to-claim entailment and consequences. Model-supplied citations are not self-certifying.
6. Evaluate operating cost, source update burden, privacy/IP, latency, maintainability, reproducibility, and whether a simpler text packet solves the same cases.
7. Go only if predefined reviewed error reduction outweighs new retrieval-induced false support. Otherwise **NO-GO: keep simple verified context + review**.

## Invariants
- No externally consequential cooling, salinity, irrigation, legal or profit recommendation from an incomplete input record.
- The context length/session contamination in the in-chat Test B prevents clean inference about source assistance.
- A software test pass proves specified software behavior; an agronomic correctness claim requires reference verification.
- If the question is ambiguous, state required missing inputs, not invented precision.
- If no error has been established, do not propose training or new retrieval infrastructure.

## Next bounded deliverable
`TEST_A_B_001_COMPARATIVE_CLAIM_REVIEW.md`: first score source applicability and claim validity (C01/C02/C05), flag contamination; cleanly rerun only if supervisor accepts the case/protocol; then decide pre-RAG GO/NO-GO with evidence, not architecture preferences.

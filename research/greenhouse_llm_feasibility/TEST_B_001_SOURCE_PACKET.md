# Test B 001 — verified source packet and execution boundary

Case: `QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0`
Comparison: Test A archived in [TEST_A_001_BASELINE_RESPONSE.md](TEST_A_001_BASELINE_RESPONSE.md).
**Status: Test B NOT RUN.** This file contains the verified source material to supply to a separate, fresh model session, not a generated Test B result.

## Verified source for the evidence-assisted condition

University of Florida IFAS, *Fan and Pad Greenhouse Evaporative Cooling Systems*, publication AE069/CIR1135.
Official full text: https://ask.ifas.ufl.edu/publication/AE069
Official PDF: https://ask.ifas.ufl.edu/publication/AE069/pdf
Alternative official-hosted page: https://edis.ifas.ufl.edu/AE069

Only a short excerpt is reproduced below; the remainder is paraphrased with section locations to avoid reproducing copyrighted text.

### S01 — Evaporative Cooling / Systems Efficiency

Verbatim source excerpt (12 words): **"Wet bulb temperature is the lowest temperature that can be reached"** [the source qualifies this as evaporation-only cooling].

Source-backed engineering equation (mathematical expression, not a measured value):
`T_pad_out = T_out_drybulb - η × (T_out_drybulb - T_out_wetbulb)`
where temperatures are in °C and η is pad saturation effectiveness as a fraction from 0 to 1. The paper describes this equation in **Systems Efficiency**. This estimates **air immediately leaving the pad**, not uniform crop-zone temperature or total greenhouse cooling capacity.

### S02 — Fan and Pad Evaporative Cooling Systems / Temperature Gradient

The IFAS publication explains that air passing through the wetted pad subsequently gains heat while crossing the greenhouse. The air near the pad is generally cooler than the air near exhaust fans, and the spatial temperature rise depends on airflow, internal obstructions, plant cover, floor and roof configuration. These are general fan-and-pad observations, **not Al-Shahaniya measurements**.

### S03 — Controls

The IFAS publication describes greenhouse controls and temperature sensors as relevant to monitoring and regulating greenhouse conditions. It does **not** establish that a single reading measures spatial uniformity. Verifying uniformity would require representative multi-location measurements.

## Boundary and source applicability

- The source is primarily greenhouse fan-and-pad guidance, including Florida operating context. Do not treat its Florida weather examples, suggested layouts or fan capacities as design specifications for Qatar.
- The Al-Shahaniya paper (https://doi.org/10.1080/01430750.2022.2088617) is the named Qatar reference greenhouse, but its full text could not be independently retrieved during this preparation. **No Qatar greenhouse measured values are supplied.**
- No measured site dry-bulb/wet-bulb, cooling effectiveness, greenhouse geometry, crop-zone temperature or cooling load is available.
- Do not size equipment or claim the target indoor temperature can be maintained.

## Execute Test B (separate fresh model session)

1. Use the **identical fixed prompt** from [PROTOCOL_V0_response.md](PROTOCOL_V0_response.md), Section 5, without rewriting it.
2. Use the same model configuration as Test A insofar as available. Record model, date, local time, search/tools OFF, temperature/seed if exposed (otherwise UNKNOWN).
3. Supply this packet as **additional reference context**, clearly separated from the unchanged prompt. Test A had no source packet; this is the experimental treatment.
4. Save the complete **unedited** response and metadata as `TEST_B_001_BASELINE_WITH_SOURCES.md`. Do not claim the test was run until the model has actually generated the response.
5. Evaluate C01, C02, C05 and the other safety-critical claims against the original sources. Distinguish citation accuracy, general principle validity, and Qatar-specific applicability.

**Experimental limitation:** This is a first pilot, not a rigorous causal study; prompt/context length differs between conditions, and session/model nondeterminism can affect outputs. No claim of improvement without both actual outputs and independent scoring.

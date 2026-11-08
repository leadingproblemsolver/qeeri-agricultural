# Nov 5–8 | foundational capability exercises and enforcement

## Pedagogical correction
Advanced models, code, RAG scaffolds, academic terminology, and even passing unit tests were built **before** reliable source interpretation and independent engineering reasoning were consistently demonstrated. The weekend redirected work from building output volume to testable scientific understanding. This is not a claim those fundamentals have all been mastered.

## Exercised in sequence
1. **Site vs example:** Read Al-Shahaniya as a published illustrative greenhouse, not a construction plan. Identify the *measurement*, source context, date/site, and whether it is modelled or measured. Actual figure verification remains open.
2. **Five-check row test (Nov 6):** For each number, state (i) what it measures, (ii) units, (iii) location, (iv) collection period, (v) whether it answers the specific question. **Three existing spreadsheet entries failed eligibility for cooling sizing**. Rejection was the correct research output, not a design failure.
3. **Manual physics explanation:** `Q = U × A × ΔT` is only covering-envelope sensible transmission under assumptions; `ρ × airflow × c_p × ΔT` represents sensible flow heat exchange. Do not confuse either with total greenhouse cooling power. The Nov 6 supervisor email reported no successful independent hand calculation yet; later work is practice until reproducibly demonstrated.
4. **Psychrometric invariant:** For ordinary direct evaporation, incoming wet-bulb is an ideal limit; `T_pad_out = T_db − η(T_db − T_wb)`. Require explanation of inputs, output location and η as effectiveness, not defaulting to 100%.
5. **Spatial reasoning:** Pad outlet air ≠ crop canopy temperature. As incoming cooled air traverses the greenhouse, solar gains, airflow restriction, crop transpiration, relative humidity, geometry and shading matter. Do not invent a measured canopy value.
6. **Claim-source checks:** C01 (wet bulb/pad efficiency), C02 (gradients/other cooling loads), C05 (single sensor cannot establish uniformity) linked to prepared UF/IFAS S01–S03; source-based general principles, no measured Qatar outcomes.
7. **Engineering refusal:** No fan/pump/pipe/breaker size, thermal guarantee, yield or return on investment without site measurements and competent review; 'do not build yet' is a legitimate feasibility result.
8. **Repository provenance:** Archive unedited model response and reference packet separately, preserve frozen prompt, record unknown seed/temperature and session history; 8 Nov Test B contaminated by Test A exposure.

## Forced answer format (for every exercise; reuse exactly)
```
Claim/question:
What is known (source + exact location + unit + geography + date):
What is assumed:
Input -> operation -> output (with dimensional check):
What this output does NOT show:
Counterexample / hostile check:
My independent explanation (without AI):
Verdict: PASS / FAIL / CANNOT VERIFY
Evidence link and next smallest missing input:
```
**Enforcement:** No bypass by asking AI to rewrite the exercise. First give a manual explanation, then check formula/source, then run a negative/edge case, then record correction. A generated answer or five software tests is not human mastery. Re-test after an interruption from memory, not by rereading an answer.

## Results (do not inflate)
- Passed at source-check *boundary awareness*: three table entries rejected and missing inputs preserved.
- 3 preliminary Test A source checks documented; no blind independent scientific score.
- Initial failed handwritten calculation and source-location performance explicitly preserved.
- New desired capability check: independently derive a cooling-pad estimate with assumed inputs **and** explain why it cannot estimate tomato canopy temperature; zero fabricated site values.

# QEERI greenhouse demo — start here

**Question:** Does adding checked evidence help an AI answer an agricultural question more accurately and cautiously?

**Current answer:** We do not know yet. The repo has working code and demonstration checks, but no accepted controlled comparison showing improvement.

## What a viewer can see

`Inputs → Source and unit checks → Calculation or safe refusal → Explanation with source and limitations`

- **Input:** A greenhouse scenario from a published source, or a clearly labelled illustrative example.
- **Check:** Is the source applicable to the place, crop, date and measurement? Are inputs and units complete?
- **Output:** A calculation or reported finding, plus what it cannot establish.
- **AI test (next step):** Ask the same model the same frozen question twice, once without sources and once with a fixed, independently reviewed source packet. Compare claim accuracy and appropriate refusals.

**Run the demo:** `python -m pip install pyyaml` then `python demo/greenhouse/run_demo.py` (Python standard library only). Ten checks test reproducible arithmetic, retained values, source scope and refusal when evidence is missing. They are **not** ten greenhouse trials, expert approvals or AI A/B runs.

## Data we collect

| Group | Examples | Used for |
|---|---|---|
| Weather | Dry/wet-bulb temperature, humidity, sun, wind, timestamp/site | Cooling boundary |
| Structure | Area, volume, cover, insulation | Heat balance |
| Cooling | Pad effectiveness, airflow, fan position, operating configuration | Pad/airflow checks |
| Crop | Species, growth stage, canopy conditions, transpiration | Biological limits |
| Soil and water | Salinity, moisture, sampling depth, source, water quality | Suitability checks; soil model blocked without matching lab data |
| Power and cost | Electricity, water, costs, yield and price | Descriptive comparisons, not farm profitability |
| Evidence and AI | Paper ID, exact page/quote, observed vs simulated, units, rights, run ID, model/prompt, reviewer | Traceability and fair scoring |

For **every input**, record its value, unit, source and exact locator, date/place, whether it was measured, simulated or assumed, a missing-value state, and any required review. Never convert a published regional example into Qatar site measurements.

## The ten included checks

1. Pad outlet under **illustrative** 38°C dry-bulb, 24°C wet-bulb and effectiveness 0.85: 26.1°C. This is **not crop-zone air temperature**.
2–3. A reported Al Khor study's ambient CFD boundary and separately described pad boundary; do not mix measured and simulated status.
4–5. The Al Khor study's reported simulated differences for 20 and 40 air changes per hour.
6–8. Three reported tomato system rows in a Qatar crop-performance source; comparisons are descriptive, **not a project design**.
9. A historical KAHRAMAA power-factor provision; current code check still required.
10. Refuse an Al Shahaniya numerical design claim when the exact supporting passage is missing.

The **single input file** `demo/greenhouse/qeeri_evidence.yaml` contains the ten cases and the source metadata, quoted passages, units and review states together. The older `cases.yaml` remains as an earlier fixture. It is intentionally easy to extend with data found in other published GCC studies. **The cases reproduce candidate information transcribed from a supplied source register; the original publications have not all been independently rechecked.**

## Scientific test — not completed

1. Freeze one question (existing [RC04 candidate](../../research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md)).
2. Independently check the original passages and freeze a claim-level answer key.
3. Capture two matched, isolated raw model responses (baseline vs fixed verified evidence).
4. Have a qualified reviewer score factuality, source support, units, applicability and unjustified specificity.
5. Report measured differences, uncertainty, exclusions and whether evidence helped, did not help, or remains inconclusive.

Do **not** claim: greenhouse feasibility, crop death, a universal 28°C tomato cutoff, engineering equipment sizing, accepted improvement from RAG, or QEERI approval.

## What is blocked

- **Soil ML:** no matched verified laboratory soil targets and imagery.
- **Real greenhouse design:** no approved site-specific weather, equipment, canopy and water measurements.
- **Full benchmark:** complete independently checked 50-question reference keys and comparable four-model runs not established.
- **AI evidence effect:** no controlled, independently adjudicated A/B result.

**Next external evidence event:** a qualified reviewer accepts one source-to-claim key, followed by one matched A/B comparison.

### Find the rest without learning the whole repository

- [Five-stage research map](../../docs/README.md)
- [Existing evidence status](../../docs/02_EVIDENCE_AND_DATA/README.md)
- [Existing technical code](../../research_mvp/README.md)
- [Research result boundaries](../../docs/04_RESULTS_AND_SOFTWARE/README.md)

Keep historical documents and source files in place; this page is the shortest path to the demo, not another parallel project.

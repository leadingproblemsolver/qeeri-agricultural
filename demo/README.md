# Greenhouse example: ten checks

**Purpose:** Show how agricultural data moves from input → scientific rule or reported study value → output → limitation.

Run from the repository root:

```bash
python demo/check_cases.py
```

No installation is needed: `cases.yaml` is written as JSON, a valid subset of YAML, and the runner uses only Python's standard library.

## What you will see

| Cases | Plain-language check |
| --- | --- |
| 01–03 | Pad cooling arithmetic; missing canopy temperature; impossible weather input |
| 04–06 | Al Khor study location and two CFD ventilation scenarios |
| 07–09 | Three published Qatar tomato-system comparison rows, as transcribed in the *working* source register |
| 10 | Abstain when an original numeric source passage has not been verified |

## What goes in

The case file records: identifier, question, source key, kind of evidence, example inputs, expected output, and the decision rule. For real experiments, add original-document hash, exact page/table, measurement date, site, units, independent reviewer and raw model response. Do not silently treat these fields as present when they are not.

## Where numbers come from

The corresponding **working** register is at [master_source_register.yaml](../research/greenhouse_llm_feasibility/master_source_register.yaml). The register was uploaded by the researcher and has **not** been independently reconciled with all original PDFs. In particular, some literature statuses disagree with the repo's earlier evidence audit. The checks use the values in that working register; they **cannot prove the original authors reported those values**.

Inputs labeled ILLUSTRATIVE are deliberately made-up examples. PUBLISHED_STUDY_REPORTED means a number attributed to a named study in the working register, not independent verification of that attribution. Neither means verified Qatar field telemetry.

## What counts as a result

- **PASS:** The local calculation or rule matched this example's expected result.
- **FAIL:** The example or rule contradicted the expected result.
- **Scientific finding:** **Not obtained** by this script. Original paper checks, measured greenhouse performance, expert approval and matched model A/B runs require separate evidence.

**Next scientific test:** independently review the RC04 reference key, then compare preserved answers from the same AI model with and without a locked verified source packet. See [the existing RC04 test](../research/greenhouse_llm_feasibility/RC04_CROP_ZONE_ABSTENTION.md).

**Optional source search prompt (Gemini or another search tool):**

> Find up to ten real published greenhouse case studies from Qatar or the GCC. For each, provide DOI or publisher URL, exact table/figure/page, location, date, greenhouse type, crop, observed vs simulated status, weather conditions with units, ventilation/cooling parameters with units, reported crop-zone temperatures and energy/water measurements if available. Say NOT REPORTED for missing fields. Return YAML matching the example fields in cases.yaml; distinguish study measurements from assumed inputs. Do not invent values or claim a source was verified until I inspect its original text.

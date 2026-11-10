# Greenhouse cooling — smallest reproducible research case

**What is this?** One check of a dangerous reasoning leap: a correct pad-exit temperature does **not** prove the tomato crop is safe.

**Status: synthetic example only. No measured Al-Shahaniya weather, independent source-to-number review, crop-zone temperature, agronomic approval or LLM A/B result.** No one should use these calculations to select equipment.

## One equation, two calculations
From [UF/IFAS AE069, Systems Efficiency](https://edis.ifas.ufl.edu/AE069): `pad_exit_C = dry_bulb_C - effectiveness * (dry_bulb_C - wet_bulb_C)`.

| Scenario | Assumed inputs | Calculated pad-exit | What it DOES NOT establish |
|---|---|---:|---|
| Google-generated worked example | 40°C dry bulb, 20°C wet bulb, 85% pad effectiveness | **23.0°C** | Crop-zone temperature, tomato safety or a real Qatar observation |
| Synthetic extreme example | 45°C dry bulb, 31°C wet bulb, 85% pad effectiveness | **33.1°C** | Actual summer design weather, canopy temperature, harvest loss or equipment sizing |

The claimed Hamad International Airport weather record dated November 9, 2026 is **unverified and excluded**. November weather does not establish summer conditions.

## What was actually executed?
The supplied Python unit tests were run locally on November 10: **5 passed, 0 failed**. These verify arithmetic, input rejection and the refusal to infer crop safety. They do **not** verify engineering validity or improve scientific evidence.

The separate RAG branch once passed **74 software tests**, not 74 scientific checks. Its A/B/C model runs are still **NOT_EXECUTED**. Any pasted report claiming a measured 20%→100% LLM improvement, universal model failures, validated 30–32°C Qatar summer wet-bulb or an expert-approved 28°C crop threshold is **UNVERIFIED** absent original responses, data and independent scoring.

## Run it
From this directory:
```bash
python evaluate.py
python -m unittest discover -s . -p 'test_*.py' -v
```

Files:
- [case.json](case.json) — frozen question, two hypothetical inputs, missing inputs, unverified weather note.
- [evaluate.py](evaluate.py) — transparent pad-exit equation, no site predictions.
- [results.json](results.json) — numeric outputs and `NOT_ASSESSABLE` crop-safety status.
- [test_evaluate.py](test_evaluate.py) — five defensive/unit checks.
- [RESEARCHER_PROMPT.md](RESEARCHER_PROMPT.md) — optional AI critique; **not** an expert review.

## Where it fits in the actual research
The project has four workstreams: (1) soil salinity/moisture from UAV/Sentinel-2 with lab samples; (2) 50-question, four-model agricultural LLM reliability benchmark; (3) one Qatar greenhouse feasibility case; (4) optional retrieval if experiments prove it beats a fixed evidence packet.

**Current priority is workstream 2**, using workstream 3 as a concrete question. Do not train soil ML without lab labels and spatial validation. Do not expand RAG without a verified improvement.

## What must happen next?
1. Confirm primary Qatar research paper text and extract one **exact, checkable claim** with table/page, conditions and units. The uploaded Mahmood source YAML says `verified_full_text_extracted`; earlier repository ledgers say abstract-only. That conflict must be resolved against the original document. **Neither label alone is proof.**
2. Acquire attributable summer weather or explicitly restrict the experiment to a synthetic math question. Validate selected wet-bulb and pad effectiveness assumptions.
3. Make a ground-truth answer key **before** seeing new model outputs. Define pad-exit versus crop-zone separately; review crop threshold independently.
4. Run identical A/B prompts in new isolated sessions and save complete raw outputs and scoring receipts. If evidence does not measurably help, stop.
5. Seek qualified human review before calling any result scientifically established. An AI “research reviewer” can flag issues but cannot sign off its own outputs.

**Current decision: SOFTWARE EXAMPLE RUNS; SCIENTIFIC QUESTION NOT YET ANSWERED.**

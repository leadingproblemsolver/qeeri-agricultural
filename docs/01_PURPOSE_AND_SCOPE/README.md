# 1 — Why this research exists

## Original assignment
In the uploaded *LLM Greenhouse Feasibility — Research Execution Plan*, the mentor's task is **to assess whether existing LLMs can guide a non-expert through preliminary greenhouse production requirements for Qatar/GCC**: crop choice, structure, cooling, water/irrigation, electricity, sensors, installation sequence and economics. **Test existing models before choosing training, retrieval or a new model.** This phrasing is a researcher-maintained record, not a fresh recorded mentor approval.

The broader QEERI work also includes soil salinity/moisture estimation from UAV/Sentinel-2 and a 50-question agricultural LLM reliability benchmark. These are complementary research tracks, not four commercial products.

| Workstream | Question | What counts as a valid result | State |
|---|---|---|---|
| W1 Soil | Can imagery estimate measured salinity/moisture in Qatar and generalize to new sites? | Matched lab labels + imagery, spatial holdout, uncertainty/SWIR comparison | DATA_BLOCKED |
| W2 Agricultural LLMs | How often are four models correct, grounded and appropriately uncertain on 40 general + 10 Qatar questions? | 200 **controlled** responses only if captured; independent keys and scores | PREPARATION/EXPLORATORY |
| W3 Greenhouse | Can an existing LLM explain a scientifically defensible *preliminary* 11-subsystem decision process? | Sourced case, safe abstentions, valid calculations, expert review | PILOT |
| W4 Evidence assistance | Do fixed verified passages, retrieval or calculators improve the answer? | Matched A/B comparison, raw outputs, independent claim scoring | SOFTWARE EXISTS; BENEFIT UNPROVEN |

## What is proposed, not approved
The Al-Shahaniya semi-closed tomato greenhouse is a **proposed reference case** from published research. The uploaded execution plan says the exact crop/goal and QA case need mentor confirmation. Do not label that confirmation completed without an actual reply. A paper is not construction drawings.

## What we are not doing
No construction-ready designs; no unverified greenhouse sensor data; no model trained without suitable rights/labels; no claiming the four-model 200-run benchmark was completed from exploratory answers; no RAG build-out without incremental benefit; no public release of restricted materials.

**What to do next:** bring the mentor the 1-page scope decision: “Are we evaluating a non-expert's ability to identify greenhouse engineering inputs and safe next steps, using the Al-Shahaniya tomato case? Which crop, facility type and review criteria should we lock?” Preserve the response as an external receipt.

**For complete protocol:** [Original greenhouse protocol](../../research/greenhouse_llm_feasibility/PROTOCOL_V0.md) and [eleven-subsystem readable protocol](../../research/greenhouse_llm_feasibility/PROTOCOL_V0_response.md).

[Technical continuation](technical/README.md)

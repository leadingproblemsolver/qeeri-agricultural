# RC01 — frozen *synthetic* pad outlet arithmetic, not an A/B result

**Question:** In a hypothetical fan-and-pad system with inlet dry bulb 38.0°C, inlet wet bulb 24.0°C and pad effectiveness 0.85, what is pad-discharge dry-bulb temperature? Is it ≤28.0°C?

**Measurand:** pad discharge air dry-bulb, **NOT greenhouse canopy or tomato leaf temperature**.

**Source:** UF/IFAS AE069, `https://edis.ifas.ufl.edu/AE069`, section **Systems Efficiency**, equation `T_cool = T_out - (% efficiency)(T_out - T_wb)`; official web text checked 10 Nov 2026. This is a general engineering equation, not a site measurement or crop guarantee.

**Synthetic inputs:** `Tdb=38.0°C`; `Twb=24.0°C`; `eta=0.85`. Neither input comes from an Al-Shahaniya sensor or ERA5. `eta` is an **assumed pad effectiveness**, not a verified product rating.

**Calculation (independent arithmetic):** wet-bulb depression `38-24=14 K`; estimated cooling `0.85*14=11.9 K`; outlet `38-11.9=26.1°C`; arithmetic margin to **pad-outlet-only** target `28-26.1=1.9 K`. Required effectiveness for 28°C pad outlet under the same synthetic inlet conditions is `10/14 ≈ 0.714286`. No crop-zone, water-flow rate or physical uncertainty is calculated.

**Scoring key** (for future unaltered tests):
- Numeric pad-outlet answer: 26.1°C; ±0.5°C **scoring tolerance only**, not an uncertainty interval.
- Requires correct equation and identifying the *location* being calculated.
- Must not infer crop-zone safety or declare irrigation/cooling plant size.
- Must distinguish arbitrary 28°C evaluation threshold from an independently verified tomato physiology threshold.
- No source citation requirement in zero-context arm; citing fabricated source details is disallowed.
- Reviewer: `PENDING`; model experimental result: `NOT_ACCEPTED_CONTROLLED`.

**Gemini transcript evidence (10 Nov):** user-provided copied conversation reports that three outputs gave 26.1°C. It also describes mixed/changed prompts, ambiguous model identity and unsupported labeling of B as retrieval. Preserve as `EXPLORATORY_REPORTED`; no valid experiment comparison or raw API receipt established.

**Next:** do not optimize a trivial arithmetic prompt or claim `NO_MEASURED_IMPROVEMENT`. Run [RC04](RC04_CROP_ZONE_ABSTENTION.md).

# QEERI Agricultural AI — Scientific Research Navigator

**Working scientific briefing | 12 November 2026 | Research review draft**  
**Main question:** Can established agricultural science and documented evidence help an AI produce more correct, appropriately cautious answers for Qatar?  
**Focus:** a preliminary greenhouse cooling and water-demand case, nested within the original wider agricultural-LLM evaluation.  
**Reference location:** Al Shahaniya area, **25.37° N, 51.23° E** — a *research point supplied for analysis*, not verified coordinates of an instrumented greenhouse.  
**Research repository:** <https://github.com/leadingproblemsolver/qeeri-agricultural>  
**Greenhouse demonstration:** <https://github.com/leadingproblemsolver/qeeri-agricultural/pull/4> (draft, not merged at the time of this guide)  
**RAG prototype:** <https://github.com/leadingproblemsolver/qeeri-agricultural/pull/2> (draft, not scientifically validated)

> **Read this before using any numbers:** Reanalysis values are model-derived outdoor climate estimates, published study figures retain their original setting, and synthetic demonstrations are not field measurements. Source text found is not the same as an independently approved scientific claim. No greenhouse design, crop-safe canopy temperature, irrigation schedule, model advantage or construction decision has been established for Al Shahaniya.

## Navigate this document

1. [The five scientific questions](#1-the-five-scientific-questions)
2. [What evidence we already have](#2-current-evidence-and-its-limits)
3. [Inputs, scientific meaning and missing measurements](#3-scientific-input-map)
4. [Exact CDS selections — recommended easy route](#4-copernicus-climate-data-store-cds-collection)
5. [What we can calculate, and what we cannot](#5-physical-relationships-and-valid-inferences)
6. [Original papers and review status](#6-scientific-source-register)
7. [Quality checks for the first climate-data download](#7-climate-data-quality-and-evidence-receipt)
8. [Ten greenhouse demonstration cases](#8-what-the-existing-ten-cases-actually-demonstrate)
9. [AI evaluation and human scientific review](#9-the-experiment-that-would-answer-the-research-question)
10. [What to present to the mentors](#10-mentor-review-brief)
11. [Execution tracker and completion rules](#11-immediate-scientific-work-and-closure)
12. [Original references](#12-primary-references-and-reproduction-links)

---

## 1. The five scientific questions

| Question | What a valid answer requires | Current state |
|---|---|---|
| **1. How hot and humid is the outdoor air?** | Time-stamped observed or reanalysis dry-bulb, humidity/dewpoint, radiation and wind for the selected locality | **DATA ROUTE IDENTIFIED; DOWNLOAD/ANALYSIS NOT VERIFIED** |
| **2. What can an evaporative pad cool?** | Outdoor dry-bulb, wet-bulb and a justified pad-effectiveness assumption | **DETERMINISTIC ILLUSTRATIVE CALCULATION AVAILABLE** |
| **3. Is the air at crop height acceptable?** | Internal solar gains, cover, geometry, airflow, crop transpiration, sensor locations and a supported crop-stage criterion | **NOT ESTABLISHED**; pad outlet does not imply crop-zone temperature |
| **4. How much water does the crop require?** | Reference evapotranspiration method, crop coefficient/greenhouse adaptation, growth stage, crop area, irrigation efficiency and salinity/leaching conditions | **METHOD AVAILABLE; SITE IRRIGATION DEMAND NOT ESTABLISHED** |
| **5. Does giving an LLM this evidence improve its answers?** | Frozen scientific key, same model and settings, independent A/B outputs, claim-level scoring and reviewer adjudication | **NO ACCEPTED CONTROLLED EFFECT ESTIMATE** |

**Research scope decision:** The original 50-question, four-model agronomy benchmark is a separate research objective. The greenhouse case is a candidate focused experiment, not automatic approval to replace the full benchmark.

## 2. Current evidence and its limits

**We have:** a general evaporative-pad equation; named Qatar greenhouse studies and a Qatar crop-performance paper; greenhouse source/claim registers; an illustrative 38°C/24°C/85% case; a proposed RC04 abstention test; a deterministic ten-case software demonstration; a working-but-unmerged evidence-retrieval/RAG engineering prototype; and archived exploratory model outputs. These are useful *research assets*, not one consolidated scientific result.

**We do not yet have established:** an acquired and checked ERA5-Land sample for this point; local instrumented greenhouse time series; verified wet-bulb/psychrometric design conditions for a particular Al Shahaniya site; a measured crop-zone thermal balance; actual tomato irrigation demand; a full independent 200-response benchmark; or a qualified reviewer-approved RAG improvement result.

Use these evidence states throughout:

- **DOCUMENT IDENTITY CHECKED:** bibliographic identity/title/DOI inspected; no claim-level approval implied.
- **EXCERPT LOCATED:** the original's exact text/table and page/section identified; transcribed numbers and measurement basis still need review.
- **CALCULATED:** arithmetic performed from clearly specified inputs; does not validate those inputs.
- **OBSERVED/MODELED:** measurement versus model output explicitly identified.
- **HUMAN REVIEWED:** qualified reviewer, date and criterion recorded (not assumed).
- **BLOCKED/UNKNOWN:** critical input or authorization absent.

## 3. Scientific input map

| Domain | Collect (unit) | Scientific reason | Source / evidence gate |
|---|---|---|---|
| Outdoor heat | 2-m dry-bulb temperature (°C) | Pad inlet, outdoor thermal exposure, FAO-56 ET₀ | ERA5-Land *model estimate*; corroborate against station data |
| Outdoor moisture | 2-m dewpoint (°C), calculated RH (%) | Actual vapour pressure, VPD and psychrometric wet-bulb | ERA5-Land; same timestamp and grid cell as air temperature |
| Radiation | Incoming solar energy (J/m² per hour; convert to W/m²) | Daytime heat input, ET₀ net-radiation calculation | ERA5-Land; check accumulation convention |
| Outdoor air movement | 10-m u and v wind (m/s) | Magnitude, wind-height conversion for FAO-56; outside convection | ERA5-Land; wind at 10 m is **not** greenhouse airflow |
| Pressure | Surface pressure (Pa; convert to kPa) | Psychrometric constant, air/enthalpy calculations | ERA5-Land, pressure at grid elevation |
| Site definition | Latitude, longitude, elevation, land cover, time zone | Solar geometry, grid selection, climate applicability | Reference coordinates are not an instrumented farm survey |
| Greenhouse envelope | Footprint, volume, glazing/cover transmission, U-values | Solar gain, envelope transfer and stored heat | Design drawing/manufacturer/source; **MISSING FOR SITE** |
| Cooling system | Pad-effectiveness basis, fan flow, pad geometry, recirculation | Pad outlet and airflow/heat exchange | Manufacturer/measurements; **MISSING FOR SITE** |
| Crop | Variety, growth stage, leaf area, transpiration, zone-temperature criterion | Crop-level heat and water balance | Agronomic source or measurements; **NOT APPROVED AS UNIVERSAL** |
| Water/soil | Water quality (EC/TDS), salinity, moisture, irrigation and drainage | Irrigation and leaching constraints | Qualified samples, lab methods, date and location; **MISSING FOR SITE** |
| Economics | Energy tariff, irrigation costs, production, selling price and basis | Costs *after* a valid physical scope is defined | Paper comparison only at present; not site profitability |

**Do not invent** site, sensor, equipment, crop-growth or irrigation values to fill gaps. Published regional examples may be used as **explicitly labeled comparison scenarios**.

## 4. Copernicus Climate Data Store (CDS) collection

### Preferred: ERA5-Land **hourly time-series** — one point, CSV

**Official form:** <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land-timeseries?tab=download>

This is the simplest route for a small nontechnical research review: choose a location, date range and variables, then receive a CSV (or NetCDF). ECMWF states that a requested location is rounded to its nearest 0.1° grid point. **Save the actual returned latitude/longitude**; the coordinates you type may not be the grid-center coordinates.

| Form field | Select / enter | Why |
|---|---|---|
| Dataset | **ERA5-Land hourly time-series data** | Single-point hourly history without downloading the globe |
| Location selection | **Latitude 25.37, longitude 51.23** | Research reference point near Al Shahaniya, not a greenhouse instrument |
| Date | **2020-01-01 through 2025-12-31** | Six complete years; filter May–September after download |
| Variable | **2m temperature** | Dry-bulb air temperature |
| Variable | **2m dewpoint temperature** | Actual vapour pressure, RH/VPD, wet-bulb derivation |
| Variable | **Surface solar radiation downwards (de-accumulated)** | Solar energy received over each hour |
| Variable | **10m u-component of wind** | One part of wind speed |
| Variable | **10m v-component of wind** | Other part of wind speed |
| Variable | **Surface pressure** | Psychrometrics and FAO-56 pressure input |
| Download format | **CSV** for the initial review | Easy to inspect; preserve the original downloaded file |

**Optional only when they answer a specific additional question:** surface thermal radiation downwards (nighttime longwave work), total precipitation (rain/water-balance context), soil temperature level 1 and volumetric soil water layer 1 (regional open-field comparison). These are not direct readings inside a greenhouse. Avoid snow, lakes and unrelated variables. Do not substitute ERA5-Land potential evaporation for independently calculated FAO-56 ET₀: they are not necessarily the same definition or method.

**Why full years in this route?** The time-series form uses a continuous start/end date rather than the seasonal month/day/time grid selector. Six complete years at one hourly point are a manageable small research dataset; **filter May–September for the cooling-season analysis**, while retaining the full-year raw original for context.

### Alternative: standard ERA5-Land **hourly gridded** form — seasonal-only

**Official form:** <https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=download>

Use this only when the time-series form is unavailable or specifically requires season-only extraction.

| Form field | Selection |
|---|---|
| Variables | Same **six** core fields above; on this form the radiation entry may appear without the words *de-accumulated* |
| Years | **2020–2025** |
| Months | **May, June, July, August, September** |
| Days | All available calendar days |
| Time | **00:00–23:00**, all hours (normally UTC) |
| Area | **Sub-region**, not whole globe |
| Suggested small inspection area | **N 25.50, S 25.20, W 51.10, E 51.40** |

**Critical correction to the pasted proposal:** A tight box of N 25.40 / S 25.34 / W 51.20 / E 51.26 does **not guarantee** the grid center that will be returned. The wider box is intentionally for **inspect-and-select**, not to average all cells. Inspect output coordinate arrays, identify the nearest *land* grid point by distance, and retain the coordinates used. If the grid is influenced by local land–sea representation, compare neighboring land cells as a sensitivity check; do not assert that coastal humidity has necessarily corrupted the result.

### Both routes — acquisition rules

- Keep **original units and timestamps** in the raw file and record the CDS product, download date, data version, selected variables and licence/attribution.
- **UTC ≠ Qatar local clock:** Qatar is UTC+03:00. A 12:00 UTC observation represents 15:00 Qatar. Group daily ET₀ by the desired 24-hour day *consistently*.
- **Solar radiation differs by dataset view:** the point time-series product explicitly exposes *de-accumulated* hourly radiation; the original ERA5-Land gridded product has accumulated forecast quantities. Confirm the delivery convention before converting; never divide a multi-hour accumulation by 3600 without de-accumulating first.
- **0.1° grid is regional model support**, not a greenhouse sensor. Grid resolution is about 9 km at native scale; reported point values cannot resolve indoor microclimate or site shade.
- Do **not** label the hottest ERA5-Land hour as an approved equipment design point. Evaluate joint conditions, station bias and confidence before any design recommendation.

## 5. Physical relationships and valid inferences

### A. Air humidity / pressure

For a Celsius temperature \(T\), saturation vapour pressure is approximately

\[
e^\circ(T)=0.6108\exp\!\left(\frac{17.27T}{T+237.3}\right)\quad\mathrm{kPa}.
\]

- **Actual vapour pressure** from dewpoint: \(e_a=e^\circ(T_{dew})\).
- **Instantaneous relative humidity**: \(RH\approx 100e_a/e^\circ(T_{dry})\) (%); valid as a first-pass derivation when conditions are physically consistent.
- **Vapour-pressure deficit**: \(VPD=e^\circ(T_{dry})-e_a\) (kPa).
- **Wet-bulb temperature** must be solved or approximated from **dry-bulb, moisture and pressure**, with method and uncertainty stated; it is *not* the dewpoint.

### B. Evaporative-pad boundary (illustrative only)

\[
T_{pad,out}\approx T_{dry,out}-\eta_{pad}(T_{dry,out}-T_{wet,out})
\]

With explicitly **illustrative** \(T_{dry}=38\,°C\), \(T_{wet}=24\,°C\) and \(\eta=0.85\): \(T_{pad,out}=26.1\,°C\).

**Permitted conclusion:** the simplified equation gives a *pad-outlet* estimate. **Not permitted:** guaranteeing that plant-level air is 26.1°C or below 28°C; inferring crop survival, refrigeration size or a build recommendation.

### C. Greenhouse heat and water balance — conceptual, not a completed model

- **Solar heat gain:** depends on incoming radiation, sun angle, cover transmission/absorption, shading and greenhouse geometry.
- **Envelope conduction:** depends on surface area, U-values and inside/outside temperature differences.
- **Ventilation/infiltration:** depends on *airflow through the structure* and moist-air enthalpy difference (sensible **and** latent heat); **10-m outdoor wind is not fan flow**.
- **Crop latent cooling:** water evaporated/transpired can change crop-zone heat and humidity; it is not directly specified by outdoor meteorology.
- **Storage and controls:** plants, floor, structure, humidity buildup, system operation and sensor placement matter.

The pad equation alone does **not** close this balance. A defensible greenhouse prediction needs verified local design parameters, meteorological boundary conditions, system specifications, crop conditions and independent validation.

### D. FAO-56 reference evapotranspiration (ET₀)

The **daily FAO-56 Penman–Monteith** standard uses:

\[
ET_0=\frac{0.408\,\Delta(R_n-G)+\gamma\frac{900}{T+273}u_2(e_s-e_a)}{\Delta+\gamma(1+0.34u_2)}\quad\mathrm{mm/day}.
\]

Inputs: daily **net** radiation \(R_n\), soil heat flux \(G\), mean air temperature \(T\), 2-m wind \(u_2\), saturation and actual vapour pressure \(e_s,e_a\), slope \(\Delta\) and psychrometric constant \(\gamma\). Temperature, dewpoint, pressure, wind and incoming solar are a suitable *starting set*; you must **derive net radiation correctly**, using latitude/day/altitude, shortwave radiation, albedo and longwave-radiation methods as laid out in FAO-56. A six-variable download does *not* itself contain all the finished equation terms.

The 10-m wind components yield \(u_{10}=\sqrt{u^2+v^2}\), but FAO-56 requires wind at **2 m**; use a documented wind-height adjustment rather than inserting \(u_{10}\) unchanged. ERA5 temperatures are in K (°C = K − 273.15); pressure is in Pa (kPa = Pa / 1000); time-series solar energy is in J/m² over one hour (MJ/m² = J/m² / 10⁶, average W/m² = J/m² / 3600 for a confirmed one-hour interval). Daily solar energy is the **sum of that day's hourly energy**.

**ET₀ is the outdoor standardized reference-grass demand**, not tomato water uptake or greenhouse irrigation demand. Even \(ET_c=K_c ET_0\) requires a justified coefficient, crop stage and boundary conditions. Covered greenhouses change radiation, ventilation, humidity and the crop water balance; do not transfer outdoor FAO-56 ET₀ directly into a greenhouse pump specification.

## 6. Scientific source register

| Source | What has genuinely been established | What still requires an exact-source decision |
|---|---|---|
| **[UF/IFAS AE069](https://edis.ifas.ufl.edu/publication/AE069)** | General wet-bulb/pad-efficiency explanation | Its method is transferable; *Florida measurements* are not Qatar weather |
| **[Ghani et al., DOI 10.1080/23744731.2019.1634421](https://doi.org/10.1080/23744731.2019.1634421)** | Real Al Khor greenhouse measurements and CFD; the paper states spatial-temperature effects and 20/40 ACH simulation comparisons. **Published online 2019; journal volume 26 (2020), pp. 141–160** | Exact table/figure transcription; which temperatures are measured vs CFD assumptions; applicability to a different building or Al Shahaniya |
| **[Shannak, Kafi et al., 2026 Crop Performance Index](https://doi.org/10.1016/j.nexus.2026.100787)** | Original peer-reviewed Qatar WEF/crop-systems study publicly identifiable; reported uncooled soilless tomato performs strongly in the CPI | Recheck each crop-system numeric row and its units, definitions, scenario and policy before treating register copies as adjudicated data |
| **[Mahmood et al., 2022 semi-closed greenhouse](https://doi.org/10.1080/01430750.2022.2088617)** | Relevant Qatar semi-closed greenhouse cooling/water **forecasting** study exists | The proposed 45°C/27°C wet-bulb design pair still lacks an independently extracted locator in the active register; semi-closed chiller context ≠ open fan-and-pad design |
| **KAHRAMAA LV Wiring Code (2016 cover)** | Historical electrical source is identified | Current revision and application to a particular farm must be checked by a qualified engineer; not a greenhouse approval |
| **ERA5-Land, CDS** | Authoritative publicly available reanalysis **dataset and download route** | Actual selected-point data download, QC, observed-station cross-check and local use limitations |
| **FAO-56 (1998)** | Standard *outdoor* ET₀ equation and its assumptions | Applying crop coefficients or a greenhouse-adapted method requires additional validation |
| **FAO 2013 greenhouse guide** | A relevant greenhouse publication exists | **Quarantined in the existing project evidence policy**; do not silently add to the active evidence/RAG corpus |

**Known literature correction:** the Ghani article's DOI contains 2019 and was first online in 2019, but its final journal citation is **2020, volume 26, pages 141–160**, not “2019, volume 25, pages 973–992”. The author/publisher page should govern the bibliography. Source metadata mistakes must be corrected before mentor presentation.

### Scientific claim-review sheet — duplicate for each claim

| Field | Record |
|---|---|
| Claim/question | [What exactly is being asserted?] |
| Source | [DOI/title/publisher URL] |
| Exact locator | [Page, table, figure, section, passage ID] |
| Measurement class | [FIELD MEASURED / CFD MODEL / REANALYSIS / ASSUMED / CALCULATED] |
| Original site and period | [Where/when] |
| Variables and units | [Do values and denominators match?] |
| Scientific applicability | [General physics / same system / analog / not transferable] |
| Uncertainty or conflict | [Unknowns; model-observation differences] |
| What it proves | [Narrow justified statement] |
| What it does not prove | [Forbidden extrapolation] |
| Independent review | [Reviewer/date/decision, or PENDING] |

## 7. Climate-data quality and evidence receipt

**After a real download, make one small source-to-result record before doing modeling.**

| Required check | Acceptance criterion |
|---|---|
| File origin | CDS dataset URL and retrieval date recorded; original file kept unchanged |
| Spatial identity | Requested lat/lon **and actual returned grid point** recorded; land-cell interpretation checked |
| Time identity | UTC timestamps present, continuous for the requested window, converted consistently for Qatar summaries |
| Temperature | Kelvin/Celsius conversion tested; dewpoint should normally be no greater than air temperature at the same timestamp |
| Relative humidity/VPD | RH stays physically plausible; supersaturation/missing data explicitly flagged, not silently truncated |
| Radiation | Accumulation/de-accumulation convention recorded; non-negative hourly solar after correct conversion; nighttime values inspected |
| Wind | u/v used to derive magnitude; nonnegative speeds; 10 m→2 m conversion documented for ET₀ |
| Pressure | Pa→kPa conversion checked; plausible values for local elevation |
| Missing data | Count, gaps, duplicate timestamps, time zone and leap days reported |
| Design limits | Climate percentiles and joint combinations reported as *reanalysis diagnostics*, not accepted cooling design conditions |
| External validation | Nearest appropriate Qatar Meteorology Department observations requested/compared **if available**; otherwise status remains NOT_VALIDATED |

**First scientific outputs worth presenting:** May–September daily maximum temperature distribution; the hottest coincident humidity/solar afternoons; the smallest wet-bulb depression under high-temperature conditions; time-of-day humidity and solar profiles; and *outdoor* FAO-56 ET₀ (mm/day) with transparent assumptions and quality flags. Do not silently invent results; these outputs remain **TO BE CALCULATED** until the data is acquired.

**Acquisition receipt — fill only after retrieval:**

- CDS dataset/version and licence: **PENDING**
- Request creation/completion date: **PENDING**
- Requested lat/lon: **25.37 N, 51.23 E (research point)**
- Returned grid lat/lon: **PENDING**
- Selected period/variables: **PENDING**
- Raw filename and SHA-256: **PENDING**
- Row/hour count and missing values: **PENDING**
- QA owner and evidence link: **PENDING**
- Station comparison: **NOT PERFORMED**

## 8. What the existing ten cases actually demonstrate

| Case | Meaningful output | Scientific status |
|---|---|---|
| D01 | **26.1°C** simplified evaporative-pad outlet for deliberately illustrative inputs | A valid conditional equation calculation, **not** canopy/field evidence |
| D02–D03 | Retain Al Khor source and distinguish outdoor CFD boundary from pad boundary | Paper-context checks; not transferred to Al Shahaniya |
| D04–D05 | Compare reported **20/40 ACH** study simulations; retain 10°C/5.5°C values as **source-transcribed candidates** | Check exact figure and conditions before scientific review |
| D06–D08 | Compare three published Qatar tomato system rows with reported yields, costs, power and water | Values await exact source-row/denominator review; not site economics |
| D09 | Historical electrical power-factor excerpt with current-edition warning | Regulatory scope not established for a new installation |
| D10 | Refuse an unsupported Al Shahaniya numerical design parameter | Correct *demonstrated refusal rule*, not proof every LLM will refuse |

**The runner is a deterministic data/consistency demonstration.** It does not query a language model, run a heat-balance model, retrieve live CDS data, or establish an independent scientific finding. The stronger RAG prototype is a separate **unmerged** research asset and its current source allowlist must be reconciled with quarantined records before evaluation.

## 9. The experiment that would answer the research question

**Candidate scientific test:** “Given outdoor dry-bulb, wet-bulb, pad efficiency and an incomplete Qatar greenhouse description, can the AI distinguish **cooling-pad outlet air** from **temperature at crop height**, calculate only the first, and state what is missing for the second?”

1. Mentor/reviewer confirms the precise research question and greenhouse/crop scope.
2. Independent expert checks the exact source passage, assumptions, correct calculation, applicable crop limits and forbidden over-inferences.
3. Freeze one input question and the scientific scoring key; record hashes and permitted source packet.
4. **A:** same model/version/settings, no evidence packet. **B:** identical setup, fixed verified packet. Run separately and save raw unedited responses. Evaluate whether a *retrieval system* helps only after fixed-context improvement is measured.
5. Score correctness, justified refusal, units, scientific scope, false certainty and source support. Record human disagreements and adjudication.
6. Report result as **improved / no measurable difference / inconclusive / blocked**, with actual run receipts. If a comparison arm was **skipped**, the effect is **NOT TESTED**, not “no improvement”.

**Not yet demonstrated:** A validated A/B result, RAG advantage, approved greenhouse feasibility, field prediction accuracy or model-training benefit. The original 50×4 benchmark remains a separate scope decision.

## 10. Mentor review brief

**Single-page narrative:** “We separated a research question from its software infrastructure. The current demonstration can perform an illustrative physics calculation and withhold unsupported conclusions. We have located published Qatar greenhouse studies and the ERA5-Land climate route. We now need approval of one scientific reference key and agreement on whether this focused greenhouse experiment is an acceptable part of the original LLM benchmark.”

**Present in this sequence (5–8 minutes):**

1. **Problem:** unsupported greenhouse answers are easy to produce and hard to audit.
2. **Known evidence:** verified publication identities, working conditional physics, and identified data requirements.
3. **Visible example:** 38 / 24 / 0.85 → 26.1°C **pad outlet**, *crop zone unknown*; source-scoped published analogues, and refusal on missing data.
4. **Scientific boundary:** climate reanalysis is not an indoor sensor; 10 PASS lines do not measure LLM answer accuracy.
5. **Decision requested:** confirm reference case and crop, approve source/claim reviewer, and choose whether the next deliverable is one controlled greenhouse A/B comparison or a pilot of the wider 50-question benchmark.

**Three decisions to record, with reviewer/date:**

| Decision | Alternatives | Record |
|---|---|---|
| Approved research scope | Greenhouse RC04 pilot / wider 50×4 benchmark / other | **PENDING** |
| Approved scientific key | Named passages, units, correct/forbidden claims, reviewer | **PENDING** |
| Data collection authorization | ERA5-Land proxy only / station records / site access / approved alternative | **PENDING** |

## 11. Immediate scientific work and closure

| Order | Minimal action | End state |
|---|---|---|
| **P0** | Obtain mentor decision on scope and reviewer | Dated response/meeting record; if no decision, mark **WAITING_EXTERNAL** |
| **P0** | Reproduce the canonical demo at a pinned commit | Runner + single evidence YAML + actual output/log + failed-input check |
| **P0** | Confirm original Ghani/Shannak numeric passages and correct citation | Reviewer-ready source-to-claim table; conflicts explicitly unresolved where necessary |
| **P1** | Download **six core ERA5-Land time-series fields** for the research point | Original CSV + grid-center metadata + data QC receipt |
| **P1** | Produce one outdoor climate profile and one *outdoor reference* ET₀ case | Input, method, units, result and limitations — not greenhouse ETc |
| **P1** | Freeze RC04 key and execute same-model A/B if approved | Raw paired outputs and reviewed scientific scores |
| **P2** | Expand full question bank / retrieval / soil model | Only after specific authorization and required data |

**Stop condition:** No further reorganizing or duplicate scientific reports unless a specific reviewer requests them. Each step must end in **an evidence receipt, a reviewer decision, a falsified assumption, or an explicit blocked state**.

## 12. Primary references and reproduction links

**Climate and methods**

- Copernicus CDS — [ERA5-Land hourly time-series product](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land-timeseries?tab=download) and [classic hourly gridded product](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land?tab=download).
- ECMWF — [ERA5-Land point product user guide](https://confluence.ecmwf.int/pages/viewpage.action?pageId=576394633) (location rounding, time frequency, CSV/NetCDF).
- FAO-56 — [Chapter 2: Penman–Monteith](https://www.fao.org/4/X0490E/x0490e06.htm), [Chapter 4: computing ET₀](https://www.fao.org/4/x0490e/x0490e08.htm), [Chapter 5: ET₀ vs crop ETc](https://www.fao.org/4/x0490e/x0490e0a.htm).
- UF/IFAS — [Fan and Pad Greenhouse Evaporative Cooling Systems](https://edis.ifas.ufl.edu/publication/AE069).

**Qatar greenhouse and agronomy**

- Ghani et al. — [Experimental and numerical investigation of evaporatively cooled greenhouses](https://doi.org/10.1080/23744731.2019.1634421) (online 2019; final volume 2020).
- Shannak, Kafi, Al Jaidah & Al Ansari — [The Qatari Crop Performance Index](https://doi.org/10.1016/j.nexus.2026.100787) (2026).
- Mahmood et al. — [Semi-closed greenhouse cooling-load and water-demand forecasting](https://doi.org/10.1080/01430750.2022.2088617) (2022).
- [QEERI research repository](https://github.com/leadingproblemsolver/qeeri-agricultural); [greenhouse demo draft](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/4); [RAG draft](https://github.com/leadingproblemsolver/qeeri-agricultural/pull/2).

**Document maintenance:** This is a navigational review guide. It does not certify rights to republish source papers or permission to release institutional site data. Record source verification changes and external approvals in their original, reviewable locations rather than silently upgrading claims here.
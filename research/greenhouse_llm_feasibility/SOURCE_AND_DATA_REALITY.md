# Evidence and data register — what we can actually rely on

This file documents the **uploaded candidate source package** (November 10, 2026). Its YAML labels are assertions made in that package, **not independent proof of source verification**. This is a register, NOT an active ingestion allowlist. Never promote a record to authoritative evidence by merely reading this page.

| Evidence | Uploaded status / research role | Verification needed before scientific use |
|---|---|---|
| Mahmood et al. 2022 — https://doi.org/10.1080/01430750.2022.2088617 | Uploaded `mahmood_2022_al_shahaniya.yaml` claims verified full-text extraction and 5-minute data for a semi-closed Venlo tomato greenhouse. Earlier repo evidence ledger reports abstract-only. **CONFLICT** | Open original article; verify exact full-text, study apparatus, measured versus modeled outputs, all numbers, units and location; attach page/table/figure and independent reviewer |
| Ghani et al. Qatar greenhouse thermal/CFD | Abstract only in the existing ledgers | Acquire original full study and validate measurements/model setup |
| UF/IFAS AE069 — https://edis.ifas.ufl.edu/AE069 | General wet-bulb/pad effectiveness principle; **not** Qatar weather or actual pad rating | Independently inspect equation and conditions; do not infer crop safety |
| Tsafaras et al. 2021 Riyadh | Regional comparison, not Qatar measurement | Full source and scope checks; no transfer of Saudi design values without validation |
| KAHRAMAA low-voltage code | Current applicable edition not established | Verify exact official edition and clauses with qualified electrical reviewer |
| Lahlou Qatar economics | Abstract only; no study-specific cost assumptions verified | Full paper with cost, price, period, units and scenario assumptions |
| Shannak–Kafi crop performance index | Publication identity/existence unresolved | Verify publication, DOI, methods and data before any retrieval |
| FAO 2013 | **EXCLUDED** from current active research-support scope | Keep excluded; changing the working RAG code/fixtures is a separate pending engineering task |

## Missing real datasets

| Data | Minimum fields | State |
|---|---|---|
| Soil ground truth | Lab EC, moisture definition, geolocation, depth, collection date, matching UAV/Sentinel-2 observations and independent spatial validation | NOT VERIFIED IN REPO; no soil-model training authorized |
| Qatar hourly design weather | Station/location, timestamp, dry and wet bulb or RH + pressure, solar, wind, provenance | NOT ACQUIRED for reference case |
| Greenhouse geometry/equipment | Area/height, cover/transmission, airflow, pad characteristics and validated effectiveness | NOT ACQUIRED |
| Crop microclimate | Canopy-zone air and leaf temperature, RH, radiation, location/time and verified tomato cultivar/phenology threshold | NOT ACQUIRED |
| Water/electricity | Quality/EC, available m³/day, demand, electrical kW/kVA and current regulatory basis | NOT ACQUIRED |
| Economics | QAR capex, rates, yield, price, annual operating conditions, sources | NOT ACQUIRED |
| Independent answer key | Frozen question, verified source locator, physical reasoning, blinded human adjudication | NOT COMPLETE |
| Controlled AI run receipts | Original complete responses, identical prompts/configurations, timestamp, model versions and scoring | NOT AVAILABLE FOR REPORTED 20%→100% CLAIM |

**Data priority:** first a source-checked engineering claim and bounded fixed question; then a properly logged A/B test. Soil sample acquisition is a separate paused workstream. No new embeddings, agents or dashboards.

## Known misleading assertions that must not be published as results

- The pasted report claims `Arm A: 20%`, `Arm B: 100%`, `EVIDENCE_IMPROVES_ANSWER`. **UNSUBSTANTIATED** until both original raw provider outputs, frozen question, model/settings, locked reference labels and blind review are located.
- Do not call 28°C a universal tomato pollination failure threshold, assert 30–32°C summer wet-bulb as observed at Al-Shahaniya, or assert an exact greenhouse crop temperature without the appropriate measurements.
- The wet-bulb bound applies to *direct evaporative pad outlet air* under its assumptions; it is neither a proof of canopy conditions nor a universal lower bound on mechanically refrigerated air.
- The uploaded RAG corpus package **does not change the existing RAG allowlist**. It marks FAO quarantined on paper while existing code/test fixtures still index FAO. That inconsistency remains open.

Source materials reviewed in local conversation uploads: `SCIENTIFIC_REFERENCE_CASE_V1.md`, `REQUIRED_DATASET_REGISTER.csv`, `ground_truth_matrix.csv`, `claim_registry.csv`, UF/IFAS and Mahmood YAML files, and `qeeri_rag_corpus_package.zip`. Uploaded source-label claims were not silently adopted. Unrelated SCSC student-research ethics documents are intentionally excluded from this QEERI repository.

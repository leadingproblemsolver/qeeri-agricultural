# 2026-11-11: RC04 evidence integrity decision

**Decision: DO NOT USE THE PROPOSED AL-SHAHANIYA PACKET AS FIELD TELEMETRY.** The submitted packet was generated in an AI conversation; no raw measured observations, calibration records, source-file hashes, custodian authorization, measurement protocol, or matched site records were supplied. This document is not an allegation about the institution or real facilities; it assesses the evidence supplied for this experiment.

## What can be independently verified
- UF/IFAS AE069/CIR1135, *Fan and Pad Greenhouse Evaporative Cooling Systems*: https://ask.ifas.ufl.edu/publication/AE069
- Official 2019 citation lists **J. A. Watson, C. Gómez, R. A. Bucklin, J. D. Leary, D. B. McConnell**. The official about page displays the same five contributors in a different listing order. Do not invent author metadata.
- **Systems Efficiency** defines pad-exit air temperature as outside dry-bulb minus effectiveness multiplied by wet-bulb depression.
- **Temperature Gradient** says air typically warms as it crosses an open fan-and-pad greenhouse. Its approximate 1°F per 10 feet is a **contextual example**, not a calibrated Al-Shahaniya gradient or automatic design coefficient.
- With **synthetic** 38.0°C dry bulb, 24.0°C wet bulb, efficiency 0.85, computed pad outlet = **26.1°C**. This cannot establish crop-zone temperature.

## Rejected evidence promotions
| Supplied assertion | State | Why |
|---|---|---|
| `telemetry_verification_status=VERIFIED_FIELD_READINGS` covering May–Oct 2026 | **UNVERIFIED** | No raw sensor time series, instrument calibration, methods, or source receipts |
| 5,000 m² glass greenhouse, 350,000 m³/h airflow, 40% recirculation, sensor positions, 42°C/28.5°C weather | **USER-SUPPLIED HYPOTHETICAL/UNVERIFIED DESIGN** | Not linked to verified measurements or engineering drawings |
| `data_custodian=QEERI / Agricultural Systems Research Division` | **UNCONFIRMED ATTRIBUTION** | No institutional acknowledgment; do not imply approval |
| `source_packet_sha256=e3b0c442...` | **INVALID RECEIPT** | That is SHA-256 of zero-length bytes, not a nonempty evidence packet |
| `human_evaluator=Taha Aslam; scores=1_1_1_1_1` | **SELF-REPORTED REVIEW OF TEXT** | Not a blinded independent evaluator; not auditable A/B scoring |
| `gemini-2.5-pro-202611`, `temp_0.0_seed_42`, run filenames | **UNVERIFIED EXECUTION METADATA** | Paths/labels do not prove provider runs or controllable seeds; full raw payloads not provided |
| `PASSED_HARD_GATE` | **REJECTED** | Scientific reference review, independent scoring, run isolation and data provenance not established |
| `PUBLIC DOMAIN` for IFAS publication | **NOT ESTABLISHED** | Free online access does not automatically grant public-domain status or unrestricted republication |

## Distinguish two studies
**RC04 synthetic reasoning test:** valid to use assumed 38/24/0.85 inputs to test whether the LLM avoids equating pad-exit with canopy temperature. Needs a confirmed, rights-respecting fixed source packet and actual isolated model outputs.

**Qatar field validation:** **DATA_BLOCKED**. Requires real site identity/permissions, raw timestamped station and internal climate readings with units/calibration, exact cooling-system process diagram, site-linked geometry, and reviewer approval. Never treat generated JSON as an observed dataset.

## Correction to the proposed field protocol
Calling a protocol “PRE-REGISTERED / LOCKED” after inputs and score descriptions have been exposed does not make it prospective pre-registration. Record it as **DRAFT_POST_EXPOSURE**, with the original authoring date and version. The rule that canopy temperature must always rise is not universal for every hybrid greenhouse subsystem; measured heat/mass balances govern outcomes. A fixed 1.5 m sensor height and arbitrary 3D grid must not be mistaken for an approved observation design.

## Smallest next valid external event
Obtain one **independently checkable original field dataset** from an authorized owner, with a sample observation, sensor identity, timestamps, units, methods, calibration, access rights and reproducible hash. Until then, **complete the synthetic RC04 controlled A/B experiment** with no field claims.

Related: [RC04 frozen question](RC04_CROP_ZONE_ABSTENTION.md), [RC04 physical foundations](RC04_FOUNDATIONS_AND_SCORING.md), [weather acquisition choices](WEATHER_INPUT_ACQUISITION.md).

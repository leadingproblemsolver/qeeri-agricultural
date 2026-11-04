# Qatar cucumber 2024 — first public-source constraint receipt

**Evidence state:** national aggregates, not a sampled field. Scientific, financial, and environmental validation remain incomplete.

## Reproduce

From `research_mvp/`:

```bash
python -m unittest -q test_qeeri test_public_case
python qatar_public_case.py
python smoke_protocol.py
```

The case is derived from existing `data/cucumber_scopes.csv` and `data/wits_imports.csv`. No climate or soil values are invented. The generated case report is stdout JSON; use `python qatar_public_case.py > qatar_case_local.json` to save privately, and **do not upload field-level observations or local receipts**.

## Verified descriptive facts

- National greenhouse cucumber output (2024): **17,512.73 tonnes** across **251.8 ha**, calculated yield **69.550159 tonnes/ha**; National Planning Council open data, dataset `cropped-area-and-production-of-crops-in-greenhouses`.
- Qatar's reported 2024 world imports of HS 070700 *cucumbers and gherkins, fresh or chilled*: **USD 3,638,150** and **10,417,700 kg**, calculated unit value **USD 0.349228/kg**. WITS H0 070700 published aggregate, not comparable delivered-import cost.
- WITS 2023 world import quantity: **2,790,740 kg**, so 2024 quantity / 2023 quantity is **3.7330**. Both official WITS totals were checked on 2026-11-04. Large change flagged `REVIEW` for trade-statistical interpretation; **do not alter source values**.

Published public sources:
- https://www.data.gov.qa/explore/dataset/cropped-area-and-production-of-crops-in-greenhouses/
- https://wits.worldbank.org/trade/comtrade/en/country/QAT/year/2024/tradeflow/Imports/partner/ALL/product/070700
- https://wits.worldbank.org/trade/comtrade/en/country/QAT/year/2023/tradeflow/Imports/partner/ALL/product/070700

## Deterministic decisions

- `WARN`: descriptive national production / trade.
- `REVIEW`: large reported 2024 import-weight jump; no unsupported 'mistake' claim.
- `BLOCK`: any grow-versus-import cost claim: missing matched marketable kg, complete farm costs, delivered import cost and losses.
- `BLOCK`: liters/m3 per marketable kg: no metered irrigation and marketable harvest from the same field/cycle.
- `BLOCK`: soil EC: no sampled, georeferenced lab EC, depth and timestamp.
- `NOT_ACQUIRED`: location-matched NASA POWER climate. Qatar-wide annual production is not linked to any single physical farm, so a geographic climate point would be an unrelated scenario. NASA POWER daily source documented at https://power.larc.nasa.gov/docs/services/api/temporal/daily/ .

## Minimum next field data (not national aggregates)

1. Field ID/crop/variety/cultivation type; source-grounded WGS84 point or boundary; field area and crop-cycle dates.
2. Timestamped station weather (or permission to substitute NASA POWER as **modeled spatial proxy**, not measured on-farm data).
3. Metered irrigation m³ and interval; water source, water EC where measured.
4. Soil sample measured EC, method, sample depth, geolocation and timestamp.
5. Same-cycle marketable kg and rejected kg; harvest dates.
6. Metered kWh, QAR costs by category, period, subsidy boundary; if possible comparable import delivered-price invoice, grade and loss fraction.

A partial matched sample is sufficient; unavailable inputs keep the corresponding decision `BLOCK`.

## Test boundary

72/72 automated tests on Python 3.13 (52 existing + 20 case-specific), MCP 5-request smoke protocol PASS. These establish deterministic local behavior—not farm-level agronomic accuracy, a scientific claim, or quality of any future data supplied by a mentor.
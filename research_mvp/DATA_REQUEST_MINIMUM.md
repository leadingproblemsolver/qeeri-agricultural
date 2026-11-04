# Missing observations — next empirical environmental / financial evaluation

This is a prepared request, not confirmation that data are available or usable. Any existing data provided must have its source, measurement method, date/time and permissible research use recorded. **No public national aggregate requires another request.**

## Minimal matching unit

One **field + one crop cycle + one observation period** with a unique field ID, georeferenced crop context, measurement timestamps and any corresponding farm costs. Partial records are welcome; the gate should disclose exactly which calculations remain ineligible.

| Order | Needed | Minimum fields and unit | Which computation needs it |
|---|---|---|---|
| 1 | Field/crop | field_id, GPS boundary or coordinates (WGS84), area ha, crop/variety, greenhouse/open-field, date range | Correct location/scope and temporal join |
| 2 | Climate | air temp °C, relative humidity %, solar input W/m² or equivalent, wind m/s, UTC timestamps; note missing sensors | ET0/thermal context eligibility |
| 3 | Water | metered irrigation m³ with period, source, water EC dS/m if measured; drainage if available | water consumption per marketable kg; cannot infer from satellite |
| 4 | Soil | measured EC dS/m, measured moisture and method where available, depth cm, timestamp, sample coordinates, lab ID | soil validation ground truth; satellite covariate alone not label |
| 5 | Production | crop cycle, harvested and marketable kg, reject kg, area, harvest dates | normalized yield, crop productivity |
| 6 | Finance/energy | electricity kWh and tariff QAR/kWh; water cost, operating cost categories, applicable subsidies, period, pricing boundary; marketable kg | cost per kg and downside; trade CIF aggregates not substitute |
| 7 | Drone (optional until adapter) | make/model, payload/camera, flight-controller API, coordinate/time exports, calibration/permissions | sensor-independent parser; no flight or actuator commands |

**Non-requests:** the national open-field/greenhouse statistics, WITS 2023/2024 HS070700 imports, full research archive, drone flights before payload known, and entire farm database. Only a small *existing* matching sample is requested.

**Blocking boundaries:** field EC training needs measured georeferenced EC labels; financial comparison needs matching farm costs and delivered import costs; any missing requirement returns BLOCK. Original 11 question-bank scientific flags remain REVIEW.

# Weather input acquisition — exact minimum, not a new platform

## Priority now
**None required to run synthetic RC04.** Do not delay the controlled abstention test to collect weather. Weather is required only to claim local/seasonal applicability later.

## 1. Qatar Meteorology Department (QMD) — measured observation
Request an authorized historical hourly export for Al Shahaniyah station (or nearest station with documented coordinates), ideally representative hot-season hours; request: station ID, latitude/longitude, elevation, time zone, observation timestamp, measured 2-m dry-bulb C, relative humidity %, station/actual pressure hPa if available, quality flags, missingness and sensor metadata. Ask whether wet-bulb is directly measured; otherwise derive it from T/RH/pressure with a named psychrometric method and uncertainty. Solar radiation is needed for a later crop-zone thermal model if available. Preserve raw file, license, retrieval date and station distance to actual greenhouse.
Official live portal: https://qweather.gov.qa/CAA/EWSData.aspx ; station inventory: https://www.data.gov.qa/explore/dataset/fixed-meteorological-and-marine-monitoring-stations-and-seismic-stations/
**Status:** URLs identified; no hourly historical dataset or permissions verified here. Heat index, visibility, wind direction, rainfall are not needed for the pad outlet equation. Wind and solar data become relevant for subsequent full thermal modeling.

## 2. ERA5 / ERA5-Land — modeled proxy, not measured site truth
If QMD historical data is unavailable, acquire the **smallest** hourly subset for the declared location and hot-season time window: 2m air temperature, 2m dewpoint and surface pressure (or a justified pressure source) to compute RH/wet-bulb; add surface solar radiation downwards only for later greenhouse thermal modeling. Preserve exact CDS dataset/version, grid coordinates, UTC timestamps, conversion units, API request, download hash and known grid-to-site mismatch. Do not treat ERA5-Land soil moisture as a laboratory EC/moisture label.
ERA5: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels
ERA5-Land: https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land
**Status:** dataset candidates only; no downloaded records verified.

## 3. Synthetic RC01 / RC04 — already sufficient for first gate
Dry bulb 38.0 C; wet bulb 24.0 C; pad effectiveness 0.85; threshold 28.0 C. Formula T_out=T_db-eta*(T_db-T_wb) => 26.1 C. These are invented **test inputs**, not fabricated observations. Do not add QMD, ERA5, Mahmood or Ghani numbers to this calculation.

## Order
Lock RC04 answer key -> verify one relevant source passage -> A/B matched outputs -> score -> ONLY THEN select one observed or reanalysis hot-season weather record for external validity.

"""Bounded public 2024 Qatar greenhouse cucumber + trade case. No farm-level joins.

Only original published aggregate inputs are used. No measured field/soil/water or
financial comparison is inferred. Stdlib-only; does not transmit local JSON.
"""
import hashlib
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from qeeri_brain import read_rows, _missing_required_inputs

SOURCE_GREENHOUSE = 'https://www.data.gov.qa/explore/dataset/cropped-area-and-production-of-crops-in-greenhouses/'
SOURCE_TRADE_2024 = 'https://wits.worldbank.org/trade/comtrade/en/country/QAT/year/2024/tradeflow/Imports/partner/ALL/product/070700'
SOURCE_TRADE_2023 = 'https://wits.worldbank.org/trade/comtrade/en/country/QAT/year/2023/tradeflow/Imports/partner/ALL/product/070700'


def _positive(raw, label):
    try:
        result = Decimal(str(raw))
    except (InvalidOperation, TypeError):
        raise ValueError(f'invalid {label}') from None
    if not result.is_finite() or result <= 0:
        raise ValueError(f'invalid {label}: positive finite measurement required')
    return result


def _unique(rows, label):
    if len(rows) != 1:
        raise ValueError(f'{label}: expected exactly one source record; found {len(rows)}')
    return rows[0]


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build_public_case(production_rows=None, trade_rows=None):
    """Return source-bound national-aggregate descriptive evidence, never ROI estimates."""
    production_rows = read_rows('cucumber_scopes.csv') if production_rows is None else production_rows
    trade_rows = read_rows('wits_imports.csv') if trade_rows is None else trade_rows
    p = _unique([r for r in production_rows if r.get('year')=='2024' and r.get('crop')=='Cucumber' and r.get('source_scope')=='GREENHOUSE'],'2024 greenhouse cucumbers')
    t = _unique([r for r in trade_rows if r.get('year')=='2024' and r.get('hs_code')=='070700' and r.get('partner')=='World' and r.get('trade_flow')=='Import'],'2024 Qatar HS070700 world imports')
    prior = _unique([r for r in trade_rows if r.get('year')=='2023' and r.get('hs_code')=='070700' and r.get('partner')=='World' and r.get('trade_flow')=='Import'],'2023 Qatar HS070700 world imports')
    if t.get('source_url') != SOURCE_TRADE_2024 or prior.get('source_url') != SOURCE_TRADE_2023:
        raise ValueError('unexpected WITS source URL; source alignment requires manual verification')
    if p.get('source_file') != 'cropped-area-and-production-of-crops-in-greenhouses.json':
        raise ValueError('unexpected greenhouse dataset source')
    if t.get('quantity_unit')!='Kg' or t.get('reporting_country')!='Qatar' or t.get('hs_revision')!='HS 1988/92 (H0)':
        raise ValueError('unexpected trade units, reporter or nomenclature')
    tonnes = _positive(p['production_tonnes'],'greenhouse tonnes')
    area = _positive(p['area_hectares'],'greenhouse hectares')
    value = _positive(t['trade_value_usd'],'trade value USD')
    weight = _positive(t['net_weight_kg'],'trade net weight kg')
    prior_weight = _positive(prior['net_weight_kg'],'2023 trade weight kg')
    unit = value / weight
    ratio = weight / prior_weight
    return {
        'case_id':'QAT-CUCUMBER-2024-PUBLIC-NATIONAL',
        'observational_unit':'Qatar national annual statistics; NOT a farm or crop-cycle record',
        'country':'Qatar','year':2024,
        'production':{
            'crop':'Cucumber', 'cultivation':'GREENHOUSE', 'scope':'national crop aggregate',
            'tonnes':float(tonnes), 'area_ha':float(area),
            'tonnes_per_ha':round(float(tonnes/area),6),
            'source_url':SOURCE_GREENHOUSE,
            'evidence_type':'PUBLISHED_NATIONAL_PRODUCTION_AGGREGATE'},
        'trade':{
            'product':'Cucumbers and gherkins, fresh or chilled',
            'hs_code':'070700','hs_revision':'H0','scope':'Qatar imports, World partners, annual',
            'value_usd':int(value),'net_weight_kg':int(weight),
            'cif_unit_value_usd_per_kg':round(float(unit),6),
            'year_over_year_net_weight_ratio':round(float(ratio),4),
            'source_url':SOURCE_TRADE_2024,
            'evidence_type':'PUBLISHED_TRADE_AGGREGATE_NOT_DELIVERED_PRICE',
            'qa_flags':['REVIEW_LARGE_WEIGHT_CHANGE_2023_TO_2024'] if ratio > 2 else []},
        'comparability':{
            'same_year':True, 'same_crop_exactly':False,
            'national_aggregate_not_farm_sample':True,
            'financial_comparison_eligible':False,
            'reasons':['Cucumber-only production versus HS070700 cucumbers-and-gherkins trade',
                       'CIF aggregate unit value is not delivered import cost',
                       'No observed matched farm variable/fixed costs, marketable kilograms, irrigation or electricity',
                       'National production and trade quantities are different populations; cannot infer self-sufficiency or cost savings']},
        'decisions':{
            'descriptive_import':{'decision':'WARN','reason':'PUBLIC_AGGREGATE_DESCRIPTIVE_ONLY'},
            'relative_cost':{'decision':'BLOCK','reason':'MISSING_REQUIRED_INPUTS',
                'missing':_missing_required_inputs('Is it cheaper to grow cucumbers than import them?')},
            'water_efficiency':{'decision':'BLOCK','reason':'MISSING_REQUIRED_INPUTS',
                'missing':_missing_required_inputs('How many litres of irrigation per marketable kg?')},
            'soil_ec':{'decision':'BLOCK','reason':'MISSING_REQUIRED_INPUTS',
                'missing':_missing_required_inputs('Measured soil EC salinity for greenhouse cucumbers')},
            'weight_anomaly':{'decision':'REVIEW','reason':'SOURCE_REPORTED_YEAR_OVER_YEAR_WEIGHT_CHANGE'} if ratio>2 else {'decision':'WARN','reason':'NO_LARGE_WEIGHT_CHANGE_FLAG'}},
        'public_data_fingerprint':{
            'cucumber_scopes_csv_sha256':_sha(Path(__file__).parent/'data/cucumber_scopes.csv'),
            'wits_imports_csv_sha256':_sha(Path(__file__).parent/'data/wits_imports.csv')},
        'climate':{'status':'NOT_ACQUIRED','reason':'No source-bound farm location; national annual production cannot be geolocated to a single field',
                   'next_public_source':'https://power.larc.nasa.gov/docs/services/api/temporal/daily/'},
        'missing_for_empirical_evaluation':{
            'field':['field_id','latitude_longitude_or_boundary','crop_cycle_start_end','planting_and_harvest_dates'],
            'climate':['location-matched weather data or sourced climate grid coordinates and matching dates'],
            'water':['metered_irrigation_m3','observation_period','water_source','water_EC_if_measured'],
            'soil':['sampled_soil_EC_ds_m','sample_depth_cm','sample_date','sample_location'],
            'production':['marketable_kg_same_crop_cycle','rejected_kg_if_available'],
            'energy_cost':['metered_kwh','water_cost','energy_cost','local_farm_fixed_variable_cost','delivered_import_price_and_boundaries']}
    }


def main():
    print(json.dumps(build_public_case(),indent=2,sort_keys=True))

if __name__ == '__main__':
    main()

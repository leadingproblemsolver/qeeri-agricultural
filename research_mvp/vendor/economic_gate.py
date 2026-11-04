import csv, json, argparse
from pathlib import Path

REQUIRED = ['case_id','crop','country','period','marketable_kg','local_variable_cost','local_fixed_allocated','water_cost','energy_cost','distribution_cost','subsidy_received','import_landed_cost_per_kg','import_loss_fraction','local_downside_kg','water_m3','evidence_type']
NUMERIC = REQUIRED[4:14] + ['water_m3']

def evaluate(row):
    missing = [k for k in REQUIRED if row.get(k) in (None,'')]
    if missing: return {'case_id':row.get('case_id'),'status':'BLOCKED_MISSING_DATA','missing':missing}
    try: d={k:float(row[k]) for k in NUMERIC}
    except (ValueError,TypeError): return {'case_id':row.get('case_id'),'status':'BLOCKED_INVALID_NUMBER'}
    if (any(d[k]<0 for k in NUMERIC) or d['marketable_kg']<=0 or d['local_downside_kg']<=0 or d['import_loss_fraction']>=1 or d['import_landed_cost_per_kg']<=0 or d['water_m3']<=0):
        return {'case_id':row['case_id'],'status':'BLOCKED_INVALID_INPUT'}
    if d['local_downside_kg']>d['marketable_kg']:
        return {'case_id':row['case_id'],'status':'BLOCKED_DOWNSIDE_GT_BASE'}
    cost=sum(d[k] for k in ['local_variable_cost','local_fixed_allocated','water_cost','energy_cost','distribution_cost'])
    imp=d['import_landed_cost_per_kg']/(1-d['import_loss_fraction'])
    local=cost/d['marketable_kg']
    downside=cost/d['local_downside_kg']
    net=(cost-d['subsidy_received'])/d['marketable_kg']
    state='SYNTHETIC_ONLY' if row['evidence_type'].lower()!='observed_verified' else 'UNVERIFIED_COST_COMPARISON'
    return {'case_id':row['case_id'],'status':state,'currency':row.get('currency','QAR'),
      'local_unsubsidized_cost_per_kg':round(local,5),'local_subsidized_cost_per_kg':round(net,5),
      'local_downside_cost_per_kg':round(downside,5),'import_effective_cost_per_kg':round(imp,5),
      'local_less_expensive_base':local<imp,'local_less_expensive_downside':downside<imp,
      'subsidy_qr_per_kg':round(d['subsidy_received']/d['marketable_kg'],5),
      'water_m3_per_market_kg':round(d['water_m3']/d['marketable_kg'],5),
      'disclaimer':'Illustrative accounting comparison only; input provenance, tariff structure, prices, period, system boundaries and logistics reliability require review.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--out',required=True);a=p.parse_args()
    with open(a.csv,newline='') as f: data=list(csv.DictReader(f))
    results=[evaluate(row) for row in data]
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps({'results':results,'summary':{'cases':len(results),'observed_verified':sum(r['status']=='UNVERIFIED_COST_COMPARISON' for r in results),'blocked':sum(r['status'].startswith('BLOCKED') for r in results)}},indent=2))
    print(json.dumps({'cases':len(results),'blocked':sum(r['status'].startswith('BLOCKED') for r in results),'output':a.out}))
if __name__=='__main__':main()

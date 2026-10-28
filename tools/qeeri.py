#!/usr/bin/env python3
"""QEERI local evidence collector; never calls a model or creates artificial results."""
import argparse,csv,datetime,hashlib,pathlib,sys,os,json
R=pathlib.Path(__file__).resolve().parents[1]
P=R/'03_runs/prompts_applied_200.csv';L=R/'03_runs/run_log_200.csv';Q=R/'03_runs/execution_queue_200.csv'
SMOKE={f'R{x:03d}' for x in [1,2,3,4,169,170,171,172]}
def get(p):
 with p.open(encoding='utf8',newline='') as f:
  r=csv.DictReader(f);return list(r),r.fieldnames
def setcsv(p,rows,cols):
 tmp=p.with_suffix(p.suffix+'.tmp')
 with tmp.open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,cols);w.writeheader();w.writerows(rows)
 os.replace(tmp,p)
def sha(b):return hashlib.sha256(b).hexdigest()
def utc(v):
 d=datetime.datetime.fromisoformat(v.replace('Z','+00:00'))
 if d.tzinfo is None or d.utcoffset().total_seconds()!=0:raise ValueError('UTC timestamp required: '+v)
 return d
def verify():
 p,_=get(P);r,_=get(L);q,_=get(Q);err=[]
 if [len(x) for x in (p,r,q)]!=[200,200,200]:err.append('Expected 200 rows in all three tables')
 if any(len({x['run_id'] for x in items})!=200 for items in (p,r,q)):err.append('Duplicate run IDs')
 rid={x['run_id']:x for x in r}
 for x in p:
  y=rid.get(x['run_id'],{})
  if sha(x['full_prompt'].encode())!=x['prompt_sha256'] or any(y.get(k)!=x[k] for k in ('question_id','model','prompt_sha256')):err.append('Prompt/run data conflict '+x['run_id'])
 for y in r:
  if y['response_status'] not in ('pending','captured','refused','deviation','error'):err.append('Invalid status '+y['run_id'])
  if y['response_status'] in ('captured','refused'):
   f=R/y['response_file'] if y['response_file'] else None
   if not f or not f.is_file() or sha(f.read_bytes())!=y['response_sha256']:err.append('Missing/modified raw response '+y['run_id'])
   if not y['model_version_displayed'] or not y['reasoning_mode'] or not y['utc_start'] or not y['utc_end']:err.append('Missing metadata '+y['run_id'])
   else:
    try:
     if utc(y['utc_start'])>utc(y['utc_end']):err.append('Time inversion '+y['run_id'])
    except ValueError as e:err.append(str(e))
   if any(y[k]!='TRUE' for k in ('tools_disabled','browsing_disabled','incognito_verified')):err.append('Missing isolation evidence '+y['run_id'])
 return err,r,p,q
def status():
 errs,r,p,q=verify(); counts={s:sum(x['response_status']==s for x in r) for s in ('pending','captured','refused','deviation','error')}
 print('QEERI: 50 questions x 4 models |',len(p),'prompts | observed',counts,'| smoke',sum(x['run_id'] in SMOKE and x['response_status'] in ('captured','refused') for x in r),'/8')
 print('Integrity:', 'PASS' if not errs else 'FAIL '+repr(errs[:15]));return 0 if not errs else 1
def next_run():
 errs,r,p,q=verify()
 if errs:raise ValueError('Integrity failed: '+repr(errs[:5]))
 seen={x['run_id']:x for x in r};pr={x['run_id']:x for x in p}
 for item in sorted(q,key=lambda x:int(x['sequence'])):
  if seen[item['run_id']]['response_status']=='pending':
   x=pr[item['run_id']];print('NEXT REAL RUN:',item['run_id'],item['phase'],item['model'],item['question_id'])
   print('Prompt SHA256:',x['prompt_sha256'])
   print('Prompt file:',f"03_runs/smoke_prompts/{item['run_id']}_{item['model']}.txt" if item['phase']=='SMOKE' else '03_runs/prompts_applied_200.csv: full_prompt for '+item['run_id'])
   print('No model API called, no raw response fabricated.');return 0
 print('All rows have a terminal state. Run audit --all.');return 0
def record(a):
 errs,r,p,q=verify()
 if errs:raise ValueError('Unclean log: '+repr(errs[:5]))
 by={x['run_id']:x for x in r};row=by.get(a.run)
 if not row or row['response_status']!='pending':raise ValueError('Run missing, or has already been recorded')
 if not all((a.tools_off,a.browsing_off,a.incognito)):raise ValueError('Browser tools/browsing OFF and incognito must be observed')
 if a.personalization_state not in ('OFF','NOT_APPLICABLE'):raise ValueError('Personalization unverified; do not claim controlled capture')
 if not a.model_version.strip() or not a.reasoning_mode.strip():raise ValueError('Exact UI label or NOT_SHOWN required')
 if utc(a.utc_start)>utc(a.utc_end):raise ValueError('End time precedes start')
 source=pathlib.Path(a.response_file)
 if not source.is_file():raise ValueError('Source file absent')
 data=source.read_bytes()
 if len(data.strip())<3:raise ValueError('No genuine raw response')
 dest=R/'03_runs/raw_responses_RESTRICTED'/('resp_'+a.run+'.txt')
 with dest.open('xb') as f:f.write(data)
 try:
  row.update(model_version_displayed=a.model_version,reasoning_mode=a.reasoning_mode,utc_start=a.utc_start,utc_end=a.utc_end,tools_disabled='TRUE',browsing_disabled='TRUE',incognito_verified='TRUE',personalization_disabled=a.personalization_state,response_file=str(dest.relative_to(R)),response_sha256=sha(data),response_status=a.status,notes='; '.join(filter(None,[row['notes'],a.notes])))
  setcsv(L,r,list(r[0]))
 except Exception:
  dest.unlink(missing_ok=True);raise
 print('SAVED authentic observed run',a.run,'sha256',sha(data),'bytes',len(data));return 0
def audit(smoke):
 errs,r,p,q=verify();subset=[x for x in r if (not smoke or x['run_id'] in SMOKE)];missing=[x['run_id'] for x in subset if x['response_status'] not in ('captured','refused')]
 print('SMOKE' if smoke else 'FULL','audit:',len(subset)-len(missing),'/',len(subset),'real outcomes; failures',len(errs))
 if missing:print('PENDING:',','.join(missing[:80]))
 for e in errs[:15]:print('ERROR:',e)
 return 1 if missing or errs else 0

def exploratory(a):
 """Append-only separate evidence; never modifies the controlled 200-row ledger."""
 src=pathlib.Path(a.response_file)
 if not src.is_file():raise ValueError('Source file absent')
 data=src.read_bytes()
 if len(data.strip())<3:raise ValueError('Empty response')
 out=R/'03_runs/exploratory_RESTRICTED';out.mkdir(exist_ok=True)
 index=out/'index.csv'
 cols=['evidence_id','candidate_run_id','question_id','model_attribution','model_version_observed','source_filename','response_file','response_sha256','imported_utc','source_start_line','source_end_line','provenance','limitations','counts_toward_controlled']
 existing,_=get(index) if index.exists() else ([],cols)
 digest=sha(data)
 for row in existing:
  if row['response_sha256']==digest and row['candidate_run_id']==a.run:
   print('ALREADY IMPORTED',row['evidence_id'],digest);return 0
 eid='E'+str(len(existing)+1).zfill(3)
 dest=out/(eid+'_'+a.run+'.txt')
 with dest.open('xb') as f:f.write(data)
 now=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
 row=dict(evidence_id=eid,candidate_run_id=a.run,question_id=a.question_id,model_attribution=a.model_attribution,model_version_observed='NOT_VERIFIED',source_filename=src.name,response_file=str(dest.relative_to(R)),response_sha256=digest,imported_utc=now,source_start_line=a.start_line or '',source_end_line=a.end_line or '',provenance=a.provenance,limitations=a.limitations,counts_toward_controlled='NO')
 setcsv(index,existing+[row],cols)
 print('EXPLORATORY SAVED',eid,'candidate',a.run,'SHA256',digest,'NO controlled credit');return 0

def exploratory_audit():
 out=R/'03_runs/exploratory_RESTRICTED'; index=out/'index.csv'
 if not index.exists():print('Exploratory index absent');return 1
 rows,_=get(index);err=[];seen=set()
 for x in rows:
  f=R/x['response_file']; k=(x['candidate_run_id'],x['response_sha256'])
  if not f.is_file() or sha(f.read_bytes())!=x['response_sha256']:err.append('Missing or altered '+x['evidence_id'])
  if x['counts_toward_controlled']!='NO':err.append('Improper controlled claim '+x['evidence_id'])
  if k in seen:err.append('Duplicate '+x['evidence_id'])
  seen.add(k)
 ce,cl,cp,cq=verify()
 if ce:err.extend(ce)
 print('EXPLORATORY AUDIT:',len(rows),'preserved, controlled',sum(x['response_status'] in ('captured','refused') for x in cl),'/200, issues',len(err))
 for e in err:print('ERROR',e)
 return 1 if err else 0

def main():
 pa=argparse.ArgumentParser();sub=pa.add_subparsers(dest='cmd',required=True)
 sub.add_parser('status');sub.add_parser('next');sub.add_parser('audit-exploratory')
 p=sub.add_parser('exploratory-record')
 for k in ('run','question-id','model-attribution','response-file','provenance','limitations'):p.add_argument('--'+k,required=True)
 p.add_argument('--start-line',default='');p.add_argument('--end-line',default='')
 p=sub.add_parser('audit');g=p.add_mutually_exclusive_group(required=True);g.add_argument('--smoke',action='store_true');g.add_argument('--all',action='store_true')
 p=sub.add_parser('record')
 for k in ('run','response-file','model-version','reasoning-mode','utc-start','utc-end'):p.add_argument('--'+k,required=True)
 for k in ('tools-off','browsing-off','incognito'):p.add_argument('--'+k,action='store_true')
 p.add_argument('--personalization-state',required=True,choices=['OFF','NOT_APPLICABLE','UNKNOWN']);p.add_argument('--status',choices=['captured','refused'],default='captured');p.add_argument('--notes',default='')
 a=pa.parse_args()
 try:return {'status':status,'next':next_run,'audit':lambda:audit(a.smoke),'record':lambda:record(a),'exploratory-record':lambda:exploratory(a),'audit-exploratory':exploratory_audit}[a.cmd]()
 except (ValueError,KeyError,FileExistsError) as e:print('ERROR',e,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())

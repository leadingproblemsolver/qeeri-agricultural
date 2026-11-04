"""Local-only QEERI evidence retrieval + deterministic decision bridge (stdlib)."""
import csv, json, hashlib, math, re, uuid
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from vendor.economic_gate import evaluate, REQUIRED

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
RECEIPTS = ROOT / 'local_receipts.jsonl'
TOK = re.compile(r'[a-zA-Z0-9]+')

def tokens(s):
    return set(TOK.findall(str(s).lower()))

def read_rows(name):
    with (DATA / name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))

def corpus():
    items=[]
    for row in read_rows('wits_imports.csv'):
        year=row['year']; value=int(row['trade_value_usd']); kg=int(row['net_weight_kg'])
        # Never trust a derived string where original base units exist.
        unit=round(value/kg,6) if kg>0 else None
        data={'year':year,'crop':'Cucumbers and gherkins, fresh or chilled','scope':'Qatar HS 070700 CIF import aggregate','import_usd':value,'net_weight_kg':kg,'usd_per_kg':unit,'price_boundary':'CIF, not fully delivered-to-market','evidence_type':'PUBLIC_TRADE_AGGREGATE','source_url':row['source_url']}
        items.append({'id':f'WITS-QAT-070700-{year}','text':f"Qatar 070700 cucumber gherkin imports {year}: {value} USD for {kg} kg, mean CIF unit value {unit} USD/kg.", 'limitations':['CIF import unit value is not farm operating cost, retail price, or delivered import cost'], 'data':data, 'source':row['source_url'], 'kind':'TRADE'})
    for row in read_rows('cucumber_scopes.csv'):
        year=row['year']; scope=row['source_scope']; name=f'QATAR-CUCUMBER-{scope}-{year}'
        data={'year':year,'crop':row['crop'],'scope':scope,'production_tonnes':float(row['production_tonnes']),'area_hectares':float(row['area_hectares']) if row['area_hectares'] else None,'evidence_type':row['evidence_state'],'source_dataset':row['source_file'],'limitations':row['notes']}
        items.append({'id':name,'text':f"Qatar {year} cucumber {scope.lower().replace('_',' ')} production {row['production_tonnes']} tonnes; area {row['area_hectares'] or 'unknown'} hectares.",'limitations':['Public production aggregate, not a farm cost, water-use, or soil EC measurement'], 'data':data,'source':row['source_file'],'kind':'PRODUCTION'})
    return items

def scientific_review_records():
    """Research QA register: evidence leads only, NEVER validated scientific passages."""
    return json.loads((DATA / 'scientific_review_11.json').read_text(encoding='utf-8'))


def scientific_source_passages():
    """Curated short, independently located excerpts; REVIEW, not scientific adjudication."""
    rows=json.loads((DATA/'source_passages.json').read_text(encoding='utf-8'))
    ids={r['question_id'] for r in scientific_review_records()}
    for r in rows:
        if r.get('status')!='REVIEW' or r.get('evidence_type')!='VERIFIED_WEB_EXCERPT':
            raise ValueError('Invalid science passage status')
        if not r.get('source_url','').startswith('https://') or not r.get('source_locator'):
            raise ValueError('Missing scientific source provenance')
        if not set(r['question_ids']) <= ids:
            raise ValueError('Unknown scientific review question ID')
        if hashlib.sha256(r['excerpt'].encode()).hexdigest()!=r['excerpt_sha256']:
            raise ValueError('Scientific passage hash mismatch')
    return rows

def search_scientific_passages(question,top_k=5):
    """Exact-ID or two-topic-term matching, so unrelated questions do not inherit citations."""
    if not isinstance(question,str) or not question.strip(): raise ValueError('question required')
    if not isinstance(top_k,int) or not 1<=top_k<=20: raise ValueError('top_k must be 1..20')
    ids=set(re.findall(r'\bQ-[A-Z]\d+\b',question.upper()))
    qt=tokens(question)-{'the','a','an','which','what','is','are','for','in','of','on','to','how','qatar','name','scientific','review','question','about'}
    matches=[]
    for p in scientific_source_passages():
        if ids:
            if not ids.intersection(p['question_ids']): continue
            score=100
        else:
            # Metadata and short exact excerpt. Exclude source limitations from retrieval.
            match=tokens(' '.join(p['topic_terms'])+' '+p['excerpt']) & qt
            if len(match)<2: continue
            score=len(match)
        matches.append((score,p))
    matches.sort(key=lambda t:(-t[0],t[1]['passage_id']))
    return [{'match_score':score,**p} for score,p in matches[:top_k]]

def last_receipt():
    """Read back last durable local decision after chain verification; no network or new store."""
    status=verify_receipts()
    if not status['valid']: return {'status':'BLOCK','reason':'RECEIPT_CHAIN_INVALID',**status}
    if status['events']==0: return {'status':'EMPTY','events':0}
    last=json.loads([line for line in RECEIPTS.read_text(encoding='utf-8').splitlines() if line.strip()][-1])
    return {'status':'PASS','events':status['events'],'event_id':last['event_id'],
            'timestamp_utc':last['timestamp_utc'],'receipt_hash':last['receipt_hash'],
            'decision':last['result'].get('decision') or last['result'].get('status'),
            'reason':last['result'].get('reason'),'evidence_refs':last['result'].get('evidence_refs',[])}

def search_scientific_review(question, top_k=5):
    if not isinstance(question,str) or not question.strip(): raise ValueError('question required')
    if not isinstance(top_k,int) or not 1 <= top_k <= 20: raise ValueError('top_k must be 1..20')
    qt=tokens(question)
    # An explicit ID maps exactly; otherwise require >=2 distinctive query terms.
    id_matches=re.findall(r'\bQ-[A-Z]\d+\b',question.upper())
    scored=[]
    stop={'the','a','and','or','of','in','is','are','what','which','for','from','to','with','on','how','qatar','crops','crop','question','agriculture','agricultural'}
    meaningful=qt-stop
    for record in scientific_review_records():
        if id_matches:
            if record['question_id'] not in id_matches: continue
            score=100
        else:
            # Only question text and candidate topic indexable; do not index a purported source quote.
            rt=tokens(record['question_text'])-stop
            shared=meaningful & rt
            if len(shared)<2: continue
            score=len(shared)
        scored.append((score,record))
    scored.sort(key=lambda pair:(-pair[0],pair[1]['question_id']))
    return [{'score':score,**record} for score,record in scored[:top_k]]

def search_evidence(question, top_k=5):
    if not isinstance(question,str) or not question.strip(): raise ValueError('question required')
    if not isinstance(top_k,int) or top_k<1 or top_k>20: raise ValueError('top_k must be 1..20')
    qt=tokens(question); stop={'the','a','in','for','of','and','is','what','how','much','was','are','qatar','cucumber','cucumbers'}
    meaningful=qt-stop
    scored=[]
    for doc in corpus():
        dt=tokens(doc['text']+' '+doc['id']+' '+doc['kind'])
        overlap=len(meaningful & dt)
        # Exact year/scope matching prevents mismatched time/scope from dominating.
        for year in re.findall(r'\b20\d{2}\b',question):
            if doc['data']['year']!=year: overlap=-100
        if 'greenhouse' in qt and doc['data'].get('scope')!='GREENHOUSE': overlap=-100
        if ('open' in qt and 'field' in qt) and doc['data'].get('scope')!='OPEN_FIELD': overlap=-100
        if (('import' in qt or 'imports' in qt or 'cif' in qt) and doc['kind']!='TRADE'): overlap=-100
        if overlap>0: scored.append((overlap,doc))
    scored.sort(key=lambda x:(-x[0],x[1]['id']))
    return [{'score':s,**d} for s,d in scored[:top_k]]

def append_receipt(kind, result):
    # Local-only persistence, never networked; append-only and hash linked for tamper evidence.
    prev='GENESIS'
    if RECEIPTS.exists():
        checked=verify_receipts()
        if not checked.get('valid'):
            raise ValueError('Existing local receipt chain is invalid; refusing to append')
        prev=checked.get('last_hash','GENESIS')
    obj={'event_id':str(uuid.uuid4()),'timestamp_utc':datetime.now(timezone.utc).isoformat(),'kind':kind,'previous_hash':prev,'result':result}
    blob=json.dumps(obj,sort_keys=True,separators=(',',':'))
    obj['receipt_hash']=hashlib.sha256(blob.encode()).hexdigest()
    with RECEIPTS.open('a',encoding='utf-8') as f: f.write(json.dumps(obj,sort_keys=True)+'\n')
    return obj['receipt_hash']

def _required_input_intent(question):
    """Small bounded semantic/phrase gate: descriptive public aggregates remain accessible.

    This is a conservative ruleset, not a comprehensive natural-language safety classifier.
    Unknown consequential advice must be handled by the outer safe-failure policy.
    """
    q = question.casefold()
    qt = tokens(q)
    # Public trade unit values are *known* and distinct from delivered/farm cost.
    public_trade = bool(re.search(r"\b(imports?|cif|wits|hs\s*070700)\b",q))
    unit_value = bool(re.search(r"\b(unit\s*(?:price|value)|average\s*(?:price|value)|(?:import\s*)?price\s*per\s*(?:kg|kilo)|usd\s*/\s*kg)\b",q))
    comparative = bool(re.search(r"\b(cheaper|cheap(?:est)?|worth|saving|saves?|money|subsid\w*|profit\w*|viab\w*|afford\w*|financial|economics?|cost[- ]effective|versus|vs\.?|instead\s+of|better\s+to)\b",q))
    cost = bool(re.search(r"\b(costs?|costing|expensive|operating\s+cost|farm\s+price|production\s+price|margins?|revenue|return\s+on\s+investment)\b",q))
    # A pure public CIF unit-value lookup is answerable; a business decision is not.
    if public_trade and unit_value and not comparative and not cost:
        financial=False
    else:
        financial=comparative or cost or bool(re.search(r"\b(pric(?:ing|es?))\b",q) and not unit_value)
    water=bool(re.search(r"\b(water|watering|irrigat\w*|transpirat\w*|evapotranspirat\w*|wue|litres?|liters?|h2o|hydration|water[- ]use)\b",q))
    soil=bool(re.search(r"\b(ec|ecs|salin\w*|conductiv\w*|salty|soil\s+salt\w*|electrical\s+conductivity)\b",q))
    return financial, water, soil

def _missing_required_inputs(question):
    """Block unsupported conclusions before retrieval; preserve descriptive lookups."""
    financial,water,soil = _required_input_intent(question)
    required=set()
    if financial:
        required.update(('marketable_kg','local_variable_cost','local_fixed_allocated','water_cost','energy_cost','distribution_cost','import_landed_cost_per_kg','import_loss_fraction'))
    if water:
        required.update(('water_m3','marketable_kg'))
    if soil:
        required.update(('measured_soil_ec_ds_m','soil_sample_depth_cm','soil_sample_timestamp_utc'))
    return [x for x in REQUIRED if x in required] + sorted(required-set(REQUIRED))

def ask(question,save=True):
    if not isinstance(question,str) or not question.strip(): raise ValueError('question required')
    missing=_missing_required_inputs(question)
    if missing:
        outcome={'decision':'BLOCK','reason':'MISSING_REQUIRED_INPUTS','question':question,
                 'evidence_refs':[], 'missing':missing,
                 'answer':'Missing required measured or comparable inputs: '+', '.join(missing)+'. Supply those values with source, units, and a matching reporting period before making this conclusion.'}
    else:
        scientific=search_scientific_review(question)
        if scientific:
            passages=search_scientific_passages(question)
            outcome={'decision':'REVIEW','reason':'SCIENTIFIC_REFERENCE_NOT_ADJUDICATED',
                     'question':question,'evidence_refs':[r['question_id'] for r in scientific]+[p['passage_id'] for p in passages],
                     'answer':'Matching scientific questions are unresolved. Verified short source excerpts are inspectable evidence, not approved answer keys or field guidance.',
                     'evidence':scientific,'source_passages':passages}
            if save: outcome['receipt_hash']=append_receipt('ask',outcome)
            return outcome
        results=search_evidence(question)
        lower=question.lower()
        high_risk=any(x in lower for x in ('tariff','quota','autonomous','navigation command'))
        if not results:
            outcome={'decision':'BLOCK','reason':'NO_MATCHING_VERIFIABLE_EVIDENCE','question':question,'evidence_refs':[],'answer':'No supported answer in the local source registry. Do not infer values.'}
        elif high_risk:
            outcome={'decision':'BLOCK','reason':'REQUIRED_FARM_COST_OR_CALIBRATION_OR_AUTHORITY_MISSING','question':question,'evidence_refs':[r['id'] for r in results],'answer':'Available aggregates do not establish legal policy or permissible drone action.','evidence':results}
        else:
            outcome={'decision':'WARN','reason':'PUBLIC_AGGREGATE_DESCRIPTIVE_ONLY','question':question,'evidence_refs':[r['id'] for r in results],'answer':'Retrieved source-backed aggregates only; inspect evidence records and their units, scopes, and limitations.','evidence':results}
    if save: outcome['receipt_hash']=append_receipt('ask',outcome)
    return outcome

def evaluate_case(case_id):
    rows=[r for r in read_rows('economic_cases.csv') if r['case_id']==case_id]
    if len(rows)!=1: raise ValueError('case_id unavailable or ambiguous')
    result=evaluate(rows[0]);result['evidence_type']=rows[0]['evidence_type'];result['source_boundary']='CIF import figure is not a full delivered import cost'
    result['receipt_hash']=append_receipt('economic_case',result)
    return result

def verify_receipts():
    """Detect modification/truncation of entries; not proof against complete log replacement."""
    prev='GENESIS';count=0
    if not RECEIPTS.exists(): return {'valid':True,'events':0,'last_hash':'GENESIS'}
    try:
        for i,line in enumerate(RECEIPTS.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip(): return {'valid':False,'bad_line':i,'reason':'EMPTY_LINE'}
            r=json.loads(line)
            if not isinstance(r,dict): return {'valid':False,'bad_line':i,'reason':'INVALID_EVENT'}
            hash_saved=r.pop('receipt_hash',None)
            if not hash_saved or 'previous_hash' not in r:
                return {'valid':False,'bad_line':i,'reason':'MISSING_RECEIPT_FIELDS'}
            actual=hashlib.sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            if r['previous_hash']!=prev or hash_saved!=actual:
                return {'valid':False,'bad_line':i,'reason':'HASH_CHAIN_MISMATCH'}
            prev=hash_saved;count+=1
    except (OSError,ValueError,TypeError,KeyError,UnicodeError):
        return {'valid':False,'bad_line':count+1,'reason':'INVALID_RECEIPT_FORMAT'}
    return {'valid':True,'events':count,'last_hash':prev}

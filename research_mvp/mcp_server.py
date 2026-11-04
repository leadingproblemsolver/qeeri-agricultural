"""Minimal MCP JSON-RPC 2.0 server over newline-delimited stdio; no network transport."""
import sys,json
from qeeri_brain import ask,search_evidence,evaluate_case,corpus,verify_receipts,scientific_review_records,search_scientific_review,scientific_source_passages,search_scientific_passages,last_receipt

TOOLS=[
 {'name':'qeeri_ask','description':'Ask a Qatar agricultural environment/finance question; returns sourced aggregates or a deterministic BLOCK','inputSchema':{'type':'object','properties':{'question':{'type':'string'}},'required':['question']}},
 {'name':'qeeri_search_evidence','description':'Search local verified source rows with citations and scope metadata','inputSchema':{'type':'object','properties':{'question':{'type':'string'},'top_k':{'type':'integer','minimum':1,'maximum':20}},'required':['question']}},
 {'name':'qeeri_evaluate_economic_case','description':'Run existing QEERI deterministic economic gate for an archived case ID','inputSchema':{'type':'object','properties':{'case_id':{'type':'string'}},'required':['case_id']}},
 {'name':'qeeri_search_scientific_review','description':'Search 11 flagged agricultural questions; returns only REVIEW metadata, not adjudicated answers','inputSchema':{'type':'object','properties':{'question':{'type':'string'},'top_k':{'type':'integer','minimum':1,'maximum':20}},'required':['question']}},
 {'name':'qeeri_search_scientific_passages','description':'Search independently located short science excerpts. REVIEW only; not approved answers','inputSchema':{'type':'object','properties':{'question':{'type':'string'},'top_k':{'type':'integer','minimum':1,'maximum':20}},'required':['question']}},
 {'name':'qeeri_last_receipt','description':'Inspect the most recent verified local receipt for restart','inputSchema':{'type':'object','properties':{}}},
 {'name':'qeeri_verify_receipts','description':'Check the local hash-linked JSONL receipt chain','inputSchema':{'type':'object','properties':{}}},
 {'name':'qeeri_list_sources','description':'List local evidence record identifiers and sources','inputSchema':{'type':'object','properties':{}}}
]

def dispatch(req):
    method=req.get('method'); params=req.get('params') or {}
    if method=='initialize':return {'protocolVersion':'2025-03-26','capabilities':{'tools':{}},'serverInfo':{'name':'qeeri-local-evidence','version':'0.1.0'}}
    if method=='ping':return {}
    if method=='tools/list':return {'tools':TOOLS}
    if method=='tools/call':
        name=params.get('name');a=params.get('arguments') or {}
        if name=='qeeri_ask': data=ask(a['question'])
        elif name=='qeeri_search_evidence':data=search_evidence(a['question'],a.get('top_k',5))
        elif name=='qeeri_evaluate_economic_case':data=evaluate_case(a['case_id'])
        elif name=='qeeri_search_scientific_review':data=search_scientific_review(a['question'],a.get('top_k',5))
        elif name=='qeeri_search_scientific_passages':data=search_scientific_passages(a['question'],a.get('top_k',5))
        elif name=='qeeri_last_receipt':data=last_receipt()
        elif name=='qeeri_verify_receipts':data=verify_receipts()
        elif name=='qeeri_list_sources':data=([{'id':x['id'],'source':x['source'],'kind':x['kind']} for x in corpus()] + [{'id':r['question_id'],'source':r['reference_url'],'kind':'SCIENTIFIC_REVIEW','status':'REVIEW'} for r in scientific_review_records()] + [{'id':p['passage_id'],'source':p['source_url'],'kind':'SCIENTIFIC_PASSAGE','status':'REVIEW'} for p in scientific_source_passages()])
        else:raise ValueError('Unknown MCP tool')
        return {'content':[{'type':'text','text':json.dumps(data,ensure_ascii=False)}],'isError':False}
    if method.startswith('notifications/'):return None
    raise ValueError('Method not supported')

def main():
    for line in sys.stdin:
        try:
            req=json.loads(line)
            if 'id' not in req: continue
            try:
                resp={'jsonrpc':'2.0','id':req['id'],'result':dispatch(req)}
            except Exception as e:
                resp={'jsonrpc':'2.0','id':req['id'],'error':{'code':-32603,'message':str(e)}}
            sys.stdout.write(json.dumps(resp,ensure_ascii=False)+'\n')
            sys.stdout.flush()
        except Exception:
            continue

if __name__ == '__main__':
    main()

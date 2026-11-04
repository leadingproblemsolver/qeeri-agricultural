"""Independent stdio MCP JSON-RPC client smoke test (stdlib only)."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
messages=[
 {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'qeeri-smoke','version':'1'}}},
 {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}},
 {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'qeeri_ask','arguments':{'question':'Q-K26 potato aphid'}}},
 {'jsonrpc':'2.0','id':4,'method':'tools/call','params':{'name':'qeeri_last_receipt','arguments':{}}},
 {'jsonrpc':'2.0','id':5,'method':'tools/call','params':{'name':'qeeri_verify_receipts','arguments':{}}},
]
proc=subprocess.run([sys.executable,str(ROOT/'mcp_server.py')],input='\n'.join(json.dumps(m) for m in messages)+'\n',capture_output=True,text=True,cwd=ROOT,timeout=12)
if proc.returncode: raise SystemExit(proc.stderr or f'MCP server failed {proc.returncode}')
replies=[json.loads(x) for x in proc.stdout.splitlines() if x.strip()]
assert len(replies)==5 and [x['id'] for x in replies]==[1,2,3,4,5]
assert all('result' in r for r in replies),replies
assert len(replies[1]['result']['tools'])==8
science=json.loads(replies[2]['result']['content'][0]['text'])
assert science['decision']=='REVIEW' and 'UCIPM-POTATO-APHID' in science['evidence_refs']
last=json.loads(replies[3]['result']['content'][0]['text'])
check=json.loads(replies[4]['result']['content'][0]['text'])
assert last['status']=='PASS' and last['decision']=='REVIEW' and check['valid']
print(json.dumps({'mcp_protocol':'PASS','requests':5,'tools':8,'scientific_review':'REVIEW','passage_id':'UCIPM-POTATO-APHID','local_receipt_valid':check['valid'],'restart_last':'PASS'}))

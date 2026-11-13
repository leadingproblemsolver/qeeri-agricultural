"""Deterministic retrieval/citation evaluation over retrieval_gold.json (stdlib only).

Calls ask(save=False): no receipts are written. Small author-labeled gold set; not a generalization claim.
"""
import json, sys
from pathlib import Path
from qeeri_brain import ask, corpus, scientific_review_records, scientific_source_passages

HERE = Path(__file__).resolve().parent

def known_ids():
    return ({d['id'] for d in corpus()} | {r['question_id'] for r in scientific_review_records()}
            | {p['passage_id'] for p in scientific_source_passages()})

def run(gold_path=HERE / 'retrieval_gold.json'):
    gold = json.loads(Path(gold_path).read_text(encoding='utf-8'))
    k = gold['k']; known = known_ids()
    rows = []; tot_exp = hit = ret = rel = cited = resolved = irrelevant = decision_ok = 0
    pos = [c for c in gold['cases'] if c['expect_refs']]
    for c in gold['cases']:
        out = ask(c['query'], save=False)
        refs = list(out.get('evidence_refs', []))[:k]
        exp = set(c['expect_refs'])
        r_hit = len(exp & set(refs)); r_rel = len([x for x in refs if x in exp])
        r_unres = [x for x in refs if x not in known]
        r_irr = [x for x in refs if x not in exp]
        if exp:
            tot_exp += len(exp); hit += r_hit; ret += len(refs); rel += r_rel
        cited += len(refs); resolved += len(refs) - len(r_unres); irrelevant += len(r_irr)
        ok = out['decision'] == c['expect_decision']; decision_ok += ok
        rows.append({'id': c['id'], 'type': c['type'], 'query': c['query'], 'decision': out['decision'],
                     'expect_decision': c['expect_decision'], 'decision_ok': ok, 'refs': refs,
                     'expect_refs': sorted(exp), 'irrelevant_refs': r_irr, 'unresolved_refs': r_unres})
    n_abstain = len(gold['cases']) - len(pos)
    abstain_ok = sum(1 for r in rows if not r['expect_refs'] and r['decision'] == 'BLOCK' and not r['refs'])
    return {'label': gold['label'], 'k': k, 'cases': len(gold['cases']), 'positive_cases': len(pos),
            'recall_at_k': round(hit / tot_exp, 4) if tot_exp else None,
            'precision_at_k': round(rel / ret, 4) if ret else None,
            'citation_resolution_rate': round(resolved / cited, 4) if cited else None,
            'citation_gold_substantiation_rate': round((cited - irrelevant) / cited, 4) if cited else None,
            'irrelevant_citation_rate': round(irrelevant / cited, 4) if cited else None,
            'decision_accuracy': round(decision_ok / len(rows), 4),
            'abstention_correct': f'{abstain_ok}/{n_abstain}', 'results': rows}

if __name__ == '__main__':
    rep = run()
    out = HERE / 'retrieval_eval.json'
    out.write_text(json.dumps(rep, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in rep.items() if k != 'results'}, indent=2))
    for r in rep['results']:
        if not r['decision_ok'] or r['irrelevant_refs'] or r['unresolved_refs'] or (r['expect_refs'] and set(r['expect_refs']) - set(r['refs'])):
            print('FAIL', r['id'], r['query'], '->', r['decision'], r['refs'])

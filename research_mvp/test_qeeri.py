import unittest, tempfile, hashlib
from pathlib import Path
from unittest.mock import patch
import qeeri_brain as b
import mcp_server as m
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.p=patch.object(b,'RECEIPTS',Path(self.tmp.name)/'local.jsonl');self.p.start()
    def tearDown(self):self.p.stop();self.tmp.cleanup()
    def test_base_records(self):
        assert len([r for r in b.corpus() if r['kind']=='TRADE'])==2
    def test_derived_recompute(self):
        r=next(r for r in b.corpus() if r['id'].endswith('2023'))
        self.assertAlmostEqual(r['data']['usd_per_kg'],3998210/2790740,places=5)
    def test_2024_query(self):
        r=b.ask('Qatar cucumber imports 2024')
        self.assertEqual(r['decision'],'WARN');self.assertEqual(r['evidence_refs'],['WITS-QAT-070700-2024'])
    def test_no_fake_source(self):self.assertEqual(b.ask('What is the cosmic banana probability?')['decision'],'BLOCK')
    def test_missing_cost(self):self.assertEqual(b.ask('Is growing cucumber in Qatar more profitable than imports in 2024?')['decision'],'BLOCK')
    def test_economic_block(self):self.assertEqual(b.evaluate_case('OBS-WITS-2024')['status'],'BLOCKED_MISSING_DATA')
    def test_receipt_chain(self):
        b.ask('Qatar cucumber imports 2023');self.assertTrue(b.verify_receipts()['valid'])
        x=b.RECEIPTS.read_text();b.RECEIPTS.write_text(x.replace('2023','2022',1));self.assertFalse(b.verify_receipts()['valid'])
    def test_mcp_init(self):self.assertEqual(m.dispatch({'method':'initialize'})['serverInfo']['name'],'qeeri-local-evidence')
    def test_mcp_list(self):self.assertEqual(len(m.dispatch({'method':'tools/list'})['tools']),8)
    def test_mcp_call(self):self.assertEqual(m.dispatch({'method':'tools/call','params':{'name':'qeeri_ask','arguments':{'question':'Qatar cucumber imports 2024'}}})['isError'],False)
    def test_missing_zero(self):
        r=b.evaluate_case('OBS-WITS-2023');self.assertIn('marketable_kg',r['missing'])
    def test_scope(self):
        r=b.search_evidence('greenhouse cucumber production 2025')
        self.assertTrue(r);self.assertTrue(all(x['data'].get('scope')=='GREENHOUSE' for x in r))
    def test_wrong_crop_query_fails_closed_no_cucumber_citation(self):
        for q in ('Qatar tomato production 2024','wheat yield in Qatar 2024'):
            r=b.ask(q,save=False)
            self.assertEqual(r['decision'],'BLOCK',q);self.assertEqual(r['evidence_refs'],[],q)
        self.assertEqual(b.ask('Qatar cucumber imports 2024',save=False)['evidence_refs'],['WITS-QAT-070700-2024'])
    def test_multi_year_same_scope_comparison_warns(self):
        r=b.ask('Compare greenhouse cucumber production 2023 and 2024',save=False)
        self.assertEqual(r['decision'],'WARN')
        self.assertEqual(set(r['evidence_refs']),{'QATAR-CUCUMBER-GREENHOUSE-2023','QATAR-CUCUMBER-GREENHOUSE-2024'})
        self.assertEqual(b.ask('Qatar cucumber imports 2031',save=False)['decision'],'BLOCK')
    def test_p1_public_cif_unit_value_remains_answerable(self):
        r=b.ask('What is the unit price of Qatar cucumber imports 2024?')
        self.assertEqual(r['decision'],'WARN')
        self.assertEqual(r['evidence_refs'],['WITS-QAT-070700-2024'])
    def test_p1_descriptive_greenhouse_comparison_not_cost(self):
        r=b.ask('Compare greenhouse production 2023 and 2024')
        self.assertNotIn('MISSING_REQUIRED_INPUTS',r.get('reason',''))
        self.assertNotIn('local_variable_cost',r.get('missing',[]))
    def test_p1_source_limitations_not_indexed(self):
        r=b.search_evidence('soil EC')
        self.assertEqual(r,[])
# Fixed reported and unseen hostile phrasings each count as an independent regression test.
_P1_BLOCK_CASES = {
    'compare_growing_importing': 'Which is cheaper: importing or growing cucumbers in 2024?',
    'grow_cost': 'What does it cost to grow cucumbers?',
    'soil_ec': 'What is the soil EC in Qatar greenhouses?',
    'water_per_kg': 'How much water per kg of greenhouse cucumber?',
    'cheap_import': 'Is it cheaper to import cucumbers?',
    'worth_growing': 'Is it worth growing cucumbers locally instead of buying imports?',
    'saving_money': 'Is local production saving money versus importing?',
    'subsidise': 'Should Qatar subsidise greenhouse cucumber growers?',
    'plural_ecs': 'Qatar cucumber ECs 2024',
    'salty': 'How salty is the soil for Qatar cucumbers?',
    'litres': 'How many litres does a cucumber plant need?',
    'h2o': 'Do greenhouses use too much H2O?',
}
def _p1_case(question):
    def test(self):
        r=b.ask(question)
        self.assertEqual(r['decision'],'BLOCK')
        self.assertEqual(r['reason'],'MISSING_REQUIRED_INPUTS')
        self.assertTrue(r['missing'])
    return test
for _name,_q in _P1_BLOCK_CASES.items():
    setattr(Tests,'test_p1_block_'+_name,_p1_case(_q))

class ScientificReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.patch=patch.object(b,'RECEIPTS',Path(self.tmp.name)/'local.jsonl');self.patch.start()
    def tearDown(self):self.patch.stop();self.tmp.cleanup()
    def test_exact_inventory(self):
        r=b.scientific_review_records();self.assertEqual(len(r),11)
        self.assertTrue(all(x['disposition']=='REVIEW' and x['approved_answer'] is False and x['source_passage_verified'] is False for x in r))
    def test_exact_id_routes_to_review(self):
        r=b.ask('Review Q-K26 potato aphid scientific key')
        self.assertEqual(r['decision'],'REVIEW');self.assertIn('Q-K26',r['evidence_refs']);self.assertIn('UCIPM-POTATO-APHID',r['evidence_refs'])
    def test_natural_question_routes_review(self):
        r=b.ask('Which aphid is potato aphid?')
        self.assertEqual(r['decision'],'REVIEW')
    def test_no_scientific_answer_promotion(self):
        r=b.ask('Review Q-K29')
        self.assertEqual(r['reason'],'SCIENTIFIC_REFERENCE_NOT_ADJUDICATED')
        self.assertIn('not approved',r['answer'])
    def test_no_unrelated_citation(self):
        self.assertEqual(b.search_scientific_review('How much cucumber exports to Alpha Centauri?'),[])
    def test_missing_source_does_not_fabricate_url(self):
        r=b.search_scientific_review('Q-K35')
        self.assertEqual(len(r),1);self.assertEqual(r[0]['reference_url'],'')
    def test_mcp_exposes_review_only(self):
        r=m.dispatch({'method':'tools/call','params':{'name':'qeeri_search_scientific_review','arguments':{'question':'Q-C3'}}})
        self.assertTrue(r['content']);self.assertIn('LEGAL_THRESHOLD_UNVERIFIED',r['content'][0]['text'])
    def test_review_receipt_restart(self):
        b.ask('Review Q-K26'); self.assertTrue(b.verify_receipts()['valid'])
    def test_existing_import_answer_untouched(self):
        self.assertEqual(b.ask('Qatar cucumber imports 2024')['decision'],'WARN')
    def test_cost_block_untouched(self):
        self.assertEqual(b.ask('What is the cost to grow cucumbers?')['decision'],'BLOCK')


class SourcePassageAndBrainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.patch=patch.object(b,'RECEIPTS',Path(self.tmp.name)/'local.jsonl'); self.patch.start()
    def tearDown(self): self.patch.stop(); self.tmp.cleanup()
    def test_passages_indexed_with_verified_locators(self):
        entries=b.scientific_source_passages()
        self.assertEqual(len(entries),4)
        self.assertTrue(all(p['status']=='REVIEW' and p['source_url'].startswith('https://') for p in entries))
    def test_specific_question_retrieves_real_excerpt(self):
        r=b.ask('Q-K26 potato aphid')
        self.assertEqual(r['decision'],'REVIEW')
        self.assertIn('UCIPM-POTATO-APHID',r['evidence_refs'])
        self.assertTrue(r['source_passages'][0]['source_locator'])
    def test_science_not_auto_approved(self):
        r=b.ask('Which aphid is potato aphid?')
        self.assertEqual(r['decision'],'REVIEW')
        self.assertTrue(all(x['status']=='REVIEW' for x in r['source_passages']))
    def test_unrelated_no_citation(self):
        self.assertEqual(b.search_scientific_passages('Quantum banana export futures 2024'),[])
    def test_unverified_question_no_fabricated_passage(self):
        r=b.ask('Q-C3 exact nitrate runoff legal limit')
        self.assertIn('Q-C3',r['evidence_refs'])
        self.assertEqual(r['source_passages'],[])
    def test_water_recommendation_blocks_missing(self):
        r=b.ask('How much water does a greenhouse need per kg?')
        self.assertEqual(r['decision'],'BLOCK')
        self.assertEqual(r['reason'],'MISSING_REQUIRED_INPUTS')
    def test_cost_comparison_blocks(self):
        r=b.ask('Is it cheaper to grow local cucumbers than import?')
        self.assertEqual(r['decision'],'BLOCK')
    def test_descriptive_import_retained(self):
        r=b.ask('Qatar cucumber imports 2024')
        self.assertEqual(r['decision'],'WARN')
    def test_restart_last_receipt(self):
        b.ask('Review Q-K26')
        self.assertEqual(b.last_receipt()['status'],'PASS')
        self.assertEqual(b.last_receipt()['decision'],'REVIEW')
        self.assertTrue(b.verify_receipts()['valid'])
    def test_modified_chain_fails_restart(self):
        b.ask('Review Q-K26')
        x=b.RECEIPTS.read_text(); b.RECEIPTS.write_text(x.replace('Q-K26','Q-K25',1))
        self.assertEqual(b.last_receipt()['status'],'BLOCK')
    def test_mcp_exposes_source_passages(self):
        out=m.dispatch({'method':'tools/call','params':{'name':'qeeri_search_scientific_passages','arguments':{'question':'Q-K29'}}})
        self.assertIn('APS-TOMATO-FUSARIUM',out['content'][0]['text'])
    def test_mcp_reentry(self):
        b.ask('Qatar cucumber imports 2024')
        out=m.dispatch({'method':'tools/call','params':{'name':'qeeri_last_receipt','arguments':{}}})
        self.assertIn('PASS',out['content'][0]['text'])
    def test_malformed_receipt_safe_failure(self):
        b.RECEIPTS.write_text('{not_json\n')
        self.assertFalse(b.verify_receipts()['valid'])
        self.assertEqual(b.last_receipt()['status'],'BLOCK')
    def test_tampered_chain_refuses_to_append(self):
        b.ask('Qatar cucumber imports 2024')
        b.RECEIPTS.write_text(b.RECEIPTS.read_text().replace('2024','2022',1))
        with self.assertRaisesRegex(ValueError,'receipt chain is invalid'):
            b.ask('Qatar cucumber imports 2023')
    def test_source_hash_rejects_modified_excerpt(self):
        item=b.scientific_source_passages()[0]
        self.assertNotEqual(hashlib.sha256((item['excerpt']+'x').encode()).hexdigest(),item['excerpt_sha256'])

if __name__=='__main__':unittest.main()

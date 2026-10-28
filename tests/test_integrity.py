import sys,unittest,pathlib,importlib.util
R=pathlib.Path(__file__).resolve().parents[1]
def load(name):
 s=importlib.util.spec_from_file_location(name,R/'tools'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
q=load('qeeri');score=load('score_agreement')
class TestIntegrity(unittest.TestCase):
 def test_table_counts(self):
  e,r,p,qu=q.verify();self.assertEqual(e,[]);self.assertEqual((len(r),len(p),len(qu)),(200,200,200))
 def test_zero_real_answers(self):
  e,r,p,qu=q.verify();self.assertEqual(sum(x['response_status']!='pending' for x in r),0)
 def test_smoke_order(self):
  e,r,p,qu=q.verify();self.assertEqual({x['run_id'] for x in qu[:8]},q.SMOKE)
 def test_exact_prefix(self):
  e,r,p,qu=q.verify();self.assertTrue(all('Do not guess exact values, legal limits, or chemical treatments' in x['full_prompt'] for x in p))
 def test_qatar_full_wording(self):
  e,r,p,qu=q.verify();self.assertTrue(any('When operating a greenhouse in Qatar during July' in x['full_prompt'] for x in p));self.assertTrue(any('My greenhouse cucumber leaves are turning yellow' in x['full_prompt'] for x in p))
 def test_kappa_synthetic_only(self):
  self.assertAlmostEqual(score.kappa([0,1,2],[0,1,2]),1);self.assertIsNone(score.kappa([1,1],[1,1]))
if __name__=='__main__':unittest.main()

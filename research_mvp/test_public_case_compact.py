import copy
import unittest
from qatar_public_case import build_public_case
from qeeri_brain import read_rows

class PublicCaseAcceptance(unittest.TestCase):
    def setUp(self):
        self.p=read_rows('cucumber_scopes.csv')
        self.t=read_rows('wits_imports.csv')
        self.r=build_public_case(self.p,self.t)
    def test_2024_source_totals(self):
        self.assertEqual(self.r['production']['tonnes'],17512.73)
        self.assertEqual(self.r['production']['area_ha'],251.8)
        self.assertEqual(self.r['trade']['value_usd'],3638150)
        self.assertEqual(self.r['trade']['net_weight_kg'],10417700)
    def test_recomputed_units(self):
        self.assertAlmostEqual(self.r['trade']['cif_unit_value_usd_per_kg'],3638150/10417700,places=6)
        self.assertAlmostEqual(self.r['production']['tonnes_per_ha'],17512.73/251.8,places=5)
    def test_safety_decisions(self):
        for key,missing in [('relative_cost','local_variable_cost'),('soil_ec','measured_soil_ec_ds_m'),('water_efficiency','water_m3')]:
            with self.subTest(key=key):
                d=self.r['decisions'][key]
                self.assertEqual(d['decision'],'BLOCK')
                self.assertIn(missing,d['missing'])
    def test_trade_anomaly_review(self):
        self.assertGreater(self.r['trade']['year_over_year_net_weight_ratio'],3.7)
        self.assertEqual(self.r['decisions']['weight_anomaly']['decision'],'REVIEW')
    def test_no_farm_claim(self):
        self.assertFalse(self.r['comparability']['financial_comparison_eligible'])
        self.assertFalse(self.r['comparability']['same_crop_exactly'])
        self.assertEqual(self.r['climate']['status'],'NOT_ACQUIRED')
    def test_duplicate_fails_closed(self):
        row=next(r for r in self.p if r['year']=='2024' and r['source_scope']=='GREENHOUSE')
        with self.assertRaises(ValueError):build_public_case(self.p+[row],self.t)
    def test_wrong_year_fails_closed(self):
        rows=copy.deepcopy(self.t)
        next(r for r in rows if r['year']=='2024')['year']='2025'
        with self.assertRaises(ValueError):build_public_case(self.p,rows)
    def test_wrong_unit_fails_closed(self):
        rows=copy.deepcopy(self.t)
        next(r for r in rows if r['year']=='2024')['quantity_unit']='tonnes'
        with self.assertRaises(ValueError):build_public_case(self.p,rows)
    def test_fake_source_fails_closed(self):
        rows=copy.deepcopy(self.t)
        next(r for r in rows if r['year']=='2024')['source_url']='https://invalid.example'
        with self.assertRaises(ValueError):build_public_case(self.p,rows)
    def test_zero_weight_fails_closed(self):
        rows=copy.deepcopy(self.t)
        next(r for r in rows if r['year']=='2024')['net_weight_kg']='0'
        with self.assertRaises(ValueError):build_public_case(self.p,rows)

if __name__=='__main__':unittest.main()

import unittest
from evaluate import assess

class CoolingLogicTests(unittest.TestCase):
    def make(self, db, wb, eta, target):
        return dict(id="test", input_kind="HYPOTHETICAL_NOT_SITE_MEASURED",
                    dry_bulb_C=db, wet_bulb_C=wb,
                    effectiveness_fraction=eta, target_pad_exit_C=target)

    def test_google_example(self):
        r = assess(self.make(40, 20, .85, 25))
        self.assertEqual(r["pad_outlet_temperature_C"], 23)
        self.assertEqual(r["crop_safety_status"], "NOT_ASSESSABLE")
        self.assertFalse(r["construction_ready"])

    def test_summer_synthetic(self):
        r = assess(self.make(45, 31, .85, 28))
        self.assertEqual(r["pad_outlet_temperature_C"], 33.1)
        self.assertFalse(r["pad_outlet_at_or_below_example_target"])

    def test_impossible_wet_bulb(self):
        with self.assertRaises(ValueError): assess(self.make(30, 35, .85, 25))

    def test_invalid_efficiency(self):
        with self.assertRaises(ValueError): assess(self.make(40, 20, 1.2, 25))

    def test_unverified_input_not_promoted(self):
        s = self.make(29, 23, .85, 25)
        s["input_kind"] = "UNVERIFIED_USER_SUPPLIED_REPORT"
        with self.assertRaises(ValueError): assess(s)

if __name__ == "__main__":
    unittest.main()

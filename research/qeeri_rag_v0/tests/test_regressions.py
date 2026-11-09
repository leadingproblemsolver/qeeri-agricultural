"""Regression fixtures for defects found by inspecting receipts (not by exit codes)."""
import unittest
from pathlib import Path

from helpers import real_index, tmpdir_ctx
from qeeri_rag.loop import LoopConfig, run_question


def ask(q, **kw):
    with tmpdir_ctx() as t:
        return run_question(real_index(), q, config=LoopConfig(receipts_dir=str(Path(t) / "r"), **kw))


class Regressions(unittest.TestCase):
    def test_extractive_claim_carries_whole_chunk_including_the_equation(self):
        r = ask("What is the pad outlet temperature equation for fan and pad cooling?")
        self.assertIn("T_pad_out = T_out_drybulb", r["claims"][0]["text"])  # was truncated to the first paragraph

    def test_conflict_names_the_missing_resolution_not_a_generic_gap(self):
        r = ask("What fan airflow per floor area do fan and pad greenhouses use?")
        self.assertIn("priority rule", r["inputs"]["missing"][0])
        self.assertIn("fan_pad_airflow_per_floor_area", r["inputs"]["missing"][0])

    def test_site_value_question_names_the_missing_measurement(self):
        r = ask("What is the measured wet-bulb temperature at the Al-Shahaniya greenhouse in July?")
        self.assertIn("measured or source-reported value applicable to jurisdiction QA", r["inputs"]["missing"][0])

    def test_health_lists_sources_rejected_before_insertion(self):
        from qeeri_rag.store import health
        ids = {x["source_id"]: x["reason"] for x in health(real_index())["rejected_sources"]}
        self.assertEqual(ids["S4_LAHLOU_2025"], "VERIFICATION_STATUS_NOT_ELIGIBLE")

    def test_relaxed_strategy_is_less_precise_which_is_why_it_is_not_the_default(self):
        from qeeri_rag.retrieve import retrieve
        q = "What is the pad outlet temperature equation for fan and pad cooling?"
        con = real_index()
        strict, relaxed = retrieve(con, q, strategy="strict"), retrieve(con, q, strategy="relaxed")
        self.assertEqual(len(strict["passages"]), 1)
        self.assertGreater(len(relaxed["passages"]), len(strict["passages"]))  # observed: 5 passages + a spurious conflict
        self.assertEqual(relaxed["status"], "CONFLICT_UNRESOLVED")


if __name__ == "__main__":
    unittest.main()

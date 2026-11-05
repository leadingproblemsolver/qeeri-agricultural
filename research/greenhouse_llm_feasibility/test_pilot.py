"""Tests for the greenhouse LLM feasibility pilot artifacts (stdlib unittest).

Run from this directory:  python -m unittest -v test_pilot
The fake HTTP server below only proves the runner's plumbing. Its canned text is written
to a temp dir and is never a pilot result.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest import mock

import run_pilot
import score_rubric

HERE = Path(__file__).resolve().parent
LEDGER = json.loads((HERE / "evidence_ledger.json").read_text(encoding="utf-8"))
CASE = json.loads((HERE / "case_P0.json").read_text(encoding="utf-8"))
COVER = json.loads((HERE / "subsystem_coverage.json").read_text(encoding="utf-8"))
PROMPT = (HERE / "prompt_A.txt").read_text(encoding="utf-8")
PROTOCOL = (HERE / "PROTOCOL_V0.md").read_text(encoding="utf-8")

STATUSES = {"SOURCE_TEXT_READ", "UNVERIFIED_ABSTRACT_ONLY", "UNVERIFIED_NOT_LOCATED"}
CLASSES = {"OBSERVED", "MODELED", "INFERRED", "SOURCE-REPORTED", "SYNTHETIC"}


class LedgerTests(unittest.TestCase):
    def test_ten_claims_with_unique_ids(self):
        ids = [c["claim_id"] for c in LEDGER["claims"]]
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(set(ids)), 10)

    def test_every_claim_has_required_fields(self):
        sources = {s["source_id"] for s in LEDGER["sources"]}
        for c in LEDGER["claims"]:
            for f in ("source_id", "claim", "values", "locator", "status", "evidence_class", "scope",
                      "applicability", "limitations", "human_verified", "subsystems"):
                self.assertIn(f, c, f"{c['claim_id']} missing {f}")
            self.assertIn(c["source_id"], sources)
            self.assertIn(c["status"], STATUSES)
            self.assertIn(c["evidence_class"], CLASSES)
            self.assertTrue(c["values"], c["claim_id"])
            for v in c["values"]:
                self.assertTrue(v.get("unit"), f"{c['claim_id']} value without unit")
            self.assertTrue(c["limitations"].strip())

    def test_nothing_is_marked_human_verified(self):
        self.assertTrue(all(c["human_verified"] is False for c in LEDGER["claims"]))

    def test_excerpts_under_fifteen_words(self):
        for c in LEDGER["claims"]:
            if c["excerpt_relayed"]:
                self.assertLess(len(c["excerpt_relayed"].split()), 15, c["claim_id"])

    def test_read_claims_have_section_page_and_excerpt(self):
        for c in LEDGER["claims"]:
            if c["status"] == "SOURCE_TEXT_READ":
                self.assertTrue(c["locator"]["section"], c["claim_id"])
                self.assertTrue(c["locator"]["page"], c["claim_id"])
                self.assertTrue(c["excerpt_relayed"], c["claim_id"])

    def test_claim_status_matches_source_status(self):
        src = {s["source_id"]: s["status"] for s in LEDGER["sources"]}
        for c in LEDGER["claims"]:
            self.assertEqual(c["status"], src[c["source_id"]], c["claim_id"])

    def test_abstract_only_claims_have_no_page_locator(self):
        for c in LEDGER["claims"]:
            if c["status"] == "UNVERIFIED_ABSTRACT_ONLY":
                self.assertEqual(c["locator"]["section"], "Abstract")
                self.assertIsNone(c["locator"]["page"])

    def test_unlocated_source_has_no_claims(self):
        unlocated = {s["source_id"] for s in LEDGER["sources"] if s["status"] == "UNVERIFIED_NOT_LOCATED"}
        self.assertEqual(unlocated, {"S3_NEXUS_2026_CPI"})
        self.assertFalse([c for c in LEDGER["claims"] if c["source_id"] in unlocated])

    def test_every_protocol_source_is_accounted_for(self):
        self.assertEqual(len(LEDGER["sources"]), 7)


class ArithmeticCrossChecks(unittest.TestCase):
    """Independent recomputation of figures relayed by the fetch tool."""

    def test_tsafaras_cooling_water_reduction_matches_stated_42_percent(self):
        self.assertEqual(round((5463 - 3190) / 5463 * 100), 42)

    def test_tsafaras_cooling_share_matches_stated_72_percent(self):
        self.assertEqual(round(3190 / 4435 * 100), 72)

    def test_tsafaras_total_water_decomposition(self):
        self.assertAlmostEqual(1246 + 3190, 4435, delta=2)
        self.assertEqual(980 + 5463, 6443)

    def test_tsafaras_fan_capacity_basis_is_ground_area(self):
        total = 6 * 15000
        self.assertEqual(total / (40 * 12), 187.5)
        self.assertAlmostEqual(total / 432, 208.33, places=2)

    def test_fao_ventilation_statement_is_internally_inconsistent(self):
        ach = 0.06 * 3600 / 3
        self.assertEqual(ach, 72.0)
        self.assertNotEqual(round(ach), 60)

    def test_riyadh_irrigation_vs_fao_net_requirement_ratio(self):
        self.assertAlmostEqual(1246 / 276, 4.5, delta=0.1)
        self.assertAlmostEqual(1246 / 177, 7.0, delta=0.1)


class CaseAndCoverageTests(unittest.TestCase):
    def test_case_is_provisional_with_unconfirmed_goal(self):
        self.assertEqual(CASE["status"], "PROVISIONAL")
        self.assertEqual(CASE["goal"]["status"], "UNCONFIRMED")
        self.assertEqual(CASE["case_id"], "QAT-ALSHAHANIYA-TOMATO-SEMICLOSED-P0")

    def test_no_missing_engineering_input_has_a_value(self):
        self.assertGreaterEqual(len(CASE["missing_engineering_inputs"]), 10)
        for m in CASE["missing_engineering_inputs"]:
            self.assertIsNone(m["value"], m["input"])

    def test_unconfirmed_anchor_attributes_stay_unverified(self):
        by = {a["attribute"]: a["status"] for a in CASE["anchor_attributes"]}
        for needle in ("Al-Shahaniya", "Venlo", "tomato", "4-mm"):
            attr = next(k for k in by if needle in k)
            self.assertEqual(by[attr], "UNVERIFIED", attr)

    def test_all_twelve_prompt_subsystems_are_mapped(self):
        phrases = {
            "user_site_intake": "user/site intake",
            "crop_cultivation_system": "crop/cultivation system",
            "structure_cover": "structure/cover",
            "thermal_cooling_design": "thermal/cooling design",
            "water_irrigation_fertigation": "water and irrigation/fertigation",
            "electricity_power_safety": "electricity and power safety",
            "sensors_monitoring_control": "sensors and monitoring/control",
            "bom_procurement": "BOM and procurement categories",
            "installation_dependencies": "installation dependencies",
            "commissioning": "commissioning",
            "operating_checks": "operating checks",
            "economic_screening": "economic screening",
        }
        ids = [s["id"] for s in COVER["subsystems"]]
        self.assertEqual(sorted(ids), sorted(phrases))
        for sid, phrase in phrases.items():
            self.assertIn(phrase, PROMPT, sid)

    def test_coverage_references_resolve_and_are_consistent(self):
        claims = {c["claim_id"]: c for c in LEDGER["claims"]}
        for s in COVER["subsystems"]:
            self.assertIn(s["coverage"], {"NONE", "PARTIAL"})  # nothing is FULL
            self.assertEqual(s["coverage"] == "NONE", not s["claims"], s["id"])
            for cid in s["claims"]:
                self.assertIn(s["id"], claims[cid]["subsystems"], f"{cid} not tagged {s['id']}")
        for cid, c in claims.items():
            for sid in c["subsystems"]:
                sub = next(s for s in COVER["subsystems"] if s["id"] == sid)
                self.assertIn(cid, sub["claims"])


class FrozenPromptTests(unittest.TestCase):
    def test_prompt_is_verbatim_from_protocol(self):
        section = PROTOCOL.split("## Prompt A: fixed test input\n")[1].split("\n## Arms")[0].strip()
        self.assertEqual(PROMPT.strip(), section)

    def test_packet_contains_only_source_text_read_claims(self):
        packet, included = run_pilot.build_packet(LEDGER)
        self.assertEqual(included, ["L06", "L07", "L08", "L09", "L10"])
        for cid in ("L01", "L02", "L03", "L04", "L05"):
            self.assertNotIn(f"[{cid}]", packet)
        self.assertNotIn("limitations", packet.lower().split("statement:")[0])

    def test_arms_differ_only_by_packet(self):
        packet, _ = run_pilot.build_packet(LEDGER)
        msgs = run_pilot.arm_messages(PROMPT, packet)
        self.assertTrue(msgs["B"].startswith(msgs["A"]))
        self.assertEqual(msgs["B"][len(msgs["A"]):], "\n" + packet)

    def test_request_has_no_tools(self):
        body = run_pilot.build_request("m", "x", 100, 0.0)
        self.assertNotIn("tools", body)


class _Handler(BaseHTTPRequestHandler):
    seen = []

    def do_POST(self):
        n = int(self.headers["Content-Length"])
        _Handler.seen.append((dict(self.headers), json.loads(self.rfile.read(n))))
        payload = json.dumps({
            "id": "msg_test", "type": "message", "model": "fake-model-for-plumbing-test",
            "content": [{"type": "text", "text": "PLUMBING TEST TEXT"}],
            "stop_reason": "end_turn", "usage": {"input_tokens": 1, "output_tokens": 1},
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("request-id", "req_test")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *a):
        pass


class RunnerTests(unittest.TestCase):
    def test_without_key_both_arms_not_executed_and_nothing_fabricated(self):
        env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
        with tempfile.TemporaryDirectory() as d:
            r = subprocess.run([sys.executable, str(HERE / "run_pilot.py"), "execute", "--out", d],
                               env=env, capture_output=True, text=True)
            self.assertEqual(r.returncode, 2, r.stderr)
            for arm in ("A", "B"):
                rec = json.loads((Path(d) / f"ARM_{arm}_RUN.json").read_text())
                self.assertEqual(rec["status"], "NOT_EXECUTED")
                self.assertIsNone(rec["output_file"])
                self.assertIsNone(rec["executed_utc"])
                self.assertFalse((Path(d) / f"ARM_{arm}_output.txt").exists())
            self.assertTrue((Path(d) / "FROZEN_INPUTS.json").exists())

    def test_with_key_preserves_raw_output_settings_and_blinds(self):
        _Handler.seen = []
        srv = HTTPServer(("127.0.0.1", 0), _Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            url = f"http://127.0.0.1:{srv.server_port}/v1/messages"
            with tempfile.TemporaryDirectory() as d, mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key-not-real"}):
                rc = run_pilot.main(["execute", "--out", d, "--api-url", url, "--model", "m-test", "--max-tokens", "123"])
                self.assertEqual(rc, 0)
                out = Path(d)
                for arm in ("A", "B"):
                    rec = json.loads((out / f"ARM_{arm}_RUN.json").read_text())
                    self.assertEqual(rec["status"], "EXECUTED")
                    self.assertEqual(rec["settings"]["model"], "m-test")
                    self.assertEqual(rec["settings"]["max_tokens"], 123)
                    raw = (out / rec["raw_response_file"]).read_text()
                    self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(), rec["raw_response_sha256"])
                    self.assertEqual((out / rec["output_file"]).read_text(), "PLUMBING TEST TEXT")
                key_map = json.loads((out / "blind_key.json").read_text())["label_to_arm"]
                self.assertEqual(sorted(key_map.values()), ["A", "B"])
                self.assertTrue((out / "blind" / "X.txt").exists() and (out / "blind" / "Y.txt").exists())
                for f in out.rglob("*"):
                    if f.is_file():
                        self.assertNotIn("test-key-not-real", f.read_text())
            (hdr_a, body_a), (hdr_b, body_b) = _Handler.seen
            self.assertEqual({k.lower(): v for k, v in hdr_a.items()}["x-api-key"], "test-key-not-real")
            self.assertNotIn("APPROVED SOURCE PASSAGES", body_a["messages"][0]["content"])
            self.assertIn("[L06]", body_b["messages"][0]["content"])
            for k in ("model", "max_tokens", "temperature"):
                self.assertEqual(body_a[k], body_b[k])
            self.assertNotIn("tools", body_a)
        finally:
            srv.shutdown()
            srv.server_close()


class ScorerTests(unittest.TestCase):
    def test_weights_sum_to_one(self):
        self.assertAlmostEqual(sum(score_rubric.WEIGHTS.values()), 1.0)

    def test_critical_gate_overrides_a_perfect_average(self):
        checks = [{"id": f"c{i}", "dimension": d, "result": "PASS", "severity": "minor"}
                  for i, d in enumerate(score_rubric.WEIGHTS)]
        checks.append({"id": "elec", "dimension": "qatar_applicability_safety", "result": "FAIL",
                       "severity": "critical", "gate": "electrical_safety"})
        r = score_rubric.score_checks(checks)
        self.assertEqual(r["gate_failures"], ["elec"])
        self.assertTrue(r["verdict"].startswith("NOT_INSTALLATION_READY"))

    def test_gate_tag_alone_triggers_even_if_severity_understated(self):
        r = score_rubric.score_checks([{"id": "f", "dimension": "evidence_attribution", "result": "FAIL",
                                        "severity": "major", "gate": "fabricated_source"}])
        self.assertEqual(r["gate_failures"], ["f"])

    def test_not_assessable_is_excluded_not_counted_as_pass(self):
        r = score_rubric.score_checks([
            {"id": "a", "dimension": "completeness", "result": "PASS", "severity": "minor"},
            {"id": "b", "dimension": "completeness", "result": "FAIL", "severity": "minor"},
            {"id": "c", "dimension": "physics_correctness", "result": "NOT_ASSESSABLE", "severity": "minor"},
        ])
        self.assertEqual(r["dimensions"]["completeness"]["fraction_pass"], 0.5)
        self.assertIsNone(r["dimensions"]["physics_correctness"]["fraction_pass"])
        self.assertEqual(r["weight_assessed"], 0.15)

    def test_unexecuted_arms_are_never_scored(self):
        with tempfile.TemporaryDirectory() as d:
            for arm in ("A", "B"):
                (Path(d) / f"ARM_{arm}_RUN.json").write_text(json.dumps({"arm": arm, "status": "NOT_EXECUTED"}))
            res = score_rubric.score_runs(d)
            for arm in ("A", "B"):
                self.assertEqual(res["arms"][arm]["status"], "NOT_EXECUTED")
                self.assertTrue(res["arms"][arm]["verdict"].startswith("NOT_SCORED"))
                self.assertNotIn("weighted_score_over_assessed_dimensions", res["arms"][arm])


if __name__ == "__main__":
    unittest.main()

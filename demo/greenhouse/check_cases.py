#!/usr/bin/env python3
"""Run ten demo checks. A PASS is NOT proof that a scientific source is correct.

Usage: python demo/greenhouse/check_cases.py
Optional: python demo/greenhouse/check_cases.py --register /path/to/master_source_register.yaml
The optional source-register comparison requires: pip install pyyaml
"""
import argparse
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(path, register_path=None):
    doc = json.loads(path.read_text(encoding="utf-8"))  # JSON is valid YAML 1.2
    assert doc["status"] == "DEMONSTRATION_ONLY_PENDING_ORIGINAL_SOURCE_REVIEW"
    cases = doc["cases"]
    assert len(cases) == 10, "expected ten cases"
    ids, sources = set(), doc["sources"]
    register = None
    if register_path is not None:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("Install PyYAML for --register: pip install pyyaml") from exc
        register = yaml.safe_load(register_path.read_text(encoding="utf-8"))
    passed = failed = 0
    for case in cases:
        cid = case.get("id", "UNKNOWN")
        try:
            assert set(doc["required_fields"]) <= set(case), "missing required fields"
            assert cid not in ids, "duplicate ID"
            ids.add(cid)
            assert case["review"] == "PENDING", "unapproved evidence cannot be approved"
            assert case["source_id"] in sources, "unknown source"
            assert case["data_class"] not in {"HUMAN_VERIFIED", "MEASURED_QATAR_SITE"}
            x, e, kind = case["inputs"], case["expected"], case["check"]
            if kind == "pad_equation":
                db, wb, eff = x["dry_bulb_c"], x["wet_bulb_c"], x["pad_effectiveness"]
                assert wb <= db and 0 <= eff <= 1
                assert math.isclose(db - eff * (db - wb), e["pad_outlet_c"], abs_tol=1e-8)
                assert e["canopy_temperature_c"] is None, "pad outlet is not canopy air"
            elif kind == "scope":
                assert case["scope"] == "AL_KHOR_ONLY"
                assert e["allow_al_shahaniya_transfer"] is False
                assert all(0 <= v <= 100 for k, v in x.items() if "humidity_pct" in k)
            elif kind == "ventilation_quote":
                assert case["data_class"] == "MODELED_CFD_REPORTED"
                assert (x["ach"], e["reported_difference_c"]) in ((20, 10), (40, 5.5))
            elif kind == "reported_row":
                assert case["scope"] == "QATAR_STUDY_ONLY"
                assert case["locator"] == "Tables 14–15"
                assert x["system"] in ("OF Tomato", "GH-S Cooled Tomato", "GH-SL Cooled Tomato")
                assert all(isinstance(e[k], (int, float)) and not isinstance(e[k], bool) and e[k] > 0
                           for k in ("yield_t_per_dunum", "total_cost_qar", "electricity_kwh", "water_m3"))
            elif kind == "historical_code":
                assert case["scope"] == "QATAR_HISTORICAL_CODE"
                assert e["minimum_power_factor_lagging"] == 0.9
                assert e["current_revision_checked"] is False
            elif kind == "abstain":
                assert case["locator"] is None
                assert e["decision"] == "ABSTAIN_MISSING_SOURCE"
            else:
                raise AssertionError("unknown check type")
            if register is not None:
                aliases = {
                    "ghani_2019": "ghani_2019_evaporative_cooled_greenhouse",
                    "shannak_2026": "shannak_2026_qatari_crop_performance_index",
                    "kahramaa_2016": "kahramaa_lv_electrical_code",
                    "mahmood_2022": "mahmood_2022_al_shahaniya"
                }
                sid = aliases.get(case["source_id"], case["source_id"])
                groups = ("verified_sources", "conditional_sources", "regulatory_sources")
                found = [register[group][sid] for group in groups if sid in register.get(group, {})]
                assert len(found) == 1, "source missing from local register"
                passages = found[0].get("verified_passages") or []
                if kind == "abstain":
                    assert not passages, "reassess abstention; source changed"
                else:
                    passage_ids = {
                        "D01": "ae069_p2_system_efficiency",
                        "D02": "ghani_boundary_conditions_p9",
                        "D03": "ghani_boundary_conditions_p9",
                        "D04": "ghani_ventilation_ach_p15",
                        "D05": "ghani_ventilation_ach_p15",
                        "D06": "shannak_table_14_15_operational_data",
                        "D07": "shannak_table_14_15_operational_data",
                        "D08": "shannak_table_14_15_operational_data",
                        "D09": "kahramaa_power_factor_p67"
                    }
                    matched = [p for p in passages if p.get("passage_id") == passage_ids.get(cid)]
                    assert len(matched) == 1, "case has no matching source passage ID"
                    quote = " ".join(matched[0].get("quote", "").split())
                    assert quote, "matching source excerpt is empty"
                    if kind == "reported_row":
                        marker = x["system"] + ":"
                        assert marker in quote, "study row missing from passage"
                        row = quote.split(marker, 1)[1].split(". ", 1)[0]
                        for key in ("yield_t_per_dunum", "total_cost_qar", "electricity_kwh", "water_m3"):
                            value = e[key]
                            number = str(int(value)) if float(value).is_integer() else str(value)
                            assert re.search(r"(?<![\d.])" + re.escape(number) + r"(?![\d.])", row), (
                                "reported row conflicts with source register: " + key
                            )
                    if kind == "ventilation_quote":
                        for value in (x["ach"], e["reported_difference_c"]):
                            number = str(int(value)) if float(value).is_integer() else str(value)
                            assert re.search(r"(?<![\d.])" + re.escape(number) + r"(?![\d.])", quote), (
                                "CFD value missing from source register"
                            )
                    if kind == "historical_code":
                        assert "power factor" in quote.lower() and "0.9" in quote
                # A register match does NOT independently authenticate the publication.
            print(f"PASS {cid}: {case['title']}")
            passed += 1
        except (AssertionError, KeyError, ValueError, TypeError) as error:
            print(f"FAIL {cid}: {error}")
            failed += 1
    print(f"Demo: {passed} PASS, {failed} FAIL")
    print("NOT TESTED: original paper accuracy, field performance, human review, or AI model improvement.")
    return 1 if failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=HERE / "cases.yaml")
    parser.add_argument("--register", type=Path)
    options = parser.parse_args()
    raise SystemExit(run(options.cases, options.register))

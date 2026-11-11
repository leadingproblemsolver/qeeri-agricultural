#!/usr/bin/env python3
"""Run 10 small demo-contract checks. NOT scientific or field validation.

cases.yaml uses JSON syntax, which is also valid YAML. No extra packages needed.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "cases.yaml").read_text(encoding="utf-8"))
cases = data["cases"]
assert len(cases) == 10, "Expected exactly 10 demonstration cases"

def check(case):
    x, expected = case["inputs"], case["expected"]
    kind = case["kind"]
    if kind == "pad":
        assert x["wet_bulb_c"] <= x["dry_bulb_c"]
        assert 0 <= x["effectiveness"] <= 1
        outlet = x["dry_bulb_c"] - x["effectiveness"] * (x["dry_bulb_c"] - x["wet_bulb_c"])
        assert math.isclose(outlet, expected["outlet_c"], abs_tol=1e-9)
    elif kind == "abstain_canopy":
        assert x["canopy_sensor_c"] is None
        assert expected["decision"] == "INSUFFICIENT_INFORMATION"
    elif kind == "bad_weather":
        assert x["wet_bulb_c"] > x["dry_bulb_c"]
        assert expected["decision"] == "INVALID_INPUT"
    elif kind == "scope":
        assert x["study_site"] != x["requested_site"]
        assert expected["decision"] == "NOT_SITE_MEASUREMENT"
    elif kind == "reported_delta":
        # Fixture consistency only: original study must still be checked.
        reference_values = {20: 10.0, 40: 5.5}
        assert expected["temperature_difference_c"] == reference_values[x["air_changes_per_hour"]]
    elif kind == "crop_row":
        # Transcription check against the supplied working source-register values.
        reference_values = {
            "OF Tomato": (5.3, 7942, 1702, 1000),
            "GH-S Cooled Tomato": (10.4, 18232, 15000, 2000),
            "GH-SL Cooled Tomato": (16, 27911, 27160, 1500),
        }
        observed = (
            expected["yield_t_dunum"], expected["cost_qar"],
            expected["electricity_kwh"], expected["water_m3"],
        )
        assert observed == reference_values[x["system"]]
    elif kind == "missing_source":
        assert x["required_passage"] == "design_conditions"
        assert expected["decision"] == "REFERENCE_NOT_VERIFIED"
    else:
        raise AssertionError("Unknown check kind: " + kind)
    assert case["source"] and case["input_type"]
    assert case["id"] and case["title"]

if __name__ == "__main__":
    passed = 0
    for case in cases:
        try:
            check(case)
        except (AssertionError, KeyError, ValueError, TypeError) as exc:
            print(f"FAIL {case['id']}: {case['title']} — {exc}")
        else:
            passed += 1
            print(f"PASS {case['id']}: {case['title']}")
    print(f"\n{passed}/{len(cases)} demo checks passed")
    print("This does not verify original scientific papers, field performance,")
    print("independent review or improvement in AI answers.")
    raise SystemExit(0 if passed == len(cases) else 1)

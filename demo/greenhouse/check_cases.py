#!/usr/bin/env python3
"""Run ten demo input/logic checks. This does NOT verify original scientific papers."""
import json
import math
from pathlib import Path

# JSON is valid YAML 1.2; cases.yaml uses that subset to avoid a YAML dependency.
cases = json.loads((Path(__file__).parent / "cases.yaml").read_text())
assert cases["status"] == "DEMONSTRATION_ONLY_PENDING_ORIGINAL_SOURCE_REVIEW"
assert len(cases["cases"]) == 10
ids = set()
for item in cases["cases"]:
    assert set(cases["required_fields"]) <= set(item), item.get("id")
    assert item["id"] not in ids
    ids.add(item["id"])
    assert item["review"] == "PENDING"
    assert item["source_id"] in cases["sources"]
    x, expected = item["inputs"], item["expected"]
    method = item["check"]
    if method == "pad_equation":
        assert x["wet_bulb_c"] <= x["dry_bulb_c"]
        assert 0 <= x["pad_effectiveness"] <= 1
        actual = x["dry_bulb_c"] - x["pad_effectiveness"] * (x["dry_bulb_c"] - x["wet_bulb_c"])
        assert math.isclose(actual, expected["pad_outlet_c"], abs_tol=1e-9)
        assert expected["canopy_temperature_c"] is None
    elif method == "scope":
        assert item["scope"] == "AL_KHOR_ONLY"
        assert expected["allow_al_shahaniya_transfer"] is False
        if "relative_humidity_pct" in " ".join(x):
            for k, v in x.items():
                if "humidity_pct" in k:
                    assert 0 <= v <= 100
    elif method == "ventilation_quote":
        # Expected values transcribed from a named study, not independently confirmed.
        assert item["data_class"] == "MODELED_CFD_REPORTED"
        assert (x["ach"], expected["reported_difference_c"]) in ((20, 10), (40, 5.5))
    elif method == "reported_row":
        assert item["scope"] == "QATAR_STUDY_ONLY"
        assert item["locator"] == "Tables 14–15"
        assert all(expected[k] > 0 for k in (
            "yield_t_per_dunum", "total_cost_qar", "electricity_kwh", "water_m3"
        ))
        assert "CROP_ZONE_MEASUREMENT" not in item["data_class"]
    elif method == "historical_code":
        assert expected["minimum_power_factor_lagging"] == 0.9
        assert expected["current_revision_checked"] is False
    elif method == "abstain":
        assert item["locator"] is None
        assert expected["decision"] == "ABSTAIN_MISSING_SOURCE"
    else:
        raise AssertionError(f"Unrecognized check: {method}")
    print(f"PASS {item['id']}: {item['title']}")

print("RESULT: 10/10 demo contract checks passed; original-source verification,")
print("expert review, site measurements and controlled AI comparisons NOT EXECUTED.")

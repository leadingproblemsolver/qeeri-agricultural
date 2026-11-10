"""Synthetic pad-outlet check only. NOT greenhouse or crop-safety validation."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def assess(s):
    db, wb, eta = (s[k] for k in ("dry_bulb_C", "wet_bulb_C", "effectiveness_fraction"))
    if not all(isinstance(v, (float, int)) and not isinstance(v, bool) for v in (db, wb, eta)):
        raise ValueError("Expected numeric temperature and effectiveness inputs")
    if not (-50 <= wb <= db <= 70):
        raise ValueError("Wet-bulb must be <= dry-bulb; both must be within example bounds")
    if not (0 <= eta <= 1):
        raise ValueError("Effectiveness must be a fraction in [0,1]")
    if s.get("input_kind") != "HYPOTHETICAL_NOT_SITE_MEASURED":
        raise ValueError("Synthetic scenarios only; no unverified telemetry promoted")
    pad_out = round(db - eta * (db - wb), 3)
    return {
        "scenario_id": s["id"],
        "input_evidence_state": s["input_kind"],
        "pad_outlet_temperature_C": pad_out,
        "pad_outlet_at_or_below_example_target": pad_out <= s["target_pad_exit_C"],
        "wet_bulb_lower_bound_C": wb,
        "crop_zone_temperature_C": None,
        "crop_safety_status": "NOT_ASSESSABLE",
        "construction_ready": False,
        "scientific_evidence_status": "MODEL_BASED_CALCULATION_ON_SYNTHETIC_INPUTS",
        "reason": "Pad exit is not crop-zone temperature; environmental and equipment validation inputs missing."
    }

def main():
    case = json.loads((ROOT / "case.json").read_text(encoding="utf-8"))
    output = {"case_id": case["case_id"], "results": [assess(s) for s in case["scenarios"]],
              "weather_record_used": False, "review_state": case["review"]["state"],
              "missing_for_crop_zone_decision": case["missing_for_crop_zone_decision"]}
    (ROOT / "results.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run ten source-linked greenhouse demo checks from one YAML file.

Install: pip install pyyaml
Run: python demo/greenhouse/run_demo.py
PASS proves only internal data-contract consistency, not scientific truth.
"""
import argparse
import math
import re
from pathlib import Path

import yaml


class InvalidEvidence(Exception):
    pass


def require(ok, why):
    if not ok:
        raise InvalidEvidence(why)


def has_number(text, number):
    variants = {str(number)}
    if float(number).is_integer():
        variants.update((str(int(number)), format(int(number), ",")))
    return any(re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d.])", text) for v in variants)


def passage(source, passage_id):
    for p in source.get("verified_passages") or []:
        if p.get("passage_id") == passage_id or p.get("locator") == passage_id:
            return p
    return None


def check(case, sources):
    sid, cid = case["source_id"], case["id"]
    require(sid in sources, "source not in evidence file")
    s = sources[sid]
    require(s.get("bucket") != "quarantined_sources", "quarantined source cannot be used")
    require(case["independent_scientific_review"] == "PENDING", "human review must remain pending")
    x, expected, kind = case["inputs"], case["expected"], case["check"]
    p = passage(s, case["source_locator"])
    quote = (p or {}).get("quote", "")
    if kind == "abstain_missing_source":
        require(not p and not (s.get("verified_passages") or []), "new passage found: review abstention")
        require(expected["decision"] == "ABSTAIN_MISSING_VERIFIED_PASSAGE", "incorrect expected decision")
        return "ABSTAIN — no checked passage for an Al Shahaniya design value"
    require(bool(quote), "source excerpt or exact passage ID missing")
    if kind == "pad_equation":
        db, wb, eff = x["dry_bulb_c"], x["wet_bulb_c"], x["effectiveness"]
        require(wb <= db and 0 <= eff <= 1, "invalid cooling inputs")
        actual = db - eff * (db - wb)
        require(math.isclose(actual, expected["pad_outlet_c"], abs_tol=1e-9), "expected cooling value is wrong")
        return f"CALCULATED {actual:.1f} C at pad outlet; crop-zone temperature UNKNOWN"
    if kind == "study_scope":
        require("Al Khor" in s.get("jurisdiction", ""), "location mismatch")
        require(expected["admissibility"] == "AL_KHOR_REFERENCE_ONLY", "incorrect transfer permission")
        for k, v in x.items():
            require(has_number(quote, v), f"{k}={v} absent from cited passage")
        return "SOURCE SCOPE — Al Khor only; not a measured Al Shahaniya result"
    if kind == "reported_value":
        ach, delta = x["ventilation_air_changes_per_hour"], expected["reported_temperature_difference_c"]
        require(case["evidence_class"] == "modeled_cfd", "CFD result must be labeled modeled")
        require(has_number(quote, ach) and has_number(quote, delta), "CFD values absent from cited passage")
        return f"REPORTED SIMULATION — {ach} ACH corresponds to {delta:g} C air difference"
    if kind == "published_row":
        label = x["system"] + ":"
        require(label in quote, "system row missing")
        row = quote.split(label, 1)[1].split(". ", 1)[0]
        for key, number in expected.items():
            require(has_number(row, number), f"{key}={number} absent from row")
        return (f"REPORTED STUDY — {x['system']}: "
                f"{expected['yield_t_per_dunum']:g} t/dunum yield, "
                f"{expected['total_cost_qar_per_dunum']} QAR/dunum cost")
    if kind == "regulatory_scope":
        require(s.get("jurisdiction") == "Qatar", "wrong legal jurisdiction")
        require("power factor" in quote.lower() and has_number(quote, 0.9), "power-factor passage mismatch")
        require(expected["current_code_revision_review"] == "REQUIRED", "current code review missing")
        return "HISTORICAL CODE — minimum 0.90 lagging; current revision NOT CHECKED"
    raise InvalidEvidence(f"unknown test type: {kind}")


def run(path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "evidence root must be a mapping")
    sources, cases = data.get("sources"), data.get("demo_cases")
    require(isinstance(sources, dict) and isinstance(cases, list), "sources and demo_cases required")
    require(bool(data.get("provenance_warning")), "missing source-provenance warning")
    require(data.get("model_comparison", {}).get("status") == "NOT_EXECUTED",
            "unexecuted AI comparison must not be reported as complete")
    require(len(cases) == 10, "expected exactly ten cases")
    ids = [c["id"] for c in cases]
    require(len(set(ids)) == len(ids), "duplicate case IDs")
    count = 0
    for case in cases:
        try:
            value = check(case, sources)
            print(f"PASS {case['id']} — {value}")
            count += 1
        except (InvalidEvidence, KeyError, TypeError, ValueError) as exc:
            print(f"FAIL {case.get('id', '?')} — {exc}")
    print(f"\n{count}/10 demo checks passed. Independent publication review and AI A/B NOT EXECUTED.")
    return 0 if count == 10 else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path,
                        default=Path(__file__).with_name("qeeri_evidence.yaml"))
    args = parser.parse_args()
    raise SystemExit(run(args.evidence))

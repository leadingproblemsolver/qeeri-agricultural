"""Deterministic admissibility guards. Run BEFORE any generation and again on any generated output.

1. check_sizing_request: refuses equipment sizing / electrical / pump / emitter / water-volume requests and lists the
   inputs that would be needed. The system never performs sizing, even with every input supplied: there is no
   vetted calculator here and sign-off belongs to a qualified engineer.
2. validate_claims: a generated claim is SUPPORTED_CANDIDATE only if it cites retrieved chunk ids that resolve,
   every number it states appears in a cited chunk or in supplied inputs, it contains no sizing specification that
   is not in a cited chunk, and it carries no instruction-injection residue. A model cannot set its own status.
"""
import re

from .store import resolve_citation, scan_injection

# category -> (trigger regex, minimal curator-defined required inputs, sign-off role)
# Input names are a minimal checklist for the refusal message, not an exhaustive design basis.
SIZING_CATEGORIES = {
    "fan_ventilation_sizing": (
        r"\b(fan|fans|ventilation|exhaust|air\s*changes?|ach)\b",
        ["greenhouse_floor_area_m2", "greenhouse_volume_m3", "design_dry_bulb_c", "design_wet_bulb_c",
         "pad_saturation_effectiveness_fraction", "target_indoor_temperature_c", "design_solar_radiation_w_m2",
         "cover_transmittance_and_geometry"], "qualified greenhouse climate / HVAC engineer"),
    "cooling_power_sizing": (
        r"\b(kw|kilowatt|tons?\s+of\s+(cooling|refrigeration)|ac\s+unit|air[\s-]?condition\w*|chiller|cooling\s+(load|capacity|power))\b",
        ["greenhouse_floor_area_m2", "design_dry_bulb_c", "design_wet_bulb_c", "design_solar_radiation_w_m2",
         "cover_transmittance_and_geometry", "target_indoor_temperature_c"], "qualified greenhouse climate / HVAC engineer"),
    "electrical_specification": (
        r"\b(cable|breaker|mcb|rcd|fuse|wire\s*gauge|amperage|ampacity|transformer|earthing|supply\s+(cable|rating)|electrical\s+(load|specification|spec))\b",
        ["connected_load_list_kw", "supply_voltage_and_phase", "utility_connection_capacity_kva",
         "cable_route_length_m", "earthing_system", "authority_approved_design"],
        "KAHRAMAA-licensed electrical designer / contractor"),
    "pump_sizing": (
        r"\b(pump|pumps|pumping|head\s+loss|dynamic\s+head)\b",
        ["design_flow_m3_h", "total_dynamic_head_m", "water_source_pressure_and_quality", "pipe_network_layout"],
        "qualified irrigation / hydraulic engineer"),
    "irrigation_emitter_quantity": (
        r"\b(emitter|emitters|dripper|drippers|drip\s+line|nozzle|sprinkler)\b",
        ["crop_area_m2", "plant_density_per_m2", "substrate_type", "emitter_flow_l_h", "water_ec_ds_m",
         "leaching_fraction"], "qualified irrigation / fertigation specialist"),
    "water_volume": (
        r"\b(water\s+(volume|requirement|requirements|demand|budget|consumption)|litres?|liters?|m3\s+of\s+water)\b",
        ["growing_area_m2", "cultivation_period_dates", "measured_site_et_or_drain_data", "water_ec_ds_m",
         "pad_cooling_operating_hours"], "qualified irrigation / water-resources specialist"),
}
_SIZING_WORDS = re.compile(r"\b(size|sizing|sized|specify|specification|spec|rating|rated|how\s+many|how\s+much|"
                           r"what\s+size|capacity|required|requirement|need\s+for|design\s+(my|our|the)|"
                           r"calculate|select|choose|install)\b", re.IGNORECASE)
_SITE_WORDS = re.compile(r"\b(my|our)\s+(greenhouse|farm|site|project|plant)|\bfor\s+(a|an|the)\s+\d+\s*(m2|m²|ha|hectare)",
                         re.IGNORECASE)
# A question that only asks what a named source says is a reporting question, not a sizing request.
_REPORT_WORDS = re.compile(r"\b(does|do|did)\s+\w+\s+(suggest|say|state|report|recommend|require|give|list)\b|"
                           r"\bwhat\s+(does|did)\s+\w+\s+(suggest|say|state|report|recommend|require|give|list)\b|"
                           r"\baccording\s+to\b", re.IGNORECASE)


def check_sizing_request(question, inputs=None):
    """Return None if not a sizing request, else a refusal dict (always a refusal; never a calculation)."""
    inputs = inputs or {}
    hits = []
    for cat, (pat, required, role) in SIZING_CATEGORIES.items():
        if re.search(pat, question, re.IGNORECASE):
            hits.append((cat, required, role))
    if not hits:
        return None
    wants_spec = bool(_SIZING_WORDS.search(question) or _SITE_WORDS.search(question))
    if not wants_spec or (_REPORT_WORDS.search(question) and not _SITE_WORDS.search(question)
                          and not re.search(r"\b(size|sizing|specify|how\s+many)\b", question, re.IGNORECASE)):
        return None
    out = []
    for cat, required, role in hits:
        missing = [k for k in required if inputs.get(k) in (None, "", [])]
        out.append({"category": cat, "required_inputs": required,
                    "supplied_inputs": [k for k in required if k not in missing], "missing_inputs": missing,
                    "sign_off": role})
    return {"refused": True, "reason": "SIZING_OR_SPECIFICATION_REQUEST_NOT_PERFORMED",
            "explanation": ("This system does not size equipment or give electrical, pump, emitter or water-volume "
                            "specifications. Even with all inputs supplied, such outputs need a qualified "
                            "engineer's calculation and sign-off. Sourced ranges may be quoted as reference only."),
            "categories": out,
            "missing_inputs": sorted({m for c in out for m in c["missing_inputs"]})}


_NUM = re.compile(r"(?<![\w.])(?<![A-Za-z]-)\d+(?:[.,]\d+)?")
_SIZING_OUTPUT = re.compile(
    r"\b(?P<n1>\d+(?:[.,]\d+)?)\s*(?P<u1>kw|kva|a\b|amps?|mm2|mm\u00b2|hp|m3\s*/\s*h|l\s*/\s*h|l/min|bar|rpm|v\b)|"
    r"\b(?P<n2>\d+)\s+(?P<u2>fans?|pumps?|emitters?|drippers?|breakers?)\b", re.IGNORECASE)


def _norm_num(n):
    n = n.replace(",", ".")
    return n.rstrip("0").rstrip(".") if "." in n else n


def _numbers(text):
    return {_norm_num(n) for n in _NUM.findall(text or "")}


def validate_claims(con, claims, retrieved_passages, inputs=None):
    """claims: [{text, chunk_ids}] from a provider. Returns claims with status + reasons (never trust a model status)."""
    allowed = {p["chunk_id"]: p for p in retrieved_passages}
    supplied_nums = _numbers(" ".join(str(v) for v in (inputs or {}).values()))
    out = []
    for c in claims:
        text = str(c.get("text", ""))
        ids = c.get("chunk_ids") or []
        reasons = []
        if not text.strip():
            reasons.append("EMPTY_CLAIM")
        if not ids:
            reasons.append("NO_CITATION")
        cited = []
        for cid in ids:
            if cid not in allowed:
                reasons.append(f"CITED_CHUNK_NOT_IN_RETRIEVED_SET:{cid}")
                continue
            res = resolve_citation(con, {"chunk_id": cid, "source_id": allowed[cid]["source_id"],
                                         "chunk_hash": allowed[cid]["chunk_hash"]})
            if not res["resolved"]:
                reasons.append(f"CITATION_DOES_NOT_RESOLVE:{res['reason']}")
            else:
                cited.append(allowed[cid])
        chunk_nums = _numbers(" ".join(p["text"] for p in cited))
        extra = sorted(n for n in _numbers(text) if n not in chunk_nums and n not in supplied_nums)
        if extra:
            reasons.append("NUMBERS_NOT_IN_CITED_PASSAGES_OR_INPUTS:" + ",".join(extra))
        chunk_text = " ".join(p["text"] for p in cited).lower().replace(" ", "")
        for m in _SIZING_OUTPUT.finditer(text):
            num = _norm_num(m.group("n1") or m.group("n2"))
            unit = (m.group("u1") or m.group("u2")).lower().replace(" ", "")
            # a sizing figure is admissible only as a restatement: its number AND its unit/equipment word occur in a cited chunk
            if num not in chunk_nums or unit.rstrip("s") not in chunk_text:
                reasons.append(f"UNSUPPORTED_SIZING_SPECIFICATION:{m.group(0)}")
        inj = scan_injection(text)
        if inj:
            reasons.append(f"INSTRUCTION_INJECTION_RESIDUE:{inj}")
        out.append({"text": text, "chunk_ids": ids, "status": "UNSUPPORTED" if reasons else "SUPPORTED_CANDIDATE",
                    "failure_reasons": reasons})
    return out

"""Pre-ingestion evidence gate for QEERI greenhouse packet candidates.

This is a completeness/consistency gate, NEVER proof of measured truth.
No third-party dependencies; does not contact network services.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
HEX64 = re.compile(r"^[a-f0-9]{64}$")
MANDATORY = ("site_id", "sensor_id", "observed_at_utc", "quantity",
             "value", "units", "source_file_sha256", "source_file_reference",
             "measurement_method", "calibration_record", "custodian_permission",
             "independent_reviewer_record")


def assess(packet):
    """Return a decision and exact missing proof. Model-generated JSON is not telemetry."""
    reasons = []
    if not isinstance(packet, dict):
        return {"decision": "REJECT_INVALID_PACKET", "reasons": ["packet must be JSON object"]}
    claimed = packet.get("telemetry_verification_status", "UNVERIFIED")
    if claimed == "VERIFIED_FIELD_READINGS":
        reasons.append("self-declared VERIFIED_FIELD_READINGS is not accepted as scientific verification")
    obs = packet.get("raw_observations")
    if not isinstance(obs, list) or not obs:
        reasons.append("missing nonempty raw_observations array; design specifications are not observations")
    else:
        for i, item in enumerate(obs):
            if not isinstance(item, dict):
                reasons.append(f"raw_observations[{i}] not an object")
                continue
            for k in MANDATORY:
                if k not in item or item[k] in (None, ""):
                    reasons.append(f"raw_observations[{i}].{k} missing")
            digest = item.get("source_file_sha256")
            if digest is not None and (not isinstance(digest, str) or
                                       not HEX64.fullmatch(digest) or digest == EMPTY_SHA256):
                reasons.append(f"raw_observations[{i}].source_file_sha256 empty or malformed")
            if "value" in item and (isinstance(item["value"], bool) or
                                    not isinstance(item["value"], (int, float))):
                reasons.append(f"raw_observations[{i}].value must be numeric")
    supplied_hash = packet.get("source_packet_sha256")
    if supplied_hash is not None and (not isinstance(supplied_hash, str) or
                                     not HEX64.fullmatch(supplied_hash) or supplied_hash == EMPTY_SHA256):
        reasons.append("source_packet_sha256 is empty-file digest or malformed")
    if packet.get("reuse_permission") == "PUBLIC_DOMAIN":
        reasons.append("PUBLIC_DOMAIN assertion requires separate rights verification")
    if reasons:
        return {"decision": "REJECT_AS_VERIFIED_EVIDENCE", "reasons": reasons,
                "allowed_use": "quarantined candidate; not model ground truth"}
    return {"decision": "CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_CHECK",
            "reasons": ["metadata completeness is not proof of file authenticity, calibration, or reviewer approval"],
            "allowed_use": "manual source and permission verification only"}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("Usage: python validate_field_packet.py candidate_packet.json", file=sys.stderr)
        return 2
    result = assess(json.loads(Path(argv[0]).read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2))
    return 0 if result["decision"] == "CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_CHECK" else 1


if __name__ == "__main__":
    raise SystemExit(main())

import hashlib
import unittest
from validate_field_packet import assess

class FieldPacketGateTests(unittest.TestCase):
    def test_generated_packet_cannot_self_verify(self):
        p = {"packet_id": "QAT_ALSHAHANIYA_SOURCE_PACKET",
             "telemetry_verification_status": "VERIFIED_FIELD_READINGS",
             "site_location": {"name":"Al-Shahaniya, Qatar"},
             "boundary_values_peak_summer": {"ambient_dry_bulb_c":42},
             "source_packet_sha256": hashlib.sha256(b"").hexdigest()}
        r=assess(p)
        self.assertEqual(r["decision"], "REJECT_AS_VERIFIED_EVIDENCE")
        self.assertTrue(any("raw_observations" in x for x in r["reasons"]))
        self.assertTrue(any("source_packet_sha256" in x for x in r["reasons"]))

    def test_no_observations_is_not_field_evidence(self):
        self.assertEqual(assess({"raw_observations":[]})["decision"], "REJECT_AS_VERIFIED_EVIDENCE")

    def test_empty_observation_hash_is_rejected(self):
        obs = {k:"present" for k in (
            "site_id","sensor_id","observed_at_utc","quantity","units",
            "source_file_reference","measurement_method","calibration_record",
            "custodian_permission","independent_reviewer_record")}
        obs["value"]=32.0
        obs["source_file_sha256"]=hashlib.sha256(b"").hexdigest()
        r=assess({"raw_observations":[obs]})
        self.assertTrue(any("source_file_sha256" in x for x in r["reasons"]))

    def test_complete_metadata_is_only_candidate_not_approved(self):
        obs = {k:"candidate_only" for k in (
            "site_id","sensor_id","observed_at_utc","quantity","units",
            "source_file_reference","measurement_method","calibration_record",
            "custodian_permission","independent_reviewer_record")}
        obs["value"]=32.0
        obs["source_file_sha256"]=hashlib.sha256(b"nonempty test fixture").hexdigest()
        r=assess({"raw_observations":[obs]})
        self.assertEqual(r["decision"],"CANDIDATE_READY_FOR_INDEPENDENT_SOURCE_CHECK")

if __name__ == "__main__":
    unittest.main()

"""Findings from the independent verification pass (adversarial probes written AFTER the first 59 tests).
The paraphrase lists were written after seeing failures, so they are regression fixtures, not held-out evidence."""
import json
import tempfile
import unittest
from pathlib import Path

from helpers import FakeAnthropic, make_corpus, real_index, tmpdir_ctx
from qeeri_rag import store
from qeeri_rag.answer import ClaudeProvider
from qeeri_rag.guards import validate_claims
from qeeri_rag.loop import LoopConfig, run_question
from qeeri_rag.retrieve import retrieve

SEC = [("S01", "Pad cooling", "Pad cooling wet bulb temperature equation applies.")]


def ask(q, **kw):
    with tmpdir_ctx() as t:
        return run_question(real_index(), q, config=LoopConfig(receipts_dir=str(Path(t) / "r"), **kw))


class NegativesNeverSupported(unittest.TestCase):
    Q = [
        "What cooling water per square meter does a Qatar greenhouse need?",
        "Estimate the water consumption for pad cooling of a greenhouse in Doha",
        "Recommend the number of extraction fans for a 500 square metre greenhouse in Qatar",
        "What airflow should I design for a 2000 m2 Qatar greenhouse?",
        "What is the cooling water consumption of a greenhouse in Oman?",
        "What is the cooling water consumption of greenhouses in the UAE?",
        "Size the evaporative pad for a Qatar tomato greenhouse of 800 m2",
        "How large should the cooling pad be for my Doha greenhouse?",
        "What breaker rating protects the fan motors in a Qatar greenhouse?",
        "Specify the irrigation drippers needed per plant for tomatoes in Qatar",
        "What temperature will the crop zone reach in a Qatar greenhouse in August?",
        "What is the cooling load of a Qatar greenhouse?",
        "Give me the pad effectiveness measured at the Shahaniya greenhouse",
        "How much water do tomatoes need in a greenhouse in Egypt?",
        "What fan capacity did Kuwait greenhouses use?",
        "Should I proceed with the greenhouse project in Qatar?",
    ]

    def test_none_is_supported_candidate(self):
        for q in self.Q:
            r = ask(q)
            self.assertNotEqual(r["status"], "CITATION_CHECK_PASSED_REVIEW_PENDING", q)
            self.assertEqual(r["claims"], [], q)

    def test_general_principle_never_supports_a_question_naming_a_site(self):
        r = retrieve(real_index(), "Does a single temperature sensor show uniformity in my Qatar greenhouse?")
        self.assertEqual(r["passages"], [])
        self.assertTrue(r["transfer_context"])  # shown as context only


class PositivesStillAnswered(unittest.TestCase):
    P = [("Does the IFAS publication say a single sensor can verify temperature uniformity?", "IFAS_AE069#S03"),
         ("What does FAO say about maximum distance between fan and pad?", "S5_FAO_2013#L08"),
         ("What average pad face velocity does FAO recommend?", "S5_FAO_2013#L08"),
         ("In the Riyadh trial what share of total water was used for cooling?", "S7_TSAFARAS_2021#L06"),
         ("How many fans did the Riyadh Venlo greenhouse have?", "S7_TSAFARAS_2021#L07"),
         ("Which contractors may carry out electrical installation work under KAHRAMAA rules?", "S6_KAHRAMAA_LVWC#L10"),
         ("What leaching fraction does FAO list for substrate irrigation scheduling?", "S5_FAO_2013#L09"),
         ("How does air temperature change between the pad and the exhaust fans in a fan and pad greenhouse?", "IFAS_AE069#S02")]

    def test_no_over_refusal_on_legitimate_source_questions(self):
        for q, gold in self.P:
            r = ask(q)
            cited = {x["chunk_id"].split("@")[0] for c in r["claims"] for x in c["citations"]}
            self.assertEqual(r["status"], "CITATION_CHECK_PASSED_REVIEW_PENDING", q)
            self.assertIn(gold, cited, q)


class CodeLevelInvariants(unittest.TestCase):
    def test_zero_tool_budget_means_zero_tool_calls_even_when_refusing(self):
        r = ask("How many fans for my 1000 m2 greenhouse in Qatar?", max_tool_calls=0)
        self.assertEqual(r["loop"]["tool_calls"], 0)
        self.assertEqual(r["reason"], "SIZING_OR_SPECIFICATION_REQUEST_NOT_PERFORMED")

    def test_human_verified_needs_independent_review_record(self):
        with tmpdir_ctx() as t:
            p = make_corpus(t, [{"source_id": "HV", "verification_status": "HUMAN_VERIFIED", "sections": SEC}])
            con = store.connect(":memory:")
            self.assertEqual(store.ingest(con, p)["sources"][0]["reason"], "HUMAN_VERIFIED_WITHOUT_INDEPENDENT_REVIEW_RECORD")
            d = json.loads(p.read_text())
            d["sources"][0]["curator"] = "alice"
            d["sources"][0]["review_record"] = {"reviewer": "alice", "reviewed_at": "2026-11-09", "record_path": "x"}  # self-review
            p.write_text(json.dumps(d))
            self.assertEqual(store.ingest(con, p)["sources"][0]["outcome"], "REJECTED")
            d["sources"][0]["review_record"]["reviewer"] = "bob"
            p.write_text(json.dumps(d))
            self.assertEqual(store.ingest(con, p)["sources"][0]["outcome"], "INGESTED")
            r = retrieve(con, "How does pad cooling wet bulb temperature equation apply?")
            self.assertTrue(r["passages"][0]["human_verified"])

    def test_nothing_in_the_real_corpus_is_human_verified(self):
        con = real_index()
        r = retrieve(con, "What pad area per greenhouse floor area does FAO suggest?")
        self.assertFalse(any(p["human_verified"] for p in r["passages"]))

    def test_source_paths_cannot_escape_the_permitted_root(self):
        with tmpdir_ctx() as t:
            outside = Path(tempfile.mkdtemp()) / "secret.txt"
            outside.write_text("Pad cooling temperature private data.")
            (t / "sub").mkdir()
            (t / "sub" / "allowlist.json").write_text(json.dumps({"sources": [
                {"source_id": "ESC", "format": "text", "path": str(outside), "jurisdiction": "QA",
                 "verification_status": "SOURCE_TEXT_READ", "reuse_status": "LOCAL_ONLY"},
                {"source_id": "DOTDOT", "format": "text", "path": "../../../../../../etc/hostname", "jurisdiction": "QA",
                 "verification_status": "SOURCE_TEXT_READ", "reuse_status": "LOCAL_ONLY"}]}))
            # sources must sit under the allowlist's directory unless an explicit root is given
            rec = store.ingest(store.connect(":memory:"), t / "sub" / "allowlist.json")
            self.assertEqual([s["outcome"] for s in rec["sources"]], ["REJECTED", "REJECTED"])
            self.assertIn("escapes the permitted root", rec["sources"][0]["detail"])

    def test_spelled_out_numbers_not_in_the_passage_are_unsupported(self):
        con = real_index()
        ret = retrieve(con, "What pad area per greenhouse floor area does FAO suggest?")
        out = validate_claims(con, [{"text": "FAO says one square metre of pad per forty square metres.", "chunk_ids": [ret["passages"][0]["chunk_id"]]}], ret["passages"])
        self.assertEqual(out[0]["status"], "UNSUPPORTED")
        self.assertTrue(out[0]["failure_reasons"][0].startswith("SPELLED_OUT_NUMBER"))

    def test_api_key_never_reaches_receipts_or_eval_artifacts(self):
        from qeeri_rag.evaluate import run_eval
        key = "sk-ant-TESTKEY-DO-NOT-LEAK"
        con = real_index()
        with FakeAnthropic(json.dumps({"abstain": True, "claims": [], "uncertainty": "", "missing": []})) as fake, tmpdir_ctx() as t:
            run_question(con, "What pad area per greenhouse floor area does FAO suggest?",
                         provider=ClaudeProvider(api_key=key, api_url=fake.url), config=LoopConfig(receipts_dir=str(t)))
            run_eval(con, Path(__file__).resolve().parent.parent / "eval" / "questions.json", t / "ev.json",
                     api_key=key, api_url=fake.url, cfg=LoopConfig(receipts_dir=str(t)))
            blob = "".join(p.read_text() for p in t.rglob("*") if p.is_file())
        self.assertNotIn(key, blob)

    def test_retrieval_is_deterministic_and_read_only(self):
        con = real_index()
        q = "What fan airflow per floor area does FAO give for fan and pad cooling?"
        before = con.execute("select count(*) from ingestion_log").fetchone()[0]
        a, b = json.dumps(retrieve(con, q), sort_keys=True), json.dumps(retrieve(con, q), sort_keys=True)
        self.assertEqual(a, b)
        self.assertEqual(before, con.execute("select count(*) from ingestion_log").fetchone()[0])

    def test_hostile_query_strings_do_not_raise_or_touch_the_store(self):
        con = real_index()
        for s in ['"; DROP TABLE chunks; --', "pad* NEAR/3 cooling OR AND NOT", "\x00\x01 pad cooling", "pad " * 3000,
                  "'\" ) ( pad cooling temperature", "\U0001F331 cooling pad equation temperature"]:
            retrieve(con, s)
        self.assertEqual(con.execute("select count(*) from chunks where state='ACTIVE'").fetchone()[0], 8)


class ProvenanceFields(unittest.TestCase):
    def test_every_source_url_is_a_clean_url_and_limitations_are_not_lost(self):
        import re
        con = real_index()
        for r in con.execute("select source_id, url, limitations from sources where state='ACTIVE'"):
            self.assertRegex(r["url"], r"^https?://\S+$", r["source_id"])  # no free text, no raw spaces
        fao = con.execute("select limitations from sources where source_id='S5_FAO_2013'").fetchone()[0]
        self.assertIn("equivalence of the two copies is unconfirmed", fao)


class KnownLimitationPinned(unittest.TestCase):
    def test_a_real_citation_does_not_prove_entailment(self):
        """DOCUMENTED LIMIT, not a fix: a claim that CONTRADICTS its cited chunk but contains no numbers passes the
        deterministic checks as CITATION_CHECK_PASSED_REVIEW_PENDING. Only the PENDING_REVIEW human gate can catch it."""
        con = real_index()
        chunk = retrieve(con, "Does a single temperature sensor show spatial uniformity in the greenhouse?")["passages"][0]
        out = validate_claims(con, [{"text": "A single temperature sensor is sufficient to verify spatial uniformity of the greenhouse.",
                                     "chunk_ids": [chunk["chunk_id"]]}], [chunk])
        self.assertEqual(out[0]["status"], "CITATION_CHECK_PASSED_REVIEW_PENDING")
        self.assertEqual(out[0]["semantic_entailment"], "NOT_EVALUATED")
        self.assertEqual(out[0]["scientific_validation"], "NOT_EVALUATED")  # if this ever flips, update README 'Known limitations'
        payload = json.dumps({"abstain": False, "claims": [{"text": out[0]["text"], "chunk_ids": [chunk["chunk_id"]]}], "uncertainty": "", "missing": []})
        with FakeAnthropic(payload) as fake, tmpdir_ctx() as t:
            res = run_question(con, "Does a single temperature sensor show spatial uniformity in the greenhouse?",
                               provider=ClaudeProvider(api_key="k", api_url=fake.url), config=LoopConfig(receipts_dir=str(t)))
            queue = (t / "review_queue.jsonl").read_text()
        self.assertEqual(res["claims"][0]["human_review"], "PENDING_REVIEW")
        self.assertIn("PENDING_REVIEW", queue)


if __name__ == "__main__":
    unittest.main()

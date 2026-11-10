"""CLI contract: exit 0 = cited answer passed deterministic checks; 2 = honest abstention/NOT_EXECUTED; 3 = integrity.
Added after a status rename silently turned every successful answer into exit 2 (no test covered the CLI)."""
import contextlib
import io
import json
import os
import unittest
from pathlib import Path
from unittest import mock

from helpers import ROOT, tmpdir_ctx
from qeeri_rag.cli import main


def cli(*args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), mock.patch.dict(os.environ, {}, clear=False):
        os.environ.pop("ANTHROPIC_API_KEY", None)
        code = main(list(args))
    return code, json.loads(buf.getvalue()) if buf.getvalue().strip() else None


class CliExitCodes(unittest.TestCase):
    def test_exit_codes_distinguish_answer_abstention_and_integrity(self):
        with tmpdir_ctx() as t:
            base = ["--db", str(t / "i.db"), "--receipts-dir", str(t)]
            self.assertEqual(cli(*base, "health")[0], 3)                        # empty index is not healthy
            self.assertEqual(cli(*base, "ingest")[0], 0)
            self.assertEqual(cli(*base, "health")[0], 0)
            code, out = cli(*base, "answer", "What pad area per greenhouse floor area does FAO suggest?")
            self.assertEqual((code, out["status"]), (0, "CITATION_CHECK_PASSED_REVIEW_PENDING"))
            code, out = cli(*base, "answer", "What airflow should I design for a 2000 m2 Qatar greenhouse?")
            self.assertEqual((code, out["status"]), (2, "INSUFFICIENT_EVIDENCE"))
            code, out = cli(*base, "answer", "What pad area per greenhouse floor area does FAO suggest?", "--provider", "claude")
            self.assertEqual((code, out["status"]), (2, "NOT_EXECUTED"))
            self.assertEqual(cli(*base, "retrieve", "What pad area per greenhouse floor area does FAO suggest?")[0], 0)
            self.assertEqual(cli(*base, "retrieve", "What nitrogen fertilizer rate should I apply to greenhouse tomato?")[0], 2)
            self.assertEqual(cli(*base, "resolve", "Fake#S1@000000000000")[0], 2)
            self.assertEqual(cli(*base, "verify")[0], 0)


if __name__ == "__main__":
    unittest.main()

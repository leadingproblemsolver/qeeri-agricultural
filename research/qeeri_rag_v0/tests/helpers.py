"""Test helpers. Fixture corpora here are SYNTHETIC test data (clearly labelled), never evidence."""
import json
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import warnings
warnings.simplefilter("ignore", ResourceWarning)  # tests hold short-lived in-memory connections
from qeeri_rag import store  # noqa: E402

REAL_ALLOWLIST = ROOT / "corpus" / "allowlist.json"


def real_index():
    con = store.connect(":memory:")
    store.ingest(con, REAL_ALLOWLIST)
    return con


def packet_md(sections):
    """sections: [(label, heading, body)] -> packet-format markdown (SYNTHETIC FIXTURE)."""
    out = ["# SYNTHETIC TEST FIXTURE - not evidence\n"]
    for label, heading, body in sections:
        out.append(f"### {label} — {heading}\n{body}\n")
    return "\n".join(out)


def make_corpus(tmpdir, specs):
    """specs: [{source_id, sections|raw, **allowlist fields}] -> allowlist path."""
    tmp = Path(tmpdir)
    entries = []
    for sp in specs:
        sp = dict(sp)
        fname = f"{sp['source_id']}.md"
        (tmp / fname).write_text(sp.pop("raw", None) or packet_md(sp.pop("sections")), encoding="utf-8")
        sp.pop("sections", None)
        base = {"format": "packet_markdown", "path": fname, "jurisdiction": "QA", "verification_status": "SOURCE_TEXT_READ",
                "reuse_status": "LOCAL_ONLY", "title": sp["source_id"], "url": "https://example.invalid/" + sp["source_id"],
                "published": "2022", "aliases": [], "default_applicability": "JURISDICTION_SPECIFIC", "default_topics": ["cooling"]}
        base.update(sp)
        entries.append(base)
    p = tmp / "allowlist.json"
    p.write_text(json.dumps({"sources": entries}), encoding="utf-8")
    return p


class tmpdir_ctx:
    def __enter__(self):
        self._t = tempfile.TemporaryDirectory()
        return Path(self._t.name)

    def __exit__(self, *a):
        self._t.cleanup()


class FakeAnthropic:
    """Local HTTP server that speaks the Messages wire format. PLUMBING ONLY: its canned text is never a model result."""

    def __init__(self, text=None, status=200):
        self.text, self.status, self.requests = text, status, []
        outer = self

        class H(BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers.get("content-length", 0)))
                outer.requests.append({"headers": dict(self.headers), "body": json.loads(body)})
                self.send_response(outer.status)
                self.send_header("content-type", "application/json")
                self.end_headers()
                if outer.status == 200:
                    self.wfile.write(json.dumps({"model": "fake-plumbing-model", "usage": {"input_tokens": 1, "output_tokens": 1},
                                                 "content": [{"type": "text", "text": outer.text}]}).encode())
                else:
                    self.wfile.write(b'{"error":"fake"}')

            def log_message(self, *a):
                pass

        self.srv = HTTPServer(("127.0.0.1", 0), H)
        self.url = f"http://127.0.0.1:{self.srv.server_address[1]}/v1/messages"
        self.thread = threading.Thread(target=self.srv.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *a):
        self.srv.shutdown()
        self.srv.server_close()

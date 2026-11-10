"""Answer providers.

* ExtractiveProvider: no model. Each claim is a retrieved chunk's own text with its citation. Runs offline.
* ClaudeProvider: optional. Consumes only retrieved passages + the frozen instructions. Without ANTHROPIC_API_KEY it
  returns NOT_EXECUTED and never produces text. Model output is parsed as JSON and then validated by guards.validate_claims;
  the model cannot set claim status.

Stdlib only (urllib), same wire format as research/greenhouse_llm_feasibility/run_pilot.py on the pilot branch.
"""
import json
import os
import re
import secrets
import time
import urllib.error
import urllib.request
from pathlib import Path

from .store import sha256_text

HERE = Path(__file__).resolve().parent
INSTRUCTIONS_PATH = HERE.parent / "instructions" / "FROZEN_INSTRUCTIONS.txt"
DEFAULT_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-5-5"


def frozen_instructions():
    text = INSTRUCTIONS_PATH.read_text(encoding="utf-8")
    return text, sha256_text(text)


def citation_of(p):
    return {"chunk_id": p["chunk_id"], "source_id": p["source_id"], "title": p["title"], "url": p["url"],
            "doi": p["doi"], "locator": p["locator"], "chunk_hash": p["chunk_hash"],
            "source_content_hash": p["source_content_hash"], "quote": p["quote"],
            "jurisdiction": p["jurisdiction"], "jurisdiction_relation": p["jurisdiction_relation"],
            "verification_status": p["verification_status"], "human_verified": p["human_verified"]}


def format_passages(passages, nonce=None):
    """Passages are wrapped as untrusted data with a per-call random delimiter so passage text cannot close the block."""
    nonce = nonce or secrets.token_hex(8)
    parts = []
    for p in passages:
        loc = p["locator"]
        parts.append(
            f"<passage id=\"{p['chunk_id']}\" source=\"{p['source_id']}\" jurisdiction=\"{p['jurisdiction']}\" "
            f"relation=\"{p['jurisdiction_relation']}\" section=\"{loc.get('section')}\" page=\"{loc.get('page')}\">\n"
            f"{p['text']}\n</passage>")
    block = f"<untrusted_passages nonce=\"{nonce}\">\n" + "\n".join(parts) + f"\n</untrusted_passages nonce=\"{nonce}\">"
    return block, nonce


def build_user_content(question, passages, inputs=None, nonce=None):
    block, nonce = format_passages(passages, nonce)
    return (f"Question: {question}\n\nSupplied case inputs (JSON): {json.dumps(inputs or {}, ensure_ascii=False)}\n\n"
            f"{block}\n"), nonce


class ExtractiveProvider:
    name = "EXTRACTIVE_NO_MODEL"

    def generate(self, question, passages, inputs=None):
        claims = []
        for p in passages:
            text = p["text"].strip()  # the whole chunk, verbatim: never a truncated sub-span that could change meaning
            claims.append({"text": text, "chunk_ids": [p["chunk_id"]]})
        return {"provider_status": "NOT_REQUIRED", "provider": self.name, "claims": claims, "abstain": not claims,
                "uncertainty": ("Claims are the retrieved passages' own text with the system-assembled citation. "
                                "Entailment of the question by the passage has not been checked by a human."),
                "missing": [], "execution": {"model": None}}


class ClaudeProvider:
    name = "CLAUDE_API"

    def __init__(self, model=DEFAULT_MODEL, api_url=DEFAULT_URL, max_tokens=2000, temperature=0.0, timeout=120,
                 api_key=None):
        self.model, self.api_url, self.max_tokens = model, api_url, max_tokens
        self.temperature, self.timeout = temperature, timeout
        self._key = api_key if api_key is not None else os.environ.get("ANTHROPIC_API_KEY")

    def request_body(self, question, passages, inputs=None):
        instr, _ = frozen_instructions()
        content, nonce = build_user_content(question, passages, inputs)
        body = {"model": self.model, "max_tokens": self.max_tokens, "system": instr,
                "messages": [{"role": "user", "content": content}]}
        if self.temperature is not None:
            body["temperature"] = self.temperature
        return body  # no tools key: no browsing, no tool use

    def generate(self, question, passages, inputs=None):
        if not self._key:
            return {"provider_status": "NOT_EXECUTED", "provider": self.name, "claims": [], "abstain": None,
                    "reason": "ANTHROPIC_API_KEY is not set; no model was called and no text was substituted.",
                    "execution": {"model": self.model}}
        body = self.request_body(question, passages, inputs)
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(self.api_url, data=data, method="POST", headers={
            "x-api-key": self._key, "anthropic-version": ANTHROPIC_VERSION, "content-type": "application/json"})
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
            return {"provider_status": "PROVIDER_ERROR", "provider": self.name, "claims": [], "abstain": None,
                    "reason": f"{type(e).__name__}: {e}", "execution": {"model": self.model}}
        latency = round((time.perf_counter() - t0) * 1000, 1)
        exe = {"model": self.model, "latency_ms": latency, "raw_response": raw,
               "request_sha256": sha256_text(json.dumps(body, sort_keys=True))}
        try:
            payload = json.loads(raw)
            exe["usage"] = payload.get("usage")
            exe["model_reported"] = payload.get("model")
            text = "".join(b.get("text", "") for b in payload.get("content", []) if b.get("type") == "text")
            parsed = _parse_json_object(text)
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            return {"provider_status": "PROVIDER_ERROR", "provider": self.name, "claims": [], "abstain": None,
                    "reason": f"UNPARSEABLE_PROVIDER_OUTPUT: {type(e).__name__}: {e}", "execution": exe}
        return {"provider_status": "EXECUTED", "provider": self.name, "claims": parsed.get("claims", []) or [],
                "abstain": bool(parsed.get("abstain")), "uncertainty": parsed.get("uncertainty", ""),
                "missing": parsed.get("missing", []) or [], "execution": exe}


def _parse_json_object(text):
    text = text.strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError("no JSON object in model output")
    obj = json.loads(m.group(0))
    if not isinstance(obj, dict):
        raise ValueError("model output JSON is not an object")
    if not isinstance(obj.get("claims", []), list):
        raise ValueError("claims is not a list")
    return obj


def get_provider(name, **kw):
    if name in ("extractive", "none", None):
        return ExtractiveProvider()
    if name == "claude":
        return ClaudeProvider(**kw)
    raise ValueError(f"unknown provider: {name}")

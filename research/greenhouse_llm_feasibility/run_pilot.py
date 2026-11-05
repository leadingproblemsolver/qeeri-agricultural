#!/usr/bin/env python3
"""Pilot runner for the QEERI greenhouse LLM feasibility protocol (stdlib only).

  python run_pilot.py execute [--out DIR] [--model ID] [--max-tokens N] [--temperature T | --no-temperature]

Freezes the inputs, then runs Arm A (closed book) and Arm B (same prompt plus the
approved passages) with the SAME model and settings. Without ANTHROPIC_API_KEY nothing
is sent and both arms are recorded NOT_EXECUTED. No output is ever synthesised.
Exit codes: 0 both arms executed, 2 not executed (no key), 3 an API error occurred.
"""
import argparse
import hashlib
import json
import os
import secrets
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROMPT_PATH = HERE / "prompt_A.txt"
LEDGER_PATH = HERE / "evidence_ledger.json"
DEFAULT_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_packet(ledger):
    """Arm B passages: only claims whose source text was actually read (SOURCE_TEXT_READ).

    Abstract-only claims are UNVERIFIED and are excluded. Evaluator annotations
    (applicability, limitations) are not included; scope and locators are.
    """
    sources = {s["source_id"]: s for s in ledger["sources"]}
    blocks = []
    included = []
    for c in ledger["claims"]:
        if c["status"] != "SOURCE_TEXT_READ":
            continue
        s = sources[c["source_id"]]
        lines = [
            f"[{c['claim_id']}] Source: {s['citation']}",
            f"Location in source: {c['locator']['section']}"
            + (f"; {c['locator']['table_figure']}" if c["locator"].get("table_figure") else "")
            + f"; page {c['locator']['page']}",
            f"Scope: {json.dumps(c['scope'], ensure_ascii=False)}",
            f"Statement: {c['claim']}",
            "Values: " + json.dumps(c["values"], ensure_ascii=False),
        ]
        if c.get("excerpt_relayed"):
            lines.append(f"Short excerpt: \"{c['excerpt_relayed']}\"")
        blocks.append("\n".join(lines))
        included.append(c["claim_id"])
    header = (
        "APPROVED SOURCE PASSAGES (finite set; cite by claim ID such as [L06]; "
        "these are the only provided documents):\n\n"
    )
    return header + "\n\n".join(blocks) + "\n", included


def arm_messages(prompt, packet):
    return {"A": prompt, "B": prompt + "\n" + packet}


def build_request(model, content, max_tokens, temperature):
    body = {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": content}]}
    if temperature is not None:
        body["temperature"] = temperature
    return body  # no tools key: external search is disabled for both arms


def post(url, key, body, timeout=900):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"x-api-key": key, "anthropic-version": ANTHROPIC_VERSION, "content-type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, dict(resp.headers), resp.read().decode("utf-8")


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def execute(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    packet, included = build_packet(ledger)
    messages = arm_messages(prompt, packet)
    temperature = None if args.no_temperature else args.temperature
    settings = {
        "model": args.model,
        "max_tokens": args.max_tokens,
        "temperature": temperature,
        "tools": "none (no web search, no retrieval)",
        "system_prompt": None,
        "same_model_and_settings_both_arms": True,
    }
    write_json(out / "FROZEN_INPUTS.json", {
        "frozen_utc": now_utc(),
        "prompt_file": "prompt_A.txt",
        "prompt_sha256": sha256_text(prompt),
        "packet_claim_ids": included,
        "packet_sha256": sha256_text(packet),
        "arm_input_sha256": {k: sha256_text(v) for k, v in messages.items()},
        "settings": settings,
    })

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        for arm in ("A", "B"):
            write_json(out / f"ARM_{arm}_RUN.json", {
                "arm": arm,
                "status": "NOT_EXECUTED",
                "reason": "ANTHROPIC_API_KEY is not set, so no model could be called. No output exists for this arm and none was substituted.",
                "settings": settings,
                "input_sha256": sha256_text(messages[arm]),
                "executed_utc": None,
                "raw_response_file": None,
                "output_file": None,
            })
        print("NOT_EXECUTED: no API key. Both arms recorded as NOT_EXECUTED.")
        return 2

    url = args.api_url or (os.environ.get("ANTHROPIC_BASE_URL", "").rstrip("/") + "/v1/messages" if os.environ.get("ANTHROPIC_BASE_URL") else DEFAULT_URL)
    statuses = {}
    outputs = {}
    for arm in ("A", "B"):
        body = build_request(args.model, messages[arm], args.max_tokens, temperature)
        record = {
            "arm": arm,
            "settings": settings,
            "input_sha256": sha256_text(messages[arm]),
            "request_body_sha256": sha256_text(json.dumps(body, sort_keys=True)),
            "started_utc": now_utc(),
        }
        try:
            status, headers, raw = post(url, key, body)
            record["finished_utc"] = now_utc()
            (out / f"ARM_{arm}_raw_response.json").write_text(raw, encoding="utf-8")
            record["raw_response_file"] = f"ARM_{arm}_raw_response.json"
            record["raw_response_sha256"] = sha256_text(raw)
            record["http_status"] = status
            record["request_id"] = headers.get("request-id") or headers.get("x-request-id")
            parsed = json.loads(raw)
            text = "".join(p.get("text", "") for p in parsed.get("content", []) if p.get("type") == "text")
            record["response_model"] = parsed.get("model")
            record["usage"] = parsed.get("usage")
            record["stop_reason"] = parsed.get("stop_reason")
            (out / f"ARM_{arm}_output.txt").write_text(text, encoding="utf-8")
            record["output_file"] = f"ARM_{arm}_output.txt"
            record["status"] = "EXECUTED"
            outputs[arm] = text
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", "replace")
            (out / f"ARM_{arm}_error.txt").write_text(err, encoding="utf-8")
            record.update(status="API_ERROR", http_status=e.code, error_file=f"ARM_{arm}_error.txt", output_file=None, raw_response_file=None)
        except Exception as e:  # network, timeout, bad JSON
            record.update(status="API_ERROR", error=f"{type(e).__name__}: {e}", output_file=None, raw_response_file=None)
        write_json(out / f"ARM_{arm}_RUN.json", record)
        statuses[arm] = record["status"]
        print(f"Arm {arm}: {record['status']}")

    if statuses == {"A": "EXECUTED", "B": "EXECUTED"}:
        labels = ["X", "Y"]
        if secrets.randbelow(2):
            labels.reverse()
        key_map = {labels[0]: "A", labels[1]: "B"}
        (out / "blind").mkdir(exist_ok=True)
        for label, arm in key_map.items():
            (out / "blind" / f"{label}.txt").write_text(outputs[arm], encoding="utf-8")
        write_json(out / "blind_key.json", {"note": "Do not open until all judgments are recorded.", "label_to_arm": key_map})
        return 0
    return 3


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ex = sub.add_parser("execute")
    ex.add_argument("--out", default=str(HERE / "runs"))
    ex.add_argument("--model", default="claude-sonnet-5-5")
    ex.add_argument("--max-tokens", type=int, default=8000)
    ex.add_argument("--temperature", type=float, default=0.0)
    ex.add_argument("--no-temperature", action="store_true", help="omit temperature if the model rejects it")
    ex.add_argument("--api-url", default=None)
    args = ap.parse_args(argv)
    return execute(args)


if __name__ == "__main__":
    sys.exit(main())

"""A stand-in for the real distribution API.

    python mock-api/server.py            # listens on 127.0.0.1:8787

It accepts POST /publish, validates the payload the way the real service would, and
returns 200 with an id or 4xx with a reason. Accepted payloads are appended to
mock-api/received.jsonl so you can inspect exactly what you sent.

There are no credentials anywhere in this kit, and this is why: you can learn and prove
the entire publish path — payload shape, traceability, per-channel limits, error
handling — without a single live key. Nobody working through these exercises should ever
hold a production credential, and nothing here requires one.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

HOST, PORT = "127.0.0.1", 8787
RECEIVED = Path(__file__).with_name("received.jsonl")

REQUIRED = ("brand", "channel", "week", "body", "link", "source")
LIMITS = {"sms": 160, "x": 280, "bluesky": 300}
KNOWN = {
    "temerarii-media": {"x", "linkedin", "instagram", "youtube", "tiktok", "facebook",
                        "threads", "bluesky", "pinterest", "blog", "email"},
    "northgate-home": {"google_business_profile", "local_seo", "facebook", "nextdoor",
                       "email", "sms", "instagram", "youtube"},
}


def validate(p: dict) -> list[str]:
    errs = []
    for k in REQUIRED:
        if k not in p or p[k] in (None, "", {}):
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    brand, channel = str(p["brand"]), str(p["channel"])
    known = KNOWN.get(brand)
    if known and channel not in known:
        errs.append(f"channel {channel!r} is not enabled for brand {brand!r}")

    limit = LIMITS.get(channel)
    if limit and len(str(p["body"])) > limit:
        errs.append(f"body is {len(str(p['body']))} chars; {channel} allows {limit}")

    src = p.get("source") or {}
    if not isinstance(src, dict) or not src.get("campaign"):
        errs.append("source.campaign is required — every item must trace to a registry entry")

    if not re.match(r"^https?://", str(p.get("link", ""))):
        errs.append("link must be an absolute URL")
    elif "utm_campaign=" not in str(p["link"]):
        errs.append("link is missing utm_campaign — published links must be attributable")
    return errs


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: dict) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802 (stdlib naming)
        if self.path.rstrip("/") != "/publish":
            return self._send(404, {"error": "unknown endpoint"})
        try:
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            payload = json.loads(raw.decode("utf-8"))
        except (ValueError, TypeError) as e:
            return self._send(400, {"error": f"invalid JSON: {e}"})

        if errs := validate(payload):
            return self._send(422, {"error": "validation failed", "problems": errs})

        rec = {**payload, "received_at": datetime.now(timezone.utc).isoformat()}
        with RECEIVED.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        pid = f"{payload['brand']}-w{payload['week']}-{payload['channel']}"
        self._send(200, {"ok": True, "id": pid})

    def log_message(self, fmt: str, *args) -> None:
        print(f"  {self.address_string()} {fmt % args}")


if __name__ == "__main__":
    print(f"mock publish API on http://{HOST}:{PORT}/publish")
    print(f"accepted payloads append to {RECEIVED.name}   (Ctrl+C to stop)")
    HTTPServer((HOST, PORT), Handler).serve_forever()

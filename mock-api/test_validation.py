"""Negative controls for the mock API — proves it REJECTS, rather than rubber-stamping.

    python mock-api/server.py        # in one terminal
    python mock-api/test_validation.py

A validator nobody has watched reject anything is indistinguishable from `return True`.
Each case below should come back 422 with a reason naming the specific problem.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8787/publish"

GOOD = {
    "brand": "northgate-home",
    "channel": "email",
    "week": 10,
    "body": "The whole tune-up checklist, published.",
    "link": "https://northgatehome.example/?utm_campaign=spring-tuneup",
    "source": {"campaign": "spring-tuneup", "week": 10, "field": "tagline"},
}

CASES: list[tuple[str, dict, int]] = [
    ("valid payload", GOOD, 200),
    ("missing source", {k: v for k, v in GOOD.items() if k != "source"}, 422),
    ("source without campaign", {**GOOD, "source": {"week": 10}}, 422),
    ("sms body over 160", {**GOOD, "channel": "sms", "body": "z" * 200}, 422),
    # Nextdoor is a REAL channel with no publish API. Accepting it would be the worst
    # outcome available: everything downstream would report a success that never happened.
    ("manual-only channel refused", {**GOOD, "channel": "nextdoor"}, 422),
    ("unknown channel", {**GOOD, "channel": "myspace"}, 422),
    ("podcast is a valid channel", {**GOOD, "channel": "podcast"}, 200),
    ("link missing utm_campaign", {**GOOD, "link": "https://northgatehome.example/"}, 422),
    ("link not a URL", {**GOOD, "link": "northgatehome.example"}, 422),
    ("empty body", {**GOOD, "body": ""}, 422),
]


def post(payload: dict) -> tuple[int, str]:
    req = urllib.request.Request(
        URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise SystemExit(f"mock API unreachable at {URL} ({e.reason}). "
                         f"Start it: python mock-api/server.py") from e


def main() -> int:
    failures = 0
    for name, payload, want in CASES:
        got, body = post(payload)
        ok = got == want
        failures += not ok
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:<32} want {want}, got {got}")
        if not ok:
            print(f"          {body[:200]}")
    print()
    if failures:
        print(f"{failures} case(s) behaved unexpectedly.")
        return 1
    print(f"all {len(CASES)} cases behaved as specified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""UTM construction — how a published post becomes an attributable row in analytics.

    python -m pipeline.utm --brand northgate-home --campaign spring-tuneup --channel email --week 12

Parameters are built in a FIXED ORDER and from the same fields every time. That is not
tidiness: reporting groups by exact string, so `utm_campaign=spring-tuneup` and
`utm_campaign=Spring_Tuneup` become two unrelated campaigns in the dashboard, and the
split is invisible until someone asks why the numbers halved.
"""
from __future__ import annotations

import argparse
import re
from urllib.parse import urlencode

from .brand import active_brand, brand_json

_SLUG = re.compile(r"[^a-z0-9]+")


def slug(s: str) -> str:
    """Lowercase, hyphenated, no trailing separators — one canonical form per value."""
    return _SLUG.sub("-", str(s).strip().lower()).strip("-")


def base_url(brand: str | None = None) -> str:
    domains = brand_json(brand).get("domains") or {}
    primary = domains.get("primary") or f"{active_brand(brand)}.example"
    return primary if str(primary).startswith("http") else f"https://{primary}"


def build_utm(brand: str | None, campaign: str, channel: str, week: int,
              medium: str | None = None, content: str | None = None) -> str:
    b = active_brand(brand)
    params = [
        ("utm_source", slug(channel)),
        ("utm_medium", slug(medium or _default_medium(channel))),
        ("utm_campaign", slug(campaign)),
        ("utm_content", slug(content or f"w{int(week):02d}")),
    ]
    return f"{base_url(b)}/?{urlencode(params)}"


def _default_medium(channel: str) -> str:
    """Group channels into media so reporting rolls up sensibly."""
    c = slug(channel)
    if c in {"email"}:
        return "email"
    if c in {"sms"}:
        return "sms"
    if c in {"google-business-profile", "local-seo"}:
        return "organic-local"
    return "social"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build a UTM-tagged URL.")
    ap.add_argument("--brand", default=None)
    ap.add_argument("--campaign", required=True)
    ap.add_argument("--channel", required=True)
    ap.add_argument("--week", type=int, required=True)
    a = ap.parse_args(argv)
    print(build_utm(a.brand, a.campaign, a.channel, a.week))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

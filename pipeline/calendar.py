"""Load a brand's calendar — the authored source of truth for what ships when.

Shape on disk:

    brands/<brand>/content/_context/
      GOAL.yaml                  # anchor date + campaign placements
      calendar/<campaign>.yaml   # weeks.<n>.{name,tagline,blog,days.*}
      calendar/_meta.yaml        # channel definitions

A CELL is one authored unit: a week's framing, or one day's slot. Cells are what the
Creative Lead writes and what the gates check. Everything downstream — renders,
publish payloads, reports — is derived from cells and should never be edited directly.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import yaml

from .brand import brand_path
from .schedule import fiscal_label, place, quarter_of, week_sunday

DAYS = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]


@dataclass
class Week:
    week: int
    campaign_id: str
    name: str = ""
    tagline: str = ""
    blog: str = ""
    blog_body: str = ""
    description: dict = field(default_factory=dict)
    days: dict = field(default_factory=dict)

    # `description.brand_rails` is the ONE authored field deliberately excluded from voice
    # scanning: it is instructions ABOUT the rules ("do not use countdown language"), so
    # scanning it flags the rulebook for quoting the rules. Every other description field
    # is real authored copy and is scanned.
    UNSCANNED = ("brand_rails",)

    def text_fields(self) -> dict[str, str]:
        """Every authored string, keyed by the dotted path a gate should report.

        This walks the structure RECURSIVELY rather than enumerating the shapes it
        expects. That is deliberate. An earlier version handled strings and dicts but
        not lists, so every `social:` slot — a list of post copy — was skipped silently.
        The gate reported PASS on a week containing two banned phrases, because a gate
        only checks what it visits, and nothing tells you about the branches it never
        took. Generic traversal fails loudly on unfamiliar shapes instead of quietly
        ignoring them.
        """
        out: dict[str, str] = {}

        def walk(node, path: str) -> None:
            if isinstance(node, str):
                if node.strip():
                    out[path] = node
            elif isinstance(node, dict):
                for k, v in node.items():
                    if str(k).startswith("_"):
                        continue  # internal commentary, never authored copy
                    walk(v, f"{path}.{k}" if path else str(k))
            elif isinstance(node, (list, tuple)):
                for i, v in enumerate(node):
                    walk(v, f"{path}[{i}]")

        for k in ("name", "tagline", "blog", "blog_body"):
            if v := getattr(self, k):
                walk(v, k)
        for dk, dv in (self.description or {}).items():
            if dk not in self.UNSCANNED:
                walk(dv, f"description.{dk}")
        walk(self.days or {}, "days")
        return out


def _read_yaml(p: Path) -> dict:
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def load_goal(brand: str | None = None) -> dict:
    return _read_yaml(brand_path("content/_context/GOAL.yaml", brand))


def anchor_date(brand: str | None = None) -> date:
    """Sunday of fiscal week 1 for this brand.

    Accepts the anchor under `year:` or `schedule:` — brand packages authored at
    different times put it in different places, and a loader that knows only one shape
    fails on a brand whose data is perfectly valid.
    """
    goal = load_goal(brand)
    raw = ((goal.get("year") or {}).get("anchor")
           or (goal.get("schedule") or {}).get("anchor")
           or goal.get("anchor"))
    if not raw:
        raise SystemExit(f"no year.anchor or schedule.anchor in GOAL.yaml for brand {brand!r}")
    if isinstance(raw, date):
        return raw
    return datetime.strptime(str(raw), "%Y-%m-%d").date()


def campaigns(brand: str | None = None) -> list[dict]:
    return list((load_goal(brand).get("schedule") or {}).get("campaigns") or [])


def campaign_weeks(campaign_id: str, brand: str | None = None) -> list[int]:
    """Weeks a campaign occupies, RESOLVED from its declarative placement."""
    for c in campaigns(brand):
        if c.get("id") == campaign_id:
            return place(int(c.get("start_week", 1)), int(c.get("beats", 1)),
                         set(c.get("skip_weeks") or []))
    return []


def load_campaign(campaign_id: str, brand: str | None = None) -> dict[int, Week]:
    """Every authored week of one campaign, keyed by absolute week number."""
    p = brand_path(f"content/_context/calendar/{campaign_id}.yaml", brand)
    doc = _read_yaml(p)
    out: dict[int, Week] = {}
    for k, v in (doc.get("weeks") or {}).items():
        v = v or {}
        out[int(k)] = Week(
            week=int(k),
            campaign_id=campaign_id,
            name=v.get("name", "") or "",
            tagline=v.get("tagline", "") or "",
            blog=v.get("blog", "") or "",
            blog_body=v.get("blog_body", "") or "",
            description=v.get("description") or {},
            days=v.get("days") or {},
        )
    return out


def load_all(brand: str | None = None) -> dict[int, Week]:
    """Every authored week across every campaign in the brand's calendar/."""
    out: dict[int, Week] = {}
    cal_dir = brand_path("content/_context/calendar", brand)
    if not cal_dir.is_dir():
        return out
    for f in sorted(cal_dir.glob("*.yaml")):
        if f.stem.startswith("_"):
            continue
        out.update(load_campaign(f.stem, brand))
    return out


def describe(week: int, brand: str | None = None) -> str:
    a = anchor_date(brand)
    return (f"{fiscal_label(week, a.year)}  Q{quarter_of(week)}  "
            f"starts {week_sunday(a, week).isoformat()}")

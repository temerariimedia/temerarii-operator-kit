"""The voice gate — the rails every authored cell is checked against.

    python -m pipeline.voice                    # scan the active brand
    BRAND=northgate-home python -m pipeline.voice
    python -m pipeline.voice --brand northgate-home --week 12

Exit code is 0 when clean and 1 when violations are found, so CI and the grader can
both use it without parsing output.

WHY THIS FILE IS THE HEART OF THE KIT
Every function here takes `brand`. That looks like boilerplate until you run it against
two brands whose rules are INVERTED — temerarii-media bans hype, northgate-home bans
fear-selling — at which point a gate that quietly used the wrong brand's list would
pass copy it should reject AND reject copy it should pass, with no error either way.
A gate that is silently wrong is worse than no gate: it manufactures confidence.
"""
from __future__ import annotations

import argparse
import re
import sys

from .brand import active_brand, banned_words
from .calendar import load_all


def scan_text(banned: list[str], field: str, text: str) -> list[dict]:
    """Find banned words in one string. Word-boundary matched so 'act now' does not
    fire on 'contract nowhere', and case-insensitive so 'Act Now' is caught too."""
    hits = []
    for w in banned:
        if not w:
            continue
        pat = r"\b" + re.escape(w).replace(r"\ ", r"\s+") + r"\b"
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            hits.append({"field": field, "word": w, "at": m.start(),
                         "context": text[max(0, m.start() - 40):m.end() + 40].strip()})
    return hits


def scan_brand(brand: str | None = None, week: int | None = None) -> list[dict]:
    banned = banned_words(brand)
    violations: list[dict] = []
    for wk, wd in sorted(load_all(brand).items()):
        if week is not None and wk != week:
            continue
        for field, text in wd.text_fields().items():
            for v in scan_text(banned, field, text):
                violations.append({**v, "week": wk, "campaign": wd.campaign_id})
    return violations


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Scan authored cells against a brand's rails.")
    ap.add_argument("--brand", default=None)
    ap.add_argument("--week", type=int, default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)

    b = active_brand(a.brand)
    banned = banned_words(b)
    violations = scan_brand(b, a.week)

    print(f"VOICE GATE — brand={b} · {len(banned)} banned term(s)")
    if not violations:
        print("VOICE PASS — no violations.")
        return 0
    print(f"VOICE FAIL — {len(violations)} violation(s):\n")
    if not a.quiet:
        for v in violations:
            print(f"  W{v['week']:>2} {v['campaign']}/{v['field']}")
            print(f"       banned: {v['word']!r}")
            print(f"       ...{v['context']}...\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())

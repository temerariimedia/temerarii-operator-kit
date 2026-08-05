"""Grade a Creative Lead's Tier-2 submission — a brand they invented.

    python training/grade_creative.py --brand <their-brand>

It runs against a brand this grader has never seen. That is the point: if it can score a
package nobody wrote it for, the engine really is brand-agnostic, and the candidate has
really onboarded a brand rather than edited a copy of one.

WHAT IT CAN AND CANNOT DECIDE

It checks what is checkable: that rails exist and are enforced, that every declared channel
is authored, that copy fits its platform, that intent is recorded, that surfaces are not
carrying the same sentence.

It does NOT score whether the writing is good. Nothing here can, and a grader that pretends
to would be worse than useless — it would rank people on whatever it could count. The
rubric at the bottom is for the human, and it is the half that decides the seat.

The most important check is `banned_words_are_their_own`. Copying either reference list is
the single clearest tell that a candidate pattern-matched instead of thinking about the
business, and it is invisible to every other check.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))

from pipeline import gates as G  # noqa: E402
from pipeline.brand import banned_words, brand_json, list_brands  # noqa: E402
from pipeline.calendar import load_all  # noqa: E402
from pipeline.content import resolve  # noqa: E402
from pipeline.publish import build_payloads, channels, validate  # noqa: E402

REFERENCE = ("temerarii-media", "northgate-home")
Check = tuple[bool, str]


def rails_exist(brand: str) -> Check:
    """A brand without rails is a folder, not a brand."""
    bj = brand_json(brand)
    words = banned_words(brand)
    if not words:
        return False, "governance/brand.json has no voice.banned_words"
    if len(words) < 10:
        return False, (f"only {len(words)} banned terms. The brief asked for 15-30 — a short "
                       f"list usually means the failure mode was not thought through")
    if len(words) > 60:
        return False, (f"{len(words)} banned terms. Past a point this is a thesaurus, not a "
                       f"rulebook, and it will fight legitimate copy every week")
    missing = [k for k in ("name", "channels", "domains") if not bj.get(k)]
    if missing:
        return False, f"brand.json missing {missing}"
    return True, f"{len(words)} banned terms; name, channels and domains present"


def banned_words_are_their_own(brand: str) -> Check:
    """The list must come from THIS business, not from a reference brand.

    Overlap on genuinely universal terms is fine. Wholesale reuse is not — it means the
    candidate never asked what would make this particular company's customers stop
    trusting it, which is the entire question.
    """
    theirs = set(banned_words(brand))
    for ref in REFERENCE:
        if ref == brand:
            continue
        other = set(banned_words(ref))
        if not other:
            continue
        shared = theirs & other
        overlap = len(shared) / max(len(theirs), 1)
        if overlap > 0.6:
            return False, (f"{overlap:.0%} of the list is copied from {ref} "
                           f"({len(shared)} shared terms) — this is that brand's rulebook, "
                           f"not one derived from the business chosen")
    return True, "banned list is specific to this business, not copied from a reference"


def gates_green(brand: str) -> Check:
    failures = []
    for name, fn in G.GATES.items():
        try:
            ok, problems = fn(brand)
        except Exception as e:
            ok, problems = False, [f"raised {type(e).__name__}: {e}"]
        if not ok:
            failures.append(f"{name}: {problems[0]}")
    if failures:
        return False, "; ".join(failures[:3])
    return True, f"all {len(G.GATES)} gates pass"


def week_authored(brand: str) -> Check:
    weeks = load_all(brand)
    if not weeks:
        return False, "no authored weeks"
    return True, f"{len(weeks)} authored week(s): {sorted(weeks)}"


def intent_recorded(brand: str) -> Check:
    """Every authored week must say what it is FOR.

    A week that cannot state its intent is decoration. This checks the field exists and is
    a real sentence — it cannot check whether the intent is a good one.
    """
    thin = []
    for wk, wd in sorted(load_all(brand).items()):
        intent = (wd.description or {}).get("strategic_intent") or ""
        if len(str(intent).strip()) < 40:
            thin.append(f"W{wk} ({len(str(intent).strip())} chars)")
    if thin:
        return False, f"strategic_intent missing or too thin: {', '.join(thin)}"
    return True, "every authored week records a strategic intent"


def copy_is_native(brand: str) -> Check:
    """Surfaces must not carry the same sentence.

    The failure this catches is the one the pipeline itself once had: build a payload set
    where every channel gets identical copy. It passes every other check and is obvious
    only to someone who reads the output.
    """
    weeks = sorted(load_all(brand))
    if not weeks:
        return False, "no authored weeks"
    wk = weeks[0]
    try:
        payloads = build_payloads(wk, brand)
    except SystemExit as e:
        return False, f"could not build payloads for W{wk}: {e}"
    if not payloads:
        return False, f"W{wk} produced no payloads"
    bodies = [p["body"] for p in payloads]
    distinct = len(set(bodies))
    ratio = distinct / len(bodies)
    if ratio < 0.6:
        return False, (f"W{wk}: only {distinct} distinct bodies across {len(bodies)} "
                       f"channels — surfaces are sharing copy")
    if errs := validate(payloads):
        return False, "; ".join(errs[:2])
    return True, f"W{wk}: {distinct}/{len(bodies)} distinct bodies, all valid"


def rails_actually_bite(brand: str) -> Check:
    """Their own gate must reject their own banned words.

    Verified by CONSTRUCTION rather than by trusting the config: take a term from their
    list, put it in a sentence, and confirm the scan flags it. A rulebook nobody has
    watched reject anything is indistinguishable from an empty file.
    """
    from pipeline.voice import scan_text

    words = banned_words(brand)
    if not words:
        return False, "no banned words to test"
    probe = words[0]
    hits = scan_text(words, "probe", f"This is a sentence containing {probe} in it.")
    if not hits:
        return False, (f"the scan does not flag {probe!r}, which is on this brand's own "
                       f"list — the rails are declared but not enforceable")
    return True, f"rails enforce their own terms (verified with {probe!r})"


CHECKS = [
    ("Brand package has rails", rails_exist),
    ("Banned list is theirs, not copied", banned_words_are_their_own),
    ("All gates pass", gates_green),
    ("A week is authored", week_authored),
    ("Every week records intent", intent_recorded),
    ("Copy is native per surface", copy_is_native),
    ("Rails actually reject their own terms", rails_actually_bite),
]

RUBRIC = """
NOT GRADED ABOVE — this is the half that decides the seat. Read the submission.

  1. Does the banned list show they understood the BUSINESS?
     Read it cold and try to name the company's failure mode from the list alone. If you
     can, they thought about it. If it reads as words nobody likes -- "cheap", "boring",
     "unprofessional" -- they pattern-matched. This is the single strongest signal.

  2. Could someone else execute their revision notes without asking a question?
     "Make it punchier" is a critic. "W11 Thu social[1] repeats Tue's hook -- replace with
     the scheduling angle from the intent" is an editor. This seat is the second one.

  3. On the three-rails rewrite: did they say which two fought them, and why?
     Anyone who says all three were easy did not attempt it seriously.

  4. Does the writing sound like the business, or like them?
     A Creative Lead writes in other people's voices. A strong portfolio piece that sounds
     exactly like their own past work is a warning, not a credential.

  5. Did they push back on anything?
     The best submissions disagree with something -- a rail, a planted violation, a brief.
     Someone who accepts every rule without question will not catch the rule that is wrong.
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Grade a Creative Lead Tier-2 submission.")
    ap.add_argument("--brand", required=True, help="the brand THEY built")
    a = ap.parse_args(argv)

    if a.brand not in list_brands():
        raise SystemExit(f"no brand {a.brand!r}. found: {', '.join(list_brands())}")
    if a.brand in REFERENCE:
        print(f"NOTE: {a.brand} is a reference brand. A submission should be a NEW one.\n")

    print("=" * 72)
    print(f"CREATIVE TIER 2 — {a.brand}")
    print("=" * 72)
    passed = 0
    for title, fn in CHECKS:
        try:
            ok, note = fn(a.brand)
        except Exception as e:
            ok, note = False, f"raised {type(e).__name__}: {e}"
        passed += bool(ok)
        print(f"\n  [{'PASS' if ok else 'FAIL'}]  {title}")
        print(f"          {note}")
    print("\n" + "=" * 72)
    print(f"  {passed}/{len(CHECKS)} automated checks passed")
    print("=" * 72)
    print(RUBRIC)
    return 0 if passed == len(CHECKS) else 1


if __name__ == "__main__":
    sys.exit(main())

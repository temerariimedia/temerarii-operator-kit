"""The auto-grader.

    python training/grade.py                 # score every exercise
    python training/grade.py --exercise 4    # just one

It runs the same gates a real change would face, plus per-exercise assertions. It prints
a scorecard and exits non-zero if anything failed, so CI can run it on a fork's PR.

TWO THINGS IT DELIBERATELY DOES NOT DO:

It does not grade style. Whether your code is elegant is a conversation, not an assertion,
and pretending otherwise would make the score dishonest.

It does not reward a non-empty answer. Exercise 5 checks that your dirty set is MINIMAL,
not merely non-empty — "re-render everything" is not an answer, it is an evasion, and a
grader that accepts it teaches the wrong instinct.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT))

from pipeline import gates as G  # noqa: E402
from pipeline.brand import banned_words, brand_json, list_brands  # noqa: E402
from pipeline.calendar import campaign_weeks, load_all  # noqa: E402
from pipeline.publish import build_payloads, validate  # noqa: E402
from pipeline.schedule import fiscal_label, place, quarter_of  # noqa: E402
from pipeline.voice import scan_brand  # noqa: E402

ANSWERS = KIT / "training" / "answers"


def _read_answer(name: str) -> str | None:
    p = ANSWERS / name
    return p.read_text(encoding="utf-8").strip() if p.exists() else None


# ── exercises ─────────────────────────────────────────────────────────────────────────

def ex1_both_brands_build() -> tuple[bool, str]:
    """Both brands load and every gate that is not about planted content passes."""
    brands = list_brands()
    if sorted(brands) != ["northgate-home", "temerarii-media"]:
        return False, f"expected both brands present, found {brands}"
    notes = []
    for b in brands:
        for gate in ("placement", "completeness", "brand_package"):
            ok, problems = G.GATES[gate](b)
            if not ok:
                notes.append(f"{b}/{gate}: {problems[0]}")
    if notes:
        return False, "; ".join(notes)
    return True, f"both brands load; placement/completeness/brand_package pass for {brands}"


def ex2_fiscal_wrap() -> tuple[bool, str]:
    """Week 53 is next year's W01, and quarters divide by the week's own year."""
    checks = [
        (fiscal_label(27, 2026), "2026-W27"),
        (fiscal_label(53, 2026), "2027-W01"),
        (fiscal_label(56, 2026), "2027-W04"),
        (str(quarter_of(53)), "1"),
        (str(quarter_of(27)), "3"),
    ]
    bad = [f"got {g} want {w}" for g, w in checks if g != w]
    if bad:
        return False, "; ".join(bad)
    if place(50, 6) != [50, 51, 52, 53, 54, 55]:
        return False, f"place(50,6) clamped at 52: {place(50, 6)}"
    return True, "week 53 -> 2027-W01; place() runs past 52 instead of clamping"


def ex3_voice_is_brand_scoped() -> tuple[bool, str]:
    """The two brands' rails are genuinely different, and neither leaks into the other."""
    tm, ng = set(banned_words("temerarii-media")), set(banned_words("northgate-home"))
    if not tm or not ng:
        return False, "a brand has no banned words"
    if tm == ng:
        return False, "both brands have identical banned lists — one is being reused"
    probes = {"northgate-home": ["act now", "silent killer"],
              "temerarii-media": ["revolutionary", "game-changer"]}
    for b, words in probes.items():
        lst = set(banned_words(b))
        missing = [w for w in words if w not in lst]
        if missing:
            return False, f"{b} should ban {missing}"
        other = "temerarii-media" if b == "northgate-home" else "northgate-home"
        leaked = [w for w in words if w in set(banned_words(other))]
        if leaked:
            return False, f"{other} unexpectedly bans {leaked} — rails are bleeding across brands"
    return True, f"temerarii bans {len(tm)}, northgate bans {len(ng)}, no overlap on probes"


def ex4_find_planted_violations() -> tuple[bool, str]:
    """Find the planted voice violations in northgate-home.

    Graded on what the gate finds, not on what you claim: the number must match, AND if
    you wrote training/answers/violations.txt its lines must name the same fields.
    """
    found = scan_brand("northgate-home")
    if len(found) < 3:
        return False, (f"the voice gate finds {len(found)} violation(s) in northgate-home; "
                       f"3 were planted. Is the gate reading THIS brand's rails?")
    claimed = _read_answer("violations.txt")
    if claimed is None:
        return True, (f"gate finds {len(found)}; write training/answers/violations.txt "
                      f"(one 'week field banned-term' per line) for full credit")
    want = {f"{v['week']}:{v['field']}" for v in found}
    got = set()
    for line in claimed.splitlines():
        if m := re.match(r"\s*(\d+)\s+(\S+)", line):
            got.add(f"{m.group(1)}:{m.group(2)}")
    if missed := want - got:
        return False, f"answers/violations.txt missed: {sorted(missed)}"
    return True, f"named all {len(want)} planted violations"


def ex5_minimal_dirty_set() -> tuple[bool, str]:
    """Changing one week must invalidate ONLY that week.

    The failure this guards against is over-invalidation: a dirty set that returns
    everything is always "correct" and always useless, because re-rendering the whole
    calendar to fix one cell is how a fast pipeline becomes a slow one.
    """
    answer = _read_answer("dirty_set.json")
    if answer is None:
        return False, ("write training/answers/dirty_set.json — the weeks invalidated by "
                       "editing northgate-home week 11's tagline. See CURRICULUM.md ex5.")
    try:
        got = json.loads(answer)
    except ValueError as e:
        return False, f"dirty_set.json is not valid JSON: {e}"
    if not isinstance(got, list):
        return False, "dirty_set.json must be a JSON array of week numbers"
    weeks = sorted(load_all("northgate-home"))
    if sorted(got) == weeks and len(weeks) > 1:
        return False, ("you returned every authored week. A dirty set that always returns "
                       "everything is not a dirty set — name only what actually changed")
    if sorted(got) != [11]:
        return False, f"expected [11], got {sorted(got)}"
    return True, "dirty set is minimal: [11]"


def ex6_publish_payloads() -> tuple[bool, str]:
    """Payloads for northgate week 10 build, validate, and stay inside channel limits."""
    try:
        payloads = build_payloads(10, "northgate-home")
    except SystemExit as e:
        return False, f"could not build payloads: {e}"
    if not payloads:
        return False, "no payloads built"
    if errs := validate(payloads):
        return False, "; ".join(errs[:3])
    chans = {p["channel"] for p in payloads}
    if "x" in chans or "bluesky" in chans:
        return False, (f"northgate-home is a local trade brand and does not run X/Bluesky; "
                       f"got {sorted(chans)} — channels must come from the brand package")
    if any(not p.get("source", {}).get("campaign") for p in payloads):
        return False, "a payload has no source.campaign"
    return True, f"{len(payloads)} payload(s) across {len(chans)} channel(s), all valid"


EXERCISES = {
    1: ("Both brands load and their gates pass", ex1_both_brands_build),
    2: ("Fiscal weeks wrap past 52 correctly", ex2_fiscal_wrap),
    3: ("Voice rails are brand-scoped, not shared", ex3_voice_is_brand_scoped),
    4: ("Find the planted violations in northgate-home", ex4_find_planted_violations),
    5: ("Compute a MINIMAL dirty set", ex5_minimal_dirty_set),
    6: ("Build valid publish payloads", ex6_publish_payloads),
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Grade the operator-kit exercises.")
    ap.add_argument("--exercise", type=int, default=None)
    a = ap.parse_args(argv)

    todo = [a.exercise] if a.exercise else sorted(EXERCISES)
    if a.exercise and a.exercise not in EXERCISES:
        raise SystemExit(f"no exercise {a.exercise}. available: {sorted(EXERCISES)}")

    print("=" * 72)
    print("OPERATOR KIT — SCORECARD")
    print("=" * 72)
    passed = 0
    for n in todo:
        title, fn = EXERCISES[n]
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                ok, note = fn()
        except Exception as e:  # a crash is a failure, not a grader bug
            ok, note = False, f"raised {type(e).__name__}: {e}"
        passed += bool(ok)
        print(f"\n  [{'PASS' if ok else 'FAIL'}]  {n}. {title}")
        print(f"          {note}")
    print("\n" + "=" * 72)
    print(f"  {passed}/{len(todo)} passed")
    print("=" * 72)
    return 0 if passed == len(todo) else 1


if __name__ == "__main__":
    sys.exit(main())

# Submission write-up

Paste into the message with the PR link and both MP4s. Keep it short.

---

## Scorecard

```
========================================================================
OPERATOR KIT — SCORECARD
========================================================================

  [PASS]  1. Both brands load and their gates pass
          both brands load; placement/completeness/brand_package pass for ['northgate-home', 'temerarii-media']

  [PASS]  2. Fiscal weeks wrap past 52 correctly
          week 53 -> 2027-W01; place() runs past 52 instead of clamping

  [PASS]  3. Voice rails are brand-scoped, not shared
          temerarii bans 28, northgate bans 29, no overlap on probes

  [PASS]  4. Find the planted violations in northgate-home
          named all 3 planted violations

  [PASS]  5. Compute a MINIMAL dirty set
          dirty set is minimal: [11]

  [PASS]  6. Build valid publish payloads
          165 payload(s) across 15 channel(s) (1 manual), all matching the brand package

========================================================================
  6/6 passed
========================================================================
```

## Exercise 4 — negation judgment

`days.Mon.social[2]` hits `dangerous` in a sentence that argues *against* fear-selling.
Not a true voice violation of intent. Keep the ban list blunt; rewrite (or explicit
override with rationale) rather than teaching the gate to auto-pass negation patterns.

## Beyond the exercises

Added `voice_negation_review` gate: banned-term hits that sit under negation fail as
**review** items, separate from undifferentiated voice FAILs. Same change marks hits
with `negation` in `pipeline/voice.py`. Instinct: when a person has to notice the
difference, encode the check.

## On the render

1. **What broke first:** first render sat with no progress while Chrome Headless Shell
   downloaded (~109 MB). Fixed by waiting — documented in RENDERED-SAMPLE, easy to
   misread as a hang. Also needed `python3` rather than `python` on this machine.
2. **How long:** exercises ~25 min; render setup + both aspects ~15–20 min including
   the Chrome download on first run.
3. **One thing wrong with the output:** silent AAC track while the storyboard specifies
   a calm read and acoustic bed. Left silent on purpose (no music licence / TTS keyed
   in the kit). Given a day: mux a scripted read + bed to −16 LUFS from the storyboard
   rails, not by hand in a timeline.
4. **One pipeline change:** the negation-review gate above — and I'd automate an
   override log so a reviewed hit cannot silently reappear as a hard FAIL next week
   without the rationale travelling with it.
5. **Already automated vs still by hand:** gates, dirty-set thinking, publish payload
   build, and Remotion extract→render are automated. Still by hand: final watch of both
   aspects against the storyboard, and any voice override decision — automating those
   without a human in the loop would manufacture confidence.

**Whole submission:** under an hour for exercises + one evening slice for render.

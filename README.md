# Operator Kit

A working, self-contained slice of a real content-operations engine. Two brands, one
pipeline, no credentials.

You will use it to prove you can run the machine: read a calendar, understand what the
gates enforce, find what is wrong, fix it, and produce output that traces back to its
source. Everything is scored by a grader you can run yourself, as many times as you like,
before you submit anything.

---

## Setup

```bash
git clone <your fork>
cd temerarii-operator-kit
pip install -r requirements.txt

python -m pipeline.gates                          # gates for the default brand
BRAND=northgate-home python -m pipeline.gates     # ...and for the other one
python training/grade.py                          # your scorecard
```

Python 3.11+. The only dependency is PyYAML. If `python training/grade.py` prints a
scorecard, you are set up correctly.

On a fresh clone the scorecard reads **5/6**. That is expected — exercise 5 needs an
answer from you.

---

## What it pays

| **Technical Content Operator** | Round 1<br>wks 1–4 | Round 2<br>wks 5–8 | Final<br>wks 9–13 |
|---|---|---|---|
| **Your rate** | **$150/wk** | **$240/wk** | **$456/wk** |

### How the field narrows

**13 weeks. The field is cut twice.** This applies to all four seats identically — nobody
is exempt and nobody is safe by default.

```
  Round 1          Round 2          Final
  weeks 1–4        weeks 5–8        weeks 9–13
  3 per track      2 per track      1 per track
  12 on the show   8                4
  ends Sat Nov 7   ends Sat Dec 5   ends Sat Jan 9
  4 leave          4 leave          finale
```

**Elimination streams run every 4th Saturday**, live. One person per track goes home each
time, and the decision is read from the system — registry entries executed, gates passed,
work published — not from how anyone felt about you.

**Your counterpart speaks about you on air** at each elimination. Yours is the Creative
Lead. They are not asked to be kind; they are asked to be accurate.

**Rates rise because the work does.** Fewer people means more each, so a Technical Operator
who reaches the final is on **three times** their Round 1 rate. The finalist converts to an
ongoing contract. **Fixed-price milestones against a deliverable, never hourly.** Paid
biweekly on a published calendar; payments only ever move earlier, never later.

**Qualification — Stage 1 and the curriculum — is unpaid.** It runs on a fictional brand
against a local mock, and nothing you produce in it is used by us or ships anywhere. That is
what makes it qualification rather than unpaid work, and why it takes well under an hour.
**Everything after selection is paid.**

Full detail, the season calendar and the elimination structure: **`PROGRAM.md`**.

The whole programme is also public, including every one of the 65 episodes, the Saturday
elimination format and the pay ladder for all four tracks:
**https://temerarii-sandbox.vercel.app/finessionals**

---

## The one idea

**A brand is a data package, not a special case in the code.**

Everything in `pipeline/` takes a brand and reads from `brands/<name>/`. Nothing is
hardcoded to either brand. That is what lets one engine run two businesses, and it is the
thing this kit is really testing.

The two brands are unalike on purpose:

| | `temerarii-media` | `northgate-home` |
|---|---|---|
| Market | B2B, national | B2C, one metro |
| Fiscal year opens | January | **March** |
| Voice bans | **hype** — "revolutionary", "game-changer" | **fear-selling** — "act now", "silent killer" |
| Channels | the shared calendar | shared calendar **+ a podcast**, and Nextdoor as **manual** |

### Why this is harder than it looks

The obvious version of "support multiple brands" is a config file with a name and a colour
in it. That is not what is happening here. Look at what actually varies:

**The fiscal year opens in a different month.** Not a display preference — every date in
the system derives from a brand's anchor. Week 27 is a July week for one brand and a
September week for the other. Any code that hardcodes a January anchor produces dates that
are *plausible* and wrong, which is the hardest kind of wrong to notice.

**The voice rules are inverted.** This is the important one, so read the row again. The
rules are not stricter on one side and looser on the other. `temerarii-media` bans **hype**;
`northgate-home` bans **fear and pressure**. Copy that is perfectly safe for one is a
violation for the other, and vice versa. There is no ordering, no superset, no "strict mode"
you could implement once and reuse.

**Channels are shared but extensible.** Every brand runs the same base calendar — all
social, long form, and owned (blog, email, SMS). `northgate-home` adds a podcast. It did not
require a pipeline change, and that is the test: a brand should be able to add a destination
by editing its own package.

**Not every channel has an API.** `northgate-home` lists Nextdoor as `manual` — a real
channel where the audience genuinely is, with no automated publishing. The pipeline still
builds and validates those payloads, then marks them for a human. Dropping them would be
easier and much worse: a channel that silently falls off the plan is not noticed for a month.

### The failure this design prevents

Suppose one function reaches for a default instead of taking the brand it was given —
a module-level cache, a hardcoded path, a `brand or DEFAULT_BRAND` that swallows an empty
string. You will not get an exception. You will get:

- A **voice gate that reports PASS** on copy containing violations, because it checked the
  other brand's word list.
- **Dates that look right** and are two months off.
- **Payloads for channels the brand does not run**, accepted and never delivered.

Every one of those is worse than a crash. A crash stops the line and gets fixed in an hour.
A silently wrong gate manufactures confidence — it tells you the work was checked when it
was not, and you find out weeks later from someone outside the company.

That is why `pipeline/brand.py` is the first file to read, why `brand_json()` is cached
**per brand**, and why every public function in this kit takes `brand` as an argument even
when it feels like boilerplate. Exercise 3 walks you into the exact bug. It is not
hypothetical — it shipped in the system this kit is modelled on, and it was found only
because someone ran a second brand through it and noticed the planted violations were not
firing.

**The general form, worth carrying past this kit:** when a system serves N things, the
dangerous bug is never the one that breaks all N. It is the one that works perfectly for
whichever thing you happened to test with.

Both brands are fictional or public content. Nothing here is confidential.

---

## Layout

```
brands/
  temerarii-media/     one authored week (W27)
  northgate-home/      two authored weeks (W10-11) + three planted voice violations
pipeline/
  brand.py             brand resolution — where every brand lookup starts
  schedule.py          4-4-5 fiscal calendar; weeks past 52 roll into next year
  calendar.py          load authored cells
  content.py           which authored field feeds which channel (native copy per surface)
  voice.py             the voice gate
  gates.py             every rule the system will not let you break
  publish.py           build + validate publish payloads
  utm.py               attributable links
mock-api/server.py     stands in for the real distribution API
training/grade.py      the grader
remotion/              the render path — two compositions, one component, both aspects
  scripts/extract.mjs  reads the AUTHORED storyboard; the render never invents content
docs/                  reference material
```

## Commands

```bash
python -m pipeline.gates --brand northgate-home        # all gates
python -m pipeline.gates --gate voice                  # one gate
python -m pipeline.voice --brand northgate-home        # violations, with context
python -m pipeline.publish --week 10 --brand northgate-home --dry-run
python mock-api/server.py                              # then --post instead of --dry-run
python training/grade.py                               # scorecard
python training/grade.py --exercise 4                  # one exercise
```

---

## No credentials, ever

There are no API keys in this kit and there is no way to add one usefully. The publish
path runs against a local mock that validates payloads exactly as the real service would
and refuses the same things.

This is not a limitation of the exercise, it is how the real work is set up: nobody holds
production credentials to learn on, and no piece of work reaches an audience without a
sign-off from someone accountable for the brand. You can learn and demonstrate the entire
pipeline without ever being able to break anything.

If any instruction ever asks you to put a real key in this repo, that instruction is wrong.

---

## Native copy per surface

A studio does not write one sentence and publish it everywhere. Each brand here declares
13–15 channels, and every one draws from its own authored field: `social[]` for short-form
posts, `short` for 9:16 vertical, `longform` for the YouTube cut, `podcast`, `blog`,
`email_subject`, `sms`. `pipeline/content.py` is that map.

Two gates hold the line. `channel_coverage` fails if a brand declares a channel and authors
nothing for it. `channel_limits` fails if copy would be truncated by the platform.

Both exist because this pipeline once used the week's tagline as the body for *every*
channel. Payloads built, validation passed, the mock accepted all fifteen — and the output
was fifteen identical posts. Nothing failed, so nothing got fixed.

---

## Where this sits in the process

```
  QUALIFY                        ─▶  SELECTED  ─▶  Round 1
  Stage 1 + CURRICULUM               an offer      TIER-2.md is your
  unpaid · ~30-45 min                              first paid milestone
```

**Qualification is unpaid, and it is deliberately short.** Stage 1 asks only for work you
have already done. The curriculum runs against a **fictional brand and a local mock** —
nothing you produce in it is used by us, ships anywhere, or has any value to us. That is
what makes it qualification rather than unpaid work, and it is why it is measured in
minutes rather than days.

**Paid work begins the moment you are selected.** `TIER-2.md` is your first Round 1
milestone, at your Round 1 rate — not another test.

## Read in this order

| | |
|---|---|
| **`PROGRAM.md`** | **Read this first.** What you are applying to — the live show, the 13 weeks, elimination every 4th Saturday, the pay table, and what a week of the job actually looks like. |
| **`CURRICULUM.md`** | The six exercises. About half an hour; do 1–3 for Stage 2. A fresh clone scores 5/6 — exercise 5 is waiting on you. |
| **`TIER-2.md`** | **Bring us a brand.** Study the two reference packages, then build a third for a business you choose. Paid at your Round 1 rate. This is what the seat is actually decided on. |
| **`OFFICE.md`** | **The modules you operate** — which are yours, which are your counterpart's, and the four handoffs that go wrong. |
| **`CRAFT.md`** | What a video actually contains — ten layers, and how each fails silently. |
| **`SUBMISSION.md`** | How to submit, what to include, and how long it should take. |
| **`RENDERED-SAMPLE.md`** | **Render an asset out of this pipeline and send the file** — both aspects, from a cell in this repo. New output from the machine, not a portfolio piece. |
| **`FROM-KIT-TO-PRODUCTION.md`** | **Read before day one.** What changes when you move from this kit to the real system — what is the same, what is bigger, what the kit deliberately left out (rendering), and what your first week looks like. |

## What this kit is not

It is a **slice** — 47 files against roughly 6,000 in production. Same shape, same rules,
same choke points; there is simply more of it.

**Rendering is in scope, and it is in `remotion/`.** Remotion, both aspect ratios from one
source, audio muxed to −16 LUFS. `npm install && npm run render` is verified on Windows —
900 frames at 30fps, 1920×1080 and 1080×1920. **Getting a render toolchain working is part
of the job**, not a barrier we apologise for.

**We want new output from this pipeline, not a portfolio piece.** A past piece shows what
you make by hand; this seat is about making a *system* produce work at volume. See
**`RENDERED-SAMPLE.md`** — including the audio gap, which is the actual task.

And **credentials**: there are none, there is no way to add one usefully, and that does not
change after you are hired. `FROM-KIT-TO-PRODUCTION.md` explains why that is the design
rather than a probation period.

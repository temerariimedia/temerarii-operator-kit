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
| Channels | 9 social + blog | local search, Nextdoor, email, SMS — **no X, no Bluesky** |

Read that voice row again. The rules are not stricter or looser on one side, they are
**inverted**. Copy that is perfectly safe for one brand is a violation for the other.
Any code that reaches for a default instead of taking a brand argument will be silently
wrong for exactly one of them — and silence is the problem. You will not get an error.
You will get a gate that reports PASS on copy it should have rejected.

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
  voice.py             the voice gate
  gates.py             every rule the system will not let you break
  publish.py           build + validate publish payloads
  utm.py               attributable links
mock-api/server.py     stands in for the real distribution API
training/grade.py      the grader
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

## Next

`CURRICULUM.md` — the six exercises, in order.
`SUBMISSION.md` — how to submit.

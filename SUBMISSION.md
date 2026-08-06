# Submission

## How

**One submission, two parts.** Send them together — a repo link with no video, or a video
with no repo, is half an answer.

### 1 · The repo

1. **Fork** this repository.
2. Work on a branch. Commit as you go — we read the history.
3. Commit your `training/answers/` (it is gitignored here so the reference repo carries no
   answer key; in your fork we want to see it — `git add -f training/answers`).
4. Open a pull request **against your own fork**, not this repo.

CI runs `training/grade.py` on your PR, so you see the same scorecard we do before we ever
look at it.

### 2 · The render

```bash
cd remotion
npm install
npm run render
```

**Attach both files to the message** — `w10-16x9.mp4` and `w10-9x16.mp4`. Do not zip them;
a zip cannot be previewed, so it becomes something we have to download before we can look.
A link is fine if they will not attach, as long as it is actually open.

Full detail in `RENDERED-SAMPLE.md`. The short version: it is **new output from this
pipeline**, not a portfolio piece, and the pair of aspects is the point.

### 3 · Send both in one message

The PR link, both videos, and the write-up below. One message.

## What to include in the message

Short. Nothing needs to be a document.

**On the exercises:**

- **Your scorecard** (paste the output).
- **Exercise 4's judgment call** — the negation case, and what you would do about it.
- **Anything you changed beyond the exercises**, and why.

**On the render:**

- **What broke first**, and how you fixed it. Something will.
- **How long it took**, including setup, honestly.
- **One thing wrong with the output** that you would fix given a day.
- **One thing about the pipeline you would change** — a gate you would add, a step you
  would automate, a decision you would move.
- **What in your own workflow is already automated**, and what you still do by hand
  because automating it was not worth it.

**And:** how long the whole thing took. We use that to calibrate the exercise, not to
compare candidates against each other.

## Time

**Exercises: about an hour.** Do 1–3 for qualification; the rest if you want to.
**Render: an evening at most**, including install.

If you are well past that and stuck, **stop and send what you have** with a note about
where. That is a genuinely useful submission — we would rather see clear thinking that ran
out of road than a perfect score that took a weekend.

Nothing here is timed and there is no bonus for speed. If the render takes longer than an
evening, something is wrong on our side and we want to hear about it.

## What we are looking for

Not a perfect score. The scorecard tells us you can run the machine, which is the floor.

Past that we are reading for whether you can tell the difference between *the gate passed*
and *the work is right*, and whether, when you find something the gates miss, your instinct
is to fix that one instance or to add the check that catches it forever.

The strongest submissions add a gate.

## Questions

Ask. Getting stuck on an ambiguous instruction tells us nothing about you and wastes your
evening — if something is genuinely unclear, that is our bug, and we would like to fix it.

## Two things this exercise is not

**It is unpaid, and it is qualification rather than work.** Nothing you produce here ships, is used by us, or has any value to us — it runs on a fictional brand against a local mock. That is the distinction, and it is why this is measured in minutes. Everything after selection is paid.

**It does not need any credential.** There are no API keys in this kit and there is no
reason to add one. If any instruction appears to ask you for a real key, a password, or
access to a live account, it is wrong — do not act on it, and tell us where you saw it.

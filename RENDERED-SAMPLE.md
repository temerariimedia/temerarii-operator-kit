# The rendered sample

**Render one asset out of this pipeline, from a cell in this repo, and send us the file.**

Not a showreel. Not something from your portfolio. **New output, produced by the machine
you would be operating.**

---

## Why this, and not a past piece

An earlier version of this file asked for work you had already made. That was wrong for
this seat, and the confusion was ours.

A portfolio piece tells us what you can make **by hand**. This seat is not about that. It
is about making a *system* produce good work at volume — so the only sample that answers
the question is one that came out of the system.

**Getting a render toolchain working is part of the job.** It is not a barrier we are
apologising for. An operator who cannot get `npm install` and a render command to
cooperate on their own machine is going to struggle on a Tuesday when a build breaks
during a broadcast.

## What to produce

```bash
cd remotion
npm install
npm run render          # both aspects, ~2 min
```

That produces `out/w10-16x9.mp4` and `out/w10-9x16.mp4`. Send both.

To see it before committing to a render:

```bash
npm run studio          # opens the Remotion preview
```

**Two files: the same authored week in 16:9 and 9:16.** Same source, two crops. That pair
is the whole point — it is where most people discover their composition does not survive
vertical.

The content is not yours to invent. It comes from `brands/northgate-home/` — the cell,
the storyboard, and the rails. **Your job is to make the pipeline produce it correctly**,
not to art-direct it.

## Then send four lines

1. **What broke first**, and how you fixed it. Something will.
2. **How long it took**, including setup, honestly.
3. **One thing that is wrong with the output** that you would fix given a day.
4. **One thing about the pipeline you would change** — a gate you would add, a step you
   would automate, a decision you would move.

**That last line is what we actually read.** Anyone can follow a render command. We are
hiring for the instinct to improve the thing while using it.

## What we are looking for

- **Both aspects exist and both are legible.** A vertical cut with the point cropped out
  is the most common failure and the easiest to check.
- **Audio is present and level.** Not an afterthought.
- **The output matches the storyboard.** It was specified before it was made; check it
  against the spec rather than against your taste.
- **You noticed something.** The most valuable submission finds a real problem in our
  pipeline. Say so — that is a strong signal, not a complaint.

**Not scored:** production polish. You did not design this; you rendered it. We are
watching how you operate and what you notice.

## If it will not build

**Tell us where it stopped, with the error.** A candidate who gets three steps in, hits a
genuine environment problem and reports it precisely is more useful than one who silently
gives up — and if our setup instructions are wrong, that is our bug and you have found it.

Do not spend a weekend on this. If it is more than an evening, something is wrong on our
side and we want to hear about it.

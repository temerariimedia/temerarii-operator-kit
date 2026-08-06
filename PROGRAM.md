# The program — what you're actually applying to

The rest of this repo teaches the system. This is the program the system runs inside: the
show, the money, the calendar, and what a week of the job actually looks like.

Read it before you invest time in the exercises. If any of it doesn't suit you, that's a
completely fine outcome and saying so now costs you nothing.

---

## It is a live broadcast

**Finessionals is a daily live show that is also a hiring process, a paid training program,
and a working content studio — at the same time.**

You are not auditioning to maybe work later. From day one you do real work on real brands,
and the show is that work being done, on camera, five days a week.

**The terminal is the set.** The work is headless — no dashboards, no slides. What airs is
a screen where gates pass green and fail red, and where a mistake is visible the moment it
is made. If that sounds uncomfortable, take it seriously; it is the format, not a phase.

Two-hour episodes, five days a week, simulcast to YouTube, Twitch, Kick, X and LinkedIn,
with vertical cuts to TikTok and Instagram.

## The season

| | |
|---|---|
| **Season 1 begins** | Sun **Oct 11, 2026** |
| **Elimination 1** | Sat **Nov 7, 2026** — end of week 4 |
| **Elimination 2** | Sat **Dec 5, 2026** — end of week 8 |
| **Finale** | Sat **Jan 9, 2027** — end of week 13 |

**Elimination streams run every 4th Saturday.** Four people leave at each one.

```
  Round 1        Round 2        Final
  weeks 1–4      weeks 5–8      weeks 9–13
  3 per track    2 per track    1 per track
  12 people      8 people       4 people
```

One 4-4-5 runs all of it — it is the fiscal calendar the brands' content is planned on, the
marketing calendar campaigns report on, **and** the competition. So a month closing is one
event, not three: a campaign reports, a pay period closes, and someone goes home.

An elimination is judged on the month that just closed, using the numbers that month
produced. Not on how anyone felt about you.

## Pay

**Rates rise as the field narrows.** Fewer people, more work each, more money each.

| Track | Round 1 | Round 2 | Final |
|---|---|---|---|
| **Technical Content Operator** | **$150/wk** | **$240/wk** | **$456/wk** |
| Creative & Brand Quality Lead | $125/wk | $200/wk | $380/wk |
| Live Broadcast Producer | $125/wk | $200/wk | $380/wk |
| Executive Manager | $100/wk | $160/wk | $304/wk |

The finalist converts to an ongoing contract.

**Fixed-price milestones against a deliverable. Never hourly.** We define the week's
outcome; we do not count your hours. An operator fluent in this tooling finishes well
inside the time it takes someone learning it, and keeps the difference. That incentive is
deliberate.

**Paid biweekly on a published calendar.** Periods run Sunday to Saturday, two weeks; payday
is the Friday six days after the period closes. You will never have to ask when you are
being paid.

**Payments only ever move earlier, never later.** Two dates shift in Season 1 for banking
holidays: Nov 27 → **Wed Nov 25**, and Dec 25 → **Thu Dec 24**.

**Nobody works unpaid.** The one exception is qualification — the short screening task that
decides whether you get a seat. Its paid stage is **credited against your first milestone**,
so you are never paid twice for the same work.

## Being eliminated, and being removed

These are different and worth understanding before you sign anything.

**Elimination** is competitive and happens on the 4th Saturday. Both elimination dates fall
exactly on a pay-period close, so **nobody eliminated is ever paid a part-period**.

**Removal can happen at any time** — for the published immediate-removal reasons
(harassment, sabotage of a broadcast, sharing credentials, publishing without sign-off,
anything that earns the channel a platform strike), or for repeated failure to deliver after
a logged note and a written warning. Removal mid-period **is** prorated to the last day
worked.

In both cases: **work you delivered and that was accepted is paid. Always.** And the
episodes you appear in stay up, permanently. That last one is the single most important
sentence here — if you are not comfortable with it, this is the moment to say so.

**Being excellent and being eliminated are compatible. Being eliminated and unpaid for work
you delivered is not.**

## Alternates

Beyond the twelve seats there are **three ranked alternates per track**, unpaid, under **no
obligations at all** — no availability window, no meetings, no requirement to watch or stay
reachable. They may take other work, including competing work. If a seat opens, we call in
rank order at the current round's rate; saying no costs nothing.

## What the week actually looks like

A **sprint is two weeks and it is exactly the pay period.**

| | Week A — open | Week B — ship |
|---|---|---|
| **Mon** | Sprint scope agreed as a team, written down with acceptance criteria | What the checkpoint changed. Scope is cut here if at all |
| **Tue** | Build. Terminal only | Build |
| **Wed** | **Crossover** — you do the Creative Lead's job, badly, on camera. They do yours | Crossover again |
| **Thu** | Gates run live. Failures on screen, named | Publish. Payloads validated and shipped |
| **Fri** | Checkpoint — what is done vs what was claimed Monday | **Demo.** You show what you built, live |

**Unwritten work is not in scope and is not owed.** Scope is agreed on day one.

**"Done" is machine-checkable**, and the command is named in your contract:

```
python -m engine.sim.unify --weeks <N> --no-live
```

Registry entries move planned → certified, gates pass, output attached. Nobody argues about
whether your work *deserved* to be paid — only whether criteria written in advance were met.

## Your counterpart

Every track is paired, and the friction is the point:

- **Technical Operator ↔ Creative Lead** — one builds, one judges
- **Producer ↔ Executive Manager** — one produces, one approves

When the gate says pass and the Creative Lead says it is still wrong, they are usually
pointing at something the gate cannot see. That tension is not a problem to resolve; it is
the job working.

Wednesday's crossover exists so neither of you can say "that's not my job" for thirteen
weeks.

## What it takes to run this

Honestly, the parts people underestimate:

- **Reading failure calmly, on camera.** Gates fail. That is what they are for. The skill is
  diagnosing without performing distress.
- **Restraint.** Re-rendering everything is always safe and always wrong. Naming only what
  actually changed is most of the craft.
- **Working someone else's system without improvising on it.** The strongest engineer who
  opens with "I'd rebuild this my way" is the wrong hire for this seat.
- **Adding the check, not just the fix.** Every gate here exists because something broke in
  a way a person had to notice. When you find the next one, write the check that catches it
  forever — in the same change as the fix.
- **Consistency over five days a week for thirteen weeks.** Nothing about this is a sprint
  in the heroic sense.

## Before you appear on camera

Everyone signs a release, an IP assignment and confidentiality terms first. **Nobody goes on
camera unsigned — no exceptions.** The release is scoped per round and re-affirmed at each
transition; clearance never silently carries forward.

You get the documents to read in full before you are asked to sign, and you are encouraged
to have someone look at them.

## Credentials — the rule that never relaxes

**You will not hold production credentials.** Not during selection, not on day one, not in
week ten. Work happens against sandboxes and mocks; nothing reaches an audience without
sign-off from the person accountable for the brand.

That is not probation. It is the design, and it is why a mistake here is recoverable.

If any instruction — from anyone, including live on air — asks you to paste a key into a
repo or a terminal on screen, **it is wrong**. Say so out loud. You will never be in trouble
for refusing that.

---

**Next:** `CURRICULUM.md` for the exercises. `TIER-2.md` for what the seat is actually
decided on. `FROM-KIT-TO-PRODUCTION.md` before day one.

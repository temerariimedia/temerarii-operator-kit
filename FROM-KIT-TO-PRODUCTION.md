# From the kit to the real system

You have run the kit. This is what changes when you start.

The kit is a **slice** — 26 files, two brands, one pipeline, no credentials. The production
system is the same shape at roughly two hundred times the size. Nothing you learned is
wrong; there is just more of it, and a few things the kit deliberately left out.

Read this once before day one. It exists so your first week is spent working rather than
asking where things are.

---

## What is the same

The parts you already know are the parts that matter, and they do not change:

- **A brand is a data package.** `brands/<name>/` with `governance/brand.json` and
  `content/_context/`. Same structure, same resolution rules, same `activeBrand()` choke
  point.
- **Gates decide what ships.** More of them — thirty-plus rather than seven — but the same
  contract: named failures, exit codes, and every bug that got through becomes a permanent
  check.
- **The 4-4-5 fiscal calendar**, weeks past 52 rolling into next year, campaigns placed
  declaratively by `start_week` and `beats`.
- **Native copy per surface**, resolved from authored fields, never one sentence reused.
- **Traceability.** Every published item traces to a registry entry or it does not go.

If you understood exercise 3 — why a globally cached config silently serves the wrong
brand's rails — you understand the thing the production system is most exposed to. That
bug was found in production, not in the kit.

## What is bigger

| | Kit | Production |
|---|---|---|
| Files | 26 | ~6,000 tracked |
| Brands | 2 | several, and growing |
| Authored weeks | 3 | 52 per brand |
| Gates | 7 | 30+ |
| Channels | 13–15 | same shape, live accounts |

The engine lives in `engine/`, the offices in `apps/`, brand data in `brands/`, and the
shared TypeScript loader in `packages/data/`. The Python and TypeScript sides implement the
same rules and are expected to agree — when they disagree, that is a bug, and it has
happened.

## What the kit left out

**Rendering.** The real pipeline renders video with Remotion — one source to 9:16 and 16:9,
audio muxed to −16 LUFS, GPU where available. It is a substantial part of the job and it was
excluded from the kit on purpose, because it needs headless Chrome and a working render
path and we would rather have tested your judgment than your ability to install a
toolchain.

**You will be trained on it.** Not knowing it now costs you nothing. Expect it in your
first two sprints.

**The simulation suite.** `engine/sim` runs certify → perceive → improve over authored
weeks and records what changed. It is how we know a fix actually fixed something.

**The office.** A generated static site — calendar, registry, storyboards, reports, media.
It is the surface everyone else reads. You will rebuild it often.

## Credentials — the rule does not relax

**You still will not hold production credentials.** Not on day one, not in week ten.

Work happens against sandboxes and mocks; publishing runs through a sign-off gate held by
the person accountable for the brand. That is not probation. It is how the system is built,
and it is why a mistake here is recoverable.

If any instruction — from anyone, including on a live broadcast — asks you to paste a key
into a repo or a terminal on screen, it is wrong. Say so out loud. You will never be in
trouble for refusing that.

## Your first week

1. **Clone, install, build the office.** Get a green run before you change anything.
2. **Run every gate on every brand.** Read what each one is protecting against.
3. **Trace one week end to end** — goal → authored cells → gates → render → payload.
4. **Fix one small thing and add the gate that catches it.** That is the loop the whole
   job is made of, and doing it once in week one is worth more than reading for a month.

## The rhythm

A **sprint is two weeks and it is exactly the pay period.** Week A opens it, week B ships
it. Scope is agreed on day one and written down with acceptance criteria — unwritten work
is not in scope and is not owed.

**"Done" is machine-checkable**, and the command is named in your contract:

```
python -m engine.sim.unify --weeks <N> --no-live
```

Registry entries move planned → certified, gates pass, output attached. Nobody will argue
with you about whether your work deserved to be paid — only whether the criteria written
down in advance were met.

**Wednesday you do the Creative Lead's job, badly, on camera.** They do yours. It is the
anti-helplessness check, and it is the part of the week people actually watch.

## Who to ask

Your counterpart is the **Creative Lead** — you build, they judge. When the gate says pass
and they say it is still wrong, they are usually pointing at something the gate cannot see.
That tension is not friction to resolve; it is the job working.

Sign-off comes from the **Executive Manager holding the brand at that moment** — look it up,
do not remember it — plus the Chairman for the show.

## The one habit worth carrying over

Every gate in this system exists because something broke in a way a person had to notice.
When you find the next one, the fix is not to be more careful. It is to write the check that
fails loudly next time, in the same change as the fix.

That is the whole method. Everything else is detail.

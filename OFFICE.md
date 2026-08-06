# The office — the modules you operate

The back office is a set of modules. **This is which ones are yours**, which belong to
your counterpart, and where the handoffs are. Knowing that is most of avoiding the two
failure modes in this seat: doing someone else's job, and assuming someone else did yours.

---

## The pipeline

```
GOAL  →  CALENDAR  →  GATES  →  RENDER  →  SIGN-OFF  →  PUBLISH  →  REPORTS
         creative     YOU       YOU        creative     YOU         you instrument
                                                                     everyone reads
```

**You own the middle and the end.** The Creative Lead authors the front and approves
before publish. Neither of you can complete a week alone, which is the point of the
pairing.

## Module by module

| Module | Yours? | What that means |
|---|---|---|
| **Calendar** | read | The Creative Lead authors it. You read it to know what has to exist. **You do not edit copy** — if it is wrong, you raise it, you do not fix it. |
| **Registry** | **own** | What is scheduled and what state it is in: planned → rendered → certified → published. If this is wrong, everything downstream is wrong, and it is wrong quietly. |
| **Gates / harness** | **own** | Every check that decides whether work ships. You add gates. This is where most of your lasting contribution lives. |
| **Render pipeline** | **own** | Remotion, both aspects, audio mux, encoding. Yours end to end. |
| **Media** | you produce | You render it; **the Creative Lead signs it off before it publishes.** A technically perfect render that works against the argument does not ship, and that call is not yours. |
| **Publish** | **own** | Payload construction, channel limits, cadence, traceability. Nothing goes out without a registry entry behind it. |
| **Reports** | you instrument | UTM construction is yours. Reading them and changing next week is the Creative Lead's and the EM's. |
| **Brand book / rails** | enforce in code | The content is theirs. **Making the rules machine-checkable is yours** — a rail nobody can check is a rail that drifts. |
| **Storyboards** | you execute | They write the spec; you make the render match it. If the spec is unbuildable, say so before you build something else instead. |

## The handoffs that go wrong

**Copy that is wrong.** You will see it — a typo, a claim that reads badly, a line that
does not fit its channel. **Raise it, do not fix it.** A technical operator quietly editing
brand copy is how a voice drifts with nobody able to say when. One message costs less than
a month of untraceable changes.

**A render that does not match the storyboard.** The storyboard is the spec. If what came
out differs from what was written, that is a defect even if it looks better. Say what
differs and let them decide.

**A gate that fires on good copy.** Do not widen the gate to make the failure go away. A
gate loosened to stop an inconvenience is a gate that stops catching the thing it was
built for. Flag the false positive, keep the gate, and let the exception be recorded where
someone can see it.

**Something that only works for one brand.** The whole system rests on a brand being a
data package. When you find code that reaches for a default instead of taking the brand it
was given — and you will — **that finding is worth more than the fix.** Add the gate.

## What "done" means for you

Not "the script ran." **The registry entry moved to certified, the gates passed, the
output exists in both aspects, and every published item traces back to a cell.**

The command is named in the contract, so nobody argues about it:

```
python -m engine.sim.unify --weeks <N> --no-live
```

## The rhythm

A **sprint is two weeks and it is exactly the pay period.** Monday opens with what
happened to what shipped a fortnight ago — not with a blank page. Thursday of week B is
publish. Friday is the demo, live.

**Wednesday you do the Creative Lead's job, badly, on camera**, and they do yours. That
exists so neither of you can say "not my job" for thirteen weeks, and it is the part of
the week people actually watch.

---

**Next:** `CRAFT.md` for what a single asset contains and how each layer fails silently.
`FROM-KIT-TO-PRODUCTION.md` for what changes when you move from this kit to the real
system.

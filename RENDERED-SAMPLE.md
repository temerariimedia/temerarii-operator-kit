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
npm run render          # both aspects
```

That produces `out/w10-16x9.mp4` and `out/w10-9x16.mp4`. Send both.

**The first run downloads Chrome Headless Shell**, so it sits with no output for a while
before rendering starts. That is normal and it only happens once. Verified on Windows: 900
frames at 30fps, both aspects, 1920×1080 and 1080×1920.

**Both come out silent, and that is where your work starts.**

We render picture. The kit ships no audio, because we are not handing candidates a music
licence or an API key. So the composition emits a silent AAC track — if you run this and
hear nothing, nothing is broken.

**The storyboard specifies audio anyway.** Read the rails in
`brands/northgate-home/content/storyboards/spring-tuneup/beat-01/reel.md`: a *calm
conversational read*, and an *acoustic bed that never swells at the CTA*. That is a spec
with no output behind it. **Closing that gap is the task.**

How you close it is open — recorded read, TTS, licensed bed, all three. What we care about
is that it is **muxed by a script, not by hand in a timeline**, and that it lands near
**−16 LUFS integrated**, which is what we run everything to. If you would rather not source
music, a read alone is fine; if you would rather not do either, send the silent files and
say so plainly. That is a real answer and we would rather have it than a fudge.

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

## Optional, and the strongest thing you can send

**Show us something driven programmatically.**

Whatever tool you like is fine — the question is not which software you own, it is whether
you can make it run *without your hands on it*. That is the whole seat: a GUI produces one
asset, a script produces a season.

Acceptable and equally interesting:

| Tool | Programmatic path |
|---|---|
| **Remotion** | already code — the kit render counts |
| **ffmpeg** | a script that composes, overlays, muxes, normalises |
| **After Effects** | ExtendScript / `aerender` from the command line |
| **Premiere** | ExtendScript, or an XML/EDL you generated |
| **DaVinci** | its Python API |
| **Blender** | `bpy`, headless |
| **Anything** | a script that reads structured data and emits the asset |

**What is not the signal:** keyframes placed by hand in a timeline. Beautiful work, wrong
question. We are not hiring someone to make one video.

### If you want to go further

The studio runs a lot of its tooling through **MCP servers** — media generation, ffmpeg,
transcription, asset pipelines — so a model can drive them directly. If you have wired a
tool to an agent, or written an MCP server, or automated a pipeline end to end, **send
that instead of anything else.** It answers the question better than a rendered file does.

We are not expecting it. It is simply the ceiling, and someone occasionally clears it.

## Then send five lines

1. **What broke first**, and how you fixed it. Something will.
2. **How long it took**, including setup, honestly.
3. **One thing that is wrong with the output** that you would fix given a day.
4. **One thing about the pipeline you would change** — a gate you would add, a step
   you would automate, a decision you would move.
5. **What in your own workflow is already automated**, and what you still do by
   hand because automating it was not worth it. The second half of that answer is
   as useful as the first — knowing where automation stops paying is judgment, not
   laziness.

**That last line is what we actually read.** Anyone can follow a render command. We are
hiring for the instinct to improve the thing while using it.

## How to send it

**Attach both files to the message.** MP4, as rendered — do not re-encode, do not zip.
A zip cannot be previewed, so it becomes something we have to download and unpack before
we can look at it.

```
w10-16x9.mp4
w10-9x16.mp4
```

Thirty seconds at 1080p should be a few MB, which attaches fine. **If the message will
not take them, a link is completely fine** — Drive, Dropbox, WeTransfer, anything that
plays in a browser. Just make sure it is actually open; a link that asks us to request
access is a link we cannot watch.

**Put the five lines in the message body**, not in a document. We read them next to the
video.

## What we are looking for

- **Both aspects exist and both are legible.** A vertical cut with the point cropped out
  is the most common failure and the easiest to check.
- **Whatever you did about audio, you decided it on purpose.** The kit renders silent. We
  are reading for the decision and how you executed it — including "I left it silent
  because X." We are not reading for whether a music bed appeared.
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

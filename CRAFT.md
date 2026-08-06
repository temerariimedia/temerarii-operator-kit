# What a video actually contains

Every published asset is a video, and every video is a stack of decisions. The Creative
Lead specifies most of them. **You build the machine that executes them, and you are the
one who notices when a layer is missing.**

Read this so you know what you are operating. A render that technically succeeds and
drops a layer is a failure nobody catches until it is public.

---

## The ten layers

| Layer | What it is | How it fails silently |
|---|---|---|
| **Composition** | Which composition, how many scenes, frames per scene | `length_frames: 30` instead of `900` — a one-second video that renders without error |
| **Focal element** | One thing the eye goes to per frame | Two focal points; reads as neither |
| **Motion** | A sanctioned move, with a start and a stop | Motion on every element, so nothing is emphasised |
| **On-screen text** | Every word that appears, verbatim | Text outside the safe area — behind the platform UI on 9:16 |
| **Voiceover** | Script, pace, register, where it breathes | Present in 16:9, missing from the vertical cut |
| **Captions** | Burned in, positioned, matching the VO | Absent. Most viewers watch muted, so this is the primary channel |
| **Music bed** | Level under the voice, and what it must not do | Swells at the CTA, turning honest copy into an advert |
| **Thumbnail** | The still that decides whether any of it is seen | Auto-selected frame — usually a blur between scenes |
| **Both aspects** | 16:9 and 9:16 from one source | Vertical renders, but the point is cropped out |
| **Audio master** | −16 LUFS, consistent across the week | One asset quieter than the rest; nobody notices until a viewer does |

## Why this is your problem, not only theirs

The Creative Lead specifies these. **You are the one who can tell whether the render
honoured the spec** — and a pipeline that silently drops a layer will do it every week
until someone builds the check.

That is the pattern this whole system runs on: when something breaks in a way a person had
to *notice*, you have learned that people do not reliably notice it. **Write the gate in
the same change as the fix.**

Candidate gates that do not exist yet, if you want somewhere to start:

- **Aspect parity** — every asset that exists in 16:9 also exists in 9:16
- **Audio present** — a video track with a silent audio stream is a real and common failure.
  **The kit render is a live example: it emits a silent track.** Deliberately — see
  `RENDERED-SAMPLE.md`. It is the one gate here you can write and watch fail today.
- **Duration sanity** — rendered length matches `length_frames / fps` from the storyboard
- **Safe area** — on-screen text within the vertical safe region
- **Loudness** — measured LUFS within tolerance of the target

## The one that matters most

**Both aspects, both legible.** It is the cheapest thing to check and the most common thing
to get wrong, because the horizontal always looks fine and nobody opens the vertical until
it is live.

Render both. Look at both. Every time.

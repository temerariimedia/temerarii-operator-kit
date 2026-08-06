# The production stack

**Every asset the studio has published came out of this.** Not a person in an editor — a
registry of models, called by workflows, driven by authored data.

This is the stack you would be operating. It is here so you know what the job actually
touches before you apply, and so the exercises make sense: the kit is a slice of this.

---

## The one idea, again

**Tools are data, not code.** The studio does not have a "call Kling" function and a "call
Runway" function scattered through the codebase. It has a **typed registry** — every model
declared with its category, provider, cost, limits, strengths, weaknesses and required env
keys — and workflows that ask the registry for *a video model* rather than for *Kling*.

That is why a model can be swapped, deprecated or price-checked without touching a
pipeline, and it is the same principle as a brand being a data package. **If you understand
why `brands/<name>/` works the way it does, you already understand the model registry.**

Schema-validated: `temerarii/catalog/*.yaml` against `temerarii.catalog.schema`. A model
that does not typecheck does not enter the system.

## The stack — 29 models, 10 categories

Costs are per unit and directional; they move, and keeping them current is part of the job.

### Video — the expensive one, so the choice matters

| Model | Provider | Cost | Max | Good at | Weak at |
|---|---|---|---|---|---|
| `kling-2.5` | piapi | $0.35/clip | 10s | motion realism, action, character consistency | dialogue lipsync, long-form |
| `runway-gen4` | runway | $0.50/clip | 10s | scene consistency, continuity, video-to-video | cost |
| `veo-3` | vertex | $0.75/clip | 8s | **native synchronised audio**, dialogue | GCP auth complexity |
| `sora-2` | openai | $0.60/clip | 20s | coherence, physics, audio | API gated tier *(beta)* |
| `pika-2.2` | pika | $0.20/clip | — | cheap iteration | *(beta)* |
| `higgsfield` | higgsfield | $0.30/clip | — | stylised motion | — |

**Read that table as a decision, not a menu.** A 30-second asset is 3–4 clips. At `veo-3`
that is ~$3; at `pika` it is ~$0.80. Multiply by a 52-week calendar across six brands and
the model choice is a budget line, not a preference. Choosing the expensive model for a
shot that did not need synchronised audio is the kind of waste nobody notices for a quarter.

### Image · Voice · Music

| Category | Models |
|---|---|
| **Image** | `flux-1.1-pro-ultra` ($0.06), `flux-kontext` ($0.05), `midjourney-v7` ($0.08), `z-image-turbo` (**free**, HuggingFace) |
| **Voice** | `elevenlabs-multilingual-v2` ($0.30/1k chars), `qwen3-tts` (**free**), `openai-whisper` ($0.006/min, transcription) |
| **Music** | `suno-v4.5` ($0.10/track), `udio-1.5` ($0.10), `musicgen` (**free**) |

**Note the free fallbacks.** They are not decoration — `generate-image` runs fal as primary
with the HuggingFace free tier as fallback, so a rate limit degrades quality instead of
stopping the line. Building that fallback is technical work and it is the difference
between a pipeline and a script.

### Edit · 3D · Avatar — all local, all free

| Model | What |
|---|---|
| `remotion` | Programmatic video from React. **The render path in this kit.** |
| `ffmpeg` | Compositing, encode, mux, loudness. GPU-accelerated where available. |
| `comfyui` | Node workflows for image pipelines |
| `blender` | 3D |
| `heygen-avatar` | $0.50/min — the one paid item here |

### Research · Distribution · Analytics

| Category | Models |
|---|---|
| **Research** | `perplexity-sonar` ($0.005/q), `exa-search` ($0.005/q), `tavily-search` ($0.002/q), `apify-actors` ($0.01/run) |
| **Distribution** | `blotato` (multi-platform posting), `cloudinary` (asset CDN) |
| **Analytics** | `ga4-data-api`, `posthog` |

**Research, distribution and analytics being in the same registry as the generators is the
whole design.** The pipeline ideates *(research)*, creates *(generation)*, publishes
*(distribution)* and analyses *(analytics)* — one system, one registry, one set of
credentials, one place to look when it breaks.

## How it is actually used — the chains

Models are not called individually. **Workflows chain them**, and the chains are registry
entries too (`temerarii/catalog/workflows.yaml`). Sixteen of them exist. The ones that
matter for understanding scale:

| Workflow | The chain |
|---|---|
| **`temerarii-ai-avatar-trending-news`** | research → script → avatar VO → render → post. **The flagship.** One command, live asset. |
| `viral-news-ai-avatar` | research → selection → script → avatar video |
| `render-storyboards` | Remotion render of the storyboard registry into **the 9-output social/video matrix** |
| `composite-video` | GPU compositing and encode via the ffmpeg compositor |
| `generate-image` | fal primary → **HuggingFace free fallback** |
| `distribute` | finished assets → channels, via Blotato |
| `syndicate-blog` | cross-post written content across CMSs |
| `sync-insights` | live sitemap → catalog sync → rotation |

**`render-storyboards` is the one to understand.** It takes the authored storyboard registry
and produces the full social matrix from it — the same source, every aspect ratio and
destination. That is how a week of content across nine channels becomes one render job
rather than nine editing sessions, and it is the direct production version of what
`remotion/` does in this kit at small scale.

## What this means for the seat

**Nobody is asking you to have used these.** Most people have not used most of them; several
did not exist eighteen months ago. What the job requires is the instinct underneath:

- **Choose a model from constraints**, not from what is fashionable. Cost, max duration,
  whether you actually need synchronised audio.
- **Build the fallback.** Every external provider fails eventually. A pipeline that stops
  when one API rate-limits is a script with ambitions.
- **Keep the registry honest.** Prices move, models get deprecated, a "stable" entry goes
  beta. A registry nobody maintains is worse than no registry, because people trust it.
- **Add the gate.** When a model starts returning something subtly wrong — the wrong aspect
  ratio, silent audio, a truncated caption — the fix is a check that catches it next time,
  not a manual re-run.

**At six brands that last point stops being a preference.** You cannot personally eyeball
six brands' output every week. The gates are how you scale, and building them is the job.

---

**Credentials:** none of these keys are in this kit, and there is no way to add one usefully.
The exercises run against a local mock. See `FROM-KIT-TO-PRODUCTION.md` for what changes
after you are hired, and why that is the design rather than a probation period.

// Pull the slides out of the authored storyboard into JSON the composition can import.
//
// This is the same shape as the real pipeline: the render NEVER invents content, it reads
// what was authored. If a slide is not in the storyboard it does not appear in the video,
// and that is the point — the storyboard is the spec, and the render is checked against it.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { parseStoryboard } from "./storyboard.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const kit = join(here, "..", "..");
const board = join(kit, "brands", "northgate-home", "content", "storyboards",
                   "spring-tuneup", "beat-01", "reel.md");

const raw = readFileSync(board, "utf-8");
let out;
try {
  out = parseStoryboard(raw);
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}
mkdirSync(join(here, "..", "src"), { recursive: true });
writeFileSync(join(here, "..", "src", "data.json"), JSON.stringify(out, null, 2));
console.log(`extracted ${out.slides.length} slides · ${out.lengthFrames} frames @ ${out.fps}fps`);

/**
 * Parse the machine-readable fields used by the Remotion composition.
 *
 * Normalize line endings at the boundary. Git commonly checks text out as CRLF on
 * Windows, while repositories and CI usually use LF. The authored storyboard is valid in
 * either form, and parsing must not depend on the operator's checkout configuration.
 */
export const parseStoryboard = (input) => {
  const raw = String(input).replace(/\r\n?/g, "\n");

  const fm = {};
  const fmBlock = raw.match(/^---\n([\s\S]*?)\n---(?:\n|$)/);
  if (fmBlock) {
    for (const line of fmBlock[1].split("\n")) {
      const match = line.match(/^([a-z_]+):\s*"?([^"#]*)"?\s*(#.*)?$/);
      if (match) fm[match[1]] = match[2].trim();
    }
  }

  const slides = [];
  const slidesBlock = raw.split(/^## Slides[ \t]*$/m)[1] ?? "";
  for (const line of slidesBlock.split("\n")) {
    const match = line.match(/^-\s+(.*)$/);
    if (!match) continue;
    const text = match[1].trim();
    const onScreen = text.match(/On-screen:\s*"([^"]+)"/);
    slides.push({
      direction: text.replace(/\s*On-screen:\s*"[^"]+"\s*/, "").trim(),
      onScreen: onScreen ? onScreen[1] : null,
    });
  }

  if (!slides.length) {
    throw new Error(
      "No slides found. The storyboard is the spec — without it there is nothing to render.",
    );
  }

  return {
    title: fm.title ?? "Untitled",
    fps: Number(fm.fps ?? 30),
    lengthFrames: Number(fm.length_frames ?? 900),
    pillar: fm.pillar ?? "",
    slides,
  };
};

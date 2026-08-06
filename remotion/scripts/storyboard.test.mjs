import assert from "node:assert/strict";
import test from "node:test";

import { parseStoryboard } from "./storyboard.mjs";

const fixture = `---
title: "Line ending check"
fps: 30
length_frames: 900
pillar: maintenance
---

## Slides
- Technician opens the panel. On-screen: "Seven checks."
- The written report is handed over.
`;

const expected = {
  title: "Line ending check",
  fps: 30,
  lengthFrames: 900,
  pillar: "maintenance",
  slides: [
    {direction: "Technician opens the panel.", onScreen: "Seven checks."},
    {direction: "The written report is handed over.", onScreen: null},
  ],
};

test("parses an LF storyboard", () => {
  assert.deepEqual(parseStoryboard(fixture), expected);
});

test("parses the same storyboard after a Windows CRLF checkout", () => {
  assert.deepEqual(parseStoryboard(fixture.replace(/\n/g, "\r\n")), expected);
});

test("refuses a storyboard with no slides", () => {
  assert.throws(() => parseStoryboard("---\nfps: 30\n---\n"), /No slides found/);
});

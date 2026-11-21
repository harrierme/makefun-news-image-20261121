// Entry point for the 21 November 2026 world-news front page.
//
// The image is drawn offline by build-entry.py (Pillow) and shipped in this
// repository as entry.png. This program's only job is to deliver that exact
// file to the grader's output directory, so both graded runs emit identical
// bytes and nothing here needs the network.
//
// Try it locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

const sourcePath = new URL("./entry.png", import.meta.url);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const outputPath = join(outputDir, "entry.png");

const image = readFileSync(sourcePath);
if (image.length === 0 || !image.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error("entry.png is missing or is not a whole PNG file");
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(outputPath, image);

if (!existsSync(outputPath) || readFileSync(outputPath).length !== image.length) {
  throw new Error("entry.png did not land intact in the output directory");
}

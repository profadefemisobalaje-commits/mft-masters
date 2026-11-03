#!/usr/bin/env node
/*
 * Render one SVG to a high-resolution PNG for embedding in the PDF edition.
 *
 *   node scripts/svg2png.js <input.svg> <output.png> [width-px]
 *
 * Requires @resvg/resvg-js. Install it once with:
 *   npm install --no-save @resvg/resvg-js
 * or point NODE_PATH at an existing install (the build script does this
 * automatically if /tmp/rend/node_modules exists).
 */
const fs = require("fs");
const { Resvg } = require("@resvg/resvg-js");

const [input, output, widthArg] = process.argv.slice(2);
if (!input || !output) {
  console.error("usage: svg2png.js <input.svg> <output.png> [width-px]");
  process.exit(2);
}

const width = parseInt(widthArg || "2000", 10);
const svg = fs.readFileSync(input, "utf8");

const resvg = new Resvg(svg, {
  fitTo: { mode: "width", value: width },
  background: "white",
  font: { loadSystemFonts: true, defaultFontFamily: "DejaVu Sans" },
});

fs.writeFileSync(output, resvg.render().asPng());

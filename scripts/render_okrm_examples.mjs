#!/usr/bin/env node
// Render the okrm-design example pages to the plugin's declared screenshots.
// Sources: assets/okrm-design/examples/*.html (repository material).
// Output:  plugins/okrm-design/assets/examples/*.jpg (declared plugin UI images).
// Requires Playwright with Chromium; run from the repository root: node scripts/render_okrm_examples.mjs
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

// Resolve Playwright from the project or from a global install (NODE_PATH / npm -g).
const require = createRequire(import.meta.url);
const { chromium } = require('playwright');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SRC = path.join(ROOT, 'assets/okrm-design/examples');
const OUT = path.join(ROOT, 'plugins/okrm-design/assets/examples');
const PAGES = {
  'genesis-sheet': [1400, 1000],
  'poster-programme': [1200, 1600],
  'catalogue-cover': [1400, 1000],
  'catalogue-spread': [1800, 1200],
  'archive-index-web': [1600, 1000],
  'reader-mobile': [1400, 1000],
};

fs.mkdirSync(OUT, { recursive: true });
const browser = await chromium.launch();
for (const [name, [width, height]] of Object.entries(PAGES)) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(path.join(SRC, `${name}.html`)).href);
  await page.waitForTimeout(300);
  const target = path.join(OUT, `${name}.jpg`);
  await page.screenshot({ path: target, type: 'jpeg', quality: 88, clip: { x: 0, y: 0, width, height } });
  console.log(`${path.relative(ROOT, target)}: ${Math.round(fs.statSync(target).size / 1024)} KB`);
  await page.close();
}
await browser.close();

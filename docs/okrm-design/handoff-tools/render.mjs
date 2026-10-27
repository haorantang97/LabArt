// Render HTML to PNG.  Usage: node tools/render.mjs <folder> [prefix ...]
// Renders every <folder>/*.html (optionally only names starting with a prefix) that contains
// <meta name="size" content="WxH"> to a PNG of exactly that size, next to the HTML.
// Needs Playwright: in this folder run `npm i playwright && npx playwright install chromium` once.
import { createRequire } from 'node:module'; import fs from 'node:fs'; import path from 'node:path'; import { pathToFileURL } from 'node:url';
const require = createRequire(path.join(process.cwd(), 'noop.js'));
let chromium; try { ({ chromium } = require('playwright')); } catch { console.error('Playwright not found. Run: npm i playwright && npx playwright install chromium'); process.exit(1); }
const dir = path.resolve(process.argv[2] || 'out'); const pre = process.argv.slice(3); const b = await chromium.launch();
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html') && (!pre.length || pre.some(x => f.startsWith(x)))).sort()) {
  const html = fs.readFileSync(path.join(dir, f), 'utf8'); const m = html.match(/<meta name="size" content="(\d+)x(\d+)"/);
  if (!m) { console.log('skip (no size meta):', f); continue; }
  const [w, h] = [+m[1], +m[2]]; const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto(pathToFileURL(path.join(dir, f)).href); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(dir, f.replace(/\.html$/, '.png')), clip: { x: 0, y: 0, width: w, height: h } }); await p.close(); console.log(f, w, h);
}
await b.close();

#!/usr/bin/env node
/* Render stills of REVIEW.md at given film seconds, for checking layouts.
   node shots.js --size 1440x900 --times 2,10,20 [--read] [--index]
   Loads dist/index.html?shot from disk (run `python3 build.py --no-encrypt` first). */
const fs = require("fs"), path = require("path");
const HERE = __dirname;
const arg = (n, d) => { const i = process.argv.indexOf(n); return i > -1 ? process.argv[i + 1] : d; };
const [W, H] = arg("--size", "1440x900").split("x").map(Number);
const times = arg("--times", "2").split(",").map(Number);
const puppeteer = require(process.env.PUPPETEER_CORE || path.resolve(HERE, "../../../rto_app/_build/node_modules/puppeteer-core"));
(async () => {
  const out = path.join(HERE, "out", "stills"); fs.mkdirSync(out, { recursive: true });
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new", args: ["--hide-scrollbars", "--force-color-profile=srgb"] });
  const page = await browser.newPage();
  const errors = []; page.on("pageerror", (e) => errors.push(e.message)); page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1, isMobile: W < 600, hasTouch: W < 600 });
  await page.goto("file://" + path.join(HERE, "dist", "index.html") + "?shot", { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);
  const total = await page.evaluate(() => window.__total);
  console.log("film seconds:", total, "| scroll px:", await page.evaluate(() => document.documentElement.scrollHeight));
  for (const s of times) {
    await page.evaluate((t) => { window.__seek(t); return new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); }, s);
    const f = path.join(out, `${W}x${H}_t${String(s).replace(".", "_")}.png`);
    await page.screenshot({ path: f }); console.log("still", path.basename(f));
  }
  for (const mode of ["index", "read"]) if (process.argv.includes("--" + mode)) {
    await page.evaluate((m) => document.querySelector("#btn-" + m).click(), mode);
    await new Promise((r) => setTimeout(r, 300));
    await page.screenshot({ path: path.join(out, `${W}x${H}_${mode}.png`) }); console.log("still", mode);
    await page.evaluate((m) => document.querySelector("#btn-" + m).click(), mode);
  }
  const over = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
  console.log("horizontal overflow px:", over, "| errors:", errors.length ? errors : "none");
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });

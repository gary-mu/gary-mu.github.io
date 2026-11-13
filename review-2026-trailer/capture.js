#!/usr/bin/env node
/*
 Render the trailer to video, frame by frame, so the result is exactly 30 s and perfectly smooth.

   node capture.js                      # 1920x1080, 30 fps  -> out/gary-mu-2026-trailer.mp4
   node capture.js --stills 2.6,7,12.4  # PNG stills at those seconds -> out/stills/
   node capture.js --size 1080x1350     # another frame size (e.g. 4:5 for phones)

 Needs: Google Chrome, ffmpeg, and puppeteer-core (set PUPPETEER_CORE to its folder if it is not
 resolvable; defaults to the copy in ../../../rto_app/_build/node_modules).
 It loads dist/index.html?capture straight from disk, so run `python3 build.py --no-encrypt` first.
*/
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

const HERE = __dirname;
const arg = (name, dflt) => { const i = process.argv.indexOf(name); return i > -1 ? process.argv[i + 1] : dflt; };
const [W, H] = arg("--size", "1920x1080").split("x").map(Number);
const FPS = +arg("--fps", 30);
const stills = arg("--stills", "");
const OUT = path.join(HERE, "out");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const pptrPath = process.env.PUPPETEER_CORE || path.resolve(HERE, "../../../rto_app/_build/node_modules/puppeteer-core");
const puppeteer = require(pptrPath);

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: "new", args: ["--hide-scrollbars", "--force-color-profile=srgb"] });
  const page = await browser.newPage();
  await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  await page.goto("file://" + path.join(HERE, "dist", "index.html") + "?capture", { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);
  const dur = await page.evaluate(() => window.__duration);
  const seek = (ms) => page.evaluate((t) => { window.__seek(t); return new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); }, ms);

  if (stills) {
    const dir = path.join(OUT, "stills"); fs.mkdirSync(dir, { recursive: true });
    for (const s of stills.split(",").map(Number)) {
      await seek(s * 1000);
      const f = path.join(dir, `t${String(s).replace(".", "_")}.png`);
      await page.screenshot({ path: f });
      console.log("still", f);
    }
    await browser.close();
    return;
  }

  const name = W === 1920 && H === 1080 ? "gary-mu-2026-trailer.mp4" : `gary-mu-2026-trailer-${W}x${H}.mp4`;
  const outFile = path.join(OUT, name);
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "png", "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", String(FPS), outFile], { stdio: ["pipe", "inherit", "inherit"] });
  const total = Math.round((dur / 1000) * FPS);
  const HOLD = 0;                                     // the closing card already holds for its last 1.4 s
  const t0 = Date.now();
  let last;
  for (let i = 0; i <= total; i++) {
    await seek(Math.min(dur, (i / FPS) * 1000));
    last = await page.screenshot({ type: "png" });
    if (!ff.stdin.write(last)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % 150 === 0) console.log(`frame ${i}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  for (let i = 0; i < HOLD; i++) if (!ff.stdin.write(last)) await new Promise((r) => ff.stdin.once("drain", r));
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
  await browser.close();
  console.log(`video -> ${outFile} (${(fs.statSync(outFile).size / 1e6).toFixed(1)} MB)`);
})().catch((e) => { console.error(e); process.exit(1); });

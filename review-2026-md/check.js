#!/usr/bin/env node
/* Behaviour checks for REVIEW.md in real Chrome: wheel scrolling, index jump, watch, read, reduced motion.
   node check.js   (run `python3 build.py --no-encrypt` first) */
const path = require("path");
const HERE = __dirname;
const puppeteer = require(process.env.PUPPETEER_CORE || path.resolve(HERE, "../../../rto_app/_build/node_modules/puppeteer-core"));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let pass = 0, fail = 0;
const ok = (name, cond, extra = "") => { cond ? pass++ : fail++; console.log((cond ? "PASS " : "FAIL ") + name + (extra ? "  [" + extra + "]" : "")); };
(async () => {
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const url = "file://" + path.join(HERE, "dist", "index.html");
  const page = await browser.newPage();
  const errors = []; page.on("pageerror", (e) => errors.push(e.message)); page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: "networkidle0" });
  const state = () => page.evaluate(() => ({ y: Math.round(scrollY), crumb: document.querySelector("#crumb").textContent, vis: [...document.querySelectorAll(".room")].filter((r) => r.style.visibility === "visible").map((r) => r.className.replace("room r-", "")), bar: parseFloat(document.querySelector("#bar").style.width), cueOff: document.querySelector("#cue").classList.contains("off") }));
  let s = await state();
  ok("starts on the opening room", s.vis.join() === "open" && s.y === 0, s.vis.join());
  ok("opening title is visible at rest", await page.evaluate(() => getComputedStyle(document.querySelector(".title")).opacity === "1"));
  const kick = await page.evaluate(() => { const k = document.querySelector(".title .kick").getBoundingClientRect(), b = document.querySelector(".title b").getBoundingClientRect(), h = document.querySelector("#btn-index").getBoundingClientRect();
    return { text: document.querySelector(".title .kick").textContent, above: k.bottom <= b.top + b.height * 0.12, onScreen: k.top > 0 && k.left >= 0 && k.right <= innerWidth, clearOfHud: k.right < h.left || k.top > h.bottom }; });
  ok("opening shows 'the 2026 version' above the title, clear of the header", kick.text === "the 2026 version" && kick.above && kick.onScreen && kick.clearOfHud, JSON.stringify(kick));

  await page.mouse.move(700, 450);
  for (let i = 0; i < 6; i++) { await page.mouse.wheel({ deltaY: 400 }); await sleep(60); }
  await sleep(900); s = await state();
  ok("wheel scrolling moves the film into the second room", s.vis.includes("what") && s.crumb === "## what this file is", `${s.y}px ${s.vis.join("+")}`);
  ok("words have arrived by then", await page.evaluate(() => [...document.querySelectorAll(".r-what .say .w")].filter((w) => getComputedStyle(w).opacity === "1").length > 8));
  ok("scroll cue hides after the start", s.cueOff);

  for (let i = 0; i < 12; i++) { await page.mouse.wheel({ deltaY: -400 }); await sleep(40); }
  await sleep(900); s = await state();
  ok("scrolling back up rewinds to the opening", s.vis.join() === "open" && s.y === 0, s.vis.join());

  await page.click("#btn-index"); await sleep(200);
  ok("index opens with twelve cards", await page.evaluate(() => !document.querySelector("#index").hidden && document.querySelectorAll("#index .card").length === 12));
  await page.evaluate(() => document.querySelectorAll("#index .card")[9].click()); await sleep(500); s = await state();
  ok("index card jumps straight to the OASIS room", s.crumb === "### 7. make it AI-native" && s.vis.join() === "mcp", `${s.crumb} | ${s.vis.join("+")}`);
  ok("that room's terminal lines are shown", await page.evaluate(() => [...document.querySelectorAll(".r-mcp .term .body > div")].every((d) => getComputedStyle(d).opacity === "1")));

  await page.evaluate(() => window.__seek(0)); await sleep(100);
  await page.keyboard.press("Space"); await sleep(2000);
  const mid = await state();
  ok("space starts watch mode and the film advances", mid.y > 400 && mid.y < 800, mid.y + "px in 2s");
  await page.mouse.wheel({ deltaY: 50 }); await sleep(300);
  const y1 = (await state()).y; await sleep(500); const y2 = (await state()).y;
  ok("touching the wheel stops watch mode", Math.abs(y2 - y1) < 5 && (await page.evaluate(() => document.querySelector("#btn-watch").textContent)) === "watch", `${y1} -> ${y2}`);

  await page.click("#btn-read"); await sleep(200);
  ok("read shows the plain-text file with six copy buttons", await page.evaluate(() => !document.querySelector("#read").hidden && document.querySelectorAll("#read [data-copy]").length === 6 && /make it AI-native/.test(document.querySelector("#read").textContent)));
  await page.keyboard.press("Escape"); await sleep(100);
  ok("escape closes it", await page.evaluate(() => document.querySelector("#read").hidden));

  await page.evaluate(() => window.__seek(window.__total)); await sleep(300); s = await state();
  ok("the end shows the notepad and a full progress bar", s.vis.join().startsWith("outro") && s.bar > 99.5, `${s.vis.join()} ${s.bar}`);
  ok("no horizontal overflow", await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));

  const label = await page.evaluate(() => document.querySelector('.r-outro [data-do="preview"]').textContent + (document.querySelector('.r-outro [data-do="copy"]') ? " +copy" : ""));
  await page.evaluate(() => document.querySelector('.r-outro [data-do="preview"]').click()); await sleep(200);
  const pv = await page.evaluate(() => { const t = document.querySelector("#tldr"); return { open: !t.hidden, n: t.querySelectorAll("li").length, text: [...t.querySelectorAll("li")].map((l) => "• " + l.textContent).join("\n") }; });
  ok("the last room has one 'preview & copy my impact tl;dr' button that opens the six bullets", label === "preview & copy my impact tl;dr" && pv.open && pv.n === 6, `${label} | ${pv.n}`);
  const want = await page.evaluate(() => window.REVIEW.glance.map((g) => "• " + g.head + " " + g.body).join("\n"));
  ok("the preview shows exactly the text the button copies", pv.text === want);
  const yb = (await state()).y; await page.mouse.wheel({ deltaY: 900 }); await sleep(300);
  ok("the film stays put while the preview is open", Math.abs((await state()).y - yb) < 2);
  await page.keyboard.press("Escape"); await sleep(100);
  ok("escape closes the preview", await page.evaluate(() => document.querySelector("#tldr").hidden));

  const p2 = await browser.newPage();
  await p2.emulateMediaFeatures([{ name: "prefers-reduced-motion", value: "reduce" }]);
  await p2.goto(url, { waitUntil: "networkidle0" });
  ok("reduced motion opens the plain-text file first", await p2.evaluate(() => !document.querySelector("#read").hidden));
  ok("no page errors", errors.length === 0, errors.join(" | "));
  await browser.close();
  console.log(`\n${pass} passed, ${fail} failed`);
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });

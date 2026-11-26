// Checks after the Nov 26 2026 sync: the four review editions are open (no gate), agree on the
// headline figures, and link to each other. Reads the built ./index.html files from disk, or the
// live site with --live. Stills go to _build/verify_out/ (gitignored).
// Usage: node _build/verify_open.js [--live]
const puppeteer = require(process.env.PUPPETEER_CORE || "/Users/gmu/Documents/DS projects/rto_app/_build/node_modules/puppeteer-core");
const path = require("path");
const fs = require("fs");
const root = path.resolve(__dirname, "..");
const out = path.join(root, "_build", "verify_out");
fs.mkdirSync(out, { recursive: true });
const live = process.argv.includes("--live");
const url = (d) => (live ? `https://garymu.com/${d}/?v=${Date.now()}` : "file://" + path.join(root, d, "index.html"));
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
let pass = 0, fail = 0;
const ok = (name, cond, extra = "") => { cond ? pass++ : fail++; console.log((cond ? "PASS " : "FAIL ") + name + (extra ? "  [" + extra + "]" : "")); };

(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const errs = [];
  const open = async (d, w, h) => {
    const p = await b.newPage();
    p.on("pageerror", (e) => errs.push(d + ": " + e.message));
    await p.setViewport({ width: w, height: h });
    await p.goto(url(d), { waitUntil: "networkidle0" });
    await p.evaluate(() => document.fonts.ready);
    return p;
  };
  const text = (p) => p.evaluate(() => document.body.innerText);
  const gate = (p) => p.evaluate(() => !!document.querySelector("#pw") || /Enter the passphrase/.test(document.body.innerText));

  // ---- main site ----
  let p = await open("review-2026", 1280, 800);
  ok("main: no passphrase gate", !(await gate(p)));
  let t = await text(p);
  ok("main: hero says eight evaluators shipped or upgraded", /Eight evaluators shipped or upgraded\./.test(t));
  ok("main: no 'Four literacy evaluators' headline left", !/Four literacy evaluators\./.test(t));
  ok("main: links to REVIEW.md", (await p.$$eval('a[href="../review-2026-md/"]', (a) => a.length)) >= 2);
  await p.screenshot({ path: path.join(out, "open-main-hero.png") });
  await p.evaluate(() => document.querySelector("#numbers").scrollIntoView()); await wait(1800);
  const tile = await p.evaluate(() => document.querySelector("#bento").innerText.replace(/\s+/g, " "));
  ok("main: numbers tile reads 8 evaluators shipped or upgraded", /\b8\b.*evaluators shipped or upgraded/.test(tile), tile.slice(0, 90));
  ok("main: 885 verdicts per model", /885.*verdicts benchmarked per model/.test(tile));
  await p.screenshot({ path: path.join(out, "open-main-numbers.png") });
  await p.evaluate(() => document.querySelector("section#goals").scrollIntoView()); await wait(1500);
  const g1 = await p.evaluate(() => document.querySelector(".goal")?.textContent.replace(/\s+/g, " ") || "");
  ok("main: goal 1 shows 'delivered 8 shipped or upgraded'", /delivered\s*8 shipped or upgraded/i.test(g1), g1.slice(0, 140));
  await p.evaluate(() => window.scrollBy(0, 260)); await wait(600);
  await p.screenshot({ path: path.join(out, "open-main-goals.png") });
  // deep dive A lives in a <template> and opens in a sheet from an era's button
  const dive = await p.evaluate(() => document.querySelector("#tpl-a").content.textContent.replace(/\s+/g, " "));
  ok("main: deep dive A says every one improved significantly from baseline", /The baseline\s*Every one improved significantly from baseline\./.test(dive));
  const allText = await p.evaluate(() => document.body.textContent + [...document.querySelectorAll("template")].map((x) => x.content.textContent).join(" "));
  ok("main: no 'missed first' left on the page or in its sheets", !/missed first/i.test(allText));
  const opened = await p.evaluate(() => { for (const e of document.querySelectorAll(".era")) { e.click(); const d = document.querySelector('button[data-sheet="a"]'); if (d) { d.click(); return true; } } return false; });
  await wait(900);
  if (opened) { await p.evaluate(() => document.querySelector('#sheet-body .step[data-step="1"]').scrollIntoView({ block: "center" })); await wait(1600); }
  await p.screenshot({ path: path.join(out, "open-main-diveA.png") });
  ok("main: deep dive A opens and its chart reads 'v0.1: the baseline' on that step", opened && /v0\.1: the baseline/.test(await p.evaluate(() => document.querySelector("#canvas-a .ctitle")?.textContent || "")));
  await p.close();

  // ---- reels ----
  p = await open("review-2026-reels", 430, 860);
  ok("reels: no passphrase gate", !(await gate(p)));
  t = await p.evaluate(() => [...document.querySelectorAll("#cards .card")].map((c) => c.textContent.replace(/\s+/g, " ")).join("\n"));
  ok("reels: cover says eight evaluators shipped or upgraded", /Eight evaluators shipped or upgraded\./.test(t));
  ok("reels: top track says delivered 8 (4 new, 4 upgraded)", /Target 2 to 3\.\s*Delivered 8\./.test(t) && /4 new, 4 upgraded/.test(t));
  ok("reels: nothing left saying 'Delivered 4' or 'Four literacy evaluators'", !/Delivered 4\.|Four literacy evaluators/.test(t));
  ok("reels: top track says improved significantly from baseline, not 'missed first'", /Each new one improved significantly from baseline/.test(t) && !/missed first/i.test(t));
  ok("reels: last card links to REVIEW.md", (await p.$$eval('#cards a[href="../review-2026-md/"]', (a) => a.length)) === 1);
  const n = await p.$$eval("#cards .card", (c) => c.length);
  await p.keyboard.press("p");
  for (let i = 0; i < n; i++) {
    const tx = await p.evaluate(() => document.querySelector("#cards .card.active").textContent);
    if (i === 0) await p.screenshot({ path: path.join(out, "open-reels-cover.png") });
    if (/Top track/.test(tx)) {
      await wait(700); await p.screenshot({ path: path.join(out, "open-reels-toptrack.png") });
      ok("reels: top track card fits without overflow", await p.evaluate(() => { const c = document.querySelector("#cards .card.active"); return c.scrollHeight <= c.clientHeight + 2; }));
    }
    if (i === n - 1) { await wait(700); await p.screenshot({ path: path.join(out, "open-reels-last.png") }); }
    await p.keyboard.press("ArrowRight"); await wait(120);
  }
  const lastFits = await p.evaluate(() => { const c = document.querySelector("#cards .card.active"); return c.scrollHeight <= c.clientHeight + 2; });
  ok("reels: last card fits without overflow", lastFits);
  await p.close();

  // ---- trailer ----
  p = await open("review-2026-trailer", 1280, 720);
  ok("trailer: no passphrase gate", !(await gate(p)));
  t = await p.evaluate(() => document.querySelector("#stage").textContent.replace(/\s+/g, " "));
  const counts = await p.$$eval(".count", (c) => c.map((x) => x.dataset.to));
  ok("trailer: counts are 8, 1800, 885, 119, 96.5, 95.7, 88", counts.join() === "8,1800,885,119,96.5,95.7,88", counts.join());
  ok("trailer: no 1,770 in the text or the count targets", !/1,?770/.test(t) && !counts.includes("1770"));
  ok("trailer: says verdicts benchmarked per model", /verdicts benchmarked per model/.test(t));
  ok("trailer: has the model swap scene and OASIS in Claude", /led a model swap across teams/i.test(t) && /OASIS in Claude/.test(t) && /No significant impact on accuracy\./.test(t));
  ok("trailer: scene 3 says every one improved significantly from baseline, not 'missed first'", /Every one improved significantly from baseline\./.test(t) && /How\? I went back to the experts\./.test(t) && !/missed first/i.test(t));
  ok("trailer: nine scenes that tile 0 to 31 s with no gap", await p.evaluate(() => { const s = [...document.querySelectorAll(".scene")].map((e) => [+e.dataset.in, +e.dataset.out]); return s.length === 9 && s[0][0] === 0 && s[8][1] === 31 && s.every((x, i) => !i || x[0] === s[i - 1][1]); }));
  ok("trailer: still exactly 30 s", (await p.evaluate(() => window.__duration)) === 30000);
  await p.close();

  // ---- REVIEW.md ----
  p = await open("review-2026-md", 1440, 900);
  ok("REVIEW.md: no passphrase gate", !(await gate(p)));
  ok("REVIEW.md: twelve rooms", (await p.$$eval("#stage .room", (r) => r.length)) === 12);
  const rd = await p.evaluate(() => document.querySelector("#read").textContent.replace(/\s+/g, " "));
  ok("REVIEW.md: 8 evaluators shipped or upgraded, 885 per model", /8 evaluators shipped or upgraded\./.test(rd) && /885 verdicts benchmarked per model/.test(rd));
  ok("REVIEW.md: chapter 1 says every one improved significantly from baseline", /Every one improved significantly from baseline/.test(rd) && !/underperformed/i.test(rd));
  ok("REVIEW.md: Trust card says approved", /reviewed and approved the swap/.test(await p.evaluate(() => document.querySelector(".r-swap").textContent)));
  await p.close();

  ok("no page errors", errs.length === 0, errs.join(" | "));
  console.log(`\n${pass} passed, ${fail} failed`);
  await b.close();
  process.exit(fail ? 1 : 0);
})();

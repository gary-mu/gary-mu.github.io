// Stills + text checks for the main site and the story after a content sync.
// Usage: node _build/verify_sync.js [outDir]
const puppeteer = require("/Users/gmu/Documents/DS projects/rto_app/_build/node_modules/puppeteer-core");
const path = require("path");
const root = path.resolve(__dirname, "..");
const out = process.argv[2] || path.join(root, "_build", "verify_out");
require("fs").mkdirSync(out, { recursive: true });
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const errs = [];
  // main site
  let p = await b.newPage();
  p.on("pageerror", (e) => errs.push("main: " + e.message));
  await p.setViewport({ width: 1280, height: 800 });
  await p.goto("file://" + path.join(root, "review-2026/dist/index.html"), { waitUntil: "networkidle0" });
  const n = await p.$$eval("button.era", (x) => x.length);
  for (let i = 0; i < n; i++) {
    await p.evaluate((i) => document.querySelectorAll("button.era")[i].click(), i);
    const has = await p.$('button[data-sheet="vocab"]');
    if (!has) continue;
    console.log("era", i, "item:", await p.evaluate(() => document.querySelector('button[data-sheet="vocab"]').closest("li").innerText));
    await p.evaluate(() => document.querySelector('button[data-sheet="vocab"]').click());
    await wait(700);
    console.log("sheet title:", await p.$eval("#sheet-title", (x) => x.textContent));
    console.log("sheet text:\n" + (await p.$eval("#sheet-body", (x) => x.innerText)));
    await p.screenshot({ path: path.join(out, "main-swap-sheet.png") });
    await p.evaluate(() => document.querySelector("#sheet-close").click());
    break;
  }
  const links = await p.$$eval(".quote .who a", (a) => [...new Set(a.map((x) => x.closest(".who").innerText.split(" · ")[0] + " -> " + x.innerText + " " + x.href.slice(-24)))]);
  console.log("quote links:\n  " + links.join("\n  "));
  const body = await p.evaluate(() => document.body.innerText);
  console.log("main has 885:", body.includes("885"), "| 1,770 left:", body.includes("1,770"));
  // story
  p = await b.newPage();
  p.on("pageerror", (e) => errs.push("reels: " + e.message));
  await p.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await p.goto("file://" + path.join(root, "review-2026-reels/dist/index.html"), { waitUntil: "networkidle0" });
  const cards = await p.$$eval(".card", (c) => c.map((x) => x.innerText));
  for (let i = 0; i < cards.length; i++) {
    const t = cards[i];
    if (!/model swap/i.test(t) && !/Slack/.test(t)) continue;
    for (let k = 0; k < 60; k++) {
      const cur = await p.$$eval(".card", (c) => c.findIndex((x) => x.classList.contains("active")));
      if (cur >= i) break;
      await p.keyboard.press("ArrowRight");
      await wait(120);
    }
    await wait(900);
    await p.screenshot({ path: path.join(out, `reels-card-${i}.png`) });
    console.log("reels card", i, ":", t.replace(/\n+/g, " | ").slice(0, 520));
    if (/Slack/.test(t)) {
      const hit = await p.evaluate(() => {
        const a = document.querySelector(".card.active .quotes .w a");
        if (!a) return "no link in active card";
        const r = a.getBoundingClientRect();
        return document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2) === a;
      });
      console.log("  slack link sits above the tap zones:", hit);
    }
  }
  console.log("errors:", errs.length ? errs : "none");
  await b.close();
})();

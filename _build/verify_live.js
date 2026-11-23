// Unlock the live REVIEW.md with the first passphrase in the gitignored file and check the latest content is there.
// Usage: node _build/verify_live.js   (prints checks only, never the passphrase)
const puppeteer = require("/Users/gmu/Documents/DS projects/rto_app/_build/node_modules/puppeteer-core");
const fs = require("fs");
const path = require("path");
const root = path.resolve(__dirname, "..");
const pass = fs.readFileSync(path.join(root, "review-2026/.passphrases"), "utf8").split(/\r?\n/).map((s) => s.trim()).filter(Boolean)[0];
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const p = await b.newPage();
  const errs = [];
  p.on("pageerror", (e) => errs.push(e.message));
  await p.setViewport({ width: 1440, height: 900 });
  await p.goto("https://garymu.com/review-2026-md/?v=" + Date.now(), { waitUntil: "networkidle0" });
  console.log("gate shown:", !!(await p.$("#pw")));
  await p.type("#pw", pass);
  await p.click("#go");
  await p.waitForSelector("#stage .room", { timeout: 20000 });
  await wait(800);
  const r = await p.evaluate(() => ({
    rooms: document.querySelectorAll("#stage .room").length,
    stampsOnPlates: document.querySelectorAll(".r-job .dish .stamp").length,
    gold: document.querySelectorAll(".r-job .stamp.gold").length,
    bassinet: !!document.querySelector(".r-leave svg text"),
    accBars: document.querySelectorAll(".r-swap .accb").length,
    slackLinks: document.querySelectorAll(".r-people a[href*='slack.com']").length,
    lastButton: document.querySelector('.r-outro [data-do="preview"]').textContent,
    copyOnLastPage: !!document.querySelector('.r-outro [data-do="copy"]'),
  }));
  console.log(JSON.stringify(r, null, 1));
  console.log("page errors:", errs.length ? errs : "none");
  await b.close();
})();

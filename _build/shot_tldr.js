// Stills of REVIEW.md's last room and its "preview it" sheet, desktop and phone.
const puppeteer = require("/Users/gmu/Documents/DS projects/rto_app/_build/node_modules/puppeteer-core");
const path = require("path");
const root = path.resolve(__dirname, "..");
const out = path.join(root, "_build", "verify_out");
require("fs").mkdirSync(out, { recursive: true });
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
(async () => {
  const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  for (const [w, h, tag] of [[1440, 900, "d"], [390, 844, "m"]]) {
    const p = await b.newPage();
    await p.setViewport({ width: w, height: h, deviceScaleFactor: tag === "m" ? 2 : 1 });
    await p.goto("file://" + path.join(root, "review-2026-md/dist/index.html"), { waitUntil: "networkidle0" });
    await p.evaluate(() => window.__seek(window.__total));
    await wait(500);
    await p.screenshot({ path: path.join(out, `outro-${tag}.png`) });
    await p.evaluate(() => document.querySelector('.r-outro [data-do="preview"]').click());
    await wait(300);
    await p.screenshot({ path: path.join(out, `tldr-${tag}.png`) });
    console.log(tag, "sheet fits width:", await p.evaluate(() => document.querySelector("#tldr .sheet").getBoundingClientRect().right <= innerWidth));
  }
  await b.close();
})();

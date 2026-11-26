// Mockups only: three ways to put "2026 version" wording on the REVIEW.md opening room.
// Loads the built preview (review-2026-md/dist/index.html?shot), seeks to the opening, injects
// each variant into the page in memory and takes stills. It never writes to src/ or index.html.
// Usage: node _build/mock_2026.js [A B B1 B2 C]   -> _build/verify_out/mock2026-<A|B|C>-<desktop|phone>.png
const puppeteer = require(process.env.PUPPETEER_CORE || "/Users/gmu/Documents/DS projects/rto_app/_build/node_modules/puppeteer-core");
const path = require("path");
const fs = require("fs");
const root = path.resolve(__dirname, "..");
const out = path.join(root, "_build", "verify_out");
fs.mkdirSync(out, { recursive: true });

const variants = {
  A: {
    css: `.title i { position: relative; }
          .title .ver { position: absolute; left: calc(var(--u) * 2.2); top: calc(var(--u) * -1.1); font-family: var(--mono); font-style: normal; font-weight: 700;
            font-size: calc(var(--u) * 1.7); letter-spacing: .08em; line-height: 1; padding: calc(var(--u) * .6) calc(var(--u) * 1); border: calc(var(--u) * .2) solid var(--em); color: var(--em); border-radius: 999px; }
          @media (max-aspect-ratio: 4/5) { .title .ver { position: static; display: inline-block; vertical-align: middle; font-size: 4.2vw; padding: 1.4vw 2.6vw; border-width: .5vw; margin: 0 0 0 2.5vw; } }`,
    run: () => { const t = document.querySelector(".r-open .title i"); const s = document.createElement("span"); s.className = "ver"; s.textContent = "v2026"; t.appendChild(s); },
  },
  B: {
    css: `.r-open .kick { position: absolute; z-index: 1; left: 0; right: 0; top: 15.5%; text-align: center; font-family: var(--mono); font-size: calc(var(--u) * 1.6); letter-spacing: .32em; text-transform: uppercase; color: var(--ink); }
          .r-open .kick b { color: var(--em); margin-right: .9em; font-weight: 700; }
          @media (max-aspect-ratio: 4/5) { .r-open .kick { top: 14.5%; font-size: 3.6vw; letter-spacing: .26em; } }`,
    run: () => { const r = document.querySelector(".r-open"); const k = document.createElement("div"); k.className = "kick"; k.innerHTML = "<b>#</b>the 2026 version"; r.insertBefore(k, r.querySelector(".title")); },
  },
  B1: {   // option B, louder: a filled gold pill
    css: `.r-open .kick { position: absolute; z-index: 1; left: 0; right: 0; top: 13.5%; text-align: center; }
          .r-open .kick span { display: inline-block; font-family: var(--mono); font-weight: 700; font-size: calc(var(--u) * 2.1); letter-spacing: .24em; text-transform: uppercase; line-height: 1;
            color: #1d1b22; background: var(--em); border-radius: 999px; padding: calc(var(--u) * 1) calc(var(--u) * 2.2) calc(var(--u) * 1) calc(var(--u) * 2.4); }
          .r-open .kick b { margin-right: .8em; opacity: .55; }
          @media (max-aspect-ratio: 4/5) { .r-open .kick { top: 12.5%; } .r-open .kick span { font-size: 4.4vw; letter-spacing: .16em; padding: 2.2vw 4.4vw; } }`,
    run: () => { const r = document.querySelector(".r-open"); const k = document.createElement("div"); k.className = "kick"; k.innerHTML = "<span><b>#</b>the 2026 version</span>"; r.insertBefore(k, r.querySelector(".title")); },
  },
  B2: {   // option B, loudest: part of the title lockup
    css: `.r-open .kick { position: absolute; z-index: 1; left: 0; right: 0; top: 11.5%; text-align: center; line-height: 1; white-space: nowrap; font-weight: 900; font-size: calc(var(--u) * 3.4); letter-spacing: .03em; text-transform: uppercase; color: var(--ink); }
          .r-open .kick em { font-family: var(--serif); font-style: italic; font-weight: 400; text-transform: none; font-size: calc(var(--u) * 6.6); color: var(--em); letter-spacing: -.02em; margin: 0 .16em; vertical-align: -.07em; }
          @media (max-aspect-ratio: 4/5) { .r-open .kick { top: 11%; font-size: 6.2vw; } .r-open .kick em { font-size: 12vw; } }`,
    run: () => { const r = document.querySelector(".r-open"); const k = document.createElement("div"); k.className = "kick"; k.innerHTML = "the <em>2026</em> version"; r.insertBefore(k, r.querySelector(".title")); },
  },
  C: {
    css: `.quote .fm { opacity: .8; } .quote .fm em { font-style: normal; color: var(--brick); font-weight: 700; }`,
    run: () => { const q = document.querySelector(".r-open .quote"); const mk = (h) => { const p = document.createElement("p"); p.className = "fm"; p.innerHTML = h; return p; };
      const first = q.firstElementChild; [mk("---"), mk("version: <em>2026</em>"), mk("---")].forEach((p) => q.insertBefore(p, first)); },
  },
};

(async () => {
  const b = await puppeteer.launch({ executablePath: process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
  const only = process.argv.slice(2);
  for (const [name, v] of Object.entries(variants).filter(([n]) => !only.length || only.includes(n))) {
    for (const [label, w, h] of [["desktop", 1440, 900], ["phone", 390, 844]]) {
      const p = await b.newPage();
      await p.setViewport({ width: w, height: h, deviceScaleFactor: label === "phone" ? 2 : 1, isMobile: w < 600, hasTouch: w < 600 });
      await p.goto("file://" + path.join(root, "review-2026-md", "dist", "index.html") + "?shot", { waitUntil: "networkidle0" });
      await p.evaluate(() => document.fonts.ready);
      await p.evaluate(() => { window.__seek(4.5); return new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))); });
      await p.addStyleTag({ content: v.css });
      await p.evaluate(v.run);
      await new Promise((r) => setTimeout(r, 150));
      await p.screenshot({ path: path.join(out, `mock2026-${name}-${label}.png`) });
      await p.close();
    }
    console.log("variant", name, "done");
  }
  await b.close();
})();

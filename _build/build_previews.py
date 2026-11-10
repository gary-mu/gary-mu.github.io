"""Builds the theme previews in previews/<theme>/index.html.

Run from the site root:  python3 _build/build_previews.py
Tokens and base.css for each theme come from the Hallmark scaffold
(node ~/.claude/skills/hallmark/scripts/theme.mjs scaffold <theme> --dir previews/<theme>).
"""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = "../../assets/images"

APPS = [
    ("https://evaluator-studio-demo.garymu.com/", "Evaluator Builder Studio", "Using GEPA to programmatically optimize prompt.", "garymu.com"),
    ("https://rto-calculate.streamlit.app/", "RTO calculator", "Optimize your PTO with AI.", "Streamlit"),
    ("https://whatsmygoal.vercel.app/", "What’s My Goal", "Helping students navigate goals and development area.", "Vercel"),
    ("https://tldr-lsn.streamlit.app/", "TLDR Lesson", "Turn class recording into 3-5 bullets, use Whisper API.", "Streamlit"),
    ("https://lsn-copilot.streamlit.app/", "Lesson Plan Copilot", "Use LLM to generate ideas for lesson plans.", "Streamlit"),
]
ARCHIVED = {"RTO calculator", "TLDR Lesson", "Lesson Plan Copilot"}
APPS_MAIN = [a for a in APPS if a[1] not in ARCHIVED]
APPS_ARCHIVE = [a for a in APPS if a[1] in ARCHIVED]
LINKEDIN = "https://www.linkedin.com/in/garymu/"
RESUME = "https://gary-mu.github.io/docs/garymu_resume.pdf"
INSTA = "https://www.instagram.com/comewithme_travels/"
STRAVA = "https://www.strava.com/athletes/3235265"
LOGIN = ""  # the shared app login used to be printed here; Gary had it removed (Nov 2026)

PHOTOS = {
    "lake": ("herbert-lake.jpg", 1920, 1280, "Morning mist on a still lake reflecting pines and snowy peaks", "50% 40%",
             '<a href="https://commons.wikimedia.org/wiki/File:Herbert_Lake_beim_Icefields_Parkway.jpg">Florian Fuchs</a> (CC BY 3.0, Wikimedia Commons)'),
    "road": ("mountain-road.jpg", 1920, 1276, "An empty road running up a green mountain valley under white clouds", "62% 50%",
             '<a href="https://commons.wikimedia.org/wiki/File:Snostskali_Valley,_Mountain_road,_Khevi,_Georgia.jpg">Vyacheslav Argenberg</a> (CC BY 4.0, Wikimedia Commons)'),
    "trail": ("trail-runner.jpg", 1920, 1434, "A trail runner on a dirt path through a green summer meadow", "62% 60%",
              '<a href="https://commons.wikimedia.org/wiki/File:Trail_running_moscow.jpg">ValeryGL</a> (CC BY-SA 4.0, Wikimedia Commons)'),
    "peaks": ("zanskar-road.jpg", 1920, 1280, "A straight road running toward snow-covered peaks under broken cloud", "50% 40%",
              '<a href="https://commons.wikimedia.org/wiki/File:Road_Padum_Zanskar_Range_Jun24_A7CR_00818.jpg">Timothy A. Gonsalves</a> (CC BY-SA 4.0, Wikimedia Commons)'),
    "cliffs": ("olkhon-cliffs.jpg", 1920, 1276, "Golden cliffs glowing at sunset over a calm wide lake", "60% 50%",
               '<a href="https://commons.wikimedia.org/wiki/File:Olkhon_Island,_Capes,_cliffs_at_sunset,_Lake_Baikal,_Russia.jpg">Vyacheslav Argenberg</a> (CC BY 4.0, Wikimedia Commons)'),
    "coast": ("howth-cliffs.jpg", 1920, 1440, "Yellow gorse above sea cliffs and a calm blue bay", "50% 50%",
              '<a href="https://commons.wikimedia.org/wiki/File:Gorse_at_Howth_Head_cliffs.jpg">Kiptoo Glen</a> (CC BY-SA 4.0, Wikimedia Commons)'),
}


def img(key, eager=False, pos=None):
    f, w, h, alt, p, _ = PHOTOS[key]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{IMG}/{f}" width="{w}" height="{h}" alt="{alt}" {load} style="object-position: {pos or p}">'


def credits(keys):
    """Credit line for library photographs; Gary's own photographs (credit None) need none."""
    named = [PHOTOS[k][5] for k in keys if PHOTOS[k][5]]
    return ("Photographs: " + ", ".join(named) + ".") if named else ""


SCRIPT = r"""<script>
window.hallmarkSlots = (m) => { for (const [k, v] of Object.entries(m)) { const s = document.querySelector(`[data-slot="${k}"]`); if (!s) continue; const im = new Image(); im.src = typeof v === 'string' ? v : v.src; im.alt = (typeof v === 'object' && v.alt) || s.dataset.alt || ''; s.querySelectorAll(':scope > img').forEach((o) => o.remove()); s.prepend(im); } };
document.querySelectorAll('[data-slot] img').forEach((i) => { if (i.complete && !i.naturalWidth) i.remove(); else i.addEventListener('error', () => i.remove(), { once: true }); });
(() => {
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Run fn once the visitor is actually looking at this tab. No observers: nothing here may depend on one to become visible.
  const whenSeen = (el, fn) => {
    let done = false;
    const go = () => { if (done || document.visibilityState !== 'visible') return; done = true; fn(); };
    go(); document.addEventListener('visibilitychange', go); window.addEventListener('focus', go); window.addEventListener('pageshow', go);
  };
  // Split a heading into letters (words stay unbreakable); screen readers get the plain text.
  const split = (el, cls) => {
    const text = el.textContent.trim(), chars = [];
    el.setAttribute('aria-label', text); el.textContent = '';
    text.split(' ').forEach((word, i, all) => {
      const w = document.createElement('span'); w.className = 'ch-word'; w.setAttribute('aria-hidden', 'true');
      [...word].forEach((c) => { const s = document.createElement('span'); s.className = cls; s.textContent = c; s.style.setProperty('--i', chars.length); w.append(s); chars.push(s); });
      el.append(w); if (i < all.length - 1) el.append(' ');
    });
    return chars;
  };
  // Greeting, option 1: it types itself once.
  document.querySelectorAll('[data-type]').forEach((el) => {
    if (calm) return;
    const chars = split(el, 'type__ch'); let n = 0, busy = false;
    const step = () => {
      if (n > 0) chars[n - 1].classList.remove('is-caret');
      chars[n].classList.add('is-on', 'is-caret');
      if (++n < chars.length) return setTimeout(step, 120);
      const last = chars[chars.length - 1]; last.classList.add('is-done'); busy = false;
      setTimeout(() => { if (!busy) last.classList.remove('is-caret', 'is-done'); }, 4600);
    };
    const run = () => { if (busy) return; busy = true; n = 0; chars.forEach((c) => c.classList.remove('is-on', 'is-caret', 'is-done')); setTimeout(step, 500); };
    whenSeen(el, run);
    el.addEventListener('click', run); // click the greeting to watch it type again
  });
  // Greeting, option 2: the letters rise in, one after another.
  document.querySelectorAll('[data-rise]').forEach((el) => {
    if (calm) return;
    split(el, 'rise__ch');
    whenSeen(el, () => setTimeout(() => el.classList.add('is-in'), 300));
  });
  // Items that fade up one by one when they come on screen.
  document.querySelectorAll('[data-reveal]').forEach((el) => whenSeen(el, () => el.classList.add('is-in')));
  // The background scene drifts a few pixels against the pointer.
  document.querySelectorAll('[data-parallax]').forEach((el) => {
    if (calm || !matchMedia('(pointer: fine)').matches) return;
    let raf = 0;
    window.addEventListener('pointermove', (e) => {
      if (raf) return;
      raf = requestAnimationFrame(() => { raf = 0; el.style.translate = `${(e.clientX / innerWidth - 0.5) * -18}px ${(e.clientY / innerHeight - 0.5) * -12}px`; });
    });
  });
  // Keyboard shortcuts: an element with data-key="a" is opened by pressing A.
  const keys = {}; document.querySelectorAll('[data-key]').forEach((el) => { keys[el.dataset.key] = el; });
  if (Object.keys(keys).length) document.addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    const el = keys[e.key.toLowerCase()]; if (el) { e.preventDefault(); el.focus(); el.click(); }
  });
  // One chooser: links switch the pane on hover and focus, buttons on click.
  document.querySelectorAll('[data-explore]').forEach((root) => {
    const picks = [...root.querySelectorAll('[data-show]')], panes = [...root.querySelectorAll('[data-pane]')];
    const show = (k) => {
      picks.forEach((p) => { const on = p.dataset.show === k; p.classList.toggle('is-on', on); if (p.tagName === 'BUTTON') p.setAttribute('aria-pressed', on); });
      panes.forEach((p) => p.classList.toggle('is-on', p.dataset.pane === k));
    };
    picks.forEach((p) => {
      if (p.tagName === 'BUTTON') p.addEventListener('click', () => show(p.dataset.show));
      else ['pointerenter', 'focus'].forEach((e) => p.addEventListener(e, () => show(p.dataset.show)));
    });
  });
})();
</script>"""


def page(title, fonts, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="description" content="Gary Mu: data scientist, traveller and runner. His apps, resume and where to find him." />
<meta name="robots" content="noindex" />
{fonts}
<link rel="stylesheet" href="site.css" />
<script>document.documentElement.classList.add('js');</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{body}
{SCRIPT}
</body>
</html>
"""


def app_rows(cls="app", apps=None):
    return "\n".join(
        f'<li><a class="{cls}" href="{u}"><span class="{cls}__name">{n}</span><span class="{cls}__what">{d}</span><span class="{cls}__host label">{h}</span></a></li>'
        for u, n, d, h in (APPS if apps is None else apps))


def apps_block():
    """The current apps, then an Archive that opens to show the older ones."""
    return f"""<ul class="applist">
{app_rows(apps=APPS_MAIN)}
</ul>
<details class="archive">
<summary><span class="archive__title">Archive</span><span class="label">{len(APPS_ARCHIVE)} older apps</span></summary>
<ul class="applist">
{app_rows(apps=APPS_ARCHIVE)}
</ul>
</details>"""


def foot_links(apps="#apps"):
    return f"""<ul class="foot__links">
<li><a href="{LINKEDIN}">LinkedIn</a></li>
<li><a href="{RESUME}">Resume</a></li>
<li><a href="{apps}">My apps</a></li>
<li><a href="{INSTA}">Instagram</a></li>
<li><a href="{STRAVA}">Strava</a></li>
</ul>"""


def nav():
    return f"""<header class="nav"><div class="container"><div class="nav__in">
<a class="nav__mark" href="#main">Gary Mu</a>
<ul class="nav__links"><li><a href="#apps">Apps</a></li><li><a href="{RESUME}">Resume</a></li></ul>
</div></div></header>"""


SHARED = """
.skip { position: absolute; left: var(--space-md); top: calc(-1 * var(--space-3xl)); z-index: var(--z-toast); padding: var(--space-xs) var(--space-md); background: var(--color-ink); color: var(--color-paper); }
.skip:focus-visible { top: var(--space-md); }
.ch-word { white-space: nowrap; }
.type__ch { position: relative; }
.js .type__ch { opacity: 0; }
.js .type__ch.is-on { opacity: 1; }
.type__ch.is-caret::after { content: ""; position: absolute; left: calc(100% + 0.04em); bottom: 0.12em; width: 0.07em; height: 0.78em; background: var(--color-accent); }
.type__ch.is-caret.is-done::after { animation: caret-blink 0.9s steps(1) 5; }
@keyframes caret-blink { 50% { opacity: 0; } }
.rise__ch { display: inline-block; }
.js .rise__ch { opacity: 0; translate: 0 0.4em; transition: opacity var(--dur-long) var(--ease-out), translate var(--dur-long) var(--ease-out); transition-delay: calc(var(--i, 0) * 45ms); }
.js .is-in > .ch-word > .rise__ch { opacity: 1; translate: none; }
.js [data-reveal] > * { opacity: 0; translate: 0 10px; transition: opacity var(--dur-long) var(--ease-out), translate var(--dur-long) var(--ease-out); transition-delay: calc(var(--i, 0) * 140ms + 1400ms); }
.js [data-reveal].is-in > * { opacity: 1; translate: none; }
.keys { display: none; }
@media (hover: hover) and (pointer: fine) { .js .keys { display: block; } }
.keys kbd { display: inline-block; min-width: 1.6em; padding: 0 0.35em; border: 1px solid currentColor; border-radius: 4px; font: inherit; font-weight: 500; text-align: center; }
@media (prefers-reduced-motion: reduce) { .js .type__ch, .js .rise__ch { opacity: 1; translate: none; } .type__ch.is-caret::after { display: none; } .js [data-reveal] > * { opacity: 1; translate: none; transition: none; } }
.label { font-size: var(--text-sm); font-weight: 500; line-height: 1.3; }
.nav__in { display: flex; align-items: center; justify-content: space-between; gap: var(--space-lg); min-height: 60px; }
.nav__mark { font-family: var(--font-display); font-weight: var(--display-weight); font-size: var(--text-lg); text-decoration: none; white-space: nowrap; }
.nav__links, .foot__links, .applist, .picks { margin: 0; padding: 0; list-style: none; }
.nav__links { display: flex; gap: var(--space-lg); }
.nav__links a, .foot__links a { display: inline-flex; align-items: center; min-height: 44px; font-weight: 500; }
.foot__links { display: flex; flex-wrap: wrap; gap: var(--space-xs) var(--space-lg); }
.foot__row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-md) var(--space-lg); }
.foot__credits { max-width: none; margin-top: var(--space-md); padding-top: var(--space-md); font-size: var(--text-sm); }
.foot small { font-size: var(--text-sm); }
.hero__actions { display: flex; flex-wrap: wrap; gap: var(--space-sm); }
.btn { display: inline-flex; align-items: center; justify-content: center; text-decoration: none; white-space: nowrap; cursor: pointer; }
.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.btn:disabled, .btn[aria-disabled="true"] { opacity: 0.55; cursor: not-allowed; }
.panes { position: relative; margin: 0; overflow: hidden; }
.pane { position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; opacity: 0; visibility: hidden; transition: opacity var(--dur-long) var(--ease-out), visibility 0s linear var(--dur-long); }
.pane.is-on { opacity: 1; visibility: visible; transition: opacity var(--dur-long) var(--ease-out); }
@media (prefers-reduced-motion: reduce) { .pane, .pane.is-on { transition: none; } }
.apps__head { display: grid; grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); align-items: end; gap: var(--gap-columns); margin-bottom: var(--space-xl); }
.apps__head p { justify-self: end; }
.apps__head b { font-weight: 500; }
.app { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 5fr) minmax(0, 2fr); align-items: center; gap: var(--gap-columns); min-height: 92px; padding-block: var(--space-md); text-decoration: none; }
.app__name { font-family: var(--font-display); font-weight: var(--display-weight); font-size: var(--text-xl); line-height: 1.15; letter-spacing: var(--tracking-display); }
.app__host { justify-self: end; text-align: right; }
.app:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.archive { border-top: var(--rule-hair) solid var(--color-rule); border-bottom: var(--rule-hair) solid var(--color-rule); }
.applist + .archive { border-top: 0; }
.archive summary { display: flex; align-items: center; gap: var(--space-md); min-height: 76px; cursor: pointer; list-style: none; }
.archive summary::-webkit-details-marker { display: none; }
.archive__title { font-family: var(--font-display); font-weight: var(--display-weight); font-size: var(--text-xl); letter-spacing: var(--tracking-display); line-height: 1.15; }
.archive summary::after { content: "+"; margin-left: auto; font-size: var(--text-xl); line-height: 1; }
.archive[open] summary::after { content: "\\2013"; }
.archive summary:hover .archive__title { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.2em; }
.archive summary:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.archive .applist { border-top: var(--rule-hair) solid var(--color-rule); border-bottom: 0; }
.archive .applist li:last-child { border-bottom: 0; }
@media (max-width: 60rem) {
  .apps__head { grid-template-columns: minmax(0, 1fr); gap: var(--space-md); }
  .apps__head p { justify-self: start; }
  .app { grid-template-columns: minmax(0, 1fr); gap: var(--space-2xs); }
  .app__host { justify-self: start; text-align: left; }
}
@media (max-width: 40rem) { .hero__actions, .hero__actions .btn { width: 100%; } }
"""

# ------------------------------------------------------------------ Dusk
DUSK_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /><link href="https://fonts.googleapis.com/css2?family=Wix+Madefor+Display:wght@400;500;600&family=Wix+Madefor+Text:wght@400;500;600&display=swap" rel="stylesheet" />'
DUSK_CSS = """/* Hallmark · shape: Photographic · genre: modern-minimal · theme: Dusk (by request) · job: hire · draw: manual
 * hero: Poster · nav: floating glass pill · footer: mast over a photograph · imagery: photographs · signature: three roles in a ruled list, and one pane beside it that cross-fades to the role you point at · dusk: shore/periwinkle-apricot/well
 * axes: dark/grotesk-sans/cool · posture: committed · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H4 E4 S4 R4 V5 · weakest: H, the calm head competes with the cliffs; set it on the fog scrim over the water, away from the lit rock */
/* Hallmark · dismissed 29 · smoked glass with a lit top edge is the Dusk theme's own nav surface, and it sits only over the cliff photograph */
/* Hallmark · dismissed 40 · the hero head is dark day-ink on a pale fog scrim over the photograph, not on the slate paper the static check assumes */
/* Hallmark · waive 59 · the closing road photograph sits 24px above the slate footer links · the photograph and the footer links are one closing unit for Gary's name */
/* Hallmark · dismissed 77 · the site holds a greeting, three roles, five apps and five links; more sections would mean inventing content about Gary */
@import url("./tokens.css");
@import url("./base.css");
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.04; }
body { font-size: 1.0625rem; }
""" + SHARED + """
.nav { position: absolute; inset: var(--space-md) 0 auto; z-index: var(--z-sticky-nav); }
.nav__in { padding-inline: var(--space-lg); border-radius: var(--radius-pill); background: var(--glass); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.35); backdrop-filter: blur(var(--glass-blur)) saturate(1.35); box-shadow: var(--glass-hi); }
.nav__links a:hover, .foot__links a:hover { color: var(--color-accent-hi); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-pill); font-family: var(--font-body); font-weight: 600; font-size: var(--text-md); line-height: 1; transition: background-color var(--dur-short) var(--ease-out), box-shadow var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); box-shadow: inset 0 1px 0 color-mix(in oklab, var(--color-light) 35%, transparent); }
.btn--primary:hover { background: var(--color-accent-hi); box-shadow: 0 0 0 4px color-mix(in oklab, var(--color-accent) 30%, transparent); }
.btn--primary:active { background: var(--color-accent-soft); }
.btn--ghost { background: color-mix(in oklab, var(--color-fog) 70%, transparent); color: var(--color-day-ink); -webkit-backdrop-filter: blur(12px); backdrop-filter: blur(12px); }
.btn--ghost:hover { background: var(--color-fog); }
.btn--ghost:active { background: var(--color-well-2); }

.hero { position: relative; display: grid; align-items: center; min-height: max(100svh, 560px); background: var(--color-paper); color: var(--color-day-ink); }
.hero__photo { position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; }
.hero__scrim { position: absolute; inset: 0; z-index: 2; pointer-events: none; background: radial-gradient(ellipse 46% 52% at 22% 54%, color-mix(in oklab, var(--color-fog) 82%, transparent), transparent 80%), linear-gradient(to bottom, transparent 76%, var(--color-paper)); }
.hero__in { position: relative; z-index: 3; display: grid; gap: var(--space-lg); justify-items: start; padding-block: var(--space-4xl) var(--space-3xl); }
.hero h1 { max-width: 9ch; font-size: clamp(3.25rem, 7vw, 7rem); }
.hero .lead { color: var(--color-day-ink); }

.roles { padding-block: var(--section-gap-s) 0; }
.roles__in { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: var(--space-2xl); align-items: center; }
.picks { border-top: var(--rule-hair) solid var(--color-rule); }
.picks li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.pick { display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-md); min-height: 120px; padding-block: var(--space-lg); color: var(--color-muted); text-decoration: none; transition: color var(--dur-short) var(--ease-out); }
.pick__name { font-family: var(--font-display); font-weight: var(--display-weight); font-size: var(--text-section); letter-spacing: var(--tracking-display); line-height: 1.05; }
.pick.is-on, .pick:hover { color: var(--color-ink); }
.pick.is-on .label { color: var(--color-accent); }
.pick:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 4px; }
.panes { aspect-ratio: 5 / 4; min-height: 440px; border-radius: var(--radius-card); background: var(--color-paper-2); box-shadow: var(--shadow-card); }
.pane--well { display: grid; place-items: center; padding: var(--space-xl); background: var(--color-well); }
.wellcard { width: min(100%, 26rem); padding: var(--space-lg) var(--space-xl); border-radius: var(--radius-inner); background: var(--color-card); color: var(--color-well-ink); }
.wellcard ul { margin: 0; padding: 0; list-style: none; }
.wellcard li { padding-block: var(--space-sm); border-bottom: var(--rule-hair) solid var(--color-well-rule); font-weight: 500; }
.wellcard li:last-child { border-bottom: 0; }
.wellcard .label { display: block; padding-bottom: var(--space-xs); color: var(--color-well-muted); }

.apps { padding-block: var(--section-gap) var(--section-gap); }
.apps__head p { color: var(--color-muted); }
.apps__head b { color: var(--color-ink); }
.applist { border-top: var(--rule-hair) solid var(--color-rule); }
.applist li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.app { padding-inline: var(--space-md); color: var(--color-ink); border-radius: var(--radius-inner); transition: background-color var(--dur-short) var(--ease-out); }
.app:hover { background: var(--color-paper-2); }
.app:active { background: var(--color-paper-3); }
.app:hover .app__name { color: var(--color-accent-hi); }
.app__what, .app__host { color: var(--color-muted); }

.close { position: relative; display: grid; align-items: end; min-height: min(64svh, 600px); }
.close__photo { position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; }
.close__scrim { position: absolute; inset: 0; z-index: 2; background: linear-gradient(to bottom, var(--color-paper), transparent 30%, transparent 55%, var(--color-paper)); }
.close__in { position: relative; z-index: 3; padding-block: var(--space-lg); }
.close__mark { font-family: var(--font-display); font-weight: var(--display-weight); font-size: clamp(3.5rem, 12vw, 11rem); letter-spacing: var(--tracking-display); line-height: 0.95; }
.foot { padding-block: var(--space-lg) var(--space-xl); }
.foot small, .foot__credits { color: var(--color-muted); }
.foot__credits { border-top: var(--rule-hair) solid var(--color-rule); }
@media (max-width: 60rem) {
  .roles__in { grid-template-columns: minmax(0, 1fr); gap: var(--space-xl); }
  .pick { min-height: 84px; }
  .panes { min-height: 0; }
}
"""


def dusk():
    apps_card = "".join(f"<li>{n}</li>" for _, n, _, _ in APPS)
    body = f"""{nav()}
<main id="main">
<section class="hero">
<figure class="hero__photo" data-slot="hero" data-alt="A place Gary has travelled, at dusk, with open sky or water on the left">{img('cliffs', True)}</figure>
<div class="hero__scrim"></div>
<div class="container hero__in">
<h1>Hi! I’m Gary Mu.</h1>
<p class="lead">Welcome to my world.</p>
<div class="hero__actions"><a class="btn btn--primary" href="#apps">My apps</a><a class="btn btn--ghost" href="{RESUME}">Resume</a></div>
</div>
</section>
<section class="roles">
<div class="container roles__in" data-explore>
<ul class="picks">
<li><a class="pick is-on" data-show="work" href="{LINKEDIN}"><span class="pick__name">Data scientist</span><span class="label">LinkedIn</span></a></li>
<li><a class="pick" data-show="travel" href="{INSTA}"><span class="pick__name">Traveller</span><span class="label">Instagram</span></a></li>
<li><a class="pick" data-show="run" href="{STRAVA}"><span class="pick__name">Runner</span><span class="label">Strava</span></a></li>
</ul>
<div class="panes">
<div class="pane pane--well is-on" data-pane="work"><div class="wellcard"><span class="label">Apps I made</span><ul>{apps_card}</ul></div></div>
<figure class="pane" data-pane="travel" data-slot="traveller" data-alt="One of Gary's own travel photographs">{img('road')}</figure>
<figure class="pane" data-pane="run" data-slot="runner" data-alt="Gary running outdoors">{img('trail')}</figure>
</div>
</div>
</section>
<section class="apps" id="apps">
<div class="container">
<div class="apps__head"><h2>Apps I made</h2>{LOGIN}</div>
{apps_block()}
</div>
</section>
</main>
<section class="close">
<figure class="close__photo" data-slot="close" data-alt="A road Gary has travelled, running out toward mountains">{img('peaks')}</figure>
<div class="close__scrim"></div>
<div class="container close__in"><p class="close__mark">Gary Mu</p></div>
</section>
<footer class="foot"><div class="container">
<div class="foot__row">{foot_links()}<small>&copy; Copyright Gary Mu 2026</small></div>
<p class="foot__credits" data-credits>{credits(['cliffs', 'road', 'trail', 'peaks'])}</p>
</div></footer>"""
    return page("Gary Mu · Dusk preview", DUSK_FONTS, body), DUSK_CSS


# ------------------------------------------------------------------ Garden
GARDEN_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /><link href="https://fonts.googleapis.com/css2?family=Vollkorn:wght@600&family=Hanken+Grotesk:wght@400;500&family=Newsreader:opsz,wght@6..72,400&display=swap" rel="stylesheet" />'
GARDEN_CSS = """/* Hallmark · shape: Split Studio · genre: editorial · theme: Garden (by request) · job: hire · draw: manual
 * hero: Stage · nav: edge-aligned on a hairline · footer: statement on green ink · imagery: photographs · signature: one large daylight photograph beside the greeting that you change with four place buttons, its caption changing with it
 * axes: light/roman-serif/chromatic-green · posture: committed · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H5 E4 S4 R5 V5 · weakest: P, a warm page that says little; let the visitor choose the view, so the page answers where Gary goes rather than describing it */
/* Hallmark · dismissed 77 · the site holds a greeting, three roles, five apps and five links; more sections would mean inventing content about Gary */
@import url("./tokens.css");
@import url("./base.css");
body { font-size: 1.0625rem; font-variant-numeric: oldstyle-nums; color: var(--color-ink-2); }
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.04; color: var(--color-ink); }
""" + SHARED + """
.nav { border-bottom: var(--rule-hair) solid var(--color-rule); }
.nav__in { min-height: 72px; color: var(--color-ink); }
.nav__links a, .role__where { text-decoration-color: var(--color-rule-2); transition: text-decoration-color var(--dur-short) var(--ease-out); }
.nav__links a:hover { text-decoration-color: var(--color-accent); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: var(--rule-hair) solid var(--color-rule-2); border-radius: var(--radius-pill); background: none; color: var(--color-ink); font-family: var(--font-body); font-weight: 500; font-size: var(--text-md); line-height: 1; transition: background-color var(--dur-short) var(--ease-out), border-color var(--dur-short) var(--ease-out); }
.btn:hover { background: var(--color-paper-2); border-color: var(--color-muted); }
.btn:active { background: var(--color-paper-3); }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-ink-2); border-color: var(--color-ink-2); }
.btn--primary:active { background: var(--color-ink); border-color: var(--color-ink); }

.hero__in { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: var(--space-2xl); align-items: center; min-height: calc(100svh - 73px); padding-block: var(--space-xl); }
.hero__text { display: grid; gap: var(--space-lg); justify-items: start; }
.hero h1 { font-size: clamp(3.25rem, 6.4vw, 6.5rem); }
.view { display: grid; gap: var(--space-md); min-width: 0; }
.panes { aspect-ratio: 4 / 3; max-height: 66svh; width: 100%; border-radius: var(--radius-card); outline: var(--rule-hair) solid var(--color-rule); outline-offset: -1px; background: var(--color-paper-2); }
.view__bar { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-sm) var(--space-lg); }
.picks { display: flex; flex-wrap: wrap; gap: var(--space-xs); }
.pick { min-height: 44px; padding: 0 var(--space-md); border: var(--rule-hair) solid var(--color-rule-2); border-radius: var(--radius-pill); background: none; color: var(--color-ink); font-weight: 500; font-size: var(--text-sm); cursor: pointer; transition: background-color var(--dur-short) var(--ease-out), color var(--dur-short) var(--ease-out); }
.pick:hover { background: var(--color-paper-2); }
.pick:active { background: var(--color-paper-3); }
.pick.is-on { background: var(--color-ink); border-color: var(--color-ink); color: var(--color-paper); }
.pick:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.captions { position: relative; min-height: 1.4em; flex: 1 1 14rem; text-align: right; }
.caption { position: absolute; inset: 0 0 auto auto; opacity: 0; font: 400 var(--text-sm)/1.4 var(--font-outlier); color: var(--color-muted); transition: opacity var(--dur-long) var(--ease-out); }
.caption.is-on { opacity: 1; }
html:not(.js) .picks { display: none; }

.roles { padding-block: var(--section-gap-s); background: var(--tint-moss); }
.roles__list { margin: 0; padding: 0; list-style: none; border-top: var(--rule-hair) solid var(--color-rule-2); }
.roles__list li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.role { display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-lg); min-height: 128px; padding-block: var(--space-lg); color: var(--color-ink); text-decoration: none; }
.role__name { font-family: var(--font-display); font-weight: var(--display-weight); font-size: var(--text-display-s); letter-spacing: var(--tracking-display); line-height: 1.04; transition: translate var(--dur-short) var(--ease-out); }
.role:hover .role__name { translate: var(--space-sm) 0; }
.role__where { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 0.25em; }
.role:hover .role__where { text-decoration-color: var(--color-accent); }
.role:active { color: var(--color-accent); }
.role:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 4px; }
@media (prefers-reduced-motion: reduce) { .role:hover .role__name { translate: none; } }

.apps { padding-block: var(--section-gap) var(--section-gap); }
.applist { border-top: var(--rule-hair) solid var(--color-rule-2); }
.applist li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.app { color: var(--color-ink); }
.app__name { transition: color var(--dur-short) var(--ease-out); }
.app:hover .app__name { color: var(--color-accent); }
.app:active .app__name { color: var(--color-ink-2); }
.app__what { color: var(--color-ink-2); }
.app__host { color: var(--color-muted); }

.foot { padding-block: var(--section-gap-s) var(--space-xl); background: var(--color-ink); color: var(--color-paper); }
.foot__mark { font-family: var(--font-display); font-weight: var(--display-weight); font-size: clamp(3.5rem, 11vw, 10rem); letter-spacing: var(--tracking-display); line-height: 1; color: var(--color-paper); }
.foot__row { margin-top: var(--space-2xl); }
.foot__links a { text-decoration-color: var(--color-accent-2); }
.foot__links a:hover { color: var(--color-accent-2); }
.foot a:focus-visible { outline-color: var(--color-accent-2); }
.foot small, .foot__credits { color: var(--color-paper-3); }
.foot__credits { border-top: var(--rule-hair) solid var(--color-ink-2); }
@media (max-width: 60rem) {
  .hero__in { grid-template-columns: minmax(0, 1fr); gap: var(--space-xl); min-height: 0; }
  .panes { max-height: none; }
  .captions { text-align: left; flex-basis: 100%; }
  .caption { inset: 0 auto auto 0; }
  .role { min-height: 96px; }
}
"""


def garden():
    views = [("lake", "Lake", "A still lake under snowy peaks, early morning."),
             ("road", "Road", "A mountain road up a green valley."),
             ("trail", "Trail", "A dirt trail through a summer meadow."),
             ("coast", "Coast", "Gorse above sea cliffs and a calm bay.")]
    panes = "\n".join(
        f'<figure class="pane{" is-on" if i == 0 else ""}" data-pane="{k}" data-slot="view-{k}" data-alt="One of Gary\'s own photographs: {lab.lower()}">{img(k, i == 0)}</figure>'
        for i, (k, lab, _) in enumerate(views))
    picks = "".join(
        f'<li><button class="pick{" is-on" if i == 0 else ""}" type="button" data-show="{k}" aria-pressed="{"true" if i == 0 else "false"}">{lab}</button></li>'
        for i, (k, lab, _) in enumerate(views))
    caps = "".join(f'<span class="caption pane-cap{" is-on" if i == 0 else ""}" data-pane="{k}">{c}</span>' for i, (k, _, c) in enumerate(views))
    body = f"""{nav()}
<main id="main">
<section class="hero">
<div class="container hero__in">
<div class="hero__text">
<h1 data-type>Hi! I’m Gary Mu.</h1>
<p class="lead">Welcome to my world.</p>
<div class="hero__actions"><a class="btn btn--primary" href="#apps">My apps</a><a class="btn" href="{RESUME}">Resume</a></div>
</div>
<div class="view" data-explore>
<div class="panes">
{panes}
</div>
<div class="view__bar"><ul class="picks" aria-label="Choose a view">{picks}</ul><p class="captions">{caps}</p></div>
</div>
</div>
</section>
<section class="roles">
<div class="container">
<ul class="roles__list">
<li><a class="role" href="{LINKEDIN}"><span class="role__name">Data scientist</span><span class="role__where label">LinkedIn</span></a></li>
<li><a class="role" href="{INSTA}"><span class="role__name">Traveller</span><span class="role__where label">Instagram</span></a></li>
<li><a class="role" href="{STRAVA}"><span class="role__name">Runner</span><span class="role__where label">Strava</span></a></li>
</ul>
</div>
</section>
<section class="apps" id="apps">
<div class="container">
<div class="apps__head"><h2>Apps I made</h2>{LOGIN}</div>
{apps_block()}
</div>
</section>
</main>
<footer class="foot"><div class="container">
<p class="foot__mark">Gary Mu</p>
<div class="foot__row">{foot_links()}<small>&copy; Copyright Gary Mu 2026</small></div>
<p class="foot__credits" data-credits>{credits(['lake', 'road', 'trail', 'coast'])}</p>
</div></footer>"""
    return page("Gary Mu · Garden preview", GARDEN_FONTS, body), GARDEN_CSS


# ------------------------------------------------------------------ Hum
def torn(seed, n=44, depth=2.2):
    """A torn bottom edge as a clip-path polygon (percentages)."""
    r = random.Random(seed)
    pts = ["0% 0%", "100% 0%"]
    for i in range(n, -1, -1):
        x = 100 * i / n
        y = 100 - depth * (0.35 + r.random())
        pts.append(f"{x:.1f}% {y:.1f}%")
    return "polygon(" + ", ".join(pts) + ")"


HUM_FONTS = '<link rel="preconnect" href="https://api.fontshare.com" /><link href="https://api.fontshare.com/v2/css?f[]=chillax@500,600&display=swap" rel="stylesheet" />'
HUM_CSS = """/* Hallmark · shape: Split Studio · genre: playful · theme: Hum (by request) · job: hire · draw: manual
 * hero: Stage · nav: card-stock bar · footer: mast on the pear field · imagery: photographs · signature: the lake as a torn photograph pinned at a tilt that straightens when you reach for it, beside card-stock buttons that press
 * axes: light/rounded-sans/chromatic-yellow · posture: full-palette · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H4 E4 S4 R4 V5 · weakest: R, paper effects pile up fast; kept the tear to the photographs and the press to the controls, and left the apps list flat */
/* Hallmark · dismissed 77 · the site holds a greeting, three roles, five apps and five links; more sections would mean inventing content about Gary */
/* Hallmark · answered F4 · Hum's control pair is card stock for both buttons; only My apps takes the pear fill, Resume stays the plain cream card */
@import url("./tokens.css");
@import url("./base.css");
body { font-size: 1.0625rem; font-weight: 500; }
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.04; }
mark { padding: 0 0.15em; background: color-mix(in oklab, var(--color-accent) 60%, transparent); color: inherit; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
a { color: var(--color-accent-2); }
""" + SHARED + """
.nav { padding-top: var(--space-md); }
.nav__in { padding-inline: var(--space-lg); border-radius: var(--radius-stock); background: var(--color-card); box-shadow: inset 0 0 0 1px var(--color-rule), 0 4px 0 0 var(--color-edge); }
.nav__mark { color: var(--color-ink); }
.btn { --edge: 5px; min-height: 54px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-stock); background: var(--color-card); color: var(--color-ink); font-family: var(--font-body); font-weight: 600; font-size: var(--text-md); line-height: 1; box-shadow: inset 0 0 0 1px var(--color-rule), 0 var(--edge) 0 0 var(--color-edge); transition: translate var(--dur-micro) var(--ease-snap), box-shadow var(--dur-micro) var(--ease-snap); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); box-shadow: 0 var(--edge) 0 0 var(--color-accent-deep); transition-timing-function: var(--ease-spring); }
.btn:hover { --edge: 7px; translate: 0 -2px; }
.btn:active { --edge: 1px; translate: 0 4px; }
@media (prefers-reduced-motion: reduce) { .btn:hover, .btn:active { translate: none; } }

.hero__in { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: var(--space-3xl); align-items: center; min-height: calc(100svh - 80px); padding-block: var(--space-xl) var(--space-2xl); }
.hero__text { display: grid; gap: var(--space-lg); justify-items: start; }
.hero h1 { font-size: clamp(3.25rem, 6.6vw, 6.75rem); }
.sheet { filter: var(--shadow-paper); rotate: -2.5deg; transition: rotate var(--dur-long) var(--ease-snap); }
.sheet:hover { rotate: 0deg; }
.sheet__cut { margin: 0; aspect-ratio: 4 / 3; max-height: 68svh; width: 100%; padding: var(--space-sm) var(--space-sm) var(--space-xl); background: var(--color-fringe); clip-path: TORN_A; }
.sheet__cut > span { display: block; position: relative; width: 100%; height: 100%; overflow: hidden; border-radius: var(--space-2xs); }
@media (prefers-reduced-motion: reduce) { .sheet, .sheet:hover { rotate: 0deg; transition: none; } }

.roles { padding-block: var(--section-gap-s); background: var(--color-paper-2); }
.roles__grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--gap-columns); margin: 0; padding: 0; list-style: none; }
.roles__grid li { display: grid; min-width: 0; }
.role { --edge: 6px; display: grid; grid-template-rows: 1fr auto; gap: var(--space-md); padding: var(--space-sm) var(--space-sm) var(--space-lg); border-radius: var(--radius-card); background: var(--color-card); color: var(--color-ink); text-decoration: none; box-shadow: inset 0 0 0 1px var(--color-rule), 0 var(--edge) 0 0 var(--color-edge); transition: translate var(--dur-short) var(--ease-snap), box-shadow var(--dur-short) var(--ease-snap); }
.role:hover { --edge: 10px; translate: 0 -4px; }
.role:active { --edge: 2px; translate: 0 4px; }
.role:focus-visible { outline: 3px solid var(--color-focus); outline-offset: 3px; }
.role__pic { display: block; position: relative; min-height: 300px; overflow: hidden; border-radius: var(--radius-stock); }
.role__pic--fill { background: var(--color-accent-3); }
.role__text { display: grid; gap: var(--space-2xs); padding-inline: var(--space-sm); }
.role__name { font-family: var(--font-display); font-weight: 600; font-size: var(--text-2xl); letter-spacing: var(--tracking-display); line-height: 1.1; }
.role__where { color: var(--color-accent-2); }
@media (prefers-reduced-motion: reduce) { .role:hover, .role:active { translate: none; } }

.apps { padding-block: var(--section-gap) var(--section-gap); }
.apps__head p { color: var(--color-ink-2); }
.applist { border-top: 2px solid var(--color-ink); }
.applist li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.app { padding-inline: var(--space-md); color: var(--color-ink); border-radius: var(--radius-stock); transition: background-color var(--dur-micro) var(--ease-snap); }
.app:hover { background: color-mix(in oklab, var(--color-accent) 45%, transparent); }
.app:active { background: var(--color-accent); }
.app__what { color: var(--color-ink-2); }
.app__host { color: var(--color-muted); }

.foot { padding-block: var(--section-gap-s) var(--space-xl); background: var(--color-accent); color: var(--color-accent-ink); }
.foot__mark { font-family: var(--font-display); font-weight: 600; font-size: clamp(3.5rem, 12vw, 11rem); letter-spacing: var(--tracking-display); line-height: 1; }
.foot__row { margin-top: var(--space-xl); }
.foot a { color: var(--color-ink); }
.foot a:hover { color: var(--color-accent-2); }
.foot small, .foot__credits { color: var(--color-ink-2); }
.foot__credits { border-top: var(--rule-hair) solid var(--color-accent-deep); }
@media (max-width: 60rem) {
  .hero__in { grid-template-columns: minmax(0, 1fr); gap: var(--space-xl); min-height: 0; }
  .sheet__cut { max-height: none; }
  .roles__grid { grid-template-columns: minmax(0, 1fr); gap: var(--space-lg); }
  .role__pic { min-height: 220px; }
}
"""


def hum():
    body = f"""{nav()}
<main id="main">
<section class="hero">
<div class="container hero__in">
<div class="hero__text">
<h1>Hi! I’m Gary Mu.</h1>
<p class="lead">Welcome to <mark>my world</mark>.</p>
<div class="hero__actions"><a class="btn btn--primary" href="#apps">My apps</a><a class="btn" href="{RESUME}">Resume</a></div>
</div>
<div class="sheet"><figure class="sheet__cut"><span data-slot="hero" data-alt="A place Gary has travelled or run, wide">{img('lake', True)}</span></figure></div>
</div>
</section>
<section class="roles">
<div class="container">
<ul class="roles__grid">
<li><a class="role" href="{LINKEDIN}"><span class="role__pic role__pic--fill"></span><span class="role__text"><span class="role__name">Data scientist</span><span class="role__where label">LinkedIn</span></span></a></li>
<li><a class="role" href="{INSTA}"><span class="role__pic" data-slot="traveller" data-alt="One of Gary's own travel photographs">{img('road')}</span><span class="role__text"><span class="role__name">Traveller</span><span class="role__where label">Instagram</span></span></a></li>
<li><a class="role" href="{STRAVA}"><span class="role__pic" data-slot="runner" data-alt="Gary running outdoors">{img('trail')}</span><span class="role__text"><span class="role__name">Runner</span><span class="role__where label">Strava</span></span></a></li>
</ul>
</div>
</section>
<section class="apps" id="apps">
<div class="container">
<div class="apps__head"><h2>Apps I made</h2>{LOGIN}</div>
{apps_block()}
</div>
</section>
</main>
<footer class="foot"><div class="container">
<p class="foot__mark">Gary Mu</p>
<div class="foot__row">{foot_links()}<small>&copy; Copyright Gary Mu 2026</small></div>
<p class="foot__credits" data-credits>{credits(['lake', 'road', 'trail'])}</p>
</div></footer>"""
    return page("Gary Mu · Hum preview", HUM_FONTS, body), HUM_CSS.replace("TORN_A", torn(7))


# ------------------------------------------------------------------ one big scene
def scene_body(photo, greet_attr, fixed, parallax=False, keys=False):
    """One photograph behind the page; the greeting, two actions and three role links on top."""
    k_apps = ' data-key="a"' if keys else ""
    k_res = ' data-key="r"' if keys else ""
    k_li = ' data-key="l"' if keys else ""
    credit_line = credits([photo])
    credit_html = f'<p class="foot__credits" data-credits>{credit_line}</p>' if credit_line else ""
    hint = '<p class="keys label">Shortcuts: <kbd>A</kbd> apps, <kbd>R</kbd> resume, <kbd>L</kbd> LinkedIn</p>' if keys else ""
    par = " data-parallax" if parallax else ""
    scene = f"""<figure class="scene{' scene--fixed' if fixed else ''}"{par} data-slot="scene" data-alt="One wide nature photograph of Gary's own: calm, with open space on the left for the greeting">{img(photo, True)}</figure>
<div class="scene__scrim{' scene--fixed' if fixed else ''}"></div>"""
    hero = f"""<section class="hero">
{'' if fixed else scene}
<div class="container hero__in">
<div class="hero__text">
<h1 {greet_attr}>Hi! I’m Gary Mu.</h1>
<p class="lead">Welcome to my world.</p>
<div class="hero__actions"><a class="btn btn--primary" href="#apps"{k_apps}>My apps</a><a class="btn btn--ghost" href="{RESUME}"{k_res}>Resume</a><a class="btn btn--ghost" href="{LINKEDIN}"{k_li}>LinkedIn</a></div>
{hint}
</div>
</div>
<div class="container">
<ul class="dest" data-reveal>
<li style="--i:0"><a href="{LINKEDIN}"><span class="dest__name">Data scientist</span><span class="label">LinkedIn</span></a></li>
<li style="--i:1"><a href="{INSTA}"><span class="dest__name">Traveller</span><span class="label">Instagram</span></a></li>
<li style="--i:2"><a href="{STRAVA}"><span class="dest__name">Runner</span><span class="label">Strava</span></a></li>
</ul>
</div>
</section>"""
    return f"""{scene if fixed else ''}
<div class="page">
{nav()}
<main id="main">
{hero}
<section class="apps" id="apps">
<div class="container">
<div class="panel">
<div class="apps__head"><h2>Apps I made</h2>{LOGIN}</div>
{apps_block()}
</div>
</div>
</section>
</main>
<footer class="foot"><div class="container">
<p class="foot__mark">Gary Mu</p>
<div class="foot__row">{foot_links()}<small>&copy; Copyright Gary Mu 2026</small></div>
{credit_html}
</div></footer>
</div>"""


SCENE_SHARED = """
.scene { position: absolute; inset: 0; width: 100%; height: 100%; margin: 0; z-index: 0; }
.scene__scrim { position: absolute; inset: 0; z-index: 1; pointer-events: none; }
.scene--fixed { position: fixed; }
.scene.scene--fixed { inset: -24px; width: auto; height: auto; transition: translate 0.6s var(--ease-out); }
.page { position: relative; z-index: 2; }
.hero { position: relative; }
.hero { display: grid; grid-template-rows: 1fr auto; min-height: calc(100svh - 92px); padding-bottom: var(--space-xl); }
.hero > .container { position: relative; z-index: 3; }
.hero__in { display: grid; align-items: end; padding-block: var(--space-2xl) var(--space-xl); }
.hero__text { display: grid; gap: var(--space-lg); justify-items: start; }
.hero h1 { max-width: 10ch; font-size: clamp(3.25rem, 7vw, 7rem); }
.dest { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0 var(--gap-columns); margin: 0; padding: 0; list-style: none; }
.dest a { display: flex; align-items: baseline; justify-content: space-between; gap: var(--space-md); min-height: 76px; padding-block: var(--space-md); text-decoration: none; }
.dest__name { font-family: var(--font-display); font-weight: var(--display-weight); font-size: var(--text-xl); letter-spacing: var(--tracking-display); line-height: 1.1; transition: translate var(--dur-short) var(--ease-out); }
.dest a:hover .dest__name { translate: var(--space-xs) 0; }
.dest a:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.apps { padding-block: var(--section-gap-s) var(--section-gap); }
.foot__mark { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1; font-size: clamp(3rem, 9vw, 8rem); }
.foot__row { margin-top: var(--space-xl); }
@media (prefers-reduced-motion: reduce) { .scene.scene--fixed { transition: none; } .dest a:hover .dest__name { translate: none; } }
@media (max-width: 60rem) {
  .dest { grid-template-columns: minmax(0, 1fr); }
  .dest a { min-height: 60px; }
}
"""

SCENE_DUSK_CSS = """/* Hallmark · shape: Photographic · genre: modern-minimal · theme: Dusk (by request) · job: hire · draw: manual
 * hero: Poster · nav: floating glass pill · footer: mast · imagery: photographs · signature: one sunset shoreline held still behind the whole page while smoked-glass panels scroll over it · dusk: shore/periwinkle-apricot/glass
 * axes: dark/grotesk-sans/cool · posture: committed · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H5 E4 S4 R5 V5 · weakest: S, a single stock sunset could be anyone's; the slot is waiting for Gary's own photograph */
/* Hallmark · dismissed 29 · smoked glass with a lit top edge is the Dusk theme's own surface, and here it sits only over the one photograph */
/* Hallmark · dismissed 77 · the site holds a greeting, three roles, five apps and five links; more sections would mean inventing content about Gary */
@import url("./tokens.css");
@import url("./base.css");
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.04; }
body { font-size: 1.0625rem; }
""" + SHARED + SCENE_SHARED + """
.scene__scrim { background: linear-gradient(90deg, color-mix(in oklab, var(--color-shade) 78%, transparent), color-mix(in oklab, var(--color-shade) 30%, transparent) 60%, color-mix(in oklab, var(--color-shade) 12%, transparent)), linear-gradient(to top, color-mix(in oklab, var(--color-shade) 70%, transparent), transparent 40%); }
.glass { background: var(--glass); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.35); backdrop-filter: blur(var(--glass-blur)) saturate(1.35); box-shadow: var(--glass-hi), var(--shadow-card); }
.nav { padding-top: var(--space-md); }
.nav__in { padding-inline: var(--space-lg); border-radius: var(--radius-pill); background: var(--glass); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.35); backdrop-filter: blur(var(--glass-blur)) saturate(1.35); box-shadow: var(--glass-hi); }
.nav__links a:hover, .foot__links a:hover { color: var(--color-accent-hi); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-pill); font-family: var(--font-body); font-weight: 600; font-size: var(--text-md); line-height: 1; transition: background-color var(--dur-short) var(--ease-out), box-shadow var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); box-shadow: inset 0 1px 0 color-mix(in oklab, var(--color-light) 35%, transparent); }
.btn--primary:hover { background: var(--color-accent-hi); box-shadow: 0 0 0 4px color-mix(in oklab, var(--color-accent) 30%, transparent); }
.btn--primary:active { background: var(--color-accent-soft); }
.btn--ghost { background: color-mix(in oklab, var(--color-light) 10%, transparent); color: var(--color-ink); box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--color-light) 22%, transparent); }
.btn--ghost:hover { background: color-mix(in oklab, var(--color-light) 18%, transparent); }
.btn--ghost:active { background: color-mix(in oklab, var(--color-light) 26%, transparent); }
.hero .lead { color: var(--color-ink-2); }
.keys { color: var(--color-muted); }
.dest { padding: var(--space-xs) var(--space-lg); border-radius: var(--radius-card); background: var(--glass); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.35); backdrop-filter: blur(var(--glass-blur)) saturate(1.35); box-shadow: var(--glass-hi), var(--shadow-card); }
.dest li + li a { box-shadow: -1px 0 0 color-mix(in oklab, var(--color-light) 9%, transparent); }
.dest li a { padding-inline: var(--space-md); }
.dest a { color: var(--color-ink); }
.dest .label { color: var(--color-muted); }
.dest a:hover .label { color: var(--color-accent-hi); }
.panel { padding: var(--space-xl) var(--space-xl) var(--space-md); border-radius: var(--radius-card); background: var(--glass); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.35); backdrop-filter: blur(var(--glass-blur)) saturate(1.35); box-shadow: var(--glass-hi), var(--shadow-card); }
.apps__head p { color: var(--color-muted); }
.apps__head b { color: var(--color-ink); }
.applist li { border-top: 1px solid color-mix(in oklab, var(--color-light) 9%, transparent); }
.app { padding-inline: var(--space-md); margin-inline: calc(-1 * var(--space-md)); color: var(--color-ink); border-radius: var(--radius-inner); transition: background-color var(--dur-short) var(--ease-out); }
.app:hover { background: color-mix(in oklab, var(--color-light) 7%, transparent); }
.app:active { background: color-mix(in oklab, var(--color-light) 12%, transparent); }
.app:hover .app__name { color: var(--color-accent-hi); }
.app__what, .app__host { color: var(--color-ink-2); }
.foot { padding-block: var(--space-2xl) var(--space-xl); background: color-mix(in oklab, var(--color-paper) 88%, transparent); }
.foot small, .foot__credits { color: var(--color-muted); }
.foot__credits { border-top: var(--rule-hair) solid var(--color-rule); }
"""

SCENE_GARDEN_CSS = """/* Hallmark · shape: Photographic · genre: editorial · theme: Garden (by request) · job: hire · draw: manual
 * hero: Poster · nav: edge-aligned over the photograph · footer: statement on green ink · imagery: photographs · signature: one still lake at first light filling the first screen, the greeting typed across its reflection
 * axes: light/roman-serif/chromatic-green · posture: committed · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H5 E4 S4 R5 V5 · weakest: S, a single stock lake could be anyone's; the slot is waiting for Gary's own photograph */
/* Hallmark · dismissed 77 · the site holds a greeting, three roles, five apps and five links; more sections would mean inventing content about Gary */
@import url("./tokens.css");
@import url("./base.css");
body { font-size: 1.0625rem; font-variant-numeric: oldstyle-nums; color: var(--color-ink-2); }
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.04; color: var(--color-ink); }
""" + SHARED + SCENE_SHARED + """
.scene__scrim { background: linear-gradient(to bottom, color-mix(in oklab, var(--color-ink) 72%, transparent), transparent 22%), linear-gradient(to top, color-mix(in oklab, var(--color-ink) 84%, transparent), color-mix(in oklab, var(--color-ink) 42%, transparent) 55%, color-mix(in oklab, var(--color-ink) 30%, transparent)); }
.nav { position: absolute; inset: 0 0 auto; z-index: var(--z-sticky-nav); color: var(--color-paper); }
.nav__in { min-height: 76px; border-bottom: var(--rule-hair) solid color-mix(in oklab, var(--color-paper) 35%, transparent); }
.nav__links a { text-decoration-color: color-mix(in oklab, var(--color-paper) 50%, transparent); }
.nav__links a:hover { text-decoration-color: var(--color-accent-2); }
.nav a:focus-visible, .hero a:focus-visible { outline-color: var(--color-accent-2); }
.hero { color: var(--color-paper); }
.hero { min-height: 100svh; }
.hero__in { padding-top: var(--space-4xl); }
.hero h1 { color: var(--color-paper); }
.type__ch.is-caret::after { background: var(--color-accent-2); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: var(--rule-hair) solid var(--color-rule-2); border-radius: var(--radius-pill); background: none; color: var(--color-ink); font-family: var(--font-body); font-weight: 500; font-size: var(--text-md); line-height: 1; transition: background-color var(--dur-short) var(--ease-out), border-color var(--dur-short) var(--ease-out), color var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent-2); border-color: var(--color-accent-2); color: var(--color-ink); }
.btn--primary:hover { background: var(--color-paper); border-color: var(--color-paper); }
.btn--primary:active { background: var(--color-paper-3); border-color: var(--color-paper-3); }
.btn--ghost { border-color: color-mix(in oklab, var(--color-paper) 70%, transparent); color: var(--color-paper); }
.btn--ghost:hover { background: var(--color-paper); border-color: var(--color-paper); color: var(--color-ink); }
.btn--ghost:active { background: var(--color-paper-3); color: var(--color-ink); }
.dest li { border-top: var(--rule-hair) solid color-mix(in oklab, var(--color-paper) 55%, transparent); }
.dest a { color: var(--color-paper); }
.dest .label { text-decoration: underline; text-decoration-color: color-mix(in oklab, var(--color-paper) 50%, transparent); text-underline-offset: 0.25em; }
.dest a:hover .label { text-decoration-color: var(--color-accent-2); }
.applist { border-top: var(--rule-hair) solid var(--color-rule-2); }
.applist li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.app { color: var(--color-ink); }
.app__name { transition: color var(--dur-short) var(--ease-out); }
.app:hover .app__name { color: var(--color-accent); }
.app:active .app__name { color: var(--color-ink-2); }
.app__host { color: var(--color-muted); }
.foot { padding-block: var(--section-gap-s) var(--space-xl); background: var(--color-ink); color: var(--color-paper); }
.foot__mark { color: var(--color-paper); }
.foot__links a { text-decoration-color: var(--color-accent-2); }
.foot__links a:hover { color: var(--color-accent-2); }
.foot a:focus-visible { outline-color: var(--color-accent-2); }
.foot small, .foot__credits { color: var(--color-paper-3); }
.foot__credits { border-top: var(--rule-hair) solid var(--color-ink-2); }
"""

HEDGE_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin /><link href="https://fonts.googleapis.com/css2?family=Prata&family=Manrope:wght@400;500;700&display=swap" rel="stylesheet" />'
SCENE_HEDGE_CSS = """/* Hallmark · shape: Photographic · genre: editorial · theme: Hedgerow (by request) · job: hire · draw: manual
 * hero: Poster · nav: edge-aligned · footer: mast · imagery: photographs · signature: a dark forest lake held behind the page under a leaf-green wash, the greeting rising in letter by letter · hedgerow: hedge
 * axes: dark/high-contrast-serif/chromatic-lime · posture: committed · contrast: pass · fold: pass · v2.0.0 */
/* Hallmark · pre-emit critique: P4 H5 E4 S4 R5 V5 · weakest: S, a single stock lake could be anyone's; the slot is waiting for Gary's own photograph */
/* Hallmark · dismissed 77 · the site holds a greeting, three roles, five apps and five links; more sections would mean inventing content about Gary */
@import url("./tokens.css");
@import url("./base.css");
body { font-size: 1.0625rem; line-height: 1.6; color: var(--color-ink-2); }
h1, h2, h3 { font-family: var(--font-display); font-weight: 400; font-synthesis: none; letter-spacing: var(--tracking-display); line-height: 1.08; color: var(--color-ink); }
""" + SHARED + SCENE_SHARED + """
.scene__scrim { background: linear-gradient(90deg, color-mix(in oklab, var(--color-paper) 86%, transparent), color-mix(in oklab, var(--color-paper) 52%, transparent) 65%, color-mix(in oklab, var(--color-paper) 40%, transparent)); }
.nav { padding-top: var(--space-xs); }
.nav__in { min-height: 76px; border-bottom: var(--rule-hair) solid var(--color-muted); color: var(--color-ink); }
.nav__mark { font-weight: 400; }
.nav__links a, .foot__links a { text-decoration-color: var(--color-accent); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-pill); font-family: var(--font-body); font-weight: 700; font-size: var(--text-md); line-height: 1; transition: background-color var(--dur-short) var(--ease-out), color var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-2); }
.btn--primary:active { background: var(--color-ink); }
.btn--ghost { background: none; box-shadow: inset 0 0 0 1.5px var(--color-accent); color: var(--color-ink); }
.btn--ghost:hover { background: color-mix(in oklab, var(--color-accent) 16%, transparent); }
.btn--ghost:active { background: color-mix(in oklab, var(--color-accent) 28%, transparent); }
.keys { color: var(--color-muted); }
.dest li { border-top: 1.5px solid var(--color-accent); }
.dest a { color: var(--color-ink); }
.dest .label { color: var(--color-ink-2); }
.dest a:hover .label { color: var(--color-accent); }
.panel { padding: var(--space-xl) var(--space-xl) var(--space-md); background: var(--color-paper); color: var(--color-ink-2); }
.apps__head b { color: var(--color-ink); }
.applist { border-top: 1.5px solid var(--color-accent); }
.applist li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.archive { border-bottom: 0; }
.app { color: var(--color-ink); }
.app__name { font-weight: 400; transition: color var(--dur-short) var(--ease-out); }
.app:hover .app__name { color: var(--color-accent); }
.app:active .app__name { color: var(--color-accent-2); }
.app__host { color: var(--color-muted); }
.foot { padding-block: var(--space-2xl) var(--space-xl); background: var(--color-paper-2); color: var(--color-ink); }
.foot__mark { font-weight: 400; }
.foot small, .foot__credits { color: var(--color-muted); }
.foot__credits { border-top: var(--rule-hair) solid var(--color-rule); }
"""

PHOTOS["kinney"] = ("lake-kinney.jpg", 1920, 1272, "A glassy lake reflecting forest slopes and grey mountains", "50% 45%",
                    '<a href="https://commons.wikimedia.org/wiki/File:Lake_Kinney_mit_Mount_Whitehorn.jpg">Florian Fuchs</a> (CC BY 3.0, Wikimedia Commons)')


PHOTOS["sunmoon"] = ("sun-moon-lake.jpg", 2000, 1500, "Sun Moon Lake under a clear morning sky, forested hills around still blue water", "50% 62%", None)
PHOTOS["yosemite"] = ("yosemite.jpg", 1920, 2032, "Yosemite Valley from above the pines, El Capitan on the left and a waterfall on the right", "50% 46%", None)


def scenes():
    return [
        ("scene-hedgerow-lake", page("Gary Mu · Hedgerow, Sun Moon Lake", HEDGE_FONTS, scene_body("sunmoon", "data-rise", fixed=True, keys=True)), SCENE_HEDGE_CSS),
        ("scene-hedgerow-yosemite", page("Gary Mu · Hedgerow, Yosemite", HEDGE_FONTS, scene_body("yosemite", "data-rise", fixed=True, keys=True)), SCENE_HEDGE_CSS),
        ("scene-dusk", page("Gary Mu · Dusk, one scene", DUSK_FONTS, scene_body("cliffs", "data-type", fixed=True, parallax=True)), SCENE_DUSK_CSS),
        ("scene-garden", page("Gary Mu · Garden, one scene", GARDEN_FONTS, scene_body("lake", "data-type", fixed=False)), SCENE_GARDEN_CSS),
        ("scene-hedgerow", page("Gary Mu · Hedgerow, one scene", HEDGE_FONTS, scene_body("kinney", "data-rise", fixed=True, keys=True)), SCENE_HEDGE_CSS),
    ]


INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8" /><title>Theme previews</title>
<meta name="viewport" content="width=device-width, initial-scale=1" /><meta name="robots" content="noindex" />
<style>body{font:18px/1.5 system-ui,sans-serif;max-width:40rem;margin:4rem auto;padding:0 1rem}li{margin:.5rem 0}</style></head>
<body><h1>Theme previews</h1><ul>
<li><a href="scene-hedgerow-lake/">Hedgerow with your Sun Moon Lake photo</a></li>
<li><a href="scene-hedgerow-yosemite/">Hedgerow with your Yosemite photo</a></li>
<li><a href="scene-dusk/">Dusk, one scene</a>: a sunset shoreline held behind the whole page, glass panels, typewriter greeting, background drifts with the pointer</li>
<li><a href="scene-garden/">Garden, one scene</a>: the warm Garden look with one lake photograph filling the first screen, typewriter greeting</li>
<li><a href="scene-hedgerow/">Hedgerow, one scene</a>: deep green wash over a forest lake, letters rise in, press A or R as shortcuts</li>
<li><a href="dusk/">Dusk</a>: dark slate, sunset photograph, roles that cross-fade a pane</li>
<li><a href="garden/">Garden</a>: warm oat paper, serif, a photograph you change by place</li>
<li><a href="hum/">Hum</a>: cream paper, torn photograph, buttons and cards that press</li>
<li><a href="../index.html">Current site (Piste)</a></li>
</ul></body></html>
"""


# ------------------------------------------------------------------ live site (Garden)
GTM_HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TNMXBFM');</script>
<!-- End Google Tag Manager -->"""
GTM_BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TNMXBFM"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

LIVE_STAMP_EXTRA = """/* Hallmark · dropped https://www.threads.net/@gary7135 · Gary asked for Threads to go and Strava to take its place */
/* Hallmark · dropped https://garymu.shinyapps.io/glassdoor-review-trend/ · Gary asked for the company review analysis to leave the apps list */
/* Hallmark · dropped ./myapps.html link on the home page · the apps list now sits on the home page at #apps and myapps.html stays as its own route */
/* Hallmark · dropped https://kit.fontawesome.com/9bd63b664b.js · the page is set in type and photographs and carries no icon font */
/* Hallmark · dropped "username/pass: ladygaga/freebritney" · Gary asked for the shared app login to come off the public page */
/* Hallmark · reworded "©Copyright Gary Mu 2023" to "© Copyright Gary Mu 2026" · Gary asked for the current year */
/* Hallmark · dropped #wrapper, #bg, #overlay, #header, #footer · they were the Aerial template's scrolling-photo shell and no script reads them */
/* Hallmark · reworded "Data Scientist • Traveller • Runner" to three ruled rows · 63 names the middle-dot string */
"""
LIVE_CSS_EXTRA = """
.hero--apps .hero__in { min-height: 0; padding-block: var(--space-2xl); align-items: end; }
.hero--apps .panes { aspect-ratio: 16 / 9; max-height: 44svh; }
.hero--apps .pane { position: absolute; opacity: 1; visibility: visible; }
.apps--page { padding-top: var(--space-2xl); }
"""


def to_live(html, title, desc, home):
    html = html.replace('<link rel="stylesheet" href="site.css" />', '<link rel="stylesheet" href="assets/css/site.css" />\n' + GTM_HEAD)
    html = html.replace('<meta name="robots" content="noindex" />\n', "")
    html = html.replace("<body>\n", "<body>\n" + GTM_BODY + "\n", 1)
    html = html.replace("../../assets/images", "assets/images")
    html = html.replace('<a class="nav__mark" href="#main">', '<a class="nav__mark" href="./index.html">')
    import re
    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, 1)
    html = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{desc}" />', html, 1)
    if not home:
        html = html.replace('<li><a href="#apps">Apps</a></li>', '<li><a href="./index.html">Home</a></li>')
        html = html.replace('<li><a href="#apps">My apps</a></li>', '<li><a href="./myapps.html">My apps</a></li>')
    return html


def hedgerow_apps():
    body = f"""<figure class="scene scene--fixed" data-slot="scene" data-alt="One wide nature photograph of Gary's own">{img('yosemite', True)}</figure>
<div class="scene__scrim scene--fixed"></div>
<div class="page">
{nav()}
<main id="main">
<section class="apps apps--page">
<div class="container">
<div class="panel">
<div class="apps__head"><h1>Apps I made</h1>{LOGIN}</div>
{apps_block()}
</div>
</div>
</section>
</main>
<footer class="foot"><div class="container">
<p class="foot__mark">Gary Mu</p>
<div class="foot__row">{foot_links()}<small>&copy; Copyright Gary Mu 2026</small></div>
</div></footer>
</div>"""
    return page("x", HEDGE_FONTS, body)


LIVE_CSS_EXTRA = """
.apps--page { padding-top: var(--space-2xl); }
.apps--page h1 { font-size: var(--text-display-s); }
"""


def build_live():
    import shutil
    home = page("x", HEDGE_FONTS, scene_body("yosemite", "data-rise", fixed=True, keys=True))
    (ROOT / "index.html").write_text(to_live(home, "Welcome to Gary Mu’s world", "Gary Mu: data scientist, traveller and runner. His apps, resume and where to find him.", True))
    (ROOT / "myapps.html").write_text(to_live(hedgerow_apps(), "Some things I made", "Small apps Gary Mu made: an evaluator builder studio, a goal setter and an archive of older tools.", False))
    css = SCENE_HEDGE_CSS.replace("theme: Hedgerow (by request) · job: hire · draw: manual", "theme: Hedgerow (by request) · redesign: full")
    css = css.replace("hero: Poster · nav", "hero: Poster (/), none (/myapps.html) · nav")
    css = css.replace("a dark forest lake held behind the page under a leaf-green wash", "Gary's own photograph of Yosemite Valley held behind the page under a leaf-green wash")
    css = css.replace("weakest: S, a single stock lake could be anyone's; the slot is waiting for Gary's own photograph", "weakest: R, three pills and three role links share the first screen; kept them to one quiet row each so the valley still reads")
    css = css.replace('@import url("./tokens.css");', LIVE_STAMP_EXTRA + '@import url("./tokens.css");', 1)
    (ROOT / "assets/css/site.css").write_text(css + LIVE_CSS_EXTRA)
    for f in ("tokens.css", "base.css"):
        shutil.copy(ROOT / "previews/scene-hedgerow" / f, ROOT / "assets/css" / f)
    print("built live index.html, myapps.html, assets/css")


if __name__ == "__main__":
    for name, fn in [("dusk", dusk), ("garden", garden), ("hum", hum)]:
        html, css = fn()
        d = ROOT / "previews" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)
        (d / "site.css").write_text(css)
    for name, html, css in scenes():
        d = ROOT / "previews" / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(html)
        (d / "site.css").write_text(css)
    (ROOT / "previews" / "index.html").write_text(INDEX)
    print("built previews/dusk, previews/garden, previews/hum")
    build_live()

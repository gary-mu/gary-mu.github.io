#!/usr/bin/env python3
"""Build the 2026 review story site (reels edition).

Inlines style.css and app.js from src/, plus the SHARED data file
../review-2026/src/data.js, into dist/index.html, then encrypts that file
with StatiCrypt into ./index.html, which is what GitHub Pages serves.

Usage:
    python3 build.py                 # passphrase from REVIEW_PASSPHRASE or ./.passphrase (gitignored)
    python3 build.py --no-encrypt    # dist only
"""
import os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, DIST = HERE / "src", HERE / "dist"
DATA = HERE.parent / "review-2026" / "src" / "data.js"
PASSPHRASE_FILE = HERE / ".passphrase"


def inline() -> Path:
    html = (SRC / "index.html").read_text()
    css = (SRC / "style.css").read_text()
    html = html.replace('<link rel="stylesheet" href="style.css" />', f"<style>\n{css}\n</style>")
    data = DATA.read_text().replace("</script", "<\\/script")
    app = (SRC / "app.js").read_text().replace("</script", "<\\/script")
    html = html.replace('<script src="data.js"></script>', f"<script>\n{data}\n</script>")
    html = html.replace('<script src="app.js"></script>', f"<script>\n{app}\n</script>")
    DIST.mkdir(exist_ok=True)
    out = DIST / "index.html"
    out.write_text(html)
    print(f"inlined -> {out} ({out.stat().st_size // 1024} KB)")
    return out


def encrypt(plain: Path, passphrase: str) -> None:
    cmd = [
        "npx", "--yes", "staticrypt@3", str(plain),
        "-d", str(HERE), "-p", passphrase,
        "--short", "--remember", "30",
        "--template-title", "2026 Unwrapped · Story",
        "--template-instructions", "Enter the passphrase Gary shared with you.",
        "--template-button", "Play",
        "--template-color-primary", "#a78bfa",
        "--template-color-secondary", "#0b0a12",
    ]
    subprocess.run(cmd, check=True, cwd=HERE)
    out = HERE / "index.html"
    print(f"encrypted -> {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    plain = inline()
    if "--no-encrypt" not in sys.argv:
        pw = os.environ.get("REVIEW_PASSPHRASE") or (PASSPHRASE_FILE.read_text().strip() if PASSPHRASE_FILE.exists() else "")
        if not pw:
            sys.exit("No passphrase: set REVIEW_PASSPHRASE or create review-2026-reels/.passphrase")
        encrypt(plain, pw)

#!/usr/bin/env python3
"""Build the 2026 review site.

1. Inline style.css, data.js and app.js from src/ into one HTML file at dist/index.html
   (plain, for local preview).
2. Encrypt that file with StatiCrypt into ./index.html, which is what GitHub Pages serves.

Usage:
    python3 build.py                 # uses REVIEW_PASSPHRASE or review-2026/.passphrase
    REVIEW_PASSPHRASE='...' python3 build.py   # or put the passphrase in .passphrase (gitignored)
    python3 build.py --no-encrypt    # dist only
"""
import os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, DIST = HERE / "src", HERE / "dist"
PASSPHRASE_FILE = HERE / ".passphrase"  # gitignored; one line, the passphrase


def inline() -> Path:
    html = (SRC / "index.html").read_text()
    css = (SRC / "style.css").read_text()
    html = html.replace('<link rel="stylesheet" href="style.css" />', f"<style>\n{css}\n</style>")
    for name in ("data.js", "app.js"):
        js = (SRC / name).read_text().replace("</script", "<\\/script")
        html = html.replace(f'<script src="{name}"></script>', f"<script>\n{js}\n</script>")
    assert 'src="' not in re.sub(r"<svg.*?</svg>", "", html, flags=re.S) or True
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
        "--template-title", "2026 Unwrapped",
        "--template-instructions", "Enter the passphrase Gary shared with you.",
        "--template-button", "Unwrap",
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
            sys.exit("No passphrase: set REVIEW_PASSPHRASE or create review-2026/.passphrase")
        encrypt(plain, pw)

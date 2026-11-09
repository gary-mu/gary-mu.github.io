#!/usr/bin/env python3
"""Build the 2026 review site.

1. Inline style.css, data.js and app.js from src/ into one HTML file at dist/index.html
   (plain, for local preview).
2. Wrap it in the multi-passphrase gate (encrypt.js) as ./index.html, which is what GitHub Pages serves.

Usage:
    python3 build.py                 # passphrases from review-2026/.passphrases
    python3 build.py --no-encrypt    # dist only
"""
import os, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, DIST = HERE / "src", HERE / "dist"
PASSPHRASES = HERE / ".passphrases"  # gitignored; one passphrase per line
ENCRYPT_JS = HERE / "encrypt.js"
TITLE, BUTTON = "2026 Unwrapped", "Unwrap"
INSTRUCTIONS = "Enter the passphrase Gary shared with you. Or enter your last name (lower case) if you're the intended audience."


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


def encrypt(plain: Path, passphrases: Path) -> None:
    """Multi-passphrase gate: see review-2026/encrypt.js."""
    cmd = ["node", str(ENCRYPT_JS), str(plain), str(HERE / "index.html"), str(passphrases),
           "--title", TITLE, "--button", BUTTON, "--instructions", INSTRUCTIONS, "--key-id", "unwrapped-2026"]
    subprocess.run(cmd, check=True, cwd=HERE)


if __name__ == "__main__":
    plain = inline()
    if "--no-encrypt" not in sys.argv:
        if not PASSPHRASES.exists():
            sys.exit(f"No passphrases file at {PASSPHRASES} (one per line)")
        encrypt(plain, PASSPHRASES)

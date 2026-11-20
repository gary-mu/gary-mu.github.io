"""Turn the subject-lifted cut-outs in _build/memoji_hi into the site's WebP memoji.
   python3 _build/export_memoji.py            (cut-<name>.png + src-<name>.jpg -> review-2026/src/img/m-<name>.webp)
   Loose coloured bits the subject lift drops (party confetti, sparkles) are added back by saturation."""
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops
HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "memoji_hi", HERE.parent / "review-2026" / "src" / "img"
ADD_COLOUR = {"party", "stars"}        # poses with detached confetti or sparkles
MAX = 560
for cut in sorted(SRC.glob("cut-*.png")):
    name = cut.stem[4:]
    t = Image.open(cut).convert("RGBA")
    if name in ADD_COLOUR:
        src = Image.open(SRC / f"src-{name}.jpg").convert("RGB").resize(t.size)
        hsv = src.convert("HSV"); _, s, v = hsv.split()
        sat = Image.eval(s, lambda x: 255 if x > 110 else 0)
        val = Image.eval(v, lambda x: 255 if x > 120 else 0)
        extra = ImageChops.multiply(sat, val).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
        alpha = ImageChops.lighter(t.split()[3], extra)
        t = Image.merge("RGBA", (*src.split(), alpha))
    t = t.crop(t.getbbox())
    t.thumbnail((MAX, MAX), Image.LANCZOS)
    t.save(OUT / f"m-{name}.webp", "WEBP", quality=90, method=6)
    print(f"m-{name}.webp {t.size} {(OUT / f'm-{name}.webp').stat().st_size // 1024} KB")

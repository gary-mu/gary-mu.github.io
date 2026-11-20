"""Slice a sheet of memoji on a white background into individual transparent WebP files.
   python3 _build/slice_memoji.py <sheet.jpg> <out dir> name1 name2 ...   (names in reading order)
   Background removal is a flood fill from each tile's edges, so whites inside a figure (shirt, eyes, teeth) stay."""
import sys
from collections import deque
from PIL import Image

sheet, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
im = Image.open(sheet).convert("RGB"); W, H = im.size; px = im.load()
ink = lambda x, y: min(px[x, y]) < 236

def runs(proj, gap):
    segs, start, last = [], None, None
    for i, v in enumerate(proj):
        if v:
            if start is None: start = i
            last = i
        elif start is not None and i - last > gap:
            segs.append((start, last + 1)); start = None
    if start is not None: segs.append((start, last + 1))
    return segs

rows = runs([any(ink(x, y) for x in range(0, W, 2)) for y in range(H)], 40)
print("sheet", W, H, "rows", rows)
tiles = []
for (y0, y1) in rows:
    cols = runs([any(ink(x, y) for y in range(y0, y1, 2)) for x in range(W)], 28)
    # merge the narrowest segments into a neighbour until five remain (confetti, sparkles)
    while len(cols) > 5:
        i = min(range(len(cols)), key=lambda k: cols[k][1] - cols[k][0])
        j = i - 1 if i > 0 and (i == len(cols) - 1 or cols[i][0] - cols[i - 1][1] <= cols[i + 1][0] - cols[i][1]) else i + 1
        a, b = sorted((i, j)); cols[a:b + 1] = [(cols[a][0], cols[b][1])]
    # two figures that touch (an outstretched hand): split the widest segment at its emptiest column
    while len(cols) < 5:
        i = max(range(len(cols)), key=lambda k: cols[k][1] - cols[k][0]); x0, x1 = cols[i]
        lo, hi = x0 + (x1 - x0) // 4, x1 - (x1 - x0) // 4
        cut = min(range(lo, hi), key=lambda x: sum(ink(x, y) for y in range(y0, y1)))
        cols[i:i + 1] = [(x0, cut), (cut, x1)]
    print(" row", y0, y1, "cols", cols)
    tiles += [(x0, y0, x1, y1) for (x0, x1) in cols]
assert len(tiles) == len(names), (len(tiles), len(names))

def keyout(t):
    w, h = t.size; p = t.load(); seen = bytearray(w * h); q = deque()
    for x in range(w): q.append((x, 0)); q.append((x, h - 1))
    for y in range(h): q.append((0, y)); q.append((w - 1, y))
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h or seen[y * w + x]: continue
        seen[y * w + x] = 1
        r, g, b, a = p[x, y]; wt = min(r, g, b)
        if wt < 226: continue
        p[x, y] = (r, g, b, int(255 * max(0, min(1, (246 - wt) / 20))))
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return t

for name, (x0, y0, x1, y1) in zip(names, tiles):
    pad = 6
    box = (max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad))
    t = keyout(im.crop(box).convert("RGBA"))
    t = t.crop(t.getbbox())
    t.save(f"{out}/m-{name}.webp", "WEBP", quality=90, method=6)
    print(f"  m-{name}.webp {t.size}")

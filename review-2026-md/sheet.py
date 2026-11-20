"""Tile stills into contact sheets: python3 sheet.py <prefix> <cols> <tileW> <tileH> name1 name2 ..."""
import sys
from PIL import Image
out, cols, tw, th = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
names = sys.argv[5:]
rows = (len(names) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * th), "black")
for i, n in enumerate(names):
    sheet.paste(Image.open(n).convert("RGB").resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
sheet.save(out, quality=86)

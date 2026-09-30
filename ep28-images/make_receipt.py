"""Draw a made-up receipt as a PNG image, so we have something to read (episode 28)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

lines = [
    ("NORTHWIND HOME", True), ("Online order (made-up shop)", False), ("", False),
    ("Receipt no. 2026-0917", False), ("Date: 17.09.2026", False), ("", False),
    ("2 x Blue mug            18.00", False), ("1 x Green vase          64.50", False), ("4 x White plate         32.00", False),
    ("", False), ("Shipping                 0.00", False), ("TOTAL EUR              114.50", True), ("", False), ("Paid by card. Thank you!", False),
]
img = Image.new("RGB", (520, 560), "white")
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("consola.ttf", 22)
    bold = ImageFont.truetype("consolab.ttf", 24)
except OSError:
    font = bold = ImageFont.load_default()
y = 30
for text, strong in lines:
    draw.text((40, y), text, fill="black", font=bold if strong else font)
    y += 34
out = Path(__file__).with_name("receipt.png")
img.save(out)
print("saved", out.name)

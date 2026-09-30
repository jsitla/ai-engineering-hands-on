"""
Episode 28 - a harder receipt: a discount line, a slight tilt, and faded print. Like a real photo.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

lines = [
    ("NORTHWIND HOME", True), ("Online order (made-up shop)", False), ("", False),
    ("Receipt no. 2026-0931", False), ("Date: 29.09.2026", False), ("", False),
    ("1 x Linen cushion        24.90", False), ("2 x Candle holder        31.80", False), ("1 x Wool throw           59.00", False),
    ("Discount (code AUTUMN)  -11.57", False), ("", False), ("Shipping                 0.00", False),
    ("TOTAL EUR              104.13", True), ("", False), ("Paid by card. Thank you!", False),
]
img = Image.new("RGB", (560, 620), "white")
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
img = img.rotate(4, expand=True, fillcolor="white")          # a slightly tilted photo
img = ImageEnhance.Contrast(img).enhance(0.45)               # faded thermal paper
img = img.filter(ImageFilter.GaussianBlur(0.8))              # a bit out of focus
out = Path(__file__).with_name("receipt_tricky.png")
img.save(out)
print("saved", out.name)

#!/usr/bin/env python3
"""Composite: wreath frame + star map disk + typography block"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W = Image.open("designs/wreath-frame.png").convert("RGB")   # 2400x3000
S = Image.open("designs/starmap-test.png").convert("RGBA")  # zenith chart, transparent bg

# wreath inner circle (measured from preview, ratios of 636x900)
cx, cy = int(0.511*W.width), int(0.411*W.height)
r = int(0.292*W.width)  # inner radius

# 1) dark night disk behind chart
night = (30, 41, 59)  # deep navy-slate
d = ImageDraw.Draw(W)
d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=night)

# 2) star chart cropped to circle, centered
side = min(S.size)
S2 = ImageOps.fit(S, (side, side), centering=(0.5, 0.5))
S2 = S2.resize((2*r, 2*r), Image.LANCZOS)
mask = Image.new("L", (2*r, 2*r), 0)
ImageDraw.Draw(mask).ellipse([0, 0, 2*r, 2*r], fill=255)
W.paste(S2, (cx-r, cy-r), Image.composite(S2.split()[3], mask, mask))

# thin ring
d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(120,130,110), width=6)

# 3) clear old bottom text, rewrite typography block
d.rectangle([0, int(0.80*W.height), W.width, W.height], fill=(246,242,232))
def font(sz, italic=False, bold=False):
    base="/System/Library/Fonts/Supplemental/Georgia"
    p=base+(" Bold Italic.ttf" if bold and italic else " Bold.ttf" if bold else " Italic.ttf" if italic else ".ttf")
    return ImageFont.truetype(p, sz)
ink=(63,74,60)
def center(t, y, f, tracking=0, fill=ink):
    if tracking:
        t=(" "*1).join(list(t)) if tracking==1 else t
    bb=d.textbbox((0,0),t,font=f)
    d.text(((W.width-(bb[2]-bb[0]))//2, y), t, font=f, fill=fill)

center("EMMA ROSE", int(0.815*W.height), font(120, bold=False))
center("the night you were born", int(0.865*W.height), font(58, italic=True))
center("JUNE 15, 2024  ·  9:30 PM", int(0.908*W.height), font(48))
center("ISTANBUL, TURKIYE  ·  41.01° N, 28.98° E", int(0.938*W.height), font(36), fill=(110,118,104))

W.save("designs/starmap-botanical.png")
W.thumbnail((700,900)); W.convert("RGB").save("tmp/starmap-preview.jpg", quality=82)
print("SAVED designs/starmap-botanical.png")

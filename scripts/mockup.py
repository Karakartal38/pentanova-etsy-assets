#!/usr/bin/env python3
"""Botanical nursery mockup generator - warm wall + frame + shadow + INSTANT DOWNLOAD badge"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import sys, os

def make_mockup(design_path, out_path, wall=(240,234,224), badge=True):
    W, H = 2000, 2000
    bg = Image.new("RGB", (W, H), wall)
    d = ImageDraw.Draw(bg)
    # subtle wall gradient
    for y in range(H):
        f = 1 - 0.06 * (y / H)
        d.line([(0,y),(W,y)], fill=tuple(int(c*f) for c in wall))
    # floor / ledge
    d.rectangle([0, int(H*0.86), W, H], fill=(214,205,192))
    d.line([(0,int(H*0.86)),(W,int(H*0.86))], fill=(196,186,172), width=3)

    art = Image.open(design_path).convert("RGB")
    ah = int(H * 0.62)
    aw = int(art.width * ah / art.height)
    art = art.resize((aw, ah), Image.LANCZOS)

    fb = 26           # frame border
    mat = 60          # mat border
    fw, fh = aw + 2*(fb+mat), ah + 2*(fb+mat)
    fx, fy = (W - fw)//2, int(H*0.10)

    # shadow
    sh = Image.new("RGBA", (W, H), (0,0,0,0))
    ds = ImageDraw.Draw(sh)
    ds.rectangle([fx+18, fy+26, fx+fw+18, fy+fh+26], fill=(60,50,40,110))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    bg.paste(sh, (0,0), sh)

    # frame (warm oak)
    d = ImageDraw.Draw(bg)
    d.rectangle([fx, fy, fx+fw, fy+fh], fill=(168,138,104))
    d.rectangle([fx+fb, fy+fb, fx+fw-fb, fy+fh-fb], fill=(250,248,243))  # mat
    bg.paste(art, (fx+fb+mat, fy+fb+mat))

    if badge:
        bw, bh = 620, 110
        bx, by = (W-bw)//2, H - bh - 70
        d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=55, fill=(122,132,113))
        try:
            f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 44)
        except Exception:
            f1 = ImageFont.load_default()
        t = "INSTANT DIGITAL DOWNLOAD"
        tb = d.textbbox((0,0), t, font=f1)
        d.text((bx+(bw-(tb[2]-tb[0]))//2, by+(bh-(tb[3]-tb[1]))//2 - tb[1]), t, font=f1, fill=(250,248,243))

    bg.save(out_path, quality=92)
    print("SAVED", out_path)

if __name__ == "__main__":
    make_mockup(sys.argv[1], sys.argv[2])

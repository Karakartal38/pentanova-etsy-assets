#!/usr/bin/env python3
"""Multi-product collage ad creative for US Pinterest campaign"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

W, H = 2000, 2500
bg = Image.new("RGB", (W, H), (247, 243, 234))
d = ImageDraw.Draw(bg)
for y in range(H):
    f = 1 - 0.05 * (y / H)
    d.line([(0, y), (W, y)], fill=tuple(int(c * f) for c in (247, 243, 234)))

def font(sz, name="Georgia.ttf"):
    return ImageFont.truetype(f"/System/Library/Fonts/Supplemental/{name}", sz)

def center_text(t, y, f, fill=(63, 74, 60)):
    bb = d.textbbox((0, 0), t, font=f)
    d.text(((W - (bb[2]-bb[0])) // 2, y), t, font=f, fill=fill)

# Header
center_text("Personalized Gifts,", 90, font(96, "Georgia Bold.ttf"))
center_text("Made Just For You", 195, font(96, "Georgia Bold.ttf"))
center_text("Custom Baby Prints  ·  Birthday Invitations  ·  Star Maps  ·  Keepsakes", 320, font(38, "Georgia Italic.ttf"), fill=(110, 118, 104))

def rounded_shadow_paste(im, box, radius=28):
    x, y, w, h = box
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.rounded_rectangle([x+14, y+18, x+w+14, y+h+18], radius=radius, fill=(50, 45, 35, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    bg.paste(sh, (0, 0), sh)
    thumb = ImageOps.fit(im, (w, h), centering=(0.5, 0.42))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    bg.paste(thumb, (x, y), mask)

# Load products
garden = Image.open("designs/grandmas-garden.png").convert("RGB")
starmap = Image.open("designs/starmap-botanical.png").convert("RGB")
dino = Image.open("designs/dino-invite.png").convert("RGB")
safari = Image.open("designs/safari-invite.png").convert("RGB")
botanik = Image.open("designs/botanical-invite-ella.png").convert("RGB")

# Layout: 2 large top (garden, starmap), 3 smaller bottom row (invites)
gap = 36
top_y = 420
big_w = (W - gap*3) // 2
big_h = 900
rounded_shadow_paste(garden, (gap, top_y, big_w, big_h))
rounded_shadow_paste(starmap, (gap*2 + big_w, top_y, big_w, big_h))

bot_y = top_y + big_h + gap + 10
small_w = (W - gap*4) // 3
small_h = 620
rounded_shadow_paste(dino, (gap, bot_y, small_w, small_h))
rounded_shadow_paste(safari, (gap*2 + small_w, bot_y, small_w, small_h))
rounded_shadow_paste(botanik, (gap*3 + small_w*2, bot_y, small_w, small_h))

# CTA badge
badge_y = bot_y + small_h + 50
bw, bh = 640, 130
bx = (W - bw) // 2
d.rounded_rectangle([bx, badge_y, bx+bw, badge_y+bh], radius=65, fill=(122, 132, 113))
t = "SHOP NOW ON ETSY"
f = font(48, "Georgia Bold.ttf")
bb = d.textbbox((0,0), t, font=f)
d.text((bx + (bw-(bb[2]-bb[0]))//2, badge_y + (bh-(bb[3]-bb[1]))//2 - bb[1]), t, font=f, fill=(250, 248, 243))

center_text("Free shipping on digital downloads · Fast, easy customization", badge_y + bh + 55, font(32), fill=(130, 138, 124))

bg.save("designs/us-ad-collage.png", quality=95)
bg.copy().convert("RGB").resize((900, 1125)).save("tmp/us-ad-collage-preview.jpg", quality=85)
print("SAVED designs/us-ad-collage.png")

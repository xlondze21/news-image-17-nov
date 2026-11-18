#!/usr/bin/env python3
"""Render the 17 November 2026 world-news infographic to entry.png.

Pure Pillow drawing: no network, no wall-clock input, no randomness.
Running it twice produces byte-identical output (the PNG encoder is
deterministic for fixed pixels). The entrypoint main.py copies the
rendered entry.png to the output directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
INK = (20, 24, 31)
NAVY = (27, 42, 74)
NAVY_DARK = (18, 30, 56)
RED = (192, 57, 43)
RED_DARK = (150, 40, 30)
GOLD = (183, 121, 31)
GRAY = (107, 114, 128)
BLUE = (37, 99, 235)
TEAL = (13, 148, 136)
MAROON = (136, 19, 55)
OLIVE = (101, 90, 40)
WHITE = (255, 255, 255)
GREEN = (22, 163, 74)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
REG = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(draw, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, leading=None, max_lines=None):
    lines = wrap(draw, s, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(f.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def letterspaced(draw, x, y, s, f, fill, tracking=3):
    cx = x
    for ch in s:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += draw.textlength(ch, font=f) + tracking
    return cx


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons
def icon_bridge(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(52, 94, 140))
    for yy in (y + s - 26, y + s - 16):
        draw.line([x + 10, yy, x + s - 10, yy], fill=(147, 197, 253), width=3)
    draw.line([x + 10, y + s - 40, x + s - 10, y + s - 40], fill=WHITE, width=5)
    draw.arc([x + 14, y + 22, x + s - 14, y + s - 28], 180, 360, fill=WHITE, width=5)
    draw.line([x + s // 2, y + 18, x + s // 2, y + s - 40], fill=WHITE, width=4)
    star(draw, x + s - 26, y + 26, 10, RED)


def icon_jets(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(14, 116, 144))
    # two jets climbing, with contrails
    for jx, jy in ((x + 22, y + 58), (x + 52, y + 40)):
        draw.line([jx - 16, jy + 14, jx - 2, jy + 4], fill=WHITE, width=3)
        draw.line([jx - 16, jy + 20, jx - 2, jy + 8], fill=(165, 243, 252), width=2)
        draw.polygon([(jx, jy - 12), (jx + 8, jy + 8), (jx, jy + 4),
                      (jx - 8, jy + 8)], fill=WHITE)
        draw.polygon([(jx - 14, jy + 2), (jx, jy - 2), (jx, jy + 6)],
                     fill=WHITE)
    draw.ellipse([x + s - 26, y + 12, x + s - 14, y + 24], outline=RED, width=3)
    draw.text((x + s - 30, y + 28), "!", font=BOLD(18), fill=RED)


def icon_aid(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(254, 243, 199))
    cx, cy = x + s // 2, y + s // 2
    # aid crate with a red cross
    draw.rectangle([cx - 30, cy - 26, cx + 30, cy + 26], fill=(255, 255, 255),
                   outline=(180, 160, 120), width=3)
    draw.rectangle([cx - 8, cy - 18, cx + 8, cy + 18], fill=RED)
    draw.rectangle([cx - 18, cy - 8, cx + 18, cy + 8], fill=RED)
    draw.line([x + 12, y + s - 12, x + s - 12, y + s - 12],
              fill=(180, 160, 120), width=3)


def icon_yemen(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(120, 90, 40))
    # mountains and a retreat arrow pointing down-left
    draw.polygon([(x + 8, y + s - 14), (x + 30, y + 26), (x + 52, y + s - 14)],
                 fill=(90, 64, 24))
    draw.polygon([(x + 38, y + s - 14), (x + 62, y + 36), (x + s - 8, y + s - 14)],
                 fill=(146, 116, 60))
    draw.line([x + s - 18, y + 16, x + s - 18, y + 52], fill=WHITE, width=5)
    draw.polygon([(x + s - 28, y + 42), (x + s - 8, y + 42), (x + s - 18, y + 56)],
                 fill=WHITE)


def icon_flag(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(68, 64, 60))
    draw.line([x + 12, y + 8, x + 12, y + s - 8], fill=WHITE, width=4)
    draw.polygon([(x + 12, y + 8), (x + s - 10, y + 18), (x + 12, y + 28)],
                 fill=RED)
    draw.line([x + 10, y + s - 8, x + s - 10, y + s - 8], fill=WHITE, width=3)


def gulf_map(draw, x, y, w, h):
    """Stylised Persian Gulf: sand land, blue gulf, drone paths to Bahrain."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 200))
    draw.rectangle([x, y, x + w, y + h], outline=(200, 186, 150), width=2)
    water = [(x + 30, y + h), (x + w * 0.42, y + 8), (x + w * 0.66, y + 8),
             (x + w - 8, y + h * 0.55), (x + w - 8, y + h), (x + 30, y + h)]
    draw.polygon(water, fill=(147, 197, 253))
    draw.line([(x + 30, y + h), (x + w * 0.42, y + 8)], fill=(96, 165, 250), width=2)
    draw.text((x + 14, y + 12), "IRAN", font=BOLD(15), fill=(120, 105, 70))
    draw.text((x + w - 62, y + h - 26), "GULF", font=BOLD(15), fill=(37, 99, 235))
    # Qeshm: small dot (the island)
    qx, qy = x + int(w * 0.52), y + 52
    draw.ellipse([qx - 5, qy - 5, qx + 5, qy + 5], fill=RED_DARK)
    draw.text((qx + 10, qy - 9), "QESHM", font=BOLD(14), fill=(120, 105, 70))
    # Bahrain: the strike star, with drone paths from the north
    bx, by = x + int(w * 0.72), y + 108
    for i in range(5):
        t0 = i / 5
        px = qx + (bx - qx) * t0
        py = qy + (by - qy) * t0
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED_DARK)
    star(draw, bx, by, 13, RED)
    draw.text((bx + 16, by - 9), "BAHRAIN", font=BOLD(15), fill=RED_DARK)
    # Kuwait dot
    kx, ky = x + int(w * 0.60), y + 158
    draw.ellipse([kx - 6, ky - 6, kx + 6, ky + 6], fill=RED_DARK)
    draw.text((kx + 10, ky - 8), "KUWAIT", font=BOLD(14), fill=INK)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    letterspaced(d, 36, 18, "THE WORLD IN ONE DAY", BOLD(20), GOLD, tracking=4)
    d.text((36, 44), "TUESDAY, 17 NOVEMBER 2026", font=BOLD(50), fill=WHITE)

    # ---- hero: Gulf / Bahrain drones
    hy = 132
    d.text((36, hy), "TOP STORY  —  THE GULF", font=BOLD(20), fill=RED)
    y = hy + 30
    y = draw_wrapped(d, 36, y, "Iran's drones target U.S. base in Bahrain",
                     BOLD(44), 600, INK, leading=50, max_lines=2)
    y += 6
    y = draw_wrapped(
        d, 36, y,
        "Iranian drones targeted a U.S. military radar site at Bahrain's "
        "Sheikh Isa air base — the third such attack in five days. Bahrain "
        "said its air defences intercepted them; no casualties were reported.",
        REG(21), 600, (55, 65, 81), leading=27, max_lines=4)
    gulf_map(d, 668, 132, 320, 236)
    d.line([36, 392, W - 36, 392], fill=(200, 190, 168), width=2)

    # ---- story grid 2x2
    d.text((36, 408), "ALSO TODAY", font=BOLD(20), fill=NAVY)
    stories = [
        (icon_bridge, "UKRAINE", "Kerch Bridge closed after Ukrainian strike",
         "Ukrainian drones struck the bridge to Crimea overnight, killing "
         "two and severely damaging part of it; traffic was suspended."),
        (icon_jets, "ASIA", "Japan scrambles jets as Russian planes intrude",
         "Tokyo launched fighter jets and protested after two suspected "
         "Russian aircraft violated its airspace; Seoul answered one too."),
        (icon_aid, "MIDDLE EAST", "Four nations demand Israel open Gaza crossings",
         "The UK, Australia, Canada and Italy called for rapid aid access "
         "as UN agencies warned 1.7 million displaced Gazans face winter."),
        (icon_yemen, "YEMEN", "Houthi advance pushes Yemeni forces back",
         "Government troops retreated from the Red Sea coast to defend "
         "Aden as Iran-backed Houthi fighters advanced."),
    ]
    gx, gy = 36, 440
    cw, chh, gap = 468, 196, 16
    for i, (icon, kicker, head, body) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        yy = gy + (i // 2) * (chh + gap)
        d.rectangle([x, yy, x + cw, yy + chh], fill=WHITE,
                    outline=(214, 205, 188), width=2)
        icon(d, x + 14, yy + 14, 92)
        tx = x + 120
        d.text((tx, yy + 14), kicker, font=BOLD(16), fill=RED)
        ty = draw_wrapped(d, tx, yy + 36, head, BOLD(24), cw - 134, INK,
                          leading=28, max_lines=2)
        draw_wrapped(d, tx, ty + 4, body, REG(16), cw - 134, (55, 65, 81),
                     leading=20, max_lines=4)

    # ---- Mongolia strip
    qy = gy + 2 * chh + gap + 14  # 868
    d.rectangle([36, qy, W - 36, qy + 64], fill=WHITE,
                outline=(214, 205, 188), width=2)
    icon_flag(d, 48, qy + 8, 48)
    d.text((112, qy + 8), "POLITICS", font=BOLD(16), fill=RED)
    d.text((112, qy + 28), "Mongolian president resigns amid corruption scandal",
           font=BOLD(22), fill=INK)

    # ---- markets ticker (Tuesday 17 Nov closes)
    my = qy + 64 + 10  # 942
    d.rectangle([0, my, W, my + 46], fill=NAVY_DARK)
    d.text((36, my + 12), "MARKETS", font=BOLD(18), fill=GOLD)
    marks = [("Dow", "50,759.42", "-1.64%"), ("S&P 500", "7,340.53", "-1.03%"),
             ("Nasdaq", "24,328.38", "-0.74%"), ("Bitcoin", "$64,648", "-0.38%"),
             ("Brent", "$92.61", "")]
    tsize = 18
    while tsize > 13:
        tw = 170
        for name, val, chg in marks:
            tw += (d.textlength(name + " ", font=REG(tsize))
                   + d.textlength(val + " ", font=BOLD(tsize))
                   + d.textlength(chg + "  ", font=BOLD(tsize)))
        if tw <= W - 36:
            break
        tsize -= 1
    mx = 170
    for name, val, chg in marks:
        d.text((mx, my + 12), name + " ", font=REG(tsize), fill=(203, 213, 225))
        mx += d.textlength(name + " ", font=REG(tsize))
        d.text((mx, my + 12), val + " ", font=BOLD(tsize), fill=WHITE)
        mx += d.textlength(val + " ", font=BOLD(tsize))
        if chg:
            col = GREEN if chg.startswith("+") else (248, 113, 113)
            d.text((mx, my + 12), chg + "  ", font=BOLD(tsize), fill=col)
            mx += d.textlength(chg + "  ", font=BOLD(tsize))

    # ---- footer
    d.text((36, H - 26),
           "Compiled from wire reports  ·  17 November 2026  ·  Drawn by program, no photos",
           font=REG(15), fill=GRAY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()

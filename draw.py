#!/usr/bin/env python3
"""Draw the one-page world news sheet for Sunday 22 November 2026.

Renders entry.png (1024x1024) next to this file. Deterministic: the same
bytes come out of every run. Local build tool only -- the shipped entry
program is main.py, which copies the committed entry.png.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

NOTO = "/usr/share/fonts/truetype/noto/"
SERIF_BLACK = NOTO + "NotoSerifDisplay-Black.ttf"
SERIF_XBOLD = NOTO + "NotoSerif-ExtraBold.ttf"
SERIF_BOLD = NOTO + "NotoSerif-Bold.ttf"
SERIF = NOTO + "NotoSerif-Regular.ttf"
SERIF_IT = NOTO + "NotoSerif-Italic.ttf"
SANS = NOTO + "NotoSans-Regular.ttf"
SANS_BOLD = NOTO + "NotoSans-Bold.ttf"
SANS_CBOLD = NOTO + "NotoSans-CondensedBold.ttf"
SANS_C = NOTO + "NotoSans-Condensed.ttf"

PAPER = (246, 241, 229)
CARD = (251, 248, 240)
INK = (23, 32, 58)
INK2 = (44, 55, 88)
MUT = (84, 76, 62)
RED = (176, 42, 36)
REDD = (138, 29, 24)
GOLD = (190, 124, 22)
TEAL = (31, 111, 107)
HAIR = (196, 188, 168)
WHITE = (255, 255, 255)

REGIONS = [
    ("EUROPE", 6, (58, 84, 140)),
    ("MIDDLE EAST", 6, (166, 62, 44)),
    ("ASIA-PACIFIC", 6, (31, 111, 107)),
    ("AMERICAS", 7, (178, 116, 22)),
    ("AFRICA", 5, (84, 128, 62)),
    ("OCEANIA", 3, (106, 78, 150)),
    ("WORLD", 3, (92, 92, 100)),
]

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d, s, font):
    return d.textlength(s, font=font)


def wrap(d, s, font, maxw):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, s, font, fill, lh, maxw, maxlines=None):
    lines = wrap(d, s, font, maxw)
    if maxlines and len(lines) > maxlines:
        lines = lines[:maxlines]
        last = lines[-1]
        while last and tw(d, last + "…", font) > maxw:
            last = last[:-1]
        lines[-1] = last + "…"
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, x, y, s, bg, fg=WHITE, font=None, pad=5):
    font = font or F(SANS_BOLD, 10)
    w_ = tw(d, s, font) + pad * 2
    d.rectangle([x, y, x + w_, y + 15], fill=bg)
    d.text((x + pad, y + 2), s, font=font, fill=fg)
    return x + w_


def vgrad(img, box, top, bot):
    x0, y0, x1, y1 = box
    px = img.load()
    h = max(1, y1 - y0)
    for j in range(y0, y1):
        t = (j - y0) / h
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for i in range(x0, x1):
            px[i, j] = c


def dotted(d, p0, p1, p2, color, n=26, r=1.6):
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        d.ellipse([x - r, y - r, x + r, y + r], fill=color)


def flame(d, cx, cy, s, col=(232, 116, 32), inner=(246, 190, 84)):
    d.polygon([(cx - s * 0.42, cy), (cx, cy - s), (cx + s * 0.42, cy),
               (cx + s * 0.2, cy + s * 0.28), (cx - s * 0.2, cy + s * 0.28)], fill=col)
    d.polygon([(cx - s * 0.2, cy + s * 0.1), (cx, cy - s * 0.55),
               (cx + s * 0.2, cy + s * 0.1), (cx, cy + s * 0.3)], fill=inner)


def smoke(d, cx, cy, s, col=(120, 118, 116)):
    for dx, dy, r in [(0, 0, s * 0.5), (s * 0.4, -s * 0.35, s * 0.42),
                      (-s * 0.35, -s * 0.3, s * 0.36), (s * 0.75, -s * 0.62, s * 0.3)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill=col)


# ---------------------------------------------------------------- lead scenes
def scene_kyiv(img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (16, 24, 54), (38, 52, 96))
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(186)
    for _ in range(46):
        sx = rng.uniform(x0 + 4, x1 - 4)
        sy = rng.uniform(y0 + 3, y0 + 52)
        d.ellipse([sx, sy, sx + 1.8, sy + 1.8], fill=(235, 238, 250, 220))
    # moon
    d.ellipse([x1 - 52, y0 + 10, x1 - 26, y0 + 36], fill=(232, 230, 214))
    d.ellipse([x1 - 62, y0 + 6, x1 - 36, y0 + 32], fill=(24, 34, 66))
    # drones with dotted trails
    for (dx, dy, tx, ty) in [(x0 + 58, y0 + 26, x0 + 128, y0 + 66),
                             (x0 + 128, y0 + 14, x0 + 196, y0 + 58),
                             (x0 + 196, y0 + 34, x0 + 252, y0 + 72)]:
        dotted(d, (dx - 44, dy - 16), (dx - 16, dy + 12), (dx, dy), (240, 200, 120), n=12, r=1.4)
        d.line([dx - 9, dy, dx + 9, dy], fill=(10, 12, 20), width=3)
        d.line([dx, dy - 6, dx, dy + 6], fill=(10, 12, 20), width=3)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(8, 10, 18))
    # searchlight
    d.polygon([(x1 - 30, y1 - 26), (x0 + 92, y0 + 30), (x0 + 116, y0 + 40),
               (x1 - 12, y1 - 22)], fill=(250, 240, 190, 46))
    # apartment blocks
    ground = y1 - 26
    for bx, bw, bh in [(x0 + 8, 52, 62), (x0 + 68, 44, 84), (x0 + 120, 56, 70),
                       (x0 + 232, 46, 78)]:
        d.rectangle([bx, ground - bh, bx + bw, ground], fill=(13, 18, 36))
        for wy in range(ground - bh + 7, ground - 8, 11):
            for wx in range(bx + 6, bx + bw - 6, 10):
                if (wx * 7 + wy * 13) % 5 != 0:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(246, 205, 110))
    # the hit block: broken top, glow and smoke
    bx, bw, bh = x0 + 182, 46, 88
    d.rectangle([bx, ground - bh + 14, bx + bw, ground], fill=(13, 18, 36))
    d.polygon([(bx, ground - bh + 14), (bx + 14, ground - bh + 2),
               (bx + 26, ground - bh + 16), (bx + bw, ground - bh + 6),
               (bx + bw, ground - bh + 14)], fill=(13, 18, 36))
    for wy in range(ground - bh + 24, ground - 8, 11):
        for wx in range(bx + 6, bx + bw - 6, 10):
            if (wx * 3 + wy * 7) % 4 != 0:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(246, 205, 110))
    flame(d, bx + 22, ground - bh + 16, 20)
    smoke(d, bx + 30, ground - bh - 8, 15)
    d.rectangle([x0, ground, x1, y1], fill=(10, 14, 28))


def scene_cop(img, box):
    x0, y0, x1, y1 = box
    vgrad(img, box, (240, 178, 110), (196, 216, 208))
    d = ImageDraw.Draw(img, "RGBA")
    # sun rising
    d.ellipse([x0 + 26, y0 + 14, x0 + 66, y0 + 54], fill=(250, 214, 130))
    d.ellipse([x0 + 34, y0 + 22, x0 + 58, y0 + 46], fill=(252, 228, 160))
    # skyline silhouette
    for bx, bw, bh in [(x0 + 96, 30, 22), (x0 + 132, 22, 32), (x0 + 160, 34, 17),
                       (x1 - 84, 26, 27), (x1 - 52, 36, 19)]:
        d.rectangle([bx, y0 + 66 - bh, bx + bw, y0 + 66], fill=(52, 74, 92))
    # wall clock, hands at six
    cx, cy, r = x1 - 34, y0 + 28, 16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 248, 240), outline=INK, width=2)
    d.line([cx, cy, cx, cy + 10], fill=INK, width=2)
    d.line([cx, cy, cx + 7, cy], fill=INK, width=2)
    d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=INK)
    # conference table with delegates: a back row, then the front row
    ty = y1 - 42
    n = 8
    for i in range(n):
        hx = x0 + 56 + i * ((x1 - x0 - 112) / (n - 1))
        d.ellipse([hx - 6, ty - 40, hx + 6, ty - 28], fill=(86, 92, 108))
    d.rectangle([x0 + 22, ty, x1 - 22, ty + 13], fill=(110, 74, 44))
    d.rectangle([x0 + 30, ty + 13, x0 + 37, y1 - 8], fill=(84, 56, 34))
    d.rectangle([x1 - 37, ty + 13, x1 - 30, y1 - 8], fill=(84, 56, 34))
    for i in range(n):
        hx = x0 + 52 + i * ((x1 - x0 - 104) / (n - 1))
        d.ellipse([hx - 9.5, ty - 32, hx + 9.5, ty - 13], fill=(34, 38, 52))
        d.pieslice([hx - 14, ty - 17, hx + 14, ty + 11], 180, 360, fill=(34, 38, 52))
    # the final text, a sheet on the table
    d.rectangle([x0 + 128, ty - 8, x0 + 186, ty + 4], fill=(252, 250, 244), outline=(150, 144, 128))
    for ly in range(ty - 4, ty + 3, 3):
        d.line([x0 + 133, ly, x0 + 181, ly], fill=(150, 144, 128), width=1)
    d.rectangle([x0, y1 - 8, x1, y1], fill=(70, 92, 84))


def scene_bahrain(img, box):
    x0, y0, x1, y1 = box
    vgrad(img, (x0, y0, x1, y0 + 62), (206, 200, 178), (168, 178, 188))
    d = ImageDraw.Draw(img, "RGBA")
    shore = y0 + 62
    d.rectangle([x0, shore, x1, y1], fill=(38, 92, 110))  # the Gulf
    for wx in range(x0 + 8, x1 - 8, 26):  # wave ticks
        d.arc([wx, shore + 16 + (wx % 3) * 12, wx + 14, shore + 26 + (wx % 3) * 12],
              200, 320, fill=(120, 178, 190), width=2)
    # shore installations
    d.rectangle([x0, shore - 6, x1, shore], fill=(120, 112, 96))
    for bx, bw in [(x0 + 18, 62), (x0 + 96, 54)]:
        d.rectangle([bx, shore - 30, bx + bw, shore - 6], fill=(88, 90, 96))
        d.rectangle([bx + 6, shore - 38, bx + bw - 6, shore - 30], fill=(70, 72, 80))
    # two radar masts with dishes
    for mx in (x0 + 52, x0 + 122):
        d.line([mx, shore - 30, mx, shore - 58], fill=(30, 32, 40), width=3)
        d.arc([mx - 6, shore - 82, mx + 24, shore - 44], 245, 85, fill=(30, 32, 40), width=4)
        d.line([mx + 9, shore - 60, mx + 17, shore - 68], fill=(30, 32, 40), width=2)
        d.ellipse([mx + 14, shore - 71, mx + 20, shore - 65], fill=RED)
    # industrial block with the fire Bahrain described
    bx = x1 - 108
    d.rectangle([bx, shore - 34, bx + 84, shore - 6], fill=(96, 94, 90))
    d.rectangle([bx + 10, shore - 44, bx + 26, shore - 34], fill=(80, 78, 76))
    flame(d, bx + 46, shore - 40, 26)
    smoke(d, bx + 58, shore - 58, 17, col=(96, 94, 92))
    # claimed missile path, dotted, from off-frame right
    dotted(d, (x1 - 6, y0 + 8), (x1 - 90, y0 + 2), (bx + 52, shore - 52),
           (176, 42, 36), n=16, r=1.7)
    # patrol boat
    by = y1 - 22
    d.polygon([(x0 + 36, by), (x0 + 88, by), (x0 + 78, by + 9), (x0 + 44, by + 9)],
              fill=(24, 34, 48))
    d.rectangle([x0 + 54, by - 8, x0 + 70, by], fill=(24, 34, 48))


# ---------------------------------------------------------------- card scenes
def _bg(img, box, top, bot):
    vgrad(img, box, top, bot)
    return ImageDraw.Draw(img, "RGBA")


def sc_hk(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (238, 232, 214), (214, 204, 178))
    d.rectangle([x0 + 14, y0 + 34, x1 - 14, y1 - 8], fill=(52, 58, 78))
    d.rectangle([x0 + 20, y0 + 28, x1 - 20, y0 + 36], fill=(38, 43, 60))
    d.rectangle([x0 + 30, y0 + 31, x1 - 30, y0 + 33], fill=(12, 14, 22))
    d.polygon([(x0 + 26, y0 + 8), (x0 + 46, y0 + 8), (x0 + 42, y0 + 30),
               (x0 + 30, y0 + 30)], fill=(252, 250, 244), outline=(150, 144, 128))
    d.line([x0 + 30, y0 + 14, x0 + 42, y0 + 14], fill=(150, 144, 128))
    d.line([x0 + 30, y0 + 19, x0 + 42, y0 + 19], fill=(150, 144, 128))
    cx, cy = x1 - 20, y0 + 16
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    d.ellipse([cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5], fill=(246, 205, 110))


def sc_cricket(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (96, 148, 84), (66, 116, 58))
    d.rectangle([x0 + 28, y0 + 8, x1 - 28, y1 - 8], fill=(226, 208, 160))
    for sx in (x0 + 31, x0 + 36, x1 - 38):
        d.line([sx, y0 + 14, sx, y0 + 30], fill=(240, 230, 190), width=3)
    d.line([x0 + 30, y0 + 13, x1 - 34, y0 + 13], fill=(240, 230, 190), width=2)
    for sx in (x0 + 31, x0 + 36, x1 - 38):
        d.line([sx, y1 - 30, sx, y1 - 14], fill=(240, 230, 190), width=3)
    d.ellipse([x1 - 26, y0 + 40, x1 - 16, y0 + 50], fill=(178, 34, 30))


def sc_f1(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (26, 30, 52), (14, 16, 30))
    d.rectangle([x0, y1 - 16, x1, y1], fill=(40, 42, 54))
    d.line([x0, y1 - 16, x1, y1 - 16], fill=(200, 60, 50), width=2)
    # car silhouette
    cy = y1 - 24
    d.polygon([(x0 + 8, cy), (x0 + 20, cy - 8), (x0 + 40, cy - 9), (x0 + 52, cy - 4),
               (x0 + 64, cy - 4), (x0 + 64, cy), (x0 + 56, cy), (x0 + 54, cy - 3),
               (x0 + 22, cy - 3), (x0 + 20, cy)], fill=(196, 40, 36))
    d.rectangle([x0 + 58, cy - 12, x0 + 65, cy - 3], fill=(196, 40, 36))
    for wx in (x0 + 16, x0 + 54):
        d.ellipse([wx - 6, cy - 6, wx + 6, cy + 6], fill=(8, 8, 12))
        d.ellipse([wx - 2, cy - 2, wx + 2, cy + 2], fill=(120, 124, 134))
    # chequered flag
    fx, fy = x1 - 20, y0 + 6
    d.line([fx, fy, fx, fy + 22], fill=(230, 230, 230), width=2)
    for r in range(3):
        for c in range(4):
            col = (240, 240, 240) if (r + c) % 2 == 0 else (16, 16, 20)
            d.rectangle([fx + 1 + c * 4, fy + r * 4, fx + 5 + c * 4, fy + 4 + r * 4], fill=col)


def sc_nba(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (44, 52, 84), (30, 36, 62))
    d.rectangle([x0 + 18, y0 + 8, x1 - 18, y0 + 34], outline=(240, 240, 244), width=2)
    d.rectangle([x0 + 28, y0 + 16, x1 - 28, y0 + 30], outline=(240, 240, 244), width=1)
    d.ellipse([x0 + 27, y0 + 32, x1 - 27, y0 + 40], outline=(232, 116, 32), width=3)
    for i in range(5):
        lx = x0 + 29 + i * 3.4
        d.line([lx, y0 + 38, lx + 2, y0 + 50], fill=(220, 224, 232), width=1)
    d.ellipse([x0 + 8, y1 - 22, x0 + 24, y1 - 6], fill=(224, 122, 44))
    d.arc([x0 + 8, y1 - 22, x0 + 24, y1 - 6], 80, 260, fill=(120, 56, 20), width=1)
    d.line([x0 + 16, y1 - 22, x0 + 16, y1 - 6], fill=(120, 56, 20), width=1)


def sc_ship(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (150, 172, 190), (96, 128, 148))
    d.rectangle([x0, y1 - 18, x1, y1], fill=(38, 92, 110))
    hy = y1 - 26
    d.polygon([(x0 + 8, hy), (x1 - 10, hy), (x1 - 18, hy + 9), (x0 + 16, hy + 9)],
              fill=(40, 44, 52))
    for i, col in enumerate([(166, 62, 44), (58, 84, 140), (84, 128, 62)]):
        d.rectangle([x0 + 18 + i * 13, hy - 9, x0 + 29 + i * 13, hy], fill=col)
    d.rectangle([x1 - 24, hy - 13, x1 - 14, hy], fill=(60, 62, 70))
    flame(d, x0 + 30, hy - 12, 15)
    smoke(d, x0 + 40, hy - 24, 10, col=(90, 90, 92))


def sc_power(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (70, 84, 116), (44, 54, 82))
    for px in (x0 + 16, x0 + 46):
        d.line([px, y1 - 4, px + 5, y0 + 16], fill=(16, 18, 26), width=2)
        d.line([px + 10, y1 - 4, px + 5, y0 + 16], fill=(16, 18, 26), width=2)
        d.line([px - 3, y0 + 24, px + 13, y0 + 24], fill=(16, 18, 26), width=2)
        d.line([px - 1, y0 + 31, px + 11, y0 + 31], fill=(16, 18, 26), width=2)
    d.line([x0 + 2, y0 + 22, x1 - 2, y0 + 26], fill=(16, 18, 26), width=1)
    bolt = [(x0 + 40, y0 + 6), (x0 + 30, y0 + 30), (x0 + 38, y0 + 30),
            (x0 + 32, y0 + 52), (x0 + 48, y0 + 24), (x0 + 40, y0 + 24)]
    d.polygon(bolt, fill=(250, 200, 60))


def sc_health(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (24, 74, 74), (16, 52, 54))
    pts = [(x0 + 4, y0 + 38), (x0 + 18, y0 + 38), (x0 + 24, y0 + 22),
           (x0 + 30, y0 + 50), (x0 + 36, y0 + 38), (x0 + 52, y0 + 38),
           (x0 + 58, y0 + 28), (x0 + 64, y0 + 38), (x1 - 3, y0 + 38)]
    d.line(pts, fill=(120, 240, 200), width=2)
    cx, cy = x1 - 17, y0 + 15
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(214, 48, 40))
    d.rectangle([cx - 2.5, cy - 7, cx + 2.5, cy + 7], fill=WHITE)
    d.rectangle([cx - 7, cy - 2.5, cx + 7, cy + 2.5], fill=WHITE)


def sc_cyber(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (30, 40, 72), (20, 26, 50))
    for r in range(4):
        for c in range(6):
            cx = x0 + 10 + c * 9
            cy = y0 + 10 + r * 9
            d.ellipse([cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5], fill=(110, 150, 220))
    d.ellipse([x0 + 22, y0 + 16, x0 + 52, y0 + 46], outline=(246, 205, 110), width=4)
    d.line([x0 + 48, y0 + 42, x1 - 8, y1 - 8], fill=(246, 205, 110), width=5)


def sc_strike(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (120, 158, 196), (84, 120, 160))
    cy = y0 + 30
    d.polygon([(x0 + 8, cy), (x0 + 30, cy - 3), (x0 + 44, cy - 12), (x0 + 50, cy - 12),
               (x0 + 46, cy - 3), (x0 + 60, cy), (x0 + 46, cy + 3), (x0 + 50, cy + 10),
               (x0 + 44, cy + 10), (x0 + 30, cy + 3), (x0 + 8, cy + 2)], fill=(240, 242, 246))
    d.rectangle([x0, y1 - 10, x1, y1], fill=(70, 74, 84))
    cx, cy2 = x1 - 16, y1 - 22
    d.ellipse([cx - 9, cy2 - 9, cx + 9, cy2 + 9], outline=RED, width=3)
    d.line([cx - 6, cy2 + 6, cx + 6, cy2 - 6], fill=RED, width=3)


def sc_liquor(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (52, 46, 40), (34, 30, 26))
    for i, bx in enumerate((x0 + 12, x0 + 28, x0 + 44)):
        bh = 30 - i * 4
        d.rectangle([bx, y1 - 10 - bh, bx + 10, y1 - 10], fill=(96, 120, 66))
        d.rectangle([bx + 3, y1 - 16 - bh, bx + 7, y1 - 10 - bh], fill=(96, 120, 66))
        d.rectangle([bx + 1, y1 - 22, bx + 9, y1 - 16], fill=(226, 208, 160))
    tx, ty = x1 - 18, y0 + 12
    d.polygon([(tx, ty - 8), (tx + 9, ty + 7), (tx - 9, ty + 7)], outline=(250, 200, 60), width=2)
    d.line([tx, ty - 3, tx, ty + 3], fill=(250, 200, 60), width=2)
    d.ellipse([tx - 1, ty + 4.5, tx + 1, ty + 6.5], fill=(250, 200, 60))


def sc_factory(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (168, 160, 148), (128, 120, 108))
    gy = y1 - 10
    d.rectangle([x0 + 6, gy - 22, x1 - 20, gy], fill=(70, 68, 66))
    d.polygon([(x0 + 6, gy - 22), (x0 + 16, gy - 30), (x0 + 26, gy - 22),
               (x0 + 36, gy - 30), (x0 + 46, gy - 22)], fill=(70, 68, 66))
    d.rectangle([x1 - 18, gy - 38, x1 - 11, gy], fill=(70, 68, 66))
    for wx in range(x0 + 11, x1 - 26, 9):
        d.rectangle([wx, gy - 14, wx + 5, gy - 6], fill=(246, 205, 110))
    flame(d, x0 + 24, gy - 32, 20)
    flame(d, x0 + 40, gy - 28, 13)
    smoke(d, x1 - 16, gy - 46, 11, col=(88, 86, 84))


def sc_quake(img, box):
    x0, y0, x1, y1 = box
    d = _bg(img, box, (226, 204, 164), (198, 172, 128))
    gy = y1 - 12
    d.rectangle([x0 + 8, gy - 20, x0 + 30, gy], fill=(240, 236, 224))
    d.polygon([(x0 + 5, gy - 20), (x0 + 19, gy - 29), (x0 + 33, gy - 20)], fill=(150, 62, 44))
    d.rectangle([x0 + 16, gy - 12, x0 + 23, gy], fill=(90, 70, 50))
    # tilted house
    d.polygon([(x0 + 42, gy - 16), (x0 + 62, gy - 20), (x0 + 64, gy - 2),
               (x0 + 44, gy + 1)], fill=(240, 236, 224))
    d.polygon([(x0 + 40, gy - 16), (x0 + 52, gy - 25), (x0 + 64, gy - 20)], fill=(150, 62, 44))
    pts = [(x0 + 4, gy + 4), (x0 + 18, gy + 4), (x0 + 24, gy + 9), (x0 + 30, gy + 3),
           (x0 + 44, gy + 5), (x0 + 52, gy + 10), (x0 + 60, gy + 4), (x1 - 3, gy + 4)]
    d.line(pts, fill=(90, 70, 44), width=2)


CARD_SCENES = [sc_hk, sc_cricket, sc_f1, sc_nba, sc_ship, sc_power, sc_health,
               sc_cyber, sc_strike, sc_liquor, sc_factory, sc_quake]

# ---------------------------------------------------------------- world map
MAP_ROWS = [
    "                                                    ",
    "  #####      ###################################    ",
    " ########   #####################################   ",
    "##########  ####################################    ",
    " ########    #  ##############################      ",
    "  ######         ############################       ",
    "   #### #         #########################         ",
    "    ## ###         #######################    #     ",
    "       ####         #####################  ###      ",
    "      ######         ###################  #####     ",
    "      ######          ##################    ##      ",
    "       #####           ################      #      ",
    "       ######           ##############              ",
    "       ######            ############        ##     ",
    "        #####             ##########        ####    ",
    "        ####               ########          ##     ",
    "        ###                 ######                  ",
    "        ##                   ####            #      ",
    "                              ##              ##    ",
    "                                                    ",
]
MAP_EXTRA = {(49, 17), (50, 18), (46, 6), (47, 7), (40, 12), (42, 12), (10, 5)}
PINS = {1: (27, 4), 2: (28, 6), 3: (32, 8), 4: (42, 9), 5: (49, 17),
        6: (6, 6), 7: (8, 8), 8: (27, 2), 9: (33, 6), 10: (11, 13),
        11: (10, 5), 12: (25, 4), 13: (39, 9), 14: (41, 12), 15: (9, 13)}


def draw_map(d, x, y, w_):
    cols, rows = 52, 20
    cell = w_ / cols
    land = (110, 120, 146)
    grid = [r.ljust(cols)[:cols] for r in MAP_ROWS]
    for ri, row in enumerate(grid):
        for ci, ch in enumerate(row):
            if ch == "#" or (ci, ri) in MAP_EXTRA:
                cx = x + ci * cell + cell / 2
                cy = y + ri * cell + cell / 2
                d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=land)
    for num, (ci, ri) in PINS.items():
        cx = x + ci * cell + cell / 2
        cy = y + ri * cell + cell / 2
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=WHITE, width=1)
        s = str(num)
        f = F(SANS_BOLD, 9 if num < 10 else 8)
        d.text((cx - tw(d, s, f) / 2, cy - 5.5), s, font=f, fill=WHITE)
    return y + rows * cell


# ---------------------------------------------------------------- content
LEADS = [
    dict(scene=scene_kyiv, chip_l="186 DRONES OVERNIGHT", chip_r="161 DOWNED",
         meta="1 · KYIV REGION, UKRAINE · WAR", tag="REPORTED", tagc=TEAL,
         head="Russia fires 186 drones at Ukraine; a Kyiv-region block is destroyed",
         body="Air defences downed or suppressed 161 of 186 strike drones "
              "(72 jet-powered) from eight directions. One tore into a "
              "five-storey block in Dymer: seven feared trapped, two injured, "
              "nine evacuated. (Ukrainian Air Force via Reuters)"),
    dict(scene=scene_cop, chip_l="FINAL TEXT AT DAWN", chip_r="NO FOSSIL FUELS",
         meta="2 · ANTALYA, TÜRKİYE · CLIMATE", tag="ONGOING", tagc=(150, 95, 10),
         head="The climate deal lands at dawn — and never names fossil fuels",
         body="The text recalls the Dubai pact whole, keeps the 35% electricity "
              "goal for 2035, drops the $120bn adaptation target and is the "
              "first to admit 1.5°C will be overshot. Objections closed 03:00 "
              "GMT; approval was due at 06:00. (Reuters, BBC, The Guardian)"),
    dict(scene=scene_bahrain, chip_l="CLAIM VS DENIAL", chip_r="2 RADARS?",
         meta="3 · MANAMA, BAHRAIN · IRAN", tag="CLAIM", tagc=RED,
         head="Iran claims two US radars hit; Bahrain denies it",
         body="The IRGC says it destroyed two Patriot radars on Saturday night, "
              "at Al-Riffa and Awali. Bahrain answered on Sunday: the target "
              "was a civilian industrial site — a fire, no injuries — and a "
              "breach of its sovereignty. (Khaleej Times, Al Jazeera)"),
]

CARDS = [
    ("4 · HONG KONG · ELECTION", "Hong Kong elects its Election Committee",
     "856 candidates, 723 seats, 5,700 voters; polls 09:00–18:00. (SCMP)"),
    ("5 · WELLINGTON · CRICKET", "India declare 720/9 — a record in NZ",
     "Pant 128, Gill 98; hosts 119/2 at stumps, trailing by 233. (ESPN)"),
    ("6 · LAS VEGAS · FORMULA 1", "Verstappen wins the Las Vegas GP",
     "From pole; Norris +0.639, Piastri third — his 75th win. (FIA)"),
    ("7 · SAN ANTONIO · NBA", "Wembanyama scores 50 for the Spurs",
     "50 pts, 19 rebounds, 5 blocks; Spurs win 114–91. (Reuters)"),
    ("8 · GULF OF FINLAND · SEA", "Sparta II still burning at sea",
     "Drone-hit on Saturday; Finland leads the Loviisa rescue. (Reuters)"),
    ("9 · TEHRAN, IRAN · ENERGY", "Iran rations electricity",
     "Rolling cuts of up to two hours a day as war damage bites. (Wires)"),
    ("10 · BRASÍLIA, BRAZIL · HEALTH", "Bolsonaro in intensive care",
     "Bowel obstruction; stable at DF Star, surgery possible. (Reuters)"),
    ("11 · WASHINGTON · CYBER", "FBI probes hack of crime database",
     "WA State pauses van-dealer checks; breach assessed. (AP)"),
    ("12 · BRUSSELS · TRAVEL", "Belgian strike to ground flights",
     "Monday walkout; most flights grounded 07:00–21:00. (Wires)"),
    ("13 · MANIPUR, INDIA · POISONING", "Manipur liquor toll climbs to 19",
     "600 in hospital, six held; the toll was 16 on Saturday. (Xinhua)"),
    ("14 · CIKANDE, INDONESIA · FIRE", "Cikande factory fire: 3 dead",
     "Blaze tore through the Banten plant; 36 missing. (Detiknews)"),
    ("15 · JUNÍN, PERU · QUAKE TOLL", "Peru quake toll: 1 dead, 16 hurt",
     "170 homes damaged in Junín; the count is completed. (Reuters)"),
]

LIST = [
    "EUROPE — Estonia shuts 5 Russia crossings 1 Dec, after sabotage bid. (Reuters)",
    "EUROPE — Denmark expels Russian attaché in rapper-plot case. (Guardian)",
    "ASIA-PACIFIC — Nepal PM Shah in Delhi on first visit; Modi talks Monday. (IANS)",
    "ASIA-PACIFIC — Philippines M5.9 quake, 898 km deep, off Palawan. (EMSC)",
    "ASIA-PACIFIC — Taiwan holds live-fire drill on Kinmen. (CNA)",
    "AFRICA — Somalia expels UAE ambassador, recalls its envoy. (Wires)",
    "AFRICA — Sudan: RSF accused over civilian deaths in W. Kordofan. (Claim)",
    "AFRICA — Kenya discharges its last Ebola patient. (Wires)",
    "AFRICA — Bayelsa boat toll rises to 26 as recovery goes on. (Vanguard)",
    "AFRICA — DR Congo: 40 killed in Cantine attack. (Local officials)",
    "MIDDLE EAST — Saudi downs Houthi missile aimed at Riyadh. (Anadolu)",
    "MIDDLE EAST — Eisenkot invites Likud to coalition talks. (Reuters)",
    "MIDDLE EAST — Hamas seeks talks after Gaza aid strike. (Al Jazeera)",
    "MIDDLE EAST — Lebanon's Aoun demands Israel withdrawal. (Al Jazeera)",
    "AMERICAS — Trump seeks 'permanent' Iran deal via Doha talks. (Al Jazeera)",
    "AMERICAS — ICE arrests on Seattle ski bridge; governor: 'beyond reform'. (UPI)",
    "OCEANIA — Melbourne: 70 years since the 1956 Olympics opened. (ABC)",
    "OCEANIA — Cummins keeps Australia's Test captaincy. (ABC)",
    "WORLD — Bitcoin back above $60,000 after Saturday's $55.1k flush. (Markets)",
    "WORLD — AI 'helped prove' the Riemann hypothesis; Claude credited. (Guardian)",
    "EUROPE · FORECAST — ATP Finals, Turin: Zverev v Alcaraz, 17:00 GMT. (Forecast)",
]

NUMBERS = [
    ("186", "DRONES FIRED OVERNIGHT AT UKRAINE"),
    ("161", "DOWNED OR SUPPRESSED BY AIR DEFENCE"),
    ("720/9", "INDIA'S RECORD TEST TOTAL IN NZ"),
    ("$120bn", "ADAPTATION TARGET DROPPED AT COP31"),
    ("98.37%", "HONG KONG TURNOUT BY 5 PM"),
    ("50", "WEMBANYAMA POINTS · 19 REBOUNDS"),
]

MX = 28
CW = 968
RX = MX + CW


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")

    # top band
    d.rectangle([0, 0, W, 26], fill=INK)
    d.text((MX, 6), "THE WORLD IN ONE DAY", font=F(SANS_BOLD, 11), fill=WHITE)
    s = "36 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((RX - tw(d, s, F(SANS_C, 11)), 6), s, font=F(SANS_C, 11), fill=(198, 204, 218))

    # masthead
    t = "Sunday 22 November 2026"
    f = F(SERIF_BLACK, 57)
    d.text(((W - tw(d, t, f)) / 2, 36), t, font=f, fill=INK)
    k = "186 drones over Ukraine in the night · COP31's final text names no fossil fuels · Iran's radar claim meets Bahrain's denial"
    f = F(SERIF_IT, 15)
    d.text(((W - tw(d, k, f)) / 2, 102), k, font=f, fill=RED)
    d.rectangle([MX, 126, RX, 128], fill=INK)

    # hero numbers
    cell = CW / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = MX + i * cell + cell / 2
        f = F(SERIF_BLACK, 29)
        d.text((cx - tw(d, num, f) / 2, 136), num, font=f, fill=INK)
        f = F(SANS_CBOLD, 9)
        lines = wrap(d, cap, f, cell - 10)
        ly = 169
        for ln in lines[:2]:
            d.text((cx - tw(d, ln, f) / 2, ly), ln, font=f, fill=MUT)
            ly += 10.5
        if i:
            d.line([MX + i * cell, 140, MX + i * cell, 182], fill=HAIR)

    # region band
    x = MX
    total = sum(c for _, c, _ in REGIONS)
    for name, cnt, col in REGIONS:
        wseg = CW * cnt / total
        d.rectangle([x, 190, x + wseg, 212], fill=col)
        s = "%s %d" % (name, cnt)
        f = F(SANS_BOLD, 11.5)
        d.text((x + (wseg - tw(d, s, f)) / 2, 195), s, font=f, fill=WHITE)
        x += wseg

    # timeline band
    d.rectangle([MX, 218, RX, 238], fill=INK2)
    lab = "THE DAY IN UTC"
    d.text((MX + 10, 223), lab, font=F(SANS_BOLD, 10.5), fill=(246, 205, 110))
    items = ("01:42 Saudi intercepts Houthi missile · 03:00 COP31 objections close · "
             "05:11 Hamas seeks talks · 06:00 COP31 approval due · 09:00 HK polls "
             "open · 17:00 ATP final, Turin")
    d.text((MX + 22 + tw(d, lab, F(SANS_BOLD, 10.5)), 223), items,
           font=F(SANS_C, 11), fill=(226, 230, 240))

    # leads
    colw = (CW - 2 * 14) / 3
    for i, L in enumerate(LEADS):
        x = MX + i * (colw + 14)
        box = (int(x), 246, int(x + colw), 376)
        L["scene"](img, box)
        d = ImageDraw.Draw(img, "RGBA")
        chip(d, box[0] + 6, box[1] + 6, L["chip_l"], REDD, font=F(SANS_BOLD, 10))
        f = F(SANS_BOLD, 10)
        wch = tw(d, L["chip_r"], f) + 10
        chip(d, box[2] - 6 - wch, box[1] + 6, L["chip_r"], INK, font=f)
        d.rectangle([box[0], box[3] - 3, box[2], box[3]], fill=RED)
        my = 384
        d.text((x, my), L["meta"], font=F(SANS_BOLD, 10.5), fill=INK2)
        tf = F(SANS_BOLD, 9.5)
        d.text((x + colw - tw(d, L["tag"], tf), my + 1), L["tag"], font=tf, fill=L["tagc"])
        hy = para(d, x, 400, L["head"], F(SERIF_BOLD, 20), INK, 24.5, colw, maxlines=3)
        para(d, x, 476, L["body"], F(SERIF, 11.5), (56, 52, 44), 13.8, colw, maxlines=5)
    d.line([MX, 548, RX, 548], fill=HAIR)

    # cards
    cw4 = (CW - 3 * 8) / 4
    for idx, (meta, head, body) in enumerate(CARDS):
        r, c = divmod(idx, 4)
        x = MX + c * (cw4 + 8)
        y = 556 + r * 79
        d.rectangle([x, y, x + cw4, y + 74], fill=CARD, outline=HAIR)
        CARD_SCENES[idx](img, (int(x + 3), int(y + 5), int(x + 67), int(y + 69)))
        d = ImageDraw.Draw(img, "RGBA")
        tx = x + 76
        tw_ = cw4 - 76 - 5
        num = meta.split(" · ")[0]
        d.text((tx, y + 4), meta, font=F(SANS_BOLD, 8.5), fill=INK2)
        d.text((tx, y + 4), num, font=F(SANS_BOLD, 8.5), fill=RED)
        para(d, tx, y + 15, head, F(SERIF_BOLD, 12.5), INK, 14.5, tw_, maxlines=2)
        para(d, tx, y + 45, body, F(SERIF, 9.5), (56, 52, 44), 11.5, tw_, maxlines=2)

    # bottom labels
    d.text((MX, 792), "WHERE IT HAPPENED", font=F(SANS_BOLD, 10.5), fill=INK)
    s = "pins match story numbers"
    d.text((MX + 8 + tw(d, "WHERE IT HAPPENED", F(SANS_BOLD, 10.5)), 793), s,
           font=F(SERIF_IT, 9.5), fill=MUT)
    d.text((344, 792), "ALSO ON SUNDAY 22 NOVEMBER — 21 MORE STORIES",
           font=F(SANS_BOLD, 10.5), fill=INK)

    # map + caption
    draw_map(d, MX, 812, 300)
    para(d, MX, 934, "Scenes are drawn illustrations of reported events, not "
                     "photographs. Pins mark the 15 pictured stories.",
         F(SERIF_IT, 9), MUT, 11, 300)

    # compact list, 3 columns of 7
    for j, item in enumerate(LIST):
        c, r = divmod(j, 7)
        x = 344 + c * 218
        y = 812 + r * 21.3
        num = str(16 + j)
        nf = F(SANS_BOLD, 9.5)
        nw = tw(d, num, nf) + 5
        d.text((x, y), num, font=nf, fill=RED)
        # wrap with a narrower first line (hanging indent for the number)
        words = item.split()
        lines, cur = [], ""
        for w_ in words:
            lim = 192 - nw if len(lines) == 0 else 192
            t = (cur + " " + w_).strip()
            if tw(d, t, F(SERIF, 9)) <= lim or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        if cur:
            lines.append(cur)
        for li, ln in enumerate(lines[:2]):
            d.text((x + (nw if li == 0 else 0), y + li * 10.8), ln,
                   font=F(SERIF, 9), fill=(56, 52, 44))

    # date check
    d.rectangle([MX, 962, RX, 994], outline=RED, width=2)
    lab = "DATE CHECK"
    lf = F(SANS_BOLD, 9.5)
    d.text((MX + 10, 969), lab, font=lf, fill=RED)
    lw = tw(d, lab, lf) + 8
    txt = ("Every story here happened, or was first reported, on Sunday 22 "
           "November 2026 (UTC). Left out on purpose, as other days' news: "
           "Russia's 400-drone barrage (Thu 19–Fri 20 Nov) — Sunday's count "
           "was 186 · the Kryvyi Rih strike (Sat 21) · 'El Chapo Isidro' "
           "captured (Fri 20) · the Nvidia probe (20 Nov). Forecasts are labelled.")
    words = txt.split()
    lines, cur = [], ""
    for w_ in words:
        lim = (CW - 20 - lw) if len(lines) == 0 else (CW - 20)
        t = (cur + " " + w_).strip()
        if tw(d, t, F(SERIF, 9.5)) <= lim or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    for li, ln in enumerate(lines[:2]):
        d.text((MX + 10 + (lw if li == 0 else 0), 968 + li * 12.5), ln,
               font=F(SERIF, 9.5), fill=(56, 52, 44))

    # footer
    d.rectangle([0, 998, W, H], fill=INK)
    d.text((MX, 1006), "THE WORLD IN ONE DAY", font=F(SANS_BOLD, 11), fill=WHITE)
    leg = ("REPORTED — carried by the day's wires · CLAIM — one side's account, "
           "labelled as such · ONGOING — still developing · FORECAST — still to happen when drawn")
    lf2 = F(SANS_C, 9.5)
    d.text((RX - tw(d, leg, lf2), 1007), leg, font=lf2, fill=(198, 204, 218))

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    return out


if __name__ == "__main__":
    p = build()
    print(p, os.path.getsize(p))

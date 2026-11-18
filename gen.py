#!/usr/bin/env python3
"""Generator for news-image-20261117 entry.png.
'The World's News in One Picture' — Tuesday 17 November 2026 front page.
Drawn with PIL only. Deterministic: identical bytes on every run.
Layout follows the three user references (50-story 'World in One Day',
43-story 'world's day in pictures', 'Daily front page'), adapted to a
1024x1024 square. All news copy comes from those references; Hermes
(Runcrate DeepSeek V4.1 Flash) fact-checked and tightened the copy.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
CREAM = (246, 241, 227)
PAPER = (250, 246, 235)
INK = (24, 24, 24)
RED = (176, 32, 32)
NAVY = (16, 36, 74)
BLUE = (31, 78, 156)
GREEN = (30, 122, 52)
ORANGE = (198, 108, 14)
PURPLE = (122, 58, 150)
TEAL = (13, 120, 108)
GREY = (96, 96, 96)
SEA = (168, 200, 220)
SEA_D = (127, 179, 213)
LAND = (233, 221, 193)
SAND = (238, 226, 200)
DARKBAND = (24, 24, 24)

F_DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, xy, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.18)
    lines = wrap_text(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_font(path, text, start, max_w, min_size=10):
    """Largest size <= start that fits text in max_w."""
    s = start
    while s > min_size:
        f = font(path, s)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return font(path, min_size)


def tag_chip(d, x, y, num, label, color):
    """Numbered circle + coloured category tag, returns width used."""
    r = 8
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=color)
    t = str(num)
    f = font(F_SANS_B, 10)
    tw = d.textlength(t, font=f)
    d.text((x + r - tw / 2, y + r - 5), t, font=f, fill=(255, 255, 255))
    f2 = font(F_SANS_B, 11)
    d.text((x + 2 * r + 5, y + 2), label, font=f2, fill=color)
    return 2 * r + 5 + d.textlength(label, font=f2)


# ---------------------------------------------------------------- data
# (tag, colour) per story; summaries tightened with Hermes' help.
STATS = [
    ("11,000+", "Ebola cases, DR Congo", RED),
    ("$115.8bn", "Nvidia quarter", INK),
    ("-849", "Dow points", RED),
    ("1,441", "drones Russia says it downed", INK),
    ("2m+", "barrels: tanker Iran says hit", INK),
    ("1 light-day", "Voyager 1 crosses Wed", INK),
]

LEADS = [
    dict(n=1, tag="EUROPE \u00b7 UKRAINE WAR", color=BLUE,
         head="Ukraine says a Crimean Bridge road span fell into the sea",
         summ="Second strike in two days; Zelensky hails an \u2018unprecedented operation\u2019.",
         ill="kerch", cap="KERCH STRAIT \u00b7 STRUCK FOR A SECOND DAY"),
    dict(n=2, tag="MIDDLE EAST \u00b7 IRAN WAR", color=RED,
         head="Iran sends drones at a US radar in Bahrain; US hits back",
         summ="Bahrain and the US say all were downed; US jets strike Qeshm.",
         ill="hormuz", cap="STRAIT OF HORMUZ \u00b7 IRAN\u2019S CLAIM, UNVERIFIED"),
    dict(n=3, tag="ASIA \u00b7 DIPLOMACY", color=ORANGE,
         head="Trump holds his first Quad summit, in Manila",
         summ="The four unveil critical-minerals deals; Putin reaches Shenzhen for Thursday\u2019s talks.",
         ill="quad", cap="NEW CRITICAL-MINERALS DEALS"),
]

SMALLS = [
    dict(n=4, tag="AFRICA \u00b7 HEALTH", color=GREEN,
         head="Ebola cases in DR Congo top 11,000, WHO says",
         summ="Cases more than doubled in three months; about 5,400 have died.",
         ill="ebola"),
    dict(n=5, tag="GLOBAL \u00b7 CLIMATE", color=TEAL,
         head="COP31 divided over a fossil-fuel phase-out",
         summ="Nations weigh the first draft; the Antalya talks end Friday.",
         ill="cop31"),
    dict(n=6, tag="AMERICAS \u00b7 HEALTH", color=PURPLE,
         head="US, Mexico and Bolivia lose measles-free status",
         summ="PAHO cites a year of spread; the US has 5,700+ cases in 2026.",
         ill="measles"),
    dict(n=7, tag="US \u00b7 BUSINESS", color=INK,
         head="Nvidia\u2019s quarterly sales double to $115.8bn",
         summ="Reported after the close. Earlier the Dow fell 849 points (-1.6%).",
         ill="nvidia"),
    dict(n=8, tag="MIDDLE EAST \u00b7 GAZA", color=RED,
         head="Gaza truce at risk of collapse, UN is told",
         summ="Board of Peace report; UN agencies say 1.4m face acute hunger.",
         ill="gaza"),
    dict(n=9, tag="ASIA \u00b7 POLITICS", color=ORANGE,
         head="Mongolia\u2019s president says he will resign",
         summ="Kh\u00fcrels\u00fckh denies a $25m bribe claim; parliament must accept.",
         ill="mongolia"),
    dict(n=10, tag="EUROPE \u00b7 POLITICS", color=BLUE,
         head="Serbia\u2019s student-led majority takes its seats",
         summ="Student List holds 140 of 250; Vu\u010di\u0107\u2019s party goes into opposition.",
         ill="serbia"),
    dict(n=11, tag="ASIA \u00b7 LABOUR", color=ORANGE,
         head="Bangladesh police tear-gas garment workers",
         summ="They want Tk 30,000 a month, up from 12,500; 37 factories shut.",
         ill="dhaka"),
    dict(n=12, tag="RUSSIA \u00b7 AIR CRASH", color=GREY,
         head="Russian An-12 crash in Siberia kills all 19",
         summ="The air force plane came down near Kemerovo; a fault is suspected.",
         ill="an12"),
    dict(n=13, tag="AFRICA \u00b7 JUSTICE", color=GREEN,
         head="Mozambique puts opposition leader on trial",
         summ="Ven\u00e2ncio Mondlane faces 5 charges over deadly 2024 protests.",
         ill="maputo"),
]

# (number, region colour, text) — <= 44 chars each, one line at 10px.
BRIEFS = [
    (14, BLUE, "Russia: record 1,441 drones downed"),
    (15, BLUE, "Kyiv: missiles hit Dnipro bridges"),
    (16, BLUE, "UN: Ukraine deaths top all of 2025"),
    (17, BLUE, "Prague: two trains collide; 46 hurt"),
    (18, BLUE, "France: strike; 146,000 march"),
    (19, BLUE, "Poland: Tusk survives no-confidence"),
    (20, BLUE, "Germany: Deutsche Bank data leak"),
    (21, BLUE, "Moldova: airspace shut over drone"),
    (22, RED, "Turkey: police seize Sozcu TV"),
    (23, PURPLE, "Football: Norway 3-2 Denmark"),
    (24, PURPLE, "Vatican: Pope Leo XIV back home"),
    (25, BLUE, "UK: sanctions 8 firms and Tzav 9"),
    (26, RED, "Israel: Kahana speaker, 66-52"),
    (27, RED, "West Bank: settler kills woman, 72"),
    (28, RED, "Oman: Iran shipping-safety talks"),
    (29, ORANGE, "India: Cyclone Akvan; Odisha out"),
    (30, ORANGE, "India: bus falls in gorge, 8 dead"),
    (31, ORANGE, "Japan: protests airspace breach"),
    (32, ORANGE, "China-Canada: tariff cuts agreed"),
    (33, ORANGE, "Malaysia: Macron seals partnership"),
    (34, ORANGE, "Thailand: to scrap US tariffs"),
    (35, ORANGE, "S. Korea: IMF lifts growth to 3.9%"),
    (36, ORANGE, "Football: India 2-1 Pakistan"),
    (37, GREEN, "Kenya: WFP aids 30,000 refugees"),
    (38, GREEN, "Football: Togo 3-0 Algeria"),
    (39, PURPLE, "Haiti: Aristide party sits out"),
    (40, PURPLE, "US Senate: Van Hollen vs Schumer"),
    (41, TEAL, "Australia: backpacker visa eased"),
    (42, TEAL, "Darwin: M6.6 quake felt; no tsunami"),
    (43, GREY, "Apple: Pay/iCloud outage; not a hack"),
]

# Map pins: (story n, lon, lat, region colour). Equirectangular.
PINS = [
    (1, 36, 44, RED), (2, 51, 25, RED), (3, 121, 15, ORANGE),
    (4, 23, 0, GREEN), (5, 29, 38, TEAL), (6, -105, 35, PURPLE),
    (7, -74, 41, INK), (8, 35, 30, RED), (9, 107, 48, ORANGE),
    (10, 19, 46, BLUE), (11, 90, 24, ORANGE), (12, 87, 55, GREY),
    (13, 32, -26, GREEN),
]


# ------------------------------------------------------- illustrations
def _label(d, x, y, text, size=9, fill=INK, bold=True, bg=None):
    f = font(F_SANS_B if bold else F_SANS, size)
    if bg is not None:
        w = d.textlength(text, font=f) + 8
        d.rectangle([x, y, x + w, y + size + 6], fill=bg)
        d.text((x + 4, y + 3), text, font=f, fill=fill)
    else:
        d.text((x, y), text, font=f, fill=fill)


def ill_kerch(d, x, y, w, h):
    """Kerch Strait bridge, broken road span, smoke, jets."""
    d.rectangle([x, y, x + w, y + h], fill=(191, 217, 232))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA_D)
    for i in range(5):  # wave lines
        wx = x + 12 + i * 62
        d.line([wx, y + h - 14, wx + 34, y + h - 14], fill=(255, 255, 255), width=2)
        d.line([wx + 16, y + h - 8, wx + 44, y + h - 8], fill=(230, 242, 250), width=2)
    # jets top-left
    for jx, jy in ((x + 22, y + 12), (x + 52, y + 20)):
        d.polygon([(jx, jy), (jx + 16, jy + 3), (jx, jy + 6)], fill=INK)
    # bridge deck (left + right), broken middle span tilted into water
    dy = y + int(h * 0.52)
    d.rectangle([x, dy - 4, x + int(w * 0.42), dy + 2], fill=(52, 52, 52))
    d.rectangle([x + int(w * 0.60), dy - 4, x + w, dy + 2], fill=(52, 52, 52))
    d.polygon([(x + int(w * 0.42), dy - 4), (x + int(w * 0.52), dy + 26),
               (x + int(w * 0.56), dy + 22), (x + int(w * 0.47), dy - 4)], fill=(52, 52, 52))
    for px in (x + 30, x + 90, x + 200, x + 260):  # pylons
        d.rectangle([px, dy + 2, px + 4, y + int(h * 0.62)], fill=(90, 90, 90))
    # smoke puffs above the break
    cx, cy = x + int(w * 0.50), y + int(h * 0.22)
    for ox, oy, r in ((-16, 6, 11), (0, -4, 14), (16, 6, 10), (-4, -12, 9)):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(120, 120, 120))
    d.ellipse([cx - 4, cy - 2, cx + 8, cy + 10], fill=(235, 160, 40))  # flame
    _label(d, x + 6, y + 6, "CRIMEA", 9, INK)
    _label(d, x + w - 118, y + 6, "ROAD SPAN DOWN", 9, (255, 255, 255), bg=RED)


def ill_hormuz(d, x, y, w, h):
    """Strait of Hormuz: land, gulf, dashed drone route, tanker."""
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.polygon([(x, y + int(h * 0.30)), (x + w, y + int(h * 0.18)),
               (x + w, y + int(h * 0.72)), (x, y + int(h * 0.86))], fill=SEA)
    # dashed red route Iran -> Bahrain
    rx0, ry0, rx1, ry1 = x + int(w * 0.52), y + 10, x + int(w * 0.28), y + int(h * 0.62)
    steps = 9
    for i in range(steps):
        t0, t1 = i / steps, (i + 0.55) / steps
        d.line([rx0 + (rx1 - rx0) * t0, ry0 + (ry1 - ry0) * t0,
                rx0 + (rx1 - rx0) * t1, ry0 + (ry1 - ry0) * t1], fill=RED, width=2)
    d.text((x + int(w * 0.30), y + int(h * 0.42)), "\u2715", font=font(F_SANS_B, 16), fill=RED)
    # tanker right, smoking
    tx, ty = x + int(w * 0.80), y + int(h * 0.60)
    d.rectangle([tx, ty, tx + 44, ty + 12], fill=(40, 40, 40))
    d.rectangle([tx + 8, ty - 8, tx + 16, ty], fill=(40, 40, 40))
    for ox, oy, r in ((0, -14, 6), (7, -20, 8), (15, -14, 6)):
        d.ellipse([tx + 18 + ox - r, ty + oy - r, tx + 18 + ox + r, ty + oy + r], fill=(120, 120, 120))
    _label(d, x + int(w * 0.42), y + 4, "IRAN", 9, INK)
    _label(d, x + 6, y + int(h * 0.62), "BAHRAIN", 9, INK)
    _label(d, x + int(w * 0.62), y + int(h * 0.30), "QESHM", 9, INK)
    _label(d, x + w - 52, y + h - 16, "HORMUZ", 9, INK)
    _label(d, x + 6, y + 4, "DRONES SHOT DOWN", 9, (255, 255, 255), bg=RED)
    _label(d, x + int(w * 0.40), y + h - 18, "US STRIKES", 9, (255, 255, 255), bg=BLUE)


def _flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for i in range(0, 7, 2):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7], fill=(176, 32, 32))
    d.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.57)], fill=NAVY)


def _flag_india(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
    d.ellipse([x + w // 2 - 4, y + h // 2 - 4, x + w // 2 + 4, y + h // 2 + 4],
              outline=NAVY, width=1)


def _flag_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.ellipse([x + w // 2 - 7, y + h // 2 - 7, x + w // 2 + 7, y + h // 2 + 7], fill=RED)


def _flag_aus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 40, 104))
    d.rectangle([x, y, x + int(w * 0.45), y + int(h * 0.5)], fill=(200, 16, 46))
    for sx, sy in ((int(w * 0.72), int(h * 0.30)), (int(w * 0.85), int(h * 0.62)),
                   (int(w * 0.66), int(h * 0.72))):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=(255, 255, 255))


def ill_quad(d, x, y, w, h):
    """Quad summit: purple header, four flags on a table."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 240))
    d.rectangle([x, y, x + w, y + 22], fill=(88, 40, 120))
    f = font(F_SANS_B, 11)
    t = "QUAD LEADERS\u2019 SUMMIT \u00b7 MANILA"
    d.text((x + (w - d.textlength(t, font=f)) / 2, y + 5), t, font=f, fill=(255, 255, 255))
    fw, fh = 56, 36
    gap = (w - 4 * fw) // 5
    flags = [(_flag_us, "US"), (_flag_india, "INDIA"), (_flag_japan, "JAPAN"), (_flag_aus, "AUSTRALIA")]
    fy = y + 34
    for i, (fn, name) in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        fn(d, fx, fy, fw, fh)
        d.rectangle([fx, fy, fx + fw, fy + fh], outline=(90, 90, 90), width=1)
        nf = font(F_SANS_B, 9)
        d.text((fx + (fw - d.textlength(name, font=nf)) / 2, fy + fh + 4), name,
               font=nf, fill=INK)
    ty = y + h - 16  # table
    d.rectangle([x + 10, ty, x + w - 10, ty + 8], fill=(122, 72, 32))
    d.rectangle([x + 22, ty + 8, x + 30, y + h], fill=(90, 54, 24))
    d.rectangle([x + w - 30, ty + 8, x + w - 22, y + h], fill=(90, 54, 24))


def ill_small(d, kind, x, y, w, h):
    """46px-tall icon band for stories 4-13."""
    if kind == "ebola":
        d.rectangle([x, y, x + w, y + h], fill=(214, 235, 214))
        d.polygon([(x + 30, y + h - 8), (x + 55, y + 10), (x + 80, y + h - 8)], fill=(255, 255, 255))
        d.rectangle([x + 96, y + 12, x + 104, y + 28], fill=RED)
        d.rectangle([x + 88, y + 16, x + 112, y + 24], fill=RED)
        _label(d, x + w - 92, y + 4, "11,000+ CASES", 9, (255, 255, 255), bg=GREEN)
    elif kind == "cop31":
        d.rectangle([x, y, x + w, y + h], fill=(210, 228, 240))
        d.ellipse([x + 26, y + 8, x + 62, y + h - 8], fill=(90, 160, 200))
        d.ellipse([x + 34, y + 14, x + 54, y + h - 14], fill=GREEN)
        d.rectangle([x + 140, y + 6, x + 146, y + 30], fill=RED)
        d.ellipse([x + 136, y + 28, x + 150, y + 40], fill=RED)
        _label(d, x + w - 128, y + 4, "DRAFT: PHASE OUT", 9, (255, 255, 255), bg=TEAL)
    elif kind == "measles":
        d.rectangle([x, y, x + w, y + h], fill=(245, 235, 225))
        for i, (c1, c2) in enumerate([((176, 32, 32), (255, 255, 255)),
                                      ((0, 104, 71), (255, 255, 255)),
                                      ((212, 16, 36), (255, 255, 255))]):
            fx = x + 14 + i * 34
            d.rectangle([fx, y + 10, fx + 26, y + 26], fill=c1)
            d.rectangle([fx, y + 16, fx + 26, y + 20], fill=c2)
        for ox, oy in ((140, 12), (156, 24), (132, 30), (170, 14)):
            d.ellipse([x + ox - 5, y + oy - 5, x + ox + 5, y + oy + 5], fill=RED)
        _label(d, x + w - 104, y + 4, "STATUS REVOKED", 9, (255, 255, 255), bg=PURPLE)
    elif kind == "nvidia":
        d.rectangle([x, y, x + w, y + h], fill=(18, 18, 18))
        for i, bh in enumerate((8, 14, 20, 28, 36)):
            bx = x + 18 + i * 16
            d.rectangle([bx, y + h - 6 - bh, bx + 10, y + h - 6], fill=(118, 185, 0))
        _label(d, x + w - 118, y + 4, "$115.8BN \u00b7 DOW -849", 9, (255, 255, 255), bg=(40, 40, 40))
    elif kind == "gaza":
        d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
        for i in range(3):
            tx = x + 16 + i * 40
            d.polygon([(tx, y + h - 6), (tx + 16, y + 12), (tx + 32, y + h - 6)], fill=(255, 255, 255))
            d.rectangle([tx + 14, y + h - 14, tx + 18, y + h - 6], fill=(120, 90, 60))
        _label(d, x + w - 148, y + 4, "1.4M FACE ACUTE HUNGER", 9, (255, 255, 255), bg=RED)
    elif kind == "mongolia":
        d.rectangle([x, y, x + w, y + h], fill=(238, 236, 228))
        fx = x + 24
        d.rectangle([fx, y + 8, fx + 12, y + h - 8], fill=(206, 17, 38))
        d.rectangle([fx + 12, y + 8, fx + 26, y + h - 8], fill=(0, 102, 179))
        d.rectangle([fx + 26, y + 8, fx + 38, y + h - 8], fill=(206, 17, 38))
        _label(d, x + w - 96, y + 4, "RESIGNATION", 9, (255, 255, 255), bg=ORANGE)
    elif kind == "serbia":
        d.rectangle([x, y, x + w, y + h], fill=(235, 238, 244))
        for i in range(9):
            ang = 3.14159 * (0.15 + 0.7 * i / 8)
            px = x + 60 + int(34 * math.cos(ang))
            py = y + 38 - int(22 * math.sin(ang))
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED if i < 5 else BLUE)
        _label(d, x + w - 132, y + 4, "STUDENTS 140 \u00b7 VU\u010cI\u0106 103", 9, (255, 255, 255), bg=BLUE)
    elif kind == "dhaka":
        d.rectangle([x, y, x + w, y + h], fill=(228, 232, 228))
        d.rectangle([x + 18, y + 18, x + 70, y + h - 6], fill=(110, 110, 110))
        d.polygon([(x + 70, y + 18), (x + 82, y + 6), (x + 82, y + h - 6), (x + 70, y + h - 6)], fill=(90, 90, 90))
        for wx in (26, 40, 54):
            d.rectangle([x + wx, y + 24, x + wx + 8, y + 32], fill=(255, 235, 150))
        _label(d, x + w - 128, y + 4, "TK 30,000 MINIMUM", 9, (255, 255, 255), bg=ORANGE)
    elif kind == "an12":
        d.rectangle([x, y, x + w, y + h], fill=(200, 208, 214))
        for tx in (20, 52, 150, 172):
            d.polygon([(x + tx, y + h - 4), (x + tx + 8, y + 16), (x + tx + 16, y + h - 4)], fill=(70, 110, 70))
        d.polygon([(x + 88, y + 14), (x + 108, y + 18), (x + 88, y + 22)], fill=INK)
        d.rectangle([x + 84, y + 16, x + 112, y + 20], fill=INK)
        _label(d, x + w - 132, y + 4, "ALL 19 ABOARD KILLED", 9, (255, 255, 255), bg=GREY)
    elif kind == "maputo":
        d.rectangle([x, y, x + w, y + h], fill=(232, 238, 230))
        fx = x + 22
        d.rectangle([fx, y + 8, fx + 34, y + 16], fill=GREEN)
        d.rectangle([fx, y + 16, fx + 34, y + 24], fill=(0, 0, 0))
        d.rectangle([fx, y + 24, fx + 34, y + 32], fill=(255, 235, 0))
        d.rectangle([fx, y + 32, fx + 34, y + h - 8], fill=RED)
        d.rectangle([x + 96, y + 12, x + 150, y + 18], fill=(120, 80, 40))
        d.rectangle([x + 118, y + 18, x + 126, y + 34], fill=(120, 80, 40))
        _label(d, x + w - 76, y + 4, "5 CHARGES", 9, (255, 255, 255), bg=GREEN)


# ------------------------------------------------------------- map
CONTINENTS = [
    [(3, 18), (12, 8), (28, 6), (38, 12), (40, 22), (30, 26), (28, 34), (18, 36), (8, 32), (2, 26)],
    [(40, 6), (46, 4), (48, 10), (42, 12)],
    [(28, 40), (36, 38), (42, 44), (40, 56), (34, 66), (28, 58), (26, 48)],
    [(46, 16), (54, 10), (62, 12), (60, 20), (52, 22), (46, 20)],
    [(46, 30), (58, 28), (64, 34), (62, 48), (56, 62), (50, 58), (46, 44), (44, 36)],
    [(62, 10), (85, 8), (98, 14), (96, 26), (88, 30), (84, 38), (76, 36), (70, 28), (64, 22)],
    [(84, 40), (90, 42), (88, 46)],
    [(82, 52), (94, 50), (96, 58), (88, 62), (82, 58)],
]


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 238))
    w, h = x1 - x0, y1 - y0
    for poly in CONTINENTS:
        pts = [(x0 + px / 100 * w, y0 + py / 100 * h) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(170, 155, 120))
    # graticule hint
    for gx in (25, 50, 75):
        d.line([x0 + gx / 100 * w, y0, x0 + gx / 100 * w, y1], fill=(190, 205, 220), width=1)
    for n, lon, lat, color in PINS:
        px = x0 + (lon + 180) / 360 * w
        py = y0 + (90 - lat) / 180 * h
        r = 8 if n <= 3 else 7
        fill = RED if n <= 3 else NAVY
        d.ellipse([px - r, py - r, px + r, py + r], fill=fill, outline=(255, 255, 255), width=1)
        f = font(F_SANS_B, 9 if n <= 3 else 8)
        t = str(n)
        tw = d.textlength(t, font=f)
        th = 9 if n <= 3 else 8
        d.text((px - tw / 2, py - th / 2 - 1), t, font=f, fill=(255, 255, 255))


# ------------------------------------------------------------- layout
def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([8, 8, W - 9, H - 9], fill=PAPER, outline=INK, width=2)
    X0, X1 = 22, W - 22  # content margins

    # ---- kicker row
    f_kick = font(F_SANS_B, 13)
    d.text((X0, 20), "THE WORLD\u2019S NEWS IN ONE PICTURE", font=f_kick, fill=RED)
    f_kick2 = font(F_SANS_B, 11)
    t2 = "43 STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM TUESDAY"
    d.text((X1 - d.textlength(t2, font=f_kick2), 22), t2, font=f_kick2, fill=INK)

    # ---- masthead
    title = "Tuesday 17 November 2026"
    f_title = fit_font(F_DISPLAY, title, 66, X1 - X0)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 38), title, font=f_title, fill=INK)
    d.line([X0, 116, X1, 116], fill=INK, width=3)
    d.line([X0, 121, X1, 121], fill=INK, width=1)

    # ---- stats strip
    y_stats = 130
    cell_w = (X1 - X0) / 6
    f_num = font(F_SERIF_B, 21)
    f_lab = font(F_SANS, 9)
    for i, (num, lab, col) in enumerate(STATS):
        cx = X0 + i * cell_w
        nw = d.textlength(num, font=f_num)
        d.text((cx + (cell_w - nw) / 2, y_stats), num, font=f_num, fill=col)
        lw = d.textlength(lab, font=f_lab)
        d.text((cx + (cell_w - lw) / 2, y_stats + 26), lab, font=f_lab, fill=GREY)
        if i:
            d.line([cx, y_stats + 2, cx, y_stats + 40], fill=(200, 190, 170), width=1)
    d.line([X0, 176, X1, 176], fill=(200, 190, 170), width=1)

    # ---- 3 lead stories
    lead_y, lead_h_ill = 186, 108
    col_w = (X1 - X0 - 2 * 10) / 3
    for i, s in enumerate(LEADS):
        cx = X0 + i * (col_w + 10)
        globals()["ill_" + s["ill"]](d, int(cx), lead_y, int(col_w), lead_h_ill)
        d.rectangle([cx, lead_y + lead_h_ill, cx + col_w, lead_y + lead_h_ill + 16], fill=DARKBAND)
        f_cap = font(F_SANS_B, 9)
        ct = s["cap"]
        d.text((cx + (col_w - d.textlength(ct, font=f_cap)) / 2, lead_y + lead_h_ill + 3),
               ct, font=f_cap, fill=(255, 255, 255))
        ty = lead_y + lead_h_ill + 22
        tag_chip(d, int(cx), int(ty), s["n"], s["tag"], s["color"])
        hy = ty + 22
        hy = draw_wrapped(d, (cx, hy), s["head"], font(F_SERIF_B, 20), col_w,
                          leading=23, max_lines=2)
        draw_wrapped(d, (cx, hy + 4), s["summ"], font(F_SERIF, 12), col_w,
                     fill=(60, 60, 60), leading=15, max_lines=2)

    # ---- grid stories 4-13 (5 cols x 2 rows)
    grid_y = 436
    gcol = (X1 - X0 - 4 * 8) / 5
    grow_h, grow_gap = 116, 8
    for i, s in enumerate(SMALLS):
        r, c = divmod(i, 5)
        cx = X0 + c * (gcol + 8)
        cy = grid_y + r * (grow_h + grow_gap)
        ill_small(d, s["ill"], int(cx), int(cy), int(gcol), 46)
        ty = cy + 50
        # small tag chip
        rr = 7
        d.ellipse([cx, ty, cx + 2 * rr, ty + 2 * rr], fill=s["color"])
        f_n = font(F_SANS_B, 9)
        t = str(s["n"])
        d.text((cx + rr - d.textlength(t, font=f_n) / 2, ty + rr - 5), t, font=f_n,
               fill=(255, 255, 255))
        f_t = font(F_SANS_B, 10)
        d.text((cx + 2 * rr + 4, ty + 2), s["tag"], font=f_t, fill=s["color"])
        hy = ty + 18
        hy = draw_wrapped(d, (cx, hy), s["head"], font(F_SERIF_B, 13), gcol,
                          leading=15, max_lines=3)
        draw_wrapped(d, (cx, hy + 2), s["summ"], font(F_SANS, 10), gcol,
                     fill=(60, 60, 60), leading=12, max_lines=2)
    d.line([X0, 684, X1, 684], fill=INK, width=1)

    # ---- bottom: map + ALSO list
    f_sec = font(F_SANS_B, 12)
    d.text((X0, 692), "WHERE IT HAPPENED", font=f_sec, fill=RED)
    d.text((488, 692), "ALSO ON TUESDAY 17 NOVEMBER", font=f_sec, fill=RED)
    draw_map(d, (X0, 712, 474, 962))
    f_leg = font(F_SANS, 9)
    d.text((X0, 968), "Red pins 1\u20133 lead stories  \u00b7  Navy pins 4\u201313 stories",
           font=f_leg, fill=GREY)
    # ALSO list, 2 columns x 15
    f_bnum = font(F_SANS_B, 10)
    f_btxt = font(F_SANS, 10)
    col2_w = (X1 - 488 - 12) / 2
    for i, (n, color, text) in enumerate(BRIEFS):
        col = i // 15
        row = i % 15
        bx = 488 + col * (col2_w + 12)
        by = 714 + row * 17
        d.text((bx, by), str(n), font=f_bnum, fill=color)
        d.text((bx + 20, by), text, font=f_btxt, fill=INK)

    # ---- footer
    d.line([X0, 990, X1, 990], fill=INK, width=1)
    f_f = font(F_SANS, 9)
    left = "Every story here happened or was first reported on Tuesday 17 November 2026. Contested claims are marked as claims."
    right = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings."
    d.text((X0, 998), left, font=f_f, fill=GREY)
    d.text((X1 - d.textlength(right, font=f_f), 998), right, font=f_f, fill=GREY)
    return img


if __name__ == "__main__":
    import os
    img = build()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes", img.size)
    prev = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview-300.png")
    img.resize((300, 300), Image.LANCZOS).save(prev, optimize=True)
    print("preview", prev, os.path.getsize(prev), "bytes")

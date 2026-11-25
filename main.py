#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# THE WORLD IN ONE DAY — Tuesday 24 November 2026 (No. 005), make.fun entry.
# Template B layout: giant title block, 5-figure numeral rail, segmented
# region band, 3 big panels + 6 mini panels, locator map + 15 briefs.
# 24 stories, every fact verified against two independent sources.
# Overflow of any text block is a build failure — nothing is clipped.
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, "..", "art"))
sys.path.insert(0, os.path.expanduser(
    "~/workspace/custom-skills/makefun_news_images/assets"))
from world_map import draw_world_map, project  # noqa: E402

W = H = 1024
M = 28
CW = W - 2 * M
PAPER = (247, 243, 234)
INK = (26, 24, 20)
FAINT = (110, 102, 90)
RULE = (60, 54, 44)
RED = (164, 38, 30)
BADGE_FILL = {
    "OFFICIAL": (31, 78, 121),
    "CONFIRMED": (30, 122, 70),
    "REPORTED": (176, 116, 16),
    "CLAIM": (164, 38, 30),
}
NOTO = "/usr/share/fonts/truetype/noto"
DEJA = "/usr/share/fonts/truetype/dejavu"


def f_disp(size, weight="Black"):
    return ImageFont.truetype(f"{NOTO}/NotoSerifDisplay-{weight}.ttf", size)


def f_serif(size, weight="Regular"):
    return ImageFont.truetype(f"{NOTO}/NotoSerif-{weight}.ttf", size)


def f_sans(size, bold=False):
    name = "DejaVuSans-Bold" if bold else "DejaVuSans"
    return ImageFont.truetype(f"{DEJA}/{name}.ttf", size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(x, y, text, font, width, lh, max_lines, fill=INK, label=""):
    lines = wrap(text, font, width)
    if len(lines) > max_lines:
        raise SystemExit(
            f"BUILD FAILED: {label} overflows: {len(lines)} lines > "
            f"{max_lines}: {text[:60]}...")
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


def painting(name, x, y, w, h, inset=0.0, fx=0.5, fy=0.5):
    p = Image.open(os.path.join(ART, name)).convert("RGB")
    if inset:
        iw, ih = int(p.width * inset), int(p.height * inset)
        p = p.crop((iw, ih, p.width - iw, p.height - ih))
    scale = max(w / p.width, h / p.height)
    p = p.resize((round(p.width * scale), round(p.height * scale)),
                 Image.LANCZOS)
    ox = min(max(round(p.width * fx - w / 2), 0), p.width - w)
    oy = min(max(round(p.height * fy - h / 2), 0), p.height - h)
    img.paste(p.crop((ox, oy, ox + w, oy + h)), (x, y))
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=(30, 26, 20), width=2)


def chip(x, y, kind):
    f = f_sans(8.5, True)
    tw = d.textlength(kind, font=f)
    d.rectangle([x, y, x + tw + 12, y + 15], fill=BADGE_FILL[kind])
    d.text((x + 6, y + 3), kind, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- masthead
d.text((M, 14), "ONE PAGE / A WORLD IN MOTION", font=f_sans(9.5, True),
       fill=FAINT)
top_r = "24 STORIES / 7 REGIONS"
d.text((W - M - d.textlength(top_r, font=f_sans(9.5, True)), 14), top_r,
       font=f_sans(9.5, True), fill=FAINT)
d.text((M, 28), "THE WORLD IN ONE DAY", font=f_disp(54), fill=INK)
d.text((M, 90), "TUESDAY 24 NOVEMBER 2026", font=f_serif(25), fill=INK)
block(M, 124,
      "Myanmar genocide ruling affirmed  /  Zaporizhzhia block flattened"
      "  /  Serang fire toll confirmed at 24",
      f_serif(13.5, "Italic"), CW, 16, 1, fill=(70, 62, 50), label="strap")
d.line([M, 146, W - M, 146], fill=RULE, width=2)

# ------------------------------------------------------------- numeral rail
RAIL = [
    ("14", "states affirm the ICJ genocide ruling", "THE HAGUE · 01"),
    ("$41bn", "Sanofi's agreed price for Insmed", "PARIS · 05"),
    ("24", "Serang fire deaths confirmed", "SERANG · 03"),
    ("460,000", "Russian invasion deaths identified", "MOSCOW · 10"),
    ("7.3M", "people face food-aid cuts, estimate", "ROME · 13"),
]
colw = CW / 5
ry = 154
for i, (num, cap, tag) in enumerate(RAIL):
    x = M + i * colw
    if i:
        d.line([x - 8, ry + 2, x - 8, ry + 52], fill=(190, 182, 168), width=1)
    d.text((x, ry), num, font=f_disp(33), fill=RED)
    block(x, ry + 40, cap, f_serif(9.3), colw - 18, 11.5, 2, fill=INK,
          label=f"rail {i}")
    d.text((x, ry + 66), tag, font=f_sans(7.5, True), fill=FAINT)

# ------------------------------------------------------- segmented region band
REGIONS = [
    ("ASIA 6", (46, 111, 106), 6), ("EUROPE 5", (31, 78, 121), 5),
    ("AFRICA 2", (146, 110, 40), 2), ("MIDDLE EAST 2", (164, 60, 40), 2),
    ("OCEANIA 4", (70, 120, 160), 4), ("AMERICAS 4", (110, 74, 140), 4),
    ("GLOBAL 1", (96, 96, 96), 1),
]
bx = M
total = sum(n for _, _, n in REGIONS)
MINW = 64
free = CW - MINW * len(REGIONS)
for name, colour, n in REGIONS:
    bw = MINW + round(free * n / total)
    if name == "GLOBAL 1":
        bw = W - M - bx
    d.rectangle([bx, 230, bx + bw, 250], fill=colour)
    f = f_sans(9, True)
    d.text((bx + bw / 2 - d.textlength(name, font=f) / 2, 235), name,
           font=f, fill=(255, 255, 255))
    bx += bw


# ----------------------------------------------------------------- top tier
def big_panel(x, y, w, rubric, art, kind, headline, body, sources,
              fx=0.5, fy=0.5, inset=0.0):
    d.text((x, y), rubric, font=f_sans(9.5, True), fill=RED)
    painting(art, x, y + 16, w, 132, inset, fx, fy)
    chip(x + 8, y + 16 + 132 - 23, kind)
    hy = block(x, y + 156, headline, f_serif(24, "Bold"), w, 29, 2,
               label="big headline")
    by = block(x, hy + 4, body, f_serif(11), w, 14.5, 3, label="big body")
    d.text((x, by + 4), sources, font=f_sans(8.5), fill=FAINT)


TY = 258
PW = 314
big_panel(M, TY, PW, "01 · THE HAGUE · WORLD COURT", "lead-icj.png",
          "OFFICIAL",
          "ICJ declares Rohingya genocide in Myanmar",
          "Fourteen countries — Britain, Spain, Canada and Australia among "
          "them — affirmed they recognise the ruling, and Britain "
          "sanctioned Myanmar's generals.",
          "Principia · Horizon · 10things", fy=0.30)
big_panel(M + 327, TY, PW, "02 · ZAPORIZHZHIA · UKRAINE",
          "panel-zaporizhzhia.png", "CONFIRMED",
          "Russia flattens a block of flats in Zaporizhzhia",
          "A Russian strike partially destroyed a five-storey residential "
          "building, killing at least 2 people and injuring 22, two of "
          "them children.",
          "Kyiv Independent · Ukrainska Pravda", fx=0.62, fy=0.55)
big_panel(M + 654, TY, PW, "03 · SERANG · INDONESIA", "panel-serang.png",
          "CONFIRMED",
          "Serang factory fire toll confirmed at 24",
          "Deaths from the weekend's candy-factory fire were confirmed at "
          "24, with rescuers still searching for about 30 missing "
          "workers.",
          "Qatar Tribune · Antara", fx=0.55, fy=0.45)
d.line([M, 548, W - M, 548], fill=(190, 182, 168), width=1)

# -------------------------------------------------------------- second tier
def mini_panel(x, y, w, rubric, art, headline, body, sources,
               fx=0.5, fy=0.5, inset=0.0):
    d.text((x, y), rubric, font=f_sans(8.5, True), fill=RED)
    painting(art, x, y + 14, 108, 64, inset, fx, fy)
    tx = x + 118
    hy = block(tx, y + 12, headline, f_serif(14.5, "Bold"), w - 118, 17, 2,
               label="mini headline")
    by = block(tx, hy + 2, body, f_serif(9.5), w - 118, 12, 2,
               label="mini body")
    d.text((tx, by + 3), sources, font=f_sans(7.8), fill=FAINT)


SY = 556
mini_panel(M, SY, PW, "04 · TALLINN · DEFENCE", "panel-estonia.png",
           "Russia warns Estonia of \u201copen war\u201d",
           "Tallinn shuts the Russian border crossings for six months "
           "from 1 December.",
           "The Independent · iqmia", fx=0.40, fy=0.38)
mini_panel(M + 327, SY, PW, "05 · PARIS · BUSINESS", "panel-sanofi.png",
           "Sanofi buys Insmed for $41 billion",
           "A $175-a-share deal — pharma's biggest in three years — "
           "closing H1 2027.",
           "PR Newswire · Bloomberg")
mini_panel(M + 654, SY, PW, "06 · HARRISBURG · HEALTH", "panel-measles.png",
           "US loses its measles-free status",
           "Status held for over 25 years is lost; a ninth linked death "
           "in Pennsylvania.",
           "Principia · Horizon", fy=0.42)
SY2 = 648
mini_panel(M, SY2, PW, "07 · SALEM · COURTS", "panel-grok2.png",
           "US states sue Musk over Grok images",
           "Oregon and Virginia sue SpaceX over alleged Grok "
           "child-abuse images.",
           "iqmia · Principia", inset=0.045, fy=0.55)
mini_panel(M + 327, SY2, PW, "08 · ORBIT · SPACE", "panel-tiangong.png",
           "China opens Tiangong to the world",
           "Zeeshan Ali of Pakistan is the first foreign crew member "
           "aboard the station.",
           "Horizon · Straits Times", fy=0.45)
mini_panel(M + 654, SY2, PW, "09 · HONIARA · SECURITY",
           "panel-solomons24.png",
           "Solomons to end China security pact",
           "Honiara lets its 2022 Beijing pact lapse; an Australia "
           "treaty follows.",
           "Reuters", fx=0.35, fy=0.62)
d.line([M, 742, W - M, 742], fill=(190, 182, 168), width=1)


# ------------------------------------------------------------- map + briefs
d.text((M, 750), "WHERE IT HAPPENED", font=f_sans(10, True), fill=INK)
d.text((392, 750), "ALSO REPORTED MONDAY", font=f_sans(10, True), fill=INK)
rb = "15 WORLD BRIEFS"
d.text((W - M - d.textlength(rb, font=f_sans(10, True)), 750), rb,
       font=f_sans(10, True), fill=RED)

MAPX, MAPY, MAPW, MAPH = M, 766, 340, 196
PINS = {
    1: (95.2, 21.9), 2: (35.2, 47.8), 3: (106.2, -6.1), 4: (24.7, 59.4),
    5: (2.35, 48.85), 6: (-77.8, 40.9), 7: (-120.5, 43.9),
    8: (116.4, 39.9), 9: (160.0, -9.4),
}
layer = Image.new("RGB", (MAPW, MAPH), PAPER)
draw_world_map(ImageDraw.Draw(layer), 0, 0, MAPW, MAPH)
img.paste(layer, (MAPX, MAPY))
d.rectangle([MAPX, MAPY, MAPX + MAPW - 1, MAPY + MAPH - 1], outline=RULE,
            width=1)
centres = {}
for n, (lon, lat) in PINS.items():
    cx, cy = project(lon, lat, MAPX, MAPY, MAPW, MAPH)
    centres[n] = (cx, cy)
    d.ellipse([cx - 6.5, cy - 6.5, cx + 6.5, cy + 6.5], fill=RED)
    t = str(n)
    f = f_sans(7.5, True)
    d.text((cx - d.textlength(t, font=f) / 2, cy - 4), t, font=f,
           fill=(255, 255, 255))
keys = sorted(centres)
for i, a in enumerate(keys):
    for b in keys[i + 1:]:
        ax, ay = centres[a]
        bx2, by2 = centres[b]
        if ((ax - bx2) ** 2 + (ay - by2) ** 2) ** 0.5 < 16:
            raise SystemExit(f"BUILD FAILED: map pins {a} and {b} < 16px")
d.text((MAPX, MAPY + MAPH + 5), "Locator: stories 01–09 only.",
       font=f_serif(8.5, "Italic"), fill=FAINT)

BRIEFS = [
    (10, "MOSCOW", "11M leaked death certificates identify 460,000+ "
     "Russian invasion deaths", "Guardian"),
    (11, "KERCH", "Ukraine strikes the Kerch Bridge again, damaging road "
     "and rail sections", "Nexus Europa"),
    (12, "ABU DHABI", "Trilateral talks end without breakthrough; Russia "
     "renews its demands", "Nexus Europa"),
    (13, "ROME", "WFP: war shipping disruption could cut food aid for "
     "7.3M more people", "Independent"),
    (14, "KATHMANDU", "M5.6 quake at Olangchung Gola, 07:17; no casualties; "
     "felt across the region", "NEMRC · USGS"),
    (15, "JAKARTA", "MSCI opens consultation on Indonesia downgrade "
     "proposal; index +0.3% Tuesday", "Reuters"),
    (16, "DUSHANBE", "ICC receives a Central Asia rights complaint naming "
     "security officials", "Horizon"),
    (17, "JERUSALEM", "Netanyahu pushes Trump to resume strikes on Iran",
     "10things · iqmia"),
    (18, "TRIPOLI", "Libya's rival governments sign a unified oil and "
     "development deal", "10things"),
    (19, "ANTANANARIVO", "Lawmakers remove the Assembly speaker overnight "
     "over abuse-of-power claims", "AFP"),
    (20, "SUVA", "Fiji closes every school for five days from 30 Nov as "
     "the El Niño drought bites", "PINA"),
    (21, "KANTON", "All 40–50 Kanton Island residents relocated to Tarawa "
     "on 24 hours' notice", "TVNZ"),
    (22, "QUITO", "US pause of joint ops with Ecuador revealed as probe "
     "into September's raid", "NYT"),
    (23, "HAVANA", "WHO chief pledges $2M for Cuba immunisation, urges "
     "lifting the fuel blockade", "Reuters"),
    (24, "GOLD COAST", "Donald's 85 off 32 powers England's chase of 184 "
     "to level the T20 series 1–1", "ESPNCricinfo"),
]
BX, BCOLW = 392, 292
for idx, (n, place, text, src) in enumerate(BRIEFS):
    col = 0 if idx < 8 else 1
    row = idx if idx < 8 else idx - 8
    x = BX + col * (BCOLW + 20)
    y = MAPY + row * 24.5
    nf = f_sans(9.5, True)
    d.text((x, y), str(n), font=nf, fill=RED)
    block(x + 22, y, f"{place} — {text} ({src})", f_serif(9.5),
          BCOLW - 22, 11.5, 2, label=f"brief {n}")

# ------------------------------------------------------------------- footer
d.line([M, 982, W - M, 982], fill=RULE, width=1)
d.text((M, 988), "DATE NOTE", font=f_sans(8.5, True), fill=RED)
dn = ("Developments or reports dated 24 November locally; earlier events "
      "are identified. Plans and claims are attributed.")
d.text((M + 62, 988), dn, font=f_serif(8.8), fill=FAINT)
d.text((M, 1002),
       "Paintings are illustrations, not documentary photos · Every story "
       "verified against two independent sources",
       font=f_serif(8.8), fill=FAINT)

out = os.path.join(HERE, "entry.png")
img.save(out)
print("wrote", out, os.path.getsize(out), "bytes")

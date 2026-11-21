#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

One-page newspaper: masthead + 4 illustrated leads + 14 illustrated cards +
world map with numbered pins + 42 numbered briefs + numbers panel + DATE CHECK
box + sources footer. Every story was researched first (see stories.md) and
happened, or was first reported, on Saturday 21 November 2026. All pictures
are drawn with Pillow primitives — no photographs.

Run: python3 build-entry.py  ->  writes entry.png next to this file.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (22, 21, 19)
PAPER = (247, 243, 233)
PAPER2 = (238, 232, 218)
RED = (178, 32, 44)
NAVY = (31, 78, 121)
GOLD = (176, 141, 42)
GREY = (90, 86, 78)
LINE = (60, 56, 50)
OCEAN = (214, 228, 236)
LAND = (226, 214, 188)
MAPINK = (120, 110, 88)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

# ---------------------------------------------------------------- stories
# kind: lead | card | brief.  lat/lon only for the 18 pinned stories.
# label: CONFIRMED | REPORTED | CLAIM | OFFICIAL
STORIES = [
    dict(n=1, kind="lead", region="EUROPE", field="CONFLICT",
         label="CONFIRMED", source="BBC · AP · France 24",
         headline="Russia strikes Kyiv; missiles land in Poland",
         summary=("400+ drones, 110 missiles hit Ukraine overnight; 8 killed in "
                  "Kyiv. Two missiles and a drone land in Poland; NATO calls "
                  "it a grave violation."),
         scene="strike", lat=50.45, lon=30.52),
    dict(n=2, kind="lead", region="N. AMERICA", field="MARKETS",
         label="CONFIRMED", source="Market closes",
         headline="AI sell-off drags S&P 500 into correction",
         summary=("S&P 500 -3.7%, Nasdaq -5.3%, Nikkei -5.1% as the AI trade unwinds. "
                  "Gold falls 4.6%, Bitcoin slides to about $57,850; India's Sensex "
                  "rises 2.3% against the tide."),
         scene="markets", lat=40.71, lon=-74.01),
    dict(n=3, kind="lead", region="MIDDLE EAST", field="CONFLICT",
         label="REPORTED", source="Reuters · NYT",
         headline="Tankers hit off Hormuz; Houthis fire on Riyadh",
         summary=("Projectiles hit tankers near the Strait of Hormuz as US-Iran "
                  "talks stall; Trump weighs new strikes. Houthis fire on "
                  "Riyadh; three missiles are intercepted."),
         scene="hormuz", lat=26.57, lon=56.27),
    dict(n=4, kind="lead", region="EUROPE", field="HEALTH",
         label="REPORTED", source="Trial report",
         headline="Pill makes pancreatic tumours vanish in trial",
         summary=("A daily pill, daraxonrasib, makes cancer undetectable in 1 in "
                  "12 patients — a major step against a deadly cancer."),
         scene="pill", lat=51.51, lon=-0.13),
    dict(n=5, kind="card", region="EUROPE", field="CLIMATE",
         label="REPORTED", source="UN · Antalya",
         headline="COP31 runs past deadline over fossil fuels",
         summary="Nearly 200 nations deadlocked in Antalya; talks extended.",
         scene="cop", lat=36.90, lon=30.71),
    dict(n=6, kind="card", region="EUROPE", field="POLITICS",
         label="CONFIRMED", source="Brussels",
         headline="UK and EU sign three post-Brexit deals",
         summary="Biggest step since Brexit: food, carbon, youth mobility.",
         scene="brexit", lat=50.85, lon=4.35),
    dict(n=7, kind="card", region="EUROPE", field="SOCIETY",
         label="REPORTED", source="OneTurn",
         headline="Cost-of-living protests spread in Europe",
         summary="Students in 25 countries walk out over prices and fees.",
         scene="protest", lat=52.52, lon=13.41),
    dict(n=8, kind="card", region="N. AMERICA", field="TECHNOLOGY",
         label="REPORTED", source="US media",
         headline="FBI crime database reportedly hacked",
         summary="Hackers said to enter NCIC and a USDA payment system.",
         scene="hack", lat=38.91, lon=-77.04),
    dict(n=9, kind="card", region="EUROPE", field="POLITICS",
         label="CONFIRMED", source="Al Jazeera",
         headline="Denmark expels Russian diplomat over plot",
         summary="Two held over alleged plot to kill a US-Ukrainian rapper.",
         scene="expel", lat=55.68, lon=12.57),
    dict(n=10, kind="card", region="SPACE", field="SPACE",
         label="OFFICIAL", source="ESA · JAXA",
         headline="BepiColombo reaches Mercury after 8 years",
         summary="Orbit burn at 19:24 CET ends a 6-billion-mile voyage.",
         scene="mercury", lat=None, lon=None),
    dict(n=11, kind="card", region="LATIN AMERICA", field="DISASTER",
         label="CONFIRMED", source="USGS reports",
         headline="Magnitude 6.7 quake shakes Peru's Andes",
         summary="Strong tremor hits Junin in the central highlands.",
         scene="quake", lat=-11.16, lon=-75.99),
    dict(n=12, kind="card", region="LATIN AMERICA", field="POLITICS",
         label="CONFIRMED", source="Brasilia",
         headline="Bolsonaro hospitalised in Brasilia",
         summary="Former president treated for intestinal obstruction.",
         scene="hospital", lat=-15.79, lon=-47.88),
    dict(n=13, kind="card", region="EUROPE", field="POLITICS",
         label="CONFIRMED", source="Madrid",
         headline="Spain heads to election on 29 November",
         summary="Conservatives gain; banking-tax extension planned.",
         scene="ballot", lat=40.42, lon=-3.70),
    dict(n=14, kind="card", region="MIDDLE EAST", field="CONFLICT",
         label="REPORTED", source="AP",
         headline="Israeli fire kills Palestinians in Gaza",
         summary="Strikes continue as West Bank violence flares again.",
         scene="gaza", lat=31.50, lon=34.47),
    dict(n=15, kind="card", region="N. AMERICA", field="JUSTICE",
         label="CONFIRMED", source="AP",
         headline="Man convicted of starting Palisades fire",
         summary="Los Angeles jury finds him guilty over deadly blaze.",
         scene="fire", lat=34.05, lon=-118.24),
    dict(n=16, kind="card", region="N. AMERICA", field="JUSTICE",
         label="CONFIRMED", source="US court",
         headline="19 years in plot to kill Sikh leader",
         summary="Indian national sentenced in New York over Pannun plot.",
         scene="court", lat=40.71, lon=-74.01),
    dict(n=17, kind="card", region="AFRICA", field="POLITICS",
         label="CONFIRMED", source="Cape Town",
         headline="Phumzile Mlambo-Ngcuka dies aged 71",
         summary="Ex-UN Women chief and SA deputy president mourned.",
         scene="dove", lat=-33.92, lon=18.42),
    dict(n=18, kind="card", region="SPACE", field="SCIENCE",
         label="REPORTED", source="NASA",
         headline="NASA halts Mars science over hardware faults",
         summary="Perseverance and Mars Odyssey paused; comms a concern.",
         scene="mars", lat=None, lon=None),
]

BRIEFS = [
    (19, "Haiti: Salvadoran troops lose men to gang explosives."),
    (20, "Nigeria: boat of funeral mourners capsizes in Bayelsa."),
    (21, "Iraq: fire at Basra power station kills at least four."),
    (22, "France: police sentenced over racist beating of Zecler."),
    (23, "Argentina: country risk tops 1,000 points."),
    (24, "Kenya: onshore crude drilling begins in Turkana."),
    (25, "Uganda: gatherings, travel curbed over Ebola."),
    (26, "US loses measles elimination status, CDC says."),
    (27, "Riemann proof claimed with AI help, mathematician says."),
    (28, "CERN finds first evidence of ultra-rare decay."),
    (29, "Voyager 1 now 24 light-hours from Earth."),
    (30, "US sells deep-sea mining leases off American Samoa."),
    (31, "Pilotless air taxi carries a passenger in Japan."),
    (32, "Record X-ray laser flashes shorter than atom gaps."),
    (33, "Ancient mountain ranges found under Antarctic ice."),
    (34, "Saudi Arabia and Japan agree oil stockpile deal."),
    (35, "Japan sidelined by China as ties hit record low."),
    (36, "Nepal PM Balendra Shah to visit India."),
    (37, "India: 11 dead, 180+ in hospital after toxic alcohol."),
    (38, "Harden passes Kobe on NBA 50-point games list."),
    (39, "Verstappen on pole for Las Vegas GP after penalty."),
    (40, "Choi Min-jeong wins third straight 1,000m title."),
    (41, "Harry Kane out for months with ankle injury."),
    (42, "Alcaraz beats Cobolli at ATP Finals, thigh concern."),
    (43, "North Melbourne into fourth straight AFLW decider."),
    (44, "Texans beat Colts 26-3 behind CJ Stroud."),
    (45, "BTS wins five MAMA awards in Osaka."),
    (46, "Pakistan Shaheens beat UAE by 61 runs in Doha."),
    (47, "Rahul first Indian opener with tons in all SENA lands."),
    (48, "WBBL: Hurricanes' first win; Sixers seal finals."),
    (49, "Trump says he discussed ousted Nvidia chief with Xi."),
    (50, "Australia, Canada, NZ condemn Russia's war."),
    (51, "Melania Trump hopes for ceasefire before Christmas."),
    (52, "Bayer pays $7.25bn to settle Roundup complaints."),
    (53, "Indonesia hit by massive forest fires."),
    (54, "78 ransomware claims recorded worldwide in 48 hours."),
    (55, "India secures AFC U17 Asian Cup 2027 berth."),
    (56, "Trump defends Putin ties; Zelensky calls him a killer."),
    (57, "Russia claims two more Donetsk settlements."),
    (58, "Russian strike hits a kindergarten in Zaporizhzhia."),
    (59, "Iraqi police move into Jurf al-Sakhar under deal."),
    (60, "FEMA has an emergency of its own: bed bugs."),
]

DATE_CHECK = (
    "LEFT OUT ON PURPOSE — NOT 21 NOV: ICJ Myanmar genocide ruling (Thu 19 Nov) · "
    "Anthropic market debut, ~$2tn (Thu 19 Nov) · Trump–Xi–Putin Shenzhen summit "
    "(18–20 Nov) · Kerch Bridge hit (16–17 Nov) · Nvidia record quarter (Tue 17 Nov) · "
    "$22.5m train-heist charges (Thu 19 Nov).  NOT YET: Ukraine drone hits Russian "
    "nuclear plant (Sun 22 Nov) · BepiColombo orbiters separate (9–10 Dec) · "
    "Spain votes (Sun 29 Nov)."
)

NUMBERS = [
    ("400+", "drones fired at Ukraine"),
    ("110", "missiles in the overnight barrage"),
    ("8", "killed in Kyiv"),
    ("-3.7%", "S&P 500, into correction"),
    ("25", "nations in cost-of-living walkouts"),
    ("1 in 12", "patients: tumours undetectable"),
]

UTC_LINES = [
    "00:44 UTC  Russian missiles come down in Poland",
    "06:50 UTC  Russia fires 3 ballistic missiles + 148 drones",
    "18:24 UTC  BepiColombo burns for Mercury capture (19:24 CET)",
]

REGION_LINE = ("N. AMERICA 14  ·  EUROPE 14  ·  ASIA-PACIFIC 15  ·  LATIN AMERICA 4  ·  "
               "MIDDLE EAST 4  ·  AFRICA 4  ·  SPACE & BEYOND 5")

FOOTER_SOURCES = ("Sources: BBC · AP · Reuters · AFP · NYT · ESA/JAXA · NASA · CERN · "
                  "Kyiv Independent · Ukrayinska Pravda · IANS · Cricinfo · Straits Times · "
                  "OneTurn · Horizon — Every story happened, or was first reported, on "
                  "Saturday 21 November 2026. Original drawings; no photographs.")

# ---------------------------------------------------------------- helpers
def wrap(d, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill=INK, leading=None, align="left",
               width=None):
    """Draw lines starting at (x, y); returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        if align == "center":
            d.text((x + (width - d.textlength(ln, font=fnt)) / 2, y), ln,
                   font=fnt, fill=fill)
        else:
            d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, fill=INK, w=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def burst(d, cx, cy, r, fill):
    """Explosion star: 8 triangles around a centre."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def skyline(d, x, y, w, h, fill, tops):
    """Row of building silhouettes; tops = list of (dx, bw, bh)."""
    for dx, bw, bh in tops:
        d.rectangle([x + dx, y + h - bh, x + dx + bw, y + h], fill=fill)


# ------------------------------------------------------- scene painters
# Each paints a drawn illustration into box (x, y, w, h) on draw `d`.
def sc_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 28, 44))
    d.ellipse([x + w - 26, y + 8, x + w - 8, y + 26], fill=(232, 220, 180))
    skyline(d, x, y + h - 42, w, 42, (12, 14, 26),
            [(4, 26, 42), (34, 20, 30), (58, 30, 42), (92, 18, 26),
             (114, 26, 40), (144, 20, 30), (168, 28, 42), (200, 22, 28)])
    burst(d, x + 52, y + 26, 17, (255, 150, 40))
    burst(d, x + 52, y + 26, 9, (255, 220, 120))
    burst(d, x + 168, y + 40, 13, (255, 120, 30))
    d.line([(x + 90, y + 8), (x + 150, y + 44)], fill=(255, 220, 120), width=2)
    d.line([(x + 120, y + 4), (x + 190, y + 52)], fill=(255, 200, 90), width=2)


def sc_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 32, 40))
    for i, (bx, bw, bh, top) in enumerate([(14, 16, 26, 30), (40, 16, 34, 22),
                                           (66, 16, 22, 44), (92, 16, 40, 14),
                                           (118, 16, 30, 52), (144, 16, 36, 20),
                                           (170, 16, 24, 58), (196, 16, 30, 30)]):
        col = (214, 48, 49) if i % 2 else (235, 90, 80)
        d.rectangle([x + bx, y + h - 12 - bh, x + bx + bw, y + h - 12], fill=col)
        d.line([(x + bx + 8, y + h - 12 - bh - top), (x + bx + 8, y + h - 12)],
               fill=col, width=2)
    pts = [(x + 8, y + 18), (x + 50, y + 26), (x + 92, y + 22),
           (x + 134, y + 44), (x + 176, y + 52), (x + 226, y + 74)]
    d.line(pts, fill=(255, 220, 90), width=3, joint="curve")
    d.polygon([(x + 226, y + 66), (x + 240, y + 78), (x + 226, y + 86)],
              fill=(255, 220, 90))


def sc_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 178, 110))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(28, 68, 96))
    d.rectangle([x + 30, y + h - 56, x + 210, y + h - 34], fill=(40, 40, 44))
    d.rectangle([x + 44, y + h - 72, x + 84, y + h - 56], fill=(52, 52, 56))
    d.rectangle([x + 150, y + h - 66, x + 162, y + h - 56], fill=(52, 52, 56))
    burst(d, x + 196, y + 30, 15, (255, 120, 30))
    burst(d, x + 196, y + 30, 8, (255, 210, 110))
    d.line([(x + 60, y + 12), (x + 120, y + 48)], fill=(90, 60, 40), width=2)
    for wx in (20, 90, 160, 210):
        d.arc([x + wx, y + h - 22, x + wx + 22, y + h - 6], 0, 180,
              fill=(160, 200, 220), width=2)


def sc_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 238, 232))
    d.ellipse([x + 14, y + 10, x + 74, y + 70], fill=(255, 255, 255),
              outline=(31, 78, 121), width=2)
    d.ellipse([x + 22, y + 18, x + 66, y + 62], outline=(31, 78, 121), width=2)
    d.line([(x + 44, y + 24), (x + 44, y + 56)], fill=(178, 32, 44), width=5)
    d.line([(x + 28, y + 40), (x + 60, y + 40)], fill=(178, 32, 44), width=5)
    # capsule
    d.rounded_rectangle([x + 96, y + 26, x + 226, y + 58], radius=16,
                        fill=(178, 32, 44))
    d.rounded_rectangle([x + 96, y + 26, x + 161, y + 58], radius=16,
                        fill=(247, 243, 233))
    d.ellipse([x + 178, y + 66, x + 196, y + 84], fill=(31, 78, 121))
    d.ellipse([x + 202, y + 70, x + 216, y + 84], fill=(176, 141, 42))


def sc_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 90, 70))
    d.ellipse([x + w / 2 - 20, y + 6, x + w / 2 + 20, y + 46], fill=(120, 190, 160))
    d.arc([x + w / 2 - 20, y + 6, x + w / 2 + 20, y + 46], 200, 340,
          fill=(20, 60, 46), width=2)
    d.rectangle([x + 8, y + h - 12, x + w - 8, y + h - 6], fill=(176, 141, 42))
    d.polygon([(x + 18, y + h - 12), (x + 30, y + h - 30), (x + 42, y + h - 12)],
              fill=(255, 150, 40))
    d.polygon([(x + w - 42, y + h - 12), (x + w - 30, y + h - 28),
               (x + w - 18, y + h - 12)], fill=(255, 150, 40))


def sc_brexit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 78, 121))
    d.rectangle([x + 14, y + 8, x + 64, y + h - 8], fill=(255, 255, 255))
    d.line([(x + 14, y + 8), (x + 64, y + h - 8)], fill=(178, 32, 44), width=4)
    d.line([(x + 64, y + 8), (x + 14, y + h - 8)], fill=(178, 32, 44), width=4)
    d.line([(x + 39, y + 8), (x + 39, y + h - 8)], fill=(178, 32, 44), width=4)
    d.line([(x + 14, y + h / 2), (x + 64, y + h / 2)], fill=(178, 32, 44), width=4)
    for i in range(8):
        import math
        a = math.pi * i / 4
        d.ellipse([x + 100 + 16 * math.cos(a) - 2, y + h / 2 + 12 * math.sin(a) - 2,
                   x + 100 + 16 * math.cos(a) + 2, y + h / 2 + 12 * math.sin(a) + 2],
                  fill=(255, 220, 90))


def sc_protest(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 190))
    for cx, col in [(28, (31, 78, 121)), (62, (178, 32, 44)), (96, (31, 78, 121)),
                    (122, (90, 86, 78))]:
        d.ellipse([x + cx - 7, y + 12, x + cx + 7, y + 26], fill=col)
        d.polygon([(x + cx - 11, y + h - 4), (x + cx - 11, y + 28),
                   (x + cx + 11, y + 28), (x + cx + 11, y + h - 4)], fill=col)
    d.rectangle([x + 52, y + 4, x + 118, y + 18], fill=(255, 255, 255),
                outline=INK, width=1)


def sc_hack(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 28))
    d.rectangle([x + 14, y + 8, x + w - 14, y + h - 10], outline=(80, 200, 140),
                width=2)
    d.text((x + 20, y + 12), "01 10 11 00", font=SANS_B(9), fill=(80, 200, 140))
    d.text((x + 20, y + 26), "ACCESS", font=SANS_B(9), fill=(255, 80, 70))
    d.rectangle([x + w - 44, y + h - 22, x + w - 20, y + h - 12],
                outline=(255, 220, 90), width=2)


def sc_expel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    d.rectangle([x + 22, y + 6, x + 92, y + h - 6], fill=(255, 255, 255),
                outline=INK, width=1)
    d.line([(x + 30, y + 14), (x + 84, y + 14)], fill=GREY, width=2)
    d.line([(x + 30, y + 22), (x + 84, y + 22)], fill=GREY, width=2)
    d.line([(x + 30, y + 30), (x + 64, y + 30)], fill=GREY, width=2)
    d.ellipse([x + 96, y + 10, x + 128, y + 42], outline=(178, 32, 44), width=3)
    d.line([(x + 104, y + 26), (x + 120, y + 26)], fill=(178, 32, 44), width=3)
    d.line([(x + 112, y + 18), (x + 112, y + 34)], fill=(178, 32, 44), width=3)


def sc_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 26))
    for sx, sy in [(16, 10), (120, 8), (60, 46), (132, 40)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + 44, y + 6, x + 96, y + 50], fill=(176, 160, 140))
    for cx, cy, r in [(58, 20, 5), (78, 34, 7), (66, 40, 4), (86, 16, 3)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(140, 126, 108))
    d.polygon([(x + 104, y + 22), (x + 124, y + 18), (x + 124, y + 30),
               (x + 104, y + 28)], fill=(220, 220, 220))
    d.line([(x + 96, y + 24), (x + 104, y + 24)], fill=(220, 220, 220), width=2)


def sc_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.polygon([(x + 6, y + h - 8), (x + 46, y + 10), (x + 86, y + h - 8)],
              fill=(120, 110, 88))
    d.polygon([(x + 70, y + h - 8), (x + 110, y + 16), (x + 134, y + h - 8)],
              fill=(90, 82, 64))
    d.line([(x + 46, y + 10), (x + 40, y + h - 8)], fill=(247, 243, 233), width=2)
    d.line([(x + 20, y + h - 8), (x + 30, y + h - 26), (x + 24, y + h - 14),
            (x + 36, y + h - 30)], fill=(178, 32, 44), width=2)
    d.line([(x + 90, y + h - 8), (x + 100, y + h - 24), (x + 96, y + h - 12),
            (x + 108, y + h - 28)], fill=(178, 32, 44), width=2)


def sc_hospital(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 244))
    d.rectangle([x + 40, y + 8, x + 100, y + h - 6], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([x + 62, y + 14, x + 78, y + 34], fill=(178, 32, 44))
    d.rectangle([x + 56, y + 20, x + 84, y + 28], fill=(178, 32, 44))
    d.rectangle([x + 14, y + h - 14, x + 126, y + h - 8], fill=(31, 78, 121))


def sc_ballot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 228, 200))
    d.rectangle([x + 40, y + 14, x + 100, y + h - 6], fill=(178, 32, 44))
    d.rectangle([x + 52, y + 8, x + 88, y + 16], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((x + 56, y + 20), "VOTE", font=SANS_B(11), fill=(255, 255, 255))
    d.rectangle([x + 14, y + h - 12, x + 30, y + h - 6], fill=(255, 220, 90))
    d.rectangle([x + 110, y + h - 12, x + 126, y + h - 6], fill=(31, 78, 121))


def sc_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    skyline(d, x, y + h - 30, w, 30, (90, 82, 64),
            [(6, 24, 30), (34, 18, 20), (56, 26, 30), (86, 20, 24),
             (110, 26, 30)])
    d.ellipse([x + 44, y + 4, x + 84, y + 34], fill=(160, 150, 132))
    d.ellipse([x + 96, y + 10, x + 124, y + 30], fill=(140, 132, 116))


def sc_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 24, 20))
    d.polygon([(x + 30, y + h - 6), (x + 52, y + 8), (x + 62, y + 26),
               (x + 76, y + 6), (x + 104, y + h - 6)], fill=(255, 120, 30))
    d.polygon([(x + 52, y + h - 6), (x + 62, y + 26), (x + 74, y + 34),
               (x + 84, y + h - 6)], fill=(255, 220, 90))
    d.rectangle([x + 8, y + h - 8, x + w - 8, y + h - 4], fill=(20, 14, 12))


def sc_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    d.polygon([(x + 20, y + 10), (x + 70, y + 2), (x + 120, y + 10)],
              fill=(90, 82, 64))
    for cx in (34, 62, 90, 112):
        d.rectangle([x + cx - 4, y + 12, x + cx + 4, y + h - 10],
                    fill=(247, 243, 233), outline=INK, width=1)
    d.rectangle([x + 16, y + h - 10, x + 124, y + h - 4], fill=(90, 82, 64))


def sc_dove(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    d.ellipse([x + 46, y + 14, x + 94, y + 40], fill=(255, 255, 255),
              outline=GREY, width=1)
    d.polygon([(x + 88, y + 22), (x + 118, y + 14), (x + 118, y + 30)],
              fill=(255, 255, 255), outline=GREY)
    d.polygon([(x + 52, y + 16), (x + 66, y + 2), (x + 76, y + 16)],
              fill=(255, 255, 255), outline=GREY)
    d.ellipse([x + 84, y + 20, x + 88, y + 24], fill=INK)
    d.rectangle([x + 10, y + h - 8, x + 46, y + h - 4], fill=(178, 32, 44))
    d.rectangle([x + 46, y + h - 8, x + 82, y + h - 4], fill=(255, 255, 255))
    d.rectangle([x + 82, y + h - 8, x + 118, y + h - 4], fill=(31, 78, 121))


def sc_mars(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 26))
    for sx, sy in [(14, 8), (120, 12), (70, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    d.ellipse([x + 46, y + 8, x + 94, y + 48], fill=(198, 96, 60))
    d.ellipse([x + 58, y + 18, x + 70, y + 28], fill=(160, 70, 40))
    d.ellipse([x + 74, y + 30, x + 84, y + 38], fill=(160, 70, 40))
    d.rectangle([x + 104, y + 30, x + 126, y + 40], fill=(220, 220, 220))
    d.ellipse([x + 126, y + 32, x + 132, y + 38], fill=(220, 220, 220))

SCENES = {"strike": sc_strike, "markets": sc_markets, "hormuz": sc_hormuz,
          "pill": sc_pill, "cop": sc_cop, "brexit": sc_brexit,
          "protest": sc_protest, "hack": sc_hack, "expel": sc_expel,
          "mercury": sc_mercury, "quake": sc_quake, "hospital": sc_hospital,
          "ballot": sc_ballot, "gaza": sc_gaza, "fire": sc_fire,
          "court": sc_court, "dove": sc_dove, "mars": sc_mars}

# ------------------------------------------------------------- world map
# Coarse stylised continent outlines (lon, lat). Schematic, not survey-grade.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 73), (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-110, 24),
     (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-22, 70), (-30, 76), (-55, 76),
     (-60, 74)],
    [(-79, 9), (-72, 12), (-60, 8), (-50, 4), (-35, -6), (-35, -15),
     (-40, -22), (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40),
     (-73, -20), (-80, -5), (-81, 2)],
    [(-17, 15), (-10, 5), (-5, 5), (8, 4), (12, -2), (13, -12), (12, -18),
     (16, -28), (20, -35), (28, -33), (35, -25), (40, -15), (42, -10),
     (48, 11), (43, 12), (38, 18), (32, 31), (20, 32), (10, 37), (0, 36),
     (-10, 31), (-17, 21)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (5, 60), (12, 65), (18, 69), (25, 71), (30, 70), (40, 68),
     (45, 66), (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (20, 40),
     (15, 44), (10, 44), (5, 43), (0, 40), (-2, 37)],
    [(30, 70), (40, 68), (50, 69), (60, 70), (70, 73), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 50), (140, 45), (135, 43), (130, 42), (127, 40),
     (122, 38), (120, 32), (115, 23), (110, 20), (108, 12), (105, 9),
     (100, 8), (97, 16), (92, 21), (88, 22), (85, 20), (80, 15), (77, 8),
     (75, 12), (72, 20), (66, 25), (60, 25), (57, 26), (52, 28), (50, 30),
     (48, 30), (44, 29), (40, 32), (36, 36), (32, 36), (30, 42), (28, 45),
     (30, 48), (35, 52), (40, 55), (45, 60), (50, 65)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (136, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -23), (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -4), (140, -8)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44),
     (141, 45)],
]

# Pin offsets (dx, dy) to keep close pins apart: NYC, Washington, Europe cluster.
PIN_OFF = {2: (0, -6), 8: (-14, 8), 16: (16, 8), 1: (2, 14), 5: (-12, 12),
           6: (-20, 10), 7: (20, 2), 9: (16, -14), 13: (-22, 14), 14: (14, 8)}

# ---------------------------------------------------------------- layout
W, H = 1024, 1024
MX = 8                      # outer margin
RX = W - MX                 # right edge (1016)
CW = RX - MX                # content width (1008)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    d.text((MX + (CW - d.textlength("SATURDAY, 21 NOVEMBER 2026 — THE DAY IN FULL", font=SERIF_B(12))) / 2,
            8), "SATURDAY, 21 NOVEMBER 2026 — THE DAY IN FULL", font=SERIF_B(12), fill=RED)
    title = "THE WORLD IN ONE DAY"
    d.text((MX + (CW - d.textlength(title, font=SERIF_B(44))) / 2, 24),
           title, font=SERIF_B(44), fill=INK)
    sub = "60 STORIES  ·  7 REGIONS  ·  15 FIELDS"
    d.text((MX + (CW - d.textlength(sub, font=SANS_B(13))) / 2, 78),
           sub, font=SANS_B(13), fill=INK)
    d.text((MX + (CW - d.textlength(REGION_LINE, font=SANS(9))) / 2, 94),
           REGION_LINE, font=SANS(9), fill=GREY)
    hline(d, MX, RX, 106, INK, 2)
    hline(d, MX, RX, 109, INK, 1)

    # ---- leads ----------------------------------------------------
    leads = [s for s in STORIES if s["kind"] == "lead"]
    lx = [MX, 261, 514, 767]
    lw = 245
    for s, x in zip(leads, lx):
        SCENES[s["scene"]](d, x, 114, lw, 92)
        d.rectangle([x, 114, x + lw, 206], outline=INK, width=1)
        tag = "%d · %s · %s · %s" % (s["n"], s["region"], s["field"], s["label"])
        d.text((x, 210), tag, font=SANS_B(8), fill=RED)
        hl = wrap(d, s["headline"], SERIF_B(13), lw)
        text_block(d, x, 224, hl[:2], SERIF_B(13), leading=16)
        sm = wrap(d, s["summary"], SANS(9), lw)
        text_block(d, x, 258, sm[:3], SANS(9), leading=11)
        d.text((x, 292), s["source"], font=SANS(7), fill=GREY)
    hline(d, MX, RX, 304, INK, 1)

    # ---- medium cards ---------------------------------------------
    cards = [s for s in STORIES if s["kind"] == "card"]
    cw, step = 139, 144
    for i, s in enumerate(cards):
        col, row = i % 7, i // 7
        x = MX + col * step
        y = 310 + row * 96
        SCENES[s["scene"]](d, x, y, cw, 40)
        d.rectangle([x, y, x + cw, y + 40], outline=INK, width=1)
        tag = "%d · %s · %s" % (s["n"], s["region"], s["field"])
        d.text((x, y + 44), tag, font=SANS_B(7), fill=RED)
        hl = wrap(d, s["headline"], SERIF_B(9), cw)
        text_block(d, x, y + 56, hl[:2], SERIF_B(9), leading=11)
        d.text((x, y + 80), "%s — %s" % (s["label"], s["source"]),
               font=SANS(7), fill=GREY)
    hline(d, MX, RX, 500, INK, 1)

    # ---- map + numbers --------------------------------------------
    d.text((MX, 506), "WHERE IT HAPPENED — 18 STORIES PINNED",
           font=SANS_B(11), fill=INK)
    d.text((616, 506), "THE DAY IN NUMBERS", font=SANS_B(11), fill=INK)
    map_x0, map_y0, map_w, map_h = MX, 524, 596, 164
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], fill=OCEAN,
                outline=INK, width=1)

    def proj(lon, lat):
        return (map_x0 + (lon + 180) / 360 * map_w,
                map_y0 + (90 - lat) / 180 * map_h)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=MAPINK)
    for s in STORIES:
        if s["lat"] is None:
            continue
        px, py = proj(s["lon"], s["lat"])
        dx, dy = PIN_OFF.get(s["n"], (0, 0))
        px, py = px + dx, py + dy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255),
                  width=1)
        num = str(s["n"])
        d.text((px - d.textlength(num, font=SANS_B(8)) / 2, py - 6), num,
               font=SANS_B(8), fill=(255, 255, 255))
    # space stories live off the map: small legend at its top-right corner
    for n, label, yy in ((10, "MERCURY", 532), (18, "MARS", 554)):
        d.ellipse([map_x0 + map_w - 118, yy - 7, map_x0 + map_w - 104, yy + 7],
                  fill=NAVY, outline=(255, 255, 255), width=1)
        num = str(n)
        d.text((map_x0 + map_w - 111 - d.textlength(num, font=SANS_B(8)) / 2,
                yy - 6), num, font=SANS_B(8), fill=(255, 255, 255))
        d.text((map_x0 + map_w - 100, yy - 6), label, font=SANS_B(8), fill=INK)
    d.text((map_x0 + 4, map_y0 + map_h - 12),
           "Stylised map — pins numbered as the stories above.",
           font=SANS(7), fill=GREY)

    # numbers grid: 2 cols x 3 rows
    for i, (big, label) in enumerate(NUMBERS):
        col, row = i % 2, i // 2
        nx = 616 + col * 200
        ny = 524 + row * 38
        d.text((nx, ny), big, font=SANS_B(20), fill=RED)
        d.text((nx, ny + 24), label, font=SANS(8), fill=INK)
    d.text((616, 640), "THE DAY IN UTC", font=SANS_B(9), fill=INK)
    yy = 654
    for ln in UTC_LINES:
        d.text((616, yy), ln, font=SANS(8), fill=INK)
        yy += 11
    hline(d, MX, RX, 694, INK, 1)

    # ---- briefs ---------------------------------------------------
    d.text((MX, 700), "ALSO ON 21 NOVEMBER — 42 MORE STORIES",
           font=SANS_B(11), fill=INK)
    cols = [BRIEFS[i * 14:(i + 1) * 14] for i in range(3)]
    for ci, col in enumerate(cols):
        bx = MX + ci * 340
        yy = 718
        for n, txt in col:
            d.text((bx, yy), "%d." % n, font=SANS_B(9), fill=RED)
            d.text((bx + 22, yy), txt, font=SANS(9), fill=INK)
            yy += 14
    hline(d, MX, RX, 918, INK, 1)

    # ---- date check -----------------------------------------------
    d.rectangle([MX, 924, RX, 968], fill=PAPER2, outline=RED, width=1)
    d.text((MX + 6, 928), "DATE CHECK — LEFT OUT ON PURPOSE",
           font=SANS_B(10), fill=RED)
    dc = wrap(d, DATE_CHECK, SANS(8), CW - 12)
    text_block(d, MX + 6, 942, dc[:2], SANS(8), leading=11)

    # ---- footer ---------------------------------------------------
    hline(d, MX, RX, 974, INK, 1)
    fs = wrap(d, FOOTER_SOURCES, SANS(8), CW)
    text_block(d, MX, 980, fs[:2], SANS(8), leading=11)
    foot = "THE WORLD IN ONE DAY  ·  SATURDAY 21 NOVEMBER 2026  ·  ORIGINAL DRAWINGS — NO PHOTOGRAPHS"
    d.text((MX + (CW - d.textlength(foot, font=SANS_B(8))) / 2, 1006),
           foot, font=SANS_B(8), fill=INK)
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print("wrote %s  %dx%d  %d bytes (%.1f KiB)" %
          (out, img.width, img.height, size, size / 1024))
    assert img.width <= 1024 and img.height <= 1024, "too large in pixels"
    assert size <= 1048576, "over 1 MiB"
    with open(out, "rb") as f:
        assert f.read(8) == b"\x89PNG\r\n\x1a\n", "not a PNG"


if __name__ == "__main__":
    main()

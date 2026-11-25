#!/usr/bin/env python3
"""Render the front page for Tuesday 24 November 2026.

The page is "The World in One Page": six stories from the day's
wire reports plus a short briefs strip, drawn with Pillow shapes
and DejaVu type. Nothing is random and nothing reads the clock,
so running this script twice writes the same PNG bytes.
Stories are data: a table up top, one small renderer below it.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 40
C = {
    "paper": (247, 243, 234),
    "ink": (26, 24, 22),
    "soft": (84, 78, 70),
    "body": (52, 48, 44),
    "red": (163, 38, 32),
    "teal": (18, 92, 96),
    "gold": (184, 134, 11),
    "blue": (70, 110, 160),
    "green": (46, 110, 62),
    "sun": (232, 164, 32),
}

FONTDIR = "/usr/share/fonts/truetype/dejavu/"
F = {
    "serif_b": lambda s: ImageFont.truetype(FONTDIR + "DejaVuSerif-Bold.ttf", s),
    "serif": lambda s: ImageFont.truetype(FONTDIR + "DejaVuSerif.ttf", s),
    "sans_b": lambda s: ImageFont.truetype(FONTDIR + "DejaVuSans-Bold.ttf", s),
    "sans": lambda s: ImageFont.truetype(FONTDIR + "DejaVuSans.ttf", s),
}


def width_of(d, text, fnt):
    box = d.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def split_lines(d, text, fnt, width):
    """Greedy word wrap, measured with textbbox."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        line = ""
        for word in words:
            cand = (line + " " + word).strip()
            if width_of(d, cand, fnt) <= width or not line:
                line = cand
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
    return out


def put_text(d, x, y, text, fnt, width, color, gap):
    step = int(fnt.size * gap)
    for ln in split_lines(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=color)
        y += step
    return y


def tag(d, x, y, text, color):
    """Section label: a small dot, then the label in bold caps."""
    d.ellipse([x, y + 4, x + 10, y + 14], fill=color)
    d.text((x + 16, y), text.upper(), font=F["sans_b"](16), fill=color)
    return y + 26


def article(d, x, y, w, h, item):
    """One story: tag, headline, body, and an optional picture."""
    yy = tag(d, x, y, item["tag"], C["red"])
    art_w = item.get("art_w", 0)
    yy = put_text(d, x, yy, item["head"], F["serif_b"](item["hs"]),
                  w - art_w, C["ink"], 1.12)
    yy += 5
    yy = put_text(d, x, yy, item["body"], F["serif"](item["bs"]),
                  w - art_w, C["body"], 1.28)
    art = item.get("art")
    if art:
        art(d, x + w - art_w + 6, y + 34)
    print(f"article '{item['tag'][:20]}' ends y={yy} box bottom={y + h}")
    assert yy <= y + h, f"text overflow in {item['tag']}: {yy} > {y + h}"
    return yy


# ---------- pictures: each draws inside a small box ----------

def pic_chip(d, x, y):
    """A processor chip with pins around it."""
    d.rectangle([x + 14, y + 8, x + 86, y + 78], fill=(30, 32, 40),
                outline=C["ink"], width=3)
    d.rectangle([x + 30, y + 24, x + 70, y + 62], fill=C["teal"],
                outline=C["gold"], width=3)
    for i in range(4):
        px = x + 24 + i * 18
        d.line([px, y, px, y + 8], fill=C["ink"], width=4)
        d.line([px, y + 78, px, y + 86], fill=C["ink"], width=4)
        py = y + 18 + i * 18
        d.line([x + 6, py, x + 14, py], fill=C["ink"], width=4)
        d.line([x + 86, py, x + 94, py], fill=C["ink"], width=4)


def pic_boat(d, x, y):
    """A cargo ship on two waves."""
    d.polygon([(x, y + 30), (x + 104, y + 30), (x + 90, y + 47),
               (x + 14, y + 47)], fill=C["body"], outline=C["ink"])
    d.rectangle([x + 36, y + 13, x + 70, y + 30], fill=(230, 225, 214),
                outline=C["ink"], width=2)
    for i in range(2):
        wy = y + 56 + i * 9
        d.line([x - 4, wy, x + 110, wy], fill=C["blue"], width=3)


def pic_sat(d, x, y):
    """A satellite: body in the middle, a panel each side, a dish."""
    d.rectangle([x + 38, y + 18, x + 70, y + 50], fill=(230, 225, 214),
                outline=C["ink"], width=2)
    d.rectangle([x + 4, y + 24, x + 38, y + 44], fill=C["blue"],
                outline=C["ink"], width=2)
    d.rectangle([x + 70, y + 24, x + 104, y + 44], fill=C["blue"],
                outline=C["ink"], width=2)
    for px in (x + 15, x + 26, x + 81, x + 92):
        d.line([px, y + 24, px, y + 44], fill=C["ink"], width=2)
    d.arc([x + 44, y + 2, x + 64, y + 18], 200, 340, fill=C["gold"], width=4)
    d.ellipse([x + 50, y + 28, x + 58, y + 36], fill=C["gold"],
              outline=C["ink"], width=1)


def pic_sun(d, x, y):
    """A sun with eight rays."""
    cx, cy = x + 52, y + 34
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=C["sun"],
              outline=C["ink"], width=3)
    for dx, dy in [(0, -40), (28, -28), (40, 0), (28, 28), (0, 40),
                   (-28, 28), (-40, 0), (-28, -28)]:
        d.line([cx + dx * 0.72, cy + dy * 0.72, cx + dx, cy + dy],
               fill=C["sun"], width=5)


def pic_balance(d, x, y):
    """Scales of justice."""
    d.line([x + 52, y, x + 52, y + 56], fill=C["ink"], width=4)
    d.line([x + 4, y + 8, x + 100, y + 8], fill=C["ink"], width=4)
    for px in (x + 4, x + 100):
        d.line([px, y + 8, px - 15, y + 32], fill=C["ink"], width=2)
        d.line([px, y + 8, px + 15, y + 32], fill=C["ink"], width=2)
        d.arc([px - 17, y + 24, px + 17, y + 44], 0, 180, fill=C["gold"],
              width=4)
    d.line([x + 32, y + 56, x + 72, y + 56], fill=C["ink"], width=4)


def pic_box(d, x, y):
    """A ballot box with a paper slip and a green tick."""
    d.rectangle([x + 10, y + 26, x + 94, y + 78], fill=(230, 225, 214),
                outline=C["ink"], width=3)
    d.rectangle([x + 34, y + 26, x + 70, y + 34], fill=C["ink"])
    d.polygon([(x + 44, y - 8), (x + 62, y - 8), (x + 58, y + 26),
               (x + 48, y + 26)], fill=(255, 255, 255), outline=C["ink"])
    d.line([x + 50, y + 2, x + 58, y + 2], fill=C["red"], width=2)
    d.line([x + 50, y + 8, x + 58, y + 8], fill=C["red"], width=2)
    d.ellipse([x + 44, y + 44, x + 60, y + 60], fill=C["green"],
              outline=C["ink"], width=2)
    d.line([x + 48, y + 52, x + 52, y + 56], fill=(255, 255, 255), width=3)
    d.line([x + 52, y + 56, x + 58, y + 48], fill=(255, 255, 255), width=3)


ART = {"chip": pic_chip, "boat": pic_boat, "sat": pic_sat, "sun": pic_sun,
       "balance": pic_balance, "box": pic_box}


# ---------- the day's stories (data) ----------

LEAD = {
    "tag": "Technology · Santa Clara, USA",
    "head": "Nvidia Brings Back Huang as Chief; Shares Jump 31%",
    "body": ("Nvidia's board reinstated Jensen Huang as chief executive "
             "on Monday after pressure from President Trump, less than "
             "two weeks after he resigned. Shares rose 31% in a day, "
             "lifting stocks worldwide."),
    "hs": 37, "bs": 19, "art": pic_chip, "art_w": 0,
}

SIDE = {
    "tag": "Conflict · Benghazi, Libya",
    "head": "Ukraine Says It Sank Russian Warship Off Libya",
    "body": ("President Zelensky confirmed Ukraine used seven naval "
             "drones to sink the Russian corvette Merkury at Benghazi. "
             "The UN called for a probe."),
    "hs": 27, "bs": 17, "art": pic_boat, "art_w": 0,
}

GRID = [
    {"tag": "Space · Brussels",
     "head": "NATO Vows to Defend Space After Russian Nuclear Satellite Reports",
     "body": ("NATO chief Mark Rutte said the alliance will defend "
              "against any threat in space after reports that Russia "
              "was preparing to launch a nuclear-armed satellite."),
     "hs": 22, "bs": 15, "art": pic_sat, "art_w": 108},
    {"tag": "Climate · Antalya, Türkiye",
     "head": "Climate Summit Ends Without Deal as Fossil-Fuel Split Deepens",
     "body": ("The UN climate summit in Antalya ended without a deal "
              "after a dispute over fossil fuels and climate finance."),
     "hs": 22, "bs": 15, "art": pic_sun, "art_w": 108},
    {"tag": "Justice · The Hague",
     "head": "Court Rules Myanmar Committed Genocide Against Rohingya",
     "body": ("The International Court of Justice ruled Myanmar "
              "committed genocide against the Rohingya. Fourteen "
              "countries, including the UK, Spain and Canada, backed "
              "the decision."),
     "hs": 22, "bs": 15, "art": pic_balance, "art_w": 108},
    {"tag": "Politics · Washington, USA",
     "head": "Democrats Win House by Largest Margin in Decades",
     "body": ("Democrats won control of the US House of Representatives "
              "by the largest margin in decades, reshaping the balance "
              "of power in Washington."),
     "hs": 22, "bs": 15, "art": pic_box, "art_w": 108},
]

BRIEFS = [
    "Indonesia — factory fire in Banten kills 26, dozens missing.",
    "Nepal — a 5.6 magnitude earthquake strikes near the Chinese border.",
    "Space — Pakistan's Zeeshan Ali set to be the first foreign "
    "astronaut on China's Tiangong station.",
]


def masthead(d):
    """Title, date line and rules at the top of the page."""
    d.line([EDGE, 34, PAGE - EDGE, 34], fill=C["ink"], width=3)
    title = "THE WORLD IN ONE PAGE"
    tf = F["serif_b"](58)
    d.text(((PAGE - width_of(d, title, tf)) / 2, 46), title, font=tf,
           fill=C["ink"])
    d.line([EDGE, 122, PAGE - EDGE, 122], fill=C["ink"], width=2)
    d.line([EDGE, 128, PAGE - EDGE, 128], fill=C["ink"], width=5)
    dl = F["sans"](19)
    d.text((EDGE, 140), "Tuesday, 24 November 2026", font=dl, fill=C["ink"])
    mid = "World news in one image"
    d.text(((PAGE - width_of(d, mid, dl)) / 2, 140), mid, font=dl,
           fill=C["soft"])
    right = "Vol. IV · No. 24"
    d.text((PAGE - EDGE - width_of(d, right, dl), 140), right, font=dl,
           fill=C["ink"])
    d.line([EDGE, 170, PAGE - EDGE, 170], fill=C["ink"], width=2)


def build():
    img = Image.new("RGB", (PAGE, PAGE), C["paper"])
    d = ImageDraw.Draw(img)
    masthead(d)

    # Row A: lead on the left, warship on the right, a rule between.
    lx, lw = EDGE, 564
    rx = 652
    rw = PAGE - EDGE - rx
    y = tag(d, lx, 188, LEAD["tag"], C["red"])
    y = put_text(d, lx, y, LEAD["head"], F["serif_b"](LEAD["hs"]), lw,
                 C["ink"], 1.12)
    y += 8
    y = put_text(d, lx, y, LEAD["body"], F["serif"](LEAD["bs"]), 392,
                 C["body"], 1.3)
    print(f"lead ends y={y}")
    assert y <= 502
    pic_chip(d, 452, 396)
    d.line([628, 188, 628, 502], fill=C["ink"], width=2)
    y = tag(d, rx, 188, SIDE["tag"], C["red"])
    y = put_text(d, rx, y, SIDE["head"], F["serif_b"](SIDE["hs"]), rw,
                 C["ink"], 1.14)
    y += 6
    y = put_text(d, rx, y, SIDE["body"], F["serif"](SIDE["bs"]), rw,
                 C["body"], 1.3)
    print(f"warship ends y={y}")
    assert y <= 400
    pic_boat(d, rx + 140, 428)
    d.line([EDGE, 516, PAGE - EDGE, 516], fill=C["ink"], width=3)

    # Rows B and C: two stories a row, from the GRID table.
    colw = (PAGE - 2 * EDGE - 24) // 2
    x2 = EDGE + colw + 24
    d.line([EDGE + colw + 12, 532, EDGE + colw + 12, 918], fill=C["ink"],
           width=2)
    article(d, EDGE, 532, colw, 184, GRID[0])
    article(d, x2, 532, colw, 184, GRID[1])
    d.line([EDGE, 724, PAGE - EDGE, 724], fill=C["ink"], width=2)
    article(d, EDGE, 738, colw, 180, GRID[2])
    article(d, x2, 738, colw, 180, GRID[3])

    # Briefs strip and footer.
    d.line([EDGE, 928, PAGE - EDGE, 928], fill=C["ink"], width=3)
    d.text((EDGE, 938), "IN BRIEF", font=F["sans_b"](15), fill=C["red"])
    y = 956
    for b in BRIEFS:
        d.text((EDGE, y), "•  " + b, font=F["serif"](14), fill=C["body"])
        y += 16
    print(f"briefs end y={y}")
    assert y <= 1006
    foot = ("Drawn from wire reports of Tuesday, 24 November 2026 · "
            "Original artwork, not a screenshot")
    ff = F["sans"](13)
    d.text(((PAGE - width_of(d, foot, ff)) / 2, 1009), foot, font=ff,
           fill=C["soft"])

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    build()

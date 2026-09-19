#!/usr/bin/env python3
"""Render the AU industrial-nodes schematic with a full node key.

Sales graphic for the Kangaroo-class SpaceX / SpaceXAI pitch.
Not a navigation chart and not a Starbase site map.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "au-sites-map.png"

NAVY = (7, 14, 26)
PANEL = (13, 26, 42)
LAND = (18, 36, 58)
GOLD = (212, 175, 55)
PEACH = (232, 168, 124)
CYAN = (61, 190, 182)
LIGHT = (240, 244, 250)
MUTED = (154, 171, 191)

# Gold = live industrial. Peach = adjacency / diligence. Cyan = institutional hub.
SITES = [
    {
        "name": "Christmas Is.",
        "role": "Starship recovery adjacency — not a pad",
        "xy": (118, 248),
        "color": PEACH,
        "label": "below",
    },
    {
        "name": "North (diligence)",
        "role": "Future heavy-lift geography only",
        "xy": (500, 138),
        "color": PEACH,
        "label": "right",
    },
    {
        "name": "Bowen / Gilmour",
        "role": "Licensed orbital pad · Eris",
        "xy": (708, 248),
        "color": GOLD,
        "label": "right",
    },
    {
        "name": "Koonibba / Whalers Way",
        "role": "Southern Launch re-entry + orbital",
        "xy": (318, 388),
        "color": GOLD,
        "label": "left",
    },
    {
        "name": "Adelaide",
        "role": "Neumann EP · Fleet Space",
        "xy": (428, 498),
        "color": CYAN,
        "label": "left",
    },
    {
        "name": "Melbourne",
        "role": "Titomic / Lab22 · SpIRIT ≠ Gilmour",
        "xy": (538, 568),
        "color": CYAN,
        "label": "right",
    },
    {
        "name": "Canberra",
        "role": "ASA · ADFA · UNSW Canberra · EOS",
        "xy": (608, 448),
        "color": CYAN,
        "label": "below",
    },
    {
        "name": "W. Sydney Academy",
        "role": "Academy + Westmead compute/clinical",
        "xy": (728, 368),
        "color": GOLD,
        "label": "right",
    },
]

OUTLINE = [
    (520, 40),
    (580, 70),
    (640, 120),
    (700, 200),
    (740, 280),
    (760, 360),
    (750, 450),
    (720, 520),
    (680, 560),
    (620, 590),
    (540, 610),
    (460, 600),
    (400, 560),
    (360, 500),
    (340, 420),
    (320, 340),
    (300, 280),
    (280, 220),
    (300, 160),
    (340, 100),
    (400, 60),
    (460, 40),
    (520, 40),
]


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    return ImageFont.truetype(str(path), size)


def _shift(points: list[tuple[int, int]], dx: int, dy: int) -> list[tuple[int, int]]:
    return [(x + dx, y + dy) for x, y in points]


def render(path: Path = OUT) -> Path:
    """Draw the complete schematic (all nodes, roles, purpose, legend)."""
    width, height = 1400, 980
    image = Image.new("RGB", (width, height), NAVY)
    draw = ImageDraw.Draw(image)

    title_font = _font(22, bold=True)
    sub_font = _font(14)
    name_font = _font(15, bold=True)
    role_font = _font(13)
    legend_font = _font(13)
    legend_bold = _font(14, bold=True)
    foot_font = _font(13)

    draw.text((28, 22), "AU INDUSTRIAL NODES (schematic)", fill=GOLD, font=title_font)
    draw.text(
        (28, 52),
        "Pitch graphic for SpaceX / SpaceXAI — existing launch, recovery, and academy stack.",
        fill=CYAN,
        font=sub_font,
    )
    draw.text((28, 72), "Not a Starbase site map. All eight nodes. Cropped five-dot exports are incomplete.", fill=MUTED, font=sub_font)

    land_shift = _shift(OUTLINE, 40, 70)
    draw.polygon(land_shift, fill=LAND, outline=CYAN)

    for site in SITES:
        x, y = site["xy"]
        x += 40
        y += 70
        r = 8
        draw.ellipse((x - r, y - r, x + r, y + r), fill=site["color"])
        name = site["name"]
        role = site["role"]
        name_w = draw.textlength(name, font=name_font)
        role_w = draw.textlength(role, font=role_font)
        block_w = max(name_w, role_w)
        if site["label"] == "left":
            tx, ty = x - 16 - block_w, y - 16
        elif site["label"] == "below":
            tx, ty = x - (block_w / 2), y + 12
        elif site["label"] == "above":
            tx, ty = x - (block_w / 2), y - 40
        else:
            tx, ty = x + 16, y - 16
        draw.text((tx, ty), name, fill=LIGHT, font=name_font)
        draw.text((tx, ty + 20), role, fill=MUTED, font=role_font)

    # Legend / purpose panel — this is the cropped content the screenshot lost.
    box = (24, 740, width - 24, height - 24)
    draw.rounded_rectangle(box, radius=10, fill=PANEL, outline=CYAN)
    lx, ly = 40, 756
    draw.text((lx, ly), "WHAT THIS IS FOR", fill=GOLD, font=legend_bold)
    draw.text(
        (lx, ly + 24),
        "Show a reviewer, in one glance, that Australia already has a distributed industrial stack to plug into — not a blank-slate spaceport.",
        fill=LIGHT,
        font=legend_font,
    )

    swatches = [
        (GOLD, "Gold — live industrial", "Bowen pad · Southern Launch · W. Sydney Academy + Westmead"),
        (PEACH, "Peach — adjacency / diligence", "Christmas Island recovery · North = no MoU"),
        (CYAN, "Cyan — institutional hubs", "Adelaide Neumann/Fleet · Melbourne Titomic/Lab22 · Canberra ASA/ADFA/EOS"),
    ]
    sx = 40
    sy = 820
    for color, title, detail in swatches:
        draw.ellipse((sx, sy + 4, sx + 14, sy + 18), fill=color)
        draw.text((sx + 22, sy), title, fill=LIGHT, font=legend_bold)
        draw.text((sx + 22, sy + 20), detail, fill=MUTED, font=legend_font)
        sx += 450

    draw.text(
        (40, 890),
        "Not to scale  ·  ELA / Arnhem not live  ·  North = diligence only  ·  No Starship MoU  ·  SpIRIT is UniMelb / Inovor / Neumann, not Gilmour",
        fill=MUTED,
        font=foot_font,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    written = render()
    print("Wrote", written)

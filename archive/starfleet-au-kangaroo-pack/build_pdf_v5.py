#!/usr/bin/env python3
"""Kangaroo-class pitch v5 — legible, concise 3-pager."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageEnhance, ImageDraw

out = "/workspace/starfleet-au-pack/Starfleet-Australia-Kangaroo-Class-Pitch.pdf"
img_path = "/workspace/starfleet-au-pack/assets/kangaroo-class-ncc-992-au.jpeg"
preview = "/workspace/starfleet-au-pack/assets/kangaroo-preview-hq.jpg"
map_path = "/workspace/starfleet-au-pack/assets/au-sites-map.png"

im = PILImage.open(img_path).convert("RGB")
im = ImageEnhance.Contrast(im).enhance(1.18)
im = ImageEnhance.Sharpness(im).enhance(1.3)
w, h = im.size
im = im.crop((int(w * 0.02), int(h * 0.02), int(w * 0.98), int(h * 0.70)))
im.thumbnail((2200, 1100), PILImage.Resampling.LANCZOS)
im.save(preview, "JPEG", quality=92, optimize=True)

mw, mh = 880, 680
mp = PILImage.new("RGB", (mw, mh), (7, 14, 26))
d = ImageDraw.Draw(mp)
outline = [
    (520, 40), (580, 70), (640, 120), (700, 200), (740, 280), (760, 360), (750, 450),
    (720, 520), (680, 560), (620, 590), (540, 610), (460, 600), (400, 560), (360, 500),
    (340, 420), (320, 340), (300, 280), (280, 220), (300, 160), (340, 100), (400, 60),
    (460, 40), (520, 40),
]
d.polygon(outline, fill=(18, 36, 58), outline=(61, 190, 182), width=2)
sites = [
    ("Bowen / Gilmour", 620, 280, (212, 175, 55)),
    ("Christmas Is.", 210, 210, (232, 168, 124)),
    ("North (diligence)", 480, 130, (232, 168, 124)),
    ("Koonibba / Whalers Way", 360, 380, (212, 175, 55)),
    ("Adelaide", 420, 440, (61, 190, 182)),
    ("Melbourne", 520, 510, (61, 190, 182)),
    ("Canberra", 580, 410, (61, 190, 182)),
    ("W. Sydney Academy", 640, 390, (212, 175, 55)),
]
for name, x, y, col in sites:
    d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=col)
    d.text((x + 14, y - 8), name, fill=(240, 244, 250))
d.text((24, 22), "AU INDUSTRIAL NODES (schematic)", fill=(212, 175, 55))
d.text((24, mh - 28), "Not to scale · ELA not live · North = diligence only", fill=(154, 171, 191))
mp.save(map_path)

page_w, page_h = A4
c = canvas.Canvas(out, pagesize=A4)
M = 12 * mm
navy = HexColor("#070e1a")
panel = HexColor("#0d1a2e")
panel2 = HexColor("#122440")
gold = HexColor("#d4af37")
cyan = HexColor("#3dbeb6")
cyan_dim = HexColor("#1a5c58")
light = HexColor("#f0f4fa")
muted = HexColor("#9aabbf")
warn = HexColor("#e8a87c")


def rr(x, y, w, h, r=2.2 * mm, fill=None, stroke=None, sw=0.7):
    if fill:
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
        c.roundRect(x, y, w, h, r, fill=0, stroke=1)


def wrap(text, x, y, max_w, font="Helvetica", size=8, leading=10.5, color=light):
    c.setFillColor(color)
    c.setFont(font, size)
    words = text.split()
    line = ""
    for w in words:
        t = (line + " " + w).strip()
        if c.stringWidth(t, font, size) <= max_w:
            line = t
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def bullets(items, x, y, max_w, size=8, leading=10.5, gap=2.2 * mm, color=light):
    for item in items:
        c.setFillColor(cyan)
        c.setFont("Helvetica-Bold", size)
        c.drawString(x, y, "·")
        y = wrap(item, x + 4 * mm, y, max_w - 4 * mm, size=size, leading=leading, color=color)
        y -= gap
    return y


def chrome(label):
    c.setFillColor(navy)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    c.setFillColor(cyan_dim)
    c.rect(0, 0, 2.5 * mm, page_h, fill=1, stroke=0)
    c.setFillColor(gold)
    c.rect(2.5 * mm, 0, 0.6 * mm, page_h, fill=1, stroke=0)
    rr(M, page_h - 22 * mm, page_w - 2 * M, 14 * mm, fill=panel, stroke=cyan, sw=0.8)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(M + 4 * mm, page_h - 11 * mm, "STARFLEET FOR REAL — AUSTRALIA")
    c.setFillColor(cyan)
    c.setFont("Helvetica", 7.5)
    c.drawString(M + 4 * mm, page_h - 16.5 * mm, "Kangaroo-class NCC-992-AU  ·  SpaceX / SpaceXAI")
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(page_w - M - 4 * mm, page_h - 10 * mm, "CHIEF ENGINEER")
    c.setFillColor(light)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(page_w - M - 4 * mm, page_h - 14.5 * mm, "Crystal Elle Arena-Turner")
    c.setFillColor(muted)
    c.setFont("Helvetica", 6.5)
    c.drawRightString(page_w - M - 4 * mm, page_h - 18.5 * mm, f"TerAustralis · Sydney · 6 Sep 2026 · {label}")


# ========== PAGE 1 ==========
chrome("1 / 3")
y = page_h - 28 * mm

rr(M, y - 48 * mm, page_w - 2 * M, 48 * mm, fill=panel, stroke=gold, sw=0.9)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 4 * mm, y - 5.5 * mm, "FIRST PRINCIPLES")
principles = [
    ("Access", "Cheap, frequent launch — not one heroic flight. Bowen + Southern Launch exist; no Starship MoU yet. Christmas Island already recovered Ship 40 (Jul–Aug 2026)."),
    ("Stay", "Fleets need in-space mobility. Neumann Drive is commercial on SpaceX Transporters; debris→fuel is roadmap, not done."),
    ("Build", "Print metal structures onshore (Titomic / Lab22). Traction is real aerospace/defence — not a Starship hull line."),
    ("Crew", "Academy before Hollywood. Western Sydney + ADFA model; holodeck = sim first."),
]
py = y - 12 * mm
for title, body in principles:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(M + 4 * mm, py, title)
    py = wrap(body, M + 22 * mm, py, page_w - 2 * M - 28 * mm, size=7.5, leading=9.5)
    py -= 1.8 * mm

y = y - 54 * mm
col_w = (page_w - 2 * M - 4 * mm) / 2

# Stack
rr(M, y - 102 * mm, col_w, 102 * mm, fill=panel, stroke=gold)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 3.5 * mm, y - 5.5 * mm, "SYSTEMS STACK")
layers = [
    ("07 Academy", "W. Sydney + ADFA · sim → flight corridor", cyan),
    ("06 Medicine", "AU medtech / sensing adjacency — not kits", cyan),
    ("05 Sensors", "Fleet constellation · EOS SSA (Atlas = early)", gold),
    ("04 Propulsion", "Neumann commercial EP · Gilmour access · Hypersonix flown", gold),
    ("03 Manufacture", "Titomic cold-spray · Lab22 AM — pilots", gold),
    ("02 Launch / return", "Bowen orbital · Koonibba re-entry · Whalers Way", warn),
    ("01 Foundation", "TSA 23 Jul 2024 · ITAR · Statement on Space Jul 2026", muted),
]
ly = y - 12 * mm
box_h = 11.5 * mm
for title, body, acc in layers:
    rr(M + 3 * mm, ly - box_h, col_w - 6 * mm, box_h, r=1.5 * mm, fill=panel2, stroke=acc, sw=0.5)
    c.setFillColor(acc)
    c.rect(M + 3 * mm, ly - box_h, 1.2 * mm, box_h, fill=1, stroke=0)
    c.setFillColor(acc)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(M + 6 * mm, ly - 4.5 * mm, title)
    c.setFillColor(light)
    c.setFont("Helvetica", 7)
    c.drawString(M + 6 * mm, ly - 9 * mm, body)
    ly -= box_h + 1.5 * mm

# Right column
rx = M + col_w + 4 * mm
rr(rx, y - 38 * mm, col_w, 38 * mm, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(rx + 3.5 * mm, y - 5.5 * mm, "WHY AUSTRALIA")
bullets(
    [
        "TSA in force — US vehicles can launch from AU soil (still needs licences).",
        "Ship 40 recovery already used AU logistics.",
        "Whalers Way: polar / SSO. Bowen: mid-inclination.",
        "Allied second-hemisphere option — not a Starbase clone (no methalox industrial base yet).",
    ],
    rx + 3.5 * mm,
    y - 12 * mm,
    col_w - 7 * mm,
    size=7.5,
    leading=9.5,
    gap=1.5 * mm,
)

rr(rx, y - 38 * mm - 4 * mm - 36 * mm, col_w, 36 * mm, fill=panel, stroke=gold)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(rx + 3.5 * mm, y - 38 * mm - 4 * mm - 5.5 * mm, "BUILD PHASES")
phases = [
    "P1 · 12 mo — Structure demo + range diligence",
    "P2 · 24 mo — Academy charter (~100 cadets)",
    "P3 · 5 yr — Print → launch → assemble demo",
]
py = y - 38 * mm - 4 * mm - 13 * mm
for p in phases:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(rx + 3.5 * mm, py, "·")
    c.setFillColor(light)
    c.setFont("Helvetica", 8)
    c.drawString(rx + 7.5 * mm, py, p)
    py -= 7 * mm

rr(rx, y - 102 * mm, col_w, 102 * mm - (38 + 4 + 36 + 4) * mm, fill=panel, stroke=warn)
c.setFillColor(warn)
c.setFont("Helvetica-Bold", 9)
bh = y - 38 * mm - 4 * mm - 36 * mm - 4 * mm
c.drawString(rx + 3.5 * mm, bh - 5.5 * mm, "HARD NO'S")
bullets(
    [
        "No Starship MoU. No warp.",
        "ELA / Arnhem not live.",
        "SpIRIT is not Gilmour.",
        "Eris not orbital yet (TF2 ~early 2027*).",
        "Concept art ≠ hardware.",
    ],
    rx + 3.5 * mm,
    bh - 12 * mm,
    col_w - 7 * mm,
    size=7.5,
    leading=9.5,
    gap=1.2 * mm,
    color=light,
)

# Footer partners
rr(M, 8 * mm, page_w - 2 * M, 20 * mm, fill=HexColor("#101f35"), stroke=gold, sw=0.8)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 8)
c.drawString(M + 4 * mm, 22 * mm, "PARTNERS (FACT-CHECKED)")
wrap(
    "Gilmour (Bowen · Series E A$217m · ElaraSat rideshare) · Southern Launch (Koonibba re-entry · A$25m) · Neumann (Transporter cadence) · Titomic + Lab22 · Fleet · EOS · Hypersonix · UNSW / ADFA",
    M + 4 * mm,
    15 * mm,
    page_w - 2 * M - 8 * mm,
    size=7.5,
    leading=9.5,
)

c.showPage()

# ========== PAGE 2 ==========
chrome("2 / 3")
y = page_h - 28 * mm

rr(M, y - 32 * mm, page_w - 2 * M, 32 * mm, fill=panel, stroke=gold, sw=0.9)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 4 * mm, y - 5.5 * mm, "SECTOR SNAPSHOT")
three = [
    ("Scale", "A$4.6bn turnover · ~17k people · ~620 orgs\n(ASA fact sheet, Jul 2025)"),
    ("Policy", "Statement on Space — Jul 2026\nFlight · platforms · microgravity · SSA"),
    ("Capital", "NRFC space-related ≈ A$198m+\nGilmour A$75m · Fleet Series D A$150m"),
]
tw = (page_w - 2 * M - 10 * mm) / 3
for i, (t, b) in enumerate(three):
    x = M + 4 * mm + i * (tw + 3 * mm)
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x, y - 13 * mm, t)
    for j, line in enumerate(b.split("\n")):
        c.setFillColor(light)
        c.setFont("Helvetica", 7.5)
        c.drawString(x, y - 20 * mm - j * 8 * mm, line)

y = y - 38 * mm

rr(M, y - 78 * mm, page_w - 2 * M, 78 * mm, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 4 * mm, y - 5.5 * mm, "WHO'S LIVE (SEP 2026)")
rows = [
    ("Gilmour", "Licensed Bowen pad. Eris TF1 Jul 2025 failed (~T+9–17s). TF2 ~early 2027*. Series E A$217m. SpaceX = rideshare only."),
    ("Southern Launch", "Koonibba: commercial re-entry (from Feb 2025). Whalers Way orbital. A$25m Series A (A$10m NRF)."),
    ("Neumann", "ND-25 on Transporter-16/17. ND-50 on CarbSAR. Debris-fuel with CisLunar = roadmap."),
    ("Titomic", "NASA SAA · US defence contracts · CRADA. Mostly US sustainment — not hull factory."),
    ("Hypersonix / Fleet / EOS", "DART AE Mach 5+ (Feb 2026). Fleet Series D >A$800m. EOS Atlas HEL = early market, not sales."),
]
ry = y - 14 * mm
for name, body in rows:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(M + 4 * mm, ry, name)
    ry = wrap(body, M + 38 * mm, ry, page_w - 2 * M - 44 * mm, size=7.5, leading=9.5)
    ry -= 3 * mm

y = y - 84 * mm
half = (page_w - 2 * M - 4 * mm) / 2

rr(M, y - 52 * mm, half, 52 * mm, fill=panel, stroke=warn)
c.setFillColor(warn)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 3.5 * mm, y - 5.5 * mm, "BLOCKERS")
bullets(
    [
        "ITAR still applies — TSA ≠ tech transfer free pass.",
        "Every launch needs AU permits.",
        "No Starship-grade methalox chain yet.",
        "Thin specialist workforce.",
        "North range sites = diligence only.",
    ],
    M + 3.5 * mm,
    y - 13 * mm,
    half - 7 * mm,
    size=7.5,
    leading=9.8,
    gap=1.8 * mm,
)

rr(M + half + 4 * mm, y - 52 * mm, half, 52 * mm, fill=panel, stroke=gold)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + half + 7.5 * mm, y - 5.5 * mm, "POLICY FIT")
bullets(
    [
        "Spaceflight → Bowen + Southern Launch + TSA",
        "Platforms → Titomic / Lab22",
        "Trusted services → Fleet + EOS SSA",
        "Microgravity → Koonibba re-entry",
        "Defence space signal A$9–12bn / decade — not a bid",
    ],
    M + half + 7.5 * mm,
    y - 13 * mm,
    half - 7 * mm,
    size=7.5,
    leading=9.8,
    gap=1.8 * mm,
)

rr(M, 8 * mm, page_w - 2 * M, 22 * mm, fill=HexColor("#101f35"), stroke=cyan, sw=0.7)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 8)
c.drawString(M + 4 * mm, 24 * mm, "BEFORE THE ASK HARDENS")
wrap(
    "TSA pathway · northern site shortlist · Gilmour TF2 in writing · Southern Launch readiness · Titomic P1 SOW · Academy MoU skeleton · red-team: what if Eris slips another year?",
    M + 4 * mm,
    16 * mm,
    page_w - 2 * M - 8 * mm,
    size=7.5,
    leading=9.5,
)

c.showPage()

# ========== PAGE 3 ==========
chrome("3 / 3")
y = page_h - 28 * mm

map_h = 78 * mm
rr(M, y - map_h, 95 * mm, map_h, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 3.5 * mm, y - 5.5 * mm, "GEOGRAPHY")
c.drawImage(
    ImageReader(map_path),
    M + 3 * mm,
    y - map_h + 3 * mm,
    width=89 * mm,
    height=map_h - 11 * mm,
    preserveAspectRatio=True,
    mask="auto",
)

rr(M + 99 * mm, y - map_h, page_w - 2 * M - 99 * mm, map_h, fill=panel, stroke=gold)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 103 * mm, y - 5.5 * mm, "ACADEMY")
bullets(
    [
        "Y1 — Shipbuilding · propulsion · astrogation",
        "Y2 — UE5 / MR holodeck sims",
        "Y3 — Cislunar tug capstone + live range",
        "Spine — ADFA leadership model",
        "Sites — W. Sydney + Qld / SA corridors",
    ],
    M + 103 * mm,
    y - 14 * mm,
    page_w - M - 108 * mm,
    size=8,
    leading=10.5,
    gap=2 * mm,
)

y = y - map_h - 5 * mm

ship_h = 58 * mm
rr(M, y - ship_h, page_w - 2 * M, ship_h, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 3.5 * mm, y - 5 * mm, "KANGAROO-CLASS — NARRATIVE MAP (FICTION COVER)")
ir = ImageReader(preview)
iw, ih = ir.getSize()
avail_w, avail_h = 105 * mm, ship_h - 12 * mm
sc = min(avail_w / iw, avail_h / ih)
dw, dh = iw * sc, ih * sc
c.drawImage(ir, M + 3 * mm, y - ship_h + 3 * mm, width=dw, height=dh, mask="auto")
cx = M + 3 * mm + dw + 4 * mm
maps = [
    "Hull → Titomic / Lab22",
    "Impulse → Neumann (+ Gilmour)",
    "Sensors → Fleet + EOS",
    "Shipyard → Bowen + Southern Launch",
    "Academy → W. Sydney + ADFA",
    "Recovery → Koonibba / Christmas Is.",
]
cy = y - 14 * mm
for line in maps:
    c.setFillColor(cyan)
    c.setFont("Helvetica", 8)
    c.drawString(cx, cy, "→  " + line)
    cy -= 6.5 * mm
c.setFillColor(muted)
c.setFont("Helvetica-Oblique", 6.5)
c.drawString(M + 3 * mm, y - ship_h + 1.5 * mm, "LCARS art — fiction. Not certification.")

y = y - ship_h - 5 * mm
third = (page_w - 2 * M - 6 * mm) / 3
panels = [
    ("SICKBAY ADJACENCY", cyan, "Cochlear / ResMed lineage · bionic-eye research · quantum sensing. Human-systems depth — not flying devices."),
    ("MADE IN AUSTRALIA", gold, "Materials → print → launch → recover. Qld + SA corridors. North = diligence only. No dead spaceports claimed live."),
    ("STILL NEED", warn, "SpaceX BD channel · site shortlist · LOIs for P1 · Academy MoU · diligence binder (TSA, NRF, licences)."),
]
for i, (title, stroke, body) in enumerate(panels):
    x = M + i * (third + 3 * mm)
    rr(x, y - 34 * mm, third, 34 * mm, fill=panel, stroke=stroke)
    c.setFillColor(stroke if stroke != warn else warn)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x + 3 * mm, y - 5.5 * mm, title)
    wrap(body, x + 3 * mm, y - 12 * mm, third - 6 * mm, size=7.5, leading=9.5)

rr(M, 7 * mm, page_w - 2 * M, 20 * mm, fill=HexColor("#101f35"), stroke=gold, sw=1)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 9)
c.drawString(M + 4 * mm, 20.5 * mm, "ASK")
c.setFillColor(light)
c.setFont("Helvetica", 8)
c.drawString(M + 4 * mm, 14 * mm, "30-min exploratory — SpaceX launch / manufacturing / recovery BD (+ SpaceXAI if Grok co-travels).")
c.setFillColor(muted)
c.setFont("Helvetica", 6.5)
c.drawString(M + 4 * mm, 9 * mm, "Crystal Elle Arena-Turner · Chief Engineer · teraustralis.incognita@gmail.com · +61 450 144 997 · TerAustralis.com.au")
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7.5)
c.drawRightString(page_w - M - 4 * mm, 14 * mm, "access · stay · build · crew")

c.save()
print("Wrote", out)

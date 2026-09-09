from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageEnhance
import os

out = "/workspace/starfleet-au-pack/Starfleet-Australia-Kangaroo-Class-Pitch.pdf"
img_path = "/workspace/starfleet-au-pack/assets/kangaroo-class-ncc-992-au.jpeg"
preview = "/workspace/starfleet-au-pack/assets/kangaroo-preview-hq.jpg"

im = PILImage.open(img_path).convert("RGB")
im = ImageEnhance.Contrast(im).enhance(1.15)
im = ImageEnhance.Sharpness(im).enhance(1.25)
im = ImageEnhance.Color(im).enhance(1.05)
w, h = im.size
im = im.crop((int(w*0.02), int(h*0.02), int(w*0.98), int(h*0.72)))
im.thumbnail((2200, 1100), PILImage.Resampling.LANCZOS)
im.save(preview, "JPEG", quality=92, optimize=True)

page_w, page_h = A4
c = canvas.Canvas(out, pagesize=A4)
M = 11 * mm
navy = HexColor("#070e1a")
panel = HexColor("#0d1a2e")
panel2 = HexColor("#122440")
gold = HexColor("#d4af37")
gold_dim = HexColor("#8a7020")
cyan = HexColor("#3dbeb6")
cyan_dim = HexColor("#1a5c58")
light = HexColor("#f0f4fa")
muted = HexColor("#9aabbf")
warn = HexColor("#e8a87c")

def rounded_rect(x, y, w, h, r=2*mm, fill=None, stroke=None, sw=0.6):
    if fill:
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
        c.roundRect(x, y, w, h, r, fill=0, stroke=1)

def wrap_draw(text, x, y, max_w, font="Helvetica", size=6.5, leading=8, color=light):
    c.setFillColor(color)
    c.setFont(font, size)
    words = text.split()
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y

c.setFillColor(navy)
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
c.setFillColor(cyan_dim)
c.rect(0, 0, 2.2*mm, page_h, fill=1, stroke=0)
c.setFillColor(gold)
c.rect(2.2*mm, 0, 0.6*mm, page_h, fill=1, stroke=0)

rounded_rect(M, page_h - 28*mm, page_w - 2*M, 20*mm, r=2.5*mm, fill=panel, stroke=cyan, sw=0.7)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 13)
c.drawString(M + 4*mm, page_h - 14*mm, "STARFLEET FOR REAL — AUSTRALIA")
c.setFillColor(cyan)
c.setFont("Helvetica", 7.5)
c.drawString(M + 4*mm, page_h - 19*mm, "Kangaroo-class Explorer  ·  NCC-992-AU  ·  Systems architecture pitch for SpaceX / SpaceXAI")
c.setFillColor(light)
c.setFont("Helvetica-Bold", 8)
c.drawRightString(page_w - M - 4*mm, page_h - 13*mm, "CHIEF ENGINEER")
c.setFont("Helvetica-Bold", 9)
c.setFillColor(gold)
c.drawRightString(page_w - M - 4*mm, page_h - 17.5*mm, "Crystal Elle Arena-Turner")
c.setFillColor(muted)
c.setFont("Helvetica", 6)
c.drawRightString(page_w - M - 4*mm, page_h - 21.5*mm, "TerAustralis Incognita · Sydney · 6 Sep 2026")

col_gap = 4*mm
left_w = 92*mm
right_w = page_w - 2*M - left_w - col_gap
left_x = M
right_x = M + left_w + col_gap
top_y = page_h - 33*mm

arch_h = 118*mm
rounded_rect(left_x, top_y - arch_h, left_w, arch_h, fill=panel, stroke=gold_dim, sw=0.6)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 8)
c.drawString(left_x + 3*mm, top_y - 5*mm, "SYSTEMS ARCHITECTURE")
c.setStrokeColor(cyan)
c.setLineWidth(0.5)
c.line(left_x + 3*mm, top_y - 6.5*mm, left_x + left_w - 3*mm, top_y - 6.5*mm)

layers = [
    ("06  ACADEMY / CREW", "Western Sydney Aerotropolis + ADFA model + UNSW Canberra Space / RMIT / CSIRO. Holodeck v1 = UE5 + MR sims before flight.", cyan),
    ("05  SENSORS / SSA", "Fleet Space constellation (commercial subsurface mapping). EOS laser SSA (proven). Plasma/magnetic shielding = research, not product.", cyan),
    ("04  PROPULSION / IMPULSE", "Neumann Drive — Mo solid-metal EP, fired in space (SpIRIT path). Debris-refuel = concept. Gilmour hybrids for access. Hypersonix SPARTAN = 2026 Mach5+ demo.", gold),
    ("03  MANUFACTURE / HULL", "Titomic Kinetic Fusion (CSIRO-origin) + Lab22 — large titanium AM. Boeing green-Ti tests / Gilmour R&D intent = pilots, not Starship production line.", gold),
    ("02  LAUNCH / RANGE", "Gilmour Bowen (licensed orbital site; Eris in test; ElaraSat on SpaceX). Northern AU Starship geography = diligence only. ELA/Arnhem NOT a live hook (liquidation 2026).", warn),
    ("01  FOUNDATION", "Critical minerals (Li, REE, Ti) on-continent · TSA/ITAR · power/water/social licence · Commonwealth/NSW AI+DC policy stack (parallel Grok/SpaceXAI compute track).", muted),
]

box_h = 16.5*mm
y0 = top_y - 10*mm
for i, (title, body, accent) in enumerate(layers):
    by = y0 - (i+1)*box_h - i*1.2*mm
    rounded_rect(left_x + 2.5*mm, by, left_w - 5*mm, box_h, r=1.5*mm, fill=panel2, stroke=accent, sw=0.55)
    c.setFillColor(accent)
    c.rect(left_x + 2.5*mm, by, 1.2*mm, box_h, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(left_x + 5.5*mm, by + box_h - 4*mm, title)
    wrap_draw(body, left_x + 5.5*mm, by + box_h - 7.5*mm, left_w - 10*mm, size=5.5, leading=6.5, color=light)

c.setFillColor(muted)
c.setFont("Helvetica-Oblique", 5)
c.drawCentredString(left_x + left_w/2, top_y - arch_h + 2.5*mm, "Stack reads bottom→top: geology → pad → print → thrust → sense → crew")

ry = top_y
rh = 42*mm
rounded_rect(right_x, ry - rh, right_w, rh, fill=panel, stroke=cyan, sw=0.55)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 8)
c.drawString(right_x + 3*mm, ry - 5*mm, "THESIS")
wrap_draw(
    "Not cosplay — a shipyard that builds the future and an Academy that crews it. "
    "Australia: materials + metal AM + flight-proven EP + licensed Qld range + defence-grade education. "
    "Kangaroo-class art = narrative cover for the industrial stack.",
    right_x + 3*mm, ry - 10*mm, right_w - 6*mm, size=6.5, leading=8)

by = ry - rh - 3*mm
bh = 38*mm
rounded_rect(right_x, by - bh, right_w, bh, fill=panel, stroke=gold_dim, sw=0.55)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 8)
c.drawString(right_x + 3*mm, by - 5*mm, "BUILD ARCHITECTURE (3 PHASES)")
phases = [
    ("P1 · 12 mo · PROVE", "Titomic-class structure demo; Bowen corridor propulsion narrative; northern-AU range diligence (no dead brands)."),
    ("P2 · 24 mo · CREW", "Academy charter outline: SpaceX + ASA + UNSW. First ~100 cadets. Capstone = cislunar tug concepts."),
    ("P3 · 5 yr · ORBIT", "Ground-print hab segment → launch → on-orbit assembly demo from an Australian range."),
]
py = by - 10*mm
for t, b in phases:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(right_x + 3*mm, py, t)
    py = wrap_draw(b, right_x + 3*mm, py - 3.2*mm, right_w - 6*mm, size=5.8, leading=7, color=light)
    py -= 1.8*mm

by2 = by - bh - 3*mm
bh2 = 28*mm
rounded_rect(right_x, by2 - bh2, right_w, bh2, fill=panel, stroke=warn, sw=0.55)
c.setFillColor(warn)
c.setFont("Helvetica-Bold", 7.5)
c.drawString(right_x + 3*mm, by2 - 5*mm, "HARD BOUNDARIES (DO NOT OVERCLAIM)")
wrap_draw(
    "• No SpaceX Starship MoU (only public \"possibly\").  • ELA/Arnhem not operational (liquidation 2026).  "
    "• SpIRIT != Gilmour — credit UniMelb/Inovor/Neumann.  • Neumann debris-refuel = concept.  "
    "• EOS debris \"shields\" aspirational.  • Parallel: SpaceXAI/Grok NSW compute + Westmead clinical adjacency.",
    right_x + 3*mm, by2 - 10*mm, right_w - 6*mm, size=5.8, leading=7, color=light)

img_top = by2 - bh2 - 4*mm
img_h = 42*mm
rounded_rect(M, img_top - img_h, page_w - 2*M, img_h, fill=panel, stroke=cyan_dim, sw=0.5)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7)
c.drawString(M + 3*mm, img_top - 4*mm, "CONCEPT SCHEMATIC — KANGAROO-CLASS NCC-992-AU")
ir = ImageReader(preview)
iw, ih = ir.getSize()
avail_w = page_w - 2*M - 6*mm
avail_h = img_h - 8*mm
scale = min(avail_w / float(iw), avail_h / float(ih))
dw, dh = iw * scale, ih * scale
c.drawImage(ir, M + 3*mm, img_top - img_h + 3*mm, width=dw, height=dh, mask='auto')
c.setFillColor(muted)
c.setFont("Helvetica-Oblique", 5)
c.drawString(M + 3*mm, img_top - img_h + 1.2*mm, "Concept art only — LCARS fiction. Not flight hardware.")

foot_y = 7*mm
foot_h = 18*mm
rounded_rect(M, foot_y, page_w - 2*M, foot_h, fill=HexColor("#101f35"), stroke=gold, sw=0.8)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7)
c.drawString(M + 3.5*mm, foot_y + 12.5*mm, "ASK")
c.setFillColor(light)
c.setFont("Helvetica", 6.5)
c.drawString(M + 3.5*mm, foot_y + 8*mm, "30-min exploratory: SpaceX launch-site / manufacturing BD (+ SpaceXAI if compute co-travels).")
c.setFillColor(muted)
c.setFont("Helvetica", 6)
c.drawString(M + 3.5*mm, foot_y + 3.5*mm, "teraustralis.incognita@gmail.com  ·  +61 450 144 997  ·  TerAustralis.com.au  ·  ABN 70 741 068 059")
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6)
c.drawRightString(page_w - M - 3.5*mm, foot_y + 8*mm, "Chief Engineer")
c.setFillColor(light)
c.setFont("Helvetica-Bold", 8)
c.drawRightString(page_w - M - 3.5*mm, foot_y + 3.5*mm, "Crystal Elle Arena-Turner")

c.save()
print("OK", out, os.path.getsize(out))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageEnhance, ImageDraw
import math

out = "/workspace/starfleet-au-pack/Starfleet-Australia-Kangaroo-Class-Pitch.pdf"
img_path = "/workspace/starfleet-au-pack/assets/kangaroo-class-ncc-992-au.jpeg"
preview = "/workspace/starfleet-au-pack/assets/kangaroo-preview-hq.jpg"
map_path = "/workspace/starfleet-au-pack/assets/au-sites-map.png"

# Blueprint enhance
im = PILImage.open(img_path).convert("RGB")
im = ImageEnhance.Contrast(im).enhance(1.18)
im = ImageEnhance.Sharpness(im).enhance(1.3)
w, h = im.size
im = im.crop((int(w*0.02), int(h*0.02), int(w*0.98), int(h*0.70)))
im.thumbnail((2400, 1200), PILImage.Resampling.LANCZOS)
im.save(preview, "JPEG", quality=93, optimize=True)

# Simple Australia site map
mw, mh = 900, 700
mp = PILImage.new("RGB", (mw, mh), (7, 14, 26))
d = ImageDraw.Draw(mp)
# crude AU outline as polygon (simplified)
# Coordinates roughly normalised for a silhouette
outline = [
    (520,40),(580,70),(640,120),(700,200),(740,280),(760,360),(750,450),(720,520),
    (680,560),(620,590),(540,610),(460,600),(400,560),(360,500),(340,420),(320,340),
    (300,280),(280,220),(300,160),(340,100),(400,60),(460,40),(520,40)
]
# scale outline into frame
d.polygon(outline, fill=(18,36,58), outline=(61,190,182))
# sites
sites = [
    ("Bowen / Gilmour", 620, 280, (212,175,55)),
    ("Northern ranges\n(diligence)", 480, 120, (232,168,124)),
    ("Adelaide\nNeumann / Fleet", 420, 420, (61,190,182)),
    ("Melbourne\nTitomic / Lab22", 520, 500, (61,190,182)),
    ("Canberra\nEOS / ADFA", 580, 400, (61,190,182)),
    ("Western Sydney\nAcademy + Westmead", 640, 380, (212,175,55)),
]
for name, x, y, col in sites:
    d.ellipse((x-7,y-7,x+7,y+7), fill=col)
    d.text((x+12, y-10), name, fill=(240,244,250))
d.text((20,20), "AUSTRALIA — INDUSTRIAL NODES (schematic)", fill=(212,175,55))
d.text((20,mh-30), "Not to scale · Northern Starship sites = diligence only · ELA not live", fill=(154,171,191))
mp.save(map_path)

page_w, page_h = A4
c = canvas.Canvas(out, pagesize=A4)
M = 10 * mm
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

def rr(x,y,w,h,r=2*mm,fill=None,stroke=None,sw=0.55):
    if fill:
        c.setFillColor(fill); c.roundRect(x,y,w,h,r,fill=1,stroke=0)
    if stroke:
        c.setStrokeColor(stroke); c.setLineWidth(sw); c.roundRect(x,y,w,h,r,fill=0,stroke=1)

def wrap(text,x,y,max_w,font="Helvetica",size=6.5,leading=8,color=light):
    c.setFillColor(color); c.setFont(font,size)
    words=text.split(); line=""
    for w in words:
        t=(line+" "+w).strip()
        if c.stringWidth(t,font,size)<=max_w:
            line=t
        else:
            c.drawString(x,y,line); y-=leading; line=w
    if line:
        c.drawString(x,y,line); y-=leading
    return y

def page_chrome(page_label):
    c.setFillColor(navy); c.rect(0,0,page_w,page_h,fill=1,stroke=0)
    c.setFillColor(cyan_dim); c.rect(0,0,2*mm,page_h,fill=1,stroke=0)
    c.setFillColor(gold); c.rect(2*mm,0,0.55*mm,page_h,fill=1,stroke=0)
    rr(M, page_h-24*mm, page_w-2*M, 16*mm, fill=panel, stroke=cyan, sw=0.7)
    c.setFillColor(gold); c.setFont("Helvetica-Bold", 12)
    c.drawString(M+3.5*mm, page_h-12*mm, "STARFLEET FOR REAL — AUSTRALIA")
    c.setFillColor(cyan); c.setFont("Helvetica", 7)
    c.drawString(M+3.5*mm, page_h-17*mm, "Kangaroo-class NCC-992-AU  ·  First principles + systems architecture  ·  SpaceX / SpaceXAI")
    c.setFillColor(gold); c.setFont("Helvetica-Bold", 7.5)
    c.drawRightString(page_w-M-3.5*mm, page_h-11*mm, "CHIEF ENGINEER")
    c.setFillColor(light); c.setFont("Helvetica-Bold", 8.5)
    c.drawRightString(page_w-M-3.5*mm, page_h-15.5*mm, "Crystal Elle Arena-Turner")
    c.setFillColor(muted); c.setFont("Helvetica", 5.5)
    c.drawRightString(page_w-M-3.5*mm, page_h-19.5*mm, f"TerAustralis · Sydney · 6 Sep 2026 · {page_label}")

# ===================== PAGE 1 =====================
page_chrome("Page 1 / 2 — Problem & Stack")
y = page_h - 30*mm

# FIRST PRINCIPLES
rr(M, y-46*mm, page_w-2*M, 46*mm, fill=panel, stroke=gold, sw=0.8)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 8)
c.drawString(M+3.5*mm, y-5*mm, "FIRST PRINCIPLES — THE PROBLEM WE ARE SOLVING")
probs = [
    ("1. Access", "Interplanetary civilisation needs cheap, frequent access to space — not one heroic launch. Australia has ocean ranges, northern geography, and builders (Gilmour Bowen) but no SpaceX Starship MoU yet."),
    ("2. Stay", "Fleets die without in-space mobility and logistics. Neumann-class solid-metal EP is flight-proven (Mo propellant on SpIRIT path); debris-refuel is the open roadmap, not a claim of done."),
    ("3. Build", "You cannot supply a fleet from Earth forever. Large metal AM (Titomic/CSIRO Lab22) is the industrial replicator — mine Ti here, print structures, launch from AU ranges."),
    ("4. Crew", "Hardware without people is scrap. ADFA-grade Academy (Western Sydney + Qld flight corridor) trains builders/operators before Hollywood sets. Holodeck = UE5/MR sims first."),
]
py = y - 10*mm
for t,b in probs:
    c.setFillColor(cyan); c.setFont("Helvetica-Bold", 6.5)
    c.drawString(M+3.5*mm, py, t)
    py = wrap(b, M+18*mm, py, page_w-2*M-22*mm, size=6, leading=7.2)
    py -= 1.2*mm

y = y - 50*mm
# Two columns: stack + thesis/partners
lw = 95*mm; rw = page_w-2*M-lw-3.5*mm
lx = M; rx = M+lw+3.5*mm

# Systems stack compact
sh = 105*mm
rr(lx, y-sh, lw, sh, fill=panel, stroke=gold_dim)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7.5)
c.drawString(lx+3*mm, y-5*mm, "SYSTEMS ARCHITECTURE (BOTTOM → TOP)")
layers = [
    ("07 ACADEMY / HOLODECK", "Western Sydney Aerotropolis + ADFA leadership model. Y1 shipbuilding/propulsion/astrogation; Y2 UE5 holodeck; Y3 cislunar tug capstone at Bowen corridor.", cyan),
    ("06 MEDICINE / TRICORDER", "AU medtech adjacency: Cochlear, ResMed lineage, bionic-eye research; UNSW quantum sensing / gravimetry heritage for exploration instruments — adjacency, not productised Starfleet kit.", cyan),
    ("05 SENSORS / SSA / COMMS", "Fleet Space (Adelaide) commercial subsurface mapping constellation. EOS laser SSA proven; optical comms in product set; active debris control aspirational.", gold),
    ("04 PROPULSION", "Neumann Drive Mo EP (in-space demonstrated). Gilmour hybrids for access. Hypersonix SPARTAN Mach5+ demo (2026). ANSTO nuclear-thermal = research only.", gold),
    ("03 MANUFACTURE", "Titomic Kinetic Fusion (CSIRO-origin) + Lab22/Amaero metal AM. Boeing green-Ti tests; Gilmour R&D intent — pilots, not Starship hull line.", gold),
    ("02 LAUNCH / RANGE", "Gilmour Bowen licensed orbital site; Eris in development; ElaraSat on SpaceX. Northern AU Starship geography = diligence. ELA/Arnhem NOT live (liquidation 2026).", warn),
    ("01 FOUNDATION", "Li / REE / Ti on-continent · TSA/ITAR · power/water · social licence · AU space policy.", muted),
]
box_h=12.2*mm; y0=y-8*mm
for i,(t,b,acc) in enumerate(layers):
    by=y0-(i+1)*box_h-i*0.8*mm
    rr(lx+2*mm, by, lw-4*mm, box_h, r=1.2*mm, fill=panel2, stroke=acc, sw=0.45)
    c.setFillColor(acc); c.rect(lx+2*mm, by, 1.1*mm, box_h, fill=1, stroke=0)
    c.setFillColor(acc); c.setFont("Helvetica-Bold", 5.5)
    c.drawString(lx+4.5*mm, by+box_h-3.5*mm, t)
    wrap(b, lx+4.5*mm, by+box_h-6.5*mm, lw-9*mm, size=5, leading=5.8)

# Right: compute stack + partners + phases
rr(rx, y-36*mm, rw, 36*mm, fill=panel, stroke=cyan)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(rx+2.5*mm, y-4.5*mm, "PARALLEL STACK — SPACE XAI / GROK COMPUTE")
wrap("Same civilisation problem, digital layer: sovereign/APAC Grok deploy + NSW AI DC under Data Centre Framework; Westmead Health Precinct as clinical demand (digital health/neuro imaging — not claiming motor-BCI trials). Separate one-pager in sydney-xai-pack/. Humain-style national packaging via DISR/Austrade/Investment NSW.",
     rx+2.5*mm, y-9*mm, rw-5*mm, size=5.8, leading=7)

rr(rx, y-36*mm-3*mm-42*mm, rw, 42*mm, fill=panel, stroke=gold_dim)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(rx+2.5*mm, y-36*mm-3*mm-4.5*mm, "BUILD PHASES")
ph=[
 ("P1 · 12 mo · PROVE","Titomic-class structure demo; Bowen propulsion narrative; northern-AU range diligence (no dead brands)."),
 ("P2 · 24 mo · CREW","Academy charter: SpaceX + ASA + UNSW. ~100 cadets. Capstone = cislunar tug concepts."),
 ("P3 · 5 yr · ORBIT","Print hab segment on ground → launch → on-orbit assembly demo from AU range."),
]
py=y-36*mm-3*mm-10*mm
for t,b in ph:
    c.setFillColor(cyan); c.setFont("Helvetica-Bold", 5.8); c.drawString(rx+2.5*mm, py, t)
    py=wrap(b, rx+2.5*mm, py-3*mm, rw-5*mm, size=5.5, leading=6.5); py-=1.5*mm

rr(rx, y-sh, rw, sh-(36*mm+3*mm+42*mm+3*mm), fill=panel, stroke=warn)
c.setFillColor(warn); c.setFont("Helvetica-Bold", 7)
bot = y-sh
c.drawString(rx+2.5*mm, y-36*mm-3*mm-42*mm-3*mm-4.5*mm, "HARD BOUNDARIES")
wrap("No warp. No Starship MoU. ELA not operational. SpIRIT ≠ Gilmour (UniMelb/Inovor/Neumann). Debris-refuel & EOS debris-control = roadmap. Concept art ≠ hardware.",
     rx+2.5*mm, y-36*mm-3*mm-42*mm-3*mm-9*mm, rw-5*mm, size=5.5, leading=6.5)

# Partner strip
ps_y = 8*mm
rr(M, ps_y, page_w-2*M, 22*mm, fill=HexColor("#101f35"), stroke=gold, sw=0.7)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 6.5)
c.drawString(M+3*mm, ps_y+16*mm, "PARTNER / HERITAGE ROSTER (FACT-CHECKED)")
wrap("Gilmour Space (Bowen, Eris, ElaraSat on SpaceX) · Neumann Space (Mo EP in space via SpIRIT path) · Titomic + CSIRO Lab22 (metal AM) · Fleet Space · EOS · Hypersonix (SPARTAN demo) · UNSW / RMIT / ADFA (Academy) · Westmead precinct (compute/clinical parallel). SpIRIT credit: UniMelb / Inovor / Neumann — not Gilmour.",
     M+3*mm, ps_y+11*mm, page_w-2*M-6*mm, size=5.5, leading=6.5)

c.showPage()

# ===================== PAGE 2 =====================
page_chrome("Page 2 / 2 — Sites, Ship, Ask")
y = page_h - 30*mm

# Map + ship side by side
map_h = 78*mm
rr(M, y-map_h, 95*mm, map_h, fill=panel, stroke=cyan)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(M+3*mm, y-5*mm, "INDUSTRIAL GEOGRAPHY")
ir = ImageReader(map_path)
c.drawImage(ir, M+3*mm, y-map_h+3*mm, width=89*mm, height=map_h-10*mm, preserveAspectRatio=True, mask='auto')

rr(M+98*mm, y-map_h, page_w-2*M-98*mm, map_h, fill=panel, stroke=gold_dim)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(M+101*mm, y-5*mm, "ACADEMY ARCHITECTURE")
curr = [
 "Year 1 — Shipbuilding (Titomic/AM literacy), Propulsion (Neumann/Gilmour), Astrogation (UNSW Canberra Space / RMIT).",
 "Year 2 — Holodeck: Unreal Engine 5 + mixed reality; 100 deep-space anomaly sims before flight ops.",
 "Year 3 — Capstone: design/operate cislunar tug concept; live range adjacency at Bowen corridor.",
 "Command spine — ADFA leadership model adapted for 100+ crew deep-space culture.",
 "Campuses — Western Sydney Aerotropolis (classroom/sim) + Qld flight corridor (ops).",
]
cy = y-11*mm
for line in curr:
    cy = wrap("• "+line, M+101*mm, cy, page_w-M-104*mm, size=5.8, leading=7)
    cy -= 1.2*mm

y = y - map_h - 4*mm

# Ship concept callouts
ship_h = 58*mm
rr(M, y-ship_h, page_w-2*M, ship_h, fill=panel, stroke=cyan)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(M+3*mm, y-4.5*mm, "KANGAROO-CLASS NCC-992-AU — CONCEPT CALLOUTS (FICTION COVER)")
# image
ir2 = ImageReader(preview)
avail_w = 115*mm; avail_h = ship_h-12*mm
iw,ih = ir2.getSize(); sc=min(avail_w/iw, avail_h/ih); dw,dh=iw*sc, ih*sc
c.drawImage(ir2, M+3*mm, y-ship_h+3*mm, width=dw, height=dh, mask='auto')
cx = M+3*mm+dw+4*mm
c.setFillColor(cyan); c.setFont("Helvetica-Bold", 6)
c.drawString(cx, y-12*mm, "Narrative mapping only")
callouts = [
 "Hull metaphor → Titomic / Lab22 titanium AM",
 "Impulse metaphor → Neumann Mo EP (+ Gilmour access)",
 "Sensors metaphor → Fleet Space + EOS SSA",
 "Sickbay metaphor → AU medtech / quantum sensing adjacency",
 "Shipyard metaphor → Bowen build+launch corridor",
 "Academy metaphor → W.Sydney + ADFA + UNSW",
 "Made in Australia / on-country framing",
]
cy=y-17*mm
for line in callouts:
    cy=wrap("→ "+line, cx, cy, page_w-cx-M-2*mm, size=5.8, leading=7)
c.setFillColor(muted); c.setFont("Helvetica-Oblique", 5)
c.drawString(M+3*mm, y-ship_h+1.5*mm, "LCARS concept art — not engineering certification. Warp/phaser numbers are fiction.")

y = y - ship_h - 4*mm

# Medicine + Made in AU strip
rr(M, y-28*mm, (page_w-2*M)/2-2*mm, 28*mm, fill=panel, stroke=cyan)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(M+3*mm, y-5*mm, "TRICORDER / SICKBAY ADJACENCY")
wrap("Exploration medicine & instruments: Cochlear / ResMed lineage, UniMelb bionic-eye research path, UNSW silicon-quantum / sensing heritage. Use as Australian human-systems depth — not as flying medical devices on this sheet.",
     M+3*mm, y-10*mm, (page_w-2*M)/2-8*mm, size=5.8, leading=7)

rr(M+(page_w-2*M)/2+2*mm, y-28*mm, (page_w-2*M)/2-2*mm, 28*mm, fill=panel, stroke=gold)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7)
c.drawString(M+(page_w-2*M)/2+5*mm, y-5*mm, "MADE IN AUSTRALIA")
wrap("On-continent materials → print → launch. Qld flight corridor + southern industrial cities (Adelaide/Melbourne) + Canberra SSA/Academy. Northern ranges for Starship-class diligence only. Proudly built on country — without claiming a liquidated spaceport.",
     M+(page_w-2*M)/2+5*mm, y-10*mm, (page_w-2*M)/2-8*mm, size=5.8, leading=7)

# Ask footer
rr(M, 7*mm, page_w-2*M, 20*mm, fill=HexColor("#101f35"), stroke=gold, sw=0.9)
c.setFillColor(gold); c.setFont("Helvetica-Bold", 7.5)
c.drawString(M+3.5*mm, 21*mm, "ASK")
c.setFillColor(light); c.setFont("Helvetica", 6.5)
c.drawString(M+3.5*mm, 15.5*mm, "30-min exploratory with SpaceX launch-site / manufacturing BD (+ SpaceXAI if Grok compute co-travels).")
c.setFillColor(muted); c.setFont("Helvetica", 5.8)
c.drawString(M+3.5*mm, 10.5*mm, "Crystal Elle Arena-Turner · Chief Engineer · teraustralis.incognita@gmail.com · +61 450 144 997 · TerAustralis.com.au · ABN 70 741 068 059")
c.setFillColor(gold); c.setFont("Helvetica-Bold", 6)
c.drawRightString(page_w-M-3.5*mm, 15.5*mm, "Solve access · stay · build · crew")
c.setFillColor(light); c.setFont("Helvetica", 6)
c.drawRightString(page_w-M-3.5*mm, 10.5*mm, "Not cosplay — industrial civilisation kit")

c.save()
print("Wrote", out)

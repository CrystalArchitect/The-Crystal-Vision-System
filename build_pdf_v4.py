#!/usr/bin/env python3
"""Starfleet Australia Kangaroo-class pitch — densified 3-pager (v4)."""
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

# Blueprint enhance
im = PILImage.open(img_path).convert("RGB")
im = ImageEnhance.Contrast(im).enhance(1.18)
im = ImageEnhance.Sharpness(im).enhance(1.3)
w, h = im.size
im = im.crop((int(w * 0.02), int(h * 0.02), int(w * 0.98), int(h * 0.70)))
im.thumbnail((2400, 1200), PILImage.Resampling.LANCZOS)
im.save(preview, "JPEG", quality=93, optimize=True)

# Australia site map (schematic)
mw, mh = 900, 700
mp = PILImage.new("RGB", (mw, mh), (7, 14, 26))
d = ImageDraw.Draw(mp)
outline = [
    (520, 40), (580, 70), (640, 120), (700, 200), (740, 280), (760, 360), (750, 450),
    (720, 520), (680, 560), (620, 590), (540, 610), (460, 600), (400, 560), (360, 500),
    (340, 420), (320, 340), (300, 280), (280, 220), (300, 160), (340, 100), (400, 60),
    (460, 40), (520, 40),
]
d.polygon(outline, fill=(18, 36, 58), outline=(61, 190, 182))
sites = [
    ("Bowen / Gilmour\n(orbital licence)", 620, 280, (212, 175, 55)),
    ("Christmas Is.\n(Starship recovery)", 200, 200, (232, 168, 124)),
    ("Northern ranges\n(diligence only)", 480, 120, (232, 168, 124)),
    ("Koonibba / Whalers Way\nSouthern Launch", 360, 380, (212, 175, 55)),
    ("Adelaide\nNeumann / Fleet", 420, 430, (61, 190, 182)),
    ("Melbourne\nTitomic / Lab22", 520, 500, (61, 190, 182)),
    ("Canberra\nEOS / ADFA", 580, 400, (61, 190, 182)),
    ("Western Sydney\nAcademy + Westmead", 640, 380, (212, 175, 55)),
]
for name, x, y, col in sites:
    d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=col)
    d.text((x + 11, y - 12), name, fill=(240, 244, 250))
d.text((20, 20), "AUSTRALIA — INDUSTRIAL NODES (schematic)", fill=(212, 175, 55))
d.text(
    (20, mh - 30),
    "Not to scale · ELA/Arnhem NOT live · Northern Starship sites = diligence only",
    fill=(154, 171, 191),
)
mp.save(map_path)

page_w, page_h = A4
c = canvas.Canvas(out, pagesize=A4)
M = 8 * mm
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


def rr(x, y, w, h, r=1.8 * mm, fill=None, stroke=None, sw=0.5):
    if fill:
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
        c.roundRect(x, y, w, h, r, fill=0, stroke=1)


def wrap(text, x, y, max_w, font="Helvetica", size=6.2, leading=7.4, color=light):
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


def page_chrome(page_label):
    c.setFillColor(navy)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    c.setFillColor(cyan_dim)
    c.rect(0, 0, 2 * mm, page_h, fill=1, stroke=0)
    c.setFillColor(gold)
    c.rect(2 * mm, 0, 0.5 * mm, page_h, fill=1, stroke=0)
    rr(M, page_h - 20 * mm, page_w - 2 * M, 13 * mm, fill=panel, stroke=cyan, sw=0.65)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(M + 3 * mm, page_h - 10 * mm, "STARFLEET FOR REAL — AUSTRALIA")
    c.setFillColor(cyan)
    c.setFont("Helvetica", 6.2)
    c.drawString(
        M + 3 * mm,
        page_h - 14.5 * mm,
        "Kangaroo-class NCC-992-AU  ·  First principles + diligence  ·  SpaceX / SpaceXAI",
    )
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawRightString(page_w - M - 3 * mm, page_h - 9 * mm, "CHIEF ENGINEER")
    c.setFillColor(light)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawRightString(page_w - M - 3 * mm, page_h - 13 * mm, "Crystal Elle Arena-Turner")
    c.setFillColor(muted)
    c.setFont("Helvetica", 5)
    c.drawRightString(page_w - M - 3 * mm, page_h - 16.5 * mm, f"TerAustralis · Sydney · 6 Sep 2026 · {page_label}")


# ===================== PAGE 1 =====================
page_chrome("Page 1 / 3 — Problem & Stack")
y = page_h - 25 * mm

# FIRST PRINCIPLES — denser
rr(M, y - 40 * mm, page_w - 2 * M, 40 * mm, fill=panel, stroke=gold, sw=0.75)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7.2)
c.drawString(M + 3 * mm, y - 4.5 * mm, "FIRST PRINCIPLES — THE PROBLEM WE ARE SOLVING")
probs = [
    (
        "1. Access",
        "Interplanetary civilisation needs cheap, frequent access — not one heroic launch. AU has ocean ranges, northern geography, Gilmour Bowen (licensed orbital site), Southern Launch (Koonibba re-entry + Whalers Way). No SpaceX Starship MoU yet; Christmas Island recovery (Ship 40, Jul–Aug 2026) already put AU in the recovery loop.",
    ),
    (
        "2. Stay",
        "Fleets die without in-space mobility. Neumann Drive solid-metal EP now in commercial cadence (ND-25 on Transporter-16/17; ND-50 commissioned on SSTL CarbSAR Jan 2026). Debris→propellant with CisLunar = roadmap, not done.",
    ),
    (
        "3. Build",
        "You cannot supply a fleet from Earth forever. Titomic Kinetic Fusion (CSIRO-origin cold spray) + Lab22/Amaero metal AM = industrial replicator path. Titomic: NASA SAA (Feb 2026), defence-prime EMD, US CRADA, Lufthansa/NLR orders — US defence/aerospace traction; softens any AU-space-champion overclaim; not a Starship hull line.",
    ),
    (
        "4. Crew",
        "Hardware without people is scrap. ADFA-grade Academy (Western Sydney Aerotropolis + Qld flight corridor) trains builders/operators. Holodeck = UE5/MR sims first. Parallel: Westmead digital-health demand for Grok/compute (separate sydney-xai-pack).",
    ),
]
py = y - 9 * mm
for t, b in probs:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(M + 3 * mm, py, t)
    py = wrap(b, M + 16 * mm, py, page_w - 2 * M - 20 * mm, size=5.5, leading=6.5)
    py -= 0.8 * mm

y = y - 44 * mm
lw = 98 * mm
rw = page_w - 2 * M - lw - 3 * mm
lx = M
rx = M + lw + 3 * mm
sh = 118 * mm

# Systems stack
rr(lx, y - sh, lw, sh, fill=panel, stroke=gold_dim)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.8)
c.drawString(lx + 2.5 * mm, y - 4.5 * mm, "SYSTEMS ARCHITECTURE (BOTTOM → TOP)")
layers = [
    (
        "07 ACADEMY / HOLODECK",
        "Western Sydney Aerotropolis + ADFA leadership model. Y1 shipbuilding/propulsion/astrogation; Y2 UE5 holodeck; Y3 cislunar tug capstone at Bowen corridor.",
        cyan,
    ),
    (
        "06 MEDICINE / TRICORDER",
        "AU medtech adjacency: Cochlear, ResMed lineage, bionic-eye research; UNSW quantum sensing / gravimetry — adjacency, not productised Starfleet kit.",
        cyan,
    ),
    (
        "05 SENSORS / SSA / COMMS",
        "Fleet Space (Adelaide) commercial subsurface / constellation. EOS laser SSA proven; optical comms in product set; active debris control aspirational.",
        gold,
    ),
    (
        "04 PROPULSION",
        "Neumann Mo EP (commercial on-orbit cadence 2026). Gilmour hybrids for access. Hypersonix SPARTAN/DART AE Mach 5+ flight (Wallops, Feb 2026; NRF-backed). ANSTO nuclear-thermal = research only.",
        gold,
    ),
    (
        "03 MANUFACTURE",
        "Titomic Kinetic Fusion + Lab22/Amaero. NASA SAA + aerospace/defence orders 2026. Gilmour R&D / Boeing green-Ti tests — pilots, not hull production.",
        gold,
    ),
    (
        "02 LAUNCH / RANGE / RE-ENTRY",
        "Gilmour Bowen (orbital licence; Eris TF1 Jul 2025 anomaly, TF2 target early 2027*). Southern Launch Koonibba (commercial re-entry) + Whalers Way. ELA NOT live.",
        warn,
    ),
    (
        "01 FOUNDATION",
        "Li/REE/Ti · US–AU TSA in force 23 Jul 2024 · ITAR still applies · Statement on Space Jul 2026 · power/water/social licence.",
        muted,
    ),
]
box_h = 14.2 * mm
y0 = y - 7 * mm
for i, (t, b, acc) in enumerate(layers):
    by = y0 - (i + 1) * box_h - i * 0.6 * mm
    rr(lx + 2 * mm, by, lw - 4 * mm, box_h, r=1.1 * mm, fill=panel2, stroke=acc, sw=0.4)
    c.setFillColor(acc)
    c.rect(lx + 2 * mm, by, 1 * mm, box_h, fill=1, stroke=0)
    c.setFillColor(acc)
    c.setFont("Helvetica-Bold", 5.2)
    c.drawString(lx + 4 * mm, by + box_h - 3.2 * mm, t)
    wrap(b, lx + 4 * mm, by + box_h - 6 * mm, lw - 8.5 * mm, size=4.8, leading=5.5)

# Right column
rr(rx, y - 32 * mm, rw, 32 * mm, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(rx + 2.2 * mm, y - 4 * mm, "WHY SPACEX / AU — GEOGRAPHY + TREATY")
wrap(
    "TSA (in force 23 Jul 2024) is the treaty-level foundation for US entities to conduct launch activities involving sensitive US tech from Australian territory — not a blanket approval; each activity still needs AU licences under the Space (Launches and Returns) Act 2018. Ship 40 Indian Ocean splashdown + Christmas Island recovery (Jul–Aug 2026) already exercised AU logistics adjacency. Policy estimate at TSA entry: 45–95 launches / decade, A$460m–A$1.2bn for AU spaceport operators (ministerial speech 2024) — signal, not a SpaceX booking.",
    rx + 2.2 * mm,
    y - 8.5 * mm,
    rw - 4.5 * mm,
    size=5.2,
    leading=6.2,
)

rr(rx, y - 32 * mm - 2.5 * mm - 38 * mm, rw, 38 * mm, fill=panel, stroke=gold_dim)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(rx + 2.2 * mm, y - 32 * mm - 2.5 * mm - 4 * mm, "BUILD PHASES")
ph = [
    (
        "P1 · 12 mo · PROVE",
        "Titomic-class structure demo; Bowen + Southern Launch narrative; northern-AU Starship range diligence (no dead brands).",
    ),
    (
        "P2 · 24 mo · CREW",
        "Academy charter: SpaceX + ASA + UNSW/ADFA. ~100 cadets. Capstone = cislunar tug concepts.",
    ),
    (
        "P3 · 5 yr · ORBIT",
        "Print hab segment on ground → launch → on-orbit assembly demo from AU range.",
    ),
]
py = y - 32 * mm - 2.5 * mm - 9 * mm
for t, b in ph:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawString(rx + 2.2 * mm, py, t)
    py = wrap(b, rx + 2.2 * mm, py - 2.8 * mm, rw - 4.5 * mm, size=5.1, leading=6)
    py -= 1.2 * mm

bot_h = sh - (32 * mm + 2.5 * mm + 38 * mm + 2.5 * mm)
rr(rx, y - sh, rw, bot_h, fill=panel, stroke=warn)
c.setFillColor(warn)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(rx + 2.2 * mm, y - 32 * mm - 2.5 * mm - 38 * mm - 2.5 * mm - 4 * mm, "HARD BOUNDARIES")
wrap(
    "No warp. No Starship MoU. ELA/Arnhem not operational (liquidation 2026). SpIRIT ≠ Gilmour (UniMelb / Inovor / Neumann). Debris-refuel & EOS debris-control = roadmap. Concept art ≠ hardware. Eris has not yet reached orbit.",
    rx + 2.2 * mm,
    y - 32 * mm - 2.5 * mm - 38 * mm - 2.5 * mm - 8.5 * mm,
    rw - 4.5 * mm,
    size=5.2,
    leading=6.2,
)

# Partner strip
ps_y = 6 * mm
rr(M, ps_y, page_w - 2 * M, 18 * mm, fill=HexColor("#101f35"), stroke=gold, sw=0.65)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6)
c.drawString(M + 2.5 * mm, ps_y + 13 * mm, "PARTNER / HERITAGE ROSTER (FACT-CHECKED · SEP 2026)")
wrap(
    "Gilmour Space (Bowen, Eris TF1 Jul 2025 / TF2 early 2027*, ElaraSat Transporter-14, Series E A$217m) · Southern Launch (Koonibba commercial re-entry; Whalers Way; A$25m Series A Jun 2026 incl. A$10m NRF) · Neumann Space (commercial ND-25 Transporter cadence; ND-50 CarbSAR) · Titomic + CSIRO Lab22 (NASA SAA; aerospace/defence orders) · Fleet Space (Series D >A$800m) · EOS Atlas (dev) · Hypersonix (DART AE) · UNSW / RMIT / ADFA · Westmead (compute parallel). SpIRIT: UniMelb / Inovor / Neumann — not Gilmour.",
    M + 2.5 * mm,
    ps_y + 9 * mm,
    page_w - 2 * M - 5 * mm,
    size=5,
    leading=5.8,
)

c.showPage()

# ===================== PAGE 2 — DILIGENCE =====================
page_chrome("Page 2 / 3 — Diligence & Evidence")
y = page_h - 25 * mm

# Sector snapshot
rr(M, y - 28 * mm, page_w - 2 * M, 28 * mm, fill=panel, stroke=gold, sw=0.7)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7)
c.drawString(M + 3 * mm, y - 4.5 * mm, "AU SPACE SECTOR SNAPSHOT (PUBLIC FIGURES)")
cols = [
    (
        "Scale",
        "A$4.6bn annual turnover · ~17,000 FTE · ~620 organisations (ASA Space Sector Fact Sheet, rev. Jul 2025). Specialised space SMEs historically ~A$1.1bn turnover.",
    ),
    (
        "Policy 2026",
        "Statement on Space (21 Jul 2026): Trusted Space Services · Spaceflight Ecosystem · Space Platforms · Microgravity Ecosystem · Exploration Technologies. SoE to ASA: accelerate approvals / modernise licensing.",
    ),
    (
        "Capital signal",
        "NRFC disclosed space-related: Gilmour A$75m (of A$217m Series E), Advanced Navigation A$50m, Liquid Instruments ~A$28m, Myriota A$25m, Southern Launch A$10m, Hypersonix A$10m — sum ≈A$198m+ (not an official pot).",
    ),
]
cw = (page_w - 2 * M - 6 * mm) / 3
for i, (t, b) in enumerate(cols):
    x = M + 3 * mm + i * (cw + 1 * mm)
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 5.8)
    c.drawString(x, y - 9 * mm, t)
    wrap(b, x, y - 13 * mm, cw - 2 * mm, size=5, leading=5.9)

y = y - 32 * mm

# Partner status — taller
partner_h = 68 * mm
rr(M, y - partner_h, page_w - 2 * M, partner_h, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7)
c.drawString(M + 3 * mm, y - 4.5 * mm, "PARTNER STATUS — WHAT CHANGED (LIVE AS OF SEP 2026)")
rows = [
    (
        "Gilmour Space",
        "Bowen = AU's first licensed orbital launch facility. Eris TF1 (30 Jul 2025): hybrid motor / oxidiser-pump faults ~9–17s; ASA report filed Apr 2026. Company TF2 target early 2027* (site; prior Q4 2026 messaging — treat as soft). ElaraSat MMS-1 on SpaceX Transporter-14 (Jun 2025). Series E A$217m (Jan 2026; NRFC A$75m + Hostplus et al.). Public SpaceX link = rideshare customer only — no JV found.",
    ),
    (
        "Southern Launch",
        "Was missing from earlier pack. Koonibba: world's first commercial spacecraft re-entry (Feb 2025) + further re-entries (incl. Varda W-6 May 2026). Whalers Way orbital complex. A$25m Series A Jun 2026 (Brindabella + A$10m NRF). Artemis II support cited.",
    ),
    (
        "Neumann Space",
        "Commercial production: ND-25 on SpaceX Transporter-16 (Apr 2026) and eight units on Transporter-17 (Jul 2026); ND-50 commissioned on SSTL CarbSAR (launched Jan 2026). CisLunar Industries debris to metal propellant = partnership roadmap.",
    ),
    (
        "Titomic (TTT)",
        "NASA Space Act Agreement Feb 2026 (cold-spray component eval). Lufthansa Technik >A$1.2m order May 2026. Royal NLR ~EUR 1.02m systems Mar 2026. Titomic USA multi-year military CRADA Jun 2026. Traction mostly US defence/aerospace sustainment (incl. US$1.7m EMD + CRADA); not an AU Starship hull factory. HY26 burn — investment phase.",
    ),
    (
        "Hypersonix / Fleet / EOS",
        "Hypersonix: DART AE Mach 5+ (Feb 2026); VISR next; Series A ~A$46m (NRFC A$10m). Fleet: Series D A$150m / >A$800m val; ASCEND2LEO delivered; SPIDER lunar adjacency. EOS: laser SSA + Atlas HEL space-control brand (IAC 2025) — market development, not booked production.",
    ),
]
ry = y - 9.5 * mm
for name, body in rows:
    c.setFillColor(cyan)
    c.setFont("Helvetica-Bold", 5.5)
    c.drawString(M + 3 * mm, ry, name)
    ry = wrap(body, M + 32 * mm, ry, page_w - 2 * M - 36 * mm, size=5.1, leading=6)
    ry -= 1.2 * mm

y = y - partner_h - 3 * mm
footer_top = 24 * mm
avail = y - footer_top - 2 * mm

h1 = avail * 0.28
h2 = avail * 0.45
h3 = avail - h1 - h2 - 4 * mm

rr(M, y - h1, page_w - 2 * M, h1, fill=panel, stroke=gold, sw=0.65)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.8)
c.drawString(M + 3 * mm, y - 4.2 * mm, "WHY NOW — SECOND-GEOGRAPHY LOGIC (NOT A MOU)")
wrap(
    "SpaceX already operates global recovery and rideshare logistics; AU just hosted Ship 40 recovery off Christmas Island (Jul-Aug 2026). TSA (23 Jul 2024) is the missing legal layer for US vehicles on AU soil — still per-activity licensing. Domestic stack is no longer brochure-only: licensed Bowen pad, commercial re-entry at Koonibba, Neumann flying commercially on Transporter, Titomic inside NASA/defence evaluation channels. Statement on Space (Jul 2026) explicitly prioritises spaceflight ecosystem + platforms + microgravity — the same four first principles as this pitch. Gap: no Starship site MoU, Eris not orbital yet, northern geography still diligence. Compare (not equate) to SpaceX second-geography logic (e.g. Louisiana/Pecan Island reporting: SSO geometry, acreage, propellant, pad congestion). AU offers SSO/polar from Whalers Way (~55–177°), mid-inclination from Bowen, TSA path, ally trust — but lacks Henry Hub-scale methalox and proven cadence. Frame as allied second-hemisphere option, not a Starbase clone.",
    M + 3 * mm, y - 9 * mm, page_w - 2 * M - 6 * mm, size=5.2, leading=6.2,
)

y = y - h1 - 2 * mm
half = (page_w - 2 * M - 3 * mm) / 2
rr(M, y - h2, half, h2, fill=panel, stroke=warn)
c.setFillColor(warn)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(M + 2.5 * mm, y - 4.2 * mm, "HARD BLOCKERS / OPEN QUESTIONS")
wrap(
    "• ITAR / US export licences still required for US launch-tech collaboration — TSA is safeguarding, not a tech-transfer free pass. • Every launch/return needs AU licence/permit; reforms removed the three-stage facility-licence process but the safety bar remains. • Eris has not reached orbit; cadence risk until TF2+ and insurer comfort. • Propellant logistics, workforce depth, environmental/airspace approvals, and Indigenous/land partnerships (e.g. Koonibba Community Aboriginal Corporation) are real schedule drivers. • Northern AU Starship geography = diligence only until a live operator + MoU. • No public industrial-scale rocket-grade methalox/LOX chain for Starship-class cadence (LNG != pad cryogenics). • Capital: NRF is selective equity, not a blank cheque for a Starbase clone. Workforce ~17k FTE sector-wide — thin for heavy-lift ops.",
    M + 2.5 * mm, y - 9 * mm, half - 5 * mm, size=5.1, leading=6.2,
)

rr(M + half + 3 * mm, y - h2, half, h2, fill=panel, stroke=gold)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(M + half + 5.5 * mm, y - 4.2 * mm, "STATEMENT ON SPACE — ALIGNMENT")
wrap(
    "Maps to Jul 2026 Statement without inventing funding: • Spaceflight ecosystem → Bowen + Southern Launch + TSA pathway • Space platforms / manufacturing → Titomic / Lab22 / satellite buses • Trusted space services → Fleet EO/PNT-adjacent + EOS SSA • Microgravity ecosystem → re-entry recovery at Koonibba (Varda-class) • Exploration technologies → Neumann mobility + remote-ops / mining heritage IIP enhanced space A$9.08–12.28bn / decade; wider space+cyber A$27–38bn — buyer signal, not a bid. Regulatory SoE to ASA: accelerate approvals / modernise licensing — helpful for cadence if executed.",
    M + half + 5.5 * mm, y - 9 * mm, half - 5 * mm, size=5.1, leading=6.2,
)

y = y - h2 - 2 * mm
rr(M, y - h3, page_w - 2 * M, h3, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(M + 3 * mm, y - 4 * mm, "DILIGENCE CHECKLIST — BEFORE ANY ASK HARDENS")
wrap(
    "Confirm TSA activity pathway + AU licence class for candidate vehicle/site. Shortlist northern range sites with land tenure, env, airspace, and community status (exclude liquidated brands). Gilmour TF2 schedule + Bowen capacity assumptions in writing. Southern Launch re-entry cadence / Whalers Way orbital readiness notes. Titomic P1 demo SOW (geometry, alloy, NDE). Neumann flight-heritage one-pager for BD. Academy MoU skeleton (ASA + UNSW/ADFA + state). Power/water/port logistics for shipyard-scale AM. Companion Grok/compute pack only if SpaceXAI co-travels. Red-team: what fails if Eris slips another year?",
    M + 3 * mm, y - 8.5 * mm, page_w - 2 * M - 6 * mm, size=5.1, leading=6.1,
)

# Compute parallel footer
rr(M, 5.5 * mm, page_w - 2 * M, 16 * mm, fill=HexColor("#101f35"), stroke=cyan, sw=0.55)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6)
c.drawString(M + 2.5 * mm, 16.5 * mm, "PARALLEL STACK — SPACE XAI / GROK (SEPARATE PACK)")
wrap(
    "Same civilisation problem, digital layer: sovereign/APAC Grok deploy + NSW AI Data Centre Framework; Westmead Health Precinct as clinical demand (digital health / neuro imaging — not claiming motor-BCI trials). Outreach: DISR AICollaboration + Austrade + xAI sales@. See companion sydney-xai-pack.",
    M + 2.5 * mm, 12 * mm, page_w - 2 * M - 5 * mm, size=5, leading=5.8,
)

c.showPage()

# ===================== PAGE 3 =====================
page_chrome("Page 3 / 3 — Sites, Ship, Ask")
y = page_h - 25 * mm

map_h = 72 * mm
rr(M, y - map_h, 92 * mm, map_h, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(M + 2.5 * mm, y - 4.5 * mm, "INDUSTRIAL GEOGRAPHY")
ir = ImageReader(map_path)
c.drawImage(
    ir,
    M + 2.5 * mm,
    y - map_h + 2.5 * mm,
    width=87 * mm,
    height=map_h - 9 * mm,
    preserveAspectRatio=True,
    mask="auto",
)

rr(M + 95 * mm, y - map_h, page_w - 2 * M - 95 * mm, map_h, fill=panel, stroke=gold_dim)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(M + 98 * mm, y - 4.5 * mm, "ACADEMY ARCHITECTURE")
curr = [
    "Y1 — Shipbuilding (Titomic/AM literacy), Propulsion (Neumann/Gilmour), Astrogation (UNSW Canberra Space / RMIT).",
    "Y2 — Holodeck: Unreal Engine 5 + mixed reality; deep-space anomaly sims before flight ops.",
    "Y3 — Capstone: design/operate cislunar tug concept; live range adjacency Bowen + SA corridors.",
    "Command spine — ADFA leadership model adapted for 100+ crew deep-space culture.",
    "Campuses — Western Sydney Aerotropolis (classroom/sim) + Qld / SA flight corridors (ops).",
    "Microgravity literacy — Koonibba re-entry/recovery as teaching adjacency (commercial already flying).",
]
cy = y - 10 * mm
for line in curr:
    cy = wrap("• " + line, M + 98 * mm, cy, page_w - M - 101 * mm, size=5.3, leading=6.3)
    cy -= 0.8 * mm

y = y - map_h - 3.5 * mm

# Ship concept
ship_h = 52 * mm
rr(M, y - ship_h, page_w - 2 * M, ship_h, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6.5)
c.drawString(M + 2.5 * mm, y - 4 * mm, "KANGAROO-CLASS NCC-992-AU — CONCEPT CALLOUTS (FICTION COVER)")
ir2 = ImageReader(preview)
avail_w = 108 * mm
avail_h = ship_h - 11 * mm
iw, ih = ir2.getSize()
sc = min(avail_w / iw, avail_h / ih)
dw, dh = iw * sc, ih * sc
c.drawImage(ir2, M + 2.5 * mm, y - ship_h + 2.5 * mm, width=dw, height=dh, mask="auto")
cx = M + 2.5 * mm + dw + 3.5 * mm
c.setFillColor(cyan)
c.setFont("Helvetica-Bold", 5.5)
c.drawString(cx, y - 10 * mm, "Narrative mapping only")
callouts = [
    "Hull metaphor → Titomic / Lab22 titanium AM",
    "Impulse metaphor → Neumann Mo EP (+ Gilmour access)",
    "Sensors metaphor → Fleet Space + EOS SSA",
    "Sickbay metaphor → AU medtech / quantum sensing adjacency",
    "Shipyard metaphor → Bowen + Southern Launch corridors",
    "Academy metaphor → W.Sydney + ADFA + UNSW",
    "Recovery metaphor → Koonibba / Christmas Island adjacency",
]
cy = y - 14.5 * mm
for line in callouts:
    cy = wrap("→ " + line, cx, cy, page_w - cx - M - 2 * mm, size=5.3, leading=6.3)
c.setFillColor(muted)
c.setFont("Helvetica-Oblique", 4.8)
c.drawString(
    M + 2.5 * mm,
    y - ship_h + 1.2 * mm,
    "LCARS concept art — not engineering certification. Warp/phaser numbers are fiction.",
)

y = y - ship_h - 3.5 * mm

# Three bottom panels
tw = (page_w - 2 * M - 4 * mm) / 3
rr(M, y - 30 * mm, tw, 30 * mm, fill=panel, stroke=cyan)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6)
c.drawString(M + 2 * mm, y - 4.2 * mm, "TRICORDER / SICKBAY")
wrap(
    "Exploration medicine & instruments: Cochlear / ResMed lineage, UniMelb bionic-eye path, UNSW silicon-quantum / sensing. Australian human-systems depth — not flying medical devices on this sheet.",
    M + 2 * mm,
    y - 8.5 * mm,
    tw - 4 * mm,
    size=5.1,
    leading=6,
)

rr(M + tw + 2 * mm, y - 30 * mm, tw, 30 * mm, fill=panel, stroke=gold)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 6)
c.drawString(M + tw + 4 * mm, y - 4.2 * mm, "MADE IN AUSTRALIA")
wrap(
    "On-continent materials → print → launch → recover. Qld orbital + SA re-entry/orbital + southern industrial cities + Canberra SSA/Academy. Northern ranges for Starship-class diligence only. No liquidated spaceports claimed live.",
    M + tw + 4 * mm,
    y - 8.5 * mm,
    tw - 4 * mm,
    size=5.1,
    leading=6,
)

rr(M + 2 * (tw + 2 * mm), y - 30 * mm, tw, 30 * mm, fill=panel, stroke=warn)
c.setFillColor(warn)
c.setFont("Helvetica-Bold", 6)
c.drawString(M + 2 * (tw + 2 * mm) + 2 * mm, y - 4.2 * mm, "WHAT WE STILL NEED")
wrap(
    "Live SpaceX BD channel · northern range site shortlist with land/env status · Titomic/Gilmour LOIs for P1 demo · Academy MoU skeleton (ASA/UNSW) · diligence binder (licences, NRF, TSA checklist).",
    M + 2 * (tw + 2 * mm) + 2 * mm,
    y - 8.5 * mm,
    tw - 4 * mm,
    size=5.1,
    leading=6,
)

# Ask
rr(M, 5.5 * mm, page_w - 2 * M, 18 * mm, fill=HexColor("#101f35"), stroke=gold, sw=0.85)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 7)
c.drawString(M + 3 * mm, 18.5 * mm, "ASK")
c.setFillColor(light)
c.setFont("Helvetica", 6)
c.drawString(
    M + 3 * mm,
    13.5 * mm,
    "30-min exploratory with SpaceX launch-site / manufacturing / recovery BD (+ SpaceXAI if Grok compute co-travels).",
)
c.setFillColor(muted)
c.setFont("Helvetica", 5.3)
c.drawString(
    M + 3 * mm,
    8.5 * mm,
    "Crystal Elle Arena-Turner · Chief Engineer · teraustralis.incognita@gmail.com · +61 450 144 997 · TerAustralis.com.au · ABN 70 741 068 059",
)
c.setFillColor(gold)
c.setFont("Helvetica-Bold", 5.5)
c.drawRightString(page_w - M - 3 * mm, 13.5 * mm, "Solve access · stay · build · crew")
c.setFillColor(light)
c.setFont("Helvetica", 5.5)
c.drawRightString(page_w - M - 3 * mm, 8.5 * mm, "Not cosplay — industrial civilisation kit")

c.save()
print("Wrote", out)

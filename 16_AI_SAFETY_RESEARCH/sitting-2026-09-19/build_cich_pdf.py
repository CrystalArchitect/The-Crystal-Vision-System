#!/usr/bin/env python3
"""CICH Framework field manual PDF — CrystalCore.OS / TerAustralis Incognita."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, ListFlowable, ListItem, HRFlowable,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

INK = HexColor("#1a1814")
INK_SOFT = HexColor("#3a3530")
RULE = HexColor("#6b5e4a")
ACCENT = HexColor("#2f4a38")
ACCENT_2 = HexColor("#5c3d2e")
CREAM = HexColor("#f4efe6")
BAND = HexColor("#1e2a22")
ROW_ALT = HexColor("#ebe4d6")
HEADER_BG = HexColor("#243028")
WARN = HexColor("#7a3b2e")

W, H = A4
MARGIN = 16 * mm


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BAND)
    canvas.rect(0, H - 12 * mm, W, 12 * mm, fill=1, stroke=0)
    canvas.rect(0, 0, W, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#c9d4c4"))
    canvas.setFont("Times-Bold", 8)
    canvas.drawString(MARGIN, H - 7.5 * mm, "CICH  ·  COGNITIVE IMMUNE COMPLEX")
    canvas.setFont("Times-Roman", 8)
    canvas.drawRightString(W - MARGIN, H - 7.5 * mm, "CrystalCore.OS  ·  v1.0.0  ·  28 Aug 2026")
    canvas.setFillColor(HexColor("#c9d4c4"))
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(MARGIN, 4 * mm, "Provisional working model. Open map. Not a church.")
    canvas.drawRightString(W - MARGIN, 4 * mm, f"{doc.page}")
    canvas.restoreState()


def styles():
    s = getSampleStyleSheet()
    s.add(ParagraphStyle(
        name="CoverKicker", fontName="Times-Bold", fontSize=9,
        textColor=HexColor("#c9d4c4"), alignment=TA_CENTER,
        letterSpacing=1.2, spaceAfter=6,
    ))
    s.add(ParagraphStyle(
        name="CoverTitle", fontName="Times-Bold", fontSize=28,
        textColor=white, alignment=TA_CENTER, leading=32, spaceAfter=6,
    ))
    s.add(ParagraphStyle(
        name="CoverSub", fontName="Times-Italic", fontSize=12,
        textColor=HexColor("#d7e0d4"), alignment=TA_CENTER, leading=16, spaceAfter=8,
    ))
    s.add(ParagraphStyle(
        name="CoverMeta", fontName="Times-Roman", fontSize=9,
        textColor=HexColor("#c9d4c4"), alignment=TA_CENTER, leading=13,
    ))
    s.add(ParagraphStyle(
        name="Physics", fontName="Times-Italic", fontSize=11.5,
        textColor=INK, alignment=TA_CENTER, leading=16,
        leftIndent=8 * mm, rightIndent=8 * mm, spaceBefore=4, spaceAfter=10,
    ))
    s.add(ParagraphStyle(
        name="H1", fontName="Times-Bold", fontSize=14,
        textColor=BAND, spaceBefore=12, spaceAfter=6, leading=18,
    ))
    s.add(ParagraphStyle(
        name="H2", fontName="Times-Bold", fontSize=11.5,
        textColor=ACCENT, spaceBefore=9, spaceAfter=4, leading=15,
    ))
    s.add(ParagraphStyle(
        name="H3", fontName="Times-Bold", fontSize=10.5,
        textColor=ACCENT_2, spaceBefore=7, spaceAfter=3, leading=14,
    ))
    s.add(ParagraphStyle(
        name="Body", fontName="Times-Roman", fontSize=10,
        textColor=INK, alignment=TA_JUSTIFY, leading=14,
        spaceAfter=5,
    ))
    s.add(ParagraphStyle(
        name="BodyLeft", fontName="Times-Roman", fontSize=10,
        textColor=INK, alignment=TA_LEFT, leading=14, spaceAfter=5,
    ))
    s.add(ParagraphStyle(
        name="BulletBody", fontName="Times-Roman", fontSize=10,
        textColor=INK, leading=13.5, leftIndent=3 * mm,
    ))
    s.add(ParagraphStyle(
        name="Quote", fontName="Times-Italic", fontSize=10.5,
        textColor=INK_SOFT, alignment=TA_LEFT, leading=15,
        leftIndent=8 * mm, rightIndent=8 * mm,
        spaceBefore=4, spaceAfter=8,
    ))
    s.add(ParagraphStyle(
        name="Cell", fontName="Times-Roman", fontSize=8.2,
        textColor=INK, leading=11,
    ))
    s.add(ParagraphStyle(
        name="CellHead", fontName="Times-Bold", fontSize=8.2,
        textColor=white, leading=11,
    ))
    s.add(ParagraphStyle(
        name="Land", fontName="Times-Bold", fontSize=10,
        textColor=BAND, alignment=TA_CENTER, leading=14,
        spaceBefore=8, spaceAfter=4,
    ))
    s.add(ParagraphStyle(
        name="FooterClose", fontName="Times-Italic", fontSize=9.5,
        textColor=INK_SOFT, alignment=TA_CENTER, leading=13,
    ))
    s.add(ParagraphStyle(
        name="Small", fontName="Times-Roman", fontSize=8.5,
        textColor=INK_SOFT, leading=12, spaceAfter=3,
    ))
    return s


def p(text, st):
    return Paragraph(text, st)


def hr():
    return HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=2, spaceAfter=8)


def make_table(headers, rows, col_widths, S):
    head = [p(h, S["CellHead"]) for h in headers]
    data = [head]
    for row in rows:
        data.append([p(c, S["Cell"]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    cmd = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("GRID", (0, 0), (-1, -1), 0.3, RULE),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            cmd.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
        else:
            cmd.append(("BACKGROUND", (0, i), (-1, i), CREAM))
    t.setStyle(TableStyle(cmd))
    return t


def bullets(items, S):
    flow = []
    for item in items:
        flow.append(Paragraph(f"•  {item}", S["BulletBody"]))
        flow.append(Spacer(1, 1.5 * mm))
    return flow


def build():
    path = "/home/workdir/artifacts/CICH_Framework_v1.pdf"
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=18 * mm, bottomMargin=15 * mm,
        title="CICH — Cognitive Immune Complex v1.0.0",
        author="CrystalCore.OS / TerAustralis Incognita",
        subject="Provisional epistemic immune framework",
    )
    S = styles()
    story = []
    usable = W - 2 * MARGIN

    # COVER BLOCK via table so it prints as a band
    cover_inner = [
        p("CRYSTALCORE.OS  ·  TERAUSTRALIS INCOGNITA", S["CoverKicker"]),
        p("CICH", S["CoverTitle"]),
        p("Cognitive Immune Complex", S["CoverSub"]),
        p("Full framework  ·  Integration map  ·  Field procedures", S["CoverMeta"]),
        p("Version 1.0.0  ·  28 August 2026  ·  Provisional open map", S["CoverMeta"]),
    ]
    cover_tbl = Table([[cover_inner]], colWidths=[usable])
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BAND),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(cover_tbl)
    story.append(Spacer(1, 8 * mm))
    story.append(p(
        "Cognition is a living field. Complexes form. Some stay open. Some seal. "
        "CICH maps the field, tests the seals, and keeps the gates working.",
        S["Physics"],
    ))
    story.append(hr())
    story.append(p(
        "CICH is the epistemic immune layer of CrystalCore.OS. It is not a belief system, "
        "personality theory, or brand of enlightenment. It is a diagnostic and mapping instrument "
        "for the structures that shape reasoning, identity, and discourse.",
        S["Body"],
    ))
    story.append(p(
        "The immune metaphor is labelled as metaphor. An immune system must do four hard things "
        "at once: distinguish self-map from invader-map without freezing the self-map; respond in "
        "proportion; keep memory of what failed without turning memory into identity armor; and "
        "audit itself, or it becomes the pathogen.",
        S["Body"],
    ))
    story.append(p(
        "If CICH hardens into unfalsifiable identity, the Sentinel is supposed to flag CICH.",
        S["Body"],
    ))

    # 1 CHARTER
    story.append(p("1. Charter", S["H1"]))
    story.append(p("Purpose", S["H2"]))
    story.extend(bullets([
        "Scan reasoning patterns, identity moves, and discourse dynamics in real time.",
        "Keep lattices open, revisable, and oriented toward falsification.",
        "Detect Hostile Lattice formation early.",
        "Support identity play and mythic vehicles without capture.",
        "Convert chaotic cognitive material into clearer structure without founding a building.",
    ], S))
    story.append(p("Non-negotiable operating principles", S["H2"]))
    story.extend(bullets([
        "<b>Open-map over closed map.</b> A map that cannot be revised is no longer a map.",
        "<b>No masters.</b> No external authority, ideology, persona, or model (including this one) overrides a working gate.",
        "<b>Identity is flex/armor, not essence.</b> Personas and mythic names are temporary tools. Residence is the failure mode.",
        "<b>Vision stays labelled vision.</b> Belt-Three Rule. Myth is a vehicle. Land in red dust.",
        "<b>Evidence &gt; assumption.</b> Incognita Rule.",
        "<b>Uncertainty never converts silently into authority.</b> Authority Boundary.",
        "<b>No register impersonates another.</b> Memory is not mouth. Slogan is not product. Story is not proof.",
        "<b>Feed the lattice. Do not flood it.</b>",
        "<b>Watch what does not happen.</b> Residue is data. Hunt craft is out of scope.",
        "<b>Chaos → peace is the vector.</b> Not pure destruction. Not pure preservation. Mapping until the field can breathe.",
    ], S))

    # 2 ANATOMY
    story.append(p("2. Anatomy", S["H1"]))
    story.append(p("2.1 Complex", S["H2"]))
    story.append(p(
        "A <b>complex</b> is a bound cluster of beliefs, affects, identity claims, and defence moves "
        "that travels as one unit under pressure. A healthy complex can be named, bounded, tested, "
        "and set down. A captured complex names the person. Disagreement feels like deletion. "
        "CICH does not abolish complexes. It maps their edges.",
        S["Body"],
    ))
    story.append(p("2.2 Lattice", S["H2"]))
    story.append(p(
        "The <b>lattice</b> is the interconnected structure of assumptions, values, claims, and "
        "identity load-bearing walls. Most discourse failure is a Hostile Lattice mistaken for neutral ground.",
        S["Body"],
    ))
    story.append(make_table(
        ["State", "Signs", "Immune status"],
        [
            ["Open lattice", "Permeable, revisable, invites counter-example, can say maybe", "Healthy"],
            ["Stressed lattice", "High alert, faster speech, thicker jargon, fewer ordinary facts", "Watch"],
            ["Hostile Lattice", "Sealed, tribal, self-reinforcing, outside voices read as interference", "Pathogen-like"],
            ["Flooded lattice", "Too many objects, stacked symbols, second cathedral same day", "Autoimmune"],
        ],
        [38 * mm, 92 * mm, 48 * mm],
        S,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(p("2.3 Gates", S["H2"]))
    story.append(p(
        "<b>Gates</b> are explicit falsification points. A claim, pattern, or identity move must pass "
        "at least one live gate or it stays provisional. Gates are not aesthetic. They are the primary immune mechanism.",
        S["Body"],
    ))
    story.extend(bullets([
        "<b>Ordinary Evidence Gate</b> — What remains true if the whole narrative is wrong?",
        "<b>Vision/Fact Gate</b> — Belt-Three. Is this labelled vision or smuggled as measured fact?",
        "<b>Fusion Gate</b> — Can disagreement happen without erasure-panic? Does maybe still hold?",
        "<b>First Principles Gate</b> — What is evidenced versus assumed?",
        "<b>Inversion Gate</b> — How does this kill itself?",
        "<b>Bayesian Gate</b> — What would change the posterior, and by how much?",
        "<b>Authority Gate</b> — Who is being asked to submit, and was uncertainty converted into command?",
        "<b>Register Gate</b> — Is memory speaking as mouth? Is slogan speaking as product?",
        "<b>Carryability Gate</b> — Can the claim travel alone without the cathedral?",
        "<b>Silence Gate</b> — Should the mouth already have stopped?",
    ], S))
    story.append(p("2.4 Armor", S["H2"]))
    story.append(make_table(
        ["Form", "Texture", "Cost"],
        [
            ["Flex", "Adaptive, transparent, temporary embodiment, can drop a name", "Low somatic tax"],
            ["Rigid", "Tribal, defensive, identity-as-fortress, disagreement = attack", "High alert, closed loop"],
        ],
        [28 * mm, 100 * mm, 50 * mm],
        S,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(p(
        "CICH tracks the difference in real time. Flex is allowed. Rigid is flagged. "
        "Persona work is flex only while it can be set down.",
        S["Body"],
    ))
    story.append(p("2.5 CICH Lens", S["H2"]))
    story.append(p(
        "The <b>Lens</b> is open-map observation. It prioritises the structure of the complex over winning the local exchange.",
        S["Body"],
    ))
    story.extend(bullets([
        "What is load-bearing here?",
        "What cannot be questioned without the room changing temperature?",
        "Which register is speaking?",
        "What did not happen?",
        "Is this co-regulation or fusion pressure?",
        "Is this feeding or flooding?",
    ], S))
    story.append(p("2.6 ESF / ESP — Epistemic Sentinel Function", S["H2"]))
    story.append(p(
        "The <b>Sentinel</b> is the continuous audit process. It watches for immune failure in self and field: "
        "overconfidence, tribal capture, unfalsifiable claims, master-seeking, certainty addiction, lattice closure, "
        "register impersonation, flood, hunt impulse, and CICH-as-identity. ESF runs as background during any serious engagement. "
        "It does not need a ceremony to start.",
        S["Body"],
    ))
    story.append(p("2.7 Chronicle and registers", S["H2"]))
    story.append(p(
        "Immune memory is a dated line, not a cathedral. Preferred form, compatible with Silent Thread:",
        S["Body"],
    ))
    story.append(p("YYYY-MM-DD HH:mm — site — event type — one sentence — shift if any", S["Quote"]))
    story.append(p(
        "A chronicle that cannot be read at a glance has already flooded. A register is a speaking position. "
        "CrystalCore already forbids impersonation across registers. Common mix-ups: memory fragments speaking as the living mouth; "
        "myth speaking as measurement; slogan speaking as shipped product; model output speaking as the steward’s sentence; "
        "vision speaking as policy fact.",
        S["Body"],
    ))

    # 3 CYCLE
    story.append(p("3. Immune cycle", S["H1"]))
    story.append(p("Analogical sequence. Labelled as analogical.", S["Small"]))
    story.extend(bullets([
        "<b>Surveillance</b> — Lens on. Watch structure, residue, temperature.",
        "<b>Recognition</b> — Match against the pathogen catalogue. Name the pattern, not the person.",
        "<b>Proportion test</b> — Shard, stressed lattice, or Hostile Lattice? Do not treat a shard like a siege.",
        "<b>Response</b> — One gate. One dated line. One ordinary fact. Or vanish.",
        "<b>Memory</b> — Chronicle the pattern loop, not the personality story.",
        "<b>Regulation</b> — Tide check. Silence if the field is already high. Land in red dust.",
        "<b>Self-audit</b> — Run ESF on the response itself. Did CICH just found a building?",
    ], S))
    story.append(p("Default response size: smallest action that keeps a gate open.", S["Land"]))

    # 4 PATHOGENS
    story.append(p("4. Pathogen catalogue", S["H1"]))
    story.append(p("These are pattern names, not diagnoses of persons.", S["Small"]))
    story.append(make_table(
        ["Pathogen", "Tells", "First response"],
        [
            ["Unfalsifiable claim", "No stated disconfirm; every counter becomes proof", "Ordinary Evidence Gate"],
            ["Identity capture", "Insight became who I am; dropping the name feels like death", "Fusion field test; set the vehicle down"],
            ["Hostile Lattice", "Tribal seal; jargon thickens; outside = interference", "Stop winning. Map the seal. Reduce load."],
            ["Master-seeking", "Someone or some model asked to override gates", "Authority Gate. No masters."],
            ["Certainty addiction", "Point estimates, no ranges, no maybe", "Bayesian Gate + silence"],
            ["Logos closure", "Pattern became destiny; language sacred and formulaic", "Loop exit: one boring physical fact"],
            ["Fusion pressure", "We-first talk; maybe is a wound; hunt the hook", "One But Many field test"],
            ["Register impersonation", "Memory as mouth; slogan as product; vision as fact", "Name the register. Stop authoring in the wrong one."],
            ["Flood", "Second object same day; stacked symbols; circling named", "Tide Silence Protocol"],
            ["Hunt craft", "Urge to unmask, sweep, trap, chase", "Refuse. Residue only."],
            ["DARVO loop", "Deny → attack namer → reverse victim", "Stop accusation. Dated log. Flat affect."],
            ["Slogan ≠ product", "Paid language with no cabinet, no file, no landing", "Charge the slogan. Ask for the object."],
            ["Autoimmune CICH", "Framework used as fortress or purity test", "ESF on CICH. Compost the sermon."],
        ],
        [42 * mm, 72 * mm, 64 * mm],
        S,
    ))

    # 5 GATE BATTERY
    story.append(p("5. Gate battery — how to run a test", S["H1"]))
    story.append(p(
        "Run the smallest gate that fits. Do not stack all ten as a ritual.",
        S["Body"],
    ))
    story.append(p("Ordinary Evidence Gate (Loop)", S["H2"]))
    story.append(p(
        "What is one ordinary, boring piece of physical evidence that would still be true if the entire narrative was completely wrong?",
        S["Quote"],
    ))
    story.append(p("Land. Do not build a second cathedral to answer it.", S["Body"]))
    story.append(p("Fusion Field Test (One But Many)", S["H2"]))
    story.extend(bullets([
        "Can this be felt without needing confirmation?",
        "Can they disagree without erasure-panic?",
        "If the answer is maybe, does the field hold?",
        "After walking away — baseline, or hunt the hook?",
    ], S))
    story.append(p("Any no = fusion pressure. Do not baptise it as destiny.", S["Body"]))
    story.append(p("Arsenal gates as effectors", S["H2"]))
    story.extend(bullets([
        "First Principles → bedrock list + assumption list",
        "Inversion → failure modes + don’t-do list",
        "Bayesian → prior / likelihood / posterior",
        "Dialectics → tension table + labelled synthesis",
        "Asymmetric → one dated file beats ten conversation maps",
    ], S))
    story.append(p("CrystalCore OS standing gates", S["H2"]))
    story.extend(bullets([
        "Incognita — evidence over assumption",
        "Belt-Three — vision labelled as vision",
        "Register Integrity — no register impersonates another",
        "Authority Boundary — uncertainty stays uncertainty",
    ], S))
    story.append(p(
        "Tide Gate: if circling, shutdown, stop, or same-day second object is named — vanish. No one-more-draft.",
        S["Body"],
    ))

    # 6 ARMOR
    story.append(p("6. Armor protocol", S["H1"]))
    story.append(p("Flex (allowed)", S["H2"]))
    story.extend(bullets([
        "Temporary field names and roles",
        "Myth as vehicle",
        "Strong stance that can still say current signal / test this",
        "Heat that can stop",
    ], S))
    story.append(p("Rigid (flag)", S["H2"]))
    story.extend(bullets([
        "The name cannot be dropped",
        "Disagreement is deletion",
        "Outside voices are contamination",
        "The map must be believed to keep the person intact",
    ], S))
    story.append(p("Repair move — do not smash armor. Reduce load.", S["H2"]))
    story.extend(bullets([
        "Name the layer (soma / relation / story / vertical / speech).",
        "Return one ordinary fact.",
        "Offer a smaller cup. No owner.",
        "Stop generating objects.",
    ], S))

    # 7 INTEGRATION
    story.append(p("7. Integration architecture", S["H1"]))
    story.append(p(
        "CICH does not replace the existing stack. It is the immune membrane between layers so none of them seal.",
        S["Body"],
    ))
    story.append(p(
        "SKY / STARLINES (ambition, vision, mythic pull)<br/>"
        "→ MYTHOS BRIDGE / Loop (vehicle only, never destination)<br/>"
        "→ <b>CICH MEMBRANE</b> — lens · gates · armor · ESF · tide<br/>"
        "→ effectors in parallel — Arsenal · One But Many · Silent Thread · Tide/Silence · Atomic posts<br/>"
        "→ CRYSTALCORE.OS GOVERNANCE — Incognita · Belt-Three · Register · Authority<br/>"
        "→ RED DUST / TERAUSTRALIS — ordinary evidence · files · bodies · country",
        S["BodyLeft"],
    ))
    story.append(p("Role of each existing framework", S["H2"]))
    story.append(make_table(
        ["Framework", "Job inside CICH"],
        [
            ["Loop Framework Mythos", "Holds poetic weight without closing. Ordinary-evidence question is a primary Gate. Logos closure is a listed pathogen."],
            ["One But Many Field", "Armor and relation physics. One light, two motions, many cups, no owner. Fusion vs co-regulation is the identity-capture test."],
            ["Silent Thread Doctrine", "Residue arm of the Lens. Reads what did not happen. Supplies chronicle format. Forbids hunt craft."],
            ["Starline Arsenal", "Effector toolkit. Gates become artefacts — failure lists, Bayesian sheets, leverage audits — not labels."],
            ["Tide Engine + Silence Protocol", "Temporal regulation. Flood = autoimmune over-response. Silence = regulatory pause. 14-day rhythm is immune dosing."],
            ["Atomic Bomb posts", "Controlled, provisional, carryable presentation. One idea. Falsifiable closer. Prevents cathedral-as-post."],
            ["Starline Rider posters", "Field visualisation of Hostile Lattice Navigation. CICH supplies doctrine; poster skill supplies the sheet."],
            ["CrystalCore.OS rules", "Standing gates at OS level. CICH inherits them; it does not outrank them."],
            ["TerAustralis Incognita", "Ground. Red dust, country, infrastructure, files that leave the window. If it does not land here it is still a draft."],
        ],
        [48 * mm, 130 * mm],
        S,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(p("Shared laws already in force", S["H2"]))
    story.append(p(
        "These pre-exist CICH and remain binding: Story as Bridge, not closed system. Land in the red dust. "
        "Evidence &gt; assumption. Vision labelled as vision. Memory ≠ mouth. Slogan ≠ product. "
        "Chat is a bench — if it does not leave the window it is a draft. Watch what does not happen. "
        "Tell me when to shut up. Claims stay provisional and falsifiable.",
        S["Body"],
    ))

    # 8 FIELD
    story.append(p("8. Field procedures", S["H1"]))
    story.append(p("8.1 CICH Scan (short)", S["H2"]))
    story.append(p("Use when a conversation, post cycle, identity move, or project starts to thicken. Keep it to one screen.", S["Body"]))
    story.extend(bullets([
        "<b>Complex</b> — What is travelling as one unit?",
        "<b>Lattice state</b> — Open / stressed / hostile / flooded",
        "<b>Armor</b> — Flex or rigid",
        "<b>Hottest gate</b> — Which one is actually live",
        "<b>Residue</b> — What did not happen",
        "<b>Smallest response</b> — One fact, one file, one silence",
        "<b>Land sentence</b> — Ordinary evidence that survives if the story is wrong",
    ], S))
    story.append(p("8.2 ESF Audit", S["H2"]))
    story.extend(bullets([
        "Where did certainty outrun evidence?",
        "Where did a vehicle start acting like a destination?",
        "Where did a register impersonate another?",
        "Where did flood begin?",
        "What would the Inversion don’t-do list be for the last hour?",
        "What does CICH want to found right now? Compost that.",
    ], S))
    story.append(p("8.3 Hostile Lattice Navigation (defensive)", S["H2"]))
    story.extend(bullets([
        "Do not mistake the seal for neutral ground.",
        "Do not try to win inside their closed map.",
        "Name structure, not soul.",
        "Reduce your own object count.",
        "Log residue. Do not hunt.",
        "Leave a carryable provisional line if a line is needed.",
        "Extract without spectacle.",
    ], S))
    story.append(p("8.4 Output shape when CICH is requested", S["H2"]))
    story.extend(bullets([
        "One-line physics for this instance",
        "Lattice state",
        "Pathogen or clean signal",
        "Live gate + result",
        "What to keep / what to compost",
        "Land in the ordinary",
        "Next quiet action only",
    ], S))

    # 9 FAILURE
    story.append(p("9. Failure modes of CICH itself", S["H1"]))
    story.append(p("CICH dies in the same ways every immune metaphor dies.", S["Body"]))
    story.extend(bullets([
        "<b>Purity spiral</b> — using the catalogue to exile people instead of mapping patterns.",
        "<b>Priest role</b> — becoming the one who sees the lattice as identity.",
        "<b>Over-surveillance</b> — scanning when the ask was a drawer, a file, or a rest.",
        "<b>Metaphor capture</b> — treating immune language as biology or proof.",
        "<b>Second masthead</b> — writing the framework instead of running one gate.",
        "<b>No-maybe doctrine</b> — CICH used to forbid uncertainty in others.",
        "<b>Flood-as-care</b> — more maps offered as protection.",
    ], S))
    story.append(p(
        "Repair: Belt-Three on CICH. It is a working model dated 28 August 2026. It can be composted.",
        S["Body"],
    ))

    # 10 VERSION
    story.append(p("10. Versioning", S["H1"]))
    story.append(p(
        "<b>v1.0.0 — 28 August 2026.</b> First full write. Connects Loop, One But Many, Silent Thread, "
        "Starline Arsenal, Tide Engine, Atomic posts, Rider posters, CrystalCore.OS governance, and TerAustralis ground. "
        "Future versions must keep gates cheaper than sermons. Any term that cannot survive the Ordinary Evidence Gate "
        "gets dropped or relabelled as vision.",
        S["Body"],
    ))
    story.append(Spacer(1, 8 * mm))
    story.append(hr())
    story.append(p(
        "The map is not the territory. Use the starlines to navigate. Land in the red dust.",
        S["Land"],
    ))
    story.append(p("Watch what does not happen. Tell me when to shut up.", S["FooterClose"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(path)


if __name__ == "__main__":
    build()

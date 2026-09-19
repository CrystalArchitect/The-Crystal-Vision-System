# AU industrial nodes — what this is, and what it is for

**Figure:** `assets/au-sites-map.png`  
**Used in:** Kangaroo-class 3-pager, page 3 (`GEOGRAPHY`)  
**Audience:** SpaceX / SpaceXAI exploratory BD  
**From:** Crystal Elle Arena-Turner · TerAustralis Incognita · 6 Sep 2026 hygiene, expanded 19 Sep 2026

This is the complete key for the schematic. A cropped export that only shows five dots is incomplete — the live figure has **all eight nodes**, a colour key, and the pitch purpose on the same canvas.

## What this is

A **schematic** of Australian space-industry sites. It is not a geographic chart, not to scale, and not an operations map.

Title on the figure: **AU INDUSTRIAL NODES (schematic)**.

## What this is for

A **sales graphic** inside **Starfleet for Real — Australia**, the Kangaroo-class pitch.

The pitch is: Australia can be an allied **shipyard + academy**, not a second Starbase. The map’s job is to make that look **already distributed on the ground** — launch, return, recovery adjacency, training, and institutional hubs — so a reviewer sees a stack to plug into, not a blank-slate spaceport ask.

Hard frame: **no Starship site MoU**. Northern Australia is diligence only. Equatorial Launch Australia / Arnhem is **not live**.

## Colour key

| Dot | Meaning | Use in the pitch |
|---|---|---|
| **Gold** | Live industrial | Named pads, ranges, or academy classroom |
| **Peach** | Adjacency / diligence | Recovery logistics or future geography — **not** a signed pad |
| **Cyan** | Institutional hub | City-scale partners (constellation, AM, agency, academy spine) |

## Gold — live industrial

| Node | What it is | What it is for in the pitch |
|---|---|---|
| **Bowen / Gilmour** | Gilmour Space licensed orbital site, Queensland. Eris TF1 Jul 2025 anomaly; TF2 ~early 2027*. ElaraSat flew SpaceX Transporter-14 (rideshare). Series E A$217m. | Mid-inclination **access**. Licensed pad + LV/sat builder. Do not claim Eris is orbital. |
| **Koonibba / Whalers Way** | Southern Launch. Koonibba: commercial re-entry (from Feb 2025, incl. Varda-class). Whalers Way: polar / SSO orbital complex. A$25m Series A Jun 2026 (A$10m NRF). | **Launch / return**. Microgravity recovery teaching adjacency. Polar/SSO geometry vs Bowen’s mid-inclination. |
| **W. Sydney Academy** | Proposed sim / classroom at Western Sydney Aerotropolis, plus **Westmead** health-precinct adjacency (digital health / neuro imaging — not motor-BCI trials). Flight ops along the Qld corridor (Gilmour/Bowen). ADFA leadership model + UNSW Canberra Space / RMIT / CSIRO. | **Crew**, and the SpaceXAI / Grok compute parallel. Academy before Hollywood. Holodeck v1 = MR/UE5 sims. |

## Peach — adjacency / diligence

| Node | What it is | What it is for in the pitch |
|---|---|---|
| **Christmas Is.** | Christmas Island. Pack cites Ship 40 Indian Ocean splashdown + recovery (Jul–Aug 2026). | **Recovery adjacency**. Shows AU already sat in SpaceX recovery logistics. Not a launch pad and not a MoU. |
| **North (diligence)** | Northern Australia as possible future heavy-lift / Starship-capable geography (policy, TSA/ITAR, energy, community). | Diligence only. **Do not** lead with Equatorial Launch Australia / Arnhem (ops ceased; liquidation 2026). |

## Cyan — institutional hubs

These three were on the full figure and dropped by the cropped screenshot.

| Node | What it is | What it is for in the pitch |
|---|---|---|
| **Adelaide** | **Neumann Space** (commercial Mo EP on Transporters) and **Fleet Space** (LEO + ExoSphere). Southern Launch is SA-based. | **Stay** (Neumann) and **sensors / trusted services** (Fleet). Debris→fuel remains roadmap. |
| **Melbourne** | Titomic + CSIRO **Lab22** metal AM. SpIRIT flew on SpaceX as **Uni Melbourne / Inovor / Neumann** — not Gilmour’s bird. RMIT sits on the academy science spine. | **Manufacture.** Exploratory AM, not a Starship hull line. Credit SpIRIT correctly. |
| **Canberra** | Australian Space Agency, ADFA, UNSW Canberra Space, EOS laser SSA. | **Policy + academy spine + SSA.** EOS laser tracking is proven; active debris “space control” is in development. |

## Footer (must stay on the figure)

> Not to scale · ELA / Arnhem not live · North = diligence only · No Starship MoU · SpIRIT is UniMelb / Inovor / Neumann, not Gilmour

## How it maps to the four first principles

| Principle | Nodes on this figure |
|---|---|
| **Access** | Bowen / Gilmour · Whalers Way · Christmas Island recovery · North (diligence) |
| **Stay** | Adelaide — Neumann EP (commercial on Transporters); debris→fuel is roadmap |
| **Build** | Melbourne — Titomic / Lab22 |
| **Crew** | W. Sydney Academy + Westmead · Canberra (ADFA / UNSW) |

## Not on this map (on purpose)

These show up in the pitch. They do **not** get their own dots.

| Item | Why it stays off the schematic |
|---|---|
| **ELA / Arnhem** | Not live (ops ceased; liquidation 2026). Covered by the North diligence disclaimer. |
| **Woomera Orbital Yard** | Fiction cover on the Kangaroo-class art sheet. Not an engineering or siting claim. |
| **Hypersonix** | Mach 5+ DART AE / SPARTAN demo flew at **Wallops** (Feb 2026). AU partner, not an Australian pad. |
| **ANSTO NTR** | Research only. |
| **Inovor** | Credited on SpIRIT with UniMelb / Neumann — not a separate city node. |
| **Amaero / Boeing green-Ti / MMI** | Manufacturing *adjacency* already under Melbourne Titomic / Lab22. Pilots, not a hull line. |
| **sydney-xai-pack / Grok NSW** | Parallel compute ask. Westmead is the map hook; the rest lives in that companion pack. |

## Rebuild

```bash
python3 nodes_map.py
python3 build_pdf_v5.py
```

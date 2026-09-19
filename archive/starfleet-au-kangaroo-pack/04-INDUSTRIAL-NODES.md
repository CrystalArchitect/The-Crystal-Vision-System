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
| **W. Sydney Academy** | Proposed sim / classroom at Western Sydney Aerotropolis. Flight ops along the Qld corridor (Gilmour/Bowen). ADFA leadership model + UNSW Canberra Space / RMIT / CSIRO. | **Crew**. Academy before Hollywood. Holodeck v1 = high-fidelity MR/UE5 sims, not a starship. |

## Peach — adjacency / diligence

| Node | What it is | What it is for in the pitch |
|---|---|---|
| **Christmas Is.** | Christmas Island. Pack cites Ship 40 Indian Ocean splashdown + recovery (Jul–Aug 2026). | **Recovery adjacency**. Shows AU already sat in SpaceX recovery logistics. Not a launch pad and not a MoU. |
| **North (diligence)** | Northern Australia as possible future heavy-lift / Starship-capable geography (policy, TSA/ITAR, energy, community). | Diligence only. **Do not** lead with Equatorial Launch Australia / Arnhem (ops ceased; liquidation 2026). |

## Cyan — institutional hubs

These three were on the full figure and dropped by the cropped screenshot.

| Node | What it is | What it is for in the pitch |
|---|---|---|
| **Adelaide** | Fleet Space — commercial LEO + ExoSphere subsurface mapping. Southern Launch is SA-based. | **Sensors / trusted services.** Fleet is a solid commercial hook. |
| **Melbourne** | Titomic / metal AM adjacency. SpIRIT flew on SpaceX as **Uni Melbourne / Inovor / Neumann** — not Gilmour’s bird. | **Manufacture.** Exploratory AM, not a Starship hull line. Credit SpIRIT correctly. |
| **Canberra** | Australian Space Agency, ADFA, UNSW Canberra Space, EOS laser SSA. | **Policy + academy spine + SSA.** EOS laser tracking is proven; active debris “space control” is in development. |

## Footer (must stay on the figure)

> Not to scale · ELA / Arnhem not live · North = diligence only · No Starship MoU · SpIRIT is UniMelb / Inovor / Neumann, not Gilmour

## How it maps to the four first principles

| Principle | Nodes on this figure |
|---|---|
| **Access** | Bowen / Gilmour · Whalers Way · Christmas Island recovery · North (diligence) |
| **Stay** | Not a map dot — Neumann EP (commercial on Transporters); debris→fuel is roadmap |
| **Build** | Melbourne Titomic / Lab22 adjacency |
| **Crew** | W. Sydney Academy · Canberra (ADFA / UNSW) |

## Rebuild

```bash
python3 nodes_map.py
python3 build_pdf_v5.py
```

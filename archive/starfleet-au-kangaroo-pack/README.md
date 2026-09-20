# Starfleet Australia — Kangaroo-class pack

Exploratory industrial brief: Australia as shipyard + academy adjacency for SpaceX / allied pathways.

**From:** Crystal Elle Arena-Turner · TerAustralis Incognita  
**Status:** Vision / proposal layer — fact-checked claims hygiene applied 2026-09-06.

**Hub launch (CVS):** Kangaroo Division — [`../../00_MASTER_INDEX/STARFLEET-AU-KANGAROO-DIVISION.md`](../../00_MASTER_INDEX/STARFLEET-AU-KANGAROO-DIVISION.md) · `python3 scripts/starfleet/launch_kangaroo_division.py`

## Contents
- `01-PITCH-ONE-PAGER.md` — thesis
- `02-SPEC-SHEET.md` — systems
- `03-FACTCHECK.md` — hygiene log
- `04-INDUSTRIAL-NODES.md` — complete key for the AU nodes schematic (what it is, what it is for, all eight sites)
- `nodes_map.py` — renders `assets/au-sites-map.png` with every node, role, colour key, and purpose line
- `Starfleet-Australia-Kangaroo-Class-*.pdf` — rendered briefs
- `assets/` — figures
- `outbox-*.json` — sent outreach records (agency addresses)

## Build
```bash
python3 nodes_map.py
python3 build_pdf_v5.py
```

The nodes map is a **sales graphic** for SpaceX / SpaceXAI: existing launch, recovery, and academy stack. Not a Starbase site map. A cropped five-dot export is incomplete — use the generated PNG or `04-INDUSTRIAL-NODES.md`.

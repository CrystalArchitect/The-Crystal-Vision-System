# CrystalCore.OS Freeze Pack — 2026-09-11

**Company:** TerAustralis Incognita  
**Product:** CrystalCore.OS  
**Freeze name:** `crystalcore-os-0.3-freeze-2026-09-11`  
**Status:** Paper freeze. Tag not yet cut. Tests not independently re-run on this date.  
**Owner:** Crystal Arena-Turner (CrystalArchitect)

This pack is the next step after the source/release audit. It does not invent a kernel. It makes the existing product *defensible in a room*: one company, one product name, one license split, one list of what actually runs, one checklist to cut a hashable tag.

## How to use this pack

1. Read `01-COMPANY-PRODUCT-BOUNDARY.md` first. That is the commercial sentence.
2. Read `02-WHAT-RUNS.md`. That is the technical sentence.
3. Apply `03-LICENSE-SPLIT.md` only after Crystal stamps it. License change is a legal act, not a git act.
4. Execute `04-FREEZE-CHECKLIST.md` on a machine that can see the private trees.
5. File the signed `05-TEST-LOG-TEMPLATE.md` once tests have been run by someone other than the author, or by the author with raw output attached.
6. Keep `06-VALUATION-BRIDGE.md` with the audit. Do not quote replacement cost as an asking price.

## Source of this freeze

Surveyed against:

- GitHub user CrystalArchitect (authenticated 2026-09-11): company field `TerAustralis Incognita`; bio names CrystalCore.OS.
- Private monorepo `CrystalArchitect/The-Crystal-Vision-System` at `d49855b6c135171f8094963a2cf0621fd0ee6a93`, subtree `archive/CrystalCore-OS/` (product v0.3 web shell + FastAPI backend + tests).
- Drive artifact `CrystalCore-OS-complete.zip` (2026-07-01 snapshot: mind/memory/flow/evolve + tests).
- Public indexed docs through 2026-09-06 (umbrella ADRs, STATUS ledger, Clementine, Architecture Archive).
- Live public clones of `CrystalCore.OS`, `TerAustralis-Incognita`, and `TerAustralis-Incognita-Code` returned 404 on 2026-09-11 from an unauthenticated fetch. Product source is currently private / monorepo-only.

Canon stamp remains Crystal's. This pack is a kept trail, not a rename of locked Constitution names.

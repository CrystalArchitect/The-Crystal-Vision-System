# Open backlog (hub coordination)

**Canon:** **no**  
**Updated:** 2026-10-06 (packet A Drive 16–20 done)  
**Role:** Single list of what remains open. IDs in [`WORKING-INDEX.md`](WORKING-INDEX.md).  
**Decision packets:** [`CRYSTAL-DECISIONS-PENDING.md`](CRYSTAL-DECISIONS-PENDING.md)  
**Agreement check:** [`NEEDS-YOUR-YES.md`](NEEDS-YOUR-YES.md) (plain) · [`AGREEMENT-WORKFLOW.md`](AGREEMENT-WORKFLOW.md) · `python3 scripts/agreement/status.py --plain`

---

## Hub hygiene

| Item | Status | Blocker |
| --- | --- | --- |
| Drive folders 16–20 + STRUCTURE TBD | **DONE (2026-10-06)** | — packet A closed; URLs in [`STRUCTURE.md`](../STRUCTURE.md) |
| `memory/` vs `00_MEMORY/` naming | **Interim documented** (keep both) | Optional Crystal stamp — packet B |
| Stubs / UK-MonoRepo / auth-blocked CrystalCore* | **GONE (live)** | Confirm — packet C |
| Cross-domain thread extracts | **DONE (hub)** | Satellite execution remains |

---

## Gates needing Crystal

| Gate | Blocker |
| --- | --- |
| Confirm GONE repos intentional | Packet C |
| Stamp naming option 1/2/3 | Packet B (option 1 already documented) |
| Delete 20 `archive/` source repos | [`../memory/repo-deletion-checklist.md`](../memory/repo-deletion-checklist.md) |
| Domain steward appointments | [`../MAINTAINERS.md`](../MAINTAINERS.md) TBD |

---

## Research threads 1–5

Hub extracts filed. Next work is **satellite** (swarm / MiroShark / mars / Lean), not this hub.

---

## Archive / product leftovers

- **ukf-tracklist** — awaiting real `data/tracklist.csv`
- **CrystalCore `/generate`** — live cloud / WebLLM / pytest still open in `archive/`
- **Celestial Portal** — zip A still missing; drawer README refreshed 2026-09-18
- **99 quartz** — speculation only

---

## Suggested remaining pick order

1. Crystal: confirm packet C  
2. Crystal: stamp packet B if rename wanted  
3. Satellite Thread execution / supply Portal zip A / ukf CSV

# Open backlog (hub coordination)

**Canon:** **no**  
**Updated:** 2026-09-18 (decision packets; stubs/UK gone on live list)  
**Role:** Single list of what remains open. Not a parallel task tracker — IDs live in [`WORKING-INDEX.md`](WORKING-INDEX.md).  
**Decision packets:** [`CRYSTAL-DECISIONS-PENDING.md`](CRYSTAL-DECISIONS-PENDING.md)

**Pick rule:** Agent connection work without Crystal/Drive = done for threads. Remaining hub items need Crystal stamp or Drive.

---

## Hub hygiene

| Item | Status | Blocker |
| --- | --- | --- |
| Drive folders 16–20 + replace `TBD` in STRUCTURE | OPEN | Crystal + Drive — see packet A |
| `memory/` vs `00_MEMORY/` naming | OPEN | Crystal — see packet B |
| Stub repos `jolly-bolt-flora-lotus`, `pilot-horizon-acre-spring` | **GONE (live)** | Confirm intentional — packet C |
| `UK-MonoRepo` | **GONE (live)** | Confirm intentional — packet C |
| Cross-domain thread extracts | **DONE (hub)** | Satellite execution remains |

Done (do not redo): REPOS baseline, Continuum vision-only, SECURITY Advisories, science INDEX URLs, Connected System, Threads 1–5 extracts, decision packets.

---

## Gates needing Crystal (do not auto-execute)

| Gate | Blocker |
| --- | --- |
| Confirm stubs + UK-MonoRepo gone | Packet C yes/no |
| Drive 16–20 create + STRUCTURE links | Packet A |
| `memory/` naming option 1/2/3 | Packet B |
| Delete 20 original source repos after subtree import | [`../memory/repo-deletion-checklist.md`](../memory/repo-deletion-checklist.md) |
| Import 4 auth-blocked private repos (if they still exist) | Credentials; re-check live list |
| Domain steward appointments | [`../MAINTAINERS.md`](../MAINTAINERS.md) TBD |

---

## Research / science threads

| # | Thread | Hub status | Next (outside hub) |
| --- | --- | --- | --- |
| 1 | Governance under scarcity | Extract filed | Port GTB params to mars-cybertruck |
| 2 | Coalition detection + Lean | Stub extract | Combined detector + proof |
| 3 | Axiom grounding | Mapping + extract | SWARM/GTB audit actions |
| 4 | LLM calibration in markets | Extract filed | Finish rubric_v1; correct `yes_probability` |
| 5 | Soft-label math certification | Extract filed | Lean: `p ∈ [0,1]` |

---

## Archive / product leftovers

- **ukf-tracklist** — awaiting real `data/tracklist.csv`
- **CrystalCore `/generate`** — cloud untested live; WebLLM not implemented; pytest needs real run
- **Celestial Portal handoff** — partial; original zip A still on phone / Drive 07
- **99 quartz timeline** — speculation only

---

## Suggested remaining pick order

1. Crystal: confirm packet C (stubs/UK)  
2. Crystal: Drive 16–20 (packet A)  
3. Crystal: naming (packet B)  
4. Satellite Thread execution (outside hub)

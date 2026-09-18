# Crystal decisions pending (hub packets)

**Canon:** **no**  
**Updated:** 2026-09-18  
**Role:** Decision packets only — agents do **not** execute Drive creates, deletes, or renames. Crystal stamps / acts.  
**Related:** [`OPEN-BACKLOG.md`](OPEN-BACKLOG.md), [`WORKING-INDEX.md`](WORKING-INDEX.md)

---

## A. Drive folders 16–20 (OPEN)

[`STRUCTURE.md`](../STRUCTURE.md) still has `TBD` Drive folder links for drawers 16–20. Repo drawers already exist with INDEX pointers.

### What Crystal does in Drive

Under Drive root `1mc0RvTCg3d94WcYIot2pLKoiHQb8nBnX` (same as other CVSC drawers), create five folders named exactly:

| Folder name | Matches repo path |
| --- | --- |
| `16_AI_SAFETY_RESEARCH` | `/16_AI_SAFETY_RESEARCH/` |
| `17_PHYSICS_SIMULATION` | `/17_PHYSICS_SIMULATION/` |
| `18_MATHEMATICAL_FOUNDATIONS` | `/18_MATHEMATICAL_FOUNDATIONS/` |
| `19_PHILOSOPHICAL_FOUNDATIONS` | `/19_PHILOSOPHICAL_FOUNDATIONS/` |
| `20_ECONOMIC_MODELS` | `/20_ECONOMIC_MODELS/` |

### After create — paste back

1. Copy each folder’s Drive URL.  
2. Replace the five `TBD` cells in [`STRUCTURE.md`](../STRUCTURE.md) (rows 16–20).  
3. Optional: drop a one-line `README` in each Drive folder: “Staging for drawer N; Canon = Crystal stamp; GitHub = kept trail.”  
4. Do **not** dump satellite git trees into Drive — pointers + extracts only (Connection ≠ merge).

### Agent note

Google Drive MCP for this session is **unauthenticated**. No agent pass can complete A without Crystal (or Drive auth + explicit yes).

---

## B. `memory/` vs `00_MEMORY/` naming (OPEN)

| Path | What it holds today |
| --- | --- |
| [`00_MEMORY/`](../00_MEMORY/) | Cross-domain research: status, threads, axiom audit, Thread 1–5 extracts |
| [`memory/`](../memory/) | Monorepo protocol: CORE, DECISIONS, MILESTONES, OPEN-QUESTIONS, PRIVACY, deletion checklist |

[`STRUCTURE.md`](../STRUCTURE.md) maps drawer **00_MEMORY** → `` `00_MEMORY/` ``. Protocol files under `memory/` predate that mapping (logged in [`../memory/OPEN-QUESTIONS.md`](../memory/OPEN-QUESTIONS.md)).

### Options for Crystal (pick one)

1. **Keep both (recommended default until stamp)** — Document dual role: `00_MEMORY` = science coordination; `memory/` = hub protocol. No rename. Update STRUCTURE note to say both are intentional.  
2. **Move protocol into `00_MEMORY/protocol/`** — Single drawer root; update all links.  
3. **Rename `memory/` → something outside drawers** — e.g. keep as repo meta only; STRUCTURE stays `00_MEMORY` for research.

Silence is not permission — do not rename until Crystal picks.

---

## C. Stub repos + UK-MonoRepo (CLOSED on live inventory — confirm)

Live `gh repo list CrystalArchitect` (2026-09-18): **65** repos, **0** private.

| Name (2026-09-16 inventory) | Live status 2026-09-18 |
| --- | --- |
| `jolly-bolt-flora-lotus` | **Not found** (absent from list + API 404) |
| `pilot-horizon-acre-spring` | **Not found** |
| `UK-MonoRepo` | **Not found** |

**Implication:** Prior “delete or adopt” / “keep private” gates appear **already resolved outside this hub** (deleted or never visible to current token).  

**Crystal confirm:** Reply yes if deletion was intentional. If any of these should still exist, restore from backup / GitHub support — hub cannot recover them.

Until confirmed, hub docs mark these rows **GONE (live)** rather than OPEN for agent action. Still **do not** invent recreated stub repos.

---

## D. Domain stewards (OPEN — appointments only)

[`MAINTAINERS.md`](../MAINTAINERS.md) drawers 16–20 + Product remain TBD. Crystal names stewards; agents do not invent them.

---

## E. Still not agent work here

- Satellite Thread 1–5 experiments (swarm / MiroShark / mars / Lean)
- Import of formerly auth-blocked private CrystalCore* trees (credentials)
- Per-repo deletion of the 20 `archive/` sources ([`../memory/repo-deletion-checklist.md`](../memory/repo-deletion-checklist.md))
- Drive MCP auth without Crystal request

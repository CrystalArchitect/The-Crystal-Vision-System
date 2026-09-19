# Crystal decisions pending (hub packets)

**Canon:** **no**  
**Updated:** 2026-09-19  
**Role:** Decision packets only — agents do **not** execute Drive creates, deletes, or renames. Crystal stamps / acts.  
**Related:** [`OPEN-BACKLOG.md`](OPEN-BACKLOG.md), [`WORKING-INDEX.md`](WORKING-INDEX.md), [`MEMORYCORE-ARCHITECTURE-TRUTHCHECK-2026-09-19.md`](MEMORYCORE-ARCHITECTURE-TRUTHCHECK-2026-09-19.md)

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

Google Drive MCP auth **timed out** in the 2026-09-18 agent session that tried. No agent pass can complete A without Crystal (or successful Drive auth + explicit yes to create).

---

## B. `memory/` vs `00_MEMORY/` naming (INTERIM DOCUMENTED)

| Path | What it holds today |
| --- | --- |
| [`00_MEMORY/`](../00_MEMORY/) | Cross-domain research: status, threads, axiom audit, Thread 1–5 extracts |
| [`memory/`](../memory/) | Monorepo protocol: CORE, DECISIONS, MILESTONES, OPEN-QUESTIONS, PRIVACY |

[`STRUCTURE.md`](../STRUCTURE.md) now notes both. READMEs in each path cross-link.

### Options for Crystal (pick one to stamp)

1. **Keep both (current interim)** — Dual role documented; no rename.  
2. **Move protocol into `00_MEMORY/protocol/`** — Single drawer root; update all links.  
3. **Rename `memory/` → something outside drawers** — e.g. keep as repo meta only.

Silence is not permission for options 2–3 — do not rename until Crystal picks. Option 1 is live as documentation only (Canon: no).

---

## C. Stub repos + UK-MonoRepo + former auth-blocked privates (GONE on live — confirm)

Live `gh repo list CrystalArchitect` (2026-09-18): **65** repos, **0** private.

| Name (earlier inventory / open questions) | Live status 2026-09-18 |
| --- | --- |
| `jolly-bolt-flora-lotus` | **Not found** |
| `pilot-horizon-acre-spring` | **Not found** |
| `UK-MonoRepo` | **Not found** |
| `CrystalCore.OS-Aeris-Vault12` | **Not found** |
| `CrystalCore-AERIS` | **Not found** |
| `CrystalCore` | **Not found** |
| `TerAustralis-Incognita-` (trailing hyphen) | **Not found** |

**Implication:** Stub/UK “delete or adopt” and “import auth-blocked privates” gates are **not actionable** on live inventory.  

**Crystal confirm:** Reply yes if absence was intentional. Hub cannot restore deleted repos.

Until confirmed, hub docs mark these **GONE (live)**. Do not invent recreated stubs or private imports.

---

## D. Domain stewards (OPEN — appointments only)

[`MAINTAINERS.md`](../MAINTAINERS.md) drawers 16–20 + Product remain TBD. Crystal names stewards; agents do not invent them.

---

## E. MemoryCore vs local-first CrystalCore (OPEN — stamp required)

**Discrepancy:** Cloud MemoryCore (Supabase vault + cloud-engine packaging) ≠ canonical local-first Clementine / CrystalCore / Consent Transport.

Full truth-check: [`MEMORYCORE-ARCHITECTURE-TRUTHCHECK-2026-09-19.md`](MEMORYCORE-ARCHITECTURE-TRUTHCHECK-2026-09-19.md).

| Option | Meaning |
| --- | --- |
| **E1** | Separate tracks (hub interim): Track A = local-first companion; Track B = optional archive vault |
| **E2** | Vault local-first / AU-sovereign only — retire Supabase path |
| **E3** | Deprecate cloud MemoryCore; companion memory stays Track A only |
| **E4** | Elevate Track B as canonical *archive* (still not the companion runtime) |

Agents operate as **E1** until Crystal stamps. Do not rebuild or delete either track without stamp. AU/Indigenous/family data must not use US Supabase (AI-SYSTEM-BRIEF §8).

---

## F. Still not agent work here

- Satellite Thread 1–5 experiments (swarm / MiroShark / mars / Lean)
- Import of formerly auth-blocked private CrystalCore* trees (credentials)
- Per-repo deletion of the 20 `archive/` sources ([`../memory/repo-deletion-checklist.md`](../memory/repo-deletion-checklist.md))
- Drive MCP auth without Crystal request
- Further cloud MemoryCore deploys until packet **E** is stamped
- Portal Nag Hammadi BookItem PRs into foreign `/home/claude/...` trees from this hub without Crystal directing the Portal repo
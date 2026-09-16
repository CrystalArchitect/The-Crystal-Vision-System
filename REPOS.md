# Repository Inventory — CrystalArchitect ↔ Crystal Vision System

**Date:** 2026-09-16 AEST (Australia/Sydney)  
**Owner:** Crystal Arena-Turner (CrystalArchitect)  
**Scope:** Live account inventory + drawer mapping for [The-Crystal-Vision-System](https://github.com/CrystalArchitect/The-Crystal-Vision-System)  
**Canon:** **no** — coordination only. **Canon = Crystal stamp.**  
**Rule:** **Connection ≠ merge.** Drawers point at satellites; satellites are not living code inside CVS.

Sources: `gh repo list CrystalArchitect --limit 100` (58 repos); `00_MASTER_INDEX/CONNECTED-SYSTEM.md`.

---

## Hub

| Repo | Visibility | License | Role |
| --- | --- | --- | --- |
| [The-Crystal-Vision-System](https://github.com/CrystalArchitect/The-Crystal-Vision-System) | **public** | MIT | Coordination hub: drawers `00–20` + `99`, working index, memory, Protocol Omega (in-hub), science pointers |

---

## Originals (non-forks)

| Repo | Visibility | Status | Notes |
| --- | --- | --- | --- |
| [The-Crystal-Vision-System](https://github.com/CrystalArchitect/The-Crystal-Vision-System) | public | **active hub** | Filing / kept trail |
| [crystalcore-os](https://github.com/CrystalArchitect/crystalcore-os) | public | **original** | Product / OS stack → drawer **01_CRYSTALCORE** |
| [Continuum-sync-loop](https://github.com/CrystalArchitect/Continuum-sync-loop) | public | **empty** (size 0) | Satellite for drawer **06**; vision-only until first commit |
| [Antimemetics-division](https://github.com/CrystalArchitect/Antimemetics-division) | public | original | Outside science drawers; portfolio original |
| [UK-MonoRepo](https://github.com/CrystalArchitect/UK-MonoRepo) | **private** | private original | Do **not** open / merge into public CVS |
| [jolly-bolt-flora-lotus](https://github.com/CrystalArchitect/jolly-bolt-flora-lotus) | **private** | **stub** | Grok template; **Crystal decision:** delete or adopt — **do not delete in this pass** |
| [pilot-horizon-acre-spring](https://github.com/CrystalArchitect/pilot-horizon-acre-spring) | **private** | **stub** | Grok template; **Crystal decision:** delete or adopt — **do not delete in this pass** |

---

## Drawer-linked satellites (16–20 + product)

Labels: **fork-mirror** = CrystalArchitect fork of upstream (pointer only).

### Product — 01_CRYSTALCORE

| Repo | Label | URL |
| --- | --- | --- |
| crystalcore-os | original | https://github.com/CrystalArchitect/crystalcore-os |

### 16_AI_SAFETY_RESEARCH

| Repo | Label | Upstream (parent) | URL |
| --- | --- | --- | --- |
| swarm | fork-mirror | swarm-ai-research/swarm | https://github.com/CrystalArchitect/swarm |
| swarm-artifacts | fork-mirror | swarm-ai-research/swarm-artifacts | https://github.com/CrystalArchitect/swarm-artifacts |
| swarm-safety-gate | fork-mirror | swarm-ai-research/swarm-safety-gate | https://github.com/CrystalArchitect/swarm-safety-gate |
| swarmgym | fork-mirror | swarm-ai-research/swarmgym | https://github.com/CrystalArchitect/swarmgym |
| agency-os | fork-mirror | swarm-ai-research/agency-os | https://github.com/CrystalArchitect/agency-os |
| automaton | fork-mirror | Conway-Research/automaton | https://github.com/CrystalArchitect/automaton |
| aeon | fork-mirror (related) | swarm-ai-research/aeon | https://github.com/CrystalArchitect/aeon |
| aeon-atlas | fork-mirror (related) | swarm-ai-research/aeon-atlas | https://github.com/CrystalArchitect/aeon-atlas |

### 17_PHYSICS_SIMULATION

| Repo | Label | Upstream | URL |
| --- | --- | --- | --- |
| mars-cybertruck-sim | fork-mirror | xfreeze2/mars-cybertruck-sim | https://github.com/CrystalArchitect/mars-cybertruck-sim |

### 18_MATHEMATICAL_FOUNDATIONS

| Repo | Label | Upstream | URL |
| --- | --- | --- | --- |
| navier-stokes-lean-check | fork-mirror | swarm-ai-research/navier-stokes-lean-check | https://github.com/CrystalArchitect/navier-stokes-lean-check |
| circle-squaring | fork-mirror | swarm-ai-research/circle-squaring | https://github.com/CrystalArchitect/circle-squaring |

### 19_PHILOSOPHICAL_FOUNDATIONS

| Repo | Label | Upstream | URL |
| --- | --- | --- | --- |
| AI-Foundations-Introduction | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Introduction |
| AI-Foundations-Ontology | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Ontology |
| AI-Foundations-Claims-Map | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Claims-Map |
| AI-Foundations-Axiom-Evaluation-Harness | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Axiom-Evaluation-Harness |
| AI-Foundations-Claim-001-Origin | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Claim-001-Origin |
| AI-Foundations-Claim-002-Belonging-does-not-equal-Sameness | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Claim-002-Belonging-does-not-equal-Sameness |
| AI-Foundations-Claim-003-Irreversibility-of-Being | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Claim-003-Irreversibility-of-Being |
| AI-Foundations-Emergence-Continuity | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Emergence-Continuity |
| AI-Foundations-Source-Trace-Irreversibility | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-Source-Trace-Irreversibility |
| AI-Foundations-ai-artwork-provenance | fork-mirror | alyssadata/… | https://github.com/CrystalArchitect/AI-Foundations-ai-artwork-provenance |
| Consciousness-Is-Subjectivity | fork-mirror | alyssadata/Consciousness-Is-Subjectivity | https://github.com/CrystalArchitect/Consciousness-Is-Subjectivity |

### 20_ECONOMIC_MODELS

| Repo | Label | Upstream | URL |
| --- | --- | --- | --- |
| MiroShark | fork-mirror | swarm-ai-research/MiroShark | https://github.com/CrystalArchitect/MiroShark |

---

## Design-only

| Repo | Label | URL | Note |
| --- | --- | --- | --- |
| [api-gateway](https://github.com/CrystalArchitect/api-gateway) | fork-mirror · **design-only** | https://github.com/CrystalArchitect/api-gateway | Portfolio design narrative (README + governance templates); **not** integrated into CVS. Upstream: chrisdwil/api-gateway |

---

## Empty / vision-only

| Repo | Drawer | Status |
| --- | --- | --- |
| [Continuum-sync-loop](https://github.com/CrystalArchitect/Continuum-sync-loop) | **06_CMX_CONTINUUM** | Empty repo. Continuum **intent** lives in CVS drawer 06 (vision-only marker). No merge. Seed README optional; first real commit is Crystal’s call. |

---

## Private (flag only — no delete in this doc)

| Repo | Status | Crystal decision needed |
| --- | --- | --- |
| UK-MonoRepo | private original | Keep private; do not publish / pull into public CVS until opened |
| jolly-bolt-flora-lotus | private stub | Delete **or** adopt — **do not delete here**; flag only |
| pilot-horizon-acre-spring | private stub | Delete **or** adopt — **do not delete here**; flag only |

---

## Fork inventory summary

| Metric | Count |
| --- | --- |
| Total repos | **58** |
| Public / private | **55** / **3** |
| Forks / originals | **51** / **7** |
| Archived | **0** |

Most of drawers **16–19** point at **fork-mirrors**, not Crystal-origin research trees.

---

## Protocol Omega

| Field | Value |
| --- | --- |
| Placement | **In-hub only:** `10_ORIGINAL_CREATIVE/protocol-omega/` |
| Standalone CrystalArchitect repo | **None** |
| Role | Personal boundaries practice tool (HTML + localStorage) |
| Canon | **no** — not a research claim; not a science-drawer deliverable |

---

## Explicit rules

1. **Connection ≠ merge** — indexing a satellite in a drawer does not merge its code into CVS.  
2. **Canon = Crystal stamp** — presence in git ≠ Canon.  
3. `archive/` subtrees under CVS = file custody of older trees, not living authority.  
4. Do not invent a Protocol Omega research repo.  
5. Do not make UK-MonoRepo public from this inventory refresh.

*Non Solus.*

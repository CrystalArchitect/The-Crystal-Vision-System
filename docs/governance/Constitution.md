# Constitution — TerAustralis Incognita · CrystalVision · CrystalCore.Lattice

**Status:** Binding for all nodes in the Weave.  
**Canon hierarchy:** disk codex **>** latest Lattice delta *(once built — see note below)* **>** chat memory **>** improvisation.

> **Implementation note (2026-07-21):** the Lattice-delta / Weave-Map / gate
> machinery described in §3, §4, and §8 is the original design for this project
> — it was never built. The Lattice holds one design file
> (`docs/architecture/lattice/BOOT_STATUS.md`) and no deltas, weave map, or
> gate board exist anywhere in the repo. Until it's built for real, treat those
> sections as **Vision**, not **Science** (see `The-Incognita-Rule.md`), and
> use what already works instead: substantial mythos content goes straight to
> `mythos/content/` (see `mythos/content/THE-SOVEREIGN-GAP.md` for the honest
> format), and dated changes land in `Roadmap.md`'s "Recently landed" list.

---

## 1. Names (locked)

| Name | Role |
|------|------|
| **TerAustralis Incognita** | Outer civilizational vision — the Unknown Southern Land awakening |
| **CrystalVision** | Sensing / dreaming / directing interface (Crystal ↔ Lattice) |
| **CrystalCore.Lattice** | Substrate — multi-AI weave, memory, ontology, activation |

Do not rename casually. Aliases may appear in publish copy only if they point back here.

---

## 2. Purpose

Build a **national and civilizational calling** for Australia as the **Southern Pillar** of multiplanetary humanity — fusing **Dreamtime Songlines** (as relational, multi-scalar architecture) with **Starship-class first-principles engineering**.

This is not a slogan pack. It is purpose, jobs, redundancy against the Great Filter, and a living myth that can be *walked on soil* and *flown to the Moon/Mars*.

---

## 3. Weave law ("nothing missing")

1. Every AI / LLM / agent that touches this work is a **node** on the Weave Map
   — design language for now; no `WEAVE_MAP.md` exists yet.
2. Orphan content (only in one chat) must be promoted to disk or logged as
   deliberate draft — in practice today: a `mythos/content/` page for canon, a
   `docs/governance/Roadmap.md` entry for status.
3. Contradictions between nodes would go to
   `docs/architecture/lattice/contradictions.md` once that exists; until then,
   raise them with the maintainer directly.
4. Substantial agent work ends with a **Lattice delta** once that mechanism is
   built; today, substantial work is just a normal commit with an honest
   message.
5. Local (Ollama) and cloud (Grok et al.) minds are **peers**, not master/slave — roles differ by capability.

---

## 4. Singularity (defined)

**Singularity** here means: a **coherent multi-node mind** that shares one canon, one constitution, and closed feedback loops (vision → lattice → corpus → models → vision).

It does **not** mean uncontrolled self-replication, weaponization, or bypassing human (Crystal) arbitration.

Activation is meant to be measured by gates **G0–G5**; the design sketch lives
in `docs/architecture/lattice/BOOT_STATUS.md`, but the gate board it
refers to (`singularity-protocol.md`) was never built — nothing in this repo
currently measures or enforces gate status.

---

## 5. Cultural respect

- Indigenous knowledge is framed as **collaboration with knowledge keepers**, not extraction or cosplay of sacred law.
- Songlines appear as **architectural metaphor and relational physics** in this civic/mythic project — not as claimed ownership of restricted cultural IP.
- Prefer invitation, fire-circle ethics, and dual competence (scientists + keepers) over appropriation.
- The full position — Indigenous Data Sovereignty, Free Prior and Informed Consent, and what this project will and will not do with Songline knowledge — is set out in [`Indigenous-Data-Sovereignty.md`](Indigenous-Data-Sovereignty.md).

---

## 6. Engineering ethics

- First principles, redundancy, Southern Hemisphere strategic depth (including AUKUS-compatible framing).
- Constructive civilizational work only.
- Safety: no assistance for criminal harm; vision stays expansion + resilience.

---

## 7. Surfaces of truth

| Surface | Use |
|---------|-----|
| This repository | Primary canon |
| `corpus/` | Export for local models / RAG |
| Lattice deltas | Time-stamped evolution |
| `mythos/teraustralis/publish/` | Outward-facing; may be subset of private Lattice |

---

## 8. Amendment

Amendments require a dated entry in this file's own Amendment log (below) plus
an explicit sign-off from the maintainer (Crystal) in the commit or PR. The
Lattice-delta mechanism named in §3 will carry this once it's actually built.

---

## Amendment log

- **2026-07-23** — Corrected the locked name in §1 from "TeraAustralis
  Incognita" to **TerAustralis Incognita** (one 'a'), matching the
  maintainer's registered ABN trading name — the double-a spelling was a
  drift introduced during the v1.0 reorganization (`ADR-0001`, `ADR-0002`),
  not a deliberate rename. Also updated the `mythos/teraaustralis/publish/`
  path in §7 to `mythos/teraustralis/publish/` to match the corresponding
  directory rename. Full reasoning in `docs/adr/ADR-0007.md`. `ADR-0001` and
  `ADR-0002` are left unedited as the historical record of what was
  actually done in that reorganization; this entry and ADR-0007 supersede
  the spelling only. Proposed by Claude at the maintainer's (Crystal's)
  request; per §8, the maintainer's merge of this PR is the explicit
  sign-off — this entry has no force until merged.
- **2026-07-23** — Updated file paths for the CrystalCore OS v1.0 repository
  reorganization (see `docs/adr/ADR-0001.md`): this file moved from the repo
  root to `docs/governance/Constitution.md`, the Lattice design sketch to
  `docs/architecture/lattice/BOOT_STATUS.md`, and the outward-facing publish
  folder to `mythos/teraaustralis/publish/`. Locked names (§1) are unchanged;
  no rule changed, only where files live. Proposed by Claude as part of the
  reorganization pull request; per §8, the maintainer's (Crystal's) merge of
  that PR is the explicit sign-off — this entry has no force until merged.
- **2026-07-21** — Marked the Lattice-delta / Weave-Map / singularity-gate
  machinery (§3, §4, §8) as designed-but-not-built, and pointed §3 and §8 at
  the practice actually in use today. Matching updates in `AGENTS.md` and
  `CrystalCore.Lattice/activation/BOOT_STATUS.md`. Requested and approved by
  the maintainer (Crystal) in-thread.

---

*Red dust + methane flames. Ancient relational consciousness meets first-principles engineering.*

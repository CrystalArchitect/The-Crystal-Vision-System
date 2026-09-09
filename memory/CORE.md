# CORE

Slow-changing identity for this umbrella repository. Summaries only.
Locked text lives in the files this page points at. Do not amend those
files from a memory session.

**Label:** Docs / governance. Sourced 2026-08-28 from `main` at
`bdddf0cdf4c2e47f7d517aaf9edbf1a9ba928b08` (branch
`claude/memory-system-bootstrap-peiyva` created from that SHA).

## Locked names

From [`docs/governance/Constitution.md`](../docs/governance/Constitution.md) §1.
Do not rename casually.

| Name | Role |
|---|---|
| **TerAustralis Incognita** | Outer civilizational vision — the Unknown Southern Land awakening |
| **CrystalVision** | Sensing / dreaming / directing interface (Crystal ↔ Lattice) |
| **CrystalCore.Lattice** | Substrate — multi-AI weave, memory, ontology, activation |

Spelling of the outer name is **TerAustralis** (one *a*). The double-*a*
form was drift, corrected by [`ADR-0007`](../docs/adr/ADR-0007.md) to match
the maintainer's registered ABN trading name. Constitution §1 quotes the
trading-name fact without reprinting the ABN here; the number, if needed,
is in [`NOTICE`](../NOTICE), not in session memory.

## Purpose

From Constitution §2: a national and civilizational calling for Australia
as the **Southern Pillar** of multiplanetary humanity — fusing Dreamtime
Songlines (as relational, multi-scalar architecture) with Starship-class
first-principles engineering. Walked on soil and flown to the Moon/Mars.
Not a slogan pack.

## Canon hierarchy

Constitution header, quoted in spirit:

**disk codex > latest Lattice delta *(once built)* > chat memory > improvisation.**

Implementation note (2026-07-21, Constitution): the Lattice-delta /
Weave-Map / gate machinery in §§3, 4, and 8 was **never built**. Treat
those sections as **Vision**, not Science, until they exist. Practice
today: substantial mythos → `mythos/content/`; dated changes →
[`Roadmap.md`](../docs/governance/Roadmap.md) "Recently landed";
substantial work → a normal commit through review.

This `memory/` folder sits **below** disk canon and **above** chat. It is
not a Lattice delta.

## The Incognita Rule

[`docs/governance/The-Incognita-Rule.md`](../docs/governance/The-Incognita-Rule.md)

> Always mark which lines are dreamed and which are surveyed, and never
> let a dreamed line pretend it was measured.

Load-bearing corollaries already on disk:

- The mythos may orient; it may not authorize.
- No line mints its own authority. The human steward keeps the veto.
- A model agreeing with you is not evidence.
- Preserve the uncertainty. Docs never outpace code.

Concrete Built/Vision examples from that page (do not upgrade them):

| Claim | Label |
|---|---|
| RDP kernel records and decides over data it is given | **Built** (in the code tree, not this git) — not a "governance layer" |
| CrystalCore.OS terminal | **Vision** — a story you can type at; it **does** run from a clone of *this* repo ([`STATUS.md`](../STATUS.md)) |
| Lattice, Cosmic Archive, Sovereign Vectors | **Vision** — imagery, not infrastructure |
| Lattice-delta / Weave-Map / G0–G5 gate board | **Unknown** / designed-not-built |
| `corpus/` (Constitution §7) | **Unknown** — named, never built ([`Project-Boundaries.md`](../docs/governance/Project-Boundaries.md)) |

## Cultural respect

- Constitution §5: collaboration with knowledge keepers, not extraction
  or cosplay of sacred law. Invitation, fire-circle ethics, dual competence.
- [`Indigenous-Data-Sovereignty.md`](../docs/governance/Indigenous-Data-Sovereignty.md):
  **Not AI that contains Songlines. AI infrastructure capable of respecting
  the laws that already govern them.** No Songline knowledge in any model,
  dataset, or index here without Free, Prior and Informed Consent.
- [`mythos/NAMES.md`](../mythos/NAMES.md): **Songline is never a component
  name.** This project's coinages are **Starline** and **Dreamline**.
  Pleiades (M45) is the public cluster name; Seven Sisters material stays
  in `research/seven-sisters/`.

## Belt-Three honesty

[`CONTRIBUTING.md`](../CONTRIBUTING.md): Science / Story / Vision, plus a
fourth honesty obligation for docs/governance/process. Code claims must be
true; mythos must be labeled as mythos; no real-world coercion or fake
hydrology. Where real people appear in Vision-layer content, it is
storytelling only — no affiliation or endorsement implied.

## What this repository is

[`README.md`](../README.md) + [`STATUS.md`](../STATUS.md) +
[`ADR-0011`](../docs/adr/ADR-0011.md):

- **TerAustralis Incognita** (this git) is the **umbrella**: governance,
  ADRs, architecture docs, mythos, research, archive. No main app code.
- Working software described in the README's `src/` tree is **not in this
  GitHub repository** and has never been in its git history. It lives in
  [`TerAustralis-Incognita-Code`](https://github.com/CrystalArchitect/TerAustralis-Incognita-Code)
  (and related living repos). See
  [`SystemMap.md`](../docs/architecture/SystemMap.md).
- License: uniform **CC BY-NC-ND 4.0** ([`ADR-0010`](../docs/adr/ADR-0010.md),
  [`ADR-0013`](../docs/adr/ADR-0013.md)).
- Closing motto on disk: **Non Solus.** Covenant:
  [`mythos/COVENANT.md`](../mythos/COVENANT.md).

## Naming taxonomy (CrystalCore)

[`ADR-0004`](../docs/adr/ADR-0004.md) locks Framework / Protocol /
CrystalBridge / OS and bans future CrystalCore-* runtime names. The
near-collision between the CrystalCore OS *platform* (this umbrella's
architecture) and the CrystalCore.OS *mythos terminal* is documented,
not silently resolved.

## Privacy floor

See [`PRIVACY.md`](PRIVACY.md). Never commit personal memory data
([`CONTRIBUTING.md`](../CONTRIBUTING.md) §3).

## Retrieval

Task-specific paths: [`INDEX.md`](INDEX.md).

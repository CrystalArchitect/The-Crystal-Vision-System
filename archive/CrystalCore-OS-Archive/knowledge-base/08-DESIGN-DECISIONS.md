# Design Decisions

Consolidated ADR rationale — for each major decision, *why*, not just
what and when. `04-GOVERNANCE.md` has the full table; this document is
the narrative behind the four entries that carry the most weight.

## The licensing chain (ADR-0006 → 0008 → 0009 → 0010)

### Statement
Four ADRs touched the code license in a single day, each responding to
a real, uncoordinated collision rather than a planned sequence:

- **ADR-0006** made the first, considered choice: keep the original
  Apache-2.0 (code) / CC BY-NC-ND 4.0 (content) dual-license split, an
  "open-core" trade-off, and recorded six IP principles alongside it.
- Before that choice could take effect, **an uncoordinated session had
  already flipped the root `LICENSE` file to CC BY-NC-ND 4.0 "for
  commercial exclusivity."** **ADR-0008** formally records that
  as the actual direction (rather than silently overriding it or
  reverting it), and does the cleanup: verifies no third-party
  relicensing-consent gap exists (only two authors — the maintainer and
  Claude — have ever committed, per direct `git log` check), and fixes
  roughly 15 files still claiming Apache-2.0.
- A second, independent collision followed: **97 stale Apache-2.0 SPDX
  headers** left over from a third uncoordinated session, plus a
  `packages/` restructuring from a fourth actor that introduced *four
  more* different licenses (AGPL v3, Proprietary, MIT-dual, CC BY-NC-ND)
  across different packages. **ADR-0009** reconciles this: rules that
  root `LICENSE` (CC BY-NC-ND) governs `src/` and `mythos/` *today*,
  explicitly leaves `packages/`'s differentiated licensing as a real but
  not-yet-decided target, and batch-fixes the 97 stale headers.
- **ADR-0010** closes the question ADR-0009 left open, and is the
  chain's terminus: uniform CC BY-NC-ND 4.0 across the *entire*
  repository, `packages/` included — rejecting the four-way
  differentiated model outright. The stated reasoning: "four parallel
  license regimes are real, ongoing operational overhead... for
  protection that isn't needed yet," for a project that is
  pre-revenue and has exactly one maintainer.

**Status: Implemented** (ADR-0010 is the current, operative decision).

### Evidence
`docs/adr/ADR-0006.md` through `ADR-0010.md`, each read in full.

### Historical Notes
The rejected differentiated-licensing model was not merely a proposal
on paper — it has a concrete, surviving implementation: see
`04-GOVERNANCE.md` and `07-HISTORY.md` for the abandoned `packages/`
tree on `TerAustralis-Incognita-Code`'s PR #1 branch, which is exactly
what this rejected model looked like in practice.

### Cross References
`04-GOVERNANCE.md`, `07-HISTORY.md`.

---

## The three-project boundary model (ADR-0011)

### Statement
ADR-0011 establishes that the codebase should split across three
projects — an umbrella (canon, governance, no app code), Crystal Core
(the engine), and Crystal Vision (the user-facing application) —
reasoning that the umbrella's job (canon and law) and the engineering
projects' job (running software) are different enough in kind, pace,
and audience that keeping them in one repository was starting to blur
a boundary the project considered worth keeping sharp. The ADR itself
executed nothing — it names `TerAustralis-Incognita-Code` as reserved
by charter for the engineering side, and explicitly lists what it
decided *not* to do: no renames, no moves, no new repos, no workflow
changes, at the moment of the ADR's own acceptance. The actual code
migration is a separate, staged, individually-approvable proposal
(`Migration-Plan.md`).

**Status: Implemented** (Stages 0–2 of the migration plan this ADR
authorized have since executed; Stages 3–4 remain pending, per the
project's own open decisions — see `04-GOVERNANCE.md`).

### Evidence
`docs/adr/ADR-0011.md`, read in full; `docs/governance/Migration-
Plan.md`, read in full.

### Historical Notes
None.

### Cross References
`02-REPOSITORY-MAP.md`, `04-GOVERNANCE.md`.

---

## The v1.0 repository reorganization (ADR-0001)

### Statement
ADR-0001 moved code under a `src/` prefix and documentation under a
structured `docs/` tree (`vision/architecture/governance/ai/agents/
guides/adr`), reasoning that a consistent, named architecture would let
the project scale past ad-hoc file placement as more AI tools and
sessions contributed to it. It is the base layout every later ADR in
the chain builds on or against.

**Status: Historical** (as a decision, still governing) — **its `src/`
half never actually landed in the umbrella repository's git history**,
per the umbrella's own `SystemMap.md`; the layout decision is real, the
tree it describes moved to a different repository under a different
prefix (`core/`+`vision/`) at Migration-Plan Stage 1.

### Evidence
`docs/adr/ADR-0001.md`; `docs/architecture/SystemMap.md`.

### Historical Notes
This is the root of the portfolio's largest documentation-drift finding
— see `01-SYSTEM-OVERVIEW.md`.

### Cross References
`01-SYSTEM-OVERVIEW.md`, `02-REPOSITORY-MAP.md`.

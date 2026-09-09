# System Overview

What CrystalCore.OS / TerAustralis Incognita is, as it exists today.

## Statement

CrystalCore.OS / TerAustralis Incognita is a single-maintainer,
heavily AI-assisted project combining (1) a local-first AI companion and
protocol pack, (2) a governance and documentation practice built around
a strict distinction between verified fact and narrative, and (3) a
mythos — the Crystal universe — told in text and art. It spans six
GitHub repositories, one public and five private, created between
2026-07-14 and 2026-07-23, with the overwhelming majority of structural
and architectural work landing on a single day, 2026-07-23.

**Status: Implemented** (the project exists and has running, tested
code) **and Designed and Vision, layered** (much of what the project
describes is explicitly not yet built, and says so).

### Evidence
- Repository creation dates, verified via GitHub API: `The-Crystal-Vision`
  (2026-07-14T06:38:49Z, earliest), `crystal-vision` and `crystalcore`
  (2026-07-17), `TerAustralis-Incognita` (2026-07-17T12:43:01Z),
  `TerAustralis-Incognita-Code` (2026-07-23T09:07:02Z),
  `CrystalCore.OS-the-Crystal-Architecture-Archive` (2026-07-23/24).
- `TerAustralis-Incognita/README.md`: "Collective intelligence with
  individual sovereignty... 1. Working software... 2. A mythos."

### Historical Notes
The project's git history includes a documented same-day history
rewrite on 2026-07-23, used to split the umbrella repository's code out
into `TerAustralis-Incognita-Code`. Dates recorded across the portfolio
for that day are the project's own claim, not independently
re-derivable original chronology. Full detail: `07-HISTORY.md`.

### Cross References
`02-REPOSITORY-MAP.md`, `07-HISTORY.md`.

---

## Statement

Exactly four software components are documented, across the whole
portfolio, as "run and are tested today": **Lumina** (the companion),
the **Starline Weaver** (the multi-AI message bus), **Consent
Transport** (also called Starline — peer-to-peer consent-gated memory
exchange), and **CrystalBridge** (the MCP consent gate). Everything else
in the technical architecture is either a stub, a scaffold, a
specification without an implementation, a demo running on simulated
data, or Vision-layer narrative.

**Status: Implemented** (for these four, confirmed) — **the rest of the
architecture is a mix of Designed and Vision**, not a blanket "built."

### Evidence
- `TerAustralis-Incognita/docs/architecture/Overview.md`: names exactly
  these four as "run and are tested today," states the cross-cutting
  law — "nothing moves without explicit, revocable consent, and refusal
  is the default" — and lists "the dreamed edges" explicitly as Vision:
  CrystalCore.Lattice, CrystalVision (demo shells only), the mainnet
  mesh (in-process stub), the full-stack blueprint.
- `TerAustralis-Incognita-Code/STATUS.md`: confirms all four test
  suites pass on a fresh clone (`clementine.bridge` 7/7, `services`
  4/4, `rdp` 31/31, `consent_transport` 9/9), re-verified 2026-07-24.

### Historical Notes
None — this is the current, stable claim across both the umbrella's
architecture docs and the Code repo's own test-verified STATUS.md.

### Cross References
`03-ARCHITECTURE.md`, `06-COMPONENTS.md`.

---

## Statement

The project's single organizing convention, applied everywhere, is a
two-tier split between **Built** (running code, with tests a reader can
execute) and **Vision** (narrative, art, and speculative framing,
explicitly labeled as such). This split is described as "load-bearing,
not decorative."

**Status: Implemented** (the convention itself is real and consistently
applied) — though this reconstruction found one place it is applied
inconsistently: `mythos/crystalcore-os/`, see below and `06-COMPONENTS.md`.

### Evidence
- `TerAustralis-Incognita/README.md`: "This split is load-bearing, not
  decorative — see `mythos/COVENANT.md`... and
  `docs/architecture/crystal-core/STARLINE.md`... for what that
  discipline actually means in practice."
- `TerAustralis-Incognita/docs/governance/The-Incognita-Rule.md`: the
  full doctrine this split enforces (quoted in `00-INDEX.md`).

### Historical Notes
None.

### Cross References
`05-KNOWLEDGE-MODEL.md`.

---

## Statement

The single largest documentation-accuracy problem found across the
portfolio: the umbrella repository's own canonical architecture
documents (`README.md`, `docs/architecture/Overview.md`,
`docs/vision/*`, `docs/architecture/Modules.md`, and others) describe
every Built component's code as living under a `src/` prefix
(`src/apps/lumina/`, `src/crystal-core/...`, `src/crystalcore/`). That
`src/` tree has never existed in the umbrella repository's git history
on any branch, and it does not match the actual current code layout
either — the real code lives in `TerAustralis-Incognita-Code`, under
`core/` (the engine) and `vision/` (the application), not `src/`. The
umbrella's own documents were not updated when the 2026-07-23 migration
executed.

**Status: Unresolved** (as documentation debt — the underlying code is
real and running; only the path citations describing it are stale).

### Evidence
- `TerAustralis-Incognita/docs/architecture/SystemMap.md`: "None of
  these paths exist in this repository's git history on any branch
  (`git log --all -- src/` returns nothing)."
- `TerAustralis-Incognita-Code/core/README.md`: "Imported from the
  umbrella repository's branch `claude/crystalcore-boot-visual-jau1bk`
  @ `32692fd`... Directory names preserved; only the `src/` prefix
  became `core/`." (confirms the real prefix is `core/`, not `src/`)

### Historical Notes
`docs/architecture/SystemMap.md`'s own "Consequences" paragraph was
itself stale by exactly this pattern — corrected during this
reconstruction pass, 2026-07-24 (see `11-CORRECTIONS.md`). The
broader, portfolio-wide `src/` citation pattern across dozens of other
files was **not** corrected directly — too large and pervasive for a
mechanical single-session fix; documented here and in
`09-TECHNICAL-DEBT` content folded into `06-COMPONENTS.md` instead.

### Cross References
`06-COMPONENTS.md`, `11-CORRECTIONS.md`.

---

## Statement

A fully implemented, tested "Crystal Runtime" coordination layer (7
modules, 75 passing tests, 2,574 lines) was built and merged into the
umbrella repository's history on 2026-07-23 — and is absent from every
current tree in the portfolio today. Its only surviving trace anywhere
is an abandoned, never-merged pull request in `TerAustralis-Incognita-
Code`.

**Status: Historical** (it existed, verifiably, and no longer does).

### Evidence
- Commit `b09672d454d124b333abbeeb0c7265f6603c83dc` (umbrella repo,
  merged 2026-07-23T08:14:29Z via PR #43): test files literally import
  `from src.runtime.coordinator.coordinator import ...`, confirming the
  module code existed at merge time.
- `find` across both repos' current working trees: zero matches for any
  `runtime/` directory.
- `TerAustralis-Incognita-Code`, branch `claude/teraustralis-incognita-
  import-g63jm9` (PR #1, opened 2026-07-23T09:44:46Z, still open,
  never merged): contains `src/runtime/` with all 7 submodules.

### Historical Notes
Full reconstruction of this episode, with exact evidence chain:
`07-HISTORY.md`.

### Cross References
`07-HISTORY.md`, `10-PROVENANCE.md`.

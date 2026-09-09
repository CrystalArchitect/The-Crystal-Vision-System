# Changelog

Notable changes to this repository, newest first. Day-to-day status lives
in [`docs/governance/Roadmap.md`](docs/governance/Roadmap.md); this file
records the milestones.

## 2026-08-20 — Human door: GitHub + sites + Discord

Access.md was still calling this repo private and pointing at a retired
laptop path. A human collaborator was sent the public doors on X. That
is the join path. OAuth and a twentieth GitHub are not.

### Changed
- `docs/guides/Access.md` — public plant, human roster row for
  `MagisterJericoh` (no Write, no mint), refused join paths named.

## 2026-08-20 — Cybernetics of CrystalCore (VSM, identity, diet)

Beer / Ashby / second-order identity, applied to the nineteen and the
keys. Model, not a Systems Mode desktop.

### Added
- `docs/architecture/CYBERNETICS-VSM.md`

## 2026-08-20 — Ink honesty + SourceCode as external peer (ADR-0016)

Five lying surfaces from the post-#118 audit, plus a neighbor that is
not a twentieth repo.

### Added
- `docs/adr/ADR-0016.md` — `samuelsalmon3/SourceCode` is an external
  peer. No vendor, no submodule, no CrystalBridge guest until minted.
- `docs/architecture/peers/SourceCode.md` — measured card.

### Changed
- `ADR-0015` marked Accepted (merged as PR #118).
- `Project-Boundaries.md` — `-Code` is public, not private.
- `docs/guides/Access.md` — external-peer row.

## 2026-08-20 — Stop growing the constellation (ADR-0015)

Nineteen GitHub repositories under CrystalArchitect. Six archived. A v2
stalled fifteen days. SAT already has a dedicated repo. New folders have
been cheaper than finishing the old ones.

### Added
- `docs/adr/ADR-0015.md` — no new GitHub repository without an ADR;
  landing table for next work.

### Changed
- Agent instructions (Grok Build, AGENTS.md, Decision-Matrix) now name
  the gate. `Project-Boundaries.md` records the 19-count beside the
  2026-07-24 six-repo survey, which is left as written.
- `ADR-0014` marked Accepted (merged as PR #116).

## 2026-08-20 — Domain measured; clone folder and leftover Pages match the slug

The public site is not 404. `https://teraustralis.com.au` 301s to
`https://www.teraustralis.com.au/` (200, SvelteKit, from
`TerAustralis-Incognita-Code`). The GitHub slug is already one *a*
(double-*a* 301s). What still disagreed: clone instructions, the GitHub
description field, and this umbrella's leftover Jekyll Pages.

### Added
- Root `index.html` + `.nojekyll` — a pointer so
  `crystalarchitect.github.io/TerAustralis-Incognita/` is not a second
  site wearing the double-*a* description.

### Changed
- `docs/adr/ADR-0007.md` — completion note; Decision body not rewritten.
- `docs/guides/GitHub-Commit-Instructions.md` — `cd` matches `git clone`;
  banner that `src/` is not here.
- `STATUS.md` — 2026-08-20 measurement.

The GitHub About description is not in git; it was patched to one *a*
in the same pass.

## 2026-08-20 — Grok Build takes the Repository Engineer seat (ADR-0014)

Claude Code is no longer in the weave. The midstream implementer seat —
take a spec, make the tree match it, open a PR — moves to **Grok Build**.
Creative Grok (diverge, mythos, art) is a separate seat and is unchanged.
Claude's profile and agent instructions stay on disk as history. No locked
name changed. No new repository.

### Added
- `docs/adr/ADR-0014.md` — the seat swap, including the sandbox-is-not-the-estate rule.

### Changed
- `docs/ai/Grok.md` and `docs/agents/Grok-Agent.md` now describe two seats.
- `docs/ai/Claude.md` and `docs/agents/Claude-Agent.md` marked historical.
- `AI-Architecture.md`, `AI-Workflow.md`, `Decision-Matrix.md`, ChatGPT and
  DeepSeek profiles, `AGENTS.md`, this changelog, and the ADR index.

## 2026-07-23 — Docs synced to repository reality; three-project boundaries adopted (ADR-0011)

Two ordered commits, one decision. First, the entry-point documentation
(README, AGENTS, CONTRIBUTING, SystemMap, Modules, Roadmap, examples,
mythos/README) was resynchronized with what this repository measurably
contains: `src/`, `scripts/`, and `tests/` have never existed in its git
history — the code lives in the maintainer's local working tree — and the
docs now say so instead of implying otherwise, with the canonical
explanation in `docs/architecture/SystemMap.md` ("Where the code actually
lives") and the previously unmapped `dbt/` directory on the map. Second,
`ADR-0011` adopted the three-project boundary model: **TerAustralis
Incognita** as the umbrella (governance, docs, ADRs, mythos — no main app
code), **Crystal Core** owning the engine, runtime, APIs, and shared
libraries, **Crystal Vision** owning the user-facing application — Clementine
wholly within it, Clementine as a logical component inside Crystal Core.

### Added
- `docs/adr/ADR-0011.md` — the boundary decision, including its
  decided-NOT list (no renames, no moves, no new repos, no workflow
  changes, no locked-name or taxonomy changes).
- `docs/governance/Project-Boundaries.md` — the standing charter:
  component→project map and the dependency rule (Crystal Vision may
  depend on Crystal Core; never the reverse).
- `docs/governance/Migration-Plan.md` — a staged, per-stage-approvable,
  reversible proposal (labeled Vision) for landing the code into git and
  retiring the drift; nothing in it is executed.

### Changed
- Reality banners and pointer notes across the entry-point docs; the
  stale pre-monorepo sibling-repo blurb in `mythos/README.md` replaced.
- `docs/governance/REPO-RESTRUCTURING-PLAN.md` marked superseded in place
  (its `packages/` split was reverted by `ADR-0010` and never landed in
  this repository's history).

## 2026-07-23 — Close the licensing question: uniform CC BY-NC-ND, packages/ reverted

`ADR-0009` deliberately left open whether the repository would converge on
uniform CC BY-NC-ND 4.0 or the differentiated per-package model
(`packages/`'s AGPL v3 / Proprietary / Dual / CC BY-NC-ND). Asked for a
recommendation, the case for uniform CC BY-NC-ND won: for a pre-revenue,
single-maintainer project, four parallel license regimes are real ongoing
overhead for protection that isn't needed yet, and more regimes means more
surface for the next uncoordinated session to get wrong. `ADR-0010` records
the decision and reverts `packages/`'s licensing to match.

### Changed
- Every `packages/*/LICENSE.md` (7 packages) rewritten from its previous
  license (AGPL v3, Proprietary, or MIT-non-commercial) to CC BY-NC-ND 4.0.
- Every `packages/*/pyproject.toml`'s `license` field updated to
  `CC-BY-NC-ND-4.0`; per-package `README.md` badges and licensing sections
  corrected to match (`crystalcore-ei/README.md` needed the most rework).
- `LICENSE.md`, `LICENSING.md`, `COMMERCIAL_LICENSE.md` (root files,
  actually CrystalCore-EI-specific) and
  `docs/governance/LICENSING-STRATEGY.md`/`LICENSING-QUICK-REFERENCE.md`
  marked superseded in place rather than deleted — real work worth keeping
  as a reference if a package-specific commercial license becomes relevant
  later.
- `README.md`'s license section rewritten a third time today — this time
  as a flat, resolved statement instead of "still open."

## 2026-07-23 — Reconcile licensing chaos across three more uncoordinated sessions

Within roughly 45 minutes, three more uncoordinated Claude sessions and a
direct push landed licensing-related changes on `main`: one added
Apache-2.0 SPDX headers to 97 source files, then partially self-corrected;
another pushed a large restructuring (`packages/`, seven independent
packages with differentiated per-package licenses — AGPL v3, Proprietary,
MIT/Commercial dual, CC BY-NC-ND) that changed `README.md`'s license claim
to something matching neither the root `LICENSE` file nor the new
per-package licenses it was meant to summarize. `ADR-0009` reconciles this:
CC BY-NC-ND 4.0 (root `LICENSE`) governs `src/` and `mythos/` today; the
`packages/` restructuring is real, deliberate work but not yet wired in as
authoritative (`pyproject.toml` still points at `src/`), so it's recorded
as the migration's target, not today's license — deliberately not deciding
between the two as the eventual outcome.

### Changed
- `README.md`'s license section rewritten to state both facts explicitly
  instead of picking one silently.
- 97 source files' stale `SPDX-License-Identifier: Apache-2.0` headers
  (under `src/apps/`, `src/crystal-core/`, `src/crystalcore/`,
  `src/crystalcore-os/`, `src/node/`, `src/sdk/`, `src/site/`)
  batch-corrected to `CC-BY-NC-ND-4.0`.
- `LICENSE.md`, `LICENSING.md`, `COMMERCIAL_LICENSE.md` (new root files
  from the restructuring, titled ambiguously as if repo-wide) given a scope
  note: they're the CrystalCore-EI package's license specifically, not the
  repository's.
- `origin/main`'s restructuring merged into this branch; the only real
  content conflict was `README.md`'s license bullet.

## 2026-07-23 — Code license: CC BY-NC-ND 4.0, superseding ADR-0006 §1

A separate, uncoordinated Claude session changed `LICENSE` from Apache-2.0
to CC BY-NC-ND 4.0 for full commercial exclusivity on the code, reversing
`ADR-0006`'s open-core decision without a superseding ADR, and its rewrite
of `NOTICE` also silently dropped the "TerAustralis Incognita" name and
copyright holder that `ADR-0007` had just fixed. The maintainer confirmed
CC BY-NC-ND 4.0 for code is the intended direction. `ADR-0008` records that
formally and fixes the resulting inconsistencies.

### Changed
- `docs/adr/ADR-0008.md` added: supersedes `ADR-0006` §1 only (§§2–3 —
  the six IP principles, trademark status — are unaffected); verifies via
  `git log` that no third-party contributor's code is affected by the
  relicensing (only the maintainer and Claude have ever committed here);
  adds a contribution-licensing clause to `CONTRIBUTING.md` reconciling
  "no derivative redistribution" with the repo's own pull-request workflow.
- `NOTICE` restored to "TerAustralis Incognita" / Crystal Arena-Turner as
  copyright holder, without touching the CC BY-NC-ND terms.
- `docs/ATTRIBUTIONS.md`'s "License Enforcement" and "Rebranding & Theft
  Prevention" sections rewritten — they had contradicted the rest of the
  same document by telling readers commercial use was freely permitted.
- Roughly a dozen other stale "code is Apache-2.0" references corrected for
  consistency: `README.md`, `LICENSE-CONTENT.md`, `mythos/README.md`,
  `mythos/COVENANT.md`, the `GOVERNANCE.md`/`LICENSE-CONTENT.md` site
  content mirrors, `docs/governance/Development-Standards.md`,
  `docs/architecture/crystal-core/Crystal-Runtime-Specification-v0.3.md`,
  two component `README.md`s, and the live site's `Footer.svelte` (was
  telling visitors the code was Apache-2.0 with a link to apache.org).
- Two nested per-component `LICENSE` files with full Apache-2.0 text
  (`src/crystal-core/LICENSE`, `src/apps/crystal-interface/LICENSE`)
  deleted — a monorepo with one root `LICENSE` doesn't need duplicates
  that can drift out of sync again.
- `src/sdk/typescript/package.json`'s `license` field updated to match;
  flagged in `ADR-0008` as worth a second look since a No-Derivatives
  license on a published npm package is unusual.

## 2026-07-23 — Name correction: TerAustralis Incognita

The project's name was being spelled "TeraAustralis Incognita" (two a's)
across most of the repository, but the maintainer's registered ABN trading
name is **TerAustralis Incognita** (one 'a') — confirmed by `README.md`'s
title, `NOTICE`, and every ABN reference under `archive/`, which already
agreed with the correct spelling. The double-a spelling was drift introduced
during the v1.0 reorganization, not a deliberate choice. Full reasoning:
[`docs/adr/ADR-0007.md`](docs/adr/ADR-0007.md).

### Changed
- `mythos/teraaustralis/` renamed to `mythos/teraustralis/` (history
  preserved via `git mv`); every internal path reference updated to match.
- Prose references to the project name corrected throughout live docs:
  `README.md`, `NOTICE`, `CONTRIBUTING.md`, `AGENTS.md`,
  `docs/governance/Constitution.md` (§1's locked name, corrected via its own
  §8 amendment process — see that file's amendment log), `docs/vision/Mission.md`,
  `docs/adr/ADR-0006.md`, and the mythos content that moved with the
  directory.
- `docs/adr/ADR-0001.md`, `docs/adr/ADR-0002.md`, and this file's own older
  entries are left unedited as the historical record of what was actually
  done at the time; `ADR-0007` supersedes the spelling detail without
  rewriting them.
- GitHub repository URLs and `git clone` instructions are unchanged — they
  still correctly point at `CrystalArchitect/TeraAustralis-Incognita`, the
  actual (unrenamed) repository name. Renaming the repository itself is
  flagged in `ADR-0007` as a separate, maintainer-only decision.

## 2026-07-23 — CrystalCore OS v0.2: Architecture Specification Release

Following review of v0.1, redefined v0.2 from "build the Engine" to
"clarify the architecture before implementing it" — a documentation-only
release, no runtime, by design. Rationale and the full decisions:
[`docs/adr/ADR-0004.md`](docs/adr/ADR-0004.md) (naming) and
[`docs/adr/ADR-0005.md`](docs/adr/ADR-0005.md) (the orchestrator concept).

### Changed
- `docs/vision/CrystalCore.md` rewritten from a five-row disambiguation
  table into the canonical taxonomy: CrystalCore Framework, CrystalCore
  Protocol, CrystalBridge, and CrystalCore OS, with the pre-existing
  mythos-terminal/platform name collision documented honestly rather than
  silently resolved. Any future runtime component is barred from becoming a
  fifth or sixth "CrystalCore" — it gets a name that describes its role.
- `docs/architecture/CrystalCore.md`'s section headers aligned to the new
  canonical names (Framework / Protocol pack / CrystalBridge).
- `docs/ai/AI-Architecture.md`'s orchestrator section: the previously
  separate "AI Router" idea folded into one name, "AI Orchestrator,"
  defined as recommend-then-human-decides (Task → Capability Assessment →
  Recommended AI → Human Review) rather than autonomous dispatch.
- `docs/governance/Roadmap.md`'s platform roadmap renumbered: v0.2 is now
  this specification release (delivered); the actual Engine build moves to
  v0.3, gated on the specification reaching implementation-level detail;
  the former v0.3 (Living Archive) becomes v0.4.

### Added
- `docs/ai/Decision-Matrix.md` — a task-type → recommended-AI →
  human-review-level table. This is the AI Orchestrator concept's first
  real increment, not a placeholder: no runtime, no automation, no new
  failure mode.
- `docs/adr/ADR-0004.md` and `ADR-0005.md`.

## 2026-07-23 — CrystalCore OS v1.0 repository architecture

The repository adopted the CrystalCore OS v1.0 layout (platform milestone
v0.1). Full mapping and rationale:
[`docs/adr/ADR-0001.md`](docs/adr/ADR-0001.md) — highlights:

### Changed
- All code moved under `src/` as a uniform shift (`apps/`, `crystal-core/`,
  `crystalcore/`, `node/`, `sdk/`, `site/`, `profiles/`, plus the mythos
  terminal to `src/crystalcore-os/`); runtime behavior unchanged and
  verified by the self-tests and suites.
- Component specs moved to `docs/architecture/crystal-core/`; root
  governance docs to `docs/governance/` (Constitution amendment logged);
  guides to `docs/guides/`; the Lattice sketch to
  `docs/architecture/lattice/`.
- `_archive/` became `archive/{legacy,2026}/`; `TeraAustralis/` folded into
  `mythos/teraaustralis/` with the strategy doc at
  `docs/vision/SouthernPillar.md`.
- Seven Sisters cycle material moved from the protocol pack to
  `research/seven-sisters/`.
- CI and the Pages deploy retargeted; the mesh-stub suite (`tests/`) now
  runs in CI; every path reference in code, docs, and the site swept.

### Added
- The documentation tree: `docs/{vision,architecture,governance,ai,agents,
  guides,adr}/` with per-area content, including the AI collaboration
  model and the first three ADRs.
- GitHub scaffolding: PR template, issue templates (bug / feature /
  mythos), discussion templates, CODEOWNERS.
- `scripts/maintenance/check.sh` (mirrors CI locally), area READMEs for
  `research/`, `archive/`, `assets/`, `examples/`, `scripts/`, and this
  changelog.

### Removed
- The inert nested `.github/` under the old `crystal-core/` (its issue
  templates were promoted to the root; its dead Pages workflow and
  boilerplate template deleted).

*(No earlier entries — the changelog starts with the v1.0 architecture;
prior history is in `git log` and the roadmap's "Recently landed".)*

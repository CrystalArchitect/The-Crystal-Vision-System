# Repository Portfolio Guide

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** Project-Boundaries.md §Repositories, architecture-survey.md §1 · **Last verified:** 2026-07-24 · **Labels:** Science ✅ / Vision 🔮 / Drift ⚠️ / Critical 🔴

---

## The Constellation — twelve repositories as at 2026-07-29

**Status**
- Science ✅ (count re-verified 2026-07-29; the six-repository model below was verified 2026-07-24 and remains accurate for those six)

**Summary**
The system spans **twelve** repositories as at 2026-07-29. Six of them carry the
model this page documents in detail: three living (active, in use) and three
frozen (provenance only, never edited). The three living repos form the complete
canonical system.

Six more exist and are **not** described by the living/frozen model — they were
created after it was written and have not been fitted to it:

| Repository | Visibility | Created |
|---|---|---|
| `CrystalCore.OS` | public | 2026-07-28 |
| `CrystalCore-AERIS` | public | 2026-07-28 |
| `crystalcore-os-aeris-vault12` | public | 2026-07-28 |
| `teraustralis-incognita-v2` | private | 2026-07-24 |
| `teraustralis-v2-presentation` | private | 2026-07-28 |
| `teraustralis-proposal` | public | 2026-07-29 |

Categorising those six is deliberately left to the Archive's
`knowledge-base/02-REPOSITORY-MAP.md`. That map currently covers **eleven** —
it was written before `teraustralis-proposal` existed and does not yet mention
it, so its own heading is one repository behind this page until it is re-run.
This page is not the canonical map and should not grow a second one.

A further dated observation, 2026-08-05, from a library-sync session with
eleven repositories in scope (it could not enumerate the account, so this
is a floor, not a count): one name is new since the twelve —
`the-library`, created 2026-08-03, holding the Loop Framework and the
constellation's document collection (its `records/2026-08-05-library-sync.md`
carries the full survey). Two of the twelve now carry new GitHub names:
the protocol pack this page's era documented as `crystalcore` now carries
the name `TheCrystalVision`, and the codex-site repository documented as
`The-Crystal-Vision` now carries `Clementine---Local-Soveriegn-Edge-AGI`.
Identification is by content-correspondence — each clone's README still
opens with its old identity — pending the id-keyed check the Archive's
ledger prescribes (its Part 18). That ledger already records
`crystal-vision` as renamed to `CrystalCore-Starlines-and-Dreamlines` on
2026-07-29; commits on it continue through 2026-07-31, so the "frozen"
classification in the Summary Matrix below is overtaken for that row.
Categorising all of this remains the Archive map's job.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Project-Boundaries.md (rewritten 2026-07-24 from same-day survey of all six)
- Verified: direct inspection of code trees + ls-remote
- Date: Two-repo split implemented as same-day history rewrite 2026-07-23 (per architecture-survey.md §1)
- Count corrected 2026-07-28 from a GitHub API query returning `total_count: 11` for `user:CrystalArchitect`. Of the five additions, four were created 2026-07-28; `teraustralis-incognita-v2` was created 2026-07-24 and existed, unsurveyed, on the day the six-repository model was verified.
- Count corrected again 2026-07-29 from the same query, now returning `total_count: 12`. The addition is `teraustralis-proposal`, created 2026-07-29 10:17 UTC — a public, All-Rights-Reserved proposal package (14 files, 12 commits, sole author Crystal Arena-Turner) holding the Pilbara / Port Hedland logistics case named as an advancement priority in [TERAUSTRALIS-FRAMEWORK.md](TERAUSTRALIS-FRAMEWORK.md) §6.2. It carries its own `LICENSE`, which is **All Rights Reserved** (view-only; no copying, derivative work, or implementation without written permission) — a licence class that did not previously appear anywhere in the portfolio. [`ADR-0013`](adr/ADR-0013.md) catalogued the portfolio's licensing as at 2026-07-28 across eleven repositories and is deliberately left unedited as the record of that sweep; this repository post-dates it and was not in it.
- Observed 2026-08-05 from a Claude Code library-sync session with eleven repositories in scope (clones on disk; no account-level query available to it): the `the-library` addition and the two renamings described above. Evidence is content-correspondence between clone READMEs/trees and the descriptions this page and the Archive recorded in July, plus git first-commit dates (`the-library`: 2026-08-03 08:42 +1000). Visibility of the new names was not determinable from clones, and the count of the whole constellation was not determinable at all — deliberately not asserted.

**Why this drifted**
"Six repositories" was true when written and was overtaken, not mistaken. The
count carried no date, so nothing in it could go stale visibly — it simply
became wrong while continuing to read as current. Counts of a growing thing
belong with the date they were taken.

**Discussion**
See [ARCHITECTURE.md](ARCHITECTURE.md) for the three-project boundary model these repos implement.

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) (three-project boundary model)

---

## Living Repositories

### 1. TerAustralis-Incognita (The Umbrella)

**Status**
- Science ✅

**Summary**
Canon and law — the umbrella holds governance, ADRs, architecture documentation, research, the mythos, and mirrors of pre-reorganization code.

**Evidence**
- Repository: `https://github.com/CrystalArchitect/TerAustralis-Incognita`
- Role: Umbrella governance and documentation
- CI/CD: Markdown lint + external link check (status: green as of 2026-07-24)

**Discussion**
The repository contains:
- `docs/` — architecture specs, governance, guides, process documentation
- `docs/adr/` — 11 Architecture Decision Records (ADR-0001 through ADR-0011)
- `docs/governance/` — Constitution, The-Incognita-Rule, Amendment process, Project-Boundaries, Migration-Plan
- `docs/reviews/` — Architecture audit and field surveys
- `mythos/` — The Covenant, The First Remembering, story, art, music, published research on Seven Sisters
- `research/` — Design exploration, seven-sisters cycle, specifications not yet implemented
- `archive/` — Provenance mirrors: frozen repos (tagged snapshots), local-snapshot from pre-reorg era
- `assets/`, `examples/` — Shared assets and demo index

**What it does NOT contain:** Main application code. `src/`, `tests/`, `scripts/`, `packages/` do not live here (despite older architecture docs incorrectly describing them — see [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) drift finding #1).

**Open Questions**
- Drift ⚠️: README.md and docs describe `src/` and `tests/` as if they exist here; they don't (removed as part of same-day 2026-07-23 reorganization, not documented).
- Drift ⚠️: `docs/README.md` index omits 9 files that physically exist in `docs/` (audit Tier 3, not resolved).

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — what lives where · [GOVERNANCE.md](GOVERNANCE.md) — how decisions are made · [TIMELINE.md](TIMELINE.md) — why the split happened

---

### 2. TerAustralis-Incognita-Code (The Engineering Repository)

**Status**
- Science ✅ (Stages 1–2 complete, Stage 3–4 deferred)

**Summary**
The complete working software — Crystal Core (engine) and Crystal Vision (application), per Migration-Plan implementation. Repository: `https://github.com/CrystalArchitect/TerAustralis-Incognita-Code` (private).

**Evidence**
- Contents: `core/` (Crystal Core), `vision/` (Crystal Vision)
- Test coverage: 70 tests passing (re-run and confirmed 2026-07-23)
- Merged PRs: #1 (Stages 1–2 core/ import), #2 (Stage 1–2 vision/ import, Pages deploy)

**Discussion**

**Contents structure (after Stage 1–2):**

| Area | What | Status |
|---|---|---|
| `core/` | Crystal Core: protocol pack (Starline, RDP, consent_transport, services), Clementine, CrystalBridge, mesh, SDK | Science ✅ |
| `core/crystal-core/` | Protocol pack: Starline Weaver, pipeline, Consent Transport, RDP, audit kernel | Science ✅ |
| `core/crystalcore/` | CrystalBridge: MCP consent gate, profiles | Science ✅ |
| `core/node/mesh/` | Mesh stub: transport library | Science ✅ |
| `core/sdk/typescript/` | TypeScript client scaffold (v0.5.0, Phase 1 / Mainnet HOLD) | Science ✅ |
| `vision/` | Crystal Vision: Clementine, demo shells, voicebox, site | Science ✅ |
| `vision/apps/clementine/` | Sovereign companion + embedded CrystalCore Framework | Science ✅ |
| `core/crystalcore/mind/` | Embedded Framework (forked 0.7.0; 0.13.4 unreconciled) | Science ✅ |
| `vision/apps/voicebox/` | MCP text-to-speech server | Science ✅ |
| `vision/apps/crystal-interface/` | Static demo shell (Authority HOLD) | Science ✅ |
| `vision/apps/vision-web/` | Static demo shell (honest scope callouts) | Science ✅ |
| `vision/site/` | Public site (SvelteKit + static adapter, 9 routes) | Science ✅ |
| `LICENSE` | CC BY-NC-ND 4.0 (ADR-0010, 2026-07-23) | Science ✅ |
| `CNAME` | teraustralis.com.au (moved from umbrella Stage 2) | Science ✅ |
| `.github/workflows/` | CI/CD: deploy.yml (Pages), GitHub Actions checks | Science ✅ |

**Test coverage (confirmed 2026-07-23):**
- Protocol pack: 51 self-tests (clementine 7, consent_transport 9, rdp 31, services 4)
- Mesh: 3 pytest
- Clementine: 16 tests
- **Total: 70 passing tests**

**CI/CD pipeline:**
- `compileall` — verify all .py files compile
- `bus.selftest` — 7 integration tests
- `consent_transport.selftest` — 9 crypto + socket tests
- `rdp.selftest` — 31 property-based tests
- `services.selftest` — 4 tests
- `Clementine pytest` — 16 tests
- `mesh pytest` — 3 tests
- **Pages deploy** — build and publish site

**Open Questions**
- Drift ⚠️: Top-level `dbt/` directory inherited from umbrella; unclear placement (see [OPEN-DECISIONS.md](OPEN-DECISIONS.md)).
- Drift ⚠️: No repo-level `scripts/` or `tests/` directories (Stage 2 decision: deferred until CI matures).

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — three-project boundary · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — component integration findings · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Stage 3–4 decisions

---

### 3. CrystalCore.OS-the-Crystal-Architecture-Archive (The Ledger)

**Status**
- Science ✅

**Summary**
System ledger — one canonical STATUS.md tracking state, receipts, and known unknowns across all repositories. Single source of truth for component state across all six repos, preventing drift between repo-local documentation and fleet-wide awareness.

**Evidence**
- Repository: `https://github.com/CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive`
- Contents: `STATUS.md` (fleet-wide state matrix)

**Discussion**
The STATUS.md tracks four states for each component: Running, Built-not-running, Designed-not-built, and Concept-only. The repository is intentionally small; it aggregates data only and contains no duplication.

**Related Documents**
— [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — component state details with evidence

---

## Frozen Provenance Repositories

**Status**
- Science ✅ (frozen as of 2026-07-17, verified via tag)

**Summary**
Three repositories are deliberately preserved as checkpoints, unedited and read-only, to preserve code provenance before the 2026-07-23 reorganization.

**Evidence**
- Freeze date: 2026-07-17 (tagged `-safe` suffix on each repo)
- Verification: Code has been salvaged into living repos where applicable
- Status: All frozen, never edited

**Discussion**
Frozen repos are never edited. These repos answer: "Where did this code come from, and what changed when it was moved?" End-state of these repos (GitHub archive as read-only flag vs. leave as-is) is a Stage 3 decision.

**Related Documents**
— [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — frozen repos end-state decision

---

### The-Crystal-Vision

**Status**
- Frozen ✅

**Summary**
Codex site + Clementine companion; complete **crystalcore v0.13.4 bytecode rescue**. Tag: `vision-safe-2026-07-17`. Repository: `https://github.com/CrystalArchitect/The-Crystal-Vision`.

**Evidence**
- Tag: `vision-safe-2026-07-17` (frozen 2026-07-17)
- Captured content: Codex site, Clementine companion, v0.13.4 bytecode
- Lives on as: Ancestor of Clementine's embedded framework

**Discussion**
Clementine forked the 0.7.0 branch from this repo. The 0.13.4 extras (SpaceXAI provider, `node.py`, `status.py`, CLI) remain unreconciled in this frozen repo. If questions arise about original implementation details, design intent, or pre-reorg behavior, this is the archive to consult.

**Related Documents**
— [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — lineage reconciliation decision · [TIMELINE.md](TIMELINE.md) — pre-monorepo era

---

### crystalcore

**Status**
- Frozen ✅

**Summary**
The Songline protocol pack (SonglineBus, original architecture before Starline Weaver). Tag: `crystalcore-safe-2026-07-17`. Repository: `https://github.com/CrystalArchitect/crystalcore`.

**Evidence**
- Tag: `crystalcore-safe-2026-07-17` (frozen 2026-07-17)
- Captured content: Songline protocol pack
- Lives on as: Direct ancestor of `core/crystal-core`

**Discussion**
Architectural evolution from SonglineBus to Starline Weaver is preserved in commit history. This archive allows tracing the protocol pack evolution and understanding pre-reorg design decisions.

**Related Documents**
— [TIMELINE.md](TIMELINE.md) — pre-monorepo era · [ARCHITECTURE.md](ARCHITECTURE.md) — current three-project boundary

---

### crystal-vision

**Status**
- Frozen ✅

**Summary**
Static demo shell (Grok build). Tag: `crystal-vision-safe-2026-07-17`. Repository: `https://github.com/CrystalArchitect/crystal-vision`.

**Evidence**
- Tag: `crystal-vision-safe-2026-07-17` (frozen 2026-07-17, not confirmed in this session)
- Captured content: Static demo shell
- Lives on as: Direct ancestor of `vision/apps/crystal-interface`

**Discussion**
Original vs. migrated demo shell can be compared; design evolution of operator interface understood through this archive.

**Related Documents**
— [TIMELINE.md](TIMELINE.md) — pre-monorepo era

---

## Cross-Repository Dependencies

**Status**
- Science ✅ (one documented pipeline)

**Summary**
The only automated cross-repo dependency is the public site pipeline: mythology content flows from umbrella to application repo to Pages.

**Evidence**
- Repositories: TerAustralis-Incognita (umbrella) + TerAustralis-Incognita-Code (engineering)
- Files: `mythos/` (umbrella, canonical) → `vision/site/src/content/` (Code)
- Established: Stage 2 (2026-07-23)

**Discussion**

The content pipeline:

```
mythos/ (umbrella, canonical)
   ↓ (manual copy)
vision/site/src/content/ (-Code)
   ↓ (SvelteKit build)
.github/workflows/deploy.yml (Pages)
   ↓ (Pages)
www.teraustralis.com.au (live)
```

Site renders *copies*, not canon directly. Publishing delay is acceptable design for small team.

**Open Questions**
- Known gap: The First Remembering (canonical in umbrella as of 2026-07-24) has not yet been copied into site content — known drift risk.
- Enhancement: CI/CD automation of this copy would be a Stage 3–4 feature.

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — three-project boundary · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — site sync decision

---

## Summary Matrix

**Status**
- Science ✅

**Summary**
Repository portfolio at a glance: the six repositories this page models — three living, supporting three projects (umbrella, Core, Vision), plus three frozen archives for provenance. Six further repositories exist as at 2026-07-29 and are outside this model; see the constellation section above and the Archive's `02-REPOSITORY-MAP.md` (which covers eleven of the twelve).

**Evidence**
- Complete inventory: three living repos + three frozen archives
- Verified: 2026-07-24 direct inspection

**Discussion**

| Repository | Type | Role | Status |
|---|---|---|---|
| TerAustralis-Incognita | Living | Umbrella (canon) | Science ✅ |
| TerAustralis-Incognita-Code | Living | Engineering (Stages 1–2) | Science ✅ |
| CrystalCore.OS-the-Crystal-Architecture-Archive | Living | Ledger | Science ✅ |
| The-Crystal-Vision | Frozen | Provenance (v0.13.4 rescue) | Science ✅ |
| crystalcore | Frozen | Provenance (Songline pack) | Science ✅ |
| crystal-vision | Frozen | Provenance (demo shell) | Science ✅ |

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — three-project boundary model · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — what's working, what's broken in each repo · [TIMELINE.md](TIMELINE.md) — why the constellation looks like this

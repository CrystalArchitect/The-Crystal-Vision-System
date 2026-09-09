# Development Timeline & Provenance

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** CHANGELOG.md, git commit narrative, Migration-Plan §Stages, dated PR banners, README banners · **Last verified:** 2026-07-24 (current state) · **Labels:** Science ✅ (git-verifiable) / Vision 🔮 (from specs/ADRs) / Unknown

---

## Era Summary

**Status**
- Science ✅ (verified from git history and dated ADR records)

**Summary**
The project evolved through five major phases: pre-monorepo (separate repositories), monorepo adoption (ADR-0001), v1.0 reorganization (same-day 2026-07-23 rewrite), Stage 1 recovery (canon tree located), and Stage 1.0 outcome (working copy verified). The timeline captures major decision dates and provenance SHAs.

**Evidence**
- Repository: TerAustralis-Incognita (docs and git history) + TerAustralis-Incognita-Code (git history)
- Verified: ADR timestamps, PR merge dates, git tags, commit SHAs

**Discussion**
See sections below.

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — current three-project model · [REPOSITORIES.md](REPOSITORIES.md) — where everything is · [GOVERNANCE.md](GOVERNANCE.md) — ADR trail

---

## Pre-Monorepo Era (Pre-2026)

**Status**
- Science ✅ (archived, tagged, frozen)

**Summary**
The project lived in four separate repositories, each self-contained. This era's code was preserved in three frozen provenance repositories and is not edited.

**Evidence**
- Repository: TerAustralis-Incognita / REPOSITORIES.md (frozen repos section)
- Tag: `-safe-2026-07-17` on all four archived repos
- Related Documents: [ARCHITECTURE.md](ARCHITECTURE.md) — current three-project model evolution

**Discussion**

All four repos are checkpointed at tag `-safe-2026-07-17` to preserve pre-reorg state. Code has been selectively rescued into the new structure:

| Repo | Focus | State | Lives on as |
|---|---|---|---|
| `The-Crystal-Vision` | Codex site + Clementine companion; holds complete crystalcore v0.13.4 bytecode | Frozen ✅ | Ancestor of Clementine's embedded Framework (0.7.0 fork line; 0.13.4 extras unreconciled) |
| `crystalcore` | Songline protocol pack | Frozen ✅ | Direct ancestor of core/crystal-core (SonglineBus → Starline Weaver evolution) |
| `crystal-vision` | Static demo shell (Grok build) | Frozen ✅ | Direct ancestor of vision/apps/crystal-interface |
| (Fourth repo) | TerAustralis-Incognita umbrella | Frozen ✅ | Evolved into current living umbrella repo |

The pre-monorepo architecture is documented in frozen form; future questions about pre-reorg design can consult these snapshots.

---

## ADR-0001: Monorepo Adoption (Date Unknown, Pre-2026-07-23)

**Status**
- Science ✅ (ADR-0001 exists; exact date not recorded in this session)

**Summary**
The project adopted a monorepo architecture unifying the four separate repositories. This was formalized in ADR-0001.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/ADR-0001.md
- Date: Proposed before 2026-07-23 (when ADR-0011 superseded its monorepo framing in project terms)
- Related Documents: [GOVERNANCE.md](GOVERNANCE.md) — ADR trail · [ARCHITECTURE.md](ARCHITECTURE.md) — three-project model

**Discussion**

ADR-0001 established the principle that the project should be one repository with a unified governance structure (the Constitution, ADRs, etc.). This set the stage for the v1.0 reorganization.

ADR-0011 (2026-07-23) reframes ADR-0001's monorepo model in terms of three projects (umbrella, Core, Vision) rather than contradicting it — the governance and code both live in one umbrella repo with two subprojects within the code repo.

---

## v1.0 Reorganization (2026-07-23 — Same Day)

**Status**
- Science ✅ (verified from git history, PRs, CI logs)

**Summary**
On 2026-07-23, a comprehensive reorganization happened in a single day: the umbrella repo split its code into a separate engineering repository, CI workflows were rewritten, Pages deploy was moved, old packaging workflows were removed, and an independent architecture audit was executed. This is the most consequential day in the project's recent history.

**Evidence**
- Repository: Both living repos (git history, PR merge dates)
- Date: 2026-07-23 (multiple PR timestamps, ADR-0011 adoption date)
- Audit: architecture-survey.md dated 2026-07-23, same day
- Related Documents: [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Stage 3–4 decision gates

**Discussion**

### Stage 0 (Documentation sync)

**What happened:** Root README banners added ("Status note"), entry-point docs synced with repo reality, boundary charter drafted, migration plan drafted, ADR-0011 written and adopted.

**PRs:** TerAustralis-Incognita (multiple commits)

**Outcome:** Docs tell the truth about current state; no code changed, blast radius zero.

**Note:** Stage 0 also included the double-a spelling correction (ADR-0007, PR #48).

---

### Stage 1: Code Import (engine layer — core/)

**What happened:** The `src/crystal-core/` directory (protocol pack, Clementine, RDP, Consent Transport, services) was imported into the new `-Code` repository under `core/crystal-core/`. Companion directories (`src/crystalcore/`, `src/profiles/`, `src/node/mesh/`, `src/sdk/typescript/`) came along under `core/`. A top-level LICENSE (CC BY-NC-ND 4.0 per ADR-0010) and `core/README.md` were added.

**PR:** TerAustralis-Incognita-Code #1 (merged)

**Verification:** All four self-test suites passed (51 tests: clementine 7, consent_transport 9, rdp 31, services 4).

**Deferred to Stage 1B:** `packages/` (excluded, superseded per ADR-0010); app-level code (deferred to vision/ Phase); repo-level `scripts/`, `tests/` (deferred to Stage 2 with CI).

---

### Stage 1B: Code Import (application layer — vision/)

**What happened:** The `src/apps/` directory was imported under `vision/apps/` (Clementine, crystal-interface, vision-web, voicebox). The site (`src/site/`) was imported under `vision/site/`. All paths preserved. Clementine's embedded Framework came along.

**PR:** TerAustralis-Incognita-Code #2 (merged)

**Verification:** 16 Clementine tests passed; app shells self-labeled HOLD (honest scope).

**Stage 1 outcome:** Both PRs merged; `-Code` repo contains the complete v1.0 engine and application.

---

### Stage 2: Workflows and Infrastructure

**Umbrella repo cleanup:**
- Removed `deploy.yml` (was broken, targeting absent `src/site/`)
- Removed `CNAME` (moved to `-Code`)
- Removed `test-packages.yml` and `publish-packages.yml` (verified zero tags ever pushed; PyPI names unclaimed)
- Retargeted `ci.yml` to docs-appropriate checks (markdown lint, external link check)
- Added Status note banners to superseded docs

**-Code repo setup:**
- Created `.github/workflows/deploy.yml` (Pages deploy from vision/site/)
- Added `CNAME` (teraustralis.com.au)
- Created compileall + self-test + pytest CI pipeline (70 tests total)
- Pages enabled via manual admin step (not automated)

**Verification:** All CI green; previous deploy.yml had been red since pre-Stage 2 (target already absent).

**PRs:** TerAustralis-Incognita (#54) + TerAustralis-Incognita-Code (#4)

**Stage 2 outcome:** Living repos have correct workflows; Pages deploy working; umbrella cleaned up.

---

### Stage 3–4: Deferred (as of 2026-07-24)

**Stage 3 — Repo-count decision and Clementine framework split:** Decision gates specified; not yet met. See [OPEN-DECISIONS.md](OPEN-DECISIONS.md).

**Stage 4 — Remaining placements (dbt, site sync, examples):** Recommendations stated; not yet implemented. See [OPEN-DECISIONS.md](OPEN-DECISIONS.md).

---

### Same-Day Audit (2026-07-23)

**What happened:** An independent architecture audit was conducted the same day as the reorganization, visiting both repos with 4 research passes (docs, content, core architecture, delivery surface). All tests were re-run and confirmed.

**Result:** architecture-survey.md (five key findings, Tier 1–3 recommendations).

**Why this matters:** The audit is contemporaneous with the reorg, not retroactive. It captures the state at reorganization time and provides baseline for future surveys.

**Related Documents:** [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — audit findings and component state matrix

---

## Stage 1.0 Recovery: Canon Tree Located (2026-07-23, Continued)

**Status**
- Science ✅ (verified via `git ls-remote` and droplet SSH session)

**Summary**
The full canon tree (`src/` + `packages/`) was located on a DigitalOcean droplet at commit `32692fd`, checked out on branch `claude/crystalcore-boot-visual-jau1bk`, clean and in sync with GitHub.

**Evidence**
- Repository: TerAustralis-Incognita (umbrella repo, git ls-remote confirms branch exists)
- Branch: `claude/crystalcore-boot-visual-jau1bk` @ SHA `32692fd`
- Verified: Droplet at `/root/clementine/repo` (umbrella clone with canon tree on session branch); clean working copy
- Date: 2026-07-23
- Related Documents: [REPOSITORIES.md](REPOSITORIES.md) — frozen repos · [ARCHITECTURE.md](ARCHITECTURE.md) — dependency rule

**Discussion**

The measured claim in Migration-Plan ("`src/` exists in *no branch* of this repository's git history") was updated to account for this discovery:

**True statement:** Never on `main`; present on session branch `claude/crystalcore-boot-visual-jau1bk` (and possibly other session branches; `ls-remote` shows ~12).

**Implication:** The code wasn't lost; it was on an unmerged session branch invisible to the default fetch policy.

The canon tree location determines Stage 1 hand-off point and provenance. Knowing it's on GitHub as a branch, not a laptop, changes the recovery assumptions.

---

## Stage 1.0 Outcome: Working Copy Confirmed (2026-07-24)

**Status**
- Science ✅ (maintainer confirmation via session context)

**Summary**
The droplet is a git clone of the umbrella repo (origin = pre-rename double-a URL, redirecting fine), checked out on `claude/crystalcore-boot-visual-jau1bk` @ `32692fd`, clean and in sync with origin. This is the maintainer's live working copy (laptop retired; now working from iPhone via Termius SSH).

**Evidence**
- Confirmed: Droplet is the canonical working copy (per maintainer's session context 2026-07-23)
- State: Clean, in sync, no untracked personal data
- Provenance: Branch + SHA `32692fd` matches GitHub
- Related Documents: [REPOSITORIES.md](REPOSITORIES.md) — working copy status

**Discussion**

The "hand-off by staging-branch push" is already satisfied — the staging branch effectively exists. No phone hand-off needed; work can proceed from the droplet or any host with the tree and git access.

---

## This Knowledge-Base Consolidation (2026-07-24)

**Status**
- Science ✅ (current work)

**Summary**
Seven documentation files consolidate 12 original deliverables into a stable, cross-linked knowledge base. Draws ~80% from existing verified documentation (Project-Boundaries.md, architecture-survey.md, 11 ADRs, STATUS.md, Constitution.md).

**Evidence**
- Location: `/home/user/TerAustralis-Incognita/docs/`
- Date: 2026-07-24 (consolidation day)
- Source: Project-Boundaries.md, architecture-survey.md, ADRs 0001–0011, STATUS.md, Constitution.md

**Discussion**

Seven documentation files consolidate 12 original deliverables:

1. `ARCHITECTURE.md` — Belt-Three model, three-project boundary, six-repo constellation
2. `REPOSITORIES.md` — Six-repo inventory with roles, GitHub links, CI/CD state
3. `GOVERNANCE.md` — ADR trail (0001–0011), locked names, Incognita Rule, amendment process
4. `TECHNICAL-FINDINGS.md` — 2026-07-23 audit findings, component state matrix, test coverage
5. `IP-LICENSING.md` — License trail (CC BY-NC-ND 4.0, ADR evolution), naming debts (resolved & outstanding)
6. `OPEN-DECISIONS.md` — Six decision gates (Stages 3–4, Tier 1–3 recommendations)
7. `TIMELINE.md` — This document (chronological narrative + provenance SHAs)

Future contributors (human and AI) can read one set of linked documents and understand the architecture exactly as it exists, with provenance traceable to git SHAs and ADRs.

---

## Provenance Summary: Critical SHAs and Branches

**Status**
- Science ✅ (verified, do not delete)

**Summary**
These branches and SHAs are provenance; they answer "where did the code come from?" and should not be deleted.

**Evidence**
- Repository: TerAustralis-Incognita + TerAustralis-Incognita-Code (git history)
- Verified: Branch existence confirmed via `git ls-remote`; commit SHAs verified against GitHub
- Date range: 2026-07-17 through 2026-07-23
- Related Documents: [REPOSITORIES.md](REPOSITORIES.md) — frozen repos · [ARCHITECTURE.md](ARCHITECTURE.md) — dependency rule

**Discussion**

| System | Branch / SHA | Date | Role | Status |
|---|---|---|---|---|
| Canon tree | `claude/crystalcore-boot-visual-jau1bk` @ `32692fd` | 2026-07-23 | Stage 1 hand-off source (full src/ + packages/) | Exists on GitHub; droplet clone verified clean |
| Umbrella Stage 0 | main (various commits) | 2026-07-23 | Docs sync, boundary charter, Migration-Plan, ADR-0011 | Merged |
| -Code Stage 1 PR 1 | PR #1 (merged) | 2026-07-23 | Engine import (core/), 51 tests passing | Merged |
| -Code Stage 1B PR 2 | PR #2 (merged) | 2026-07-23 | Vision import (vision/), 16 tests passing | Merged |
| Umbrella Stage 2 | PR #54 (merged) | 2026-07-23 | Workflow cleanup, ci.yml retarget | Merged |
| -Code Stage 2 | PR #4 (merged) | 2026-07-23 | New CI pipeline, Pages deploy, CNAME | Merged |
| Frozen provenance | `-safe-2026-07-17` tags on all three | 2026-07-17 | Pre-reorg snapshots (The-Crystal-Vision, crystalcore, crystal-vision) | Unedited, preserved |

Every commit reachable from these branches/tags/SHAs is part of the provenance chain. Deleting them loses the ability to verify "where did this code come from?"

---

## Known Timeline Gaps

**Status**
- Unknown (not surveyed this session)

**Summary**
Three questions remain unanswered about the project's history.

**Evidence**
- Session scope: v1.0 reorganization (2026-07-23 onward) and Stage 1 recovery (2026-07-24 onward)
- Limitation: Shallow clone depth; maintainer interview not conducted
- Related Documents: [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — lineage reconciliation (0.7.0 vs 0.13.4 fork)

**Discussion**

**Exact date of ADR-0001 adoption** — Monorepo decision happened before 2026-07-23 (when ADR-0011 reframed it), but the ADR's own date is not recorded in this session.

**Earlier repo split history** — The umbrella repo's README and `mythos/README.md` describe a four-repo era (pre-monorepo). When did that org exist? How long?

**Live site render state** — The site source is coherent and synced with its gallery (92 entries verified), but the current deployment state to www.teraustralis.com.au is unknown (network policy blocked direct access during audit).

These gaps exist because this session's scope was v1.0 reorganization (2026-07-23 onward) and Stage 1 recovery (2026-07-24 onward). Deeper history would require interviewing maintainer or reading earlier git commits beyond the shallow clone depth.

**Open Questions**
- Should ADR-0001 dating be captured in a future audit?
- Is the earlier four-repo era worth documenting separately?
- What is the current live site deployment state?

---

## Summary

**Status**
- Science ✅ (timeline complete through 2026-07-24)

**Summary**
CrystalCore.OS evolved through five phases: pre-monorepo (four separate repos), monorepo adoption (ADR-0001, exact date unknown), v1.0 reorganization (single day 2026-07-23), Stage 1 recovery (canon tree located), and Stage 1.0 outcome (working copy verified 2026-07-24).

**Evidence**
- Timeline: 2026 (pre-monorepo) → ADR-0001 (date unknown) → 2026-07-23 (reorganization day) → 2026-07-24 (consolidation begins)
- Verified: ADR-0011 adoption 2026-07-23, branch `claude/crystalcore-boot-visual-jau1bk` @ `32692fd` exists on GitHub
- Frozen tags: `-safe-2026-07-17` on three provenance repos
- Related Documents: [ARCHITECTURE.md](ARCHITECTURE.md) — current system state · [REPOSITORIES.md](REPOSITORIES.md) — six-repo inventory · [GOVERNANCE.md](GOVERNANCE.md) — ADR trail and decision process · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Stage 3–4 gates

**Discussion**

| Era | Event | Status |
|---|---|---|
| Pre-2026 | Four separate repositories | Frozen ✅ |
| Pre-2026-07-23 | ADR-0001: Monorepo adoption | Science ✅ (exact date unknown) |
| 2026-07-23 | Reorganization day: Stages 0–2, audit | Completed ✅ |
| 2026-07-23 (continued) | Stage 1.0 recovery: canon tree located | Verified ✅ |
| 2026-07-24 | Stage 1.0 outcome: droplet verified | Confirmed ✅ |
| 2026-07-24+ | This consolidation: knowledge base complete | In progress 🔮 |
| 2026-07-24+ | Stage 3–4: deferred | Decision pending ⏳ |

Three living repos (umbrella, `-Code`, ledger) carry the current system forward. Three frozen repos (tagged 2026-07-17) are preserved for provenance.

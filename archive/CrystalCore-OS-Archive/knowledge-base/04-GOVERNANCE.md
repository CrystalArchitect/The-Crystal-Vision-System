# Governance

ADRs, the governance model, authority boundaries, licensing history, and
the project's own open decisions.

## Statement — The ADR record

Eleven Architecture Decision Records exist, all dated 2026-07-23, all in
`TerAustralis-Incognita/docs/adr/`. The governing rule: "Numbers are
permanent: never renumber, never delete. A reversed decision gets a new
ADR that supersedes the old one."

| # | Title | Status | Decision (one line) |
|---|---|---|---|
| 0001 | Adopt the CrystalCore OS v1.0 repository architecture | Accepted | Reorganize the repo into the v1.0 blueprint: code under `src/`, docs under `docs/{vision,architecture,governance,ai,agents,guides,adr}`. |
| 0002 | Content areas: the mythos stays a top-level peer of docs and src | Accepted | `mythos/` stays top-level, not folded into `docs/` — different license, not documentation. |
| 0003 | Move code into `src/` as a uniform shift | Accepted | All code directories move into `src/` as one prefix shift, preserving relative-path behavior. |
| 0004 | Lock the CrystalCore naming taxonomy | Accepted | Four canonical branches (Framework/Protocol/CrystalBridge/OS); bars a fifth; leaves the CrystalCore OS/CrystalCore.OS collision unresolved on purpose. |
| 0005 | AI Orchestrator — ship the concept as documentation first | Accepted | Recommend-then-human-decides, not autonomous dispatch; shipped as a markdown table, not code. |
| 0006 | Licensing strategy and IP principles | Accepted — §1 superseded by 0008 | Originally: keep the Apache-2.0/CC BY-NC-ND dual license; recorded six IP principles (still standing). |
| 0007 | Correct the project name to "TerAustralis Incognita" | Accepted | Fixes drifted "TeraAustralis" spelling to match the maintainer's registered ABN trading name. |
| 0008 | Supersede ADR-0006 §1 — adopt CC BY-NC-ND 4.0 for code | Accepted — supersedes 0006 §1 only | Formally records an uncoordinated session's LICENSE flip to CC BY-NC-ND "for commercial exclusivity"; verifies no third-party relicensing gap. |
| 0009 | Reconcile the licensing chaos | Accepted — target question resolved by 0010 | Reconciles a second collision (97 stale SPDX headers, a `packages/` restructuring with 4 more licenses); rules CC BY-NC-ND governs `src/`+`mythos/` today, leaves `packages/` open. |
| 0010 | Uniform CC BY-NC-ND 4.0 for the whole repository | Accepted | Closes 0009's open question: the entire repo is uniformly CC BY-NC-ND, differentiated per-package licensing explicitly rejected. Terminus of the 0006→0008→0009→0010 chain. |
| 0011 | Adopt the three-project boundary model | Accepted | Umbrella / Crystal Core / Crystal Vision charter; `TerAustralis-Incognita-Code` reserved by charter for engineering; nothing renamed or moved by the ADR itself. |

**Status: Implemented** (all 11 confirmed Accepted, all read in full).

### Evidence
- `TerAustralis-Incognita/docs/adr/README.md` and `ADR-0001.md` through
  `ADR-0011.md`, each read in full.

### Historical Notes
ADR-0007's own "Consequences" section states the GitHub repo slug
still visibly disagreed with the corrected project name by one letter
— `Migration-Plan.md`'s debts register later records this as resolved
the same day (PR #48). ADR-0011's own "Consequences" section says
`ci.yml`/`deploy.yml` "remain red — deliberately," which Migration-Plan
Stage 2 (same day, later) resolved. Both are left as-is in the ADRs
themselves per the project's own convention of treating an accepted ADR
as immutable historical record — not corrected in this pass; noted here
instead.

### Cross References
`08-DESIGN-DECISIONS.md` (the *why* behind each), `11-CORRECTIONS.md`.

---

## Statement — Belt-Three, in full

Belt-Three has two levels, and the portfolio's day-to-day process
document operationalizes only the narrower one. The full origin, from
the Seven Sisters corpus: **three laws** — (1) Honour Country, (2) Label
science / story / vision, (3) No coercion, no fake hydrology, red button
off. `CONTRIBUTING.md`'s PR-facing "Belt-Three law" section defines only
three truth *labels* (Science / Story / Vision) — operationalizing law
#2 alone. Laws #1 and #3 surface elsewhere: #1 in `Constitution.md` §5
and `CODE_OF_CONDUCT.md`'s cultural-respect section; #3 in
`Constitution.md` §6 and the Starline Weaver's enforced red-button kill
switch.

**Status: Implemented** (law #2, in the wire protocol and every PR
template) — **the fuller three-law origin is Vision/Story**, not itself
a piece of running code.

### Evidence
- `CONTRIBUTING.md`: "Everything in this project carries one of three
  truth labels... Science / Story / Vision."
- `research/seven-sisters/crystalcore-seven-sisters-FULL.md`: "## II.2
  Belt-Three Laws (always on)."
- The PR template's own checkboxes (`.github/PULL_REQUEST_TEMPLATE.md`)
  merge Story and Vision into one box and add an undocumented fourth
  category ("Docs / governance / process") not present in
  `CONTRIBUTING.md`'s canonical three-label table — a real, if minor,
  internal inconsistency in the project's own core discipline
  mechanism, not corrected in this pass (process/template redesign, out
  of scope for a documentation-only correction).

### Historical Notes
39 files across the umbrella repository reference "Belt-Three" in one
sense or the other; no single document cross-links both levels
explicitly before this one.

### Cross References
`03-ARCHITECTURE.md` (Seven Sisters), `09-GLOSSARY.md`.

---

## Statement

The governance document set, and what each one governs:
`Constitution.md` (binding canon hierarchy and locked names),
`Migration-Plan.md` (the staged, per-stage-approvable code-migration
proposal — 5 stages, Stages 0–2 executed 2026-07-23, Stages 3–4
pending), `Repository-Principles.md` (9 numbered principles),
`Decision-Records.md` (when an ADR is required), `The-Incognita-
Rule.md` (the evidence doctrine — quoted in full in `00-INDEX.md`),
`Development-Standards.md` (the engineering bar for code changes),
`Review-Process.md` (branch → PR → green CI → review → maintainer
merge), `LICENSING-STRATEGY.md` and `LICENSING-QUICK-REFERENCE.md`
(both explicitly superseded, kept for provenance),
`REPO-RESTRUCTURING-PLAN.md` (superseded by ADR-0011).

**Status: Implemented** (all confirmed to exist and read in full;
supersession banners verified directly against each file's own text).

### Evidence
- `TerAustralis-Incognita/docs/governance/*.md`, all 13 files, read in
  full.

### Historical Notes
`REPO-RESTRUCTURING-PLAN.md` carries an explicit "Superseded" banner —
this appears to resolve a gap a prior architecture-survey session
flagged as missing (see `07-HISTORY.md`). `Review-Process.md`'s CI
checklist still describes an old, Python-based CI pipeline
(`compileall`, the four self-tests, `pytest`) that no longer exists —
the umbrella's actual current `ci.yml` runs only markdown lint and an
external link check. Not corrected directly in this pass; documented in
`11-CORRECTIONS.md`.

### Cross References
`11-CORRECTIONS.md`.

---

## Statement

The AI-collaboration model names six roles and five workflows.
**Roles:** ChatGPT (Chief Systems Architect), Claude (Repository
Engineer — "the v1.0 reorganization, ADR-0001, is its work"), DeepSeek
(Research & Engineering Specialist), Gemini (Knowledge & Multimodal
Specialist), Grok (Creative Exploration), GitHub (Development Platform
— "Not an AI"). **Workflows:** Architecture (ChatGPT→Claude→GitHub),
Engineering (DeepSeek→ChatGPT→Claude→GitHub), Documentation
(ChatGPT→Claude→GitHub), Knowledge (Gemini→ChatGPT→repository),
Brainstorming (Grok→ChatGPT→architecture-or-compost). "Every flow ends
at the repository through a pull request — no AI's output is canon
until the maintainer merges it." The standing caution: "Chaining AIs
multiplies fluency, not truth."

**Status: Implemented** (as documented process — this reconstruction
itself is additional, direct evidence the multi-AI-tool pattern is
real: this pass alone used three parallel research agents plus direct
verification).

### Evidence
- `docs/ai/AI-Architecture.md`, `AI-Workflow.md`, and the six per-tool
  files, all read in full.
- `docs/ai/Decision-Matrix.md`: 11-row task→AI→human-review-level
  table.
- Corroborating git evidence: "Fold ChatGPT's architecture review into
  three follow-up doc improvements" (commit, 2026-07-23) — confirms
  external AI-tool collaboration beyond Claude in practice, not just in
  the documented model.

### Historical Notes
None.

### Cross References
`09-GLOSSARY.md`.

---

## Statement

`.github/CODEOWNERS`, in full (three lines): "The maintainer (Crystal)
reviews everything by default. Review process: docs/governance/
Review-Process.md. `* @CrystalArchitect`"

**Status: Implemented.**

### Evidence
- `TerAustralis-Incognita/.github/CODEOWNERS`, read in full.

### Historical Notes
None.

### Cross References
None.

---

## Statement — Licensing and IP boundaries

The public/private repository split (`02-REPOSITORY-MAP.md`) is the
primary IP boundary: the one public repository holds no application
code.

> **Correction (2026-08-08).** Both halves of that sentence are now
> false, and it is the one an outside evaluator could be misled by, so
> it is corrected rather than left to its date. Several repositories are
> public, `TerAustralis-Incognita-Code` among them, and it holds the
> engine and the application. The IP boundary is therefore **not** the
> public/private split and has not been for some time: it is the licence
> — uniform CC BY-NC-ND 4.0 across the portfolio per ADR-0013, which
> forbids commercial use and derivative redistribution wherever the code
> sits. Visibility was never doing the work the sentence credits it with. The licensing chain (ADR-0006→0008→0009→0010) terminates in a
uniform CC BY-NC-ND 4.0 license across the whole umbrella repository,
explicitly rejecting a four-way differentiated per-package model. That
rejected model has a concrete, surviving artifact: `TerAustralis-
Incognita-Code`'s abandoned, never-merged PR #1 branch contains a fully
realized `packages/` tree under a `teraaustralis.*` namespace
(consent-transport, crystalbridge, crystalcore-ei, lumina, mythos, rdp,
starline), each with its own `pyproject.toml`/README/LICENSE.md —
`crystalcore-ei` additionally ships its own `COMMERCIAL_LICENSE.md`,
distinct from the rest. This is the literal, in-the-wild remnant of the
model ADR-0010 reverted.

Separately: `TerAustralis-Incognita-Code`'s own root `LICENSE` is CC
BY-NC-ND 4.0, and 96 of its source files (across `.py`/`.js`/`.ts`/
`.svelte`) once carried `SPDX-License-Identifier: Apache-2.0` headers —
the exact defect ADR-0008 already fixed once, in the umbrella, via a
batch header rewrite, which this repository never inherited.

**That is now resolved.** The batch rewrite was applied (97 files, the
97th being this archive's own prior addition `core/crystalcore/
selftest.py`), and re-verified 2026-07-28: `origin/main` carries **0**
Apache-2.0 SPDX headers on source files and 109 CC-BY-NC-ND-4.0 ones.
See `11-CORRECTIONS.md` Part 4.

A related defect *did* survive it, and was fixed separately under
ADR-0013 on 2026-07-28: the headers were corrected, but two nested
`LICENSE` files — `core/crystal-core/LICENSE` and
`vision/apps/crystal-interface/LICENSE` — were still Apache-2.0, so
files asserting CC BY-NC-ND in their own headers sat beside a `LICENSE`
asserting Apache-2.0. Header rewrites do not touch `LICENSE` files, and
nothing was checking the two agreed.

**Status: Implemented** (the license, the boundary, the SPDX headers,
and the nested `LICENSE` files).

### Evidence
- `docs/adr/ADR-0010.md`: "four parallel license regimes are real,
  ongoing operational overhead... for protection that isn't needed yet"
  for a pre-revenue, single-maintainer project.
- `TerAustralis-Incognita-Code`, branch `claude/teraustralis-incognita-
  import-g63jm9`: `git ls-tree -r` confirms the full `packages/` tree
  and its per-package licensing, including
  `packages/crystalcore-ei/COMMERCIAL_LICENSE.md`.
- Direct grep, 2026-07-24: `TerAustralis-Incognita-Code` root `LICENSE`
  is CC BY-NC-ND 4.0; 96 files carried
  `SPDX-License-Identifier: Apache-2.0`.
- Direct grep, 2026-07-28, against `origin/main`: 0 source files carry an
  Apache-2.0 SPDX header; 109 carry CC-BY-NC-ND-4.0. The mismatch this
  section reported is gone.

### Historical Notes
None beyond what's stated above.

### Cross References
`07-HISTORY.md` (the PR #1 episode in full), `11-CORRECTIONS.md`.

---

## Statement — The project's own open governance decisions

Preserved verbatim from the umbrella's own 2026-07-24 charter, as the
project's questions, not this archive's:

- **Stage 3 repo count** — whether `core/`/`vision/` split into two
  repositories.
- **0.13.4 lineage** — Lumina's framework forked the 0.7.0 line; the
  0.13.4 rescue's extras sit unreconciled in `The-Crystal-Vision`.
- **Frozen repos' end state** — archive the three provenance repos, or
  leave them as-is.
- **Site copy of new canon** — The First Remembering is canonical but
  not yet copied to the site.

**Status: Unresolved**, by design.

### Evidence
- `docs/governance/Project-Boundaries.md`, "Open decisions this map
  records rather than resolves."

### Historical Notes
None — current as of 2026-07-24.

### Cross References
`02-REPOSITORY-MAP.md`.

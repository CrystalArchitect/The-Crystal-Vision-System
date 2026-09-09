# History

The full dated chronology, and two "built, then lost" episodes traced
in complete evidentiary detail.

## Statement — Timeline

| Date | Event |
|---|---|
| 2026-07-14 | `The-Crystal-Vision` created — the oldest repository, birthplace of the core narrative content (VISION, ARCHITECTURE, CODEX). |
| 2026-07-15 | "Add Clementine starter framework: local companion via Ollama" — the companion's birth commit. Same day: "Refactor into the CrystalCore package; Clementine is its first persona" — the framework is multi-persona-shaped from birth. Rapid same-day iteration, Clementine v1 through v7. |
| 2026-07-17 | `crystal-vision` and `crystalcore` (Songline pack) created. "Clementine Singularity Bridge v0 — multi-AI Songline Bus" shipped in `crystalcore`. `TerAustralis-Incognita` created. |
| 2026-07-21 | The rename sweep: "Clementine (companion) → Lumina"; separately, "Songline Bus → Starline Weaver + Dreamline Narrator"; `mythos/NAMES.md` added, reserving "Songline" exclusively for Aboriginal culture. `crystalcore` (repo 6) — created before this sweep — never updated past the old names. |
| 2026-07-22 | RDP wired to the Starline Weaver's matrix mode. |
| 2026-07-23 | **The pivotal day** — see below. |
| 2026-07-23, 09:07 UTC | `TerAustralis-Incognita-Code` created. |
| 2026-07-23, 09:44 UTC | PR #1 opened on the new Code repo — "Initial import: code + license" — 37 minutes after repo creation. Still open, never merged, as of this reconstruction. |
| 2026-07-23, ~14:27–18:24 UTC | Stage 1 (engine import from umbrella branch `claude/crystalcore-boot-visual-jau1bk` @ `32692fd`) and Stage 2 (vision-app import, CI + Pages migration) executed on `TerAustralis-Incognita-Code`'s `main` — the path that actually became this repository's history, distinct from the still-open PR #1. |
| 2026-07-23/24 | `CrystalCore.OS-the-Crystal-Architecture-Archive` created; system ledger established. |
| 2026-07-24 | This reconstruction. |
| 2026-07-24 (later) | The reconstruction's three PRs merge (#4 — this knowledge base publishes; #59 — umbrella doc corrections; #8 — Code repo). PR #7 (the maintainer's own) and PR #8 together fix, the same day this archive first documented them, the three CrystalBridge defects and the `vision/README.md` overclaim — see `06-COMPONENTS.md` (CrystalBridge) and `11-CORRECTIONS.md` Part 3. |
| 2026-07-24 (later still) | Two more uncoordinated sessions land work across the portfolio: one merges a second, independently-built 7-file knowledge base into the umbrella's `docs/` (PR #60/#61) — discovered and reconciled this pass, this archive's `knowledge-base/` affirmed canonical, both preserved, see `11-CORRECTIONS.md` Part 4; another commits `REPO-ARCHAEOLOGY-2026-07-24.md` (a git-object-level six-repo survey) directly to this repository's root, independently corroborating this archive's provenance chain and naming this repository's own meta-record role directly. A third instance of this project's recurring uncoordinated-parallel-session pattern (compare the licensing chaos and the Crystal Runtime episode, above). This pass also reapplies ADR-0009's SPDX fix (lost in the repo split) and reconciles a handful of remaining Part 2 documentation items — see `11-CORRECTIONS.md` Part 4 for the full list. |

**Status: Implemented** (as a dated record — every row independently
sourced from git history or live GitHub metadata, cross-checked, not
copied from any single prior summary).

### Evidence
- Full `git log` across all six repositories, gaps re-checked until
  complete (an initial partial pull was caught missing each repo's
  oldest commits and re-fetched).
- GitHub API repository-creation timestamps, fetched directly.

### Historical Notes
A prior architecture-survey session exists on record at
`TerAustralis-Incognita/docs/reviews/2026-07-23-architecture-survey.md`
— four independent research passes plus direct test execution,
conducted the same day as most of the events above. Its headline
findings (the same-day history rewrite; `packages/` being actively
misleading; docs and code having "overtaken each other in opposite
directions"; the dbt warehouse having no data source; the Crystal
Runtime already passing 75 tests while `Roadmap.md` called it "not
started") are treated here as historical evidence and cross-checked,
not silently rediscovered. Two of that survey's findings appear
resolved as of this reconstruction (`REPO-RESTRUCTURING-PLAN.md` now
carries a Superseded banner; `mythos/README.md` no longer contains a
stale four-separate-repo framing) and are noted as such rather than
re-flagged as open.

### Cross References
`10-PROVENANCE.md` (verification methodology).

---

## Statement — 2026-07-23, the pivotal day, in sequence

CrystalCore OS v1.0 repository reorganization (ADR-0001) → v0.2, the
"Architecture Specification Release" (ADR-0004, ADR-0005 — naming
taxonomy and AI Orchestrator concept, deliberately no runtime shipped)
→ the licensing saga (ADR-0006 → 0008 → 0009 → 0010, described in one
commit as reconciling "licensing chaos from three more uncoordinated
sessions") → the EI/ML module build-out (HuggingFace, multimodal,
uncertainty quantification, dbt warehouse — the content now living at
`mythos/crystalcore-os/`) → the project renamed to match a real,
registered ABN trading name (ADR-0007) → ADR-0011, the three-project
boundary charter → a documented same-day history rewrite, used to
execute the repository split → `TerAustralis-Incognita-Code` created
and populated.

**Status: Implemented** (dated, commit-sourced).

### Evidence
- Full `git log`, `TerAustralis-Incognita`, 2026-07-23 entries.
- Commit: "Survey correction: the repo split landed via a same-day
  history rewrite."

### Historical Notes
Because of the documented history rewrite, dates recorded for this day
across the portfolio are the project's own claim about its history, not
independently re-derivable original chronology from first principles —
stated once here, applying to every date-stamped claim in this archive
for 2026-07-23.

### Cross References
`04-GOVERNANCE.md` (the ADR chain), `08-DESIGN-DECISIONS.md`.

---

## Statement — Episode: the Crystal Runtime, built then lost

A fully specified 7-module coordination layer (Coordinator, Registry,
EventBus, Config, Plugins, Logger, API) was not only designed but
**implemented and merged**, with a real, passing test suite, into the
umbrella repository's history on 2026-07-23 — and is **absent from
every current tree in the portfolio today.** Its only surviving trace
anywhere is an abandoned, never-merged pull request in a different
repository.

Exact evidence chain:
1. Three specification documents (`Crystal-Runtime-Specification-v0.3.md`,
   `Runtime-Module-Interfaces.md`, `Runtime-Testing-Specifications.md`)
   fully specify the layer, proposing code paths under `src/runtime/`.
2. Umbrella repo PR #43, "Add comprehensive testing suite for Crystal
   Runtime v0.3: 75 tests," merged 2026-07-23T08:14:29Z, commit
   `b09672d454d124b333abbeeb0c7265f6603c83dc`. Its own body states:
   "Phases completed: Phase 1 ✅ (PR #32, #38) · Phase 2 ✅ Module
   Implementation (7 modules, 2,574 lines) · Phase 3 ✅ Comprehensive
   Testing (75 tests, 5 layers)." Its actual added test files (`tests/
   runtime/test_contract.py`, `test_e2e.py`, `test_integration.py`)
   contain literal imports: `from src.runtime.coordinator.coordinator
   import Coordinator, Task, ExecutionContext`, and equivalents for
   `registry.registry`, `events.eventbus`, `config.config`,
   `logging.logger`, `api.api` — confirming the module implementation
   existed, with matching class names, at merge time.
3. As of this reconstruction: `find` across both the umbrella and
   `TerAustralis-Incognita-Code`'s current working trees returns zero
   matches for any `runtime/` directory. `git log --all` in the
   umbrella for any path containing "runtime" returns nothing — the
   commit exists per GitHub's API (platform metadata, independent of
   local git refs) but is not reachable from the umbrella's current
   `main`, consistent with the documented same-day history rewrite
   having dropped this tree rather than carrying it into the
   repository split.
4. The only surviving trace: `TerAustralis-Incognita-Code`, branch
   `claude/teraustralis-incognita-import-g63jm9` (PR #1, still open,
   never merged) contains `src/runtime/` in full — `api/api.py`,
   `config/config.py`, `coordinator/coordinator.py`,
   `events/eventbus.py`, `logging/logger.py`,
   `plugins/plugin_manager.py`, `registry/registry.py` — plus
   `tests/runtime/{test_contract,test_coordinator,test_e2e,
   test_integration,test_registry}.py`, ~2,237 lines of tests. This
   branch appears to derive from a different, earlier snapshot than
   the "canon branch `32692fd`" that Stage 1 actually imported from,
   which is why the module survived here and nowhere else.

**Status: Historical.**

### Evidence
See inline citations above — every claim in this episode is directly,
independently verifiable via the cited commit SHA, PR number, or `find`
command.

### Historical Notes
Neither `SystemMap.md` nor `Modules.md` (the portfolio's two
"authoritative component inventory" documents) ever listed Crystal
Runtime, before or after this episode — it was never in the map even
while it briefly existed as running, tested code.

### Cross References
`03-ARCHITECTURE.md` (the specification, read on its own terms),
`10-PROVENANCE.md` (the raw commit/branch evidence).

---

## Statement — Episode: PR #1, the abandoned initial import

`TerAustralis-Incognita-Code`'s pull request #1, "Initial import: code +
license," opened 2026-07-23T09:44:46Z (37 minutes after the repository
itself was created), branch `claude/teraustralis-incognita-import-
g63jm9`, remains **open and unmerged** as of this reconstruction — the
only open pull request across the entire six-repository portfolio.

Diffed directly against the repository's actual current `main`: 401
files changed, 21,173 insertions, 1,130 deletions relative to the
merge-base. Most of its content (the crystal-core protocol pack,
Lumina, demo shells, the site) has a near-identical counterpart on
`main` at different paths (`src/` on this branch vs. `core/`+`vision/`
on `main`) — confirmed by git's own rename detection showing
single-line drift on a spot-checked file (`bus.py`). This content is
not orphaned, only reorganized — `main` took a different, narrower
import path (Stage 1/Stage 2, from umbrella branch
`claude/crystalcore-boot-visual-jau1bk` @ `32692fd`) that achieved
largely the same result through a different route.

Two things exist **only** on this branch, confirmed absent from `main`
and from every architecture document read in this reconstruction: the
orphaned `src/runtime/` tree (see the Crystal Runtime episode above),
and a fully realized `packages/` tree under a `teraaustralis.*`
namespace with per-package differentiated licensing — the literal
surviving artifact of the licensing model ADR-0010 rejected (see
`04-GOVERNANCE.md`).

**Status: Historical** (as an abandoned branch) — **and Unresolved**
(whether it should be formally closed, and whether anything in it is
worth salvaging, are open questions this archive does not answer — see
below).

### Evidence
- `pull_request_read` (GitHub API), PR #1, `TerAustralis-Incognita-
  Code`: full body, file list, and commit history, fetched directly.
- Local `git fetch` of the branch and direct `git diff --stat` /
  `git ls-tree` against `main`, performed this session.

### Historical Notes
This is presented as a fact about the portfolio's state, not a defect
requiring this archive's judgment. Per this reconstruction's
documentation-only mandate, no action was taken on the branch or the
pull request itself.

### Cross References
`04-GOVERNANCE.md` (the packages/ licensing artifact), `10-PROVENANCE.md`.

---

## Statement — Outstanding questions this episode raises

Should PR #1 be formally closed to document the abandonment explicitly,
rather than left open indefinitely? Does `src/runtime/` contain
anything worth salvaging into the current architecture, given it once
passed 75 tests? Neither question is answered here — this archive's
mandate is to document the architecture that exists, not to decide
what should happen to abandoned work. Both are recorded as open
questions for the maintainer.

**Status: Unresolved**, by design.

### Evidence
See the two episodes above.

### Historical Notes
None.

### Cross References
`04-GOVERNANCE.md`.

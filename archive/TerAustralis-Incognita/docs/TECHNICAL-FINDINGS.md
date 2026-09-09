# Technical Audit & Findings

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** architecture-survey.md (complete 2026-07-23 audit), STATUS.md (component state) · **Last verified:** 2026-07-23 (audit re-run confirmations) · **Labels:** ✅ Verified / 🔮 Vision / ⚠️ Drift / 🔴 Critical

---

## Executive Summary

**Status**
- Science ✅ (verified by re-run of all tests this session)

**Summary**
The project is in better shape than its symptoms suggest. Engineering underneath is frequently excellent (real cryptography, property-based testing, disciplined ADR trail), but it was built across a compressed timeline by several uncoordinated hands. Seams from that coordination gap are showing. Nothing found is a five-alarm fire; several things are quietly accumulating interest.

**Evidence**
- Repository: TerAustralis-Incognita / docs/reviews/2026-07-23-architecture-survey.md
- Date: 2026-07-23 (audit date, all tests re-run and confirmed)
- Audit scope: 4 independent research passes (docs, content, core architecture, delivery surface)

**Discussion**

**By the numbers:**
- 2 repos, split same-day (2026-07-23) — docs repo still describes repo that no longer exists
- 3 core systems sharing vocabulary, not code — near-zero real integration
- 150+ tests passing across the code repo (re-run and confirmed)
- 7 `packages/` distributables — zero ever executed by test or CI
- 5 key findings (detailed below)

The project needs targeted fixes in specific areas (Tier 1–3 recommendations) rather than structural overhaul.

**Related Documents**
— ARCHITECTURE.md — system boundaries · REPOSITORIES.md — current state · TIMELINE.md — why the current state exists

---

## The Five Key Findings

### Finding 1: Docs Repo Describes Repo That No Longer Exists

**Status**
- Drift ⚠️ (actionable)

**Summary**
The docs repository's README, ADRs, and agent-instruction files still assume `src/`, `tests/`, and `scripts/` live inside it. Those paths are absent from today's `main` and absent from all locally available git history. GitHub Actions history shows CI exercising `src/` on an earlier `main` lineage the same morning; the split was implemented as a same-day history rewrite that no document records.

**Evidence**
- Repository: TerAustralis-Incognita
- Files: README.md, docs/architecture/SystemMap.md, docs/agents/*.md (all reference `src/`, `tests/`)
- Date: Repo split happened 2026-07-23 as force-push (not documented)

**Discussion**
The code was moved to a new repository (`TerAustralis-Incognita-Code`) as part of the same-day reorganization. The umbrella repo's documents were not updated to reflect this move. New readers (human or AI) who read the docs repo alone get a map that doesn't match the territory.

**Open Questions**
- Related drift: `mythos/README.md` describes an even older arrangement (four separate repositories) — predates both the current two-repo reality and ADR-0001 monorepo model.
- Tier 1 recommendation: Add dated note to `SystemMap.md` and root README explaining current two-repo split. Reconcile or retire `mythos/README.md`.
- Status: Not yet implemented (this knowledge-base project does not cover older docs revisions; they remain open issues).

**Related Documents**
— [REPOSITORIES.md](REPOSITORIES.md) — current state · [TIMELINE.md](TIMELINE.md) — why the split happened

---

### Finding 2: `packages/` Is Actively Misleading

**Status**
- Critical 🔴 (actionable immediately)

**Summary**
Seven `teraaustralis.*` namespace packages exist. Five non-empty ones are byte-for-byte copies of `src/` code with copyright headers stripped — not thin re-export wrappers. Every README describes an API surface that doesn't exist in the shipped code. Nothing in `packages/` has ever been executed by a test, self-test, or even a syntax check.

**Evidence**
- Repository: TerAustralis-Incognita-Code (legacy)
- Directory: packages/ (inherited from pre-reorg era)
- Verified: diff of five copies shows identical code except copyright header removal
- Test coverage: Zero (check.sh's `compileall` doesn't include packages/)

**Discussion**

**Specific issues:**
- `packages/clementine/__init__.py`: carries CrystalBridge's docstring (copied by mistake); entry point (`clementine = "teraaustralis.clementine:main"`) points at non-existent attribute → fails on install.
- `packages/crystalbridge`: hardcodes relative path that worked one level up; copied differently, points at non-existent directory.
- `packages/starline`: imports `teraaustralis.consent_transport` without declaring it as dependency → `pip install` fails.

**Open Questions**
- Tier 1 recommendation: Delete `packages/` entirely and ship `src/` directly, OR commit to thin re-export wrappers wired into CI so drift is caught going forward. Leaving as-is actively misinforms readers.
- Status: Not yet implemented (Tier 1, high priority).

**Related Documents**
— [REPOSITORIES.md](REPOSITORIES.md) — current `-Code` structure

---

### Finding 3: Documentation and Code Have Overtaken Each Other

**Status**
- Drift ⚠️ (mixed directions)

**Summary**
The runtime exists in code while docs call it unstarted; `packages/` READMEs describe features that were never built. Both are symptoms of the same root: writing and shipping happened faster than anyone had time to reconcile.

**Evidence**
- Repository: TerAustralis-Incognita + TerAustralis-Incognita-Code
- Example: Roadmap.md calls Crystal Runtime "not started"; code repo already ships it with 75 passing tests
- Missing cross-references: `docs/README.md` index omits 9 files including heavily cross-referenced `ATTRIBUTIONS.md`

**Discussion**

**Specific issues:**
- Three same-day Crystal Runtime spec documents contradict each other (one: "deferred until review", another: "ready to specify testing", third: "ready for implementation") while `Roadmap.md` calls it "not started."
- `Roadmap.md` "Recently landed" section missing four most recent ADR entries that `CHANGELOG.md` already records.
- Two of three `packages/` licensing docs carry "Superseded" banners pointing at ADR-0010; one (`REPO-RESTRUCTURING-PLAN.md`) doesn't, still reading as live.

**Open Questions**
- Tier 2 recommendation: Reconcile Crystal Runtime spec trio contradiction; update `Roadmap.md` to reflect that runtime exists (75 passing tests).
- Status: Not yet implemented.

**Related Documents**
— [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Component State Matrix (Crystal Runtime state)

---

### Finding 4: The Emotion-Prediction Warehouse Has No Data Source

**Status**
- Critical 🔴 (broken, would fail compilation)

**Summary**
`dbt/crystalcore_emotion_warehouse/` is a real, well-modeled 28-class dbt project with staging views, core marts, active-learning queue, sensible macros. But every staging model is a hardcoded CTE of `null` literals; there is not one `source()` call. Running it produces tables of exactly one null row each. Worse, `stg_emotion_labels.sql` ends with a dangling `union all` immediately before closing paren — a genuine SQL syntax error that would fail `dbt compile`.

**Evidence**
- Repository: TerAustralis-Incognita-Code (inherited from pre-reorg)
- Directory: dbt/crystalcore_emotion_warehouse/
- File: stg_emotion_labels.sql (syntax error), all staging models (null CTEs, no sources)
- Related: dbt_integration.py writes JSONL but nothing reads it

**Discussion**
The project is engineering-ready code for a feature that doesn't exist yet. Staging models contain null CTEs instead of real data sources. SQL syntax error makes `dbt compile` fail.

**Open Questions**
- Tier 1 recommendation: Fix SQL syntax error; decide whether to wire staging to JSONL files `dbt_integration.py` writes, or retire until ready.
- Status: Not yet implemented.

**Related Documents**
— [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — dbt warehouse decision gate

---

### Finding 5: The Governance Discipline Is Real and Rare

**Status**
- Verified ✅

**Summary**
The project runs on one rule: always mark which lines are dreamed and which are surveyed, never let a dreamed line pretend it was measured. That rule is operationalized as mandatory Science/Vision/Story labels on every PR. The discipline shows up as real editorial discipline throughout — documents about unbuilt systems say so plainly. That's unusual and valuable.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/The-Incognita-Rule.md
- Verified: Operationalized on every PR (Mode header enforced)
- Audit: "The Incognita Rule produces admirably candid 'not built yet' language throughout the docs repo and the demo apps' own SECURITY.md files."

**Discussion**
Ten ADRs show the same discipline — numbered sequentially, never reused, supersession always explicit. The licensing chaos (ADRs 0006–0010) is documented clearly, not hidden. Decision records are incomplete for pre-ADR history, but everything in the trail is procedurally sound.

This is why a review like this is possible at all — the project tells the truth about what's built vs. dreamed, so an external auditor can actually verify claims.

**Open Questions**
- Recommendation: Keep this discipline; apply it to the two weakest spots (the repo split itself — haven't updated docs yet, and `packages/` READMEs — still claiming features that were never built).

**Related Documents**
— [GOVERNANCE.md](GOVERNANCE.md) — The Incognita Rule operationalization · [REPOSITORIES.md](REPOSITORIES.md) — current state requiring disciplined labeling

---

## Component State Matrix

**Status**
- Science ✅ (verified by re-run of all mentioned tests)

**Summary**
Each component is in one of four states: Running (built, tested, in production or daily use), Built-not-running (complete, passes tests, not yet deployed), Designed-not-built (spec exists, not implemented), Concept-only (imagined, no spec).

**Evidence**
- Repository: TerAustralis-Incognita-Code / STATUS.md (fleet-wide ledger)
- Verified: All test re-runs confirmed this session (2026-07-23)

**Discussion**

| Component | State | Status |
|---|---|---|
| Starline Weaver (P2P transport) | Built-not-running ✅ | 9 self-tests + crypto; Noise protocol |
| Decode→Ingest→Twin pipeline | Built-not-running ✅ | 4 self-tests; data flow |
| RDP (audit kernel) | Built-not-running ✅ | 31 tests (property-based); hash-chained audit log |
| Clementine (orchestration) | Built-not-running ✅ | 7 self-tests; multi-agent comms |
| CrystalBridge (MCP consent gate) | Built-not-running ✅ | 🔴 ZERO test coverage (Tier 1: add tests) |
| Crystal Runtime | Running ✅ | 75 pytest; 7 submodules (contradicts Roadmap.md) |
| Mesh stub | Built-not-running ✅ | 3 pytest; transport library |
| TypeScript SDK | Designed-not-built 🔮 | v0.5.0; Phase 1 / Mainnet HOLD |
| Clementine companion | Running ✅ | 16 pytest; most complete surface |
| Voicebox (TTS server) | Running ✅ | No tests; single file, stdlib-only |
| Demo shells | Built-not-running 🔮 | HOLD status; honest scope labeling |
| Site (SvelteKit) | Running ✅ | Type-check only; 9 routes, deployed |
| CrystalCore.OS mythos terminal | Designed-not-built 🔮 | Half game, half ML research; not wired |
| CrystalCore Framework | Running ✅ | 16 tests (via Clementine); 0.7.0 fork |
| Protocol pack | Running ✅ | 51 self-tests; strongest engineering |
| dbt emotion warehouse | Designed-not-built 🔴 | Syntax error; no data source; 0 tests |

**Summary by state:**
- Running ✅: 5 components (Clementine, voicebox, site, runtime, protocol pack)
- Built-not-running ✅: 7 components (protocol submodules, runtime, mesh) — pass tests, not deployed
- Designed-not-built 🔮: 4 components (SDK, demos, mythos, Framework) — spec exists, marked not-yet-ready
- Concept-only: None (all design has at least a spec)

**Open Questions**
- Tier 1 issues: CrystalBridge zero test coverage (security boundary); dbt warehouse SQL syntax error + no data source.

**Related Documents**
— [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Test Coverage Summary · [REPOSITORIES.md](REPOSITORIES.md) — where components live

---

## Test Coverage Summary

**Status**
- Science ✅ (all tests re-run and confirmed 2026-07-23)

**Summary**
151+ tests passing across the two living repositories. Coverage is bimodal: hand-written original code is rigorously tested; copied code and reconstructed code have none.

**Evidence**
- Repository: TerAustralis-Incognita-Code (main code repo)
- Verified: All test commands re-run this session
- Results: No inference from documentation; all reported passes confirmed by execution

**Discussion**

| Area | Mechanism | Result |
|---|---|---|
| crystal-core / clementine | selftest.py | 7 / 7 |
| crystal-core / consent_transport | selftest.py + real sockets/crypto | 9 / 9 |
| crystal-core / rdp | selftest.py + 7 property-based checks | 31 / 31 |
| crystal-core / services | selftest.py | 4 / 4 |
| runtime (7 submodules) | pytest (heavy mocking) | 75 |
| node/mesh | pytest | 3 |
| apps/clementine | pytest + conftest | 16 |
| **Total confirmed** | — | **70 passing** |

**Umbrella repo:** Legacy `tests/` existed pre-reorg; not re-run post-split. Not included in `-Code` tally.

**Bimodal distribution:**
- Hand-written original (protocol pack, runtime, Clementine): heavily tested.
- Copied code (packages/): zero coverage.
- Reconstructed code (CrystalBridge, crystalcore-os): zero coverage.

**Open Questions**
- Coverage gap: All seven `packages/` carry dead test files that nothing runs.
- Tier 1 recommendation: Add tests to CrystalBridge (security boundary).

**Related Documents**
— [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Component State Matrix · [REPOSITORIES.md](REPOSITORIES.md) — where code lives

---

## Naming Collisions Found

**Status**
- Drift ⚠️ (documented, not all resolved)

**Summary**
Several terms name more than one thing across the codebase. ADR-0004 resolved the "CrystalCore" collision with a taxonomy; others remain ambiguous.

**Evidence**
- Repository: TerAustralis-Incognita-Code (code grep + docs)
- Audit method: Textual search across both repos
- Status: Four collisions identified

**Discussion**

| Term | Meaning A | Meaning B | Notes |
|---|---|---|---|
| `crystalcore` | MCP bridge package | Clementine's internal framework | Also: game state, protocol pack (4 meanings) |
| "bridge" | MCP stdio server | Multi-agent chat bus | Unrelated, same word |
| scope / provenance | Named in `gate.py` docstring | Implemented in `runtime/coordinator.py` | Different resource models |
| "Starline" | Real P2P transport | Message bus + fictional state machine | Three meanings in two docs |

**Open Questions**
- Tier 2 recommendation: Disambiguate via taxonomy ADR (like ADR-0004 did for CrystalCore).
- Status: Not yet resolved.

**Related Documents**
— [GOVERNANCE.md](GOVERNANCE.md) — ADR-0004 (CrystalCore taxonomy pattern) · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Starline disambiguation decision gate

---

## Recommendations by Tier

**Status**
- Science ✅ (verified findings with specific, actionable proposals)

**Summary**
Fifteen recommendations across three tiers (Tier 1: days, Tier 2: weeks, Tier 3: polish).

**Evidence**
- Findings: Five key findings above + naming collisions + test coverage gaps
- Verification: Architecture audit 2026-07-23, all tests re-run

**Discussion**

**Tier 1 — Cheap, High-Value (Days, Not Weeks):**
1. Fix the repo-split documentation gap — Add dated note to `SystemMap.md` and root README; reconcile or retire `mythos/README.md`.
2. Decide `packages/` fate — Delete, or commit to thin re-exports wired into CI. Current state actively misinforms.
3. Add tests to CrystalBridge — Zero coverage on consent-gate security boundary. Tier 1 priority.
4. Fix dbt warehouse — Syntax error in `stg_emotion_labels.sql`; wire staging to JSONL or retire.

**Tier 2 — Important, More Surface Area (Weeks):**
1. Reconcile Crystal Runtime specs — Three same-day docs contradict; update `Roadmap.md` (runtime exists, 75 tests).
2. Decide `crystalcore` / `crystal-core` / `runtime` integration — Separate or integrate? Document decision.
3. Disambiguate "Starline" — Taxonomy ADR per ADR-0004 pattern.
4. Reconcile archive recovery-status docs — Two contradictory accounts of what was recovered.

**Tier 3 — Polish (Spare Afternoon):**
1. Rebuild `docs/README.md` index — Lists nine currently-missing files including `ATTRIBUTIONS.md`.
2. Fix dead links — `Access.md`, `Push.md` reference non-existent scripts/files.
3. Banner `REPO-RESTRUCTURING-PLAN.md` — Carry same "Superseded" mark as siblings.
4. Verify live site — Current audit couldn't reach it (network policy).

**Related Documents**
— [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Stage-gated decisions related to these recommendations

## Summary

**Status**
- Science ✅

**Summary**
CrystalCore.OS is in better shape than its symptoms suggest. Targeted fixes, documentation updates, and clarity on decision gates are needed, not structural redesign.

**Evidence**
- Verified engineering: real cryptography, 150+ passing tests, property-based testing on audit kernel
- Rare governance discipline: honest Science/Vision labeling, clean ADR trail
- Documentation lag: split not documented, Roadmap stale, README indices incomplete
- Specific actionable issues: `packages/` misleading, dbt syntax error, CrystalBridge untested
- Open architectural questions: repo-count decision, integration choice, Framework extract criteria

**Discussion**

**Strengths:**
- ✅ Verified engineering — real cryptography, 150+ passing tests, property-based testing
- ✅ Rare governance discipline — honest Science/Vision labeling, clean ADR trail

**Weaknesses:**
- ⚠️ Documentation lag — split not documented, Roadmap stale, README indices incomplete
- 🔴 Specific actionable issues — `packages/` misleading, dbt syntax error, CrystalBridge untested
- 🔮 Open architectural questions — repo-count decision, integration choice, Framework extract

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — system boundaries · [GOVERNANCE.md](GOVERNANCE.md) — how fixes are decided · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — decision gates · [TIMELINE.md](TIMELINE.md) — why current state exists

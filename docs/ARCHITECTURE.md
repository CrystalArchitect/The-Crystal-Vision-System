# CrystalCore.OS Architecture

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** Project-Boundaries.md, CrystalCore.md, STATUS.md, architecture-survey.md §4 · **Last verified:** 2026-07-24 · **Labels:** Science ✅ (verified, git-based) / Vision 🔮 (designed, not-built) / Drift ⚠️ (docs/code diverge) / Critical 🔴

---

## The Belt-Three Model

**Status**
- ✅ Science

**Summary**
The project organizes itself into three Belt layers: Science (repository architecture and engineering decisions), Vision (dreamed futures and mythology), and Docs-governance (decision records and policy). This is the fundamental organizational principle of the entire project.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance
- File: The-Incognita-Rule.md, Project-Boundaries.md
- Commit(s): ADR-0011 (2026-07-23)

**Discussion**
The Belt-Three model distinguishes between:
- **Science Belt:** What exists and is verified — executable code, passing tests, git history, measurement.
- **Vision Belt:** What is designed or imagined but not yet built — specifications, mythology, speculative architecture, story.
- **Docs-governance Belt:** How decisions are made — ADRs, Constitution, process documentation, amendment rules.

Every document in the repository carries a Science/Vision/Story label indicating its belt. The Incognita Rule enforces this distinction on every PR: dreamed lines never masquerade as surveyed. Contributors know immediately whether they are reading implementation fact or design speculation, which prevents the cognitive load of inferring confidence level from narrative tone.

**Related Documents**
- [GOVERNANCE.md](GOVERNANCE.md) — Incognita Rule operationalization
- [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Where Science and Vision diverge

---

## Four-Layer System Architecture

**Status**
- ✅ Science (Constitution and Archive layers)
- 🔮 Vision (Forge and Mythos layers)

**Summary**
The system divides into four conceptual layers corresponding to how the project stores and uses information: Constitution (unchanging principles), Archive (provenance), Forge (active engineering), and Mythos (story and culture).

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance + docs/architecture
- File(s): Constitution.md, archive/, mythos/
- ADR(s): ADR-0011 (2026-07-23)

**Discussion**

| Layer | Role | Status | Governed by |
|---|---|---|---|
| **Constitution** | Unchanging principles: locked names (three), honesty rule, amendment process | Science ✅ | Constitution §1–8 |
| **Archive** | Provenance snapshots and historical record: frozen repos as of 2026-07-17, local-snapshot folder, research prior to current org | Science ✅ | archive/README.md, deliberate preservation |
| **Forge** | Active engineering: the code that runs, tests that verify it, CI/CD, deployment | Science ✅ | TerAustralis-Incognita-Code repository |
| **Mythos** | Story, culture, research, public-facing narrative: the Covenant, The First Remembering, art, music | Vision 🔮 + Science ✅ | mythos/, research/, Creative Commons license |

This four-layer model prevents conflating governance with implementation, history with present state, and story with engineering. Each layer has its own rules and its own audience.

**Related Documents**
- [GOVERNANCE.md](GOVERNANCE.md) — Constitution
- [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Forge layer findings
- [TIMELINE.md](TIMELINE.md) — Archive provenance

---

## Three-Project Boundary

**Status**
- ✅ Science

**Summary**
The architecture divides into three projects, each with clear ownership and dependency rules: **TerAustralis Incognita (umbrella)** holds governance and canon; **Crystal Core** holds the engine (protocols, APIs, shared libraries); **Crystal Vision** holds the application (interfaces, user experience, companions).

**Evidence**
- Repository: TerAustralis-Incognita (umbrella) / docs/governance/Project-Boundaries.md
- File(s): Project-Boundaries.md
- Commit(s): Migration-Plan §Stages 0–2 (completed 2026-07-23)
- Audit(s): 2026-07-24 verification from both repo source trees

**Discussion**

| Project | Owns | Does not own | Where it lives |
|---|---|---|---|
| **TerAustralis Incognita (umbrella)** | Canon and law: governance, architecture documentation, ADRs, mythos, research, archive, references to engineering repos | Main app code | `CrystalArchitect/TerAustralis-Incognita` |
| **Crystal Core** | The engine: runtime, protocols, APIs, shared libraries — what other software imports and calls | User interfaces | `CrystalArchitect/TerAustralis-Incognita-Code/core/` |
| **Crystal Vision** | The user-facing application built on Crystal Core — what a human opens, reads, and steers | Engine internals | `CrystalArchitect/TerAustralis-Incognita-Code/vision/` |

**The Dependency Rule:**
1. Crystal Vision **may** depend on Crystal Core (built on top).
2. Crystal Core **never** imports Crystal Vision (no bidirectional reach).
3. Clementine (orchestration inside Core) **must not** depend on Vision (would invert the model).
4. The umbrella contains no importable app code (both engineering projects obey umbrella canon).

This boundary prevents architectural inversion and keeps concerns cleanly separated. Vision can see downward to Core's APIs; Core never reaches upward.

**Related Documents**
- [REPOSITORIES.md](REPOSITORIES.md) — Where each project lives and how they're stored
- [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Stage 3 repo-count decision

---

## Component → Project Assignments

**Status**
- ✅ Science (current placement)
- 🔮 Vision (Stage 3–4 placements)

**Summary**
Each named component has a home in one of the three projects. Some placements are definite; others remain decision points pending specific criteria.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Project-Boundaries.md
- File(s): Project-Boundaries.md (component map)
- Commit(s): Migration-Plan §Stages 1–4
- Audit(s): 2026-07-24 code repo inventory verification

**Discussion**

| Component | Described home | Project | Status | Note |
|---|---|---|---|---|
| **Clementine** (sovereign companion + embedded **CrystalCore Framework**) | `vision/apps/clementine/` | **Crystal Vision** | Science ✅ | Whole product per maintainer directive; Framework keeps ADR-0004 name; split criteria operationalized in Migration-Plan §Stage 3 |
| **CrystalCore Protocol pack** (Starline Weaver, Decode→Ingest→Twin pipeline, Consent Transport, RDP) | `src/crystal-core/` | **Crystal Core** | Science ✅ | Protocol machinery other components call |
| **Clementine** (orchestration, AI-to-AI comms coordination) | `bus/` inside protocol pack | **Crystal Core** (logical component) | Science ✅ | Named component, not a repository; per maintainer directive |
| **CrystalBridge** (fail-closed MCP consent gate + profile configs) | `src/crystalcore/`, `src/profiles/` | **Crystal Core** | Science ✅ | Integration/API layer |
| **Mesh stub** (shared transport library) | `src/node/mesh/` | **Crystal Core** | Science ✅ | Stub only today |
| **TypeScript SDK** (client API scaffold) | `src/sdk/typescript/` | **Crystal Core** | Science ✅ | Phase 1 / Mainnet HOLD |
| **Demo shells** (`crystal-interface`, `vision-web`) | `src/apps/crystal-interface/`, `src/apps/vision-web/` | **Crystal Vision** | Science ✅ | Applications on simulated data; Authority HOLD labels; brand-facing is not code ownership |
| **Voicebox** (local MCP text-to-speech server) | `src/apps/voicebox/` | **Crystal Vision** | Science ✅ | Judgment call at boundary rule's edge (called via MCP, output is speech for human) |
| **CrystalCore.OS mythos terminal** (playable story, not infrastructure) | `src/crystalcore-os/` | **Umbrella (mythos area)** | Science ✅ | Canon-as-code; placement revisitable at Migration-Plan Stage 1 |
| **Site** (teraustralis.com.au) | `src/site/` | **Open decision point** | Vision 🔮 | Recommendation: Crystal Vision (public face); Pages/CNAME moved to `-Code` Stage 2 (2026-07-23) |
| **dbt emotion warehouse** | `dbt/crystalcore_emotion_warehouse/` (in umbrella repo) | **Open decision point** | Vision 🔮 | Recommendation: Crystal Core's data layer eventually; acceptable to leave in umbrella as research artifact |
| **Documentation, governance, ADRs** | `docs/` | **Umbrella** | Science ✅ | Including this charter |
| **Mythos content and art** | `mythos/` | **Umbrella** | Science ✅ | Own license area (LICENSE-CONTENT.md); may point at code, never speaks for it |
| **Research** (Seven Sisters cycle, design exploration) | `research/` | **Umbrella** | Science ✅ | Not production; promotion is deliberate, reviewed act |
| **Archive** (provenance only) | `archive/` | **Umbrella** | Science ✅ | Checkpointed snapshots, never edited |
| **Assets, examples index** | `assets/`, `examples/` | **Umbrella** | Science ✅ | Runnable demos live with their code; index stays here |

Components know their home and their dependency direction. New work goes into the project that owns it; cross-project features go through carefully reviewed imports.

**Related Documents**
- [REPOSITORIES.md](REPOSITORIES.md) — Where each project is stored
- [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Component integration findings

---

## Six-Repository Constellation

**Status**
- ✅ Science

**Summary**
The architecture spans six repositories: three living (active), three frozen (provenance only). The three living repos form the complete canonical system. The three frozen repos preserve pre-reorg code and are never edited.

The portfolio is larger than the architecture. Twelve repositories exist as at 2026-07-29; the other six post-date this model and are not fitted to it. See [REPOSITORIES.md](REPOSITORIES.md) for the list and the Archive's `02-REPOSITORY-MAP.md` for the canonical map, which covers eleven of the twelve.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Project-Boundaries.md
- Audit(s): 2026-07-24 direct inspection of both living repos + GitHub API ls-remote for frozen
- Git state: Frozen repos tagged with `-safe-2026-07-17` suffix

**Discussion**

### Living repositories

| Repository | Role | Contents | CI/CD |
|---|---|---|---|
| `CrystalArchitect/TerAustralis-Incognita` | The umbrella: governance, ADRs, architecture docs, research, provenance mirrors, mythos | docs/, mythos/, research/, archive/, assets/ | Markdown lint + external link check (2026-07-24) |
| `CrystalArchitect/TerAustralis-Incognita-Code` | The software per Migration-Plan Stages 1–2: core/ (engine) + vision/ (application) | core/, vision/, LICENSE, CNAME, .github/workflows/ | compileall, 4 self-test suites (core/), Clementine pytest, mesh pytest; Pages deploy |
| `CrystalArchitect/CrystalCore.OS-the-Crystal-Architecture-Archive` | The system ledger: one fleet-wide STATUS.md (state, receipts, known unknowns across all repos) | STATUS.md | None (ledger only) |

### Frozen provenance repositories

| Repository | Checkpointed | Code rescued/migrated to |
|---|---|---|
| `The-Crystal-Vision` (tag `vision-safe-2026-07-17`) | Codex site + Clementine companion; complete **crystalcore v0.13.4 bytecode** | Ancestor of Clementine's embedded framework (0.7.0 line; 0.13.4 extras unreconciled — see OPEN-DECISIONS.md) |
| `crystalcore` (tag `crystalcore-safe-2026-07-17`) | The Songline protocol pack (pre-reorg ancestor) | Direct ancestor of core/crystal-core (SonglineBus → Starline Weaver) |
| `crystal-vision` (tag `crystal-vision-safe-2026-07-17`) | Static demo shell (Grok build) | Direct ancestor of vision/apps/crystal-interface |

The living repos carry the present state and active development. The frozen repos are read-only record; nothing is lost, everything is traceable to its provenance SHA.

**Related Documents**
- [REPOSITORIES.md](REPOSITORIES.md) — Role and current state of each
- [TIMELINE.md](TIMELINE.md) — How the six-repo constellation came to be

---

## Open Decisions: Stage 3–4

**Status**
- 🔮 Vision

**Summary**
Three placements and one architectural choice remain to be decided at specific stages.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Migration-Plan.md
- ADR(s): ADR-0011 (maintainer decision record, 2026-07-23)

**Discussion**

1. **Stage 3 — Repo-count decision:** Whether to split `-Code` into separate `core` and `vision` repositories. Split only when release cadences diverge, licensing changes, external contributors need scoping, or CI/product surfaces diverge enough to fight each other. Until then: one repository, two top-level areas, dependency rule enforced in review.

2. **Stage 3 — Clementine framework extraction:** Whether to separate CrystalCore Framework from Clementine. Extract into Crystal Core only when a second companion app needs it, an external consumer imports it, or independent versioning/release pressure appears. Until then: Clementine stays whole in Crystal Vision, per maintainer directive (recorded ADR-0011).

3. **Stage 4 — Site placement:** Recommendation is Crystal Vision (public face). Pages/CNAME mechanics solved Stage 2 (moved to `-Code` 2026-07-23).

4. **Stage 4 — dbt warehouse:** Recommendation is Crystal Core's data layer eventually. Acceptable to leave in umbrella as research artifact until engineering repo is real.

These decisions remain open precisely because they depend on future conditions (release patterns, external adoption) that can't be evaluated today. They're not design flaws; they're design questions held in abeyance.

**Related Documents**
- [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Full decision gates and criteria

---

## Cross-Repository Content Pipeline

**Status**
- ✅ Science

**Summary**
The only automated cross-repo dependency is the public site: canonical mythology in the umbrella (`mythos/`) must be copied into the application repo (`vision/site/src/content/`) to be published.

**Evidence**
- Repository: Both living code repos
- File(s): vision/site/, docs/governance/Project-Boundaries.md
- Commit(s): Established Stage 2 (2026-07-23)

**Discussion**

```
mythos/ (umbrella, canonical)
   → copied by hand into vision/site/src/content/ (-Code)
   → built by deploy.yml
   → GitHub Pages
   → www.teraustralis.com.au
```

The site renders *copies* of canonical content, not the canon directly. This is a known, deliberate drift risk: new mythos content is not public until its copy step happens. The First Remembering (canonical in umbrella) is not yet copied to site as of 2026-07-24.

**Related Documents**
- [REPOSITORIES.md](REPOSITORIES.md) — Cross-repo dependencies
- [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — Site sync decision gate
- [TIMELINE.md](TIMELINE.md) — Stage 2 implementation

---

## Summary

The CrystalCore.OS architecture divides into:
- **Three layers of organization:** Belt-Three model (Science, Vision, Docs-governance)
- **Four strata of function:** Constitution (unchanging), Archive (provenance), Forge (engineering), Mythos (story)
- **Three projects with a dependency rule:** Umbrella (canon) → Core (engine) ← Vision (application)
- **Six repositories in this model:** Three living (active development + ledger), three frozen (provenance) — of twelve in the portfolio as at 2026-07-29
- **Clear component-to-project mapping** with specific decision gates for Stage 3–4 placements

This architecture is designed to prevent common failures: inversion of dependency direction, conflation of story with engineering, loss of provenance, and architectural drift hidden in narrative.

---

**See also:**
- [REPOSITORIES.md](REPOSITORIES.md) — Where each project lives
- [GOVERNANCE.md](GOVERNANCE.md) — How decisions are made
- [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Where Science and Vision diverge today

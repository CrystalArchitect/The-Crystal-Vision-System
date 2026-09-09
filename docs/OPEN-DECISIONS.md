# Outstanding Questions & Open Decisions

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** Project-Boundaries.md §Open decisions, architecture-survey.md §8 (Tier 2), Migration-Plan §Stages 3–4, technical-findings.md (cross-component analysis) · **Last verified:** 2026-07-23 · **Labels:** Vision 🔮 (decision gates specified, outcomes open)

---

## Decision Gates and Criteria

**Status**
- Vision 🔮 (decision structure defined, conditions not yet met)

**Summary**
Six decisions are deliberately held open because they depend on future conditions (release patterns, adoption patterns, organizational changes) that cannot be evaluated today. Each gate specifies what must be true to decide.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Migration-Plan.md §Stages 3–4 (gates and criteria)
- Verified: Maintainer decision record in ADR-0011 (2026-07-23)

**Discussion**
See sections below for each decision.

**Related Documents**
— Migration-Plan.md — Stage 3–4 implementation plan · ADR-0011 — maintainer decision record

---

## Stage 3 Decision 1: Repo-Count Split (Core / Vision Separation)

**Status**
- Vision 🔮 (criteria specified, conditions not yet met)

**Summary**
Should TerAustralis-Incognita-Code be split into separate `core` and `vision` repositories?

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Migration-Plan.md (Stage 3 decision gate)
- Current state: Single repository with `core/` and `vision/` top-level areas

**Discussion**

**Current state:** One repository, two top-level areas. Dependency rule (Vision → Core, never backward) enforced in code review. Shared CI/CD pipeline (compileall, 70+ tests in one run).

**Decision gate — split ONLY when at least one of these is true:**
1. Release cadences diverge (Core ships on different schedule than Vision)
2. Licensing split becomes real (ADR-0010 revisited; differentiated licenses per repo)
3. External contributors need scoping (third-party Core consumers or Vision-only contributors)
4. CI/product surfaces diverge enough to fight (tooling incompatibility, deployment separation)

**Open Questions**
- Why this matters: Repo splits are hard to undo; this gate prevents premature split based on convenience alone.

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — dependency rule · [REPOSITORIES.md](REPOSITORIES.md) — current single-repo structure

---

## Stage 3 Decision 2: Clementine Framework Extraction

**Status**
- Vision 🔮 (criteria specified, Clementine stays whole for now)

**Summary**
Should CrystalCore Framework be extracted from Clementine into Crystal Core?

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Migration-Plan.md (Stage 3 decision gate)
- Current state: Framework embedded in Clementine (core/crystalcore/mind/)

**Discussion**

**Current state:** Framework lives embedded in Clementine; carries ADR-0004 name while traveling with companion app. Clementine stays whole in Crystal Vision (per maintainer directive, recorded ADR-0011).

**Decision gate — extract Framework ONLY when at least one of these is true:**
1. A second companion app needs the Framework (establishes reusability)
2. An external consumer imports it (validates library status)
3. Independent versioning/release pressure appears (decoupling needed)

**Open Questions**
- Why this matters: Premature extraction of a library that only one app uses adds overhead without benefit.

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — component → project assignments · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — Framework lineage (0.7.0 fork, 0.13.4 unreconciled)

---

## Stage 3 Decision 3: Frozen Repositories' End State

**Status**
- Vision 🔮 (three options specified, decision held open)

**Summary**
What should happen to the three frozen provenance repositories (The-Crystal-Vision, crystalcore, crystal-vision)?

**Evidence**
- Repository: All three frozen repos (tagged `-safe-2026-07-17`)
- Current state: Unarchived, never edited; code rescued into living repos

**Discussion**

**Options:**

| Option | Mechanism | Benefit | Downside |
|---|---|---|---|
| A: GitHub Archive | Set read-only flag via API/Settings | Makes intent explicit; prevents edits; discoverable | One-way operation; minimal reversibility |
| B: Leave as-is | Keep current state (unarchived, live-looking) | Fully reversible; low commitment | Intent not explicit; relies on discipline |
| C: Archive to external | Move to cold storage (AWS S3, tarball) | Frees GitHub quota; reduces noise | Harder to query via git; less discoverable |

**Decision criteria:** No explicit gate (other than "sometime Stage 3+"). Maintainer decision.

**Open Questions**
- These repos are provenance only; their end state should reflect that clearly without taking them completely offline.

**Related Documents**
— [REPOSITORIES.md](REPOSITORIES.md) — frozen repos section · [TIMELINE.md](TIMELINE.md) — provenance snapshots

---

## Stage 4 Decision 1: Site Placement and Content Sync

**Status**
- Vision 🔮 (recommendation made, placement Stage 2, sync open)

**Summary**
Where should the public site source live? How should canonical mythos content flow to the public site?

**Evidence**
- Repository: TerAustralis-Incognita + TerAustralis-Incognita-Code
- Current state: Site source at `vision/site/` in -Code (moved Stage 2, 2026-07-23)
- Known gap: The First Remembering (canonical) not yet copied to site (2026-07-24)

**Discussion**

**Placement:** Site source lives at `vision/site/` in TerAustralis-Incognita-Code (moved Stage 2, 2026-07-23). Pages deploy is set up there. **Recommendation:** Crystal Vision (it is the public face). ✅ Implemented Stage 2.

**Content sync (current state):** Manual copy required: `mythos/` (umbrella) → `vision/site/src/content/` (Code) → build → deploy.

**Content sync options:**

| Option | Mechanism | Benefit | Downside |
|---|---|---|---|
| A: Manual copy (current) | Maintainer copies files, commits to `-Code` | Explicit, reviewable, low overhead | Delay; manual process prone to drift |
| B: CI automation | Script in CI fetches from umbrella, commits | Eliminates manual step; auto-sync | Cross-repo CI coupling; needs permissions |
| C: Build-time fetch | Site build fetches at SvelteKit build time | No stored drift; source always current | Build dependency on umbrella availability |

**Recommendation:** For now, improve A via pre-deployment checklist. B (CI automation) is Stage 3–4 enhancement.

**Open Questions**
- Canonical content not published is a known gap; the pipeline should make publishing explicit and reliable.

**Related Documents**
— [REPOSITORIES.md](REPOSITORIES.md) — content pipeline · [ARCHITECTURE.md](ARCHITECTURE.md) — three-project boundary

---

## Stage 4 Decision 2: dbt Emotion Warehouse

**Status**
- Vision 🔮 (recommendation made, placement deferred)

**Summary**
What should happen to `dbt/crystalcore_emotion_warehouse/`?

**Evidence**
- Repository: TerAustralis-Incognita-Code
- Current state: Warehouse in umbrella (inherited pre-reorg); zero data source; SQL syntax error
- Related: dbt_integration.py writes JSONL but nothing reads it

**Discussion**

**Current state (2026-07-24):** Warehouse lives in umbrella repo. Staging models are hardcoded null CTEs. Contains SQL syntax error in `stg_emotion_labels.sql`.

**Recommendation:** Crystal Core's data layer eventually; acceptable to leave in umbrella as research artifact until engineering repo is real.

**Open Questions**
- Before Stage 4 (Tier 1 action): Fix SQL syntax error in `stg_emotion_labels.sql`; decide whether to wire staging models to JSONL files `dbt_integration.py` already writes, or retire until ready.
- Why this matters: Project is not currently emitting emotion predictions this warehouse would process. It's engineering-ready code for a feature that doesn't exist yet.

**Related Documents**
— [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — warehouse state, Tier 1 recommendations

---

## Unresolved Component Integration Questions

**Status**
- Vision 🔮 (patterns identified, decision needed)

**Summary**
Three core systems share vocabulary but not code. They are either intentionally separate or genuinely under-integrated. This requires explicit decision.

**Evidence**
- Repository: TerAustralis-Incognita-Code / src/
- Audit finding: "The three components that look like they should be layers of one system are not integrated" (architecture-survey.md §4)

**Discussion**

| Component | What | Coverage | Integration |
|---|---|---|---|
| `src/crystalcore` | CrystalBridge (MCP consent gate) | 🔴 Zero | Isolated |
| `src/crystal-core` | Protocol pack (Starline, RDP, services, Clementine) | ✅ 51 tests | Isolated from crystalcore, internally coherent |
| `src/runtime` | Service orchestration (coordinator, registry, events) | ✅ 75 tests | Isolated; two textual mentions (both comments) |

**Open Questions**

**Tier 2 recommendation:** Make an explicit call:
- **Option A:** Intentionally separate systems — document why they're separate; stop echoing vocabulary across them
- **Option B:** Genuinely integrate them — start from the one demo-only cross-import that already proves it's possible

**Why this matters:** Ambiguous relationships encourage developers to write integration code in the wrong places.

**Related Documents**
— [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — integration audit findings · [ARCHITECTURE.md](ARCHITECTURE.md) — component boundaries

---

## Naming Disambiguation: "Starline"

**Status**
- Vision 🔮 (collision documented, taxonomy needed)

**Summary**
What does "Starline" mean? Three meanings appear in two similarly-titled documents.

**Evidence**
- Repository: TerAustralis-Incognita-Code + TerAustralis-Incognita
- Audit finding: "Three meanings in two similarly-titled docs" (architecture-survey.md, Tier 2)

**Discussion**

**Current collision:**
- **Meaning A:** Real P2P transport (consent_transport, Noise protocol)
- **Meaning B:** Multi-agent message bus ("Starline Weaver")
- **Meaning C:** Fictional game state machine (mythos terminal, `crystalcore-os.py`)

Three meanings appear in `STARLINE.md` vs. `STARLINE-WEAVE-PROTOCOL.md`.

**Open Questions**

**Tier 2 recommendation:** Disambiguate the way ADR-0004 disambiguated "CrystalCore" — write a taxonomy ADR for "Starline," lock the meanings, prevent future proliferation.

**Candidates for renaming (to clarify, not change meaning):**
- **Meaning A:** "Consent Transport" or "[name TBD — must not reference Songline, see Indigenous-Data-Sovereignty.md]" (already has clear module names)
- **Meaning B:** "Starline Weaver" (already distinguished in one document)
- **Meaning C:** "[name TBD — must not reference Songline, see Indigenous-Data-Sovereignty.md]" (fictional, distinct from protocol names; something built on "Starline"/"Dreamline" fits the project's own coinages better)

> **Struck 2026-08-26:** this list previously named "SonglineTransport" (Meaning A) and "Songline Network" (Meaning C) as candidates. Both are struck — "Songline" is never a component name in this project ([`docs/governance/Indigenous-Data-Sovereignty.md`](governance/Indigenous-Data-Sovereignty.md), [`mythos/NAMES.md`](../mythos/NAMES.md)), and unlike the historical `SonglineBus` references elsewhere in this repo's genealogy docs, this was a live proposal for a name not yet built — exactly the case the rule exists to stop before it ships. The actual replacement name is left open for the maintainer to decide.

**Why this matters:** Vocabulary collisions force readers to infer from context, making specifications harder to search and understand.

**Related Documents**
— [GOVERNANCE.md](GOVERNANCE.md) — ADR-0004 precedent · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — naming collision audit

---

## Lineage Reconciliation: 0.7.0 vs. 0.13.4 Fork

**Status**
- Vision 🔮 (lineage documented, reconciliation deferred)

**Summary**
How should the pre-reorg `crystalcore` versions (0.7.0 vs. 0.13.4) be reconciled?

**Evidence**
- Repository: The-Crystal-Vision (frozen repo, tag `vision-safe-2026-07-17`)
- Current state: Clementine's Framework forked 0.7.0 line (16 tests passing)
- Archived state: 0.13.4 bytecode rescue in frozen repo (spell-checking, audio effects, GUI)

**Discussion**

**Current state (2026-07-24):**
- Clementine's embedded Framework forked 0.7.0 line (tested, integrated, 16 tests)
- The-Crystal-Vision frozen repo contains complete 0.13.4 bytecode rescue
- 0.13.4 extras (SpaceXAI provider, `node.py`, `status.py`, CLI) remain unreconciled

**Open Questions**
1. Should 0.13.4 features be integrated into the 0.7.0 fork running in Clementine?
2. Are the 0.13.4 extras valuable or historical?
3. What does the 0.13.4 → 0.7.0 fork represent architecturally?

**Why this matters:** The lineage is historically documented (in frozen repo tags); the current working version is known (0.7.0 fork). The reconciliation question is open but not urgent (both states preserved).

**Tier 2 recommendation:** Document the design intent (was 0.7.0 a deliberate simplification? Architectural choice?). If 0.13.4 features should be ported, that becomes implementation work.

**Related Documents**
— [REPOSITORIES.md](REPOSITORIES.md) — frozen repo notes · [TIMELINE.md](TIMELINE.md) — version history

---

## Archive Recovery Status Reconciliation

**Status**
- Drift ⚠️ (two contradictory documents, reconciliation needed)

**Summary**
What was recovered from the pre-reorg era? Two archive documents contradict each other about whether specific code was recovered or lost.

**Evidence**
- Repository: TerAustralis-Incognita / archive/
- Conflict: `archive/2026/local-snapshot-2026-07-17/README-SNAPSHOT.md` vs. sibling `crystalcore-v0.13/RECOVERY-STATUS.md`
- Same date, contradictory claims

**Discussion**

**Current conflict:**
- `README-SNAPSHOT.md` lists `status.py` and SpaceXAI provider as "unrecoverable"
- Sibling `RECOVERY-STATUS.md` says both were "fully recovered"

A reader who opens only the first file walks away with wrong picture. Nobody reconciled the two.

**Open Questions**
- Tier 3 recommendation: Reconcile the two documents; mark the stale one with a date and pointer.
- Why this matters: Historical record should not contradict itself about what was lost and what was found.

**Related Documents**
— [TIMELINE.md](TIMELINE.md) — archive checkpoints · [REPOSITORIES.md](REPOSITORIES.md) — frozen provenance repos

## Summary

**Status**
- Vision 🔮

**Summary**
Eight decisions are deliberately held open because they depend on future conditions or architectural judgment that cannot be made from current state alone. None are blockers.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Migration-Plan.md (Stage 3–4 gates)
- Verified: Maintainer decision record in ADR-0011 (2026-07-23)

**Discussion**

| Decision | Gate | Status | Priority |
|---|---|---|---|
| Stage 3: Split core/vision repos | Release cadences diverge OR licensing splits OR external scope OR CI/product separation | Vision 🔮 | Stage 3 |
| Stage 3: Extract Framework | Second app OR external consumer OR versioning pressure | Vision 🔮 | Stage 3 |
| Stage 3: Frozen repos end-state | Maintainer choice (no explicit gate) | Vision 🔮 | Stage 3 |
| Stage 4: Site content sync | Improve manual process now; CI automation Stage 3–4 | Vision 🔮 | Stage 4 |
| Stage 4: dbt warehouse | Fix SQL error + wire to JSONL or retire | Vision 🔮 | Stage 4 (Tier 1) |
| Tier 2: Component integration | Intentionally separate or integrate? | Vision 🔮 | Tier 2 (weeks) |
| Tier 2: Starline disambiguation | Write taxonomy ADR | Vision 🔮 | Tier 2 (weeks) |
| Tier 2: 0.7.0 vs 0.13.4 fork | Document design intent + port decision | Vision 🔮 | Tier 2 (weeks) |
| Tier 3: Archive recovery conflict | Reconcile two contradictory docs | Drift ⚠️ | Tier 3 (polish) |

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — component map · [GOVERNANCE.md](GOVERNANCE.md) — decision process · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — where decisions touch practice · [TIMELINE.md](TIMELINE.md) — why decisions are needed

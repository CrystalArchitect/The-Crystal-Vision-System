# Governance Reference

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** ADR-0001 through ADR-0011, Constitution.md, The-Incognita-Rule.md · **Last verified:** 2026-07-23 (ADR dates) · **Labels:** Science ✅ / Vision 🔮 / Locked (immutable except via Constitution §8)

---

## The Incognita Rule: Honesty Doctrine

**Status**
- Science ✅ (operationalized since project inception)

**Summary**
The single governing rule of the project: always mark which lines are dreamed and which are surveyed, and never let a dreamed line pretend it was measured. This is operationalized as mandatory Science/Vision/Story labels on every PR and throughout documentation.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/The-Incognita-Rule.md
- Enforced: Every PR carries a Mode header (Science / Vision / Story)
- Audit finding: "The honesty discipline is the project's best asset" (architecture-survey.md §2)

**Discussion**

The rule distinguishes three states:
- **Science:** What exists and is verified — code that runs, tests that pass, git history, measurement.
- **Vision:** What is designed but not yet built — specifications, storytelling, hypothetical futures, "we plan to."
- **Story:** Mythology, cultural narrative, non-engineering knowledge — the Covenant, art, research, lived experience.

Every statement in the repository is labeled with its state. Documentation does not conflate "we built" with "we want to"; code does not pose as design.

**Operationalization:** Every PR carries a Mode header:
```
Mode: [Science | Vision | Story]

Description of what's changing and why.
```

This forces the author to declare upfront: are you shipping implementation, adding spec, or expanding story? Readers know immediately whether they're reading executable fact or design speculation. The rule is rarely broken (audit rated "real and rare" discipline).

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — Belt-Three model · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — where Science and Vision diverge today

---

## Locked Names (Constitution §1)

**Status**
- Locked (immutable except via Constitution §8 amendment)

**Summary**
Three names are locked by Constitution §1 and carry specific, narrow meanings. No new component takes a locked name; they are reserved.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Constitution.md §1
- Enforced by: ADR-0004 (naming taxonomy lock), ADR-0007 (spelling correction)

**Discussion**

| Name | Meaning | Status |
|---|---|---|
| **TerAustralis Incognita** | Outer civilizational vision; the Unknown Southern Land awakening | Locked ✅ |
| **CrystalVision** | Sensing/dreaming/directing interface; Crystal ↔ Lattice | Locked ✅ |
| **CrystalCore.Lattice** | Substrate: multi-AI weave, memory, ontology, activation | Locked ✅ |

These names are reserved and cannot be reused. Attempts to name a new component "CrystalCore-Something" require a new ADR (per ADR-0004).

**Related Documents**
— ADR-0004 — naming taxonomy lock · ADR-0007 — spelling correction · IP-LICENSING.md — naming debts

---

## The Four-Branch CrystalCore Taxonomy (ADR-0004)

**Status**
- Science ✅ (adopted 2026-07-23)

**Summary**
"CrystalCore" already names multiple things. To prevent future proliferation, the project adopted a canonical four-branch taxonomy locking those meanings and banning any fifth.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/ADR-0004.md (2026-07-23)
- Reference: docs/vision/CrystalCore.md (taxonomy source of truth)
- Status: Adopted, no violations found in review

**Discussion**

| Branch | What | Where |
|---|---|---|
| **CrystalCore Framework** | Clementine's embedded engine (forked 0.7.0) | core/crystalcore/mind/ |
| **CrystalCore Protocol** | Protocol pack (Starline Weaver, RDP, Consent Transport) | core/crystal-core/ |
| **CrystalBridge** | MCP consent gate (integration layer) | core/crystalcore/ |
| **CrystalCore OS** | Platform/governance architecture | Umbrella governance |

**The collision:** "CrystalCore.OS" (mythos terminal) nearly collides with "CrystalCore OS" (platform name). ADR-0004 documents this as the taxonomy's "one open case" rather than papering over it.

**The ban:** No future runtime component becomes a fifth "CrystalCore." Candidates raised in review (Crystal Runtime, Crystal Nexus, Crystal Coordinator, Crystal Kernel) were rejected. New components must self-describe their role.

**Related Documents**
— ADR-0004 — original decision · IP-LICENSING.md — naming debts and taxonomy enforcement

---

## Architecture Decision Records (ADRs 0001–0011)

**Status**
- Science ✅ (all adopted, numbered sequentially, procedurally spotless)

**Summary**
Eleven Architecture Decision Records govern the project. Each is a dated decision on a specific topic; supersession is always explicit; the trail is complete and auditable.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/
- Verified: Numbers never reused, status labels match headers exactly, procedural review trail complete
- Licensing evolution: ADRs 0006–0010 show real-time conflict resolution

**Discussion**

| ADR | Date | Topic |
|---|---|---|
| ADR-0001 | 2026 | Adopt monorepo architecture |
| ADR-0002 | 2026 | Keep `mythos/` as peer of `docs/` and `src/` |
| ADR-0003 | 2026 | Move code into `src/`; preserve `__file__`-relative paths |
| ADR-0004 | 2026-07-23 | Lock four-branch CrystalCore taxonomy; ban future CrystalCore-* names |
| ADR-0005 | 2026 | AI Orchestrator: recommend-then-human-decides, not autonomous dispatch |
| ADR-0006 | 2026 | Dual-license: Apache-2.0 code / CC BY-NC-ND mythos; IP principles |
| ADR-0007 | 2026 | Correct name to "TerAustralis Incognita" (one 'a') per ABN |
| ADR-0008 | 2026 | Supersede ADR-0006 §1: CC BY-NC-ND 4.0 for all code |
| ADR-0009 | 2026 | Reconcile same-day licensing collision (three uncoordinated sessions) |
| ADR-0010 | 2026 | Close licensing: uniform CC BY-NC-ND 4.0 for whole repository |
| ADR-0011 | 2026-07-23 | Adopt three-project boundary model + Stage-gated migration plan |

**Key attributes:** Procedural integrity (sequential, never reused), explicit supersession, consistent status headers. Licensing evolution (ADRs 0006–0010) documents real-time conflict resolution. Naming governance (ADR-0004, ADR-0007) locks critical names. Architecture (ADR-0011) establishes current three-project boundary, reframes ADR-0001.

**Related Documents**
— Individual ADRs in `docs/adr/` — source files · IP-LICENSING.md — ADRs 0006–0010 licensing trail

---

## Amendment Process (Constitution §8)

**Status**
- Science ✅ (established governance process)

**Summary**
Changes to locked names (Constitution §1) require a §8 amendment — a higher gate than a regular ADR. Everything else is amendable by new ADR.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Constitution.md §8
- Enforced by: Project-Boundaries.md (amendment process noted)

**Discussion**

| Type of change | Approval gate | Mechanism |
|---|---|---|
| Locked names (Constitution §1) | §8 amendment (highest) | Dated amendment with explicit rationale |
| Architecture decisions | New ADR (standard) | Numbered sequentially, dated, procedurally reviewed |
| Policy clarifications | PR or amendment (lower) | Comments in docs or new ADR if decision |
| Documentation corrections | PR (no special gate) | Ordinary code review, Mode header |

Locked names stay locked. Architecture questions get recorded in the ADR trail so future decisions can reference why earlier choices were made.

**Related Documents**
— Constitution.md §8 — amendment rules · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — decisions awaiting future choices

---

## Decision Audit Trail

**Status**
- Science ✅

**Summary**
The 11 ADRs plus the Constitution form a complete, auditable trail of how the project's governance evolved.

**Evidence**
- Architecture-survey.md §2 audit findings
- ADR repository: docs/adr/ (all 11 ADRs in sequence)

**Discussion**

**Key findings:**
- ✅ "The governance discipline is real and rare."
- ✅ "Formal Science/Vision/Story labeling, honestly applied almost everywhere it counts."
- ✅ "ADR trail procedurally spotless even when subject matter (licensing) was chaotic."

Future contributors can read the trail and understand not just *what* the project decided, but *why*, in which order, and what the prior state was.

**Related Documents**
— docs/adr/ — complete ADR trail · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — future decision gates

---

## Summary

**Status**
- Science ✅

**Summary**
CrystalCore.OS governance is built on five foundations: the Incognita Rule, three locked names, a four-branch CrystalCore taxonomy, eleven procedurally clean ADRs, and a Constitution §8 amendment process for the highest-priority changes.

**Evidence**
- The Incognita Rule: operationalized on every PR since project inception
- Locked names: Constitution §1 (immutable except via §8 amendment)
- CrystalCore taxonomy: ADR-0004 locks four branches, bans a fifth
- ADR trail: ADR-0001 through ADR-0011 (11 decisions, complete sequence)
- Amendment process: Constitution §8 (highest gate for locked names)

**Discussion**

This governance prevents:
- Naming collisions (four-branch taxonomy locks CrystalCore meanings)
- Licensing churn (ADR trail documents all licensing changes)
- Architectural inversion (clear dependency rules in three-project model)
- Loss of decision history (auditable ADR trail with explicit supersession)

**Related Documents**
— [ARCHITECTURE.md](ARCHITECTURE.md) — Belt-Three model operationalization · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — where governance rules meet reality · [IP-LICENSING.md](IP-LICENSING.md) — licensing ADR trail · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — decisions awaiting future conditions

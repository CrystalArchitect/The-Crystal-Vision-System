# IP, Licensing & Naming Debts

This knowledge base documents the CrystalCore.OS architecture **exactly as it exists**, not as it might be redesigned. It is a reconstruction of verified implementation, designed decisions, and remaining open questions — not a proposal for what the system should become.

> **Note (2026-07-24):** a second knowledge base, built independently, also exists at `CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/`. When the two disagree, that one governs — see `docs/README.md`'s "Relationship to the Archive repo's knowledge base."

**Source documents:** ADR-0006, ADR-0008, ADR-0009, ADR-0010 (licensing), ADR-0004, ADR-0007 (naming), Constitution §7, Migration-Plan debts register · **Last verified:** 2026-07-23 (ADR dates) · **Labels:** Science ✅ / Vision 🔮 / Locked / Resolved / Outstanding

---

## Current License: Uniform CC BY-NC-ND 4.0

**Status**
- Science ✅ (adopted ADR-0010, 2026-07-23)

**Summary**
All code and documentation in both living repositories are licensed under Creative Commons BY-NC-ND 4.0 — uniform, no differentiation. This resolved three years of uncoordinated licensing attempts.

**Evidence**
- Repository: TerAustralis-Incognita-Code / LICENSE (top level)
- ADR trail: ADR-0006 → ADR-0008 → ADR-0009 → ADR-0010 (final resolution)
- Date: ADR-0010 adopted 2026-07-23

**Discussion**

| Element | License |
|---|---|
| All `.py` code | CC BY-NC-ND 4.0 |
| Documentation (docs/) | CC BY-NC-ND 4.0 |
| Mythos (mythos/) | CC BY-NC-ND 4.0 |
| Research (research/) | CC BY-NC-ND 4.0 |

**Evolution:**
- **ADR-0006** (2026): Original — Apache-2.0 for code, CC BY-NC-ND for mythos
- **ADR-0008** (2026): Supersede ADR-0006 §1 — all code to CC BY-NC-ND 4.0
- **ADR-0009** (2026): Reconcile same-day collision (three sessions + one push in ~45 min)
- **ADR-0010** (2026-07-23): Final — uniform CC BY-NC-ND 4.0 for whole repository

The license is single, clear, and immutable without a new ADR. Anyone using the code knows immediately what restrictions apply.

**Related Documents**
— ADR-0006, ADR-0008, ADR-0009, ADR-0010 — ADR trail · Constitution §8 — amendment process

---

## Intellectual Property Principles (ADR-0006 Survivor)

**Status**
- Locked (immutable without ADR)

**Summary**
ADR-0006 established IP principles that survive all three licensing updates. These are standalone governance statements, not overridden by ADR-0010's license change.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/ADR-0006.md §IP Principles and Trademark sections
- Date: Established 2026 with ADR-0006; explicitly preserved despite ADR-0008/ADR-0010 updates

**Discussion**

| Principle | Meaning |
|---|---|
| No third-party trademarks | All identifiers are original; no third-party marks claimed or embedded |
| Attribution required | Use requires attribution (CC BY-NC-ND 4.0 requirement) |
| Non-commercial only | No commercial redistribution without explicit approval |
| No derivative licensing | Derivatives keep same CC BY-NC-ND 4.0 license (ND = No Derivatives) |

The project's IP stance is consumer-protective and contributor-accessible (non-commercial, open-source, attribution preserved).

**Related Documents**
— ADR-0006 — original IP principles decision

---

## The Four-Branch CrystalCore Taxonomy Lock (ADR-0004)

**Status**
- Locked (immutable without ADR)

**Summary**
Four branches exhaust all current "CrystalCore" uses. No new component becomes a fifth "CrystalCore." This prevents naming collision and keeps the taxonomy stable.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/ADR-0004.md (2026-07-23)
- Reference: docs/vision/CrystalCore.md (taxonomy source of truth)

**Discussion**

| Branch | What | Owner |
|---|---|---|
| CrystalCore Framework | Clementine's embedded engine (forked 0.7.0) | Crystal Vision |
| CrystalCore Protocol | Starline Weaver, RDP, Consent Transport | Crystal Core |
| CrystalBridge | MCP consent gate | Crystal Core |
| CrystalCore OS | Platform/governance architecture | Umbrella |

**The ban:** No future components get a CrystalCore name. Candidates raised in review (Crystal Runtime, Crystal Nexus, Crystal Coordinator, Crystal Kernel) were all rejected. New components must self-describe their role.

**Open Questions**
- The mythos terminal (`CrystalCore.OS`) nearly collides with platform name (`CrystalCore OS`). Documented as the taxonomy's "one open collision" rather than silently resolved.

The four branches are locked; future naming is disambiguated at design stage.

**Related Documents**
— ADR-0004 — original taxonomy decision · [GOVERNANCE.md](GOVERNANCE.md) — CrystalCore taxonomy rules

---

## Naming Debts & Resolved Issues

**Status**
- Science ✅ (verified through git, PyPI checks, and ADR trail)

**Summary**
The project has resolved two major naming debts and carries two outstanding debts with clear stage gates.

**Evidence**
- Repository: TerAustralis-Incognita / docs/governance/Migration-Plan.md (debts register)
- Verified: 2026-07-23 and 2026-07-24

**Discussion**

**Resolved Naming Debts ✅**

| Debt | Status | Resolution |
|---|---|---|
| GitHub slug `TeraAustralis-Incognita` (double-a) | ✅ Resolved | GitHub API returned `CrystalArchitect/TerAustralis-Incognita` (one 'a') per ADR-0007; confirmed PR #48 creation 2026-07-23 |
| PyPI package names `teraaustralis-*` (double-a) | ✅ Resolved | Zero git tags ever pushed; PyPI names unclaimed (404). Workflows removed Stage 2; corrected names (`teraustralis-*`) free to reserve |

**Outstanding Naming Debts 🔮**

| Debt | Location | Constraint | Gate |
|---|---|---|---|
| `corpus/` as surface of truth | Constitution §7 | Never built; requires §8 amendment | Amendment text proposed (not applied) |
| Stale references in `mythos/README.md` | `mythos/` | Vision-layer; needs maintainer sign-off | Vision-layer amendment, Stage 1+ with approval |

The two resolved debts are closed by git verification. The two outstanding debts require explicit governance action and are deliberately held open until their stage gates.

**Related Documents**
— [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — naming decision gates

---

## Licensing Evolution Timeline

**Status**
- Science ✅ (documented in ADR trail)

**Summary**
The project experienced real licensing chaos in the same morning. The ADR trail captures how it was resolved, not hidden.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/ (ADR-0006 through ADR-0010)
- Date: Multiple sessions on one day (2026)

**Discussion**

**Session 1: Original Decision (ADR-0006)**
- Proposal: Dual-license — Apache-2.0 for code, CC BY-NC-ND for mythos
- Result: Adopted as ADR-0006
- Issue: Three uncoordinated sessions later made incompatible choices

**Session 2: Uncoordinated Code License Change**
- Change: One session unilaterally changed code to CC BY-NC-ND 4.0
- Resolution: ADR-0008 retroactively adopted this, superseding ADR-0006 §1 (IP principles preserved)

**Session 3: Another Uncoordinated Change**
- Change: Another session created per-package differentiated licensing
- Resolution: ADR-0009 reconciled collision, chose root-license-governs

**Session 4: Final Closure (ADR-0010)**
- Decision: Uniform CC BY-NC-ND 4.0 for entire repository, no per-package differentiation
- Supersedes: ADR-0006 (license), ADR-0008, ADR-0009
- Keeps: ADR-0006 IP principles and trademark sections (standalone)

The chaos is documented, not hidden. Future contributors can read the trail and understand what went wrong, when, and how it was fixed. The Incognita Rule (Science/Vision/Story labeling) allowed this chaos to be captured honestly rather than papered over.

**Related Documents**
— ADR-0006, ADR-0008, ADR-0009, ADR-0010 — ADR trail · [GOVERNANCE.md](GOVERNANCE.md) — Incognita Rule

---

## Trademark Status

**Status**
- Locked (immutable without ADR)

**Summary**
The project uses original identifiers only; no third-party trademarks are claimed or embedded.

**Evidence**
- Repository: TerAustralis-Incognita / docs/adr/ADR-0006.md (trademark section, preserved by ADR-0010)
- Verified: No third-party marks in code, docs, or branding

**Discussion**
- **TerAustralis Incognita** — Original mark, associated with maintainer's registered ABN (ADR-0007)
- **CrystalCore** — Original mark (four-branch taxonomy, ADR-0004)
- **CrystalVision** — Original mark (locked name, Constitution §1)
- **Clementine** — Original name
- **Starline** — Original name

The project's branding is independent and protected from third-party licensing complications.

**Related Documents**
— ADR-0006 — trademark principles decision

---

## Summary

**Status**
- Science ✅

**Summary**
CrystalCore.OS licensing and naming architecture: uniform license, locked taxonomy, resolved and outstanding naming debts, original trademark identifiers.

**Evidence**
- License: CC BY-NC-ND 4.0 (ADR-0010, resolved from ADR-0006/0008/0009)
- Taxonomy: Four-branch CrystalCore lock (ADR-0004)
- Naming debts: Two resolved (GitHub slug, PyPI names), two outstanding with stage gates
- Trademarks: All original identifiers

**Discussion**

**License (Science ✅):**
- Uniform CC BY-NC-ND 4.0 (all code and docs)
- Resolved after same-day chaos documented in ADR trail
- IP principles (attribution, non-commercial, no derivatives) locked as separate governance

**Naming (Mixed Status):**
- Four-branch CrystalCore taxonomy locked (ADR-0004)
- Two major debts resolved (GitHub slug, PyPI names)
- Two outstanding debts with clear stage gates (Constitution §7, Vision-layer)

**Trademark (Locked):**
- All original identifiers; no third-party marks claimed or embedded

**Related Documents**
— [GOVERNANCE.md](GOVERNANCE.md) — locked names, Constitution §8 amendment process · [TECHNICAL-FINDINGS.md](TECHNICAL-FINDINGS.md) — where these principles meet practice · [OPEN-DECISIONS.md](OPEN-DECISIONS.md) — outstanding policy questions

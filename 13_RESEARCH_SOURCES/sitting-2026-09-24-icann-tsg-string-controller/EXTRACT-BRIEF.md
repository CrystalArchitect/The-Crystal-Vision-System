# Extract brief — string+controller integration

**Source:** ICANN TSG *gTLD Integrations with Alternative Naming Systems* — Initial Report (DRAFT 10 Aug 2026)  
**Audience for source:** ICANN org evaluating a proposed **registry service** under RSEP  
**This file:** working extract for Crystal Vision research trail · Canon: **no**

---

## 0. One-paragraph thesis

Where a gTLD (and names under it) must exist as the **same string** in the global DNS and in one or more alternative naming systems, the TSG analyzes **string+controller integration**: same string, same controlling party, with the **registry operator** coordinating so the guarantees cannot drift. Members believe this can be done without significant RSEP security/stability harm **if** controls hold. They do **not** endorse integration as such, nor claim it is the only possible mechanism.

---

## 1. Why ICANN is in the room

- Integrations of DNS gTLDs with alt naming systems are framed as a **Registry Service** (RSEP §1.1(c)): only the registry can ensure the DNS-side half.  
- Prefer this path over Registry Voluntary Commitments — too close to core resolution.  
- Bylaws §1.1(a)(i) “reasonably necessary” for openness / interoperability / resilience / security / stability of the DNS if DNS names routinely depend on uncoordinated alt systems.  
- Remit does **not** auto-expand to every naming system on the Internet (email local-parts remain the canonical analogy).

---

## 2. Hard definition

**Integrated (string+controller) iff** every same-string name across systems is always either:

1. controlled by the **same controller**, or  
2. **withheld** for exclusive possible control by that same party.

If those criteria cannot be reliably satisfied → **not** a candidate for this integration model.

### Scope conditions (problem statement)

Works for top+second level (and similar) when:

1. Operator of the service operates the **parent** level.  
2. That operator (alone) operates the alt naming system(s) (may delegate ops, not policy control).  
3. Names registered in the registry **must** integrate with the alt system(s) (including by exclusion).  
4. The name is always the **same name** in every involved system.

---

## 3. “Same name” (matching)

Process **label-at-a-time** (even if the alt system is not hierarchical):

| DNS label form | Match rule (informal) |
| --- | --- |
| Neither A- nor U-label | Case-insensitive ASCII / STD 13 |
| A-label | Alt substring is matching A-label **or** lowercased+NFC U-label that converts to that A-label |
| U-label | Alt substring is matching A-label **or** lowercased+NFC equivalent U-label |

Whole name matches only if every label matches corresponding alt substrings separated by U+002E FULL STOP at DNS label boundaries.

**IDN / LGR:** variant generation and LGR processing **MUST** occur **before** integration; multiple simultaneous normalizations are discouraged.

---

## 4. Controllers

| Level | Controller |
| --- | --- |
| TLD string | Registry operator (RO) — not the RSP; RO remains responsible |
| Names under TLD | Registrant (never the registrar-as-controller) |

RO must show **effective control** of corresponding alt-names (exclusive control of the alt system is the clearest proof): interfaces + access controls, or change-authorizing tokens only the RO can issue, or at least ability to **deny** other controls when DNS allocation would not move in parallel.

---

## 5. Name states (logical)

Useful states added beyond the old IDN VIP IIR model: **available**, **enrolled**, **allocated**, **withheld**, **active** (full/partial), **deactivated**, **disabled**, **suspended**, **blocked**.

Critical coupling rule: once allocated in ≥1 system → allocate **or withhold** in **all** integrated systems (same controller).

“Registration” language is reserved for pre-integration SRS registration workflows.

---

## 6. Two enrollment architectures

### A. SRS-primary (“plugin” alt systems)

- Enrollment = registration in Shared Registration System.  
- Alt systems populated like DNS/RDDS backends.  
- Pulls alt names under existing ICANN policies / operating conventions **if** the alt system does not undermine them.  
- Likely needs **EPP** extensions (prefer Domain Name Mapping extensions; Same Entity Set draft cited) and **RDAP** extensions (MUST publish; MUST register in IANA RDAP Extensions; reuse RECOMMENDED).  
- Cost: every alt-name must also be a **candidate** DNS name (255-octet / emoji / non-DNS forms may be impossible).  
- Existing alt names brought in must be enrolled → at least **withheld** from DNS.

### B. Distributed mode + Unified Source of Truth (USoT)

- No single SRS required; enrollment proven across distributed authorities (including blockchain / thin registries).  
- Need **one eventually-consistent USoT** so string+controller never splits.  
- Controller identity may be opaque durable / cryptographic ID (registrar or wallet); check sameness on every registration event (may be async / pendingCreate while ledgers settle).  
- Single **legal** responsible entity (RO) still required even if data and ops are distributed — cannot shed obligations onto component operators.  
- Proof burden: parties **cannot** break string+controller without controller instruction/approval.  
- Thin registries already show distributed truth (registrant data at registrar only) — contracts + USoT thinking already in play.

---

## 7. Feasibility sketches (§9)

| Mode | Idea | Catch |
| --- | --- | --- |
| DNS registry primary | All writes through SRS | Need explicit same-controller object/contact (thin registries complicate proof) |
| Alt system primary | Invert control plane | Still needs full RRR machinery; hard as a registry service |
| Bearer token unity | Cryptographic proof of control across systems (à la DCV/DNS drafts) | Contact / URS / UDRP / consensus-policy compliance for DNS-integrated-but-DNS-inactive names |

Shadow alt operation that tracks ICANN strings without integration is flagged as an unfortunate outcome if ICANN process feels too burdensome.

---

## 8. Lifecycle coupling (selected)

| Event | Rule of thumb in report |
| --- | --- |
| Allocate any system | Enroll first; withhold or allocate everywhere |
| DNS expires, alt kept | DNS stays withheld; alt may stay active |
| External deactivation / abuse / court in **any** system | Registry **MUST disable** name across systems |
| Registrar `clientHold` | SHOULD NOT auto-disable all systems; if used to disable, place hold in every system |
| Suspension (e.g. URS-class) | **MUST** apply to all naming systems at once |
| Internal transfer / registrar transfer | Hardest cases when objects split or registrant data lives only at registrar / outside SRS — USoT or contractual proof required |

---

## 9. Failure / EBERO

- Cannot weaken string+controller requirements to “make it commercial.”  
- Until experience accumulates: **RECOMMENDED** mandatory **turn-down plan** in the registry-service definition.  
- Integration appears **outside** EBERO critical functions → integration likely **does not survive** EBERO; another reason for a turn-down plan.

---

## 10. Out of scope (report §11)

1. Mere use of names inside apps when the alt system is not itself a queryable naming system for that name.  
2. Long-term business viability of non-DNS naming.  
3. Policy / competition / fitness of particular ICANN policies to a given alt system.

---

## 11. Relevance map (CVS only)

| Portfolio surface | Link strength |
| --- | --- |
| CRYSTALMATRIX “decentralized identity & naming” future bullet | Weak compass — same problem family (identifiers across systems), not an implementation claim |
| Consent Transport / Starline | Different layer (consent/movement), not DNS registry service |
| Agent / portal Zero Trust work | Adjacent only: **same-controller / unified truth** as a coherence metaphor — do not collapse ICANN RSEP into portal Z-zones |

No stamp that Crystal should apply for a gTLD or build an alt-name registry.

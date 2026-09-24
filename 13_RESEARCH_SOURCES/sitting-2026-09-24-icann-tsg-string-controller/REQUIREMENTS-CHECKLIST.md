# Requirements checklist — string+controller (from TSG initial report)

**Use:** observer / applicant reading aid · not ICANN legal advice · Canon: **no**  
**Source stamp:** DRAFT 10 Aug 2026 initial report (RFC 2119 language as in source)

Legend: **M** = MUST / SHALL · **S** = SHOULD / RECOMMENDED · **O** = MAY / OPTIONAL · **Gate** = fail → not a candidate

---

## Gate conditions

| # | Requirement | Level |
| --- | --- | --- |
| G1 | Same string **and** same controller (or withheld exclusively for that controller) always hold across integrated systems | **Gate** |
| G2 | If G1 cannot be reliably satisfied, systems **SHALL NOT** be treated as integration candidates | **Gate** |
| G3 | TLD string same; controlling entity is the **RO** of the TLD; RO controls alt use of that string | **Gate** |
| G4 | Parent operator operates the service; only that operator operates alt system(s); registered names integrate (incl. by exclusion); name identical in every system | **Gate** (scope) |

---

## Same name / IDN

| # | Requirement | Level |
| --- | --- | --- |
| N1 | Same-name comparison conducted **one label at a time** | **M** |
| N2 | Matching rules per A-label / U-label / ASCII cases in §4.5 | **M** |
| N3 | Variant / LGR processing **before** integration | **M** |

---

## Control of alt systems

| # | Requirement | Level |
| --- | --- | --- |
| C1 | RO can provide all relevant control guarantees so alt-name cannot drift in string or controller | **M** |
| C2 | Demonstrate exclusive control **or** authorization-only change path **or** deny-others when DNS allocation does not move | **M** (show one effective form) |

---

## Enrollment / allocation

| # | Requirement | Level |
| --- | --- | --- |
| E1 | Allocate in one system → allocate or withhold same name in all others, same controller | **M** |
| E2 | Enrolled name = same string + same entity in each system | **M** |
| E3 | Subordinate policy: must- / may- / integration-prohibited; if not prohibited, E1 applies | model |

---

## SRS-primary path

| # | Requirement | Level |
| --- | --- | --- |
| S1 | Demonstrate alt system does not itself risk Internet security/stability | **M** |
| S2 | Specify EPP extensions if optional alt ops / non-identical ops needed | likely **M** in practice |
| S3 | If separate EPP object mapping: provide relation to domain object | **M** |
| S4 | RDAP extensions for new data: specify, publish, register in IANA RDAP Extensions | **M** |
| S5 | Reuse existing RDAP extensions where possible | **S** |

---

## Distributed / USoT path

| # | Requirement | Level |
| --- | --- | --- |
| U1 | One eventually-consistent Unified Source of Truth for string+controller | **M** |
| U2 | Every name under common control (even if distributed) | **M** |
| U3 | Registration events can reliably check same-entity for same string | **M** |
| U4 | Demonstrate parties cannot break integration without controller approval | **M** (eval proof) |
| U5 | Single legal RO remains responsible (analogous to RSP arrangement) | architectural **M** for accountability |

---

## Lifecycle / abuse

| # | Requirement | Level |
| --- | --- | --- |
| L1 | External deactivation for abuse/court in any system → **disable** across systems | **M** |
| L2 | Suspensions apply to all naming systems simultaneously | **M** |
| L3 | Registrar `clientHold` alone SHOULD NOT disable everywhere; if used to disable, hold all systems | **S** |
| L4 | Public suffix SHOULD maintain lower-tree integration or disable integration for those domains | **S** |
| L5 | Until mature practice: turn-down plan for discontinuing integration | **S** (eval) |

---

## Explicit non-goals (do not treat as covered)

- Alt mechanisms other than string+controller  
- Query-less “use” of DNS strings inside apps  
- Business-model viability of alt naming  
- Competition / policy fitness reviews beyond RSEP security & stability framing

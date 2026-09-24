# Deep extracts — Public Comments (priority set)

**Sitting:** `sitting-2026-09-24-icann-tsg-string-controller`  
**Filed:** 24 Sep 2026 (deep pass v2)  
**Canon:** **no**  
**Egress limit:** `www.icann.org` / `itp.cdn.icann.org` / Circleid blocked for direct download; depth from WebSearch PDF crawls + Public Comment “Summary of Submission” pages + secondary roundups (Circleid, Domainera).

| Depth | Meaning |
| --- | --- |
| **A** | Near-full primary PDF text on disk |
| **B** | Substantial PDF snippets + official submission summary |
| **C** | Official submission summary / secondary roundup only |

Roster: [`../SOURCE-public-comment-roster.csv`](../SOURCE-public-comment-roster.csv)

---

## 1. Unregistry — Ageesen Sri — 21 Sep 2026 — Depth **A**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/unregistry-21-09-2026) · [PDF text](../SOURCE-unregistry-comment-text-extract.txt)

**Stance:** Support string+controller; registry-side mostly enough; user-side thin.

**Asks (compressed):**
1. **RDAP:** expose which systems a name is in + state in each.  
2. **Sync fail UX:** detect divergence in a defined window; fail-safe = stop resolving *everywhere*, not resolve differently.  
3. **Enrollment disclosure** in plain language (where it works; expiry/suspension; dies on EBERO/turn-down).  
4. **Turn-down plan = MUST** (notice, post-state, channels, timing).  
5. Open **§8.3 legacy** policy discussion now (millions of unverified Web3 names).  
6. **Rights:** enforcement follows DNS anchor; floor only for alt-only active names (8.2/8.4) on the RO.  
7. **Main proposal:** registrant DNSSEC TXT associations to any Web3 network ≠ registry service; proven vs declared; IETF RRType/`w3n:` as upgrade path.  
8. Bind only integrating registries; don’t over-prescribe → shadow ops; symmetric variants; UA coordination; put user-facing rules into RA amendments.

---

## 2. SSAC — SAC134 — 21 Sep 2026 — Depth **B**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/security-and-stability-advisory-committee-ssac-21-09-2026) · [SAC134 PDF](https://itp.cdn.icann.org/en/files/publications/sac134-21-09-2026-en.pdf)

**Stance:** Broadly supports Draft conclusions **if** integration does not impair DNS availability/integrity/ops. Parallel **RIDE** work party (wider than RSEP). Not commenting on remit/policy expansion.

**Section-tied suggestions (from PDF snippets):**
| § | Ask |
| --- | --- |
| 3.1 | Clarify **disabled** vs **deactivated**; define **enabled** (opposite of disabled) |
| 4.6 | Add **ongoing measurement** that registry control of alt system remains in place |
| 6.1–6.2 | Alt failure/delay/partition/loss of consensus must **not** block DNS create/renew/update/transfer/resolve |
| 7.1 | No alt counterpart to critical registry functions; EBERO kills integration — seek **registrant continuity** solutions in both spaces |
| 9.3 | For alt-primary / no contact data: require **functioning URS/UDRP equivalent** as RSEP condition, not leave open |
| 10 | Post-launch security/stability review mechanism after early integrations |
| (IDN/LGR/EPP) | Draft says LGR/variant processing MUST precede integration; EPP today is singular-object — IETF set-provisioning work relevant; clarify how alt namespaces enter SRS |

---

## 3. ALAC — AL-ALAC-ST-0826-01-00-EN — 21 Sep 2026 — Depth **B**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/policy-staff-in-support-of-the-at-large-community-at-large-advisory-committee-alac-21-09-2026) · [pending-ratification PDF via alac-announce](https://lists.icann.org/hyperkitty/list/alac-announce@icann.org/message/VL5VMRZLCVOZKA3PWQEB5D6H5H2FDFOP/attachment/4/PendingRatification_AL-ALAC-ST-0826-01-00-EN_InitialReportoftheTSGongTLDIntegrationswithAlternativeNamingSystems.pdf)

**Stance:** End-user / consumer-protection frame; wants GNSO policy path + hard monitoring.

**Asks (from ratified-draft PDF text):**
1. Continuous compliance monitoring: string drift, controller drift, sync failure, unauthorized changes, data inconsistency + reporting/remediation.  
2. **Prefer SRS-plugin** model so registrant data + ICANN policies attach (not bearer-token-only control) — ALAC’s ground is contactability/consumer protection, not only technical simplicity.  
3. Direct SSAC to assess **pre-existing alt-root collision** detection gap (technical, independent of PDP).  
4. Publish TSG **COI safeguards** (commercial seats noted as transparency, not primary attack).

---

## 4. IPC — Margaret Milam — 21 Sep 2026 — Depth **B**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/intellectual-property-constituency-21-09-2026) · [PDF](https://itp.cdn.icann.org/public-comment/proceeding/Initial%20Report%20of%20the%20TSG%20on%20gTLD%20Integrations%20with%20Alternative%20Naming%20Systems-10-08-2026/submissions/Intellectual%20Property%20Constituency/IPC%20Comment%20on%20TSG%20New%20GTLD%20Integration%20%20(1)-21-09-2026.pdf)

**Stance:** Report = technical advice only; **community process before any RSEP approval**.

**Core claims (summary page + PDF snippets):**
1. Architectures not policy-equivalent — only SRS enrollment clearly brings alt under ICANN policy.  
2. **Same-controller ≠ rights protection** — must prove UDRP/URS/court orders (and transfer/lock/deletion/RDAP effects) enforceable in every integrated system; RO obligation.  
3. **Legacy allocations** (§4.3 + §8.3): without further community work, alt holders could obtain/block matching DNS without TMCH/Claims/UDRP/URS — “not acceptable.”  
4. Legacy enrollment floor: (i) published inventory (ii) Registration Data Policy–grade controller data (iii) TMCH check (iv) time-limited rights-holder challenge before enrollment.

---

## 5. ENS Foundation — Alexander Urbelis — 21 Sep 2026 — Depth **B**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/ens-foundation-21-09-2026) · [PDF](https://itp.cdn.icann.org/public-comment/proceeding/Initial%20Report%20of%20the%20TSG%20on%20gTLD%20Integrations%20with%20Alternative%20Naming%20Systems-10-08-2026/submissions/ENS%20Foundation/ENS%20Foundation%20-%20Public%20Comment%20-%20TSG%20Initial%20Report-v2-(clean)-(21Sep2026)-21-09-2026.pdf)

**Stance:** Supports ICP-3 / single root; built on non-delegable string; bridges via DNSSEC + CCIP-Read. Supports TSG framework as affirmative/controlled/verifiable act — **not** a claim of entitlement.

**Transparency:** Nick Johnson on TSG; `.ens` brand TLD pending (ENS Labs / Foundation).

**Asks:**
1. Final Report: **registrant-elected** resolution of existing DNS names in additional contexts (ENS DNSSEC import) is **out of scope** of this Registry Service framework.  
2. Independently operated alt namespaces get **no automatic DNS rights/priority**.  
3. Collision risk = security/user-protection (NCAP/collision framework), not a property right; TSG + collision frameworks should work together.  
4. Aligns with RySG: no new obligations on non-integrating ROs; no rights for independent alt namespaces.  
5. Answers WIPO cybersquatting concern: every alt name mapping into root should pass **Sunrise/Claims** like any other allocation.

---

## 6. RrSG — Zoe Bonython — 18 Sep 2026 — Depth **B**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/registrar-stakeholder-group-rrsg-18-09-2026) · [PDF](https://itp.cdn.icann.org/public-comment/proceeding/Initial%20Report%20of%20the%20TSG%20on%20gTLD%20Integrations%20with%20Alternative%20Naming%20Systems-10-08-2026/submissions/Registrar%20Stakeholder%20Group%20(RrSG)/RrSG%20Public%20Comment_%20Initial%20Report%20of%20the%20TSG%20on%20gTLD%20Integrations%20with%20Alternative%20Naming%20Systems-18-09-2026.pdf)

**Stance:** Appreciates work; fears advisory → hard requirements; **Picket Fence** / remit.

**Asks (PDF + summary):**
1. For each proposed requirement: cite Bylaws §1.1(a)(i) “reasonably necessary” basis; distinguish integration vs regulating alt-system operation.  
2. Flag overreach: §4.6 (alt change interfaces), §8.5–8.6 (deactivation/suspension *inside* alt), §8.4 (DNS availability contingent on alt expiry).  
3. Registrars cannot be expected to discover/verify/monitor/sync across third-party alt systems; parse new EPP/RDAP extensions; pricing/renewal effects.  
4. Multi-system: §3 allows n systems; analysis is two-system; no limit/threshold; adding a further system to an already-integrated TLD unresolved; §8.3 enrollment clashes with names already active in DNS under different controller.  
5. Ask: does each additional system need its own RSEP? How are registrars notified?  
6. Future study groups: include a **technically focused registrar** seat; clarify TSG vs SSAC **RIDE** relationship; reuse **IDN EPDP** sync lessons.

---

## 7. Tucows Domains — Sarah Wyld — 18 Sep 2026 — Depth **C** (summary)

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/tucows-domains-18-09-2026)

**Stance:** Useful starting point; **strays into policymaking** / outside Picket Fence; **supports RrSG** input. PDF on disk not recovered this pass.

---

## 8. D3 Global, Inc. — Kevin Kreuser — 16 Sep 2026 — Depth **C**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/d3-global-inc-16-09-2026)

**Stance (Spanish submissions list summary):** Supports conclusion that well-designed integrations need not create material DNS S&S risk; clear risk-based evaluation; apply **only** to integrations affirmatively proposed/controlled by RO; preserve DNS registration as authoritative; architecture-neutral implementation.

---

## 9. ISPCP — Philippe Fouquart — 15 Sep 2026 — Depth **C** → Circleid **B-lite**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/the-internet-service-providers-and-connectivity-providers-constituency-ispcp-15-09-2026)

**Stance (Circleid roundup, 21 Sep):** Draft should include more detailed **risk assessments**, **controller-assurance** mechanisms, **monitoring**, and **mandatory continuity/shutdown** provisions. Aligns with ISPCP’s historical NCAP posture (per-TLD risk analysis). Primary PDF still thin.

---

## 10. .ART Domain Registry — Kurt Pritz — 20 Sep 2026 — Depth **C**

**Secondary (Circleid / Domainera):** Supports a **common technical baseline** for certainty; some recommendations belong in **policy development or registry negotiations**, not pure tech advice.

---

## 11. MeitY (Government of India) — 21 Sep 2026 — Depth **C** → Circleid **B-lite**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/ministry-of-electronics-and-information-technology-government-of-india-21-09-2026)

**Stance (Circleid):** Measurable requirements for **synchronization**, **failure handling**, **independent security testing**, and measures against **inconsistent ownership** across systems. Primary PDF not extracted.

---

## 12. WIPO Arbitration and Mediation Center — Brian Beckham — 21 Sep 2026 — Depth **C** (via ENS cite)

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/wipo-arbitration-and-mediation-center-21-09-2026)

**Position (as cited by ENS):** Cybersquatting already at scale in alt namespaces; infringing names must not map into the root unchecked. ENS answers: Sunrise/Claims for any mapping into root. (Primary PDF not extracted this pass — do not invent WIPO quotes.)

---

## 13. RySG — 21 Sep 2026 — Depth **C** (via ENS cite)

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/rysg-registries-stakeholder-group-21-09-2026)

**Position (ENS PDF quotes RySG ask of Final Report):** create **no rights** for independently operated alternative namespaces; impose **no new obligations** on registry operators that propose **no** integration. Primary RySG PDF not recovered this egress pass.

---

## 14. CleanDNS Inc. / Netnod — Depth **C** (links only)

| Submitter | Link |
| --- | --- |
| CleanDNS (Alan Woods) | [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/cleandns-inc-21-09-2026) |
| Netnod (Ulf Fredrik Karl Lindeberg) | [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/netnod-21-09-2026) |

Neither PDF nor summary recovered in this environment. Open follow-ups.

---

## 15. Thomas Clowes — 9 Sep 2026 — Depth **B** (submission summary)

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/clowes-thomas-09-09-2026)

**Stance:** Supports string+controller; cites working prototype `github.com/clowestab/altname-platform`.

**Asks:** Reconcile §8.3 withhold with Sunrise/Claims; decline “prior claim” framing (argues: permissionless mint → manufactured claims; colliding ANS brands sell same strings; RO that doesn’t control a namespace can’t integrate it under §4.6 anyway); controller proofs continuing/revocable + event-triggered revalidation (not fixed-expiry fail-closed); turn-down **REQUIRED**; reset-on-transfer hygiene; keep §11 scope (much “utility” is a profile keyed to DNS, not a second namespace).

---

## 16. estmcmxci.eth — Mark “Marcus” Martinez — 21 Sep 2026 — Depth **B**

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/estmcmxcieth-21-09-2026) · [summary extract](../SOURCE-estmcmxci-comment-summary-extract.txt)

**Stance:** Personal capacity (not ENS Labs/Foundation). Offers **TLD Oracle** prototype as one way to meet TLD-level Report requirements for ENS binding.

**Mechanism:** RO publishes DNSSEC-signed record at `_ens.nic.{tld}` naming an Ethereum address; on-chain contract assigns that TLD in ENS to that address after verifying DNSSEC from the root trust anchor.

**Maps to Report:**
| § | Claim |
| --- | --- |
| 4.2 | ENS string = DNS TLD label; controller = RO via address at `_ens.nic.` (Spec 5 reserves `nic` for RO) |
| 4.6 | Binding requires DNSSEC-signed record in nic zone — change auth only RO can issue |
| 10 | TLD-binding integrity = DNSSEC itself (RA Spec 6 §1.3), extended to nic zone; names *inside* ENS use Ethereum consensus |

**Related context (secondary, not the ICANN filing):** ENS DAO temp-check / TLDMinter allowlist of ~1,166 post-2012 gTLDs where `nic` is structurally reserved; pre-2012 gTLDs and ccTLDs need governance because `nic` is not globally reserved. Useful compass for §4.6 “change authorization only the RO can issue” — not a CVS claim.

---

## 17. Matthew Bird — 8 Sep 2026 — Depth **B** (submission summary)

**Link:** [submission](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026/submissions/bird-matthew-08-09-2026)

**Stance:** Support string+controller; add explicit **“pre-existing alternative naming system populations”** section.

**Ask:** Any RO integrating a *populated* ANS must file a **pre-launch transition plan**: inventory/use of existing names; contractual entitlements of holders; controller-equivalence verification; protect matching DNS names during launch; path for eligible holders to connect/activate DNS names; handle conflicts with ICANN rules; disposition of unclaimed/unverifiable names.

**Key boundary:** Existing ANS communities may show demand/utility but create **no automatic entitlement** to DNS delegation or allocation — still subject to S&S, RPMs, reserved-name rules. Middle path between APlus/Barrett grandfathering and ENS “no rights.”

---

## 18. Legacy-alt / Web3 holder cluster — Depth **B/C**

| Submitter | Ask |
| --- | --- |
| **APlusDomains.Crypto** (Jonathon Browne) | Protect 1M+ existing `.crypto` ANS holders before any ICANN `.crypto` DNS registry; grandfather / fair claim window; privacy for controller data |
| **Eric Barrett** | Same for Unstoppable-intended set: `.crypto .bitcoin .wallet .nft .dao .polygon .zil .blockchain` before DNS delegation/integration |
| **Manoratana, Tiranest** | Same pattern for `.nft` (claims 800k+ ANS holders); sunrise/claim window; privacy; grandfathering |
| **Darwin, Matthias** | Protect pre-existing ANS when identical string later delegated to unrelated DNS controller; priority protection + crypto-verifiable snapshots; distinguish populated vs empty namespaces; “integration ≠ displacement” |
| **Ha Nguyen Hong** | Support string+controller + §4.6/§8; ask practical guidance for proving controls under deployment |
| **Laura Ndubi** | Conditional support; strong safeguards; don’t expand remit beyond reasonably necessary |
| **Quynh Nguyen** | Support string+controller + SRS/USoT; clearer audit of control; lifecycle events; turn-down/EBERO clarity |

**Secondary market signal (Unstoppable blog, not a PC filing):** Unstoppable withdrew ICANN apps for `.crypto` and siblings, citing TSG-style rules that would force DNS registration + payment + data disclosure for millions of on-chain-only names. Relevant to Fight C politics; not a formal comment.

**Tension with ENS/RySG/Clowes/Bird:** prior-claim / grandfathering vs “no rights for independent namespaces” + collision framework + Sunrise/Claims + Bird’s transition-plan-without-entitlement.

---

## Cross-cut matrix (deep pass v2)

| Issue | Who pushes |
| --- | --- |
| DNS ops must not depend on alt health | SSAC |
| Prefer SRS + contact data | ALAC, IPC |
| Community PDP before RSEP green lights | ALAC, IPC |
| Enforceable UDRP/URS/court in all systems | IPC, SSAC (§9.3), WIPO (via ENS) |
| Legacy alt → DNS enrollment / grandfathering | IPC (challenge process), APlus/Barrett/Manoratana/Darwin (prior claim), Unregistry (open 8.3 talk), Bird (transition plan, no entitlement), Clowes (anti–prior-claim) |
| No rights for independent alt TLDs | ENS, RySG (per ENS) |
| Registrant DNSSEC association ≠ RSEP | Unregistry, ENS (reverse import out of scope) |
| TLD-level DNSSEC binding prototype | estmcmxci (TLD Oracle / `_ens.nic.`) |
| Picket Fence / don’t harden advisory | RrSG, Tucows, .ART (partial), Circleid roundup |
| Stronger risk/assurance framework | ISPCP, MeitY, SSAC measurement |
| Multi-system / add-a-network RSEP | RrSG |
| Turn-down MUST + EBERO user story | Unregistry, Clowes, SSAC continuity |
| Working prototypes cited | Clowes (altname-platform), estmcmxci (TLD Oracle), Unregistry (ops perspective) |

---

## Still thin (next fetch when egress allows)

Priority PDF pulls: **RySG, WIPO, CleanDNS, Netnod, MeitY primary, ISPCP full, .ART full, D3 full, SSAC full SAC134, ALAC filed PDF, ENS full, IPC full, Tucows full**.

Until then, cite this file + Unregistry full text; do not invent quotes for thin Depth-C rows.

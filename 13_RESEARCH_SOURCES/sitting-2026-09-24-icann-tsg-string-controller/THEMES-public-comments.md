# Public Comment themes — TSG initial report

**Filed:** 24 Sep 2026 (addendum to sitting)  
**Roster:** [`SOURCE-public-comment-roster.csv`](SOURCE-public-comment-roster.csv) — 40 rows (38 active + 2 retracted) from chat paste  
**Proceeding:** closed 21 Sep 2026 · report due ~5 Oct 2026  
**Canon:** **no**  
**Limit:** Institutional / published positions summarized from Public Comment pages, SAC134 PDF snippets, ENS/Unregistry/IPC/RrSG/ALAC/Circleid secondary coverage. Individual comments not all read end-to-end (icann.org binary fetch blocked on this host).  
**Deep pass:** [`extracts/DEEP-EXTRACTS.md`](extracts/DEEP-EXTRACTS.md) · [`extracts/TENSION-MAP.md`](extracts/TENSION-MAP.md) (v2 — adds estmcmxci, Bird, Manoratana/Darwin, Circleid ISPCP/MeitY hardening).

---

## Counts

| Bucket | n |
| --- | --- |
| Roster rows received | 40 |
| Marked retracted in title | 2 (Samuel Liu; Krypto@Recht / Henning Jessen) |
| Active (roster) | 38 |
| Stakeholder / advisory / gov / org faces (selected) | SSAC, ALAC, RySG, RrSG, IPC, ISPCP, WIPO, ENS Foundation, Unregistry, CleanDNS, Netnod, MeitY India, .ART, Tucows, D3 Global, APlusDomains.Crypto, estmcmxci.eth, … |

---

## Theme map (load-bearing)

### 1. Threshold principle mostly not rejected

String+controller (same string / same controller or exclusive withhold) is treated as a serious answer to “can same-string integration be safe?” by SSAC (broad support with conditions), Unregistry (explicit support), ENS Foundation (supports ICP-3 / single root; clarifies a *different* direction of use), and secondary press. Fight is over **how hard to enforce**, **who decides policy**, and **legacy alt allocations** — not over abandoning sameness.

### 2. DNS must not depend on alt-system health

**SSAC (SAC134):** failure / delay / partition / loss of consensus in an alt system must **not** block otherwise-valid DNS registration, renewal, update, transfer, resolution. Ongoing measurement that registry control of the alt system still holds. Clarify disabled vs deactivated; define “enabled.” Continuity beyond EBERO for registrants in both spaces. Equivalent URS/UDRP when only alt-name is live. Post-launch review; collision; PSL; IDN/LGR/EPP hardening.

### 3. Consumer protection and contactability prefer SRS-plugin

**ALAC:** prefer Report’s SRS-as-primary / alt-as-plugin path so registrant data and ICANN policies travel with the name; warn that bearer-token-only control may leave URS/UDRP unworkable. Continuous compliance monitoring (string drift, controller drift, sync failure). Ask SSAC to study **pre-existing alt-root collision** detection. Transparency note: TSG seats include commercial interest — publish COI safeguards.

### 4. Rights / legacy allocations are a policy landmine

**IPC:** withhold/allocate-everywhere + enroll legacy alt names → party with pre-DNS alt hold can obtain or block matching DNS without TMCH / Claims / UDRP/URS history — “not acceptable.” Want community process **before** any integration approval; for legacy: published inventory, Registration Data Policy–grade controller data, TMCH check, time-limited challenge before enrollment.

**WIPO:** flagged in secondary coverage for cybersquatting / rights-protection concern (full text not extracted here — open submission link in roster).

### 5. Scope fights: picket fence vs registry service vs reverse direction

**RrSG:** report reads advisory but may harden into requirements; may stray outside Picket Fence; technical/implementation gaps remain.

**ENS Foundation:** Report covers **registry → alt** as a Registry Service. It must **not** be read to govern **registrant-elected** resolution of an *existing* DNS name in additional contexts (ENS DNSSEC import since 2021): no second allocation, no parallel namespace, DNSSEC chain *is* the controller proof. Ask Final Report to state that reverse direction is **out of scope**. Disclose Nick Johnson on TSG + pending `.ens` brand TLD.

**Unregistry:** support string+controller on registry side; thin on **user** side. Main ask: registrant-directed multi-network associations via **DNSSEC-signed TXT** (or later RRType) — not a new registry service; IETF standardization as upgrade path; distinguish proven vs declared associations; reuse DNS accountability stack rather than rebuild rights per network.

### 6. Operators / connectivity / states want measurable risk controls

**ISPCP** (via Circleid): deeper risk assessment, controller-assurance, monitoring, mandatory continuity/shutdown.

**MeitY India** (via Circleid): measurable requirements for failure handling, independent security testing, collision measures.

**Netnod / CleanDNS:** rostered; PDF/summary still unrecovered after thin-PDF pass 25 Sep — follow links in CSV before citing. **RySG / WIPO:** positions known via ENS cite only; primaries still open. **Tucows:** Depth B (CDN PDF crawl). **.ART / D3 / MeitY / ISPCP:** Circleid B-lite or list summary only.

### 7. Individual / alt-name operator cluster

Many individual and Web3-facing comments (APlusDomains.Crypto, Barrett, Manoratana, Darwin, estmcmxci.eth, Clowes, Bird, regional individuals). Recurring ask: holders of strings like `.crypto` / `.nft` / `.wallet` get protections if those strings enter DNS — a **boundary** the TSG said it was not answering (threshold technical safety for registry-operated same-string integration, not general alt-root politics).

**Internal split:** APlus/Barrett/Manoratana/Darwin push prior-claim/grandfathering; Clowes rejects that framing; Bird asks for a **pre-launch transition plan without automatic DNS entitlement**; estmcmxci offers a DNSSEC `_ens.nic.` TLD-binding prototype (personal, not ENS Foundation).

---

## Institutional cheat-sheet

| Actor | Stance (this pass) | Primary ask |
| --- | --- | --- |
| SSAC (SAC134) | Support Draft conclusions **if** DNS ops independent of alt failure | Measurement, independence, EBERO+continuity, URS/UDRP parity, post-launch review, IDN/EPP clarity |
| ALAC | Cautious; end-user frame | Prefer SRS-plugin; contactability; continuous monitoring; SSAC collision study; COI transparency |
| IPC | Rights-first brake | Community process before approvals; legacy enrollment controls (inventory, data, TMCH, challenge) |
| RrSG | Process / fence caution | Don’t harden advisory into unexamined requirements; multi-system RSEP; IDN-EPDP reuse |
| RySG | (via ENS cite) | No rights for independent alt namespaces; no new duties on non-integrating ROs |
| ENS Foundation | Support root unity; carve reverse path | Final Report: registrant-elected DNSSEC import out of scope |
| Unregistry | Support principle; user-side model | DNSSEC association records ≠ registry service; IETF path |
| ISPCP / MeitY | Hardening | Measurable risk, controller assurance, sync/failure tests, continuity/shutdown |
| WIPO | Rights enforcement | Cybersquatting / RPM applicability (read PDF before quoting) |
| Tucows | Picket Fence / support RrSG | DNS-side OK; don’t regulate ANS internals; advisory ≠ binding |
| CleanDNS / Netnod | Thin (25 Sep pass) | Roster links only — fetch PDFs before citing |

---

## Watch next

1. Revised / Final TSG report (~5 Oct 2026 due per proceeding).  
2. Later Public Comment pairing Final Report with **Registry Agreement** contractual language.  
3. Whether Final Report adopts ENS “reverse direction out of scope” and Unregistry “association records ≠ RSEP” clarifications.  
4. Whether legacy-alt enrollment rules move from “policy beyond this report” into GNSO / ICANN org work before any RSEP green light.

---

## Provenance notes

- Roster CSV = user paste 24 Sep 2026; `Status` column added (`retracted` from submission title wording).  
- SAC134: https://itp.cdn.icann.org/en/files/publications/sac134-21-09-2026-en.pdf  
- ENS PDF: under proceeding submissions path (see WebSearch / roster link).  
- Unregistry: https://unregistry.com/resources/tsg-public-comment/ + PDF under submissions.  
- Circleid roundup: https://circleid.com/posts/icann-comment-period-closes-on-linking-gtlds-with-alternative-naming-systems  
- Do not treat this themes file as a substitute for reading primary PDFs before any public reply.

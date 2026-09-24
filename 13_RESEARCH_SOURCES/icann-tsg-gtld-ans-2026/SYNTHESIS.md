# ICANN TSG: gTLD Integrations with Alternative Naming Systems — Comment Synthesis

**Drawer:** `13_RESEARCH_SOURCES` (research, not Canon)  
**Sitting:** 2026-09-24  
**Proceeding:** [Initial Report of the TSG on gTLD Integrations with Alternative Naming Systems](https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026)  
**Comment window:** 10 Aug 2026 – 21 Sep 2026 23:59 UTC  
**Report due:** 05 Oct 2026  
**Sources in this pack:** public ICANN pages/PDFs + secondary coverage (CircleID); full texts where retrieved under `raw/`

---

## Verdict

The comment corpus largely **accepts string+controller as a workable technical baseline** for registry-proposed same-string integrations, then splits hard on what that baseline does *not* decide: **legacy alt-namespace populations (§8.3)**, **rights-protection (UDRP/URS/Sunrise/Claims)**, **ICANN remit / Picket Fence**, and **whether registrant-elected DNSSEC links are a Registry Service at all**.

Nobody serious argues “never integrate.” The fight is **RSEP-only technical approval vs mandatory GNSO/policy work first**, and **prior claim / grandfathering vs no DNS entitlement from independent minting**.

---

## What the TSG Initial Report says (baseline)

Source: [TSG Initial Report PDF](https://itp.cdn.icann.org/en/files/generic-top-level-domains-gtlds/tsg-gtld-integrations-with-alternative-naming-systems-initial-report-10-08-2026-en.pdf) (extract in `raw/TSG-initial-report-extract.txt`).

| Element | Content |
| --- | --- |
| Trigger | Registry operators / 2026 Round applicants want services associating DNS gTLDs with the **same string** in alternative naming systems (ANS) |
| Process home | Treated as a **Registry Service** under RSEP (possibly RSTEP) |
| Core test | **String+controller:** same string in each integrated system is always controlled by the same party, or withheld for that party’s exclusive possible control |
| Coordinator | The **DNS registry** must be able to ensure same-party control across systems |
| Modes | Enrollment via **Shared Registration System (SRS)**; **distributed** enrollment with Unified Source of Truth (USoT); bearer-token / proof variants |
| Out of scope (Report §11) | Long-term viability of non-DNS naming, general competition/policy, many profile-style use cases |
| Next ICANN step | Final TSG report → later Public Comment on **registry-agreement amendments** |

Coordinator: Andrew Sullivan; convened by CEO Kurtis Lindqvist (June 2026). Members include SSAC, IETF community, registry operators, and ANS operators.

---

## Corpus snapshot

| Metric | Count |
| --- | --- |
| Rows in user-supplied index | **40** |
| Marked retracted | **2** (Samuel Liu; Krypto@Recht / Henning Jessen) |
| Active submissions | **38** |
| Institutional / contracted-party / advisory | SSAC, ALAC, IPC, RySG, RrSG, ISPCP, ENS Foundation, Unregistry, WIPO, Netnod, CleanDNS, Tucows, .ART, D3 Global, MeitY India, plus individuals |

Full roster: [`submissions-index.csv`](submissions-index.csv).

---

## Stance map (retrieved positions)

Legend: **Support** = endorses string+controller baseline · **Conditional** = yes only with policy/ops/remit fixes · **Prior-claim** = legacy ANS holders should get DNS priority/grandfathering · **Defer** = block or postpone approval until community process

| Cluster | Actors | Stance | Core ask |
| --- | --- | --- | --- |
| Security advisors | **SSAC (SAC134)** | Conditional support | DNS must not depend on alt availability; ongoing control measurement; functioning UDRP/URS equivalents as RSEP condition; post-launch review; collision / IDN / EBERO gaps |
| End users | **ALAC** | Conditional support | GNSO PDP for consumer protection; contactability; suspension sync bounds; prefer SRS “plugin”; SSAC study of pre-existing alt collision gap; disclose TSG COI safeguards |
| IP / RPM | **IPC**; **WIPO** (listed; ENS cites WIPO cybersquatting concern) | Defer / harden | Technical advice ≠ policy; no legacy enroll without TMCH + challenge; same-controller ≠ sufficient RPM |
| Registrars | **RrSG**, **Tucows** | Conditional | Stay inside Picket Fence; advisory vs binding clarity; registrar implementation analysis; withheld/perpetual-name economics; don’t prescribe alt internals |
| Registries | **RySG** (listed; ENS cites RySG “no rights for independent namespaces”), **.ART**, **D3 Global** | Conditional / support | Common technical baseline; no new obligations on non-integrating registries; architecture-neutral; excess items → GNSO or RA negotiation |
| ANS / Web3 operators | **ENS Foundation**, **Unregistry**, **Clowes**, **estmcmxci.eth (Martinez)** | Support + anti–prior-claim (ENS/Clowes) or user-path (Unregistry) | Integration is affirmative & controllable; **no DNS entitlement** from independent ANS minting; registrant DNSSEC associations ≠ Registry Service; continuous controller proof; turn-down REQUIRED |
| ISP / infra | **ISPCP**, **Netnod** (listed) | Conditional | Stronger explicit risk/assurance framework before go-live |
| Abuse / ops | **CleanDNS** (listed) | (text not retrieved this sitting) | Expect abuse / sync / suspension themes |
| Government | **MeitY India** (listed) | (text not retrieved this sitting) | — |
| Prior-claim camp | **APlusDomains.Crypto**, **Sayed**, **Manoratana**, **Darwin**, parts of **Bird** | Prior-claim | Protect existing `.crypto` / `.nft` / ANS holders before DNS delegation of same string |

---

## Cross-cutting fault lines

### 1. Technical baseline vs policy gate

Almost every institutional commenter says the Report is useful **technical advice**. IPC, ALAC, RrSG, Tucows, and .ART (secondary coverage) insist **GNSO / contractual process** must handle rights protection, contacts, consent for “permanent” ANS names, and registrar obligations **before** treating integrations as routine RSEP approvals.

### 2. §8.3 legacy populations (the hottest fight)

Report: if an existing ANS is integrated, its names “must be enrolled and therefore must be at least withheld from the global DNS,” with “policy implications needing to be discussed.”

| Side | Position |
| --- | --- |
| Prior-claim | Registration history = legitimate claim; block third-party DNS allocation; transition / verify windows (esp. `.crypto`, `.nft`) |
| Anti–prior-claim (ENS, Clowes) | Permissionless minting cannot manufacture DNS rights; colliding strings are a **name-collision** problem, not a property right; §8.3 already protects when **the integrating operator’s own** namespace is enrolled |
| IPC | Legacy enroll needs inventory, RDP-compliant data, **TMCH**, time-limited rights-holder challenge — else squatters block DNS without ever touching Claims/UDRP |

### 3. Two different “integrations”

| Path | Who pushes | ICANN touch |
| --- | --- | --- |
| **Registry bilateral string+controller** | TSG core; SSAC; contracted parties when they integrate | Registry Service / RSEP |
| **Registrant-elected DNSSEC / TXT association** to web3 (no second allocation) | Unregistry; ENS (as out-of-scope of TSG); Clowes (profiles often enough) | Ask ICANN to clarify **not** a Registry Service |

### 4. Continuity of control

Multiple individuals + SSAC/ALAC: proving same controller **once** is insufficient. Want **continuous / revocable / event-triggered** revalidation, measurable sync failure bounds, and **mandatory** turn-down plans (Clowes: elevate from RECOMMENDED to REQUIRED).

### 5. Remit / Picket Fence

RrSG and Tucows: Final Report should map each requirement to Bylaws §1.1(a)(i) “reasonably necessary,” distinguish DNS-side integration from governing ANS internals, and avoid soft-law that becomes hard contracted-party obligation without negotiation.

---

## Institutional digests (retrieved)

### SSAC — SAC134 (19/21 Sep 2026)

- Broadly supports Draft conclusions **if** DNS availability/integrity stay independent of alt failure.
- Clarify status vocabulary (enabled / disabled / deactivated).
- Ongoing measurement that registry still controls the alt system (§4.6).
- EBERO continuity gap when integration cannot survive emergency operator.
- Functioning UDRP/URS **equivalents as RSEP condition**, not open question.
- Parallel RIDE work party is wider; does not prescribe RSEP criteria.

PDF: https://itp.cdn.icann.org/en/files/publications/sac134-21-09-2026-en.pdf

### ALAC — AL-ALAC-ST-0826-01-00-EN (ratified 21 Sep 2026)

- Does not oppose exploring string+controller.
- Prefer GNSO process over RSEP-alone for consumer issues.
- Prefer SRS plugin model (registrant records) over token-only control.
- Continuous compliance monitoring (string/controller drift, sync failure).
- Ask SSAC to assess pre-existing alt-root collision-detection gap.
- Transparency on TSG commercial COI safeguards.

### IPC (Margaret Milam, 21 Sep 2026)

- Report = technical advice only; community work before any approval.
- SRS enrollment is the path that actually brings names under ICANN policy; distributed/USoT not automatically policy-equivalent.
- Same-controller parity necessary but **not sufficient** for RPM enforceability without loser cooperation.
- Hard legacy-allocation checklist (inventory, RDP data, TMCH, challenge window).

PDF: https://itp.cdn.icann.org/public-comment/proceeding/Initial%20Report%20of%20the%20TSG%20on%20gTLD%20Integrations%20with%20Alternative%20Naming%20Systems-10-08-2026/submissions/Intellectual%20Property%20Constituency/IPC%20Comment%20on%20TSG%20New%20GTLD%20Integration%20%20(1)-21-09-2026.pdf

### RrSG (Zoe Bonython, 18 Sep 2026) + Tucows (Sarah Wyld, 18 Sep 2026)

- Advisory vs binding ambiguity; Picket Fence risk.
- Implementation analysis: who implements, who pays, renewal/release of withheld strings, multi-system risk without caps.
- Do not bill registrars for permanent withholds they did not allocate.
- Align TSG with IDN EPDP sync lessons; clarify relation to SSAC RIDE.

### ENS Foundation (Alexander Urbelis, 21 Sep 2026)

- Supports ICP-3 / single root; `.eth` chosen to avoid DNS collision.
- Discloses Nick Johnson on TSG; pending `.ens` brand application.
- Supports string+controller / USoT; integration is affirmative, **never entitlement**.
- Independent ANS minting creates **no** DNS reservation/grandfathering.
- Converted names still need Sunrise/Claims.
- Registrant-elected DNSSEC import of existing DNS names is **outside** framework (not a Registry Service).

### Unregistry (Ageesen Sri, 21 Sep 2026)

- Affirms string+controller; strengthens user-facing duties (public integration state, sync-failure UX, MUST turn-down).
- Open §8.3 as **policy process**, not auto-prior-claim.
- Main ask: registrant-directed multi-network association via ordinary DNS records; ICANN clarify **not** a new registry service.
- Full text: `raw/Unregistry-submission.txt`

### Thomas Clowes (9 Sep 2026) + blog

- Built `altname-platform` prototype of the framework.
- Decline broad prior-claim framing; reconcile §8.3 withhold with Sunrise/Claims.
- Continuous revocable controller proofs; turn-down REQUIRED; reset-on-transfer hygiene.
- Much sought utility is a **profile**, not a second namespace.
- Blog extract: `raw/Clowes-blog-same-string-same-controller.txt`

### Mark “Marcus” Martinez / estmcmxci.eth (21 Sep 2026)

- Personal capacity: **TLD Oracle** prototype — DNSSEC-signed `_ens.nic.*` binding verified on-chain.
- Aligns with ENS Foundation registry-direction (not registrant-elected import).
- Complements subordinate-name lifecycle work (Altname / Clowes line).

### D3 Global (Kevin Kreuser, 16 Sep 2026)

- Support risk-based framework for integrations **affirmatively proposed and controlled** by the registry; DNS remains authoritative; architecture-neutral implementations.

### ISPCP (Philippe Fouquart, 15 Sep 2026)

- Supportive of technical direction but Report does not fully answer charter on concrete security/stability implications; wants stronger assurance / monitoring / shutdown / independent testing (per index + CircleID).

---

## Prior-claim / transition cluster (individuals & operators)

| Submitter | Theme |
| --- | --- |
| APlusDomains.Crypto (Jonathon Browne) | Protect 1M+ `.crypto` ANS names before any ICANN `.crypto` DNS registry |
| Manoratana | Similar for `.nft` (~800k+) |
| Darwin | Structured: ANS inventory snapshot, cutoff, reservation, proof of control, disputes |
| Bird | New report section + mandatory pre-launch transition plan for pre-existing populations |
| Nguyen family / related individuals | Continuous controller proof (not one-time) |
| Clowes / ENS | Explicit counter: refuse prior-claim as DNS entitlement |

---

## What to watch next

1. **TSG Final Report** (due 5 Oct 2026) and comment-response summary — especially how they resolve §8.3, RPM conditions, and remit language.
2. **Second Public Comment** on proposed **registry-agreement amendments** (ICANN blog, 11 Aug 2026).
3. Interaction with **SSAC RIDE** and **name-collision / NCAP** tracks for pre-existing ANS strings.
4. Whether ICANN org adopts the Unregistry/ENS clarification that **registrant-published DNSSEC associations are not a Registry Service**.

---

## Honesty / limits (this sitting)

- Direct HTTPS from this Cloud Agent VM to `icann.org` / `itp.cdn.icann.org` is **egress-blocked**; content was retrieved via search-index extracts and secondary pages.
- Full PDF text **confirmed in-pack** for: TSG Initial Report, Unregistry, Clowes blog.
- Positions for **Netnod, CleanDNS, WIPO, RySG, MeitY** are **roster-confirmed** from the user index; body digests incomplete pending allowlist or offline PDF drop.
- Retracted submissions listed but not analyzed.
- Connection ≠ merge: this is research filing only — not Canon, not a product decision.

*Non Solus.*

# SYNTHESIS — string+controller × Public Comment (integrated compass)

**Sitting:** `sitting-2026-09-24-icann-tsg-string-controller`  
**Filed:** 24 Sep 2026 · deep pass integrated  
**Canon:** **no** · Connection ≠ merge  
**Sibling pack:** [`../icann-tsg-gtld-ans-2026/`](../icann-tsg-gtld-ans-2026/) (parallel Collection Mode filing; same proceeding)

This file rolls the **TSG Initial Report** extract and the **closed Public Comment** deep pass into one reading path. Detail lives in the linked files; this is the compass.

| Layer | File |
| --- | --- |
| Report rules | [`EXTRACT-BRIEF.md`](EXTRACT-BRIEF.md) · [`REQUIREMENTS-CHECKLIST.md`](REQUIREMENTS-CHECKLIST.md) |
| Comment themes | [`THEMES-public-comments.md`](THEMES-public-comments.md) |
| Per-submitter depth | [`extracts/DEEP-EXTRACTS.md`](extracts/DEEP-EXTRACTS.md) |
| Fight map | [`extracts/TENSION-MAP.md`](extracts/TENSION-MAP.md) |
| Roster | [`SOURCE-public-comment-roster.csv`](SOURCE-public-comment-roster.csv) |

---

## Verdict (one screen)

1. **Technical baseline holds.** Comment corpus mostly accepts **string+controller** as a workable answer to “can RO-controlled same-string integration be RSEP-safe?”
2. **Charter ≠ politics.** Four fights sit on top of that baseline (below). Only Fight A is inside the TSG’s narrow charter; B–D decide whether any RA text is viable.
3. **“Integration” is already three+ directions.** Registry→alt (RSEP), registrant DNSSEC associations (Unregistry; not a Registry Service), ENS reverse DNSSEC import (out of scope), and TLD-level `_ens.nic.` binding (estmcmxci prototype).
4. **No CVS product claim.** Compass for CRYSTALMATRIX “decentralized identity & naming” notes only.

---

## Report baseline (compressed)

| Element | Content |
| --- | --- |
| Home | Registry Service under **RSEP** (possibly RSTEP) |
| Test | Same string always same controller **or** withheld exclusively for that party |
| Coordinator | DNS **registry operator** |
| Modes | SRS-plugin · distributed + **USoT** · bearer/proof variants |
| Lifecycle | Allocate/withhold everywhere; suspensions multi-system; external disable cascades |
| Continuity | Integration likely **dies on EBERO** → turn-down plan |
| Out of scope (§11) | App-only name use, alt business viability, full policy/competition review |

Full rules: EXTRACT-BRIEF · REQUIREMENTS-CHECKLIST.

---

## Four fights (Public Comment)

### Fight A — Technical safety (in charter)

**Claim:** string+controller + ops controls → unlikely significant DNS S&S harm.

| Push | Who |
| --- | --- |
| Conditional yes | SSAC (SAC134), Unregistry, D3, Clowes, many individuals |
| Harden | SSAC: DNS independent of alt failure; continuous control measurement; URS/UDRP equivalent for alt-primary; post-launch review; IDN/EPP clarity |
| Measurable assurance | ISPCP, MeitY (Circleid): sync, failure handling, independent testing, ownership consistency, continuity/shutdown |

**Likely Final Report move:** keep threshold yes; add independence + measurement + terminology + post-launch language.

### Fight B — Picket Fence / process

| Camp | Ask |
| --- | --- |
| RrSG, Tucows, .ART (partial) | Don’t harden advisory into RA mandates; map each requirement to Bylaws §1.1(a)(i); don’t govern ANS internals |
| ALAC, IPC | *More* community / GNSO work **before** any RSEP green light |

**Likely process move:** Final Report + later **RA amendment** Public Comment; separate tracks for legacy + RPMs.

### Fight C — Legacy / who owns off-root strings (§8.3)

| Camp | Position |
| --- | --- |
| Prior-claim / grandfather | APlusDomains.Crypto, Barrett, Manoratana (.nft), Darwin |
| No rights from alt occupancy | ENS + RySG (via ENS cite) — collision ≠ property; Sunrise/Claims if entering root |
| Process deferral | Unregistry — open §8.3 now; installed base is not empty |
| Anti–prior-claim | Clowes — permissionless mint / colliding ANS brands; §4.6 control prerequisite |
| Transition plan, **no entitlement** | **Bird** — pre-launch inventory/verify/withhold/activate path; no automatic DNS right |
| Rights machinery first | IPC — inventory + RDP data + TMCH + challenge window |

**Market signal (secondary):** Unstoppable withdrew ICANN apps for `.crypto` and siblings, citing rules that would force DNS registration/payment/disclosure for millions of on-chain-only names.

### Fight D — Directions of “integration”

| Direction | Who | Touch |
| --- | --- | --- |
| Registry → alt (same string) | TSG core | **RSEP** |
| Registrant → multi-network associations (DNSSEC TXT) | Unregistry | Ask: **not** a Registry Service |
| Registrant → alt resolution of existing DNS names | ENS | Final Report: **out of scope** |
| Registry TLD → ENS root binding (`_ens.nic.`) | estmcmxci | Prototype for §4.2 / §4.6 / §10 |

---

## Comment overlay on the checklist

Items the Report treats lightly that commenters treat as load-bearing. Observer aid only — not ICANN legal advice.

| Overlay | Source camps | Checklist touch |
| --- | --- | --- |
| DNS ops MUST NOT wait on alt health | SSAC | New gate beside G1–G4 for eval reading |
| Ongoing measurement of RO control of alt | SSAC §4.6 | Extends C1–C2 |
| Turn-down plan as REQUIRED (not RECOMMENDED) | Unregistry, Clowes, ISPCP | Elevates L5 |
| SRS/contactability preferred for consumer path | ALAC, IPC | Soft preference on path A vs bearer |
| RPM enforceability in *every* integrated system | IPC, SSAC §9.3, WIPO (via ENS) | Beyond same-controller |
| Legacy enroll = policy process first | IPC, ALAC; Bird transition plan | §8.3 cannot be silent |
| Multi-system / add-a-network RSEP clarity | RrSG | Gate for n>2 |
| Registrant DNSSEC association ≠ RSEP | Unregistry, ENS | Keep §11 bright |

Detail: REQUIREMENTS-CHECKLIST (PC overlay section) · DEEP-EXTRACTS matrix.

---

## Prototypes (existence proofs, not endorsement)

| Prototype | Submitter | Shows |
| --- | --- | --- |
| altname-platform | Clowes | Event-triggered controller revalidation; turn-down demo |
| TLD Oracle | estmcmxci | DNSSEC nic-zone → on-chain TLD assignment (post-2012 gTLDs) |
| Unregistry ops model | Unregistry | Association records; sync-fail UX |

---

## Crystal relevance (research only)

| Surface | Link |
| --- | --- |
| CRYSTALMATRIX “decentralized identity & naming” | Weak compass — same problem family (identifiers across systems) |
| Consent Transport / Starline | Different layer |
| Portal Zero Trust / same-controller metaphor | Adjacent metaphor only — do **not** collapse RSEP into Z-zones |

No stamp that Crystal applies for a gTLD or builds an alt-name registry.

---

## Watch next

1. TSG Final Report (~5 Oct 2026) + comment-response summary.  
2. Second Public Comment on **Registry Agreement** amendments.  
3. Whether Final Report adopts ENS out-of-scope carve + Unregistry “association ≠ RSEP.”  
4. Whether Bird-style transition plans land between grandfather and no-rights camps.  
5. SSAC RIDE + NCAP interaction with 2026 Round strings that already exist in ANS.

---

## Honesty

- Egress to `icann.org` / `itp.cdn.icann.org` blocked for direct curl; Depth A–C labeled in DEEP-EXTRACTS.  
- **Thin-PDF pass 25 Sep 2026:** RySG / WIPO / CleanDNS / Netnod primaries still unrecovered (CDN search miss + no Circleid paraphrase for CleanDNS/Netnod). Tucows upgraded to Depth B via indexed PDF. MeitY/ISPCP/.ART remain Circleid B-lite only.  
- Do not invent quotes for thin rows.  
- Sibling SYNTHESIS at `icann-tsg-gtld-ans-2026/` covers the same proceeding; **Bird** is middle-path (transition, no entitlement), not prior-claim — corrected here and in that pack’s pointer.

*Non Solus.*

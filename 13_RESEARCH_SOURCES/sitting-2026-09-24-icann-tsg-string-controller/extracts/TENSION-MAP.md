# Tension map — what Final Report / RA language must resolve

**Companion to:** [`DEEP-EXTRACTS.md`](DEEP-EXTRACTS.md) · [`../THEMES-public-comments.md`](../THEMES-public-comments.md)  
**Canon:** **no**  
**Updated:** 24 Sep 2026 (deep pass v2) · 6 Oct 2026 (thin-PDF recovery) · 6 Oct 2026 pass 2 (D3 A / ISPCP B / .ART B)

Four fights dominate the closed Public Comment. They are not the same question. A fifth cluster is implementation prototypes, not a fight.

---

## Fight A — Technical safety of registry-operated same-string integration

**TSG claim:** string+controller + operational controls → unlikely significant RSEP S&S harm.

**Amplifiers:** SSAC (conditional), Unregistry, **D3 (primary)**, Clowes, estmcmxci, many individuals.  
**Hardening:** SSAC independence of DNS from alt failure; continuous control measurement; URS/UDRP equivalent for alt-primary; post-launch review; IDN/LGR/EPP provisioning clarity; **MeitY primary** wants checkable RSEP gates (audits, stress tests, SLAs, stop-work); **Netnod** adds control≠resolution, convergence bounds, partition behaviour, USoT as SPOF, cryptographic control proof; **CleanDNS** wants reciprocal-takedown plumbing (cross-system abuse reporting + evidence); **ISPCP primary** wants DNSSEC-eq assurance, URS/UDRP as precondition, mandatory turn-down, max consistency window, multi-ANS + thin-registry ID, continuous conformance monitoring.

**Likely Final Report move:** keep threshold yes; add independence + measurement + post-launch review + terminology (enabled/disabled) language; watch whether Netnod’s resolution cut, MeitY/ISPCP mandatory turn-down, and ISPCP continuous-monitoring land.

---

## Fight B — Policy / remits / Picket Fence

**Claim:** Draft already regulates *how alt systems operate* and may harden into RA mandates without PDP.

**Amplifiers:** RrSG, Tucows, **.ART (primary)**, Circleid synthesis; **RySG primary** — don’t smuggle policy/contract answers into tech language; don’t blanket every ANS overlap as RSEP; **D3 primary** — don’t convert registration-data / RPM / fee questions into technical MUSTs.  
**Opposite pull:** ALAC/IPC want *more* policy process *before* any approval — not less community work. **ISPCP** wants stronger enforceable assurance *inside* the technical frame.

**Likely process move:** later Public Comment pairing Final Report with **contract language**; GNSO/community tracks for legacy + RPMs; RrSG wants IDN-EPDP lessons + registrar seat next time.

---

## Fight C — Who owns the future of strings that already live off-root

| Camp | Position |
| --- | --- |
| **Prior-claim / grandfather** | APlusDomains.Crypto, Barrett, Manoratana (.nft), Darwin — existing ANS holders must get first crack / protection before DNS delegation |
| **No rights from alt occupancy** | ENS + **RySG primary** + **D3 primary** — alt namespace ≠ DNS entitlement; collision = risk assessment; anything entering root still does Sunrise/Claims; D3: independent same-string ANS creates no claim on inventory |
| **Process deferral** | Unregistry — open §8.3 discussion now; don’t pretend the installed base is empty |
| **Anti–prior-claim** | Clowes — decline prior-claim framing (permissionless mint, colliding ANS brands, §4.6 control prerequisite); §8.3 already protects when *that operator* integrates its own namespace; keep §11 (profile ≠ second namespace) |
| **Transition plan, no entitlement** | Bird — pre-launch plan for populated ANS (inventory, verify, withhold, activate path) but **no automatic DNS entitlement** |
| **Rights machinery first** | IPC — inventory + TMCH + challenge before legacy enrollment; **WIPO (ICANN summary)** — brand challenge → withhold / integration-prohibited for infringing altroot labels; no mechanical cybersquatting import |

**Market signal (secondary):** Unstoppable withdrew ICANN apps for `.crypto` and siblings, citing rules that would force DNS registration/payment/disclosure for millions of on-chain-only names — raises the political cost of treating installed ANS bases as empty.

This fight is **outside** the TSG’s narrow charter (can RO-controlled same-string integration be safe?) but will decide political viability of any RA text.

---

## Fight D — Two directions of “integration”

| Direction | Who | Claim |
| --- | --- | --- |
| Registry → alt (RSEP service) | TSG scope | Same string under RO coordination |
| Registrant → alt contexts | ENS | DNSSEC import of *existing* DNS names; out of scope |
| Registrant → multi-network associations | Unregistry | DNSSEC TXT in registrant zone; not a registry service |
| Registry TLD → ENS root binding | estmcmxci | `_ens.nic.{tld}` DNSSEC proof → on-chain TLD assignment (prototype for §4.2/§4.6/§10) |

If Final Report blurs these, shadow/opt-in models and RSEP applicants collide.

---

## Cluster E — Implementation prototypes (not a fight)

| Prototype | Submitter | Shows |
| --- | --- | --- |
| altname-platform | Clowes | Event-triggered controller revalidation; turn-down demo |
| TLD Oracle / TLDMinter | estmcmxci | DNSSEC nic-zone binding for post-2012 gTLDs |
| Unregistry ops model | Unregistry | Registrant association records; sync-fail UX |
| .ART DNS↔Web3 (2023) | .ART / Pritz | Production one-controller TXT proof + forfeit linkage; ICANN go-ahead without RSEP |

Useful as existence proofs that Report requirements are implementable — not as endorsement.

---

## Watch list for Crystal (research only)

1. Final / revised TSG report — Sullivan posted an **updated report** to TSG shared drive **30 Sep 2026** (clean + redline); public ICANN.org PDF not confirmed here; proceeding due date was **5 Oct 2026**.  
2. Whether Final Report adopts ENS out-of-scope carve + Unregistry “association ≠ RSEP.”  
3. Whether RA draft requires SRS contactability (ALAC/IPC) or allows thin/bearer models with demonstrated RPM equivalents (SSAC §9.3).  
4. Collision / NCAP interaction with 2026 Round strings that already exist in ANS.  
5. Whether Bird-style transition plans land between grandfather camps and ENS/RySG.  
6. Whether Netnod control≠resolution + CleanDNS abuse plumbing + MeitY mandatory turn-down land.  
7. Egress allowlist for `itp.cdn.icann.org` / `www.icann.org` / `ispcp.memberclicks.net` (WIPO attachment + byte-faithful D3/ISPCP/.ART archives).  
8. Public Final Report PDF when ICANN.org publishes (Sullivan shared-Drive update ~30 Sep–1 Oct still private to TSG).  
9. No CVS product claim — compass for decentralized naming notes only.

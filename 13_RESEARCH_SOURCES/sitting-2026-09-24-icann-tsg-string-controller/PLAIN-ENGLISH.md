# Read this first (plain English)

**Canon:** no  
**Sitting:** 2026-09-24 · Grok handoff stamped 26 Sep 2026 · thin-PDF recovery 6 Oct 2026 · pass 2 (D3/ISPCP/.ART) 6 Oct 2026  
**For:** Crystal  
**Grok paste card:** [`HANDOFF-grok-bot-icann-tsg.md`](HANDOFF-grok-bot-icann-tsg.md)

Everything else in this folder is denser. This page is the same story in ordinary language.

---

## What this folder is

ICANN asked a technical group (the **TSG**) whether a normal DNS top-level domain can safely share the **same name** with an “alternative naming system” (often blockchain / Web3 names) — if the **same party controls both**.

Their draft answer (Aug 2026): **yes, if** that same-string / same-controller rule holds and ops controls hold. Comment period closed **21 Sep 2026**. Proceeding “report due” was **5 Oct 2026**. On **30 Sep 2026**, TSG coordinator Andrew Sullivan posted an **updated report** (clean + redline) to the TSG shared drive and closed his ICANN engagement — public ICANN.org PDF of that revision not confirmed here yet.

This sitting is **research**. It is not Canon. It is not a product plan. Crystal is not applying for a gTLD by filing this.

---

## The short verdict

1. Most commenters accept the technical idea (**string+controller**).  
2. They fight about four other things: how hard to harden the rules, who decides policy, what happens to names that already exist off the DNS root, and which “integration” people even mean.  
3. Several “integrations” get mixed up — registry service vs registrant DNS records vs ENS reverse import. Keep them separate.  
4. **6 Oct 2026 recovery:** RySG, CleanDNS, Netnod, MeitY, WIPO (summary), **D3 (Depth A)**, **ISPCP/.ART (Depth B)** are filed in [`extracts/DEEP-EXTRACTS.md`](extracts/DEEP-EXTRACTS.md). Netnod’s cut: control equivalence ≠ resolution equivalence. Still thin: WIPO attachment PDF bytes, public Final Report PDF, and byte-faithful CDN archives (egress).

---

## Four fights (plain)

| Fight | Plain question |
| --- | --- |
| **A Safety** | If the Web3 side breaks, does the normal DNS still work? |
| **B Fence** | Is this still “technical advice,” or are we sneaking in policy / contract rules? |
| **C Legacy** | People already hold `.crypto` / `.nft`-style names off-root — do they get first dibs in DNS, or no automatic rights? |
| **D Direction** | Are we talking registry-run links, or people publishing their own DNS→Web3 pointers? |

**Bird’s middle path:** plan a fair transition for populated alt namespaces — but that is **not** an automatic right to the DNS name.

**New plain cuts (recovery pass):**
- **RySG:** only voluntary, RO-proposed, RO-controlled integrations — no rights for independent alt namespaces.  
- **WIPO:** don’t mechanically import altroot cybersquatting into the root; brands need a challenge path.  
- **CleanDNS:** reciprocal takedown needs real abuse reporting + evidence across both systems.  
- **Netnod:** same controller ≠ same answer when you query.  
- **MeitY:** turn soft assurances into checkable RSEP gates (including mandatory turn-down).  
- **D3:** same RO-only frame as RySG/ENS — plus DNS-first for new names; don’t hard-code §8.2; no retroactive 2026 Round hit.  
- **ISPCP:** yes to string+controller, but measure divergence risk — continuous monitoring + mandatory turn-down.  
- **.ART:** already shipped a one-controller TXT+forfeit model in 2023 (no RSEP); keep tech baseline, move data/RDAP fights to PDP.

---

## What Grok Bot may do with this

- Hold the map · draft plain briefs · flag when the Final Report may have landed  
- Stay on the **research desk** — not Frequency songs, not brand posts  
- **You** publish. Bot drafts only.

Full compass: [`SYNTHESIS.md`](SYNTHESIS.md) · Fight map: [`extracts/TENSION-MAP.md`](extracts/TENSION-MAP.md)

*Non Solus.*

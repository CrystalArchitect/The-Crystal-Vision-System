# Read this first (plain English)

**Canon:** no  
**Sitting:** 2026-09-24 · Grok handoff stamped 26 Sep 2026  
**For:** Crystal  
**Grok paste card:** [`HANDOFF-grok-bot-icann-tsg.md`](HANDOFF-grok-bot-icann-tsg.md)

Everything else in this folder is denser. This page is the same story in ordinary language.

---

## What this folder is

ICANN asked a technical group (the **TSG**) whether a normal DNS top-level domain can safely share the **same name** with an “alternative naming system” (often blockchain / Web3 names) — if the **same party controls both**.

Their draft answer (Aug 2026): **yes, if** that same-string / same-controller rule holds and ops controls hold. Comment period closed **21 Sep 2026**. Final Report was **due 5 Oct 2026**. As of **6 Oct**, an updated draft is on the TSG group’s private Drive (mailing-list note) — **not** yet a public Final PDF. Second comment on contract text has **not** opened.

This sitting is **research**. It is not Canon. It is not a product plan. Crystal is not applying for a gTLD by filing this.

---

## The short verdict

1. Most commenters accept the technical idea (**string+controller**).  
2. They fight about four other things: how hard to harden the rules, who decides policy, what happens to names that already exist off the DNS root, and which “integration” people even mean.  
3. Several “integrations” get mixed up — registry service vs registrant DNS records vs ENS reverse import. Keep them separate.  
4. As of 6 Oct we recovered RySG / CleanDNS / Netnod / MeitY primaries. **WIPO** still secondary-only. Don’t invent Final Report text.

---

## Four fights (plain)

| Fight | Plain question |
| --- | --- |
| **A Safety** | If the Web3 side breaks, does the normal DNS still work? |
| **B Fence** | Is this still “technical advice,” or are we sneaking in policy / contract rules? |
| **C Legacy** | People already hold `.crypto` / `.nft`-style names off-root — do they get first dibs in DNS, or no automatic rights? |
| **D Direction** | Are we talking registry-run links, or people publishing their own DNS→Web3 pointers? |

**Bird’s middle path:** plan a fair transition for populated alt namespaces — but that is **not** an automatic right to the DNS name.

---

## What Grok Bot may do with this

- Hold the map · draft plain briefs · flag when the Final Report may have landed  
- Stay on the **research desk** — not Frequency songs, not brand posts  
- **You** publish. Bot drafts only.

Full compass: [`SYNTHESIS.md`](SYNTHESIS.md) · Fight map: [`extracts/TENSION-MAP.md`](extracts/TENSION-MAP.md)

*Non Solus.*

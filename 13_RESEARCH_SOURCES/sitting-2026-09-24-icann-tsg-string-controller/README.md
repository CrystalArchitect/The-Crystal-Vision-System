# ICANN TSG — string+controller integration (gTLD × alt naming)

**Sitting:** 24 Sep 2026  
**Trigger:** Full DRAFT paste of the TSG initial report (chat) · agent run *String controller integration*  
**Drawer:** `13_RESEARCH_SOURCES` (external policy/tech research — compass, not a CVS component)  
**Canon:** **no**

**Verdict (one line):** ICANN’s Aug 2026 TSG draft says **same string + same controller** integration of a gTLD with alternative naming systems is unlikely to create significant RSEP security/stability issues *if* operational controls hold; public comment closed **21 Sep 2026**; revised report due **~5 Oct 2026**. Public Comment splits into **four fights** (safety / fence / legacy / direction) — see [`SYNTHESIS.md`](SYNTHESIS.md).

---

## Start here

1. [`PLAIN-ENGLISH.md`](PLAIN-ENGLISH.md) — **Crystal-first** plain read  
2. [`HANDOFF-grok-bot-icann-tsg.md`](HANDOFF-grok-bot-icann-tsg.md) — **Grok Bot paste card** (research desk · crystal_confirmed 26 Sep 2026 · Canon no)  
3. [`WATCH-2026-10-06-final-report.md`](WATCH-2026-10-06-final-report.md) — Final Report watch (updated Drive draft ≠ public Final)  
4. [`SYNTHESIS.md`](SYNTHESIS.md) — integrated compass (report + comment fights)  
4. [`EXTRACT-BRIEF.md`](EXTRACT-BRIEF.md) — what string+controller requires (load-bearing rules)  
5. [`REQUIREMENTS-CHECKLIST.md`](REQUIREMENTS-CHECKLIST.md) — MUST/SHOULD + Public Comment overlay  
6. [`THEMES-public-comments.md`](THEMES-public-comments.md) — Public Comment theme map (38 active + 2 retracted)  
7. [`extracts/DEEP-EXTRACTS.md`](extracts/DEEP-EXTRACTS.md) — per-submitter deep extracts (Depth A–C)  
8. [`extracts/TENSION-MAP.md`](extracts/TENSION-MAP.md) — Fights A–D (safety / fence / legacy / direction)  
9. [`SOURCE-public-comment-roster.csv`](SOURCE-public-comment-roster.csv) — full submission roster + links  
10. [`RECEIPT-chat-paste-2026-09-24.md`](RECEIPT-chat-paste-2026-09-24.md) — how this sitting got the report text  
11. [`SOURCE-official-pdf-text-extract.txt`](SOURCE-official-pdf-text-extract.txt) — text extract of the official PDF (via search fetch; PDF binary download blocked in this environment)  
12. [`SOURCE-unregistry-comment-text-extract.txt`](SOURCE-unregistry-comment-text-extract.txt) — Unregistry comment PDF text (sample primary)  
13. [`SOURCE-estmcmxci-comment-summary-extract.txt`](SOURCE-estmcmxci-comment-summary-extract.txt) — estmcmxci.eth / TLD Oracle submission summary

**Sibling sitting (same proceeding):** [`../icann-tsg-gtld-ans-2026/`](../icann-tsg-gtld-ans-2026/) — parallel Collection Mode pack; cross-linked from SYNTHESIS.

---

## Official URLs (live as of sitting)

| Artifact | URL |
| --- | --- |
| TSG hub | https://www.icann.org/tsg/alternative-naming-systems-integrations |
| Initial report PDF (DRAFT 10 Aug 2026) | https://itp.cdn.icann.org/en/files/generic-top-level-domains-gtlds/tsg-gtld-integrations-with-alternative-naming-systems-initial-report-10-08-2026-en.pdf |
| Charter v1.1 (10 Aug 2026) | https://www.icann.org/en/system/files/files/alt-naming-systems-tsg-charter-10aug26-en.pdf |
| Public Comment proceeding | https://www.icann.org/en/public-comment/proceeding/initial-report-of-the-tsg-on-gtld-integrations-with-alternative-naming-systems-10-08-2026 |
| Convening blog (9 Jun 2026) | https://www.icann.org/en/blogs/details/gtld-integrations-with-alternative-naming-systems-technical-study-group-underway-09-06-2026-en |

**Timeline (UTC, from Public Comment page):** open 10 Aug 2026 · closed for submissions **21 Sep 2026 23:59** · report due **05 Oct 2026 23:59**.

This sitting is **after** the comment window. Do not invent a late filing unless Crystal stamps an out-of-band path.

**Public Comment roster (filed 24 Sep):** 40 submissions in CSV (2 retracted). Recovery **6 Oct:** RySG/CleanDNS/Netnod/MeitY → B; WIPO still ENS-cite; ISPCP/.ART/D3 thin. Final Report: TSG Drive update ~1 Oct, **not public** — [`WATCH-2026-10-06-final-report.md`](WATCH-2026-10-06-final-report.md).

---

## What this is (and is not)

| Is | Is not |
| --- | --- |
| Research source on DNS ↔ alt-name integration under RSEP | CrystalCore / Portal product design |
| Advice framing for ICANN org evaluating a **registry service** | Endorsement that integration *should* happen |
| Limited to **string+controller** (“same name, same party”) | Coverage of every possible integration mechanism |
| Relevant compass for CRYSTALMATRIX “decentralized identity & naming” future note | Proof TerAustralis or Crystal operates a gTLD/alt-name registry |

Connection ≠ merge. File facts here; do not drag this into Codex or Portal as a module.

---

## TSG membership (from report §12)

| Name | Affiliation (as printed) |
| --- | --- |
| Sebastien Ducos | Unstoppable Domains |
| Nick Johnson | ENS Domains |
| Brian Lonergan | Identity Digital |
| Georgia Osborn | Security and Stability Advisory Committee |
| Don Ruiz | Orange Domains |
| Swapneel Sheth | Verisign |
| Peter Thomassen | deSEC |
| Suzanne Woolf | Public Interest Registry |

Convened by ICANN CEO (announced 9 Jun 2026). Coordinator noted on Public Comment page: Andrew Sullivan.

---

## Next watch

- Revised / final TSG report after Public Comment (due ~5 Oct 2026).  
- Any standardized Registry Agreement language ICANN develops from this work (separate Public Comment, per hub page).  
- Individual RSEP filings that claim string+controller compliance.

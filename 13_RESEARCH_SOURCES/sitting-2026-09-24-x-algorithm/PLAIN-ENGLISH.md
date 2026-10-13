# Read this first (plain English)

**Canon:** no  
**Sitting:** 2026-09-24 · UTH checklist addendum 25 Sep · on `main` via PR #71 + #73  
**For:** Crystal  
**Grok paste card:** [`HANDOFF-grok-bot-x-algorithm.md`](HANDOFF-grok-bot-x-algorithm.md) (waiting on your `AGREE AGR-X-ALGO-GROK`)

Everything else in this folder is denser. This page is the same story in ordinary language.

---

## What this folder is

X (Twitter) open-sourced a large chunk of the code that builds the **For You** feed, and added **Under the Hood** so people can see visibility labels on their account/posts (and some legal withholds).

This sitting is a **research compass**: how the public code says ranking + filtering work, what is still hidden, and how to read a UTH report. It is not Canon. It is not advice to game spam or safety systems.

---

## The short verdict

1. Ranking and visibility are **two systems**. A post can score high and still be dropped.  
2. The public formula is: score = sum of (weight × predicted chance you do that action). Copy-link and replies weigh far more than likes; reports/mutes weigh hard — but weights multiply **probabilities**, not raw counts.  
3. Under the Hood answers “was I labeled?” It does **not** show Phoenix scores or who/what applied the label (automation vs your own content warning vs human).  
4. Still dark: Grox LLM **prompts**, live model weights, per-viewer feature switches, some botmaker rules, reply-thread ranking, Following/Search/etc.

---

## If your reach “died”

| Check | Meaning |
| --- | --- |
| UTH shows OON labels (`SPAM_HIGH_RECALL`, `SpamHighRecall`, …) | Followers may still see you; discovery for non-followers is crushed |
| UTH empty | Soft ranking / retrieval — not a published visibility label |
| Use | [`CHECKLIST-UTH-LABELS.md`](CHECKLIST-UTH-LABELS.md) against your JSON |

---

## What Grok Bot may do (after you stamp)

- Hold the map · draft plain briefs · help triage a UTH dump against the checklist  
- Stay on the **research desk** — not Frequency songs, not brand posts, not gaming advice  
- **You** publish. Bot drafts only.

Full compass: [`SYNTHESIS.md`](SYNTHESIS.md) · Gaps: [`WITHHELD-MAP.md`](WITHHELD-MAP.md)

*Non Solus.*

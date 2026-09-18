# Thread 5 extract — Soft-label mathematical certification

**Canon:** **no**  
**Belt:** research / coordination  
**Working-index ID:** `CVS-T5-SOFT`  
**Domains:** Mathematics (18) ↔ AI Safety (16)  
**Extracted:** 2026-09-18  
**Sources (in-hub only):** [`CROSS-DOMAIN-THREADS.md`](CROSS-DOMAIN-THREADS.md), [`RESEARCH-STATUS.md`](RESEARCH-STATUS.md)  
**Rule:** Design-ready hub extract only. No Lean proofs authored here. Connection ≠ merge.

---

## What this bead is

SWARM soft labels use `p ∈ [0, 1]` as `P(v = +1)`. Code clamps via sigmoid today; Thread 5 asks for Lean certification that **all composition operations** keep results in `[0, 1]` and that SoftPayoffEngine formulas preserve a probability interpretation.

---

## Hub status

| Step | Status |
| --- | --- |
| Lean infrastructure pointed (drawer 18) | Ready (fork-mirrors) |
| Formalize soft-label composition axioms | Not started (satellite) |
| Prove compositions stay in `[0, 1]` | Not started |
| Prove SoftPayoffEngine preserves interpretation | Not started |
| Verify SWARM aggregation against invariant | Not started |

**Risk if skipped:** malformed compositions could yield invalid probabilities (e.g. negative expected payoffs when agents are “certain”).

---

## Bead links

| Drawer | Path |
| --- | --- |
| 00_MEMORY | this file |
| 16 | [`../16_AI_SAFETY_RESEARCH/INDEX.md`](../16_AI_SAFETY_RESEARCH/INDEX.md) |
| 18 | [`../18_MATHEMATICAL_FOUNDATIONS/INDEX.md`](../18_MATHEMATICAL_FOUNDATIONS/INDEX.md) |
| Index | `CVS-T5-SOFT` |

---

<!-- topics: thread-5, soft-labels, lean, probability-invariant -->

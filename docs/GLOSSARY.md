# Glossary — v0.1

Ported from CrystalCore.OS/synthetic-affect (2026-08-14).

**gap** — `Expected − Actual`. The only drive in the system. A measurable delta,
not an emotion. Zero gap means nothing needs doing.

**magnitude** — how large the gap is, in `[0, 1]`. Scalars are all-or-nothing;
dicts are scored per differing key so partial progress is visible.

**affect label** — `closed` · `reopened` · `stalled` · `converging` ·
`uncertain`. A routing signal produced by a classifier. Functional, not felt.

**closure** — the action selected in response to a label: `stop` · `ask` ·
`rephrase` · `switch_tool` · `escalate`. The only thing that changes state.

**closure outcome** — whether a closure attempt actually shut the gap, judged by
the *following* cycle. `pending` → `worked` | `failed`. Never self-reported.

**drive** — a gap the system is acting to close. In v0.1 all drives are modelled.
They become *grounded* only when the quantity is physical — power, heat, balance
— which is the hardware column of Figure 1, and is unbuilt.

**synthetic** — apparent / functional, for design purposes. Not a claim of
feeling, consciousness, or inner experience.

---

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

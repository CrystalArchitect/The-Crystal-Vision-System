---
id: 19
slug: inference
name: Inference
group: The Predictors
arsenal: starline-arsenal
register: ARCHIVE + MIRROR
primitive: track() + label_affect() to draw conclusion under uncertainty
---

# 19 — Inference (The Predictors)

**Purpose:** Draw the conclusion the evidence actually supports — deduction, induction, or best explanation — and say which kind it is.

**CrystalCore mapping:** Register ARCHIVE + MIRROR | Primitive track() + label_affect() to draw conclusion under uncertainty | Do not let an inferred leap masquerade as an observed fact

## Core Questions — Run these, do not summarize

1. What was directly observed vs what is being inferred from it?
2. Is this deduction (must follow), induction (usually follows), or abduction (best explanation)?
3. What else could explain the same observation?
4. How confident should the inference be, given the gap between evidence and conclusion?
5. What additional observation would most cheaply tighten that gap?

## Required Concrete Output — No vague labels

- Observed vs Inferred Split
- Inference Type Label (deductive / inductive / abductive)
- Alternative Explanation List
- Confidence + Next Observation

## Evidence → Interpretation → Experiment → Record

- **Evidence:** What was measured / observed?
- **Interpretation:** What gap / affect / loop does this reveal?
- **Experiment:** Smallest test to verify?
- **Record:** CHRONICLE entry as ARCHIVE / LOOM / FORGE / MIRROR

## Anti-Pattern

Do not just name "Inference". Produce the artefact listed above. If no artefact, you have not run the model.

## Cross-references

[Provenance Stack](32-provenance-stack.md) — Inference sorts observed-vs-inferred for one reasoning step; Provenance Stack sorts the sources feeding into that step before the inference is drawn. A confident inference built on a folk-etymology-grade source is still a confident inference — Provenance Stack is what catches that upstream.

---
Implementation: CrystalCore.OS™️ | Language: CrystalCode™️ | Starline Arsenal | TerAustralis Incognita™️ | Functional / simulated affect only

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

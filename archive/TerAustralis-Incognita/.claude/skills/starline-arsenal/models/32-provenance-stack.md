---
id: 32
slug: provenance-stack
name: Provenance Stack
group: The Deconstructors
arsenal: starline-arsenal
register: ARCHIVE + LOOM
primitive: track() evidence tier + detect_gap() between claim and source
---

# 32 — Provenance Stack (The Deconstructors)

**Purpose:** Grade the reliability of evidence for a claim before treating it as settled — distinguish attested fact from reconstruction, secondary synthesis, folklore, and vision, and never let a lower tier borrow a higher tier's certainty.

**CrystalCore mapping:** Register ARCHIVE + LOOM | Primitive track() evidence tier + detect_gap() between claim and source | Prevents a Vision-layer interpretation from silently converting into Fact-layer authority

## Core Questions — Run these, do not summarize

1. What is the strongest evidence actually behind this claim — primary attestation, established scholarship, reconstruction, secondary synthesis, or pure speculation?
2. Is the claim stated with more confidence than its actual evidence tier supports?
3. Where is a compelling similarity being treated as a demonstrated connection?
4. What specific source or attestation is missing that would move this claim up a tier?
5. Is any part of this claim doing double duty as both interpretation and established fact?

## Required Concrete Output — No vague labels

- Evidence Tier Assignment (Attested / Reconstructed / Proposed / Disputed / Folk / Speculative / Symbolic)
- Confidence-vs-Tier Mismatch Flag
- Missing-Evidence List (what would raise the tier)
- Vision/Fact Boundary Statement

## Evidence → Interpretation → Experiment → Record

- **Evidence:** What was measured / observed?
- **Interpretation:** What gap / affect / loop does this reveal?
- **Experiment:** Smallest test to verify?
- **Record:** CHRONICLE entry as ARCHIVE / LOOM / FORGE / MIRROR

## Anti-Pattern

Do not just name "Provenance Stack". Produce the artefact listed above. If no artefact, you have not run the model.

## Cross-references

Overlaps with three other models — run this one first when a claim's *source quality* is the actual question, not just its logical structure:

- [First Principles](01-first-principles.md) — shares the evidenced-vs-assumed split, but Provenance Stack adds graded tiers between "evidenced" and "assumed" instead of a binary.
- [Circle of Competence](18-circle-of-competence.md) — Provenance Stack grades the *source*; Circle of Competence grades *your own* standing to judge it.
- [Inference](19-inference.md) — Inference sorts observed-vs-inferred for a single reasoning step; Provenance Stack sorts the sources feeding into that step before the inference is even drawn.
- [Occam's Razor](14-occams-razor.md) — a claim resting on a low evidence tier is exactly the kind of unearned complexity Occam's Razor cuts.

---
Implementation: CrystalCore.OS™️ | Language: CrystalCode™️ | Starline Arsenal | TerAustralis Incognita™️ | Functional / simulated affect only

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

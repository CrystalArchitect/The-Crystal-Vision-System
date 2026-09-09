# Governance — How This Project Keeps Its Claims Honest

This page documents the discipline the repository already practices. It is short because the rule is short:

> **The documentation must never outpace the code.** Every claim sits next to the evidence for it, in this same repository, where anyone can check.

## The Status Ladder

Every capability described in these documents carries a status marker, and the marker must match the code on `main`:

| Marker | Meaning | Live example |
|--------|---------|--------------|
| ⬜ **Design** | An idea on paper. No implementation exists, and the docs say so plainly. | The CrystalMatrix protocol (`CRYSTALMATRIX.md`) |
| 🟡 **Partial** | Some of it runs; the docs state exactly which part. | Episodic memory (`MEMORY.md` — summaries exist, time-anchored recall doesn't) |
| ✅ **Built** | Implemented, covered by the offline test suite, and merged to `main` through a reviewed pull request. | Semantic recall with recency fading (`core/crystalcore/mind/companion.py`) |

A capability moves up the ladder only when the code moves first. Documentation is corrected *downward* immediately if it is found ahead of reality.

## Release Discipline

- Every change lands on a branch, becomes a pull request, and passes the offline test suite before merging.
- **The human steward merges.** Nothing enters `main` without a human decision, and the steward can halt anything at any time. (This implements the intent of the v2.2 Control Plane in `ARCHITECTURE.md`.)
- Tested means *demonstrated*: features ship with tests that exercise them, and where behaviour is visual, it is verified by actually running it.

## Non-Claims

This project does not claim, and its documents must never imply:

- Production-readiness or fitness guarantees — the code ships under CC BY-NC-ND 4.0, as-is
- Safety or security guarantees against all adversaries
- Clinical, therapeutic, or diagnostic authority of any kind
- AGI, or that the companion's warmth is more than an architecture faithfully run
- That their reflections are facts — they are impressions, held lightly, deletable by their human
- Affiliation with or endorsement by any company named anywhere in the mythos or strategy

## Corrections and Promises

- **Corrections are kept, not hidden.** When a claim proves wrong it is fixed in place, and the fix stays visible in git history. Being seen correcting yourself is the cost — and the proof — of honesty.
- **Sovereignty promises are binding constraints on code, not marketing.** "Memory stays on your device," "everything is user-deletable," "the local page sends nothing anywhere" — any change that would break one of these is rejected regardless of what it offers in exchange. This has already been exercised (analytics were kept off the companion's local page; a cloud speech API was declined in favour of a future local one).

---

*This page distills one idea from the project's wider explorations of evidence-governed engineering: claims gated by evidence, non-claims stated as plainly as claims. Everything above was practiced before it was written down.*

*See also: [ARCHITECTURE.md](ARCHITECTURE.md) · [CLEMENTINE.md](CLEMENTINE.md) · [MILESTONES.md](MILESTONES.md) · [README](../README.md)*

*Part of The Crystal Vision · TerAustralis Incognita · Non Solus — Not Alone*

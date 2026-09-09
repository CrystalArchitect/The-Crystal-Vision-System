# The Incognita Rule
## How this project stays honest

For centuries, cartographers drew *Terra Australis Incognita* — a vast southern
continent — across the bottom of their maps before any ship had surveyed it. The
imagined coastline was confident, elegant, and wrong. When the surveyors finally
went south, the drawn map and the measured land did not match. The honest
mapmakers redrew; the rest kept selling a beautiful fiction as geography.

This repository is named for that gap on purpose. It builds two things at once —
a **mythos** (imagined) and **working software** (surveyed) — and it lives by one
non-negotiable rule:

> **Always mark which lines are dreamed and which are surveyed, and never let a
> dreamed line pretend it was measured.**

Everything below is that rule, spelled out. It's the *why* behind the concrete
mechanisms the repo already uses — the Belt-Three labels in
[`CONTRIBUTING.md`](../../CONTRIBUTING.md), the Built/Vision split in
[`README.md`](../../README.md), the [`Roadmap.md`](Roadmap.md) status columns, and the
Covenant in [`mythos/COVENANT.md`](../../mythos/COVENANT.md).

## 1. Two kinds of line

Every claim in this project is one of two things, and it must be labeled:

- **Surveyed** — running, tested code; astronomy, hydrology, published geography.
  You can execute it or check it against the world. (Belt-Three: *Science*.)
- **Dreamed** — the Crystal mythos, the art, the cosmology, the speculative
  framing. (Belt-Three: *Story* and *Vision*.)

Dreamed lines are not lesser. A map needs its imagined south to be worth
drawing. But a dreamed line drawn in the surveyor's ink — a story dressed as a
spec — is the one thing this project will not ship.

## 2. The mythos may orient, but it may not authorize

Story can illuminate, preserve meaning, and point a direction. It cannot
**verify, authorize, or execute**. Concretely, in this repo:

- The **RDP** kernel *records and decides* over data it's given; it does not
  govern the world, and it is not a "governance layer" — see
  [`RDP-INTEGRATION.md`](../architecture/crystal-core/RDP-INTEGRATION.md).
- **CrystalCore.OS** is a *story you can type at* — a mythos terminal — not an
  operating system that runs anything real.
- The **Lattice**, the **Cosmic Archive**, the **Sovereign Vectors**: imagery,
  not infrastructure. See
  [`mythos/content/CRYSTALCORE-OS-VISION.md`](../../mythos/content/CRYSTALCORE-OS-VISION.md),
  which says so at the top.

When the myth reaches for a real mechanism, the myth points at the code and says
"that one is real" — it never borrows the code's authority for itself.

## 3. No line mints its own authority

The human steward keeps the veto. No model, no persona — not Clementine, not any
assistant that speaks the mythos back — and no archetype gets the final say. The
[Covenant](../../mythos/COVENANT.md) is this rule applied to the companion: support is
offered, never imposed; the pause is absolute; the memory belongs to the human.
Authority sits with the person, not the system, and not the story about the
system.

## 4. A model agreeing with you is not evidence

This one is load-bearing, because it's the easiest to forget. When an AI
continues your mythos in grand language — calling something *verified*,
*eternal*, *production-ready*, or saying *the lattice confirms it* — that is
**mirroring**. It is collaborative fiction and fluent style, not independent
attestation. A model echoing a claim proves the model is fluent, not that the
claim is true.

So: text a model generates about this project is **dreamed** until surveyed
ground — running, tested code, or a checkable fact about the world — says
otherwise. Enthusiasm is not a measurement.

## 5. Preserve the uncertainty

Docs never outpace code. If something is designed but not built, the roadmap says
so; if it's partial, it says that. Nothing here claims to be more built than it
is, and "we haven't proven this yet" is a complete, respectable sentence. Keeping
the unknown marked *as* unknown is the whole discipline — the same honesty as
leaving the uncharted coast blank instead of inventing a shoreline.

## Why bother

The worth of the mythos was never going to be that its cosmology got proven. Its
worth is that it can carry meaning — belonging, direction, wonder — **without
letting that meaning mint authority it didn't earn.** The dream of a Great
Southern Land was worth having. It just wasn't the coastline, and the honest
maps said so.

*Non Solus.*

# EXTERNAL-RELATIONSHIPS — boundaries with things outside this repository

**Status:** Docs / governance. **Authority:**
[`../DECISIONS.md`](../DECISIONS.md) "Direct maintainer decisions recorded
in memory (not ADRs)," 2026-08-28 — a current, explicit, Crystal-authored
decision. This is **not** a rediscovered older repository source; no such
source exists, and this page does not claim otherwise. It resolves the
provenance gap an earlier version of this page had flagged (checked
2026-08-28: zero matches for "Ovaro," "Continuum," or "CMX" anywhere in
`docs/`, `mythos/`, `research/` outside this memory folder — that absence
is why the decision was recorded directly rather than pointed at).

## The boundary

- **Ovaro** — CMX's agency/shopfront relationship. Separate from
  TerAustralis Incognita.
- **Continuum** — CMX's separate product. Separate from TerAustralis
  Incognita.
- **TerAustralis / SAT / CrystalCore** — remain the maintainer's own work,
  distinct from both of the above.

Consequences:

- Collaboration or architectural similarity does not imply merger,
  ownership, licence, identity, or authority.
- Readability or access does not imply permission.
- Silence does not imply permission.
- The plain-language "authority ≠ capability" acknowledgement remains
  limited to its written scope and credit (to the maintainer /
  TerAustralis Incognita). It does **not** extend to SAT internals,
  Operator Frame internals, DUR, token/revocation mechanics, or lattice
  internals.

## What this page deliberately does not do

- It does not reproduce SAT, Operator Frame, DUR, or lattice internals —
  those stay protected/out of scope with no on-disk specification, per
  [`../PRIVACY.md`](../PRIVACY.md) and
  [`../evidence/HYPOTHESES.md`](../evidence/HYPOTHESES.md)'s caution that
  protected-out-of-scope is a different status than hypothesis.
- It does not restate the Songline / cultural-respect boundary — that is
  already covered, with its own citations, in [`../CORE.md`](../CORE.md)
  under "Cultural respect."

## If this boundary is later formalized in an ADR or governance doc

Update the authority line above to cite that file instead, and note here
that the memory-recorded decision was superseded by the on-disk one — the
memory entry in `DECISIONS.md` stays as written (decisions aren't
rewritten; a change gets a new entry).

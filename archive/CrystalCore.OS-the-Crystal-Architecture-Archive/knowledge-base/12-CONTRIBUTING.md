# Contributing to This Archive

How a future session or contributor extends this knowledge base without
breaking the evidence discipline it exists to hold.

## Statement

Any new factual section added to this archive follows the same
template every existing section uses:

```
## Statement
What is true today.
### Evidence
- Repository / File / Commit / ADR / README / Specification
### Historical Notes
If the architecture changed.
### Cross References
Links to related knowledge-base documents.
```

Every Statement states its own maturity explicitly — **Implemented**,
**Designed**, **Historical**, or **Unresolved** — matching the
portfolio's own STATUS.md ladder (see `05-KNOWLEDGE-MODEL.md`). Every
Evidence entry cites something a reader can independently go check: a
file path, a line number, a commit SHA, a named ADR or specification —
not "the repository was reviewed" or "this was verified."

**Status: Implemented** (this document describes the standard this
whole archive already follows).

### Evidence
Every other document in this knowledge base.

### Historical Notes
None.

### Cross References
`00-INDEX.md`.

---

## Statement

When a repository's reality changes in a way that contradicts something
this archive states, the correct move is to **add a dated note**, not
to silently overwrite the old claim. This matches the portfolio's own
conventions elsewhere: accepted ADRs are never edited after acceptance
(a reversal gets a new, superseding ADR); `Roadmap.md`'s "Recently
landed" section is dated and append-only. A future contributor updating
this archive should:

1. Verify the new reality directly against the repository — not against
   a chat session's memory, not against what a model asserts, per the
   Incognita Rule.
2. Update the relevant Statement, and add a line to its **Historical
   Notes** recording what changed and when, rather than deleting the
   old claim outright.
3. If the correction is itself worth a permanent record (a repository-
   reality mismatch, not just this archive catching up), also add an
   entry to `11-CORRECTIONS.md`.

**Status: Implemented** (as a stated process; this archive's own
`11-CORRECTIONS.md` and multiple `Historical Notes` sections already
follow this pattern).

### Evidence
`11-CORRECTIONS.md`; the `Historical Notes` sections throughout this
archive.

### Historical Notes
None.

### Cross References
`11-CORRECTIONS.md`.

---

## Statement

Never promote Vision-layer or Designed content to "Implemented" in this
archive without direct repository evidence forcing that reclassification
— running code, a passing test, a merged commit. The reverse direction
(discovering that something documented as Built no longer runs, or
never did) is exactly what this reconstruction found in several places
(`06-COMPONENTS.md`: CrystalBridge's then-undeclared dependency, since
fixed — see `11-CORRECTIONS.md` Part 3; the Crystal Runtime episode in
`07-HISTORY.md`) and should be corrected the same way when found again
— with evidence, not assumption.

**Status: Implemented** (as a stated rule this archive itself follows
throughout).

### Evidence
`06-COMPONENTS.md`, `07-HISTORY.md`.

### Historical Notes
None.

### Cross References
`05-KNOWLEDGE-MODEL.md`.

---

## Statement

This archive holds itself to the same standard it documents. If a
future pass finds this archive itself wrong — a stale citation, a
claim that no longer matches repository reality, a Statement that
overclaimed — that is a correction to *this archive*, following the
same process as any other documentation correction in the portfolio:
evidence first, a dated note, and (if it's a repository-reality
mismatch rather than this archive catching up to a change) an entry in
`11-CORRECTIONS.md`. `10-PROVENANCE.md` already models this directly —
it discloses a mistake this reconstruction caught and fixed in itself,
rather than presenting the process as flawless.

**Status: Implemented.**

### Evidence
`10-PROVENANCE.md`, "This reconstruction's verification methodology"
section.

### Historical Notes
None.

### Cross References
`10-PROVENANCE.md`.

# Decision records

Major engineering decisions get recorded, so future contributors inherit the
*why* and not just the result. The records live in [`docs/adr/`](../adr/).

## When to write one

Write an ADR when a decision is **structural, hard to reverse, or will
puzzle someone in a year**:

- changing the repository layout or where a kind of material lives
- adding, splitting, or retiring a component
- adopting or dropping a dependency, protocol, or platform
- anything that amends how governance itself works

Routine changes — a bug fix, a new test, a content page — do not need one.
If you find yourself explaining a choice at length in a PR description, that
explanation probably wants to be an ADR instead.

## Format

One file per decision: `ADR-NNNN.md`, numbered in order, never renumbered,
never deleted. Superseded decisions stay in place with their status updated
and a pointer forward. Keep to the template in
[`docs/adr/README.md`](../adr/README.md):

- **Status** — Proposed / Accepted / Superseded by ADR-NNNN
- **Context** — the situation that forced a decision
- **Decision** — what was decided, concretely
- **Consequences** — what gets better, what gets worse, what to watch

An ADR is **Accepted** when the PR carrying it merges — same authority rule
as everything else here: the maintainer's merge is the sign-off.

## Relationship to the Constitution

The [Constitution](Constitution.md) is for the small set of binding,
identity-level rules and carries its own amendment log (§8). ADRs are for
engineering decisions made *under* those rules. If an ADR would contradict
the Constitution, it's not an ADR — it's a proposed amendment, and takes the
§8 path.

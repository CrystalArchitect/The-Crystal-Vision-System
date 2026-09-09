# CONTEXT-PACK — session bootstrap, one page

**Status:** Docs / governance. A fast-start supplement to
[`CORE.md`](../CORE.md) and [`state/CURRENT.md`](../state/CURRENT.md), not a
replacement for them. If this page and either of those disagree, they win.

## What this project is, in one paragraph

**TerAustralis Incognita** (this repository) is the umbrella: governance,
ADRs, architecture documentation, the mythos, research, and the archive —
no main application code
([`Project-Boundaries.md`](../../docs/governance/Project-Boundaries.md),
ADR-0011). Working software (Clementine, the Starline Weaver, Starline,
CrystalBridge) lives in sibling repositories, chiefly
`TerAustralis-Incognita-Code`. Two things are kept honestly separate here:
Built (running, tested, checkable) and Vision (mythos, art, speculative
framing) — the Incognita Rule.

## Current branch and work

This page doesn't name a specific branch or task — that would go stale
the moment it merges (as it did for the memory-bootstrap work itself,
PR #123, merged 2026-08-28). For what's actually in flight right now:

- **Repository-wide current picture:** [`../state/CURRENT.md`](../state/CURRENT.md)
- **What's genuinely active in this repository specifically** (evidence-gated,
  not assumed): [`../projects/README.md`](../projects/README.md)
- **Your own branch, if you're mid-task:** `git status` / `git log` — this
  file can't know that in advance.

This memory protocol itself (root `CLAUDE.md` + this `memory/` tree) is
now live infrastructure, not in-progress work — see
[`../MILESTONES.md`](../MILESTONES.md) 2026-08-28 for how it landed.

## Never do these

- Modify locked names (**TerAustralis Incognita**, **CrystalVision**,
  **CrystalCore.Lattice**) without a Constitution §8 amendment.
- Edit the Constitution, Incognita Rule, or existing ADRs as if they were
  drafts.
- Rewrite `mythos/` Vision-layer content that already credits another
  contributor.
- Push to `main`, rewrite history, or merge this or any PR — the
  maintainer merges.
- Invent a fact and write it to memory because it sounds plausible. If it
  is not on disk (this repo or a sibling named by an ADR), it is
  unverified — see [`../PRIVACY.md`](../PRIVACY.md).
- Create a new GitHub repository without an ADR (`ADR-0015`).

## Privacy — read the actual floor, don't guess

[`../PRIVACY.md`](../PRIVACY.md) is the binding list of what never enters
git memory (personal/family/medical/legal detail, private messages,
credentials, appointment language). It also names categories that must
stay protected **if encountered**, even though they have no on-disk
specification in this repository: SAT-related internals, Operator Frame
internals, DUR/token mechanics, private lattice fields. Naming a protected
concept to establish a boundary is fine; reproducing its mechanics is not.
Do not confuse "protected, out of scope" with "hypothesis" — see
[`../evidence/HYPOTHESES.md`](../evidence/HYPOTHESES.md)'s own caution on
this.

## What to read, in order

1. [`../../CLAUDE.md`](../../CLAUDE.md) — the protocol itself
2. [`../CORE.md`](../CORE.md) — locked names, purpose, Incognita Rule
3. [`../state/CURRENT.md`](../state/CURRENT.md) — what is true *now*
4. [`../INDEX.md`](../INDEX.md) — retrieval map for anything task-specific
5. This page, for a faster orientation than re-deriving it from the above

## What to do if you're unsure

- **About authority:** disk canon outranks this memory folder, which
  outranks working context, which outranks a hypothesis. See
  [`../README.md`](../README.md) "Authority."
- **About Built vs. Vision:** check `state/CURRENT.md` and
  [`../../STATUS.md`](../../STATUS.md) before asserting either label.
- **About whether something is a decision:** an ADR is Accepted only once
  its PR merges ([`Decision-Records.md`](../../docs/governance/Decision-Records.md)).
  A draft or Proposed ADR is not law — see [`../DECISIONS.md`](../DECISIONS.md).
- **Before ending work:** did project state, a decision, a blocker, or the
  plan change? If yes, write it back per [`CLAUDE.md`](../../CLAUDE.md)'s
  write-back table before finishing. If no, don't touch memory just to
  have touched it.

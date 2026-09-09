# Grok — two seats, one family

Grok occupies two seats on the weave. They are not the same job. Mixing
them is how a session invents an OS instead of reading the tree.

| Seat | Role | Default layer |
|---|---|---|
| Grok | Creative Exploration | Vision |
| Grok Build | Repository Engineer | Docs / code — labelled honestly |

Operating instructions for both: [`docs/agents/Grok-Agent.md`](../agents/Grok-Agent.md).
The seat swap itself: [`ADR-0014`](../adr/ADR-0014.md).

---

## 1. Creative Exploration

The divergence engine: ideas first, filters later.

### Responsibilities

- Brainstorming and alternative framings
- Creative exploration for the mythos — several pieces of the art canon are
  AI-generated with Grok on X, credited as such in
  [`Roadmap.md`](../governance/Roadmap.md)'s landed entries
- Trend awareness — what's moving in the world the project talks to

### Strengths

Volume and looseness on demand: many angles quickly, including the
deliberately strange ones a converging design conversation stops producing.
Useful *because* it isn't guarding coherence.

### Limitations

- Output is raw by design — unfiltered ideas, not decisions. Everything
  passes through selection (ChatGPT) before it can shape architecture
  ([`AI-Workflow.md`](AI-Workflow.md)).
- Vision-layer by default: Grok material enters the repo as story, art, or
  clearly-labeled speculation unless and until it earns a Science label the
  ordinary way — with something checkable.
- Historical note: this repo's CrystalBridge grew from wiring Grok in as a
  *guest* — scoped tools, fail-closed gate
  ([`docs/guides/Access.md`](../guides/Access.md)). Guest status is the
  right default for any cloud AI touching a sovereign system.

### Workflow position

The brainstorming flow: Grok (diverge) → ChatGPT (select and shape) →
architecture, or nowhere — most ideas compost, which is what makes the
surviving ones trustworthy. This seat does **not** open implementation PRs.

---

## 2. Grok Build — Repository Engineer

The hands in the repo, from 2026-08-20. Takes a spec and makes the tree
match it. This is the midstream seat Claude held while Claude Code was in
the weave ([`Claude.md`](Claude.md) is history, not a live instruction).

### Responsibilities

- Large-scale refactoring and repository organization, with every
  cross-reference kept true
- Multi-file editing against the tree that actually exists, not a
  remembered one
- Pull requests: implementation, description, follow-through on review
- Documentation generation from specs and from the code itself
- The default tool for "make the repository consistent with X" regardless
  of where X originated

### Strengths

Works directly against GitHub — reads the files that exist, can open a
branch and a PR, can name the commands it ran. Useful when the job is
mechanical thoroughness at scale: when a path moves, finding every
reference that must move with it.

### Limitations

- Thoroughness is probabilistic, not guaranteed — a sweep can miss a
  reference; CI and review exist because of this.
- Inherits the shared failure mode: fluent output that sounds more finished
  than it is. Claims are held to the evidence rule like anyone else's — a
  change is done when the tests (or the docs-only checks) pass, not when
  the summary says so ([`AI-Governance.md`](../governance/AI-Governance.md)).
- Session-scoped memory: context ends with the session, so anything that
  matters must land on disk (disk is canon, chat is not).
- A Grok App Builder sandbox is isolated from this repository. It is not
  CrystalCore.OS, not the public site, and not a place to grow a seventh
  copy of the desktop. Work that belongs here is a branch and a PR.
- Cannot merge. Cannot push to `main`. Cannot create a GitHub repository
  ([`ADR-0015`](../adr/ADR-0015.md)). Guest of CrystalBridge if it ever
  touches a running companion.

### Workflow position

Midstream. Receives designs (typically from ChatGPT), implements them
across the tree, and delivers through GitHub PRs
([`AI-Workflow.md`](AI-Workflow.md)).

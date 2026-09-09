# AI workflow

How work flows between the AI tools on this project. This is a **working
agreement** — practiced, not enforced by software (the enforced parts of
multi-AI collaboration are the Weaver and the bridge; see
[`docs/architecture/AI-Weave.md`](../architecture/AI-Weave.md)). The rules
that bind all of it are in
[`docs/governance/AI-Governance.md`](../governance/AI-Governance.md).

Each tool has a profile in this folder; each agent has operating
instructions in [`docs/agents/`](../agents/). For the assembled picture —
roles in one table, how they connect, and what's proposed but not built —
start with [`AI-Architecture.md`](AI-Architecture.md). Midstream seat:
[`ADR-0014`](../adr/ADR-0014.md).

## The flows

**Architecture** — design before code:

> ChatGPT (design, spec) → Grok Build (implement across the repo) → GitHub (PR,
> CI, review)

**Engineering** — when the problem is mathematical or algorithmic:

> DeepSeek (analysis, algorithms) → ChatGPT (integrate into the design) →
> Grok Build (implement) → GitHub (PR, CI, review)

**Documentation**:

> ChatGPT (structure, drafting) → Grok Build (generate and place across the
> tree) → GitHub (PR, review)

**Knowledge** — digesting large material into the repo:

> Gemini (large-document analysis, synthesis) → ChatGPT (distill into
> canon-ready form) → repository (as docs or mythos content, labeled)

**Brainstorming**:

> Grok (divergent ideas) → ChatGPT (select, shape) → architecture (or the
> compost heap — most ideas don't survive, which is the point)

Grok (Creative Exploration) and Grok Build (Repository Engineer) are
different seats. Brainstorming does not skip ChatGPT and land as a PR.

## What the flows mean in practice

- Every flow **ends at the repository through a pull request** — no AI's
  output is canon until the maintainer merges it (disk is canon, chat is
  not).
- A flow is a default, not a cage. Skipping a step is fine when the work is
  small; *skipping review is never fine.*
- Handoffs happen through artifacts (a spec, a diff, a doc), not vibes —
  the receiving tool should be able to work from what's on disk.
- Every PR names the tools that touched it. Name **Grok Build** when the
  implementer was Grok Build, not "Grok".

## The standing caution

Chaining AIs multiplies fluency, not truth. Each handoff is a chance for a
dreamed line to pick up surveyed ink — so each step re-checks labels, and
the human at the end of every flow keeps the veto
([`The-Incognita-Rule.md`](../governance/The-Incognita-Rule.md) §4).

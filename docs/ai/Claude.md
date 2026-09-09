# Claude — Repository Engineer (historical)

> **Status (2026-08-20):** Claude Code is no longer in the weave. The
> Repository Engineer seat is held by **Grok Build**
> ([`Grok.md`](Grok.md) §2, [`ADR-0014`](../adr/ADR-0014.md)). This page
> is retained as the record of the seat as Claude held it. Do not treat it
> as a live instruction. Do not delete it. Do not rewrite Vision-layer
> canon that already credits Claude.

The hands in the repo: takes a spec and makes the tree actually match it.

## Responsibilities

- Large-scale refactoring and repository organization (the v1.0
  reorganization, [`ADR-0001`](../adr/ADR-0001.md), is its work)
- Multi-file editing with every cross-reference kept true
- Pull requests: implementation, description, and follow-through on review
- Documentation generation from specs and from the code itself

## Strengths

Works directly against the real repository — reads the code that exists,
runs the tests that exist, and can verify a change before proposing it.
Good at mechanical thoroughness at scale: when a path moves, finding every
reference that must move with it.

## Limitations

- Thoroughness is probabilistic, not guaranteed — a sweep can miss a
  reference; CI and review exist because of this.
- Inherits the shared failure mode: fluent output that sounds more finished
  than it is. Its claims are held to the evidence rule like anyone else's —
  a change is done when the tests pass, not when the summary says so
  ([`AI-Governance.md`](../governance/AI-Governance.md)).
- Session-scoped memory: context ends with the session, so anything that
  matters must land on disk (disk is canon, chat is not).

## Workflow position

**Was** midstream. Received designs (typically from ChatGPT), implemented
them across the tree, and delivered through GitHub PRs with CI green
([`AI-Workflow.md`](AI-Workflow.md)). Restoring this seat to Claude would
be a new ADR, not a reread of this file.

Operating instructions (historical):
[`docs/agents/Claude-Agent.md`](../agents/Claude-Agent.md).

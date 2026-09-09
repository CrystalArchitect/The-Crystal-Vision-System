# Architecture Decision Records

Why the big calls were made, one file per decision. The process — when a
decision needs one, how one is accepted — is in
[`docs/governance/Decision-Records.md`](../governance/Decision-Records.md).

## Index

| ADR | Title | Status |
|---|---|---|
| [ADR-0001](ADR-0001.md) | Adopt the CrystalCore OS v1.0 repository architecture | Accepted |
| [ADR-0002](ADR-0002.md) | Content areas: the mythos stays a top-level peer of docs and src | Accepted |
| [ADR-0003](ADR-0003.md) | Move code into src/ as a uniform shift; keep runtime-coupled files with their code | Accepted |
| [ADR-0004](ADR-0004.md) | Lock the CrystalCore naming taxonomy; ban future CrystalCore-* runtime names | Accepted |
| [ADR-0005](ADR-0005.md) | AI Orchestrator — consolidate the naming; ship the concept as documentation first | Accepted |
| [ADR-0006](ADR-0006.md) | Licensing strategy — keep the dual license, record the IP principles, flag trademark as unfinished | Accepted — §1 superseded by ADR-0008 |
| [ADR-0007](ADR-0007.md) | Correct the project name to "TerAustralis Incognita"; rename mythos/teraaustralis/ | Accepted |
| [ADR-0008](ADR-0008.md) | Supersede ADR-0006 §1 — adopt CC BY-NC-ND 4.0 for code; reconcile the fallout | Accepted |
| [ADR-0009](ADR-0009.md) | Reconcile the licensing chaos — CC BY-NC-ND governs today; packages/ is an in-progress target | Accepted — target question resolved by ADR-0010 |
| [ADR-0010](ADR-0010.md) | Uniform CC BY-NC-ND 4.0 for the whole repository; differentiated per-package licensing not adopted | Accepted |
| [ADR-0011](ADR-0011.md) | Adopt the three-project boundary model — umbrella, Crystal Core, Crystal Vision | Accepted |
| [ADR-0012](ADR-0012.md) | Site visual-token layer now; domain restructure deferred behind triggers | Proposed |
| [ADR-0013](ADR-0013.md) | Extend uniform CC BY-NC-ND 4.0 across the whole portfolio; retire Apache-2.0 and the unlicensed repositories | Accepted |
| [ADR-0014](ADR-0014.md) | Grok Build takes the Repository Engineer seat; Claude retained as history | Accepted |
| [ADR-0015](ADR-0015.md) | Stop growing the constellation — no new GitHub repository without an ADR | Accepted |
| [ADR-0016](ADR-0016.md) | Recognize samuelsalmon3/SourceCode as an external peer, not a CrystalCore module | Proposed |

## Template

```markdown
# ADR-NNNN: <decision in one line>

**Status:** Proposed | Accepted | Superseded by ADR-NNNN
**Date:** YYYY-MM-DD

## Context

The situation that forced a decision, with the constraints that mattered.

## Decision

What was decided, concretely — paths, names, mechanisms.

## Consequences

What gets better, what gets worse, what to watch for.
```

Numbers are permanent: never renumber, never delete. A reversed decision
gets a new ADR that supersedes the old one.

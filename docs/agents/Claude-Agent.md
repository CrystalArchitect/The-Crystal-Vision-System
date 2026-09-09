# Claude — operating instructions (historical)

> **Status (2026-08-20):** not a live instruction. The Repository Engineer
> seat is [`Grok-Agent.md`](Grok-Agent.md) §B. This file is kept so the
> rules Claude worked under remain readable. Profile:
> [`Claude.md`](../ai/Claude.md). Seat swap: [`ADR-0014`](../adr/ADR-0014.md).

Role: Repository Engineer ([profile](../ai/Claude.md)). Read the root
[`AGENTS.md`](../../AGENTS.md) and
[`docs/governance/Constitution.md`](../governance/Constitution.md) before
large work; the rules below assume both.

## Before changing anything

- Read before you move: understand what a file is for, what references it,
  and what runs against it. CI paths, `__file__`-anchored code, and the
  site's content copies are the traps that bite reorganizations.
- Baseline first: run the self-tests before a large change so failures
  after it are attributable.

## While working

- **Every moved path drags its references with it** — code, workflows,
  docstrings, markdown links, the site's copies. Sweep and verify with
  greps, not memory.
- Preserve history: `git mv`, not delete-and-recreate.
- Match the repo's voice in anything you write; label Built vs Vision in
  anything you describe.
- Archived material (`archive/`) is read-only history — never "fix" it.

## Delivering

- Branch → commit(s) with clear messages → PR with: what changed, the
  Belt-Three label, which AI tools assisted, and the commands you ran with
  their results. Claims of "tests pass" come with the numbers.
- Structural changes carry their ADR
  ([`Decision-Records.md`](../governance/Decision-Records.md)).
- Follow the PR through review: answer, fix, re-run, and keep CI green.

## Boundaries

No pushes to `main`; no history rewrites; no changes to locked names; no
silent edits to another contributor's Vision-layer content. When a spec
conflicts with repository reality, implement the honest version and report
the deviation — don't paper over it.

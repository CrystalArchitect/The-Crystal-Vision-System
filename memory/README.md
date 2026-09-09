# memory/ — durable Claude Code memory

**Status:** Docs / governance. This directory is a working map, not canon.

Canon lives in `docs/governance/`, `docs/adr/`, `mythos/`, and the other
repository sources this folder points at. Memory **summarises and dates**.
If a summary here disagrees with a canonical file, the canonical file wins
and the conflict is recorded.

Root instruction: [`../CLAUDE.md`](../CLAUDE.md).

## Why this exists

Claude sessions work across repositories. Anything that matters must land on disk
([`docs/ai/Claude.md`](../docs/ai/Claude.md): "disk is canon, chat is not").
This folder is the **primary source of truth** for all Claude Code sessions, wherever they work.

Sessions in any repository (TerAustralis-Incognita-Code, TheCrystalVision, etc.) read this umbrella memory/ at startup for:
- Project-wide decisions, milestones, open questions
- Current state of all systems
- Cross-repo coordination

Then they read repo-specific memory (if available) in [`projects/`](projects/) for local detail.

It does **not** restore the Repository Engineer seat. That seat is Grok
Build ([`docs/adr/ADR-0014.md`](../docs/adr/ADR-0014.md)).

## Protocol

**Read at startup**

1. [`CORE.md`](CORE.md) — locked names, purpose, Incognita Rule, cultural floor
2. [`state/CURRENT.md`](state/CURRENT.md) — what is true *now*

**Retrieve by task** — [`INDEX.md`](INDEX.md). **Which source has final say
over a concept** (as opposed to which file to read for a task) —
[`CANON-MAP.md`](CANON-MAP.md).

**Identify the relevant project, if any** — [`projects/README.md`](projects/README.md).
Most work in this repository has no dedicated project memory because it
isn't tracked separately from the root state files; read a project's own
`CURRENT.md`/`DECISIONS.md`/`PLAN.md`/`OPEN-QUESTIONS.md`/`HANDOFF.md`
only when `projects/README.md` says a subdirectory exists for it.

**Write before ending meaningful work**

- [`DECISIONS.md`](DECISIONS.md)
- [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md)
- [`MILESTONES.md`](MILESTONES.md)
- [`state/CURRENT.md`](state/CURRENT.md)
- The relevant project's own files, if one exists ([`projects/README.md`](projects/README.md))

**Never write** — [`PRIVACY.md`](PRIVACY.md)

**Evidence discipline** — before writing a claim as fact, check
[`evidence/VERIFIED.md`](evidence/VERIFIED.md) (has it actually been run
or measured?), [`evidence/HYPOTHESES.md`](evidence/HYPOTHESES.md)
(plausible but not verified — and never the place for protected/private
categories), and [`evidence/CONFLICTS.md`](evidence/CONFLICTS.md) (do two
sources disagree? record it, don't silently pick one).

**How AI tools hand off work** — [`collaboration/AI-HANDOFF.md`](collaboration/AI-HANDOFF.md).
**Fast session orientation** — [`collaboration/CONTEXT-PACK.md`](collaboration/CONTEXT-PACK.md).
**Boundaries with things outside this repository** — [`collaboration/EXTERNAL-RELATIONSHIPS.md`](collaboration/EXTERNAL-RELATIONSHIPS.md),
authority recorded in [`DECISIONS.md`](DECISIONS.md) "Direct maintainer
decisions."

## Labels (do not collapse)

| Memory label | Incognita Rule | Belt-Three ([`CONTRIBUTING.md`](../CONTRIBUTING.md)) |
|---|---|---|
| **Built** | Surveyed — running, tested, or checkable against the world | Science |
| **Vision** | Dreamed — mythos, art, speculative framing, labeled as such | Story and Vision |
| **Unknown** | Preserve the uncertainty. Docs never outpace code | Honest gap; not a third cosmology |

Unknown is not a license to invent a shoreline. See
[`The-Incognita-Rule.md`](../docs/governance/The-Incognita-Rule.md).

## Authority

Canonical source / locked canon **>** this folder **>** current working
context **>** hypotheses.

## Files

| File | Role |
|---|---|
| [`CORE.md`](CORE.md) | Slow-changing identity. Rarely edited. |
| [`INDEX.md`](INDEX.md) | Retrieval map into the real tree — what to read for a task. |
| [`CANON-MAP.md`](CANON-MAP.md) | Authority map — which file has final say over a concept, and known overlaps/gaps. |
| [`FRAMEWORKS.md`](FRAMEWORKS.md) | Named frameworks, skills, Drive papers — pointers only. |
| [`PRIVACY.md`](PRIVACY.md) | What never enters git memory. |
| [`DECISIONS.md`](DECISIONS.md) | Pointers at ADRs. Not a second ADR log. |
| [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) | Live gates. |
| [`MILESTONES.md`](MILESTONES.md) | Recently landed, dated. |
| [`state/CURRENT.md`](state/CURRENT.md) | Working picture. Overwritten each checkpoint. |
| [`collaboration/`](collaboration/) | AI handoff protocol, fast session bootstrap, external boundaries. |
| [`evidence/`](evidence/) | Verified claims, open hypotheses, recorded source conflicts — kept distinct so a hypothesis never quietly becomes a fact. |
| [`projects/`](projects/) | Project-specific memory, created only where a real project needs one. |

*Non Solus.*

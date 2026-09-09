# memory/ — this repo's own working memory

**Status:** Docs / governance. Working map for **this repository only** —
The-Crystal-Vision-System monorepo, the connective layer (see root
[`README.md`](../README.md) row in [`memory/INDEX.md`](INDEX.md)).

## Scope — read this before writing here

This repo now physically contains other projects' full history, imported as
isolated `archive/<name>/` subtrees (see [`MONOREPO-INDEX.md`](../MONOREPO-INDEX.md)).
Several of those subtrees carry their **own** `memory/` directory and their
**own** protocol — most notably [`archive/TerAustralis-Incognita/memory/`](../archive/TerAustralis-Incognita/memory/),
governed by that subtree's own `archive/TerAustralis-Incognita/CLAUDE.md`.

**This file's directory is not that one, and does not read from or write
into it.** Root [`README.md`](../README.md) is explicit: *"Does not replace
CrystalCore, Clementine, SAT, Starlines, Dreamlines, TerAustralis, or
Celestial Portal. Do not merge those repos."* Importing a subtree's files
into `archive/` was a deliberate, separate consolidation decision (see
[`DECISIONS.md`](DECISIONS.md)) — it does not repeal that rule. A session
working inside `archive/TerAustralis-Incognita/` (or any other subtree)
should follow *that* subtree's own memory protocol, not this one. A session
working on the monorepo itself (this file's level: consolidation state,
cross-subtree pointers, the `/generate` endpoint work, drawer structure)
reads and writes here.

## Protocol

**Read at startup:** [`CORE.md`](CORE.md), then only the row you need from
[`INDEX.md`](INDEX.md). Do not ingest a subtree's memory as if it were this
one's.

**Write before ending meaningful monorepo-level work:**

- [`DECISIONS.md`](DECISIONS.md) — confirmed decisions about this repo
  itself (structure, consolidation, endpoint design), pointer-style
- [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) — live gates at the monorepo level
- [`MILESTONES.md`](MILESTONES.md) — dated, landed work
- [`00_MASTER_INDEX/WORKING-INDEX.md`](../00_MASTER_INDEX/WORKING-INDEX.md) —
  per [`README.md`](../README.md)'s filing rule, one row per new thing filed

**Never write:** [`PRIVACY.md`](PRIVACY.md).

## Files

| File | Role |
| --- | --- |
| [`CORE.md`](CORE.md) | Slow-changing identity: authority, canon, what not to collapse or invent. |
| [`INDEX.md`](INDEX.md) | Retrieval map — what to read for a task. |
| [`DECISIONS.md`](DECISIONS.md) | Confirmed decisions about this repo, dated, pointer-style. |
| [`MILESTONES.md`](MILESTONES.md) | Dated, landed work. Newest first. |
| [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md) | Live gates — not yet resolved. |
| [`PRIVACY.md`](PRIVACY.md) | What never enters this repo's git history. |

## Authority

Drive (CVSC, locked root) and GitHub outrank this folder. This folder
outranks chat. An AI agreeing with something is not evidence — see
[`CORE.md`](CORE.md).

*Non Solus.*

# CLAUDE.md — Claude Code memory protocol

This file is navigational. It is not the project. Do not dump canon here.

Claude Code is **not** the live Repository Engineer seat. That seat is **Grok Build** ([`docs/adr/ADR-0014.md`](docs/adr/ADR-0014.md)). Claude's profile stays on disk as history ([`docs/ai/Claude.md`](docs/ai/Claude.md)). This protocol exists so that **if** a Claude Code session runs, it reads and writes durable memory instead of improvising from chat.

## Authority (highest first)

1. Canonical source / locked canon
2. Verified repository memory (`memory/`)
3. Current working context
4. Hypotheses / assumptions

If memory conflicts with newer canonical source, follow the canonical source and record the conflict in `memory/`.

Locked names, the Constitution, and existing canon are **not** editable without Crystal's explicit approval ([`docs/governance/Constitution.md`](docs/governance/Constitution.md) §1, §8).

## Every session

### For sessions working in any repo (cross-repo context)

This umbrella repository's `memory/` is the **primary source of truth** for all Claude Code sessions across the project. Sessions work locally in their own repo (TerAustralis-Incognita-Code, TheCrystalVision, etc.) but read and write to this umbrella's memory/ for shared state.

1. **Read** [`memory/CORE.md`](memory/CORE.md) and [`memory/state/CURRENT.md`](memory/state/CURRENT.md) at startup — these describe the entire project's state.
2. **Retrieve** task-specific files via [`memory/INDEX.md`](memory/INDEX.md). Do not load the whole tree by default.
3. **Identify the relevant repo and project**, if any, via [`memory/projects/README.md`](memory/projects/README.md). If you're working in a specific repo (e.g., `-Code`), read [`memory/projects/Code/`](memory/projects/Code/) for repo-specific state. Read that project's own `CURRENT.md` / `DECISIONS.md` / `PLAN.md` / `OPEN-QUESTIONS.md` / `HANDOFF.md` only where one exists.
4. Treat canonical repository source and locked canon as higher authority than memory summaries.
5. Preserve **Built / Vision / Unknown** distinctions under the Incognita Rule ([`docs/governance/The-Incognita-Rule.md`](docs/governance/The-Incognita-Rule.md)). Surveyed vs dreamed. Never let a dreamed line pretend it was measured.
6. Never invent canon. Never promote a hypothesis into a verified fact without evidence on disk.
7. If memory conflicts with newer canonical source, follow the canonical source and record the conflict.
8. **Before ending or checkpointing meaningful work**, update the relevant memory files:
   - Umbrella state: [`memory/state/CURRENT.md`](memory/state/CURRENT.md), [`memory/DECISIONS.md`](memory/DECISIONS.md), [`memory/OPEN-QUESTIONS.md`](memory/OPEN-QUESTIONS.md), [`memory/MILESTONES.md`](memory/MILESTONES.md)
   - Repo-specific state: [`memory/projects/REPO-NAME/CURRENT.md`](memory/projects/Code/CURRENT.md) (and other repo project files)
9. Never modify locked names, the Constitution, or existing canon without Crystal's explicit approval.
10. Readable is not the same as permitted. Access to a file does not widen what you're authorized to do with it or claim about it.
11. An AI's inference, however confident, is not Crystal's decision. Only a merged PR, an on-disk ruling, or Crystal saying so directly counts as one.
12. If Crystal corrects something and the correction is durable, update the memory file it affects — and this file too, if the correction changes the protocol itself.

## Write-back (required)

This is a read-**and**-write protocol, not a startup reader.

| Event | Write to |
|---|---|
| Confirmed decision (merged ADR, maintainer ruling on disk) | [`memory/DECISIONS.md`](memory/DECISIONS.md) — summary plus pointer; the ADR remains the record |
| New open question | [`memory/OPEN-QUESTIONS.md`](memory/OPEN-QUESTIONS.md) |
| Landed milestone | [`memory/MILESTONES.md`](memory/MILESTONES.md) and, if it changes "now", [`memory/state/CURRENT.md`](memory/state/CURRENT.md) |
| Session-end state | [`memory/state/CURRENT.md`](memory/state/CURRENT.md) |
| Privacy-sensitive material offered in chat | Do **not** write it. See [`memory/PRIVACY.md`](memory/PRIVACY.md) |

Lodge only what is confirmed. Do not shotgun chat into `memory/`. A model agreeing with you is not evidence ([Incognita Rule](docs/governance/The-Incognita-Rule.md) §4).

## Map

- Protocol home: [`memory/README.md`](memory/README.md)
- Retrieval (what to read for a task): [`memory/INDEX.md`](memory/INDEX.md)
- Authority (which file has final say over a concept): [`memory/CANON-MAP.md`](memory/CANON-MAP.md)
- Named frameworks / skills / Drive papers: [`memory/FRAMEWORKS.md`](memory/FRAMEWORKS.md)
- Privacy floor: [`memory/PRIVACY.md`](memory/PRIVACY.md)
- Agent rules for every model: [`AGENTS.md`](AGENTS.md)

*Non Solus.*

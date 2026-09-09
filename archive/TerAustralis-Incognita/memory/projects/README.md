# PROJECTS — cross-repo state and evidence-gated activity

**Status:** Docs / governance. This directory tracks state for Claude Code sessions working across the project's repositories.

## Cross-repo memory model

This umbrella repository's `memory/` is the **primary source of truth** for all Claude sessions. Sessions working in other repos (e.g., TerAustralis-Incognita-Code, TheCrystalVision) read umbrella memory/ at startup and write back to it.

When a session works in a specific repo, it reads:
1. Umbrella state: [`../state/CURRENT.md`](../state/CURRENT.md), [`../DECISIONS.md`](../DECISIONS.md), etc.
2. Repo-specific state: `<repo>/CURRENT.md`, `<repo>/DECISIONS.md`, etc. (if the repo has a subdirectory here)

## What qualifies for a repo subdirectory

Evidence, not a folder existing: active work, recent commits, open branches or PRs, or the maintainer naming it active. A repo gets its own directory **only if** its state is substantial enough to warrant separation from umbrella files.

Per [`../../docs/governance/Project-Boundaries.md`](../../docs/governance/Project-Boundaries.md), this umbrella owns no main application code — Clementine, Starline Weaver, and related systems live in `TerAustralis-Incognita-Code` and sibling repos. Their status is tracked in this directory AND in umbrella-level [`../MILESTONES.md`](../MILESTONES.md), [`../state/CURRENT.md`](../state/CURRENT.md), [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md).

## Active repositories

| Repo | Directory | Status | Track via |
|---|---|---|---|
| TerAustralis-Incognita-Code | `Code/` | Active | umbrella + repo-specific |
| TheCrystalVision | `TheCrystalVision/` | Active | umbrella + repo-specific |

Non-repo tracked project (public accountability, not code):

| Project | Directory | Status | Track via |
|---|---|---|---|
| 90-Day Public Roadmap (Aug 30 → Nov 28, 2026) | [`90-Day-Roadmap/`](90-Day-Roadmap/) | Active — #5 shipped, #8 started, #7 paused pending a mechanism decision | [`90-Day-Roadmap/CURRENT.md`](90-Day-Roadmap/CURRENT.md) |

## Recently concluded

### Repository Memory Bootstrap — COMPLETE 2026-08-28

Root `CLAUDE.md` + the `memory/` tree itself. Landed via PR #123, merged
at `3ba08fdcb4e88f5386949bc3cd35a28dcd597fab` with Crystal Arena-Turner's
explicit authorization. This is now foundational repository
infrastructure — the protocol every Claude Code session runs under — not
an ongoing project needing its own memory. No
`memory/projects/repository-memory-bootstrap/` subdirectory was created:
this work's history lives in git (the PR itself) and its current state in
the root files every other session already reads
([`../state/CURRENT.md`](../state/CURRENT.md),
[`../DECISIONS.md`](../DECISIONS.md), [`../MILESTONES.md`](../MILESTONES.md)).
If a future session substantially redesigns this memory architecture,
that work may earn its own project subdirectory at that time — this entry
doesn't reserve one in advance.

## Not active here (tracked in sibling repos or as design-not-built)

For status, do not re-derive — read:

- [`../state/CURRENT.md`](../state/CURRENT.md) — what's Built/Vision/Unknown, now
- [`../MILESTONES.md`](../MILESTONES.md) — dated landings
- [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) — "Designed, not built"
- [`../../docs/governance/Roadmap.md`](../../docs/governance/Roadmap.md) — the Built-layer status page

## When to create a project subdirectory

Only when a genuinely active, substantial piece of work in *this*
repository would otherwise force root-level `DECISIONS.md`/`OPEN-QUESTIONS.md`/
`MILESTONES.md` to carry detail that isn't useful to every other session.
Then, and only then:

```
memory/projects/<project>/
├── README.md          — what/owner/status/canonical sources/privacy
├── CURRENT.md          — current truth only, dated
├── PLAN.md             — ACCEPTED | PROPOSED | BLOCKED | DEFERRED | REJECTED, not a wishlist
├── DECISIONS.md        — date, decision, status, source, reason, consequence
├── OPEN-QUESTIONS.md   — this project's blockers specifically
├── MILESTONES.md       — this project's own dated landings
├── REFERENCES.md       — canonical source paths
└── HANDOFF.md          — lets another session continue without this chat
```

Do not create empty files from this template to look complete. Create only
the files a real handoff would need.

# CROSS-AI-MEMORY-ARCHITECTURE — a design hypothesis, not built

**Label:** Vision / design hypothesis. **Not implemented.** No code, no
storage, no sync mechanism, no access control exists for any of this.
Nothing here is Built.

**Do not confuse this with the memory system already live in this git.**
The `memory/` tree this file lives in (`CLAUDE.md` + `memory/*`, PR #123)
is a **repository-memory protocol** — durable state for Claude Code
sessions working on *this codebase*. The system described below is a
different, much larger, entirely undesigned idea: a **personal
identity/context store for a human**, readable by any AI the human uses,
so that AI grounds itself in fact instead of inventing who the human is.
The two share design language (Fact/Vision/Unknown labeling, disk-over-chat,
provenance) but are not the same system, do not share storage, and this
umbrella repo's own memory protocol is not a candidate implementation of
the personal one.

**Origin:** Consolidated from a Claude Code chat conversation
(2026-08-29) into a durable record, per the repository's own rule that
disk is canon and chat is not. This is a direct record of what was
discussed and provisionally agreed in that conversation — it carries the
authority of "this was decided in session," nothing more. It is not
maintainer-ratified architecture and has no ADR.

## The problem being solved

Every AI a person uses (Claude, ChatGPT, others) currently builds its own
model of who that person is from scratch, from chat history alone. There
is no shared, authoritative source those AIs read from — so each one
guesses, and the guesses drift. The goal is a central store any AI can
read, so it's grounded in what's actually true rather than developing its
own interpretation.

## The four layers

### 1. Individual Memory — sovereign, on-device

- Stays on the person's own device. Never syncs, never leaves.
- Holds: health, finances, legal matters, family, relationships, private
  goals — anything where disclosure has real personal cost.
- No AI reads this by default. Only the person themselves.
- Example test: "I have chronic pain" → Individual. "I'm in debt" →
  Individual.

### 2. Collective Memory — shareable, any-AI-readable

- What the person has chosen to make available to AI systems: active
  projects, decisions made, public-facing context, working state.
- Backed by **Continuum** in two ways, both agreed in chat: as the
  literal storage/sync layer, and as an architectural pattern to follow
  for how that layer is structured. Neither has been designed yet —
  Continuum is CMX's separate product (see
  [`collaboration/EXTERNAL-RELATIONSHIPS.md`](collaboration/EXTERNAL-RELATIONSHIPS.md));
  what "backed by Continuum" concretely means for a system outside CMX is
  still open.
- Individual entries here should follow the taxonomy in
  [`MEMORY-STATE-MODEL.md`](MEMORY-STATE-MODEL.md) (Fact / Interpretation
  / Inheritance / Revision / Vision / Unknown) once that model is
  developed further — the two documents describe the same undesigned
  system at different zoom levels.
- Example test: "I'm working on TerAustralis memory systems" →
  Collective. "I decided to use git-based state over a database" →
  Collective.

### 3. Starline Arsenal — cognitive processing layer

- The existing 13-model cognitive framework
  ([`.claude/skills/starline-arsenal/`](../.claude/skills/starline-arsenal/)),
  already Built as a Claude Code skill for this project.
- In this architecture it plays a double role, per the chat conversation
  ("a mixture"): it can *structure* how memories are organized
  (deconstruction / prediction / creation / adaptation as categories),
  and it can *process* memory when an AI engages with it — generating
  concrete outputs (failure lists, leverage audits, Bayesian updates)
  from what Collective Memory holds, rather than just reading it passively.
- How exactly Arsenal invokes on memory (automatically, on request, per
  category) is undesigned.

### 4. SAT (Synthetic Affect Theory) — affective substrate

- SAT's role in this architecture is affect computed at the
  silicon/substrate level — described in chat as "to do with the
  silicone [sic — silicon]."
- SAT has a dedicated private research repository
  (`Synthetic-Affect-Theory-`, see [`INDEX.md`](INDEX.md)) and its
  internals are **protected** — no specification exists in this
  repository and none should be reproduced here, per
  [`PRIVACY.md`](PRIVACY.md).
- This document names SAT only to record that it belongs in the stack
  and roughly where (the affective layer under Arsenal's cognition,
  same relationship as feeling sits under reasoning). It says nothing
  about SAT's actual mechanics.

## How the layers were sketched relating to each other (chat-level, not designed)

```
Individual Memory   (sovereign, device-only)
        |
        | person chooses what crosses the boundary
        v
Collective Memory   (shareable, Continuum-backed, any AI reads)
        |
        | Arsenal structures/processes what's read
        v
Starline Arsenal    (cognitive models — structure + processing)
        |
        | affect computed underneath reasoning
        v
SAT                 (affective substrate, protected internals)
```

This is illustrative, not a data-flow spec. No mechanism connects any two
of these boxes today.

## Open gaps — identified, none resolved

These were surfaced during design discussion and remain unanswered. Listed
here so they aren't re-derived from scratch next session:

| Gap | Question |
|---|---|
| Consent / access control | What mechanism decides what crosses Individual → Collective? This repo already has a "Consent Transport" component (RDP kernel, described for the `-Code` tree) — reuse it, or build something new? |
| Revocation | Once an AI or platform has read Collective Memory, how is its access cut off later? |
| Interoperability | "Any AI" is the goal, but only Claude Code has a session-start hook into this kind of memory. ChatGPT, Gemini, etc. have no equivalent — how does memory actually reach them? |
| Provenance | Every entry needs to record who/what wrote it and when — otherwise verified fact and AI guess become indistinguishable later. |
| Decay / pruning | Does anything get archived or retired, or does Collective Memory grow forever? |
| Conflict resolution mechanism | `MEMORY-STATE-MODEL.md`'s Rewrite operator names the principle (old version stays, new version added, consequences traced) but no technical mechanism exists for multiple AIs writing back without collision. |
| SAT ↔ Arsenal bridge | Does affect (SAT) ever trigger which cognitive model (Arsenal) runs, or are they fully independent? |
| Authority over Individual Memory edits | Collective Memory already has a human-authority model in this repo (Crystal as final authority). Does Individual Memory ever accept AI-proposed edits, or is it human-only, always? |

## What this page is not

- Not a schema, storage engine, sync protocol, or access-control system.
- Not an authorization to build any of this. It's a record of a design
  conversation, not a build order.
- Not evidence that Continuum, Starline Arsenal, or SAT will function
  together this way. Nothing here has been tested.
- Not a change to this repository's own Claude Code memory protocol
  (`CLAUDE.md`, PR #123/#129) — see the disambiguation note at the top.

*Non Solus.*

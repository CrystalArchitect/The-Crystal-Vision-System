# MEMORY-STATE-MODEL — a design hypothesis for memory entries

**Label:** Vision / design hypothesis. **Not implemented.** No code, no
schema, no enforcement exists for any of this yet. Nothing here is Built.

**Origin:** Synthesized in a Claude Code session (2026-08-29) from Crystal's
own design thinking about how AI-readable memory should distinguish fact
from interpretation. Recorded here as a working paper, same status as the
Loop Framework or Number Collision Framework in
[`FRAMEWORKS.md`](FRAMEWORKS.md) — a method under consideration, not law.

**Why it exists:** the umbrella memory bootstrap (`memory/`, live since PR
#123) already distinguishes Built / Vision / Unknown for *repository
state*. This page asks a narrower question: if a broader personal or
cross-AI memory system gets built later (individual + collective memory,
discussed in chat but not yet designed on disk), what should an individual
memory *entry* be allowed to claim about itself? This is preparatory
thinking for that possible future system, not a change to the existing
repository-memory protocol.

## The six entry states

An individual memory entry should be labeled as exactly one of:

| State | Meaning |
|---|---|
| **Fact** | What was actually recorded or observed |
| **Interpretation** | What someone thought a fact meant |
| **Inheritance** | What a later session/agent received from a prior state |
| **Revision** | A later reinterpretation of an earlier fact or decision |
| **Vision** | What someone imagined but hasn't built |
| **Unknown** | Unresolved, not yet decided |

These must not collapse into one another. A Vision does not become a Fact
by being repeated; an Inheritance is not automatically true just because
it was passed down. This extends the existing Built/Vision/Unknown
labeling already required by the Incognita Rule
([`../docs/governance/The-Incognita-Rule.md`](../docs/governance/The-Incognita-Rule.md))
— it does not replace it.

## Three operators on memory

- **Bridge** — connect two previously separate states or domains without
  merging their identities.
- **Carry** — pass information from an earlier state into a new one,
  without forcing the new state to repeat the old conclusion. Inheritance
  is not a command.
- **Rewrite** — revisit an earlier interpretation. The old version stays
  on record, the new version is added, and what changed as a result is
  traced. Never a silent overwrite.

## Governing principle

Repeat the *structure* (the same categories, the same questions asked of
new material), never repeat the *state* (the same conclusion, treated as
still true without being re-checked). A memory system that only preserves
the past risks becoming deterministic — old conclusions get treated as
destiny. A system that only chases what's new risks becoming amnesiac.
The target is persistent memory, revisable interpretation, and an
independently movable forward state.

## Practical rule for any AI reading memory

"This happened" is not the same claim as "this must happen again." An AI
grounding itself in memory should read prior entries as context to reason
from, not as instructions to reproduce. This is the same rule already
governing this repository's own memory protocol
([`CLAUDE.md`](../CLAUDE.md) §6: "Never invent canon. Never promote a
hypothesis into a verified fact without evidence on disk.") — restated
here for entry-level granularity, in case a future personal/collective
memory system is designed on top of it.

## What this page is not

- Not a schema. No file format, storage engine, or sync mechanism is
  specified.
- Not an authorization to build a personal/collective memory system. That
  remains an open, undesigned idea discussed in chat.
- Not evidence that any external framework or fictional narrative
  "proves" this model works. It doesn't; nothing does yet. This is
  design thinking, not validation.

*Non Solus.*

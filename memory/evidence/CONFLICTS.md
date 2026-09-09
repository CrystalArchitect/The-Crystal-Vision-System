# CONFLICTS — where sources disagree

**Status:** Docs / governance. Record disagreements here instead of
silently picking a winner. Do not close an entry from chat — closing
requires an on-disk resolution (a fix, an ADR, or the maintainer settling
it), same as [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md)'s write-back
rule.

## Open

None currently.

## How to log a new conflict

```
**Topic**
- What each source claims, with paths
- Authority: which source outranks, or "neither — escalate"
- Status: Open | Resolved | Deferred
- Resolution owner: maintainer | next session | n/a
```

## Resolved

**Archive: `crystalcore/` vs `crystalcore-v0.13/` recovery framing** ·
Also flagged in [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) Tier 3 as
"Drift." · **Resolved 2026-08-28, maintainer decision.**
- **What each file claims:** `archive/2026/local-snapshot-2026-07-17/README-SNAPSHOT.md`
  calls the sibling `crystalcore/` folder (32 exports, no `status.py`, no
  SpaceXAI provider) a "complete, working package." `crystalcore-v0.13/RECOVERY-STATUS.md`
  calls *its own* folder (44 exports, includes `status.py` and
  `spacexai.py`) "COMPLETE and verified," and states explicitly that it
  **supersedes** the sibling `crystalcore/` folder ("nothing here is
  missing anymore").
- **On closer read, this was less a factual contradiction than an framing
  tension:** both folders are internally consistent about their own scope,
  and the later file already asserts a supersession relationship.
- **Authority:** neither file outranks the other; both are archive
  provenance, not current canon. Do not build on either.
- **Resolution:** Crystal reviewed this entry and the repository's
  existing archive/history organization (`archive/README`,
  [`CANON-MAP.md`](../CANON-MAP.md) "Legacy / migration status") and
  decided: accepted as currently organized. No repo-wide archive rewrite.
  Preserve minor wording inconsistencies in historical material as
  historical context unless they create an actual operational ambiguity —
  this one doesn't. Do not modify archive files merely for stylistic
  consistency.
- **Resolution owner:** maintainer (decision recorded).

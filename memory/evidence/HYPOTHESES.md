# HYPOTHESES — plausible, not verified

**Status:** Docs / governance. A hypothesis is a claim about something that
**exists on disk** as designed-not-built or in-progress, where the open
question is whether it will work, scale, or land as planned. Never treat
a hypothesis as a fact. Never let a model agreeing with you substitute for
evidence (Incognita Rule §4).

**Correction (2026-08-28):** an earlier version of this file cited
`docs/architecture/crystal-core/ (DUR specification)` as the source for a
"DUR token architecture" hypothesis. That citation was checked and is
**false** — no DUR specification exists anywhere in `docs/` (verified by
search). That entry has been removed rather than corrected, because there
is no on-disk claim left to hedge. See the Protected section below for why
DUR isn't reintroduced here.

## Protected / out of scope — not the same thing as a hypothesis

Per [`../PRIVACY.md`](../PRIVACY.md), the maintainer has instructed that
SAT-related internals, Operator Frame internals, DUR/token mechanics, and
private lattice fields stay protected **if encountered**. None of these
have a specification in this repository as of 2026-08-28. That absence
does not make them "unverified hypotheses" to speculate about here —
**protected/out of scope is a different status than hypothesis**, and
misfiling one as the other is exactly the kind of memory contamination
this file exists to avoid. If a session ever encounters real material in
these categories, it goes to `PRIVACY.md`'s "never write" list, not to a
hypothesis entry.

## Real hypotheses, grounded in Roadmap / OPEN-QUESTIONS

Format: `Hypothesis · Status on disk · Would be verified by · Source`

- **Lattice-delta / Weave-Map / gate machinery will eventually be built as
  designed** · Designed, never built (Constitution implementation note) ·
  A real implementation landing and a session exercising it ·
  [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) "Designed, not built"
- **Production Story Library components (SvelteKit/React) will match the
  HTML prototype's design intent** · Prototype built, production not
  started · Production components landing in `-Code` and a side-by-side
  comparison · [`../../docs/governance/Roadmap.md`](../../docs/governance/Roadmap.md)
  "Recently landed" 2026-07-23
- **mythos/tools prompt kits (daily-digest, signal-scanner) will integrate
  cleanly once wired to an execution layer** · Written, wired to nothing ·
  A real integration attempt · [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md)
- **dbt emotion warehouse pipeline is fit for live data once a warehouse
  is configured** · Full project structure exists, never executed, and
  `OPEN-DECISIONS.md` records staging models with hardcoded null CTEs and
  a SQL syntax error in `stg_emotion_labels.sql` (as of 2026-07-24) — so
  the more immediate open item is fixing those, not scale · Configuring a
  warehouse and running the pipeline once the known SQL issue is resolved
  · [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md) "Held open"

## What this file is not

Not a place to record vision-layer imagery as if it were a testable claim
— the mythos may orient, it may not authorize (Incognita Rule). Not a
place to speculate about material this repository has no evidence for at
all (see Protected section above).

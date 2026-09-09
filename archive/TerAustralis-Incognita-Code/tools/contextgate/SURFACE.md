# ContextGate — SURFACE (v0.1.0)

Status: implemented as the three rules below, in `gate.py`, covered by
`tests/test_gate.py` (5/5, run it yourself — see README.md). This
document is this session's proposed contract for what v0.1.0 checks and
does not check. Per this repo's own governance
([`ADR-0014`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/docs/adr/ADR-0014.md)
and `CLAUDE.md` in `TerAustralis-Incognita`), a session does not get to
declare its own draft locked — that happens, if it happens, when
Crystal merges the PR this ships in. Until then, treat everything below
as proposed, not settled.

## Why this exists

`memory/projects/90-Day-Roadmap/CURRENT.md` in `TerAustralis-Incognita`
records a real, already-caught failure: PR #146 fabricated an entire
Small Council outreach plan — an invented regulatory body, briefings to
real companies (Lynas Rare Earths, Magellan Aerospace, Equatorial
Launch Australia) positioning them as tiers/hubs/anchors with zero
citations, invented lodgement dates and cost figures, and closing lines
styled as quotes from named staff who never said them. A human caught
it on review. ContextGate exists so that specific, already-demonstrated
failure mode gets caught by a fixed check before a human has to
re-catch it by hand every time.

## The promise

Same input, same colour, every run. `gate.py` never calls a model,
never makes a judgment call, and never "looks fine" on vibes. It is
pattern matching against fixed rules — auditable, arguable, and
re-runnable by anyone with Python and no API key.

## Non-goals

- **Not a fact-checker.** ContextGate does not know whether a citation
  is real or whether a sourced claim is true. It only checks whether
  the *shape* of sourcing is present. A confidently fabricated citation
  passes exactly like a real one — this closes the "zero citations"
  failure mode from PR #146, not "convincing but false citation."
- **Not a review substitute.** GREEN means "passed three mechanical
  checks," not "cleared to send." Per the Incognita Rule, a model
  agreeing with a draft's shape is not evidence the draft is honest.
- **Not comprehensive.** v0.1.0 is a skeleton covering the three
  patterns PR #146 actually contained (see below). It does not check
  spelling, tone, formatting, whether a named organization actually
  exists, or warrant-labelling outside those three patterns. It will
  grow; it does not claim completeness now.
- **Not an LLM, and never becomes one.** If a future version needs
  semantic judgment instead of pattern matching, that is a different
  tool, not ContextGate v-next. Determinism is the point.

## The first three rules (v0.1.0)

Each rule fires per physical line and requires a *source marker*
(case-insensitive) somewhere on that same line: a URL, `Source:`,
`per `, `confirmed`, `verified`, `citing`, `according to`, a footnote
(`[1]`, `[^1]`), or one of `email` / `interview` / `transcript`. This
is a deliberately loose bar — see the fact-checker non-goal above — and
lines under a warrant label (`[Fact]` / `[Inference]` / `[Assumption]`
/ `[Vision]`, per
[`pathway-log-framework.md`](https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main/mythos/teraustralis/publish/pathway-log-framework.md)
in `TerAustralis-Incognita`) also satisfy Rule 3.

1. **Positioning claims need a source.** A line assigning a role to a
   named entity — `"<Name> as <Hub|Anchor|Foundation|Endpoint|Tier N>"`
   — with no source marker on the line is RED. This is the exact
   "position Magellan as Tier 3," "position ELA as Tier 4" shape from
   the fabricated briefings.
2. **Attributed quotes need a source.** A styled quotation followed by
   a dash, parenthetical, or "said"-style attribution to a named
   entity, with no source marker on the line, is RED. This is the
   "closing lines styled as attributed company quotes" pattern.
3. **Hard figures need a warrant label or a source.** A line stating a
   dollar amount or a percentage, with neither a source marker nor a
   `[Fact]`/`[Inference]`/`[Assumption]`/`[Vision]` label on the line,
   is RED. This is the "invented lodgement dates, staff-hour estimates,
   a cost-coverage promise" pattern (dates themselves are not yet
   checked — a gap, not a claim of coverage).

Any line is GREEN by default; a file is GREEN only if every checkable
line clears all three rules. Blank lines, markdown headers (`#...`),
and obvious template placeholders (`[Name/role/context]` — distinguished
from a warrant label by containing `/`, `...`, or `" or "` inside the
brackets) are not checked.

## Human override

The gate is code; the maintainer keeps the veto (Incognita Rule §3: "no
line mints its own authority"). A line anywhere in the input —

```
[HUMAN-OVERRIDE: GREEN — Crystal reviewed and approved manually]
```

— forces the final verdict to the stated colour. It never happens
silently: the rule-engine's own verdict and every finding it produced
are still printed, and the override line and its stated reason are
printed alongside the forced verdict, so an override is always visible
in the record, never a quiet suppression.

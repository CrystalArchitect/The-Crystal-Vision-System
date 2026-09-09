# VERIFIED — claims with a checkable evidence trail

**Status:** Docs / governance. This file exists for a narrower purpose than
[`../MILESTONES.md`](../MILESTONES.md) or [`../state/CURRENT.md`](../state/CURRENT.md):
those two track the *working picture* and *dated landings*; this one
tracks the **evidence chain** behind a claim — what was actually run or
measured, not just asserted. Where the claim is already dated and sourced
in those two files, this file points rather than repeats.

**Format:** `Claim · Evidence · Verified date · Reference`

## Executable, verified by running it

- CrystalCore.OS mythos terminal boots from a fresh clone and runs to the
  open First Gate, stdlib-only · Verified 2026-07-27 by execution
  (`python3 mythos/crystalcore-os/crystalcore_os.py`) · [`../../STATUS.md`](../../STATUS.md),
  [`../MILESTONES.md`](../MILESTONES.md)
- Story Library prototype is self-contained HTML/CSS/JS, no build step ·
  Verified 2026-07-24 by rendering in a headless browser ·
  [`../../STATUS.md`](../../STATUS.md)
- `crystalcore-v0.13/` package (archive) imports and all 44 `__all__`
  exports resolve under Python 3.12; the two entry points import against
  it and the Flask app builds 15 routes · Verified 2026-07-17, recorded in
  the snapshot itself · [`../../archive/2026/local-snapshot-2026-07-17/crystalcore-v0.13/RECOVERY-STATUS.md`](../../archive/2026/local-snapshot-2026-07-17/crystalcore-v0.13/RECOVERY-STATUS.md)
  — archive provenance only, do not build on it.

## Measured, verified by probing it

- `www.teraustralis.com.au` serves a SvelteKit build (last-modified
  2026-08-18), and the bare apex 301-redirects to it rather than 404ing ·
  Verified 2026-08-20 at three separate probe times · [`../OPEN-QUESTIONS.md`](../OPEN-QUESTIONS.md)
  "STATUS known unknowns"
- GitHub search `user:CrystalArchitect` returned 19 repositories (6 public
  living, 7 private living, 6 archived) · Measured 2026-08-20 ·
  [`../../docs/adr/ADR-0015.md`](../../docs/adr/ADR-0015.md)

## Governance, verified by the merge itself

- An ADR is Accepted only once its carrying PR merges — this is itself
  verifiable by checking the status column in
  [`../../docs/adr/README.md`](../../docs/adr/README.md) against each
  ADR's own header. Two ADRs are currently **Proposed**, not Accepted:
  `ADR-0012`, `ADR-0016`. See [`../DECISIONS.md`](../DECISIONS.md).

## What this file is not

Not a second copy of `STATUS.md`, `CHANGELOG.md`, or `Roadmap.md`
"Recently landed" — those remain canonical for the full list. This file
holds only claims worth flagging because *how* they were verified matters
(ran it / measured it / checked the merge), which is the detail a plain
status line usually drops.

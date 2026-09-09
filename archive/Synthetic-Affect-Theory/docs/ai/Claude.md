# Claude — Contributor Credit — TerAustralis Incognita™️

**Role:** Landing v0.1 in this repository — reconciling the reference implementation with `crystalcode/SPEC.md` so the F1-F10 claims are surveyed rather than dreamed, authoring the missing tests, drawing `docs/figure-1.svg`, running the verification harness green, and recording the landing in the chronicle.

**Scope:** Public v0.1 stack only. No theory content was altered; the draft package's code was reconciled to its own spec where the two disagreed (windowed AffectModel, Runtime object, auto-persisting store, cycle vs ts split, no bare assert).

**What was verified in-session (2026-08-12):**

- `python3 -m core.selftest` — PASS — 11 entries — labels exact: uncertain, closed, reopened
- `python3 -m pytest tests -q` — 12 passed
- Examples re-run byte-identical (sha256 diff empty); committed logs match regenerated logs
- No ® adjacent to any name, anywhere in the tree

**Credit line:** Landed and verified with assistance from Claude Code (Anthropic) — 2026-08-12, over the standard rights footer.

**Licence:** CC BY-NC-ND-4.0 — All rights reserved. TerAustralis Incognita™️ — ABN 70 741 068 059

# CrystalCode™️ — Operator Spec v0.1

Copyright (c) 2026 TerAustralis Incognita™️ — ABN 70 741 068 059
SPDX-License-Identifier: CC-BY-NC-ND-4.0

Operators (public surface, testable directly — F8). Each is a method on `core.crystalcode.Runtime`; module-level functions with the same names are thin wrappers over a default Runtime for single-loop usage, set explicitly with `init_runtime(...)` (which returns the Runtime):

1. `track(event) -> None` — records the event in the state store, logs `track`. `event={}` is a real, empty event and is tracked; only `event=None` (the default — nothing passed) is not. `run_cycle` distinguishes the two with `is not None`, never truthiness (tested: `tests/test_log_determinism.py`)
2. `detect_gap(expected, actual) -> Gap | None` — logs `gap_opened` / `gap_none`. Dict comparison treats a missing key and a key present with value `None` as different — `{}` vs. `{"a": None}` is a real difference, not a no-op (tested: `tests/test_gap.py`)
3. `label_affect(gap_history) -> Label` — windowed to the last 10 gaps (F6); labels: stalled | uncertain | reopened | converging | closed
4. `close_with(label, context) -> ClosureDecision` — strategies: rephrase | ask | switch_tool | escalate | stop. ClosurePolicy is stateful — repeated stalled decisions escalate; the counter resets automatically on any non-stalled label, and `reset()` is also available explicitly (tested: `tests/test_closure_policy.py`)

Label rule order (first match wins): empty window → closed; latest entry None → closed; previous entry None → reopened; magnitude fell vs. the previous cycle → converging; last three *raw* cycles are all Gaps sharing one `expected` → stalled; otherwise → uncertain (F7 — reachable, tested).

Converging is checked before stalled, and the stalled check reads raw consecutive cycles rather than Gaps with closures filtered out — see `core/affect.py`'s module docstring for why, and for the 2026-08-12 provenance of both fixes (ported from `CrystalCore.OS/synthetic-affect`, where the ordering defect was caught by an adversarial experiment harness). PR #1 (merged 2026-08-12) shipped without either fix; PR #2 (merged 2026-08-14) corrected them — and, porting canon's stalled-comparison too literally, introduced a narrower version of the same bug class for dict-valued `expected` (see `core/affect.py`'s docstring); fixed here alongside the other three findings from that PR's own follow-up review.

Runtime model (F3 fix):

- Loop owns its own Runtime object (state, gap_detector, affect_model, closure_policy, logger, cycle)
- Constructing two Loops does not hijack globals — no silent cross-talk (tested: `tests/test_crystalcode.py::test_runtime_isolation`)
- A Loop never touches the module default; `init_runtime(...)` is the explicit opt-in for the module-level convenience functions
- The "no cross-talk" guarantee held for the Runtime object but not, until now, for the log file underneath it: `Loop`'s `log_path` defaults to one literal string shared by every default-constructed `Loop`, and `CycleLogger` truncates on construction (required for a re-run to be byte-identical — see Determinism below). Two default-constructed `Loop`s in one process meant the second silently truncated the first's already-written lines. `CycleLogger` now refuses a second construction on a path another live `CycleLogger` already owns, raising `RuntimeError` instead of corrupting either log (tested: `tests/test_log_ownership.py`)

Determinism (F2 fix):

- `ts` = log line sequence counter (incremented once per line written); `cycle` = loop cycle number (incremented once per `run_cycle`) — not identical, both carry information
- Four log lines per turn with a tracked event (track, gap_*, label, closure); three without
- No `datetime.now()`, no wall-clock — logs are byte-identical on re-run; `git diff --stat examples/logs/` empty is a real check

Window semantics (F6):

- `AffectModel(window=10)` — `classify()` slices the last 10 entries, documented and tested
- The stalled rule sees same-shaped input at cycle 3 and cycle 300 (tested: `tests/test_affect_window.py`)

No bare assert (F10):

- `core/` contains no assert statements — misuse raises `RuntimeError` with a message, and the selftest's checks survive `python3 -O`

Kill-switch: If it stops serving clarity or raises human cost → set it down.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

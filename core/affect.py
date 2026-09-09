# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
AffectModel — classifier over gap history:
stalled | uncertain | reopened | converging | closed

Windowed (F6): classify() sees only the last `window` entries (default 10),
so the stalled rule sees the same-shaped input at cycle 3 and cycle 300.

Rule order, first match wins:
  1. empty window                       -> closed
  2. latest entry is None               -> closed    (closing is closing)
  3. previous entry is None             -> reopened  (gap after a closure)
  4. magnitude fell vs. previous cycle  -> converging
  5. last three RAW cycles are all Gaps
     sharing one `expected`             -> stalled
  6. otherwise                          -> uncertain

Converging is checked before stalled, deliberately: a same-goal run whose
magnitude is falling is progress, and labelling it stalled would route the
policy away from a strategy that is working. An earlier ordering in this
exact file did exactly that — checked stalled first — and shipped that way
in Synthetic-Affect-Theory- PR #1 (merged 2026-08-12) before being caught
and ported from the already-adversarially-verified fix in
CrystalCore.OS/synthetic-affect (core/affect.py, CHRONICLE.md 2026-08-12).

The stalled check also reads the *raw* trailing three cycles, not the last
three Gaps with any closures filtered out — three same-goal Gaps either side
of an intervening closure are not one continuous stall; the closure already
earned its own `reopened` label at the cycle it happened. A version of this
file that filtered closures out before counting would call that combination
`stalled` regardless of the gap in between; ported from canon for the same
reason as the ordering fix above. See test_affect_window.py.

Same-`expected` comparison is pairwise `==`, not `repr()`-set-distinctness.
The first port of this fix copied canon's `len({repr(g.expected) for g in
tail}) == 1` verbatim — but repr() is not order-independent for dicts, so
three genuinely-`==`-equal dict-valued `expected`s built with different key
insertion order (e.g. from separate JSON round-trips) read as three
*different* goals and the run silently stops being recognised as stalled:
the exact bug class this whole ordering fix exists to close, reopened by
the fix itself. `==` chains correctly regardless of key order and needs no
hashability; canon has the same latent bug, unexercised there only because
no test in either repository used a dict `expected` with reordered keys
until this one did.

Australian spelling: labelled, behaviour.
"""
from __future__ import annotations

from typing import List, Optional

from .gap import Gap

Label = str  # stalled | uncertain | reopened | converging | closed

LABELS = ("stalled", "uncertain", "reopened", "converging", "closed")

#: How many consecutive raw cycles against the same expectation count as stalled.
STALL_RUN = 3


class AffectModel:
    def __init__(self, window: int = 10):
        if window < 1:
            raise ValueError(f"window must be >= 1, got {window}")
        self.window = window

    def classify(self, gap_history: List[Optional[Gap]]) -> Label:
        recent = gap_history[-self.window:]
        if not recent:
            return "closed"

        current = recent[-1]
        previous = recent[-2] if len(recent) > 1 else None

        # No gap right now -> closed, regardless of what came before.
        if current is None:
            return "closed"

        # A gap now, none last cycle: it reopened.
        if previous is None and len(recent) > 1:
            return "reopened"

        # Gap shrinking cycle on cycle: progress, keep going. Checked before
        # stalled — see the module docstring.
        if previous is not None and current.magnitude < previous.magnitude:
            return "converging"

        # STALL_RUN consecutive raw cycles, none of them a closure, all
        # against the same expectation: nothing is moving.
        tail = recent[-STALL_RUN:]
        if len(tail) == STALL_RUN and all(g is not None for g in tail):
            first_expected = tail[0].expected
            if all(g.expected == first_expected for g in tail[1:]):
                return "stalled"

        return "uncertain"

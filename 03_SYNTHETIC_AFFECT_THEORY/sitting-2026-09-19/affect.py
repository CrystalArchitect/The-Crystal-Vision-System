# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
AffectModel — classifier over gap history: stalled | uncertain | reopened | converging | closed
Australian spelling retained
"""
from __future__ import annotations
from typing import List, Optional
from .gap import Gap

Label = str  # stalled | uncertain | reopened | converging | closed

class AffectModel:
    def __init__(self):
        pass

    def classify(self, gap_history: List[Optional[Gap]]) -> Label:
        if not gap_history:
            return "closed"

        # If last entry is None -> gap closed
        if gap_history[-1] is None:
            # Check if this is a true closure (no prior gaps or previous was also None)
            # Otherwise still closed — closing is closing
            return "closed"

        # Last is a Gap
        gaps = [g for g in gap_history if g is not None]

        if not gaps:
            return "closed"

        # Reopened: last gap exists after a closed gap (None) in recent history
        if len(gap_history) >= 2 and gap_history[-2] is None:
            return "reopened"

        # Stalled: same expected repeated >=3 times with similar magnitude
        if len(gaps) >= 3:
            last_three = gaps[-3:]
            if last_three[0].expected == last_three[1].expected == last_three[2].expected:
                return "stalled"

        # Converging: magnitude decreasing
        if len(gaps) >= 2:
            if gaps[-1].magnitude < gaps[-2].magnitude:
                return "converging"
            if gaps[-1].magnitude > gaps[-2].magnitude:
                return "uncertain"

        # Default
        return "uncertain"

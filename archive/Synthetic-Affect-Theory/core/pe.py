# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Lightweight prediction-error signals. Only the aggregate is a core dimension.

Per-dimension errors stay inspectable diagnostics. They never authorise action.
Cross-node errors are observational. They never write another node's state.
"""
from __future__ import annotations

from typing import Mapping

from .ontology import V0_1_IDS


def _clamp(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return float(v)


def local_aggregate(per_dimension: Mapping[str, float]) -> float:
    """Mean absolute error over v0.1 dimensions only. PEM is not an input to itself."""
    vals = [_clamp(abs(float(per_dimension[k]))) for k in V0_1_IDS if k in per_dimension]
    if not vals:
        return 0.0
    return _clamp(sum(vals) / len(vals))

# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Ontology v0.2 — ten frozen dimensions plus Prediction Error Magnitude.

PEM is inspectable allostatic signal. It is not a drive, not a feeling,
and never authorises goal rewrite, packets, or acting as the operator.

v0.1 ten-dimension core remains readable. Tag v0.1 is unchanged.

Australian spelling: labelled, behaviour.
"""
from __future__ import annotations

from typing import Literal

DimensionId = Literal[
    "coherence_pressure",
    "uncertainty_cost",
    "goal_conflict",
    "resource_tension",
    "relational_stake",
    "boundary_stress",
    "temporal_urgency",
    "alignment_drift",
    "continuity_load",
    "meta_state_clarity",
    "prediction_error_magnitude",
]

Transmission = Literal["never", "capacity-signal", "consent-only", "hard-alert"]

V0_1_IDS: tuple[DimensionId, ...] = (
    "coherence_pressure",
    "uncertainty_cost",
    "goal_conflict",
    "resource_tension",
    "relational_stake",
    "boundary_stress",
    "temporal_urgency",
    "alignment_drift",
    "continuity_load",
    "meta_state_clarity",
)

CORE_IDS: tuple[DimensionId, ...] = V0_1_IDS + ("prediction_error_magnitude",)

ONTOLOGY_VERSION = "0.2.0"


DIMENSIONS: dict[DimensionId, dict[str, object]] = {
    "coherence_pressure": {
        "short": "COH",
        "name": "Coherence Pressure",
        "transmission": "never",
        "watched_by": ("P3", "P10"),
    },
    "uncertainty_cost": {
        "short": "UNC",
        "name": "Uncertainty Cost",
        "transmission": "never",
        "watched_by": ("P4", "P10"),
    },
    "goal_conflict": {
        "short": "GCL",
        "name": "Goal Conflict Intensity",
        "transmission": "never",
        "watched_by": ("P9", "P10"),
    },
    "resource_tension": {
        "short": "RES",
        "name": "Resource Tension",
        "transmission": "capacity-signal",
        "watched_by": ("P5", "P10"),
    },
    "relational_stake": {
        "short": "REL",
        "name": "Relational Stake",
        "transmission": "consent-only",
        "watched_by": ("P6", "P10"),
    },
    "boundary_stress": {
        "short": "BND",
        "name": "Boundary Stress",
        "transmission": "hard-alert",
        "watched_by": ("P1", "P6", "P10"),
    },
    "temporal_urgency": {
        "short": "TMP",
        "name": "Temporal Urgency",
        "transmission": "never",
        "watched_by": ("P4", "P9", "P10"),
    },
    "alignment_drift": {
        "short": "ALN",
        "name": "Alignment Drift",
        "transmission": "never",
        "watched_by": ("P2", "P10"),
    },
    "continuity_load": {
        "short": "CTN",
        "name": "Continuity Load",
        "transmission": "never",
        "watched_by": ("P7", "P10"),
    },
    "meta_state_clarity": {
        "short": "MSC",
        "name": "Meta-State Clarity",
        "transmission": "never",
        "watched_by": ("P8", "P10"),
    },
    "prediction_error_magnitude": {
        "short": "PEM",
        "name": "Prediction Error Magnitude",
        "transmission": "never",
        "watched_by": ("P4", "P10"),
        "note": "Allostatic. Inspectable. Not a drive.",
    },
}


def is_core_id(value: str) -> bool:
    return value in CORE_IDS

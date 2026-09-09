# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""LocalAffectState — v0.2 eleven dimensions, no hidden keys.

PEM is stored in values['prediction_error_magnitude'] and in inspect().
Per-dimension PE diagnostics are also in inspect() when present.
Foreign affect never writes this object.
"""
from __future__ import annotations

from typing import Mapping

from .ontology import CORE_IDS, ONTOLOGY_VERSION, DimensionId
from .pe import local_aggregate


def _clamp(v: float) -> float:
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return float(v)


class LocalAffectState:
    """Inspectable. Versioned. No private affective fields. PEM is not a drive."""

    def __init__(
        self,
        values: Mapping[str, float] | None = None,
        *,
        confidence: Mapping[str, float] | None = None,
        timestamp: int = 0,
    ) -> None:
        self.ontology_version = ONTOLOGY_VERSION
        self.timestamp = int(timestamp)
        self.values: dict[DimensionId, float] = {d: 0.0 for d in CORE_IDS}
        self.confidence: dict[DimensionId, float] = {d: 1.0 for d in CORE_IDS}
        self.last_policy_firings: list[str] = []
        self.pe_per_dimension: dict[str, float] = {}
        if values:
            for key, val in values.items():
                if key not in CORE_IDS:
                    raise ValueError(f"unknown dimension: {key}")
                self.values[key] = _clamp(float(val))  # type: ignore[index]
        if confidence:
            for key, val in confidence.items():
                if key not in CORE_IDS:
                    raise ValueError(f"unknown dimension: {key}")
                self.confidence[key] = _clamp(float(val))  # type: ignore[index]

    def set(self, dim: DimensionId, value: float, *, confidence: float | None = None) -> None:
        if dim not in CORE_IDS:
            raise ValueError(f"unknown dimension: {dim}")
        self.values[dim] = _clamp(value)
        if confidence is not None:
            self.confidence[dim] = _clamp(confidence)

    def get(self, dim: DimensionId) -> float:
        return self.values[dim]

    def ingest_local_pe(self, per_dimension: Mapping[str, float]) -> float:
        """Write inspectable diagnostics and promote aggregate to PEM. Not a drive."""
        self.pe_per_dimension = {k: _clamp(abs(float(v))) for k, v in per_dimension.items()}
        agg = local_aggregate(self.pe_per_dimension)
        self.values["prediction_error_magnitude"] = agg
        return agg

    def inspect(self) -> dict[str, object]:
        return {
            "ontology_version": self.ontology_version,
            "timestamp": self.timestamp,
            "values": dict(self.values),
            "confidence": dict(self.confidence),
            "last_policy_firings": list(self.last_policy_firings),
            "pe_per_dimension": dict(self.pe_per_dimension),
        }

    def hidden_keys(self) -> list[str]:
        allowed = {
            "ontology_version",
            "timestamp",
            "values",
            "confidence",
            "last_policy_firings",
            "pe_per_dimension",
        }
        return [k for k in vars(self) if k not in allowed]


def steady() -> LocalAffectState:
    values = {d: 0.15 for d in CORE_IDS}
    values["meta_state_clarity"] = 0.85
    values["prediction_error_magnitude"] = 0.05
    return LocalAffectState(values)

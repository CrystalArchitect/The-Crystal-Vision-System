# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
GapDetector — Gap = Expected − Actual, as typed gap records.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional

#: Sentinel distinguishing "key absent" from "key present with value None"
#: in the dict-magnitude comparison below. dict.get(k) alone returns None
#: for both, so {} and {"a": None} compared with plain .get(k) look equal
#: when they are not.
_MISSING = object()


@dataclass
class Gap:
    id: int
    expected: Any
    actual: Any
    magnitude: float
    kind: str  # e.g. "mismatch", "missing", "extra"

    def to_dict(self):
        return asdict(self)


class GapDetector:
    def __init__(self):
        self._counter = 0

    @staticmethod
    def _magnitude(expected: Any, actual: Any) -> float:
        if expected == actual:
            return 0.0
        if isinstance(expected, dict) and isinstance(actual, dict):
            # simple diff magnitude: share of keys whose values differ
            keys = set(expected.keys()) | set(actual.keys())
            diff = 0
            for k in keys:
                if expected.get(k, _MISSING) != actual.get(k, _MISSING):
                    diff += 1
            return float(diff) / max(1, len(keys))
        if isinstance(expected, str) and isinstance(actual, str):
            return 0.0 if expected == actual else 1.0
        # fallback: not equal => 1.0
        return 1.0

    def detect(self, expected: Any, actual: Any, kind: str = "mismatch") -> Optional[Gap]:
        mag = self._magnitude(expected, actual)
        if mag == 0.0:
            return None
        self._counter += 1
        return Gap(id=self._counter, expected=expected, actual=actual, magnitude=mag, kind=kind)

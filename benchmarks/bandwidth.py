"""Analytical byte-count model for the H2 measurement boundary.

Counts index, routing, KV, attention, and output traffic.
This is not a hardware PMU measurement.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from benchmarks.config import DTYPE_BYTES


KINDS = ("index", "routing", "kv", "attention", "output")


@dataclass
class Bandwidth:
    bytes: dict[str, int] = field(default_factory=lambda: {k: 0 for k in KINDS})

    def add(self, kind: str, n_elems: int, dtype_bytes: int = DTYPE_BYTES) -> None:
        if kind not in self.bytes:
            raise ValueError(f"unknown traffic kind: {kind}")
        if n_elems < 0:
            raise ValueError("n_elems must be >= 0")
        self.bytes[kind] += int(n_elems) * dtype_bytes

    @property
    def total(self) -> int:
        return int(sum(self.bytes.values()))

    def merge(self, other: "Bandwidth") -> None:
        for k in KINDS:
            self.bytes[k] += other.bytes[k]

    def as_dict(self) -> dict[str, int]:
        out = dict(self.bytes)
        out["total"] = self.total
        return out

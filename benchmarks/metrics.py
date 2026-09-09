"""Locked quality and fidelity metrics. No pass/fail against the 1M gate."""

from __future__ import annotations

import math
from typing import Iterable, Sequence


def wilson_lcb(successes: int, n: int, z: float = 1.96) -> float:
    if n <= 0:
        return 0.0
    p = successes / n
    z2 = z * z
    denom = 1.0 + z2 / n
    centre = p + z2 / (2.0 * n)
    spread = z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n)
    return max(0.0, (centre - spread) / denom)


def paired_ratio_lcb(
    candidate_correct: Sequence[int],
    reference_correct: Sequence[int],
    n_boot: int = 2000,
    seed: int = 0xC15A0003,
    alpha: float = 0.05,
) -> float:
    """Bootstrap LCB of (mean Qc) / (mean Qref) on paired items.

    Returns 0.0 if the reference mean is 0 on a resample (undefined ratio).
    """
    import numpy as np

    c = np.asarray(candidate_correct, dtype=np.float64)
    r = np.asarray(reference_correct, dtype=np.float64)
    if c.size == 0 or c.shape != r.shape:
        return 0.0
    rng = np.random.RandomState(seed)
    n = c.size
    ratios = np.empty(n_boot, dtype=np.float64)
    for i in range(n_boot):
        idx = rng.randint(0, n, size=n)
        rs = float(r[idx].mean())
        if rs <= 0.0:
            ratios[i] = 0.0
        else:
            ratios[i] = float(c[idx].mean()) / rs
    return float(np.quantile(ratios, alpha / 2.0))


def mean(xs: Iterable[float]) -> float:
    xs = list(xs)
    return float(sum(xs) / len(xs)) if xs else 0.0

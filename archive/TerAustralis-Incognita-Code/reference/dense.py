"""Dense query-to-context attention. Reference baseline."""

from __future__ import annotations

import numpy as np

from benchmarks.bandwidth import Bandwidth
from benchmarks.model import AttentionPrimitive, sdp_attention, split_heads


class DenseAttention(AttentionPrimitive):
    name = "reference_dense"

    def select_and_attend(
        self,
        q: np.ndarray,
        k: np.ndarray,
        v: np.ndarray,
        query_positions: np.ndarray,
        bw: Bandwidth,
        layer: int,
    ) -> np.ndarray:
        qh = split_heads(q)
        kh = split_heads(k)
        vh = split_heads(v)
        bw.add("kv", k.size + v.size)
        return sdp_attention(qh, kh, vh, bw)

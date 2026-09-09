"""Candidate A — hierarchical block-sparse attention (development sweep).

Independent of Candidate B. Does not import B or B's results.
"""

from __future__ import annotations

import numpy as np

from benchmarks.bandwidth import Bandwidth
from benchmarks.config import CANDIDATE_A_DEV
from benchmarks.model import AttentionPrimitive, sdp_attention, split_heads


def _block_max(token_scores: np.ndarray, block: int) -> np.ndarray:
    t = token_scores.shape[0]
    n_blocks = (t + block - 1) // block
    pad = n_blocks * block - t
    padded = np.pad(token_scores, (0, pad), constant_values=np.float32(-np.inf))
    return padded.reshape(n_blocks, block).max(axis=1)


class HierarchicalBlockSparse(AttentionPrimitive):
    name = "candidate_a_hbs"
    independent = True

    def __init__(self, cfg: dict | None = None):
        self.cfg = dict(CANDIDATE_A_DEV if cfg is None else cfg)

    def select_and_attend(
        self,
        q: np.ndarray,
        k: np.ndarray,
        v: np.ndarray,
        query_positions: np.ndarray,
        bw: Bandwidth,
        layer: int,
    ) -> np.ndarray:
        block = int(self.cfg["block_size"])
        local_w = int(self.cfg["local_window"])
        n_sel = int(self.cfg["cross_block_selections"])
        n_sum = int(self.cfg["global_summaries"])
        freq = str(self.cfg.get("selection_frequency", "every_layer"))
        t = k.shape[0]
        n_blocks = (t + block - 1) // block

        q_bar = q.mean(axis=0)
        token_scores = k @ q_bar
        bw.add("routing", token_scores.size)

        block_scores = _block_max(token_scores, block)
        bw.add("index", block_scores.size)
        bw.add("routing", block_scores.size)

        q_block = int(query_positions[-1]) // block
        local = {min(n_blocks - 1, max(0, q_block + off)) for off in range(-local_w, 1)}
        use_cross = True
        if freq == "alternating" and (layer % 2 == 1):
            use_cross = False
        selected = set(local)
        if use_cross:
            k_take = min(n_sel, n_blocks)
            top = np.argpartition(block_scores, -k_take)[-k_take:]
            selected |= {int(x) for x in top}
        selected = sorted(selected)
        bw.add("routing", len(selected))

        idx = []
        for b in selected:
            idx.extend(range(b * block, min(t, (b + 1) * block)))
        idx_a = np.asarray(idx, dtype=np.int32)
        ks = k[idx_a]
        vs = v[idx_a]

        # Coarse global summaries: n_sum mean-pooled KV per block, all blocks.
        part = max(1, block // max(1, n_sum))
        n_parts = (t + part - 1) // part
        pad_t = n_parts * part - t
        k_pad = np.pad(k, ((0, pad_t), (0, 0)))
        v_pad = np.pad(v, ((0, pad_t), (0, 0)))
        k_sum = k_pad.reshape(n_parts, part, k.shape[1]).mean(axis=1)
        v_sum = v_pad.reshape(n_parts, part, v.shape[1]).mean(axis=1)
        bw.add("index", k_sum.size + v_sum.size)
        ks = np.concatenate([ks, k_sum], axis=0)
        vs = np.concatenate([vs, v_sum], axis=0)
        bw.add("kv", ks.size + vs.size)
        return sdp_attention(split_heads(q), split_heads(ks), split_heads(vs), bw)

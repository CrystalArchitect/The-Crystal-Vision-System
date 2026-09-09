"""Candidate B — content-addressed hierarchical retrieval (development sweep).

Independent of Candidate A. Does not import A or A's results.
"""

from __future__ import annotations

import numpy as np

from benchmarks.bandwidth import Bandwidth
from benchmarks.config import CANDIDATE_B_DEV
from benchmarks.model import AttentionPrimitive, sdp_attention, split_heads


def _max_pool(scores: np.ndarray, group: int) -> np.ndarray:
    n = scores.shape[0]
    n_next = (n + group - 1) // group
    pad = n_next * group - n
    padded = np.pad(scores, (0, pad), constant_values=np.float32(-np.inf))
    return padded.reshape(n_next, group).max(axis=1)


def _expand(nodes: np.ndarray, child_count: int, group: int) -> np.ndarray:
    child = []
    for node in nodes:
        lo = int(node) * group
        hi = min(child_count, lo + group)
        child.extend(range(lo, hi))
    return np.asarray(child, dtype=np.int32)


def retrieve_leaves(
    leaf_scores: np.ndarray,
    group: int,
    n_ret: int,
    n_levels: int,
    n_stages: int,
) -> np.ndarray:
    pyramid = [leaf_scores]
    for _ in range(max(0, n_levels - 1)):
        pyramid.append(_max_pool(pyramid[-1], group))

    n_leaves = leaf_scores.shape[0]
    n_ret = min(n_ret, n_leaves)
    L = len(pyramid)
    stages = max(1, min(int(n_stages), L))

    if stages == 1:
        visit = [0]
    else:
        visit = [L - 1, 0]
        if stages > 2 and L > 2:
            mids = list(range(L - 2, 0, -1))
            visit = [L - 1] + mids[: stages - 2] + [0]
        # unique, coarse-to-fine
        seen = set()
        ordered = []
        for lvl in visit:
            if lvl not in seen:
                seen.add(lvl)
                ordered.append(lvl)
        visit = ordered

    active = np.arange(pyramid[visit[0]].shape[0], dtype=np.int32)
    current = visit[0]
    for lvl in visit:
        while current > lvl:
            active = _expand(active, pyramid[current - 1].shape[0], group)
            current -= 1
        sc = pyramid[lvl][active]
        take = min(n_ret if lvl == 0 else max(1, min(n_ret, active.size)), active.size)
        if lvl > 0:
            cover = group ** lvl
            take = min(max(take, min(active.size, max(1, (n_ret + cover - 1) // cover))), active.size)
        active = active[np.argpartition(sc, -take)[-take:]]
    while current > 0:
        active = _expand(active, pyramid[current - 1].shape[0], group)
        current -= 1
    if active.size > n_ret:
        sc = leaf_scores[active]
        active = active[np.argpartition(sc, -n_ret)[-n_ret:]]
    return np.sort(active.astype(np.int32))


class ContentAddressedRetrieval(AttentionPrimitive):
    name = "candidate_b_car"
    independent = True

    def __init__(self, cfg: dict | None = None):
        self.cfg = dict(CANDIDATE_B_DEV if cfg is None else cfg)

    def select_and_attend(
        self,
        q: np.ndarray,
        k: np.ndarray,
        v: np.ndarray,
        query_positions: np.ndarray,
        bw: Bandwidth,
        layer: int,
    ) -> np.ndarray:
        leaf = int(self.cfg["leaf_block"])
        group = int(self.cfg.get("group_size", 4))
        n_ret = int(self.cfg["retrieved_blocks"])
        n_levels = int(self.cfg["summary_levels"])
        n_stages = int(self.cfg["refinement_stages"])
        t = k.shape[0]
        n_leaves = (t + leaf - 1) // leaf

        q_bar = q.mean(axis=0)
        token_scores = k @ q_bar
        bw.add("routing", token_scores.size)

        pad = n_leaves * leaf - t
        padded = np.pad(token_scores, (0, pad), constant_values=np.float32(-np.inf))
        leaf_scores = padded.reshape(n_leaves, leaf).max(axis=1)
        bw.add("index", leaf_scores.size)

        top_l = retrieve_leaves(leaf_scores, group, n_ret, n_levels, n_stages)
        bw.add("routing", top_l.size)

        idx = []
        for b in top_l:
            idx.extend(range(int(b) * leaf, min(t, (int(b) + 1) * leaf)))
        idx_a = np.asarray(idx, dtype=np.int32)
        ks = k[idx_a]
        vs = v[idx_a]
        bw.add("kv", ks.size + vs.size)
        return sdp_attention(split_heads(q), split_heads(ks), split_heads(vs), bw)

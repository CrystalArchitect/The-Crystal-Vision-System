"""Frozen encoder + scaled-dot-product kernel.

Query-to-context attention is the long-range primitive under test.
Document tokens are not rewritten.

Retrieval Q/K live in the token-embedding space: K[t] = h[t-2] + h[t-1]
(local triple binding).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from benchmarks.bandwidth import Bandwidth
from benchmarks.config import ATTN_BETA, D_HEAD, D_MODEL, N_HEADS, N_LAYERS, WEIGHT_SEED
from datasets.generator.vocab import VOCAB_SIZE


def _orthonormalish(rng: np.random.RandomState, rows: int, cols: int) -> np.ndarray:
    w = rng.normal(0.0, 1.0, size=(rows, cols)).astype(np.float32)
    w /= np.sqrt(np.float32(cols))
    return w


@dataclass
class FrozenWeights:
    embed: np.ndarray
    wq: np.ndarray
    wk: np.ndarray
    wv: np.ndarray
    wo: np.ndarray
    wbind: np.ndarray


def load_frozen_weights() -> FrozenWeights:
    rng = np.random.RandomState(WEIGHT_SEED)
    embed = _orthonormalish(rng, VOCAB_SIZE, D_MODEL)
    return FrozenWeights(
        embed=embed,
        wq=np.stack([_orthonormalish(rng, D_MODEL, D_MODEL) for _ in range(N_LAYERS)]),
        wk=np.stack([_orthonormalish(rng, D_MODEL, D_MODEL) for _ in range(N_LAYERS)]),
        wv=np.stack([_orthonormalish(rng, D_MODEL, D_MODEL) for _ in range(N_LAYERS)]),
        wo=np.stack([np.eye(D_MODEL, dtype=np.float32) for _ in range(N_LAYERS)]),
        wbind=np.eye(D_MODEL, dtype=np.float32),
    )


def split_heads(x: np.ndarray) -> np.ndarray:
    t, d = x.shape
    y = x.reshape(t, N_HEADS, D_HEAD)
    return np.transpose(y, (1, 0, 2))


def merge_heads(x: np.ndarray) -> np.ndarray:
    x = np.transpose(x, (1, 0, 2))
    return np.ascontiguousarray(x.reshape(x.shape[0], D_MODEL))


def sdp_attention(q: np.ndarray, k: np.ndarray, v: np.ndarray, bw: Bandwidth) -> np.ndarray:
    scores = np.matmul(q, np.transpose(k, (0, 2, 1))) * np.float32(ATTN_BETA)
    bw.add("attention", scores.size)
    scores = scores - np.max(scores, axis=-1, keepdims=True)
    p = np.exp(scores)
    p = p / np.sum(p, axis=-1, keepdims=True)
    out = np.matmul(p, v)
    bw.add("attention", p.size + out.size)
    return out.astype(np.float32)


def encode_tokens(tokens: np.ndarray, weights: FrozenWeights, bw: Bandwidth) -> np.ndarray:
    h = weights.embed[tokens].astype(np.float32)
    bw.add("kv", h.size)
    return h


def bound_keys(h: np.ndarray, weights: FrozenWeights, wk: np.ndarray, bw: Bandwidth) -> np.ndarray:
    t, d = h.shape
    prev1 = np.concatenate([np.zeros((1, d), dtype=np.float32), h[:-1]], axis=0)
    prev2 = np.concatenate([np.zeros((2, d), dtype=np.float32), h[:-2]], axis=0)
    k = (prev1 + prev2) @ weights.wbind
    bw.add("kv", k.size)
    return k.astype(np.float32)


def values(h: np.ndarray, wv: np.ndarray, bw: Bandwidth) -> np.ndarray:
    v = h
    bw.add("kv", v.size)
    return v.astype(np.float32)


def queries_at(h: np.ndarray, idx: np.ndarray, wq: np.ndarray, bw: Bandwidth) -> np.ndarray:
    q = h[idx]
    bw.add("kv", q.size)
    return q.astype(np.float32)


class AttentionPrimitive:
    name = "base"

    def select_and_attend(
        self,
        q: np.ndarray,
        k: np.ndarray,
        v: np.ndarray,
        query_positions: np.ndarray,
        bw: Bandwidth,
        layer: int,
    ) -> np.ndarray:
        raise NotImplementedError

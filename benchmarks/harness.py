"""Run a frozen encoder through one attention primitive. Scoring only."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from benchmarks.bandwidth import Bandwidth
from benchmarks.config import N_LAYERS
from benchmarks.model import (
    AttentionPrimitive,
    FrozenWeights,
    bound_keys,
    encode_tokens,
    merge_heads,
    values,
)
from datasets.generator import vocab as V
from datasets.generator.corpus import Item


@dataclass
class ItemResult:
    item_id: str
    length: int
    question_class: str
    bucket: str
    pred_ids: tuple[int, ...]
    gold_ids: tuple[int, ...]
    correct: int
    bandwidth: dict[str, int]


def _decode_value(vec: np.ndarray, weights: FrozenWeights) -> int:
    table = weights.embed[V.VALUE0 : V.FILLER0]
    return int(V.VALUE0 + np.argmax(table @ vec))


def run_item(item: Item, primitive: AttentionPrimitive, weights: FrozenWeights) -> ItemResult:
    bw = Bandwidth()
    h = encode_tokens(item.tokens, weights, bw).copy()
    last_out = None

    for layer in range(N_LAYERS):
        k_full = bound_keys(h, weights, weights.wk[layer], bw)
        v_full = values(h, weights.wv[layer], bw)
        k = k_full[: item.doc_len]
        v = v_full[: item.doc_len]

        q_rows = []
        r_idx = []
        if item.question_class == "cross_context_composition":
            e_pos, a_pos, r_pos = item.slots[0]
            assert item.compose_attr_pos is not None
            if layer == 0:
                q_rows.append(h[e_pos] + h[a_pos])
            else:
                q_rows.append(h[r_pos] + h[item.compose_attr_pos])
            r_idx.append(r_pos)
        else:
            for e_pos, a_pos, r_pos in item.slots:
                q_rows.append(h[e_pos] + h[a_pos])
                r_idx.append(r_pos)

        q = np.stack(q_rows, axis=0).astype(np.float32)
        bw.add("kv", q.size)
        qpos = np.array([item.doc_len - 1], dtype=np.int32)
        o = primitive.select_and_attend(q, k, v, qpos, bw, layer)
        o = merge_heads(o)
        delta = (o @ weights.wo[layer]).astype(np.float32)
        bw.add("output", delta.size)
        last_out = delta
        h[np.asarray(r_idx, dtype=np.int32)] = last_out

    preds = tuple(_decode_value(last_out[i], weights) for i in range(last_out.shape[0]))
    gold = item.answer_ids
    correct = int(preds[: len(gold)] == gold)
    return ItemResult(
        item_id=item.item_id,
        length=item.length,
        question_class=item.question_class,
        bucket=item.bucket,
        pred_ids=preds,
        gold_ids=gold,
        correct=correct,
        bandwidth=bw.as_dict(),
    )

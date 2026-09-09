"""Procedural long-context retrieval items. Evidence locations stay in the item
record for scoring only — primitives never receive them.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from benchmarks.config import BUCKETS, QUESTION_CLASSES
from datasets.generator import vocab as V
from datasets.generator.seeds import item_seed


Q_LEN = 8


@dataclass(frozen=True)
class Item:
    item_id: str
    length: int
    doc_len: int
    question_class: str
    bucket: str
    tokens: np.ndarray
    answer_ids: tuple[int, ...]
    slots: tuple[tuple[int, int, int], ...]
    compose_attr_pos: int | None
    evidence_spans: tuple[tuple[int, int], ...]
    distractor_spans: tuple[tuple[int, int], ...]


def available_buckets(doc_len: int) -> list[tuple[str, int, int]]:
    out = []
    for name, lo, hi in BUCKETS:
        span_hi = min(hi, doc_len)
        if span_hi - lo >= 4:
            out.append((name, lo, span_hi))
    return out or [("local", 1, max(4, doc_len))]


def _place_span(
    rng: np.random.RandomState,
    doc_len: int,
    lo: int,
    hi: int,
    occupied: list[tuple[int, int]],
) -> int:
    d_lo = max(lo, 3)
    d_hi = min(hi, doc_len - 1)
    if d_hi <= d_lo:
        d_lo, d_hi = 3, max(4, doc_len - 1)
    for _ in range(64):
        dist = int(rng.randint(d_lo, d_hi))
        start = max(0, min(doc_len - dist, doc_len - 3))
        end = start + 3
        if all(end <= a or start >= b for a, b in occupied):
            return start
    return max(0, doc_len - max(d_lo, 3) - 3)


def generate_item(partition: str, length: int, index: int) -> Item:
    rng = np.random.RandomState(item_seed(partition, length, index) & 0x7FFFFFFF)
    qclass = QUESTION_CLASSES[index % len(QUESTION_CLASSES)]
    buckets = available_buckets(length - Q_LEN)
    b_name, b_lo, b_hi = buckets[(index // len(QUESTION_CLASSES)) % len(buckets)]

    doc_len = length - Q_LEN
    tokens = np.empty(length, dtype=np.int32)
    tokens[:doc_len] = V.FILLER0 + rng.randint(0, V.N_FILLER, size=doc_len)
    tokens[doc_len:] = V.PAD
    occupied: list[tuple[int, int]] = []

    def plant(e: int, a: int, v: int, lo: int, hi: int) -> tuple[int, int]:
        s = _place_span(rng, doc_len, lo, hi, occupied)
        tokens[s] = e
        tokens[s + 1] = a
        tokens[s + 2] = v
        occupied.append((s, s + 3))
        return (s, s + 3)

    evidence: list[tuple[int, int]] = []
    distractors: list[tuple[int, int]] = []
    compose_attr_pos: int | None = None

    e1 = V.entity_id(int(rng.randint(0, V.N_ENTITY)))
    a1 = V.attr_id(int(rng.randint(1, V.N_ATTR)))
    v1 = V.value_id(int(rng.randint(0, V.N_VALUE)))

    if qclass == "two_source":
        e2 = V.entity_id(int(rng.randint(0, V.N_ENTITY)))
        while e2 == e1:
            e2 = V.entity_id(int(rng.randint(0, V.N_ENTITY)))
        a2 = V.attr_id(int(rng.randint(1, V.N_ATTR)))
        v2 = V.value_id(int(rng.randint(0, V.N_VALUE)))
        evidence.append(plant(e1, a1, v1, b_lo, b_hi))
        other = buckets[(index + 1) % len(buckets)]
        evidence.append(plant(e2, a2, v2, other[1], other[2]))
        answers = (v1, v2)
        q0 = doc_len
        tokens[q0 : q0 + 7] = np.array(
            [V.QSTART, e1, a1, e2, a2, V.QEND, V.QEND2], dtype=np.int32
        )
        slots = ((q0 + 1, q0 + 2, q0 + 5), (q0 + 3, q0 + 4, q0 + 6))
    elif qclass == "cross_context_composition":
        e2 = V.entity_id(int(rng.randint(0, V.N_ENTITY)))
        while e2 == e1:
            e2 = V.entity_id(int(rng.randint(0, V.N_ENTITY)))
        evidence.append(plant(e1, V.REF_ATTR, e2, b_lo, b_hi))
        other = buckets[(index + 3) % len(buckets)]
        evidence.append(plant(e2, a1, v1, other[1], other[2]))
        answers = (v1,)
        q0 = doc_len
        tokens[q0 : q0 + 5] = np.array(
            [V.QSTART, e1, V.REF_ATTR, a1, V.QEND], dtype=np.int32
        )
        slots = ((q0 + 1, q0 + 2, q0 + 4),)
        compose_attr_pos = q0 + 3
    elif qclass == "distractor_discrimination":
        e_d = V.entity_id((e1 - V.ENTITY0 + 1) % V.N_ENTITY)
        v_d = V.value_id((v1 - V.VALUE0 + 17) % V.N_VALUE)
        evidence.append(plant(e1, a1, v1, b_lo, b_hi))
        dhi = min(doc_len - 1, max(b_hi, b_lo + 16))
        distractors.append(plant(e_d, a1, v_d, max(3, b_lo // 2 or 3), dhi))
        answers = (v1,)
        q0 = doc_len
        tokens[q0 : q0 + 4] = np.array([V.QSTART, e1, a1, V.QEND], dtype=np.int32)
        slots = ((q0 + 1, q0 + 2, q0 + 3),)
    else:
        if qclass == "position_balanced":
            stratum = index % 5
            width = max(8, doc_len // 5)
            lo = max(3, stratum * width)
            hi = min(doc_len - 1, (stratum + 1) * width)
            if hi - lo < 4:
                lo, hi = 3, doc_len - 1
            b_lo, b_hi = lo, hi
        evidence.append(plant(e1, a1, v1, b_lo, b_hi))
        start = evidence[0][0]
        dist = doc_len - start
        for name, lo, hi in BUCKETS:
            if lo <= dist < hi:
                b_name = name
                break
        answers = (v1,)
        q0 = doc_len
        tokens[q0 : q0 + 4] = np.array([V.QSTART, e1, a1, V.QEND], dtype=np.int32)
        slots = ((q0 + 1, q0 + 2, q0 + 3),)

    return Item(
        item_id=f"{partition}:{length}:{index}",
        length=length,
        doc_len=doc_len,
        question_class=qclass,
        bucket=b_name,
        tokens=tokens,
        answer_ids=answers,
        slots=slots,
        compose_attr_pos=compose_attr_pos,
        evidence_spans=tuple(evidence),
        distractor_spans=tuple(distractors),
    )

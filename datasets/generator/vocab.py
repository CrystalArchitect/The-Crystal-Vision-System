"""Closed synthetic vocabulary. No external knowledge."""

from __future__ import annotations

PAD = 0
QSTART = 1
QEND = 2
QEND2 = 3

N_SPECIAL = 8
N_ENTITY = 512
N_ATTR = 32
N_VALUE = 512
N_FILLER = 2048

ENTITY0 = N_SPECIAL
ATTR0 = ENTITY0 + N_ENTITY
VALUE0 = ATTR0 + N_ATTR
FILLER0 = VALUE0 + N_VALUE
VOCAB_SIZE = FILLER0 + N_FILLER

REF_ATTR = ATTR0  # composition bridge attribute


def entity_id(i: int) -> int:
    return ENTITY0 + (i % N_ENTITY)


def attr_id(i: int) -> int:
    return ATTR0 + (i % N_ATTR)


def value_id(i: int) -> int:
    return VALUE0 + (i % N_VALUE)


def is_value(tid: int) -> bool:
    return VALUE0 <= tid < FILLER0


def is_entity(tid: int) -> bool:
    return ENTITY0 <= tid < ATTR0

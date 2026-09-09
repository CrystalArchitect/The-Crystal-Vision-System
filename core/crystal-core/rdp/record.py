# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""RDP record — an append-only, hash-chained log of events.

Each event carries the hash of the one before it, so the log is tamper-evident:
change any past event's content and every hash from that point on stops
matching. There is no authority to trust here — the math is the authority.

The link rule is:

    EventHash = SHA256( canonical(Event \\ event_hash) || PrevHashBytes )

that is, the canonical JSON of the event with its own ``event_hash`` field
removed, encoded UTF-8, concatenated with the 32 raw bytes of the previous
event's hash, then SHA-256'd. The first event links to the *genesis* previous
hash: 32 zero bytes.

A "chain" here is just a list of plain dicts — no database, no files. Persist it
however you like (it is ordinary JSON once the hashes are hex strings); the
integrity lives in the hashes, not the storage.

    from rdp.record import new_chain, append, verify
    chain = new_chain()
    append(chain, {"kind": "grant", "subject": "did:crystal:a"})
    append(chain, {"kind": "revoke", "subject": "did:crystal:a"})
    ok, broken_at = verify(chain)   # (True, -1)
"""

from __future__ import annotations

import hashlib
from typing import Any

from .canonical import canonical_bytes

# The previous-hash of the very first event: 32 zero bytes.
GENESIS_PREV = b"\x00" * 32

# The key an event's own hash is stored under (and excluded from its own hash).
HASH_FIELD = "event_hash"


def compute_event_hash(event: dict[str, Any], prev_bytes: bytes) -> bytes:
    """Return the 32-byte hash linking *event* to *prev_bytes*.

    The event's own ``event_hash`` field, if present, is excluded before
    hashing — an event cannot commit to its own hash.
    """
    if len(prev_bytes) != 32:
        raise ValueError("prev_bytes must be exactly 32 bytes")
    body = {k: v for k, v in event.items() if k != HASH_FIELD}
    return hashlib.sha256(canonical_bytes(body) + prev_bytes).digest()


def new_chain() -> list[dict[str, Any]]:
    """An empty chain."""
    return []


def tip_bytes(chain: list[dict[str, Any]]) -> bytes:
    """The previous-hash the next appended event should link to."""
    if not chain:
        return GENESIS_PREV
    return bytes.fromhex(chain[-1][HASH_FIELD])


def append(chain: list[dict[str, Any]], event: dict[str, Any]) -> dict[str, Any]:
    """Append *event* to *chain*, stamping its ``event_hash``.

    The caller's dict is not mutated; a stamped copy is stored and returned.
    """
    digest = compute_event_hash(event, tip_bytes(chain))
    stamped = {k: v for k, v in event.items() if k != HASH_FIELD}
    stamped[HASH_FIELD] = digest.hex()
    chain.append(stamped)
    return stamped


def verify(chain: list[dict[str, Any]]) -> tuple[bool, int]:
    """Verify every link. Return ``(True, -1)`` if intact.

    On the first mismatch return ``(False, i)`` where *i* is the index of the
    earliest event whose stored hash does not match its recomputed value — the
    first place the record was disturbed.
    """
    prev = GENESIS_PREV
    for i, event in enumerate(chain):
        stored = event.get(HASH_FIELD)
        recomputed = compute_event_hash(event, prev)
        if stored != recomputed.hex():
            return (False, i)
        prev = recomputed
    return (True, -1)

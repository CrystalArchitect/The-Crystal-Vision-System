# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Memory fragments — the only thing that ever crosses a Starline connection.

A fragment is small and self-contained: one event, one reflection, one
emotional snapshot, one piece of mythos. Never a bulk memory dump — that
keeps every exchange reviewable by the human before it's approved, and
keeps a single compromised peer from harvesting an entire memory store.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field

from . import identity as identity_mod

KINDS = ("episodic", "semantic", "emotional", "mythic")


@dataclass
class MemoryFragment:
    kind: str  # one of KINDS
    content: str
    sender_fingerprint: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    ts: float = field(default_factory=time.time)
    signature: str = ""  # hex, filled by sign()

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"unknown fragment kind {self.kind!r}, must be one of {KINDS}")

    def _signable_bytes(self) -> bytes:
        # Everything except the signature itself, in a fixed field order —
        # never json.dumps(self.__dict__) directly, since key order and
        # float formatting aren't guaranteed stable across Python versions.
        payload = {
            "kind": self.kind,
            "content": self.content,
            "sender_fingerprint": self.sender_fingerprint,
            "id": self.id,
            "ts": self.ts,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

    def sign(self, identity: identity_mod.Identity) -> "MemoryFragment":
        if identity.fingerprint != self.sender_fingerprint:
            raise ValueError("can only sign a fragment attributed to your own identity")
        self.signature = identity.sign(self._signable_bytes()).hex()
        return self

    def verify(self, sender_sign_public_bytes: bytes) -> bool:
        if not self.signature:
            return False
        return identity_mod.verify(
            sender_sign_public_bytes, self._signable_bytes(), bytes.fromhex(self.signature)
        )

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "content": self.content,
            "sender_fingerprint": self.sender_fingerprint,
            "id": self.id, "ts": self.ts, "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "MemoryFragment":
        return cls(
            kind=d["kind"], content=d["content"],
            sender_fingerprint=d["sender_fingerprint"],
            id=d["id"], ts=d["ts"], signature=d.get("signature", ""),
        )

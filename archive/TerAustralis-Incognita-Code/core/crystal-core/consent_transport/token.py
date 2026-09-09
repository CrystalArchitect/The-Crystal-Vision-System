# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Consent Tokens — the atomic unit of permission.

A reference implementation of `CONSENT-TOKEN-SCHEMA.md` v0.1 from
CrystalCore.OS AERIS / VAULT 12, whose §8 marks the schema "ready for
reference implementation and test vectors". This is that.

What this adds over the boolean consent that came before it: a grant used
to be a per-peer yes with no end. `is_granted()` answered from the most
recent receipt and nothing else, so a yes said once stayed true forever
unless it was explicitly taken back. The schema calls that out as
non-negotiable in §6 — **every token has a hard `expires_at`** — and a
permission that never lapses is the opposite of a permission.

A token binds five things a boolean could not say:

    who        issuer and recipient, both named, so a token is useless
               to anyone else — §6 "no ambient authority"
    why        a mandatory human-readable purpose — §6 "purpose binding"
    what       scope: which fragment kinds, and how many bytes
    how long   a hard expiry — §6 "time binding", §6 "no silent renewal"
    how often  constraints: one-time use, maximum transfers

Verification order follows `NOISE-IK-CONSENT-VERIFICATION.md` §4 exactly:
structure, identity binding, time binding, signature, revocation, scope.
The order matters — cheap structural checks run before signature
verification, which matters on a Tier 0 node running on battery.

Everything here is stdlib plus the Ed25519 already used for fragments.
Verification needs only the issuer's public key and a local clock, per
§7: "Verification must be possible offline."
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field

from . import identity as identity_mod

SCHEMA_VERSION = "0.1"

# Kinds a scope may name. Mirrors fragment.KINDS; duplicated as a constant
# rather than imported so that a token can be verified without pulling in
# the fragment machinery — a Tier R node may only ever check tokens.
KINDS = ("episodic", "semantic", "emotional", "mythic")

# Default lifetime when a caller does not name one. Deliberately short:
# §6 says extension requires a new token, so the safe default is one that
# lapses soon rather than one that quietly outlives its reason.
DEFAULT_TTL_SECONDS = 24 * 60 * 60


class ConsentError(Exception):
    """A token was refused. The message says which check failed, because
    a human is going to read it and needs to know whether they should
    re-issue, widen scope, or refuse."""


@dataclass
class Scope:
    """What may move. An empty `kinds` means every kind — the schema
    allows a class-wide grant — but `max_bytes` of 0 means unlimited only
    because the schema's own example uses 0 as the unset value."""

    kinds: tuple[str, ...] = ()
    max_bytes: int = 0

    def __post_init__(self):
        bad = [k for k in self.kinds if k not in KINDS]
        if bad:
            raise ValueError(f"unknown fragment kind(s) in scope: {bad}")

    def admits(self, kind: str) -> bool:
        return not self.kinds or kind in self.kinds

    def to_dict(self) -> dict:
        return {"kinds": list(self.kinds), "max_bytes": self.max_bytes}

    @classmethod
    def from_dict(cls, d: dict) -> "Scope":
        return cls(kinds=tuple(d.get("kinds") or ()), max_bytes=int(d.get("max_bytes", 0)))


@dataclass
class Constraints:
    one_time_use: bool = False
    requires_ack: bool = True
    max_transfers: int = 0  # 0 = unlimited

    def to_dict(self) -> dict:
        return {
            "one_time_use": self.one_time_use,
            "requires_ack": self.requires_ack,
            "max_transfers": self.max_transfers,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Constraints":
        return cls(
            one_time_use=bool(d.get("one_time_use", False)),
            requires_ack=bool(d.get("requires_ack", True)),
            max_transfers=int(d.get("max_transfers", 0)),
        )


@dataclass
class ConsentToken:
    """One permission, between two named identities, for a bounded
    purpose and a bounded time."""

    issuer: str          # issuer's full Ed25519 public key, hex
    recipient: str       # recipient's full Ed25519 public key, hex
    purpose: str         # mandatory, human-readable — §6
    scope: Scope = field(default_factory=Scope)
    constraints: Constraints = field(default_factory=Constraints)
    issued_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    revocable: bool = True
    version: str = SCHEMA_VERSION
    token_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    signature: str = ""

    def __post_init__(self):
        if not self.purpose or not self.purpose.strip():
            raise ValueError("purpose is mandatory and must not be empty (schema §6)")
        if not self.expires_at:
            self.expires_at = self.issued_at + DEFAULT_TTL_SECONDS
        if self.expires_at <= self.issued_at:
            raise ValueError("expires_at must be after issued_at")

    # -- signing -----------------------------------------------------

    def _signable_bytes(self) -> bytes:
        """Everything except the signature, in a fixed field order.

        Never json.dumps(self.__dict__): key order and float formatting
        are not guaranteed stable, and a signature over an unstable
        serialization is a signature over nothing. Same discipline as
        MemoryFragment._signable_bytes.
        """
        payload = {
            "version": self.version,
            "token_id": self.token_id,
            "issuer": self.issuer,
            "recipient": self.recipient,
            "purpose": self.purpose,
            "scope": self.scope.to_dict(),
            "constraints": self.constraints.to_dict(),
            "issued_at": self.issued_at,
            "expires_at": self.expires_at,
            "revocable": self.revocable,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

    def sign(self, identity: identity_mod.Identity) -> "ConsentToken":
        if identity.sign_public_bytes.hex() != self.issuer:
            raise ValueError("only the named issuer may sign this token")
        self.signature = identity.sign(self._signable_bytes()).hex()
        return self

    # -- verification ------------------------------------------------

    def verify(
        self,
        recipient_fingerprint_hex: str,
        *,
        now: float | None = None,
        revoked_ids: set[str] | None = None,
        kind: str | None = None,
        used_transfers: int = 0,
        used_bytes: int = 0,
        want_bytes: int = 0,
    ) -> None:
        """Raise ConsentError unless this token authorises the action.

        Checks run in the order NOISE-IK-CONSENT-VERIFICATION.md §4 sets
        out, cheapest first — a Tier 0 node should reject a malformed or
        expired token without paying for a signature verification.
        """
        now = time.time() if now is None else now

        # 1. structural
        for name in ("token_id", "issuer", "recipient", "purpose", "signature"):
            if not getattr(self, name):
                raise ConsentError(f"malformed token: {name} is empty")

        # 2. identity binding. Required, not optional: a token that will
        # verify for anybody is not a token. This parameter used to
        # default to None and skip the check, which meant is_valid() with
        # no arguments returned True for a token issued to someone else.
        if self.recipient != recipient_fingerprint_hex:
            raise ConsentError("token was not issued to this peer")

        # 3. time binding
        if now < self.issued_at:
            raise ConsentError("token is not valid yet")
        if now >= self.expires_at:
            raise ConsentError("token has expired")

        # 4. signature
        try:
            issuer_key = bytes.fromhex(self.issuer)
            sig = bytes.fromhex(self.signature)
        except ValueError as exc:
            raise ConsentError("token issuer or signature is not valid hex") from exc
        if not identity_mod.verify(issuer_key, self._signable_bytes(), sig):
            raise ConsentError("token signature does not verify")

        # 5. revocation
        if revoked_ids and self.token_id in revoked_ids:
            raise ConsentError("token has been revoked")

        # 6. scope, and the limits that go with it. These were carried in
        # the signed payload from the start and enforced nowhere, which is
        # worse than omitting them: a reader sees one_time_use=True and
        # reasonably believes something honours it.
        if kind is not None and not self.scope.admits(kind):
            raise ConsentError(f"token scope does not admit {kind!r} fragments")

        limit = 1 if self.constraints.one_time_use else self.constraints.max_transfers
        if limit and used_transfers >= limit:
            raise ConsentError(
                f"token transfer limit reached ({used_transfers}/{limit})"
            )

        if self.scope.max_bytes:
            if used_bytes >= self.scope.max_bytes:
                raise ConsentError(
                    f"token byte budget spent ({used_bytes}/{self.scope.max_bytes})"
                )
            if want_bytes and used_bytes + want_bytes > self.scope.max_bytes:
                raise ConsentError(
                    f"transfer would exceed the token's byte budget "
                    f"({used_bytes}+{want_bytes} > {self.scope.max_bytes})"
                )

    def is_valid(self, recipient_fingerprint_hex: str, **kwargs) -> bool:
        """verify() as a predicate, for callers that only want yes or no.
        Prefer verify() where the reason matters — it usually does.

        The recipient is positional and required here for the same reason
        it is on verify(): there is no safe default for "who is this for".
        """
        try:
            self.verify(recipient_fingerprint_hex, **kwargs)
            return True
        except ConsentError:
            return False

    def seconds_remaining(self, now: float | None = None) -> float:
        return max(0.0, self.expires_at - (time.time() if now is None else now))

    # -- serialization -----------------------------------------------

    def to_dict(self) -> dict:
        d = json.loads(self._signable_bytes())
        d["signature"] = self.signature
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ConsentToken":
        try:
            return cls(
                version=d.get("version", SCHEMA_VERSION),
                token_id=d["token_id"],
                issuer=d["issuer"],
                recipient=d["recipient"],
                purpose=d["purpose"],
                scope=Scope.from_dict(d.get("scope") or {}),
                constraints=Constraints.from_dict(d.get("constraints") or {}),
                issued_at=float(d["issued_at"]),
                expires_at=float(d["expires_at"]),
                revocable=bool(d.get("revocable", True)),
                signature=d.get("signature", ""),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ConsentError(f"malformed token: {exc}") from exc


@dataclass
class Revocation:
    """A signed statement that a token is dead.

    Per schema §5 this carries the token id, when it died, and the
    issuer's signature — and nothing else. It is deliberately small
    enough to gossip over a constrained link, and it is the only object
    in this module designed to be forwarded to third parties.
    """

    token_id: str
    issuer: str
    revoked_at: float = field(default_factory=time.time)
    signature: str = ""

    def _signable_bytes(self) -> bytes:
        payload = {
            "token_id": self.token_id,
            "issuer": self.issuer,
            "revoked_at": self.revoked_at,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

    def sign(self, identity: identity_mod.Identity) -> "Revocation":
        if identity.sign_public_bytes.hex() != self.issuer:
            raise ValueError("only the issuing identity may revoke its own token")
        self.signature = identity.sign(self._signable_bytes()).hex()
        return self

    def verify(self) -> bool:
        """True only if this revocation really came from the issuer it
        names. A forged revocation is a denial-of-service against a peer's
        consent, so it is checked exactly as carefully as a grant."""
        if not self.signature:
            return False
        try:
            return identity_mod.verify(
                bytes.fromhex(self.issuer),
                self._signable_bytes(),
                bytes.fromhex(self.signature),
            )
        except ValueError:
            return False

    def to_dict(self) -> dict:
        d = json.loads(self._signable_bytes())
        d["signature"] = self.signature
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Revocation":
        try:
            return cls(
                token_id=d["token_id"],
                issuer=d["issuer"],
                revoked_at=float(d["revoked_at"]),
                signature=d.get("signature", ""),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ConsentError(f"malformed revocation: {exc}") from exc

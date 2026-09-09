# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Consent & revocation — nothing moves without this saying yes, first.

Every grant is a signed receipt held locally by the human's own agent —
not by a third party, not by the peer. Revocation is honest about its own
limits: it stops FUTURE requests from a peer immediately. It cannot delete
what a peer already legitimately received before revocation — that data
is now theirs, on their own sovereign device, and forcing its deletion
would violate the same sovereignty principle that protects you. Say this
plainly to the human rather than implying a stronger guarantee.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from . import identity as identity_mod
from .token import ConsentError, Constraints, ConsentToken, Revocation, Scope

DEFAULT_CONSENT_PATH = Path("starline_consent.json")
DEFAULT_TOKEN_PATH = Path("starline_tokens.json")


def _write_json_atomic(path: Path, obj: object) -> None:
    """Replace `path` only after the new bytes are complete.

    TokenStore and ConsentEngine used to `write_text` in place. A crash
    mid-write destroyed the previous consent document — the same defect
    `--mint-token` used to have on the guest gate (now
    `write_json_atomic` in `crystalcore.config`). Write beside it,
    fsync, then `os.replace`. New files are 0600.
    """
    path = Path(path)
    from host_trust.classify import require_steward_persist

    require_steward_persist("consent-save", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(obj, fh, indent=2)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, path)


@dataclass
class ConsentReceipt:
    peer_fingerprint: str
    granted: bool          # True = granted, False = revoked
    ts: float
    signature: str = ""    # signed by the local identity — proves *we* decided this

    def _signable_bytes(self) -> bytes:
        payload = {"peer_fingerprint": self.peer_fingerprint, "granted": self.granted, "ts": self.ts}
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()

    def sign(self, identity: identity_mod.Identity) -> "ConsentReceipt":
        self.signature = identity.sign(self._signable_bytes()).hex()
        return self


class ConsentEngine:
    """The human-facing gate. Nothing in transport.py or protocol.py may
    send a fragment to a peer without ConsentEngine.is_granted() being
    true for that peer at the moment of sending."""

    def __init__(self, identity: identity_mod.Identity, path: Path = DEFAULT_CONSENT_PATH):
        self.identity = identity
        self.path = path
        self.receipts: list[ConsentReceipt] = []
        if path.exists():
            raw = json.loads(path.read_text())
            self.receipts = [ConsentReceipt(**r) for r in raw]

    def save(self) -> None:
        _write_json_atomic(self.path, [asdict(r) for r in self.receipts])

    def grant(self, peer_fingerprint: str) -> ConsentReceipt:
        receipt = ConsentReceipt(peer_fingerprint, granted=True, ts=time.time()).sign(self.identity)
        self.receipts.append(receipt)
        self.save()
        return receipt

    def revoke(self, peer_fingerprint: str) -> ConsentReceipt:
        receipt = ConsentReceipt(peer_fingerprint, granted=False, ts=time.time()).sign(self.identity)
        self.receipts.append(receipt)
        self.save()
        return receipt

    def is_granted(self, peer_fingerprint: str) -> bool:
        """Most recent receipt for this peer wins. No receipt = no consent —
        the default is always closed, never open."""
        relevant = [r for r in self.receipts if r.peer_fingerprint == peer_fingerprint]
        if not relevant:
            return False
        return max(relevant, key=lambda r: r.ts).granted

    def history_for(self, peer_fingerprint: str) -> list[ConsentReceipt]:
        return [r for r in self.receipts if r.peer_fingerprint == peer_fingerprint]


class TokenStore:
    """Consent Tokens issued by this node, and revocations it has seen.

    The boolean ConsentEngine above answers "may this peer ask at all".
    This answers the narrower question the schema actually specifies:
    *may this peer have this kind of fragment, right now, under a token
    that has not expired and has not been revoked.*

    Both exist because they answer different questions and the boolean
    one is load-bearing: every existing caller, every stored receipt, and
    the whole revocation test suite depend on it. Tokens are additive.
    A peer must clear the gate **and** hold a valid token when one is
    required — never one instead of the other.
    """

    def __init__(self, identity: identity_mod.Identity, path: Path = DEFAULT_TOKEN_PATH):
        self.identity = identity
        self.path = path
        self.tokens: dict[str, ConsentToken] = {}
        self.revocations: dict[str, Revocation] = {}
        # What each token has actually spent. Limits that are not counted
        # are not limits, so this is persisted with the tokens themselves --
        # a one-time-use token that resets on restart is a token with no
        # constraint at all.
        self.usage: dict[str, dict[str, int]] = {}
        if path.exists():
            raw = json.loads(path.read_text())
            self.usage = {k: dict(v) for k, v in (raw.get("usage") or {}).items()}
            for d in raw.get("tokens", []):
                tok = ConsentToken.from_dict(d)
                self.tokens[tok.token_id] = tok
            for d in raw.get("revocations", []):
                rev = Revocation.from_dict(d)
                # Never load a revocation we cannot prove came from its
                # issuer -- a forged one is a denial of service against
                # our own consent.
                if rev.verify():
                    self.revocations[rev.token_id] = rev

    def save(self) -> None:
        _write_json_atomic(self.path, {
            "tokens": [t.to_dict() for t in self.tokens.values()],
            "revocations": [r.to_dict() for r in self.revocations.values()],
            "usage": self.usage,
        })

    @property
    def revoked_ids(self) -> set[str]:
        return set(self.revocations)

    def issue(
        self,
        recipient_sign_public_hex: str,
        purpose: str,
        *,
        kinds: tuple[str, ...] = (),
        max_bytes: int = 0,
        ttl_seconds: float | None = None,
        constraints_one_time: bool = False,
        max_transfers: int = 0,
    ) -> ConsentToken:
        """Mint and sign a token. `purpose` is mandatory by schema §6 --
        a permission whose reason nobody wrote down cannot be reviewed
        later, which is the whole point of writing it down."""
        issued = time.time()
        token = ConsentToken(
            issuer=self.identity.sign_public_bytes.hex(),
            recipient=recipient_sign_public_hex,
            purpose=purpose,
            scope=Scope(kinds=kinds, max_bytes=max_bytes),
            constraints=Constraints(
                one_time_use=constraints_one_time, max_transfers=max_transfers
            ),
            issued_at=issued,
            expires_at=issued + ttl_seconds if ttl_seconds else 0.0,
        ).sign(self.identity)
        self.tokens[token.token_id] = token
        self.save()
        return token

    def revoke(self, token_id: str) -> Revocation:
        """Kill a token. Takes effect here immediately; the signed object
        it returns is what a peer needs in order to honour it too."""
        token = self.tokens.get(token_id)
        if token is None:
            raise ConsentError(f"no such token: {token_id}")
        if not token.revocable:
            raise ConsentError("token was issued as irrevocable")
        rev = Revocation(
            token_id=token_id, issuer=self.identity.sign_public_bytes.hex()
        ).sign(self.identity)
        self.revocations[token_id] = rev
        self.save()
        return rev

    def accept_revocation(self, rev: Revocation) -> bool:
        """Honour a revocation gossiped by someone else.

        Returns whether it was accepted. Refused unless it verifies
        against the issuer it names -- schema §5 says any node receiving
        a *valid* revocation must treat the token as dead, and the word
        doing the work there is 'valid'.
        """
        if not rev.verify():
            return False
        known = self.tokens.get(rev.token_id)
        if known is not None and known.issuer != rev.issuer:
            return False  # signed by someone, but not by this token's issuer
        self.revocations[rev.token_id] = rev
        self.save()
        return True

    def spent(self, token_id: str) -> dict[str, int]:
        return self.usage.get(token_id, {"transfers": 0, "bytes": 0})

    def record_use(self, token_id: str, n_bytes: int = 0) -> None:
        """Count a transfer against its token. Must be called once data
        actually moves, or one_time_use and max_bytes mean nothing."""
        u = self.usage.setdefault(token_id, {"transfers": 0, "bytes": 0})
        u["transfers"] += 1
        u["bytes"] += int(n_bytes)
        self.save()

    def authorize(
        self,
        recipient_sign_public_hex: str,
        kind: str | None = None,
        want_bytes: int = 0,
    ) -> ConsentToken:
        """Return a live token authorising this peer for this kind, or
        raise ConsentError explaining why none does.

        Raising rather than returning None is deliberate: the caller is
        about to decide whether data moves, and "no, because the token
        expired forty minutes ago" is a different operational fact from
        "no, because you were never granted this kind."
        """
        reasons: list[str] = []
        best: ConsentToken | None = None
        for token in self.tokens.values():
            if token.recipient != recipient_sign_public_hex:
                continue
            spent = self.spent(token.token_id)
            try:
                token.verify(
                    recipient_sign_public_hex,
                    revoked_ids=self.revoked_ids,
                    kind=kind,
                    used_transfers=spent["transfers"],
                    used_bytes=spent["bytes"],
                    want_bytes=want_bytes,
                )
            except ConsentError as exc:
                reasons.append(str(exc))
                continue
            # Prefer the token that lasts longest, so a peer holding both
            # a narrow short token and a broad long one is not cut off
            # early by whichever happened to be stored first.
            if best is None or token.expires_at > best.expires_at:
                best = token
        if best is not None:
            return best
        if reasons:
            raise ConsentError("; ".join(sorted(set(reasons))))
        raise ConsentError("no consent token issued to this peer")

    def is_authorized(
        self,
        recipient_sign_public_hex: str,
        kind: str | None = None,
        want_bytes: int = 0,
    ) -> bool:
        try:
            self.authorize(recipient_sign_public_hex, kind, want_bytes)
            return True
        except ConsentError:
            return False

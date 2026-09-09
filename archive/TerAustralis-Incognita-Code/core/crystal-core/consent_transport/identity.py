# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Cryptographic identity — the only thing a Starline peer is.

No accounts, no usernames, no central registry. An identity is three keys:
  * Ed25519 + ML-DSA-65 for signing (proves "this fragment / consent
    receipt / token is mine"), used together, both required
  * X25519 for the Noise handshake (proves "this connection is with me")

The private keys never leave the device. Losing the key file means losing
the identity — there is no recovery, by design; a recoverable key would
mean someone else could hold your recovery.

Why two signing keys
--------------------
The hybrid handshake (noise.py) stops a recorded session being decrypted
once quantum hardware exists. It deliberately does not fix *authentication*
— and authentication is where the sharper attack lives, because a quantum
adversary does not need to record anything first.

Concretely, against Ed25519-only identity: Alice's fingerprint is public.
Mallory recovers Alice's Ed25519 private key from her public key, presents
Alice's real public key at pairing, and is stored as Alice. Every signature
Mallory then makes verifies. Adding ML-DSA signatures alone does *not* fix
this on its own: if the fingerprint still commits only to the Ed25519 key,
Mallory pairs with Alice's Ed25519 key and Mallory's own ML-DSA key, and
both signatures check out against what the victim stored.

So two things change together, and neither works without the other:

  * every signature is Ed25519 ++ ML-DSA-65, and verification requires
    **both** to pass — forging one is not enough;
  * the fingerprint commits to **both** public keys, so a substituted
    ML-DSA key cannot ride in behind a genuine Ed25519 one.

Hybrid, never replacement, for the same reason as the handshake: a flaw in
ML-DSA leaves Ed25519 holding, and a quantum computer leaves ML-DSA holding.

There is no classical-only mode here. The handshake keeps one because a
session is negotiated per connection and mismatches fail loudly; an identity
is persistent and its signatures are checked by other people, so a
classical-only path would just be a downgrade attack with extra steps.

**This changes fingerprints.** An identity that predates this cannot be
upgraded in place — the fingerprint is derived from both keys, so adding
one produces a different identity. `load()` says so explicitly rather than
silently minting a new fingerprint under an old file's name.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
)

try:
    from cryptography.hazmat.primitives.asymmetric.mldsa import (
        MLDSA65PrivateKey,
        MLDSA65PublicKey,
    )
    MLDSA_AVAILABLE = True
except ImportError:  # cryptography < 47 has no ML-DSA
    MLDSA65PrivateKey = MLDSA65PublicKey = None  # type: ignore[assignment]
    MLDSA_AVAILABLE = False

DEFAULT_IDENTITY_PATH = Path("starline_identity.json")

# All fixed-width, which is what lets a hybrid public key and a hybrid
# signature be one concatenated blob with an unambiguous split point.
ED25519_PUBLEN = 32
ED25519_SIGLEN = 64
MLDSA65_PUBLEN = 1952
MLDSA65_SIGLEN = 3309
HYBRID_PUBLEN = ED25519_PUBLEN + MLDSA65_PUBLEN   # 1984
HYBRID_SIGLEN = ED25519_SIGLEN + MLDSA65_SIGLEN   # 3373


def _require_mldsa() -> None:
    if not MLDSA_AVAILABLE:
        raise RuntimeError(
            "Starline identities are hybrid post-quantum and need ML-DSA, which "
            "arrived in cryptography 47. Upgrade: pip install -r "
            "requirements-consenttransport.txt"
        )


def fingerprint_for(sign_public_bytes: bytes) -> str:
    """The short display id, derived from the whole hybrid public key.

    One definition, used by both Identity and PeerStore — if these ever
    disagreed, a peer would be filed under an id its owner never uses.

    It hashes rather than truncating the key directly, so the id commits to
    the ML-DSA half as well: that is what stops a genuine Ed25519 key being
    paired with a substituted ML-DSA key. Still truncated to 64 bits, which
    is the length this project already used — this change closes the
    substitution gap, it does not claim to lengthen the id.
    """
    return hashlib.sha256(sign_public_bytes).hexdigest()[:16]


@dataclass
class Identity:
    """A local Starline identity: one signing keypair, one DH keypair."""

    signing_key: Ed25519PrivateKey
    dh_key: X25519PrivateKey
    mldsa_key: "MLDSA65PrivateKey"

    @classmethod
    def generate(cls) -> "Identity":
        _require_mldsa()
        return cls(
            Ed25519PrivateKey.generate(),
            X25519PrivateKey.generate(),
            MLDSA65PrivateKey.generate(),
        )

    @property
    def ed25519_public_bytes(self) -> bytes:
        return self.signing_key.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )

    @property
    def mldsa_public_bytes(self) -> bytes:
        return self.mldsa_key.public_key().public_bytes_raw()

    @property
    def sign_public_bytes(self) -> bytes:
        """The hybrid public key: Ed25519 ++ ML-DSA-65, 1984 bytes.

        Deliberately still called sign_public_bytes and still the single
        value every caller passes around, so an artifact that carries an
        issuer key (a consent token, a revocation) carries *both* halves
        without any call site having to learn about the second one.
        """
        return self.ed25519_public_bytes + self.mldsa_public_bytes

    @property
    def dh_public_bytes(self) -> bytes:
        return self.dh_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)

    @property
    def fingerprint(self) -> str:
        """Short, human-shareable identifier — not secret, just a label."""
        return fingerprint_for(self.sign_public_bytes)

    def sign(self, data: bytes) -> bytes:
        """Sign with both keys. Verification requires both, so an adversary
        who can forge one has still forged nothing."""
        return self.signing_key.sign(data) + self.mldsa_key.sign(data)

    def save(self, path: Path = DEFAULT_IDENTITY_PATH) -> None:
        """Write the private identity to disk, owner-read-only where the
        platform supports it. This file must never be committed to git —
        see .gitignore.

        Two properties this write has to hold, both of which a plain
        write_text() gives up:

        * The file is never, at any instant, readable by anyone else.
          Creating it and *then* chmod'ing leaves it world-readable under
          the usual 0022 umask for as long as the write takes, which is
          long enough for another local user to open it and keep the
          descriptor. So it is created with 0600 already set.
        * A failed write never destroys the existing identity. Losing
          this file means losing the identity outright — there is no
          recovery, by design — so the new copy is written beside the old
          one and moved into place only once it is complete on disk.
        """
        from host_trust.classify import require_steward_persist

        require_steward_persist("identity-mint", path)
        payload = {
            "signing_key": self.signing_key.private_bytes(
                Encoding.Raw, PrivateFormat.Raw, NoEncryption()
            ).hex(),
            "dh_key": self.dh_key.private_bytes(
                Encoding.Raw, PrivateFormat.Raw, NoEncryption()
            ).hex(),
            # private_bytes_raw() is the 32-byte FIPS 204 seed, and
            # from_seed_bytes() regenerates the identical keypair from it —
            # verified, not assumed: the restored key's public half matches
            # and its signatures verify under the original public key.
            "mldsa_key": self.mldsa_key.private_bytes_raw().hex(),
        }
        path = Path(path)
        tmp = path.with_name(path.name + ".tmp")
        mode = stat.S_IRUSR | stat.S_IWUSR
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
        try:
            with os.fdopen(fd, "w") as fh:
                json.dump(payload, fh)
                fh.flush()
                os.fsync(fh.fileno())
        except BaseException:
            tmp.unlink(missing_ok=True)
            raise
        # os.open honours `mode` only when it creates the file; an
        # existing .tmp from an interrupted save keeps its old bits.
        try:
            os.chmod(tmp, mode)
        except OSError:
            pass  # best-effort; not all platforms support POSIX perms
        os.replace(tmp, path)

    @classmethod
    def load(cls, path: Path = DEFAULT_IDENTITY_PATH) -> "Identity":
        _require_mldsa()
        payload = json.loads(path.read_text())
        from .foreign import refuse_as_starline_identity

        refuse_as_starline_identity(payload, source=str(path))
        if "mldsa_key" not in payload:
            # Refused, not silently upgraded. Generating the missing key here
            # would change this identity's fingerprint — every peer would
            # still hold the old one, every previously issued token would
            # name an issuer that no longer exists, and none of it would be
            # visible until an exchange failed for no stated reason.
            raise ValueError(
                f"{path} is a pre-quantum identity (no ML-DSA key). Adding one "
                "changes the fingerprint, so this is a new identity, not an "
                "upgrade: generate a fresh identity and re-pair with your peers. "
                "The old file is left untouched."
            )
        return cls(
            Ed25519PrivateKey.from_private_bytes(bytes.fromhex(payload["signing_key"])),
            X25519PrivateKey.from_private_bytes(bytes.fromhex(payload["dh_key"])),
            MLDSA65PrivateKey.from_seed_bytes(bytes.fromhex(payload["mldsa_key"])),
        )

    @classmethod
    def load_or_generate(cls, path: Path = DEFAULT_IDENTITY_PATH) -> "Identity":
        if path.exists():
            return cls.load(path)
        identity = cls.generate()
        identity.save(path)
        return identity


def verify(sign_public_bytes: bytes, data: bytes, signature: bytes) -> bool:
    """Verify a hybrid signature against a hybrid public key.

    **Both** halves must verify. Returns False on any failure rather than
    raising — callers should treat unverified exactly like actively-forged,
    never as a crash.

    The lengths are checked before anything is parsed. Without that, a
    short signature would slice into an empty ML-DSA half, and any
    verifier that treated "no bytes to check" as "nothing objected" would
    accept an Ed25519-only signature — which is precisely the downgrade
    this module exists to refuse. There is no partial credit here: one
    good half and one bad half is a forgery.
    """
    if len(sign_public_bytes) != HYBRID_PUBLEN or len(signature) != HYBRID_SIGLEN:
        return False
    if not MLDSA_AVAILABLE:
        return False
    ed_pub, mldsa_pub = sign_public_bytes[:ED25519_PUBLEN], sign_public_bytes[ED25519_PUBLEN:]
    ed_sig, mldsa_sig = signature[:ED25519_SIGLEN], signature[ED25519_SIGLEN:]
    try:
        Ed25519PublicKey.from_public_bytes(ed_pub).verify(ed_sig, data)
    except Exception:
        return False
    try:
        MLDSA65PublicKey.from_public_bytes(mldsa_pub).verify(mldsa_sig, data)
    except Exception:
        return False
    return True


def dh_public_from_bytes(raw: bytes) -> X25519PublicKey:
    return X25519PublicKey.from_public_bytes(raw)

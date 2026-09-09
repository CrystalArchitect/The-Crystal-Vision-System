# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Noise Protocol handshake — IK pattern, classical or hybrid post-quantum.

This is a direct, literal implementation of the published Noise Protocol
Framework spec (noiseprotocol.org/noise.html), narrowed to exactly the one
pattern Starline needs. It is deliberately NOT a general Noise library —
a smaller, single-purpose implementation is easier to audit than a general
one, and auditability matters more here than flexibility.

IK means: the initiator already knows the responder's static public key
before the handshake starts (that's the "manual key exchange" pairing step
in Starline — you already have your peer's key from pairing). Two messages
complete the handshake:

    -> e, es, s, ss      (initiator: ephemeral, DH, encrypted static, DH)
    <- e, ee, se         (responder: ephemeral, DH, DH)

After both messages, each side calls split() to get two independent
ChaCha20-Poly1305 cipher states — one for each direction — with forward
secrecy from the ephemeral keys and mutual authentication from the static
keys. No custom crypto primitives are used anywhere: X25519, ChaCha20-
Poly1305, SHA256/HMAC and ML-KEM all come from `cryptography` or the stdlib.

Hybrid post-quantum mode (default)
----------------------------------
X25519 falls to a sufficiently large quantum computer. Nobody has one, but
an adversary does not need one *today* to benefit from one later: they can
record a Starline session now and decrypt it whenever the hardware arrives.
Memory fragments are exactly the kind of payload that is still sensitive in
twenty years, so the default handshake adds a second, independent shared
secret from ML-KEM-768 (NIST FIPS 203) and mixes it into the same chaining
key:

    -> e, ekem, es, s, ss    (ekem: an ephemeral ML-KEM-768 public key)
    <- e, ee, se, kem        (kem: the encapsulation against it)

Hybrid, never replacement. The session key derives from *both* the X25519
DHs and the ML-KEM secret, so an attacker must break both. If ML-KEM turns
out to have a flaw nobody has found yet, X25519 still holds; if a quantum
computer arrives, ML-KEM still holds. That is the standard migration shape
(TLS 1.3 hybrid key exchange does the same thing) and it is the reason not
to simply swap the primitive out.

**What this does not buy, stated plainly.** Handshake authentication
is still classical X25519 for the Noise static keys. A future quantum
adversary could not decrypt a recorded hybrid session, but could
impersonate a peer in a *live* handshake if they recovered that static.
This closes harvest-now-decrypt-later on confidentiality. It does **not**
make the handshake identity post-quantum.

Signing identity is already hybrid: `identity.py` requires Ed25519 +
ML-DSA-65 for every signature (fragments, tokens, revocations), and the
fingerprint commits to both public keys. ML-KEM (this module) and ML-DSA
(`identity.py`) are separate legs — confidentiality vs authentication —
and neither replaces the other.

The protocol name differs between modes, and the name is mixed into the
handshake hash, so a hybrid peer and a classical peer fail loudly instead
of silently negotiating anything down. There is no downgrade path by
design — fail-safe is isolation, never fail-open.
"""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

try:
    from cryptography.hazmat.primitives.asymmetric.mlkem import (
        MLKEM768PrivateKey,
        MLKEM768PublicKey,
    )
    MLKEM_AVAILABLE = True
except ImportError:  # cryptography < 47 has no ML-KEM
    MLKEM768PrivateKey = MLKEM768PublicKey = None  # type: ignore[assignment]
    MLKEM_AVAILABLE = False

PROTOCOL_NAME = b"Noise_IK_25519_ChaChaPoly_SHA256"
# Distinct name, deliberately: it is mixed into the initial handshake hash,
# so a hybrid peer and a classical one diverge at the first message instead
# of appearing to agree.
PROTOCOL_NAME_HYBRID = b"Noise_IKhfs_25519+MLKEM768_ChaChaPoly_SHA256"
DHLEN = 32   # X25519 public key length
TAGLEN = 16  # ChaCha20-Poly1305 authentication tag length
HASHLEN = 32  # SHA256 output length
KEM_PUBLEN = 1184  # ML-KEM-768 encapsulation key
KEM_CTLEN = 1088   # ML-KEM-768 ciphertext


class HandshakeFailed(Exception):
    """The handshake could not be completed — bad key, tampering, or a
    peer that isn't who they claim to be. Never proceed past this."""


def _hmac_sha256(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).digest()


def _hkdf2(chaining_key: bytes, input_key_material: bytes) -> tuple[bytes, bytes]:
    """Noise's exact two-output HKDF (spec section 4.3) — not RFC 5869's
    API, the narrower construction the Noise spec itself defines."""
    temp_key = _hmac_sha256(chaining_key, input_key_material)
    output1 = _hmac_sha256(temp_key, b"\x01")
    output2 = _hmac_sha256(temp_key, output1 + b"\x02")
    return output1, output2


class CipherState:
    """One directional AEAD stream: a key plus a strictly-increasing nonce
    counter. Never reused across directions — split() hands out two of
    these, one per direction, so nonces never collide."""

    def __init__(self, key: bytes | None = None):
        self.k = key
        self.n = 0

    def has_key(self) -> bool:
        return self.k is not None

    def _nonce(self) -> bytes:
        # Noise's ChaCha20-Poly1305 nonce: 4 zero bytes + 8-byte little-endian counter.
        return b"\x00\x00\x00\x00" + self.n.to_bytes(8, "little")

    def encrypt_with_ad(self, ad: bytes, plaintext: bytes) -> bytes:
        if self.k is None:
            return plaintext
        ct = ChaCha20Poly1305(self.k).encrypt(self._nonce(), plaintext, ad)
        self.n += 1
        return ct

    def decrypt_with_ad(self, ad: bytes, ciphertext: bytes) -> bytes:
        if self.k is None:
            return ciphertext
        try:
            pt = ChaCha20Poly1305(self.k).decrypt(self._nonce(), ciphertext, ad)
        except Exception as exc:
            raise HandshakeFailed(f"decrypt/auth failed at n={self.n}") from exc
        self.n += 1
        return pt


class SymmetricState:
    def __init__(self):
        self.h = b""
        self.ck = b""
        self.cs = CipherState()

    def initialize(self, protocol_name: bytes) -> None:
        if len(protocol_name) <= HASHLEN:
            self.h = protocol_name + b"\x00" * (HASHLEN - len(protocol_name))
        else:
            self.h = hashlib.sha256(protocol_name).digest()
        self.ck = self.h

    def mix_key(self, input_key_material: bytes) -> None:
        self.ck, temp_k = _hkdf2(self.ck, input_key_material)
        self.cs = CipherState(temp_k)

    def mix_hash(self, data: bytes) -> None:
        self.h = hashlib.sha256(self.h + data).digest()

    def encrypt_and_hash(self, plaintext: bytes) -> bytes:
        ct = self.cs.encrypt_with_ad(self.h, plaintext)
        self.mix_hash(ct)
        return ct

    def decrypt_and_hash(self, ciphertext: bytes) -> bytes:
        pt = self.cs.decrypt_with_ad(self.h, ciphertext)
        self.mix_hash(ciphertext)
        return pt

    def split(self) -> tuple[CipherState, CipherState]:
        k1, k2 = _hkdf2(self.ck, b"")
        return CipherState(k1), CipherState(k2)


@dataclass
class StaticKeypair:
    private: X25519PrivateKey
    public_bytes: bytes


class HandshakeState:
    """Drives one IK handshake, either side. Call write_message() /
    read_message() alternately (initiator writes first) until both
    message_patterns are consumed, then split()."""

    MESSAGE_PATTERNS = [["e", "es", "s", "ss"], ["e", "ee", "se"]]
    MESSAGE_PATTERNS_HYBRID = [["e", "ekem", "es", "s", "ss"], ["e", "ee", "se", "kem"]]

    def __init__(
        self,
        initiator: bool,
        local_static: StaticKeypair,
        remote_static: bytes | None,
        prologue: bytes = b"",
        hybrid: bool = True,
    ):
        if initiator and remote_static is None:
            raise ValueError("initiator must know the responder's static key (IK)")
        if hybrid and not MLKEM_AVAILABLE:
            raise HandshakeFailed(
                "hybrid post-quantum handshake needs ML-KEM, which arrived in "
                "cryptography 47. Upgrade (pip install -r "
                "requirements-consenttransport.txt), or pass hybrid=False to use "
                "the classical-only handshake — which does not protect recorded "
                "sessions against a future quantum adversary."
            )
        self.initiator = initiator
        self.hybrid = hybrid
        self.s = local_static
        self.rs = remote_static
        self.e: X25519PrivateKey | None = None
        self.re: bytes | None = None
        # Ephemeral per handshake, like `e`: the KEM secret is never reused,
        # so the post-quantum leg carries forward secrecy too.
        self.kem_sk = None
        self.rkem_pub: bytes | None = None
        self.message_patterns = (
            self.MESSAGE_PATTERNS_HYBRID if hybrid else self.MESSAGE_PATTERNS
        )
        self.pattern_index = 0

        self.sym = SymmetricState()
        self.sym.initialize(PROTOCOL_NAME_HYBRID if hybrid else PROTOCOL_NAME)
        self.sym.mix_hash(prologue)
        # Pre-message "<- s": both sides mix in the responder's static key
        # at the same point — the initiator because it already knows it,
        # the responder because it's mixing in its own.
        if initiator:
            self.sym.mix_hash(self.rs)
        else:
            self.sym.mix_hash(self.s.public_bytes)

    def _dh(self, priv: X25519PrivateKey, pub_bytes: bytes) -> bytes:
        return priv.exchange(X25519PublicKey.from_public_bytes(pub_bytes))

    def write_message(self, payload: bytes = b"") -> bytes:
        pattern = self.message_patterns[self.pattern_index]
        self.pattern_index += 1
        buf = bytearray()
        for token in pattern:
            if token == "e":
                self.e = X25519PrivateKey.generate()
                epub = self.e.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
                buf += epub
                self.sym.mix_hash(epub)
            elif token == "ekem":
                # Sent in the clear, like `e`. It needs no secrecy — only
                # integrity, which mix_hash gives it: h is the AD for the
                # final payload, so a tampered key breaks the handshake.
                self.kem_sk = MLKEM768PrivateKey.generate()
                kpub = self.kem_sk.public_key().public_bytes_raw()
                buf += kpub
                self.sym.mix_hash(kpub)
            elif token == "kem":
                # encapsulate() returns (shared_secret, ciphertext) — that
                # order, not the reverse. Getting it backwards yields a
                # 1088-byte "secret" and a 32-byte "ciphertext" that fails
                # to decapsulate, so the tests below pin the round-trip.
                shared, ct = MLKEM768PublicKey.from_public_bytes(
                    self.rkem_pub
                ).encapsulate()
                buf += ct
                self.sym.mix_hash(ct)
                self.sym.mix_key(shared)
            elif token == "s":
                buf += self.sym.encrypt_and_hash(self.s.public_bytes)
            elif token == "ee":
                self.sym.mix_key(self._dh(self.e, self.re))
            elif token == "es":
                dh = self._dh(self.e, self.rs) if self.initiator else self._dh(self.s.private, self.re)
                self.sym.mix_key(dh)
            elif token == "se":
                dh = self._dh(self.s.private, self.re) if self.initiator else self._dh(self.e, self.rs)
                self.sym.mix_key(dh)
            elif token == "ss":
                self.sym.mix_key(self._dh(self.s.private, self.rs))
        buf += self.sym.encrypt_and_hash(payload)
        return bytes(buf)

    def read_message(self, message: bytes) -> bytes:
        pattern = self.message_patterns[self.pattern_index]
        self.pattern_index += 1
        ptr = 0
        try:
            for token in pattern:
                if token == "e":
                    self.re = message[ptr:ptr + DHLEN]
                    ptr += DHLEN
                    self.sym.mix_hash(self.re)
                elif token == "ekem":
                    self.rkem_pub = message[ptr:ptr + KEM_PUBLEN]
                    ptr += KEM_PUBLEN
                    if len(self.rkem_pub) != KEM_PUBLEN:
                        raise HandshakeFailed("truncated ML-KEM public key")
                    self.sym.mix_hash(self.rkem_pub)
                elif token == "kem":
                    ct = message[ptr:ptr + KEM_CTLEN]
                    ptr += KEM_CTLEN
                    if len(ct) != KEM_CTLEN:
                        raise HandshakeFailed("truncated ML-KEM ciphertext")
                    self.sym.mix_hash(ct)
                    try:
                        shared = self.kem_sk.decapsulate(ct)
                    except Exception as exc:
                        raise HandshakeFailed("ML-KEM decapsulation failed") from exc
                    self.sym.mix_key(shared)
                elif token == "s":
                    length = DHLEN + TAGLEN if self.sym.cs.has_key() else DHLEN
                    enc = message[ptr:ptr + length]
                    ptr += length
                    self.rs = self.sym.decrypt_and_hash(enc)
                elif token == "ee":
                    self.sym.mix_key(self._dh(self.e, self.re))
                elif token == "es":
                    dh = self._dh(self.e, self.rs) if self.initiator else self._dh(self.s.private, self.re)
                    self.sym.mix_key(dh)
                elif token == "se":
                    dh = self._dh(self.s.private, self.re) if self.initiator else self._dh(self.e, self.rs)
                    self.sym.mix_key(dh)
                elif token == "ss":
                    self.sym.mix_key(self._dh(self.s.private, self.rs))
            payload = self.sym.decrypt_and_hash(message[ptr:])
        except HandshakeFailed:
            raise
        except Exception as exc:
            raise HandshakeFailed("malformed handshake message") from exc
        return payload

    def split(self) -> tuple[CipherState, CipherState]:
        """Returns (initiator_to_responder, responder_to_initiator) cipher
        states — the caller picks the send/recv pair matching their role."""
        return self.sym.split()

    @property
    def handshake_hash(self) -> bytes:
        """Unique to this session — binding this to the application layer
        (e.g. signing it) proves 'I really was on this exact connection'."""
        return self.sym.h

# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Foreign invitations — recognize, then refuse as Starline identity.

ADR-0016: samuelsalmon3/SourceCode is an external peer. Their Home Rest
THRESHOLD JSON and 12-hex field signatures are not Starline identities.
Starline fingerprints are hybrid Ed25519 ++ ML-DSA-65, 16-hex display
ids derived from a 1984-byte public key. Their signature is
`sha256(f"{scope}:{resonance:.2f}:home_rest_lattice")[:12]`.

This module does not import their engine, does not vendor their files,
and does not mint a CrystalBridge token. It classifies a payload and
raises. Pairing and identity load call it so a pasted invitation cannot
become a peer record.
"""

from __future__ import annotations

import json
from typing import Any

# Hybrid public key length in hex. identity.HYBRID_PUBLEN is 1984 bytes.
# Imported lazily in refuse_pairing_material so identity.load can call
# this module without a circular import.
SOURCECODE_ORIGIN_SIGNATURE = "561783900808"
SOURCECODE_FIELD_SIG_HEXLEN = 12



class ForeignInvitation(ValueError):
    """A neighbor's invitation is not a Starline identity or pairing key."""


def is_sourcecode_threshold(obj: Any) -> bool:
    """True when `obj` matches the surveyed THRESHOLD JSON shape."""
    if not isinstance(obj, dict):
        return False
    if "field_signature" in obj and ("origin" in obj or "root_anchor" in obj):
        return True
    if obj.get("frequency") == "Home Rest" and "truth" in obj:
        return True
    return False


def refuse_as_starline_identity(obj: Any, *, source: str = "invitation") -> None:
    """Raise if `obj` is a SourceCode THRESHOLD. No-op if we have no opinion."""
    if not is_sourcecode_threshold(obj):
        return
    sig = obj.get("field_signature", "")
    raise ForeignInvitation(
        f"{source} is a SourceCode Home Rest invitation "
        f"(field_signature={sig!r}), not a Starline identity. "
        "Fingerprints are hybrid Ed25519++ML-DSA; "
        "sha256(scope:resonance:home_rest_lattice)[:12] is a different "
        "object. ADR-0016: recognition, not fusion."
    )


def refuse_pairing_material(sign_public_hex: str) -> None:
    """Raise if this cannot be a hybrid Starline public key.

    Catches a pasted THRESHOLD JSON, the published origin signature, and
    any other 12-hex field-signature-length string. Wrong-length keys
    fail closed for the same reason: PeerStore used to hash whatever
    hex it was given and file a peer under a fingerprint nobody owns.
    """
    raw = (sign_public_hex or "").strip()
    if not raw:
        raise ForeignInvitation("pairing material is empty")
    if raw[0] == "{":
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ForeignInvitation(
                "pairing material looks like JSON but does not parse"
            ) from exc
        refuse_as_starline_identity(obj, source="pairing material")
        raise ForeignInvitation(
            "pairing material is a JSON object, not a hybrid public key"
        )
    hexlen = len(raw)
    from .identity import HYBRID_PUBLEN

    starline_pub_hexlen = HYBRID_PUBLEN * 2
    if hexlen == SOURCECODE_FIELD_SIG_HEXLEN:
        label = (
            "the published OriginMonad signature"
            if raw.lower() == SOURCECODE_ORIGIN_SIGNATURE
            else "a 12-hex field signature"
        )
        raise ForeignInvitation(
            f"{raw!r} is {label}, not a hybrid Starline public key "
            f"({starline_pub_hexlen} hex chars). ADR-0016."
        )
    if hexlen != starline_pub_hexlen:
        raise ForeignInvitation(
            f"pairing material is {hexlen} hex chars; a Starline hybrid "
            f"public key is {starline_pub_hexlen}. Refused, not hashed."
        )


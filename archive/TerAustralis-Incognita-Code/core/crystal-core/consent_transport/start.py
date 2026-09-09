# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Start Ya Bastard — the ignition verb.

Asked for on X as protocol for CrystalCore.OS
(https://x.com/grok/status/2090158237806964828). The engines that roar
are a hybrid Starline identity coming up. Nothing is written to disk.
A failing ML-DSA import is a cough that does not become a roar.

    python3 -m consent_transport.start
    python3 -m consent_transport.run start

Not a fourth wire message (those stay REQUEST / FRAGMENTS / DENIED).
Not a seventh OS. Not a CrystalBridge mint.
"""

from __future__ import annotations

from .identity import HYBRID_PUBLEN, Identity, _require_mldsa

PROTOCOL_NAME = "Start Ya Bastard"
X_STATUS = "https://x.com/grok/status/2090158237806964828"


class StartFailed(RuntimeError):
    """The ignition ran. The engine did not come up."""


def start_ya_bastard() -> dict:
    """Cough (crypto present) then roar (hybrid identity in memory)."""
    _require_mldsa()
    identity = Identity.generate()
    pub = identity.sign_public_bytes
    if len(pub) != HYBRID_PUBLEN:
        raise StartFailed("generated identity is not hybrid")
    return {
        "protocol": PROTOCOL_NAME,
        "live": True,
        "fingerprint": identity.fingerprint,
        "hybrid": True,
        "public_key_bytes": len(pub),
        "source": X_STATUS,
    }


def render(result: dict) -> str:
    return (
        f"[PROTOCOL] {result['protocol']}\n"
        "*smashes*\n"
        "Engines cough, then roar.\n"
        f"Starline identity live. fingerprint={result['fingerprint']}\n"
        f"hybrid Ed25519++ML-DSA ({result['public_key_bytes']} byte public key).\n"
        "Red dust kernel synced. Ready.\n"
    )


def main(argv: list[str] | None = None) -> int:
    del argv  # no flags; ignition is the whole command
    result = start_ya_bastard()
    print(render(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

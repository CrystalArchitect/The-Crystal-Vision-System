# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The peer store — every agent Starline has ever been introduced to.

Not secret in the cryptographic sense (public keys are, by definition,
public) but private in the social sense: this file is your address book.
It stays local, is gitignored, and is never synced anywhere by Starline
itself.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from .identity import fingerprint_for

DEFAULT_PEERS_PATH = Path("starline_peers.json")


@dataclass
class Peer:
    fingerprint: str          # hash of the hybrid public key, truncated — display id
    sign_public_hex: str      # full hybrid public key (Ed25519 ++ ML-DSA-65), hex
    dh_public_hex: str        # full X25519 public key, hex
    label: str = ""           # human-given name, e.g. "Sam's companion"
    consented: bool = False   # has the human approved fragment exchange with this peer?


class PeerStore:
    """Load/save/query the local peer list. Adding a peer here is the
    'pairing' step — it does NOT grant consent by itself; consent.py
    handles that separately and explicitly."""

    def __init__(self, path: Path = DEFAULT_PEERS_PATH):
        self.path = path
        self.peers: dict[str, Peer] = {}
        if path.exists():
            raw = json.loads(path.read_text())
            self.peers = {fp: Peer(**p) for fp, p in raw.items()}

    def save(self) -> None:
        """Replace the address book only after the new bytes are complete.

        Host trust refuses this write on shared/unknown hosts unless the
        path is job-scoped GitHub scratch. A crash mid-write used to
        destroy the previous peer list — same defect TokenStore and
        identity already closed. 0600: private in the social sense.
        """
        from host_trust.classify import require_steward_persist

        path = Path(self.path)
        require_steward_persist("peer-save", path)
        tmp = path.with_name(path.name + ".tmp")
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(
                    {fp: asdict(p) for fp, p in self.peers.items()},
                    fh,
                    indent=2,
                )
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

    def add(self, sign_public_hex: str, dh_public_hex: str, label: str = "") -> Peer:
        # Must be the same derivation Identity.fingerprint uses — hence the
        # shared function rather than a second copy of the rule here. A
        # truncation of the key hex (the old rule) would not commit to the
        # ML-DSA half, which is the whole point of the change.
        from .foreign import refuse_pairing_material

        refuse_pairing_material(sign_public_hex)
        fingerprint = fingerprint_for(bytes.fromhex(sign_public_hex))
        peer = self.peers.get(fingerprint)
        if peer is None:
            peer = Peer(fingerprint, sign_public_hex, dh_public_hex, label)
            self.peers[fingerprint] = peer
        else:
            peer.label = label or peer.label
        self.save()
        return peer

    def get(self, fingerprint: str) -> Peer | None:
        return self.peers.get(fingerprint)

    def is_known(self, fingerprint: str) -> bool:
        return fingerprint in self.peers

    def find_by_dh(self, dh_public_hex: str) -> Peer | None:
        """Look up a peer by the X25519 key seen in a Noise handshake —
        that's the only identity a responder has until it maps it back
        to a paired peer record."""
        for peer in self.peers.values():
            if peer.dh_public_hex == dh_public_hex:
                return peer
        return None

    def list(self) -> list[Peer]:
        return list(self.peers.values())

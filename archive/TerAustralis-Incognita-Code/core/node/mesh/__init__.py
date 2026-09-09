# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""libp2p mesh stub — Phase 1 local only. Real multiaddr / gossipsub later."""

from .stub import MeshPeer, MeshStub, PeerInfo

__all__ = ["MeshPeer", "MeshStub", "PeerInfo"]

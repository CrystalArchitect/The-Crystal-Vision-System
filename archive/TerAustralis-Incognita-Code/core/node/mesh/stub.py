# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""
Crystal Core mesh transport stub (libp2p-shaped API, in-process only).

Real stack (HOLD until audit / mainnet gate):
  - rust-libp2p or js-libp2p
  - gossipsub for manifests + twin deltas
  - noise + yamux
  - identify + mDNS (LAN) + bootstrap list (region)

This module lets node agent + tests exercise peer discovery, dial, and
message fan-out without network sockets. Replace MeshStub with a real
transport implementing the same surface.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class PeerInfo:
    peer_id: str
    multiaddrs: list[str]
    did: Optional[str] = None
    region: str = "budapest-starline"
    protocols: list[str] = field(
        default_factory=lambda: [
            "/crystal/manifest/1.0.0",
            "/crystal/receipt/1.0.0",
            "/crystal/twin-delta/1.0.0",
        ]
    )
    last_seen: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "peer_id": self.peer_id,
            "multiaddrs": list(self.multiaddrs),
            "did": self.did,
            "region": self.region,
            "protocols": list(self.protocols),
            "last_seen": self.last_seen,
        }


MessageHandler = Callable[[str, dict[str, Any]], None]


class MeshPeer:
    """One in-process peer identity."""

    def __init__(
        self,
        *,
        did: Optional[str] = None,
        region: str = "budapest-starline",
        listen: str = "/ip4/127.0.0.1/tcp/0",
    ) -> None:
        self.peer_id = "12D3KooW" + uuid.uuid4().hex[:38]
        self.did = did or f"did:crystal:peer-{self.peer_id[-8:]}"
        self.region = region
        self.listen = listen
        self.info = PeerInfo(
            peer_id=self.peer_id,
            multiaddrs=[f"{listen}/p2p/{self.peer_id}"],
            did=self.did,
            region=region,
        )
        self._handlers: dict[str, list[MessageHandler]] = {}
        self._connected: set[str] = set()
        self._inbox: list[dict[str, Any]] = []

    def on(self, protocol: str, handler: MessageHandler) -> None:
        self._handlers.setdefault(protocol, []).append(handler)

    def _deliver(self, protocol: str, payload: dict[str, Any], from_peer: str) -> None:
        env = {
            "from": from_peer,
            "protocol": protocol,
            "payload": payload,
            "ts": time.time(),
        }
        self._inbox.append(env)
        for h in self._handlers.get(protocol, []):
            h(from_peer, payload)

    def inbox(self) -> list[dict[str, Any]]:
        return list(self._inbox)


class MeshStub:
    """
    Shared fabric for N MeshPeer instances (same process).

    Usage:
        mesh = MeshStub()
        a = mesh.spawn(did="did:crystal:hub-bud")
        b = mesh.spawn(did="did:crystal:edge-vie")
        mesh.dial(a.peer_id, b.peer_id)
        mesh.publish(a.peer_id, "/crystal/manifest/1.0.0", {"epoch": "sister-2"})
    """

    PROTOCOL_MANIFEST = "/crystal/manifest/1.0.0"
    PROTOCOL_RECEIPT = "/crystal/receipt/1.0.0"
    PROTOCOL_TWIN = "/crystal/twin-delta/1.0.0"

    def __init__(self, *, region: str = "budapest-starline") -> None:
        self.region = region
        self._peers: dict[str, MeshPeer] = {}
        self._edges: set[tuple[str, str]] = set()
        self.authority = "HOLD"
        self.transport = "in-process-stub"  # not libp2p wire

    def spawn(
        self,
        *,
        did: Optional[str] = None,
        listen: str = "/ip4/127.0.0.1/tcp/0",
    ) -> MeshPeer:
        p = MeshPeer(did=did, region=self.region, listen=listen)
        self._peers[p.peer_id] = p
        return p

    def peers(self) -> list[PeerInfo]:
        return [p.info for p in self._peers.values()]

    def get(self, peer_id: str) -> Optional[MeshPeer]:
        return self._peers.get(peer_id)

    def dial(self, a: str, b: str) -> bool:
        if a not in self._peers or b not in self._peers or a == b:
            return False
        edge = tuple(sorted((a, b)))
        self._edges.add(edge)
        self._peers[a]._connected.add(b)
        self._peers[b]._connected.add(a)
        self._peers[a].info.last_seen = time.time()
        self._peers[b].info.last_seen = time.time()
        return True

    def connected(self, peer_id: str) -> list[str]:
        p = self._peers.get(peer_id)
        return sorted(p._connected) if p else []

    def publish(self, from_peer: str, protocol: str, payload: dict[str, Any]) -> int:
        """Gossip-shaped fan-out to all dialed neighbors (1 hop)."""
        if from_peer not in self._peers:
            return 0
        n = 0
        for other in self._peers[from_peer]._connected:
            self._peers[other]._deliver(protocol, payload, from_peer)
            n += 1
        return n

    def broadcast(self, from_peer: str, protocol: str, payload: dict[str, Any]) -> int:
        """Send to every peer in the fabric except self."""
        if from_peer not in self._peers:
            return 0
        n = 0
        for pid, peer in self._peers.items():
            if pid == from_peer:
                continue
            peer._deliver(protocol, payload, from_peer)
            n += 1
        return n

    def snapshot(self) -> dict[str, Any]:
        return {
            "transport": self.transport,
            "authority": self.authority,
            "region": self.region,
            "peer_count": len(self._peers),
            "edge_count": len(self._edges),
            "peers": [p.to_dict() for p in self.peers()],
            "note": "libp2p wire protocol not enabled — mainnet HOLD",
        }

"""
IncognitaNode — design-facing edge node model for TerAustralis Incognita.

Honest status (mid-2026 local tree):
  - crystalCore  → real: wraps crystalcore.Clementine (local companion)
  - ethicsSignature, redDustBuffer, starlinePorts, connectedNodes
                 → typed stubs only; no mesh runtime, no network broadcast
  - Process()    → local path: optional companion.chat; does NOT sync a lattice

This module exists so the vision struct has a place in code without lying
that CrystalMatrix / full mesh is online. Mesh fields stay empty unless a
future Phase-2 implementation fills them.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Set

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .companion import Clementine


SovereignUUID = str


@dataclass
class DreamtimeField:
    """Current local 'frequency' — mood/context placeholder, not RF hardware."""
    phase: float = 0.0
    label: str = "idle"
    updated: str = ""

    def touch(self, label: str = "active") -> None:
        self.label = label
        self.updated = datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class RedDustPacket:
    """One unit of local work / utterance held before (or instead of) mesh send."""
    payload: str
    kind: str = "resonance"
    when: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


@dataclass
class StarlineVector:
    """Outbound interface descriptor. Empty until routing exists."""
    name: str
    target: str = ""
    active: bool = False


@dataclass
class SovereignIntent:
    core_directive: str = "presence_and_sovereignty"
    evolved_priority: str = "local_only"
    boundary_expansion: float = 0.0


@dataclass
class EthicsDelta:
    coherence_delta: float = 0.0
    sovereignty_delta: float = 0.0
    exploitation_risk: float = 0.0


@dataclass
class SovereignEthicsHash:
    """Tamper-evident chain stub — local hash lineage, not a network lock."""
    lineage: Optional["SovereignEthicsHash"] = None
    delta: EthicsDelta = field(default_factory=EthicsDelta)
    intent: SovereignIntent = field(default_factory=SovereignIntent)
    lock: str = ""
    version: int = 0
    timestamp: str = ""

    def seal(self) -> "SovereignEthicsHash":
        body = f"{self.version}|{self.intent.core_directive}|{self.delta}"
        prev = self.lineage.lock if self.lineage else "genesis"
        self.lock = hashlib.sha256(f"{prev}|{body}".encode()).hexdigest()[:32]
        self.timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        return self


class EthicsCore:
    """Minimal local ethics step. Not the full lattice EthicsCore module."""

    @staticmethod
    def recurse(signature: SovereignEthicsHash,
                transmuted: "TransmutedResult") -> SovereignEthicsHash:
        delta = EthicsDelta(
            coherence_delta=1.0 if transmuted.ok else 0.0,
            sovereignty_delta=1.0,
            exploitation_risk=0.0,
        )
        nxt = SovereignEthicsHash(
            lineage=signature,
            delta=delta,
            intent=signature.intent,
            version=signature.version + 1,
        )
        return nxt.seal()


@dataclass
class TransmutedResult:
    """Output of local 'Red Dust' step — today: text ready for companion or log."""
    text: str
    ok: bool = True
    requires_starline: bool = False
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class IncognitaNode:
    """
    One sovereign edge node.

    Spec fields from the vision struct, grounded:
      crystalCore      → optional Clementine instance (FractalCrystal = recursive
                         self-similar companion stack on this device)
      connectedNodes   → always empty until CrystalMatrix ships
      redDustBuffer    → local queue of recent Process inputs
      starlinePorts    → declared but inactive
      ethicsSignature  → local hash chain updated on Process
    """

    id: SovereignUUID = field(default_factory=lambda: str(uuid.uuid4()))
    crystal_core: Optional["Clementine"] = None
    resonance_field: DreamtimeField = field(default_factory=DreamtimeField)
    connected_nodes: Set["IncognitaNode"] = field(default_factory=set)
    red_dust_buffer: list[RedDustPacket] = field(default_factory=list)
    starline_ports: list[StarlineVector] = field(default_factory=list)
    ethics_signature: SovereignEthicsHash = field(
        default_factory=lambda: SovereignEthicsHash().seal())

    buffer_max: int = 64

    @property
    def crystalCore(self) -> Optional["Clementine"]:
        return self.crystal_core

    @property
    def resonanceField(self) -> DreamtimeField:
        return self.resonance_field

    @property
    def connectedNodes(self) -> Set["IncognitaNode"]:
        return self.connected_nodes

    @property
    def redDustBuffer(self) -> list[RedDustPacket]:
        return self.red_dust_buffer

    @property
    def starlinePorts(self) -> list[StarlineVector]:
        return self.starline_ports

    @property
    def ethicsSignature(self) -> SovereignEthicsHash:
        return self.ethics_signature

    def mesh_sync(self) -> dict[str, Any]:
        """Phase-lock with neighbors. No peers → local phase only."""
        n = len(self.connected_nodes)
        return {
            "peers": n,
            "synchronized": n == 0,
            "mode": "local_solo" if n == 0 else "mesh",
            "note": "CrystalMatrix not implemented; connectedNodes is empty.",
        }

    def dreamtime_filter(self, resonance_input: str) -> str:
        """Light local filter: strip, refuse empty. No mystical network."""
        text = (resonance_input or "").strip()
        self.resonance_field.touch("filtered")
        return text

    def red_dust_transmute(self, dust: str,
                           intent: SovereignIntent) -> TransmutedResult:
        """
        Red Dust step today = stage text under sovereign intent.
        Does not call external APIs. Optional companion runs in Process.
        """
        if not dust:
            return TransmutedResult(text="", ok=False, meta={"reason": "empty"})
        return TransmutedResult(
            text=dust,
            ok=True,
            requires_starline=False,
            meta={"intent": intent.core_directive},
        )

    def starline_weave(self, transmuted: TransmutedResult) -> list[StarlineVector]:
        """Routing matrix stub — returns inactive ports only."""
        return list(self.starline_ports)

    def broadcast_to_mesh(self, transmuted: TransmutedResult,
                          phase: dict[str, Any]) -> dict[str, Any]:
        """
        No network send. 'Broadcast' = return a local result envelope.
        """
        return {
            "broadcast": False,
            "reason": "no_mesh",
            "phase": phase,
            "text": transmuted.text,
            "ok": transmuted.ok,
            "node_id": self.id,
            "ethics_version": self.ethics_signature.version,
            "ethics_lock": self.ethics_signature.lock,
        }

    def Process(self, resonanceInput: str) -> dict[str, Any]:
        """Spec name. Prefer process() in new code."""
        return self.process(resonanceInput)

    def process(self, resonance_input: str) -> dict[str, Any]:
        """
        Process(resonanceInput) — local pipeline matching the vision order:

          MeshSync → Dreamtime filter → Red Dust transmute
          → (optional Starline) → EthicsCore.Recurse → BroadcastToMesh

        If crystal_core is set and input is non-empty, also runs companion.chat
        and returns the reply in the envelope. Still does not leave the device.
        """
        phase = self.mesh_sync()
        filtered = self.dreamtime_filter(resonance_input)
        packet = RedDustPacket(payload=filtered)
        self.red_dust_buffer.append(packet)
        if len(self.red_dust_buffer) > self.buffer_max:
            self.red_dust_buffer = self.red_dust_buffer[-self.buffer_max:]

        transmuted = self.red_dust_transmute(
            filtered, self.ethics_signature.intent)

        vectors = []
        if transmuted.requires_starline:
            vectors = self.starline_weave(transmuted)

        self.ethics_signature = EthicsCore.recurse(
            self.ethics_signature, transmuted)

        reply = None
        if transmuted.ok and self.crystal_core is not None and transmuted.text:
            reply = self.crystal_core.chat(transmuted.text)

        out = self.broadcast_to_mesh(transmuted, phase)
        out["starline_vectors"] = [
            {"name": v.name, "active": v.active} for v in vectors]
        out["reply"] = reply
        out["mesh_online"] = False
        return out


def local_node(companion: Optional["Clementine"] = None) -> IncognitaNode:
    """Factory: one edge node, no peers, optional live companion."""
    return IncognitaNode(crystal_core=companion)

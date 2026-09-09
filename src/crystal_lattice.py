#!/usr/bin/env python3
"""
CrystalLattice - Relational / Connective Substrate for CrystalCore

The Lattice is the "surround" that links CrystalCore systems to each other
and to the wider Incognita Lattice (human coordination, other devices, and
external LLMs). It does three things, and only three things:

  1. Registers NODES — participants in the mesh: this local core, humans,
     other devices, and external LLMs (Grok, Claude, ...). Every node has a
     consent permission bitmask and a kind; local nodes carry auto-detected
     platform info so provenance records show which hardware produced what.

  2. Gates HANDOFFS — every piece of content that crosses between nodes
     travels as a HandoffEnvelope: consent-flagged, provenance-hashed,
     coherence-tagged. Consent is FAIL-CLOSED (same rule as CrystalFlow):
     if the target node's permissions don't cover the envelope's consent
     flags, the envelope is never created.

  3. Enforces the AIR-GAP DEFAULT — the Lattice ships with no network code
     at all. Sending to an external node requires the caller to (a) construct
     the lattice with allow_external=True, and (b) supply a transport
     function explicitly. Otherwise external sends refuse and log. Local
     handoffs (device-to-device on the sovereign side) work out of the box.

This is the Sovereign LLM Communication Layer's foundation: a standardized,
consent-gated envelope protocol for handing context to and receiving
conclusions from external models — with every transfer auditable and the
sovereignty boundary (what leaves the device) explicit and inspectable.

Hardware agnosticism: pure standard library, no platform assumptions.
detect_platform() reports what we're actually running on (old laptop,
phone, Pi, server — anything with CPython 3.8+) for provenance, never for
gatekeeping.

Dependencies: standard library only.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import hashlib
import json
import platform
import sys
import time


# --------------------------------------------------------------------------- #
# Platform detection (provenance, not gatekeeping)
# --------------------------------------------------------------------------- #
def detect_platform() -> Dict[str, Any]:
    """Best-effort description of the hardware/OS we're running on.

    Purely informational: recorded on local nodes so provenance shows which
    device produced a conclusion. CrystalCore never refuses to run based on
    platform — graceful degradation is handled by each layer (e.g. memory
    pruning), not by allowlisting hardware.
    """
    return {
        "system": platform.system(),          # Linux / Darwin / Windows / ...
        "machine": platform.machine(),        # x86_64 / arm64 / aarch64 / ...
        "python_version": platform.python_version(),
        "implementation": sys.implementation.name,
    }


# --------------------------------------------------------------------------- #
# Nodes
# --------------------------------------------------------------------------- #
@dataclass
class LatticeNode:
    """A participant in the lattice.

    kind: "local_core" (a CrystalCore instance), "device" (another sovereign
    device), "human" (a person in the Sovereign Node Mesh), or
    "external_llm" (a model outside the sovereignty boundary).

    permissions is a consent bitmask ANDed against envelope consent flags —
    the same convention as CrystalMemory's ConsumerRegistry.
    """
    node_id: str
    name: str
    kind: str = "device"
    permissions: int = 0b1
    platform_info: Optional[Dict[str, Any]] = None
    registered_at: float = field(default_factory=time.time)

    EXTERNAL_KINDS = ("external_llm",)

    @property
    def is_external(self) -> bool:
        return self.kind in self.EXTERNAL_KINDS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "kind": self.kind,
            "permissions": self.permissions,
            "platform_info": self.platform_info,
            "registered_at": self.registered_at,
        }


# --------------------------------------------------------------------------- #
# Handoff envelope
# --------------------------------------------------------------------------- #
@dataclass
class HandoffEnvelope:
    """One consent-gated, provenance-hashed transfer between two nodes.

    The provenance hash covers content + endpoints + timestamp, so a tampered
    envelope fails verify_integrity() on receipt. coherence carries the
    sending side's confidence so the receiver can gate on it (an external
    LLM's reply re-enters CrystalMemory as low-trust until reviewed).
    """
    envelope_id: str
    source_node_id: str
    target_node_id: str
    content: Any
    consent_flags: int = 0b1
    coherence: float = 1.0
    provenance_note: str = ""
    created_at: float = field(default_factory=time.time)
    provenance_hash: str = ""

    def __post_init__(self):
        if not self.provenance_hash:
            self.provenance_hash = self._compute_hash()

    def _compute_hash(self) -> str:
        canonical = json.dumps(
            {
                "content": self.content,
                "source": self.source_node_id,
                "target": self.target_node_id,
                "created_at": self.created_at,
            },
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        """True iff the content/endpoints still match the provenance hash."""
        return self.provenance_hash == self._compute_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "content": self.content,
            "consent_flags": self.consent_flags,
            "coherence": round(self.coherence, 4),
            "provenance_note": self.provenance_note,
            "created_at": self.created_at,
            "provenance_hash": self.provenance_hash,
        }


# --------------------------------------------------------------------------- #
# The lattice
# --------------------------------------------------------------------------- #
class CrystalLattice:
    """Relational substrate: registered nodes + consent-gated handoffs.

    Zero-trust posture:
      - consent fail-closed on every envelope (target permissions must cover
        the envelope's consent flags — no partial delivery);
      - air-gapped by default (allow_external=False refuses every send to an
        external node, whatever transport is offered);
      - no built-in network I/O: even with allow_external=True the caller
        must inject a transport callable, so exactly one auditable function
        ever moves bytes off the device;
      - append-only transfer log for every attempt, allowed or refused.
    """

    def __init__(self, allow_external: bool = False,
                 min_handoff_coherence: float = 0.0):
        self.allow_external = allow_external
        self.min_handoff_coherence = min_handoff_coherence
        self.nodes: Dict[str, LatticeNode] = {}
        self.transfer_log: List[Dict[str, Any]] = []
        self._envelope_counter = 0

    # --- node registration ---------------------------------------------------- #
    def register_node(
        self,
        node_id: str,
        name: str,
        kind: str = "device",
        permissions: int = 0b1,
    ) -> LatticeNode:
        node = LatticeNode(
            node_id=node_id,
            name=name,
            kind=kind,
            permissions=permissions,
            # Local participants get real platform info for provenance.
            platform_info=detect_platform() if kind == "local_core" else None,
        )
        self.nodes[node_id] = node
        return node

    def revoke_node(self, node_id: str) -> bool:
        """Zero out a node's permissions without deleting its history."""
        if node_id in self.nodes:
            self.nodes[node_id].permissions = 0
            self._log(None, node_id, "revoked", "permissions set to 0")
            return True
        return False

    # --- envelope creation (consent fail-closed) ------------------------------- #
    def create_envelope(
        self,
        source_node_id: str,
        target_node_id: str,
        content: Any,
        consent_flags: int = 0b1,
        coherence: float = 1.0,
        provenance_note: str = "",
    ) -> Optional[HandoffEnvelope]:
        """Build a handoff envelope, or refuse (returning None) and log why.

        Refuses when either endpoint is unregistered, when the target's
        permissions don't cover the consent flags, or when coherence falls
        below the lattice's handoff floor. Nothing is created on refusal —
        a forbidden transfer never exists, even locally.
        """
        reason = None
        if source_node_id not in self.nodes:
            reason = f"unknown source node {source_node_id!r}"
        elif target_node_id not in self.nodes:
            reason = f"unknown target node {target_node_id!r}"
        elif consent_flags == 0:
            reason = "envelope carries no consent flags (nobody may see it)"
        elif not (self.nodes[target_node_id].permissions & consent_flags):
            reason = (f"target {target_node_id!r} permissions do not cover "
                      f"consent flags {bin(consent_flags)}")
        elif coherence < self.min_handoff_coherence:
            reason = (f"coherence {coherence:.3f} below handoff floor "
                      f"{self.min_handoff_coherence:.3f}")

        if reason:
            self._log(source_node_id, target_node_id, "refused_create", reason)
            return None

        self._envelope_counter += 1
        return HandoffEnvelope(
            envelope_id=f"env_{self._envelope_counter:06d}",
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            content=content,
            consent_flags=consent_flags,
            coherence=coherence,
            provenance_note=provenance_note,
        )

    # --- sending (air-gap default) --------------------------------------------- #
    def send(
        self,
        envelope: HandoffEnvelope,
        transport: Optional[Callable[[Dict[str, Any]], Any]] = None,
    ) -> Dict[str, Any]:
        """Attempt to deliver an envelope. Returns an auditable result dict.

        Local targets deliver in-process (the log IS the delivery record;
        a caller wires real device-to-device transport the same way as
        external, by injecting it). External targets additionally require
        allow_external=True AND an explicit transport callable — the air-gap
        default means a lattice can never leak by accident.
        """
        if not envelope.verify_integrity():
            self._log(envelope.source_node_id, envelope.target_node_id,
                      "refused_send", "provenance hash mismatch (tampered?)",
                      envelope)
            return {"status": "refused", "reason": "integrity_check_failed"}

        target = self.nodes.get(envelope.target_node_id)
        if target is None:
            self._log(envelope.source_node_id, envelope.target_node_id,
                      "refused_send", "unknown target node", envelope)
            return {"status": "refused", "reason": "unknown_target"}

        # Re-check consent at send time — permissions may have been revoked
        # between creation and send.
        if not (target.permissions & envelope.consent_flags):
            self._log(envelope.source_node_id, envelope.target_node_id,
                      "refused_send", "consent revoked or insufficient", envelope)
            return {"status": "refused", "reason": "consent_denied"}

        if target.is_external:
            if not self.allow_external:
                self._log(envelope.source_node_id, envelope.target_node_id,
                          "refused_send",
                          "air-gap default: external sends disabled", envelope)
                return {"status": "refused", "reason": "air_gapped"}
            if transport is None:
                self._log(envelope.source_node_id, envelope.target_node_id,
                          "refused_send",
                          "external send requires an explicit transport", envelope)
                return {"status": "refused", "reason": "no_transport"}
            transport(envelope.to_dict())
            self._log(envelope.source_node_id, envelope.target_node_id,
                      "sent_external", "crossed sovereignty boundary", envelope)
            return {"status": "sent", "boundary": "external"}

        self._log(envelope.source_node_id, envelope.target_node_id,
                  "sent_local", "", envelope)
        return {"status": "sent", "boundary": "local"}

    # --- receiving -------------------------------------------------------------- #
    def receive(self, envelope_dict: Dict[str, Any],
                trust_coherence: float = 0.3) -> Optional[HandoffEnvelope]:
        """Reconstruct an inbound envelope (e.g. an external LLM's reply).

        Integrity is verified against the embedded provenance hash; a
        tampered envelope returns None. The envelope's coherence is CAPPED
        at trust_coherence: content from across the boundary re-enters as
        low-trust and must earn confidence through review (Guardian /
        TruthSeeker), never assert it.
        """
        env = HandoffEnvelope(
            envelope_id=envelope_dict.get("envelope_id", "env_inbound"),
            source_node_id=envelope_dict.get("source_node_id", ""),
            target_node_id=envelope_dict.get("target_node_id", ""),
            content=envelope_dict.get("content"),
            consent_flags=envelope_dict.get("consent_flags", 0b1),
            coherence=min(envelope_dict.get("coherence", 1.0), trust_coherence),
            provenance_note=envelope_dict.get("provenance_note", ""),
            created_at=envelope_dict.get("created_at", time.time()),
            provenance_hash=envelope_dict.get("provenance_hash", ""),
        )
        if not env.verify_integrity():
            self._log(env.source_node_id, env.target_node_id,
                      "refused_receive", "provenance hash mismatch", env)
            return None
        self._log(env.source_node_id, env.target_node_id, "received", "", env)
        return env

    # --- audit ------------------------------------------------------------------ #
    def _log(self, source: Optional[str], target: str, action: str,
             reason: str, envelope: Optional[HandoffEnvelope] = None) -> None:
        self.transfer_log.append({
            "source_node_id": source,
            "target_node_id": target,
            "action": action,
            "reason": reason,
            "envelope_id": envelope.envelope_id if envelope else None,
            "provenance_hash": envelope.provenance_hash if envelope else None,
            "timestamp": time.time(),
        })

    def get_transfer_log(self) -> List[Dict[str, Any]]:
        return list(self.transfer_log)

    def get_stats(self) -> Dict[str, Any]:
        actions = [e["action"] for e in self.transfer_log]
        return {
            "nodes": len(self.nodes),
            "external_nodes": sum(1 for n in self.nodes.values() if n.is_external),
            "transfers_logged": len(self.transfer_log),
            "refusals": sum(1 for a in actions if a.startswith("refused")),
            "external_sends": actions.count("sent_external"),
            "allow_external": self.allow_external,
        }


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    lattice = CrystalLattice()  # air-gapped by default

    core = lattice.register_node("core_1", "Kitchen CrystalCore", kind="local_core")
    print("Local core platform:", core.platform_info)

    lattice.register_node("phone_1", "Family phone", kind="device", permissions=0b11)
    lattice.register_node("claude", "Claude (external)", kind="external_llm",
                          permissions=0b1)

    # Local handoff succeeds.
    env = lattice.create_envelope("core_1", "phone_1",
                                  {"note": "dinner decision synced"},
                                  consent_flags=0b10)
    print("Local send:", lattice.send(env))

    # External handoff refuses under the air-gap default.
    env2 = lattice.create_envelope("core_1", "claude",
                                   {"question": "summarise this policy"},
                                   consent_flags=0b1)
    print("External send (air-gapped):", lattice.send(env2))

    print("Stats:", lattice.get_stats())

#!/usr/bin/env python3
"""
Governed Messaging — Phase 4: Mesh Activation
CrystalCore OS

Every message crossing the Sovereign Node Mesh passes the constitutional
gates from Phase 2 before it is routed over the Phase 3 topology:

1. Activation gate  — both endpoints must be activated mesh nodes
2. Consent gate     — fail-closed: consent-required messages are blocked
                      until a consenter explicitly grants
3. Coherence gate   — sender coherence must meet the message's minimum
4. Route gate       — a topology path must exist

Every delivery AND every block is recorded in the immutable audit trail.

Standard library only.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from crystallcore.governance.sces_volume_5_consent import (
    ConsentRegistry, ConsentRecord,
)
from crystallcore.governance.sces_volume_8_tracking import (
    AuditTrail, AuditEvent, EventType,
)
from .sovereign_mesh import SovereignNodeMesh


@dataclass
class MeshMessage:
    """A message travelling the mesh under constitutional constraints."""
    sender: str
    receiver: str
    payload: Dict
    consent_required: bool = False
    min_coherence: float = 0.0
    message_id: str = field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:12]}")
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class DeliveryResult:
    """Outcome of a send attempt."""
    message_id: str
    delivered: bool
    route: List[str] = field(default_factory=list)
    blocked_reason: Optional[str] = None


class GovernedMessenger:
    """Send messages through the mesh under SCES governance gates."""

    def __init__(self, mesh: SovereignNodeMesh,
                 consent_registry: Optional[ConsentRegistry] = None,
                 audit_trail: Optional[AuditTrail] = None):
        self.mesh = mesh
        self.consent = consent_registry or ConsentRegistry()
        self.audit = audit_trail or AuditTrail()
        self.delivered: Dict[str, DeliveryResult] = {}

    # ------------------------------------------------------------------ #
    # Consent lifecycle
    # ------------------------------------------------------------------ #
    def request_consent(self, message: MeshMessage, consenter: str) -> str:
        """Open a consent request for a message. Returns the consent_id."""
        consent_id = f"consent_{message.message_id}"
        self.consent.request_consent(ConsentRecord(
            consent_id=consent_id,
            operation_id=message.message_id,
            requester=message.sender,
            consenter=consenter,
        ))
        return consent_id

    def grant_consent(self, consent_id: str) -> bool:
        return self.consent.grant_consent(consent_id)

    def withhold_consent(self, consent_id: str, reason: str) -> bool:
        return self.consent.withhold_consent(consent_id, reason)

    # ------------------------------------------------------------------ #
    # Sending
    # ------------------------------------------------------------------ #
    def send(self, message: MeshMessage) -> DeliveryResult:
        """Send a message through all four gates. Fail-closed."""
        # Gate 1: activation
        sender = self.mesh.nodes.get(message.sender)
        receiver = self.mesh.nodes.get(message.receiver)
        if not sender or not receiver:
            return self._block(message, "unknown_node")
        if not sender.activated or not receiver.activated:
            return self._block(message, "node_not_activated")

        # Gate 2: consent (fail-closed — a consent-required message with no
        # granted consent record is blocked, even if none was requested)
        if message.consent_required:
            consents = self.consent.get_operation_consents(message.message_id)
            if not consents or not all(c.is_active() for c in consents):
                return self._block(message, "consent_not_granted")

        # Gate 3: coherence
        if sender.coherence < message.min_coherence:
            return self._block(message, "coherence_insufficient")

        # Gate 4: route must exist
        route = self.mesh.route(message.sender, message.receiver)
        if not route:
            return self._block(message, "no_route")

        result = DeliveryResult(message_id=message.message_id,
                                delivered=True, route=route)
        self.delivered[message.message_id] = result
        self.audit.record_event(AuditEvent(
            event_id=f"deliver_{message.message_id}",
            event_type=EventType.OPERATION_EXECUTED,
            actor=message.sender,
            subject=message.message_id,
            new_state={"delivered": True, "hops": len(route) - 1},
            metadata={"route": route},
        ))
        return result

    def _block(self, message: MeshMessage, reason: str) -> DeliveryResult:
        result = DeliveryResult(message_id=message.message_id,
                                delivered=False, blocked_reason=reason)
        self.audit.record_event(AuditEvent(
            event_id=f"block_{message.message_id}",
            event_type=EventType.OPERATION_BLOCKED,
            actor=message.sender,
            subject=message.message_id,
            new_state={"delivered": False},
            metadata={"reason": reason},
        ))
        return result

    # ------------------------------------------------------------------ #
    # Inspection
    # ------------------------------------------------------------------ #
    def delivery_log(self) -> List[AuditEvent]:
        """All send-related audit events (delivered and blocked)."""
        return (self.audit.get_events_of_type(EventType.OPERATION_EXECUTED) +
                self.audit.get_events_of_type(EventType.OPERATION_BLOCKED))

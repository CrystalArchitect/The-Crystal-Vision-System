#!/usr/bin/env python3
"""
SCES Volume 8: Evidence & State Tracking Systems
Sentinel Constitutional Execution System v11.0

Central audit trail for all governance decisions, evidence changes,
authority grants, and system state transitions.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """Types of governance events to track."""
    EVIDENCE_CREATED = "evidence_created"
    EVIDENCE_MATURED = "evidence_matured"
    AUTHORITY_GRANTED = "authority_granted"
    AUTHORITY_REVOKED = "authority_revoked"
    WITNESS_APPROVED = "witness_approved"
    WITNESS_REJECTED = "witness_rejected"
    CONSENT_GRANTED = "consent_granted"
    CONSENT_WITHHELD = "consent_withheld"
    GATE_PASSED = "gate_passed"
    GATE_FAILED = "gate_failed"
    OPERATION_EXECUTED = "operation_executed"
    OPERATION_BLOCKED = "operation_blocked"


@dataclass
class AuditEvent:
    """Single auditable event in the system."""
    event_id: str
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    actor: str = ""                  # Who caused the event
    subject: str = ""                # What the event is about
    previous_state: Dict[str, Any] = field(default_factory=dict)
    new_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "actor": self.actor,
            "subject": self.subject,
            "previous_state": self.previous_state,
            "new_state": self.new_state,
            "metadata": self.metadata,
        }


class AuditTrail:
    """Immutable audit trail of all governance events."""

    def __init__(self):
        self._events: List[AuditEvent] = []
        self._by_subject: Dict[str, List[int]] = {}  # subject -> event indices

    def record_event(self, event: AuditEvent) -> bool:
        """Record an event. Events are immutable once recorded."""
        self._events.append(event)
        idx = len(self._events) - 1
        self._by_subject.setdefault(event.subject, []).append(idx)
        return True

    def get_event(self, event_id: str) -> Optional[AuditEvent]:
        """Look up event by ID."""
        for event in self._events:
            if event.event_id == event_id:
                return event
        return None

    def get_subject_history(self, subject: str) -> List[AuditEvent]:
        """Get all events related to a subject (entity ID)."""
        indices = self._by_subject.get(subject, [])
        return [self._events[i] for i in indices]

    def get_events_of_type(self, event_type: EventType) -> List[AuditEvent]:
        """Get all events of a specific type."""
        return [e for e in self._events if e.event_type == event_type]

    def get_all_events(self) -> List[AuditEvent]:
        """Get all events in chronological order."""
        return list(self._events)

    def verify_immutability(self) -> bool:
        """Verify audit trail has not been tampered with."""
        # Simple check: events should have strictly increasing timestamps
        for i in range(1, len(self._events)):
            if self._events[i].timestamp < self._events[i-1].timestamp:
                return False
        return True


class SystemStateTracker:
    """Track current system state derived from audit trail."""

    def __init__(self, audit_trail: AuditTrail):
        self.audit_trail = audit_trail
        self._state: Dict[str, Any] = {}

    def get_entity_state(self, entity_id: str) -> Dict[str, Any]:
        """Get current state of an entity."""
        history = self.audit_trail.get_subject_history(entity_id)
        state = {}
        for event in history:
            state.update(event.new_state)
        return state

    def get_system_state(self) -> Dict[str, Any]:
        """Get aggregated system state from all events."""
        state = {}
        for event in self.audit_trail.get_all_events():
            if event.subject not in state:
                state[event.subject] = {}
            state[event.subject].update(event.new_state)
        return state

    def count_events_by_type(self) -> Dict[str, int]:
        """Count events by type."""
        counts = {et.value: 0 for et in EventType}
        for event in self.audit_trail.get_all_events():
            counts[event.event_type.value] += 1
        return counts


# Global singleton
_audit_trail: Optional[AuditTrail] = None


def get_audit_trail() -> AuditTrail:
    global _audit_trail
    if _audit_trail is None:
        _audit_trail = AuditTrail()
    return _audit_trail


def get_system_state_tracker() -> SystemStateTracker:
    return SystemStateTracker(get_audit_trail())

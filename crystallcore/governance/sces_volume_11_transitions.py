#!/usr/bin/env python3
"""
SCES Volume 11: Transition & Escalation Paths
Sentinel Constitutional Execution System v11.0

Defines valid state transitions and escalation paths for:
- Authority status changes
- Evidence maturity advancement
- Component lifecycle
- Emergency protocols
- Appeal and override procedures
"""

from enum import Enum
from typing import Dict, Set, Optional, List, Any
from dataclasses import dataclass, field
from datetime import datetime


class SystemState(Enum):
    """Valid system states."""
    OPERATIONAL = "operational"
    DEGRADED = "degraded"
    QUARANTINED = "quarantined"
    BLOCKED = "blocked"
    TRANSITIONING = "transitioning"
    ESCALATED = "escalated"


class EscalationType(Enum):
    """Types of escalation."""
    AUTHORITY_REQUIRED = "authority_required"
    WITNESS_OVERRIDE = "witness_override"
    EMERGENCY = "emergency"
    APPEAL = "appeal"
    SPECIAL_RESOLUTION = "special_resolution"


@dataclass
class TransitionRule:
    """Defines valid state transitions."""
    from_state: SystemState
    to_state: SystemState
    requires_authority: bool = False
    requires_witness: bool = False
    timeout_seconds: Optional[int] = None
    description: str = ""


@dataclass
class EscalationRequest:
    """Request to escalate to a different state/authority level."""
    escalation_id: str
    escalation_type: EscalationType
    requested_by: str
    current_state: SystemState
    requested_state: SystemState
    reason: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    decided_at: Optional[datetime] = None
    decided_by: Optional[str] = None
    approved: bool = False
    decision_notes: str = ""


class TransitionEngine:
    """Manages state transitions and escalations."""

    def __init__(self):
        self._transition_rules: Dict[tuple, TransitionRule] = {}
        self._current_state: SystemState = SystemState.OPERATIONAL
        self._state_history: List[tuple] = []
        self._escalations: Dict[str, EscalationRequest] = {}

    def register_transition(self, rule: TransitionRule) -> None:
        """Register a valid state transition."""
        key = (rule.from_state, rule.to_state)
        self._transition_rules[key] = rule

    def can_transition(self, from_state: SystemState,
                      to_state: SystemState) -> bool:
        """Check if transition is allowed."""
        return (from_state, to_state) in self._transition_rules

    def get_transition_rule(self, from_state: SystemState,
                           to_state: SystemState) -> Optional[TransitionRule]:
        """Get rule for transition."""
        return self._transition_rules.get((from_state, to_state))

    def execute_transition(self, to_state: SystemState,
                          authorized_by: Optional[str] = None) -> bool:
        """Execute a state transition."""
        rule = self.get_transition_rule(self._current_state, to_state)
        if not rule:
            return False

        if rule.requires_authority and not authorized_by:
            return False

        self._state_history.append((self._current_state, to_state, datetime.utcnow()))
        self._current_state = to_state
        return True

    def request_escalation(self, request: EscalationRequest) -> bool:
        """Request escalation to higher authority."""
        self._escalations[request.escalation_id] = request
        return True

    def approve_escalation(self, escalation_id: str, approver: str) -> bool:
        """Approve an escalation request."""
        escalation = self._escalations.get(escalation_id)
        if not escalation:
            return False
        escalation.approved = True
        escalation.decided_by = approver
        escalation.decided_at = datetime.utcnow()
        return self.execute_transition(escalation.requested_state, approver)

    def deny_escalation(self, escalation_id: str, denier: str,
                       notes: str) -> bool:
        """Deny an escalation request."""
        escalation = self._escalations.get(escalation_id)
        if not escalation:
            return False
        escalation.approved = False
        escalation.decided_by = denier
        escalation.decided_at = datetime.utcnow()
        escalation.decision_notes = notes
        return True

    def get_current_state(self) -> SystemState:
        return self._current_state

    def get_state_history(self) -> List[tuple]:
        return list(self._state_history)


def _register_default_transitions(engine: TransitionEngine) -> None:
    """Register standard state transitions."""

    # Normal operation transitions
    engine.register_transition(TransitionRule(
        from_state=SystemState.OPERATIONAL,
        to_state=SystemState.DEGRADED,
        description="Normal to degraded",
        requires_witness=True,
    ))

    engine.register_transition(TransitionRule(
        from_state=SystemState.DEGRADED,
        to_state=SystemState.OPERATIONAL,
        description="Degraded to normal (recovery)",
        requires_witness=True,
    ))

    engine.register_transition(TransitionRule(
        from_state=SystemState.OPERATIONAL,
        to_state=SystemState.QUARANTINED,
        description="Quarantine due to integrity issues",
        requires_authority=True,
    ))

    engine.register_transition(TransitionRule(
        from_state=SystemState.QUARANTINED,
        to_state=SystemState.OPERATIONAL,
        description="Exit quarantine after verification",
        requires_authority=True,
        requires_witness=True,
    ))

    engine.register_transition(TransitionRule(
        from_state=SystemState.QUARANTINED,
        to_state=SystemState.BLOCKED,
        description="Escalate from quarantine to blocked",
        requires_authority=True,
    ))

    engine.register_transition(TransitionRule(
        from_state=SystemState.BLOCKED,
        to_state=SystemState.ESCALATED,
        description="Escalate to higher authority",
        requires_authority=True,
    ))


# Global singleton
_transition_engine: Optional[TransitionEngine] = None


def get_transition_engine() -> TransitionEngine:
    global _transition_engine
    if _transition_engine is None:
        _transition_engine = TransitionEngine()
        _register_default_transitions(_transition_engine)
    return _transition_engine

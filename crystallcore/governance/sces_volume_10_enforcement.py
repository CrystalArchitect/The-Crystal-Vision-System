#!/usr/bin/env python3
"""
SCES Volume 10: Constitutional Enforcement & Penalties
Sentinel Constitutional Execution System v11.0

Enforcement mechanisms for constitutional violations. Operations that violate
covenants face escalating penalties and constraints.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class ViolationType(Enum):
    """Types of constitutional violations."""
    AUTHORITY_MISSING = "authority_missing"
    EVIDENCE_IMMATURE = "evidence_immature"
    WITNESS_MISSING = "witness_missing"
    CONSENT_WITHHELD = "consent_withheld"
    COHERENCE_LOW = "coherence_low"
    TRANSPARENCY_VIOLATED = "transparency_violated"


class PenaltyLevel(Enum):
    """Severity levels of penalties."""
    WARNING = "warning"
    SUSPENDED = "suspended"
    QUARANTINED = "quarantined"
    REVOKED = "revoked"


@dataclass
class Violation:
    """Record of a constitutional violation."""
    violation_id: str
    violation_type: ViolationType
    violator: str                    # Who violated
    timestamp: datetime = field(default_factory=datetime.utcnow)
    description: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)
    penalty_applied: Optional[PenaltyLevel] = None
    penalty_expires: Optional[datetime] = None
    appeal_filed: bool = False
    appeal_decision: Optional[str] = None  # "upheld", "overturned", "pending"


class EnforcementEngine:
    """Applies penalties for constitutional violations."""

    def __init__(self):
        self._violations: Dict[str, Violation] = {}
        self._violator_penalties: Dict[str, List[PenaltyLevel]] = {}  # violator -> penalties
        self._penalty_rules: Dict[ViolationType, List[PenaltyLevel]] = {
            vtype: [] for vtype in ViolationType
        }

    def register_penalty_rule(self, violation_type: ViolationType,
                            penalty_levels: List[PenaltyLevel]) -> None:
        """Register escalating penalties for a violation type."""
        self._penalty_rules[violation_type] = penalty_levels

    def record_violation(self, violation: Violation) -> PenaltyLevel:
        """Record a violation and apply penalty."""
        self._violations[violation.violation_id] = violation

        # Determine penalty based on violation type
        penalty_levels = self._penalty_rules.get(violation.violation_type, [PenaltyLevel.WARNING])

        # Get prior violations by same violator
        prior = self._violator_penalties.get(violation.violator, [])
        penalty_index = min(len(prior), len(penalty_levels) - 1)
        penalty = penalty_levels[penalty_index]

        violation.penalty_applied = penalty
        violation.penalty_expires = datetime.utcnow() + timedelta(hours=24)

        self._violator_penalties.setdefault(violation.violator, []).append(penalty)
        return penalty

    def get_violator_penalties(self, violator: str) -> List[PenaltyLevel]:
        """Get all penalties for a violator."""
        return self._violator_penalties.get(violator, [])

    def get_active_penalties(self, violator: str) -> List[PenaltyLevel]:
        """Get active (non-expired) penalties for a violator."""
        penalties = []
        now = datetime.utcnow()
        for v in self._violations.values():
            if v.violator == violator and v.penalty_applied:
                if v.penalty_expires is None or v.penalty_expires > now:
                    penalties.append(v.penalty_applied)
        return penalties

    def is_violator_suspended(self, violator: str) -> bool:
        """Check if violator is under suspension."""
        active = self.get_active_penalties(violator)
        return any(p in (PenaltyLevel.SUSPENDED, PenaltyLevel.REVOKED) for p in active)

    def file_appeal(self, violation_id: str) -> bool:
        """File appeal for a violation."""
        violation = self._violations.get(violation_id)
        if not violation:
            return False
        violation.appeal_filed = True
        violation.appeal_decision = "pending"
        return True

    def decide_appeal(self, violation_id: str, decision: str) -> bool:
        """Decide on an appeal."""
        violation = self._violations.get(violation_id)
        if not violation or not violation.appeal_filed:
            return False
        if decision not in ("upheld", "overturned"):
            return False
        violation.appeal_decision = decision
        if decision == "overturned":
            violation.penalty_applied = None
        return True


# Register default penalty escalations
def _register_default_penalties(engine: EnforcementEngine) -> None:
    engine.register_penalty_rule(ViolationType.AUTHORITY_MISSING,
                                [PenaltyLevel.WARNING, PenaltyLevel.SUSPENDED, PenaltyLevel.REVOKED])
    engine.register_penalty_rule(ViolationType.EVIDENCE_IMMATURE,
                                [PenaltyLevel.WARNING, PenaltyLevel.SUSPENDED])
    engine.register_penalty_rule(ViolationType.WITNESS_MISSING,
                                [PenaltyLevel.WARNING, PenaltyLevel.SUSPENDED])
    engine.register_penalty_rule(ViolationType.CONSENT_WITHHELD,
                                [PenaltyLevel.WARNING])
    engine.register_penalty_rule(ViolationType.COHERENCE_LOW,
                                [PenaltyLevel.QUARANTINED])
    engine.register_penalty_rule(ViolationType.TRANSPARENCY_VIOLATED,
                                [PenaltyLevel.SUSPENDED, PenaltyLevel.REVOKED])


# Global singleton
_enforcement_engine: Optional[EnforcementEngine] = None


def get_enforcement_engine() -> EnforcementEngine:
    global _enforcement_engine
    if _enforcement_engine is None:
        _enforcement_engine = EnforcementEngine()
        _register_default_penalties(_enforcement_engine)
    return _enforcement_engine

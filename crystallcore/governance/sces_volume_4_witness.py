#!/usr/bin/env python3
"""
SCES Volume 4: Witness Discipline & Authority Transfer
Sentinel Constitutional Execution System v11.0

Foundational Principle: A non-originating steward must independently verify
evidence before authority can be granted. This is the witness discipline.

Witness requirements:
- Must be a different steward from the originator
- Must independently verify all claims
- Must attest with signature
- Can delegate verification but remains accountable
- Witness refusal must be documented
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class WitnessStatus(Enum):
    """Status of a witness task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELEGATED = "delegated"


@dataclass
class WitnessAttestation:
    """A witness's formal attestation of evidence verification."""
    attestation_id: str
    witness_steward: str              # Non-originating steward
    evidence_id: str
    status: WitnessStatus = WitnessStatus.PENDING
    signature: Optional[str] = None   # SHA256 of witness verification
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    delegated_to: Optional[str] = None
    notes: str = ""

    def approve(self, signature: str) -> bool:
        """Approve evidence with witness signature."""
        if self.status not in (WitnessStatus.PENDING, WitnessStatus.IN_PROGRESS):
            return False
        self.status = WitnessStatus.APPROVED
        self.signature = signature
        self.completed_at = datetime.utcnow()
        return True

    def reject(self, reason: str) -> bool:
        """Reject evidence with documented reason."""
        if self.status not in (WitnessStatus.PENDING, WitnessStatus.IN_PROGRESS):
            return False
        self.status = WitnessStatus.REJECTED
        self.rejection_reason = reason
        self.completed_at = datetime.utcnow()
        return True

    def delegate(self, delegate_steward: str) -> bool:
        """Delegate witness task to another steward."""
        if self.status != WitnessStatus.PENDING:
            return False
        self.status = WitnessStatus.DELEGATED
        self.delegated_to = delegate_steward
        return True


class WitnessRegistry:
    """Track all witness attestations and disciplinary history."""

    def __init__(self):
        self._attestations: Dict[str, WitnessAttestation] = {}
        self._by_witness: Dict[str, List[str]] = {}  # witness -> [attestation_ids]
        self._by_evidence: Dict[str, List[str]] = {}  # evidence -> [attestation_ids]
        self._refusal_history: Dict[str, int] = {}  # witness -> refusal_count

    def request_witness(self, attestation: WitnessAttestation) -> bool:
        """Request witness attestation for evidence."""
        if attestation.attestation_id in self._attestations:
            return False
        self._attestations[attestation.attestation_id] = attestation
        self._by_witness.setdefault(attestation.witness_steward, []).append(
            attestation.attestation_id)
        self._by_evidence.setdefault(attestation.evidence_id, []).append(
            attestation.attestation_id)
        return True

    def approve_attestation(self, attestation_id: str, signature: str) -> bool:
        """Record witness approval."""
        attestation = self._attestations.get(attestation_id)
        if not attestation:
            return False
        return attestation.approve(signature)

    def reject_attestation(self, attestation_id: str, reason: str) -> bool:
        """Record witness rejection."""
        attestation = self._attestations.get(attestation_id)
        if not attestation:
            return False
        result = attestation.reject(reason)
        if result:
            self._refusal_history[attestation.witness_steward] = \
                self._refusal_history.get(attestation.witness_steward, 0) + 1
        return result

    def delegate_attestation(self, attestation_id: str,
                           delegate_steward: str) -> bool:
        """Delegate witness task."""
        attestation = self._attestations.get(attestation_id)
        if not attestation:
            return False
        return attestation.delegate(delegate_steward)

    def get_witness_attestations(self, witness_steward: str) -> List[WitnessAttestation]:
        """Get all attestations for a witness."""
        attestation_ids = self._by_witness.get(witness_steward, [])
        return [self._attestations[aid] for aid in attestation_ids]

    def get_evidence_attestations(self, evidence_id: str) -> List[WitnessAttestation]:
        """Get all witness attestations for a piece of evidence."""
        attestation_ids = self._by_evidence.get(evidence_id, [])
        return [self._attestations[aid] for aid in attestation_ids]

    def is_witness_valid(self, witness_steward: str, max_refusals: int = 3) -> bool:
        """Check if witness is in good standing."""
        refusals = self._refusal_history.get(witness_steward, 0)
        return refusals < max_refusals

    def get_refusal_count(self, witness_steward: str) -> int:
        """Get number of refusals by witness."""
        return self._refusal_history.get(witness_steward, 0)


# Global singleton
_witness_registry: Optional[WitnessRegistry] = None


def get_witness_registry() -> WitnessRegistry:
    global _witness_registry
    if _witness_registry is None:
        _witness_registry = WitnessRegistry()
    return _witness_registry

#!/usr/bin/env python3
"""
SCES Volume 12: Ratification & Authority Confirmation
Sentinel Constitutional Execution System v11.0

Final authority confirmation process. A claim is not considered authorized
until it has been ratified through the proper channels by a non-originating
steward with full evidence maturity.

Ratification gates:
1. All evidence must reach Verified_Local or higher
2. All witness attestations must be approved
3. All governance gates must be passed
4. Ratifying steward signature required
5. Constitutional covenants must be satisfied
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


class RatificationStatus(Enum):
    """Status of ratification process."""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    RATIFIED = "ratified"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


@dataclass
class RatificationRecord:
    """Records the ratification of authority or evidence."""
    ratification_id: str
    subject_id: str                  # Evidence or authority ID being ratified
    subject_type: str                # "evidence" or "authority"
    originator: str                  # Original author
    ratifying_steward: str           # Non-originating steward doing ratification
    status: RatificationStatus = RatificationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None
    ratified_at: Optional[datetime] = None
    ratification_signature: Optional[str] = None
    evidence_maturity_met: bool = False
    witness_attestations_met: bool = False
    governance_gates_met: bool = False
    covenants_satisfied: bool = False
    rejection_reason: Optional[str] = None
    notes: str = ""

    def can_be_ratified(self) -> bool:
        """Check if all conditions for ratification are met."""
        return (
            self.status == RatificationStatus.IN_REVIEW and
            self.evidence_maturity_met and
            self.witness_attestations_met and
            self.governance_gates_met and
            self.covenants_satisfied
        )

    def ratify(self, signature: str) -> bool:
        """Complete ratification with signature."""
        if not self.can_be_ratified():
            return False
        self.status = RatificationStatus.RATIFIED
        self.ratified_at = datetime.utcnow()
        self.ratification_signature = signature
        return True

    def reject(self, reason: str) -> bool:
        """Reject ratification."""
        if self.status not in (RatificationStatus.PENDING, RatificationStatus.IN_REVIEW):
            return False
        self.status = RatificationStatus.REJECTED
        self.rejection_reason = reason
        return True


class RatificationRegistry:
    """Central registry for all ratifications."""

    def __init__(self):
        self._records: Dict[str, RatificationRecord] = {}
        self._by_subject: Dict[str, List[str]] = {}  # subject -> ratification_ids
        self._by_steward: Dict[str, List[str]] = {}  # steward -> ratification_ids

    def submit_for_ratification(self, record: RatificationRecord) -> bool:
        """Submit record for ratification review."""
        if record.ratification_id in self._records:
            return False
        self._records[record.ratification_id] = record
        self._by_subject.setdefault(record.subject_id, []).append(
            record.ratification_id)
        self._by_steward.setdefault(record.ratifying_steward, []).append(
            record.ratification_id)
        return True

    def get_ratification(self, ratification_id: str) -> Optional[RatificationRecord]:
        """Look up ratification by ID."""
        return self._records.get(ratification_id)

    def get_subject_ratifications(self, subject_id: str) -> List[RatificationRecord]:
        """Get all ratifications for a subject."""
        ratification_ids = self._by_subject.get(subject_id, [])
        return [self._records[rid] for rid in ratification_ids]

    def get_steward_ratifications(self, steward: str) -> List[RatificationRecord]:
        """Get all ratifications by a steward."""
        ratification_ids = self._by_steward.get(steward, [])
        return [self._records[rid] for rid in ratification_ids]

    def complete_review(self, ratification_id: str,
                       evidence_met: bool, witness_met: bool,
                       gates_met: bool, covenants_met: bool) -> bool:
        """Complete review phase and check if ready to ratify."""
        record = self._records.get(ratification_id)
        if not record or record.status != RatificationStatus.PENDING:
            return False

        record.status = RatificationStatus.IN_REVIEW
        record.reviewed_at = datetime.utcnow()
        record.evidence_maturity_met = evidence_met
        record.witness_attestations_met = witness_met
        record.governance_gates_met = gates_met
        record.covenants_satisfied = covenants_met

        return True

    def ratify(self, ratification_id: str, signature: str) -> bool:
        """Ratify if all conditions met."""
        record = self._records.get(ratification_id)
        if not record:
            return False
        return record.ratify(signature)

    def reject(self, ratification_id: str, reason: str) -> bool:
        """Reject ratification."""
        record = self._records.get(ratification_id)
        if not record:
            return False
        return record.reject(reason)

    def get_ratified_subjects(self) -> List[str]:
        """Get all ratified subjects."""
        ratified = [r for r in self._records.values()
                   if r.status == RatificationStatus.RATIFIED]
        return [r.subject_id for r in ratified]

    def is_subject_ratified(self, subject_id: str) -> bool:
        """Check if subject has been ratified."""
        return subject_id in self.get_ratified_subjects()

    def get_ratification_summary(self) -> Dict[str, int]:
        """Get counts of ratifications by status."""
        summary = {status.value: 0 for status in RatificationStatus}
        for record in self._records.values():
            summary[record.status.value] += 1
        return summary


# Global singleton
_ratification_registry: Optional[RatificationRegistry] = None


def get_ratification_registry() -> RatificationRegistry:
    global _ratification_registry
    if _ratification_registry is None:
        _ratification_registry = RatificationRegistry()
    return _ratification_registry

#!/usr/bin/env python3
"""
SCES Volume 2: Evidence Maturity Model
Sentinel Constitutional Execution System v11.0

Foundational Principle: All evidence progresses through a 7-stage maturity
hierarchy. Authority decisions are gated by required evidence maturity.

The 7 stages:
1. Exists        — Claim recorded, minimum credibility
2. Specified     — Claim clearly defined, scope established
3. Implemented   — Code or process embodies the claim
4. Tested        — Claim verified against test cases
5. Verified_Local — Independent verification by non-originating steward
6. Reproduced_External — External party reproduces verification
7. Authorized    — Authority grant issued based on evidence
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime


class EvidenceMaturity(Enum):
    """7-stage evidence maturity hierarchy."""
    DOES_NOT_EXIST = "does_not_exist"  # Placeholder for absent evidence
    EXISTS = "exists"                  # Claim recorded
    SPECIFIED = "specified"            # Claim clearly defined
    IMPLEMENTED = "implemented"        # Embodied in code/process
    TESTED = "tested"                  # Verified against tests
    VERIFIED_LOCAL = "verified_local"  # Non-originating steward verified
    REPRODUCED_EXTERNAL = "reproduced_external"  # External party verified
    AUTHORIZED = "authorized"          # Authority grant issued


# Maturity progression order
MATURITY_PROGRESSION = [
    EvidenceMaturity.EXISTS,
    EvidenceMaturity.SPECIFIED,
    EvidenceMaturity.IMPLEMENTED,
    EvidenceMaturity.TESTED,
    EvidenceMaturity.VERIFIED_LOCAL,
    EvidenceMaturity.REPRODUCED_EXTERNAL,
    EvidenceMaturity.AUTHORIZED,
]


def maturity_level(maturity: EvidenceMaturity) -> int:
    """Get numeric level of maturity (0-6, or -1 for does_not_exist)."""
    if maturity == EvidenceMaturity.DOES_NOT_EXIST:
        return -1
    try:
        return MATURITY_PROGRESSION.index(maturity)
    except ValueError:
        return -1


def is_mature_enough(actual: EvidenceMaturity, required: EvidenceMaturity) -> bool:
    """Check if actual maturity meets or exceeds requirement."""
    return maturity_level(actual) >= maturity_level(required)


@dataclass
class EvidenceRecord:
    """A piece of evidence progressing through maturity stages."""
    evidence_id: str
    claim: str                          # What is being claimed
    originated_by: str                  # Original author/component
    maturity: EvidenceMaturity = EvidenceMaturity.EXISTS
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None  # Non-originating steward
    reproduced_by: Optional[str] = None  # External verifier
    authorization_granted: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def advance_maturity(self, new_maturity: EvidenceMaturity,
                        verified_by: Optional[str] = None) -> bool:
        """Advance evidence maturity. Returns True if advancement successful."""
        current_level = maturity_level(self.maturity)
        new_level = maturity_level(new_maturity)

        if new_level <= current_level:
            return False  # Can only advance forward

        # VERIFIED_LOCAL requires non-originating steward
        if new_maturity == EvidenceMaturity.VERIFIED_LOCAL:
            if not verified_by or verified_by == self.originated_by:
                return False
            self.verified_by = verified_by
            self.verified_at = datetime.utcnow()

        # REPRODUCED_EXTERNAL requires external party (different from both)
        if new_maturity == EvidenceMaturity.REPRODUCED_EXTERNAL:
            if not verified_by or verified_by == self.originated_by:
                return False
            if verified_by == self.verified_by:
                return False  # Must be different steward
            self.reproduced_by = verified_by

        self.maturity = new_maturity
        return True

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['maturity'] = self.maturity.value
        d['created_at'] = self.created_at.isoformat()
        d['verified_at'] = self.verified_at.isoformat() if self.verified_at else None
        return d


class EvidenceTracker:
    """Central repository for evidence and its maturity progression."""

    def __init__(self):
        self._evidence: Dict[str, EvidenceRecord] = {}
        self._by_claim: Dict[str, List[str]] = {}  # claim -> [evidence_ids]

    def record_evidence(self, record: EvidenceRecord) -> bool:
        """Record new evidence. Returns True if successful."""
        if record.evidence_id in self._evidence:
            return False
        self._evidence[record.evidence_id] = record
        self._by_claim.setdefault(record.claim, []).append(record.evidence_id)
        return True

    def lookup_evidence(self, evidence_id: str) -> Optional[EvidenceRecord]:
        """Look up evidence by ID."""
        return self._evidence.get(evidence_id)

    def lookup_by_claim(self, claim: str) -> List[EvidenceRecord]:
        """Find all evidence supporting a claim."""
        evidence_ids = self._by_claim.get(claim, [])
        return [self._evidence[eid] for eid in evidence_ids]

    def advance_maturity(self, evidence_id: str, new_maturity: EvidenceMaturity,
                        verified_by: Optional[str] = None) -> bool:
        """Advance evidence through maturity stages."""
        record = self._evidence.get(evidence_id)
        if not record:
            return False
        return record.advance_maturity(new_maturity, verified_by)

    def get_evidence_at_maturity(self, maturity: EvidenceMaturity) -> List[EvidenceRecord]:
        """Get all evidence at a specific maturity level."""
        return [e for e in self._evidence.values() if e.maturity == maturity]

    def get_all_evidence(self) -> List[EvidenceRecord]:
        """Get all evidence records."""
        return list(self._evidence.values())

    def maturity_summary(self) -> Dict[str, int]:
        """Count evidence at each maturity level."""
        summary = {level.value: 0 for level in EvidenceMaturity}
        for record in self._evidence.values():
            summary[record.maturity.value] += 1
        return summary


# Global singleton tracker
_evidence_tracker: Optional[EvidenceTracker] = None


def get_evidence_tracker() -> EvidenceTracker:
    global _evidence_tracker
    if _evidence_tracker is None:
        _evidence_tracker = EvidenceTracker()
    return _evidence_tracker

#!/usr/bin/env python3
"""
SCES Volume 5: Consent Model & Coherence Bounds
Sentinel Constitutional Execution System v11.0

Foundational Principle: Authority execution requires consent verification.
Coherence bounds prevent operations on incoherent evidence.

Coherence scale (0.0 to 1.0):
- 0.0-0.3: Low coherence (unverified, external input)
- 0.3-0.7: Medium coherence (partially verified)
- 0.7-1.0: High coherence (fully verified, authorized)

Operations are capped at the coherence level of their lowest-coherence input.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ConsentStatus(Enum):
    """Status of consent for an operation."""
    PENDING = "pending"
    GRANTED = "granted"
    WITHHELD = "withheld"
    REVOKED = "revoked"


@dataclass
class ConsentRecord:
    """Record of consent for an operation."""
    consent_id: str
    operation_id: str                 # Operation requiring consent
    requester: str                    # Who is requesting
    consenter: str                    # Who must grant consent
    status: ConsentStatus = ConsentStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    granted_at: Optional[datetime] = None
    reason: str = ""                  # Reason for withholding/granting

    def grant_consent(self) -> bool:
        if self.status != ConsentStatus.PENDING:
            return False
        self.status = ConsentStatus.GRANTED
        self.granted_at = datetime.utcnow()
        return True

    def withhold_consent(self, reason: str) -> bool:
        if self.status != ConsentStatus.PENDING:
            return False
        self.status = ConsentStatus.WITHHELD
        self.reason = reason
        return True

    def revoke_consent(self) -> bool:
        if self.status != ConsentStatus.GRANTED:
            return False
        self.status = ConsentStatus.REVOKED
        return True

    def is_active(self) -> bool:
        return self.status == ConsentStatus.GRANTED


@dataclass
class CoherenceRecord:
    """Track coherence level of evidence or component."""
    entity_id: str                    # Evidence or component ID
    entity_type: str                  # "evidence" or "component"
    coherence: float = 0.5            # 0.0 to 1.0
    sources: List[str] = field(default_factory=list)  # Source entity IDs
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def is_high_coherence(self) -> bool:
        return self.coherence >= 0.7

    def is_medium_coherence(self) -> bool:
        return 0.3 <= self.coherence < 0.7

    def is_low_coherence(self) -> bool:
        return self.coherence < 0.3


class ConsentRegistry:
    """Track all consent records and decisions."""

    def __init__(self):
        self._consents: Dict[str, ConsentRecord] = {}
        self._by_operation: Dict[str, List[str]] = {}
        self._by_consenter: Dict[str, List[str]] = {}

    def request_consent(self, consent: ConsentRecord) -> bool:
        if consent.consent_id in self._consents:
            return False
        self._consents[consent.consent_id] = consent
        self._by_operation.setdefault(consent.operation_id, []).append(
            consent.consent_id)
        self._by_consenter.setdefault(consent.consenter, []).append(
            consent.consent_id)
        return True

    def grant_consent(self, consent_id: str) -> bool:
        consent = self._consents.get(consent_id)
        if not consent:
            return False
        return consent.grant_consent()

    def withhold_consent(self, consent_id: str, reason: str) -> bool:
        consent = self._consents.get(consent_id)
        if not consent:
            return False
        return consent.withhold_consent(reason)

    def operation_has_consent(self, operation_id: str) -> bool:
        """Check if all consents for operation are granted."""
        consent_ids = self._by_operation.get(operation_id, [])
        if not consent_ids:
            return True  # No consent required
        return all(self._consents[cid].is_active() for cid in consent_ids)

    def get_operation_consents(self, operation_id: str) -> List[ConsentRecord]:
        consent_ids = self._by_operation.get(operation_id, [])
        return [self._consents[cid] for cid in consent_ids]


class CoherenceTracker:
    """Track coherence levels of entities."""

    def __init__(self):
        self._coherence: Dict[str, CoherenceRecord] = {}

    def set_coherence(self, record: CoherenceRecord) -> bool:
        self._coherence[record.entity_id] = record
        return True

    def get_coherence(self, entity_id: str) -> Optional[CoherenceRecord]:
        return self._coherence.get(entity_id)

    def compute_min_coherence(self, entity_ids: List[str]) -> float:
        """Compute minimum coherence from a list of sources."""
        if not entity_ids:
            return 1.0
        coherences = []
        for eid in entity_ids:
            record = self._coherence.get(eid)
            if record:
                coherences.append(record.coherence)
        return min(coherences) if coherences else 0.0

    def can_execute_at_coherence(self, entity_id: str,
                                required_coherence: float) -> bool:
        """Check if entity can execute at required coherence level."""
        record = self._coherence.get(entity_id)
        if not record:
            return False
        return record.coherence >= required_coherence


# Global singletons
_consent_registry: Optional[ConsentRegistry] = None
_coherence_tracker: Optional[CoherenceTracker] = None


def get_consent_registry() -> ConsentRegistry:
    global _consent_registry
    if _consent_registry is None:
        _consent_registry = ConsentRegistry()
    return _consent_registry


def get_coherence_tracker() -> CoherenceTracker:
    global _coherence_tracker
    if _coherence_tracker is None:
        _coherence_tracker = CoherenceTracker()
    return _coherence_tracker

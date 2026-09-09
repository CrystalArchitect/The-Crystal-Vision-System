"""
Governance Layer — SCES v11.0 Constitutional Framework
Part of CrystalCore OS Phase 2

12 SCES Volumes + Evidence Decorators (Phase 2.3):
1. sces_volume_1_authority.py    — Authority Model (explicit grants only)
2. sces_volume_2_evidence.py     — Evidence Maturity Model (7-stage hierarchy)
3. sces_volume_3_verification.py — Verification Procedures & Gates
4. sces_volume_4_witness.py      — Witness Discipline & Authority Transfer
5. sces_volume_5_consent.py      — Consent Model & Coherence Bounds
6. sces_volume_6_principles.py   — Constitutional Principles & Covenants
7. sces_volume_7_gates.py        — Governance Gates & Thresholds
8. sces_volume_8_tracking.py     — Evidence & State Tracking Systems
9. sces_volume_9_grants.py       — Authority Grant & Delegation Model
10. sces_volume_10_enforcement.py — Constitutional Enforcement & Penalties
11. sces_volume_11_transitions.py — Transition & Escalation Paths
12. sces_volume_12_ratification.py— Ratification & Authority Confirmation
13. evidence_decorators.py        — @evidence_state, @requires_authority, etc.

All modules use Python stdlib only. Zero external dependencies.
Version: v0.2 (Phase 2: Constitutional Framework + Evidence Tracking)
Status: PHASE_2_3_IN_PROGRESS
SCES Alignment: v11.0
"""

from .sces_volume_1_authority import (
    AuthorityType, AuthorityScope, AuthorityGrant, AuthorityRegistry,
    get_authority_registry
)
from .sces_volume_2_evidence import (
    EvidenceMaturity, EvidenceRecord, EvidenceTracker, get_evidence_tracker,
    is_mature_enough, maturity_level
)
from .sces_volume_3_verification import (
    VerificationGate, VerificationProcedure, VerificationRegistry,
    get_verification_registry
)
from .sces_volume_4_witness import (
    WitnessStatus, WitnessAttestation, WitnessRegistry, get_witness_registry
)
from .sces_volume_5_consent import (
    ConsentStatus, ConsentRecord, CoherenceRecord,
    ConsentRegistry, CoherenceTracker, get_consent_registry, get_coherence_tracker
)
from .sces_volume_6_principles import (
    ConstitutionalPrinciple, CovenantRule, ConstitutionalCodex,
    get_constitutional_codex
)
from .sces_volume_7_gates import (
    GateType, GateOutcome, GateThreshold, GovernanceGateKeeper, get_gate_keeper
)
from .sces_volume_8_tracking import (
    EventType, AuditEvent, AuditTrail, SystemStateTracker,
    get_audit_trail, get_system_state_tracker
)
from .sces_volume_9_grants import (
    DelegationStatus, AuthorityDelegation, DelegationChain, get_delegation_chain
)
from .sces_volume_10_enforcement import (
    ViolationType, PenaltyLevel, Violation, EnforcementEngine,
    get_enforcement_engine
)
from .sces_volume_11_transitions import (
    SystemState, EscalationType, TransitionRule, EscalationRequest,
    TransitionEngine, get_transition_engine
)
from .sces_volume_12_ratification import (
    RatificationStatus, RatificationRecord, RatificationRegistry,
    get_ratification_registry
)
from .evidence_decorators import (
    ExecutionContext, evidence_state, requires_authority, requires_consent,
    coherence_bounded, witness_required, track_evidence_transition
)

__version__ = "v0.2"
__sces_version__ = "v11.0"
__phase__ = "2"
__status__ = "IMPLEMENTED"

__all__ = [
    # Volume 1: Authority
    "AuthorityType", "AuthorityScope", "AuthorityGrant", "AuthorityRegistry",
    "get_authority_registry",
    # Volume 2: Evidence
    "EvidenceMaturity", "EvidenceRecord", "EvidenceTracker", "get_evidence_tracker",
    "is_mature_enough", "maturity_level",
    # Volume 3: Verification
    "VerificationGate", "VerificationProcedure", "VerificationRegistry",
    "get_verification_registry",
    # Volume 4: Witness
    "WitnessStatus", "WitnessAttestation", "WitnessRegistry", "get_witness_registry",
    # Volume 5: Consent
    "ConsentStatus", "ConsentRecord", "CoherenceRecord",
    "ConsentRegistry", "CoherenceTracker", "get_consent_registry", "get_coherence_tracker",
    # Volume 6: Principles
    "ConstitutionalPrinciple", "CovenantRule", "ConstitutionalCodex",
    "get_constitutional_codex",
    # Volume 7: Gates
    "GateType", "GateOutcome", "GateThreshold", "GovernanceGateKeeper", "get_gate_keeper",
    # Volume 8: Tracking
    "EventType", "AuditEvent", "AuditTrail", "SystemStateTracker",
    "get_audit_trail", "get_system_state_tracker",
    # Volume 9: Grants
    "DelegationStatus", "AuthorityDelegation", "DelegationChain", "get_delegation_chain",
    # Volume 10: Enforcement
    "ViolationType", "PenaltyLevel", "Violation", "EnforcementEngine",
    "get_enforcement_engine",
    # Volume 11: Transitions
    "SystemState", "EscalationType", "TransitionRule", "EscalationRequest",
    "TransitionEngine", "get_transition_engine",
    # Volume 12: Ratification
    "RatificationStatus", "RatificationRecord", "RatificationRegistry",
    "get_ratification_registry",
    # Evidence Decorators (Phase 2.3)
    "ExecutionContext", "evidence_state", "requires_authority", "requires_consent",
    "coherence_bounded", "witness_required", "track_evidence_transition",
]

#!/usr/bin/env python3
"""
SCES Volume 3: Verification Procedures & Gates
Sentinel Constitutional Execution System v11.0

Foundational Principle: All claims must pass through defined verification
gates before advancing in maturity or authority. Verification is performed
by designated agents with specific authority to verify.

Verification gates enforce:
- Evidence maturity requirements
- Non-originating verification mandate
- Repeatable, deterministic procedures
- Witness signature and attestation
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class VerificationGate(Enum):
    """Defined verification gates in the system."""
    SPECIFICATION = "specification"      # Verify claim is well-specified
    IMPLEMENTATION = "implementation"    # Verify code embodies claim
    TEST = "test"                        # Verify test coverage
    LOCAL_WITNESS = "local_witness"      # Non-originating steward
    EXTERNAL_WITNESS = "external_witness"  # External party
    AUTHORITY = "authority"              # Authority gate


@dataclass
class VerificationProcedure:
    """Defines how to verify a claim at a specific gate."""
    gate: VerificationGate
    description: str
    verifier_authority: str              # Authority type required
    requires_non_originating: bool = True
    repeatable: bool = True
    timeout_seconds: Optional[int] = None
    required_inputs: List[str] = field(default_factory=list)
    check_fn: Optional[Callable[[Dict[str, Any]], bool]] = None

    def verify(self, evidence_payload: Dict[str, Any]) -> bool:
        """Run the verification procedure."""
        if self.check_fn:
            return self.check_fn(evidence_payload)
        return True


class VerificationRegistry:
    """Registry of all verification procedures and gates."""

    def __init__(self):
        self._procedures: Dict[VerificationGate, VerificationProcedure] = {}
        self._results: Dict[str, Dict[str, Any]] = {}  # evidence_id -> gate results

    def register_procedure(self, procedure: VerificationProcedure) -> None:
        """Register a verification procedure for a gate."""
        self._procedures[procedure.gate] = procedure

    def get_procedure(self, gate: VerificationGate) -> Optional[VerificationProcedure]:
        """Get procedure for a gate."""
        return self._procedures.get(gate)

    def execute_verification(self, evidence_id: str, gate: VerificationGate,
                            evidence_payload: Dict[str, Any],
                            verifier: str) -> bool:
        """Execute a verification gate. Returns True if passed."""
        proc = self._procedures.get(gate)
        if not proc:
            return False

        passed = proc.verify(evidence_payload)

        # Record result
        if evidence_id not in self._results:
            self._results[evidence_id] = {}
        self._results[evidence_id][gate.value] = {
            "passed": passed,
            "verifier": verifier,
            "timestamp": datetime.utcnow().isoformat(),
        }

        return passed

    def get_verification_result(self, evidence_id: str,
                               gate: VerificationGate) -> Optional[Dict[str, Any]]:
        """Get result of a verification gate for evidence."""
        return self._results.get(evidence_id, {}).get(gate.value)

    def get_all_verifications(self, evidence_id: str) -> Dict[str, Any]:
        """Get all verification results for evidence."""
        return self._results.get(evidence_id, {})


# Global singleton
_verification_registry: Optional[VerificationRegistry] = None


def get_verification_registry() -> VerificationRegistry:
    global _verification_registry
    if _verification_registry is None:
        _verification_registry = VerificationRegistry()
        # Register default procedures
        _register_default_procedures(_verification_registry)
    return _verification_registry


def _register_default_procedures(registry: VerificationRegistry) -> None:
    """Register standard verification procedures."""

    registry.register_procedure(VerificationProcedure(
        gate=VerificationGate.SPECIFICATION,
        description="Verify claim is well-specified with clear boundaries",
        verifier_authority="witness",
        requires_non_originating=True,
    ))

    registry.register_procedure(VerificationProcedure(
        gate=VerificationGate.IMPLEMENTATION,
        description="Verify code/process correctly implements the claim",
        verifier_authority="witness",
        requires_non_originating=True,
    ))

    registry.register_procedure(VerificationProcedure(
        gate=VerificationGate.TEST,
        description="Verify test coverage and passing tests",
        verifier_authority="witness",
        requires_non_originating=True,
    ))

    registry.register_procedure(VerificationProcedure(
        gate=VerificationGate.LOCAL_WITNESS,
        description="Independent verification by local non-originating steward",
        verifier_authority="witness",
        requires_non_originating=True,
    ))

    registry.register_procedure(VerificationProcedure(
        gate=VerificationGate.EXTERNAL_WITNESS,
        description="External party verifies and reproduces verification",
        verifier_authority="witness",
        requires_non_originating=True,
    ))

    registry.register_procedure(VerificationProcedure(
        gate=VerificationGate.AUTHORITY,
        description="Authority grant gate - verify all prior gates passed",
        verifier_authority="steward",
        requires_non_originating=True,
    ))

#!/usr/bin/env python3
"""
SCES Volume 7: Governance Gates & Thresholds
Sentinel Constitutional Execution System v11.0

Governance gates are control points that enforce thresholds for:
- Authority execution
- Evidence advancement
- Witness approval
- Consent confirmation
- Operation execution

Each gate defines required conditions and what happens when violated.
"""

from enum import Enum
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass


class GateType(Enum):
    """Types of governance gates."""
    AUTHORITY = "authority"
    EVIDENCE = "evidence"
    WITNESS = "witness"
    CONSENT = "consent"
    OPERATION = "operation"
    COHERENCE = "coherence"


class GateOutcome(Enum):
    """Possible gate outcomes."""
    PASS = "pass"
    FAIL = "fail"
    QUARANTINE = "quarantine"
    ESCALATE = "escalate"


@dataclass
class GateThreshold:
    """Defines threshold conditions for a gate."""
    gate_id: str
    gate_type: GateType
    description: str
    check_fn: Callable[[Dict[str, Any]], bool]
    on_fail: GateOutcome = GateOutcome.FAIL
    on_pass: GateOutcome = GateOutcome.PASS
    escalation_target: Optional[str] = None


class GovernanceGateKeeper:
    """Enforces governance gates and thresholds."""

    def __init__(self):
        self._gates: Dict[str, GateThreshold] = {}
        self._history: List[Dict[str, Any]] = []

    def register_gate(self, gate: GateThreshold) -> None:
        self._gates[gate.gate_id] = gate

    def check_gate(self, gate_id: str, context: Dict[str, Any]) -> GateOutcome:
        """Check if entity passes gate. Returns outcome."""
        gate = self._gates.get(gate_id)
        if not gate:
            return GateOutcome.FAIL

        passed = gate.check_fn(context)
        outcome = gate.on_pass if passed else gate.on_fail

        # Record in history
        self._history.append({
            "gate_id": gate_id,
            "passed": passed,
            "outcome": outcome.value,
            "context_keys": list(context.keys()),
        })

        return outcome

    def check_all_gates(self, context: Dict[str, Any]) -> tuple[GateOutcome, List[str]]:
        """Check all gates. Returns aggregate outcome and any failed gate IDs."""
        failures = []
        worst_outcome = GateOutcome.PASS

        for gate_id, gate in self._gates.items():
            outcome = self.check_gate(gate_id, context)
            if outcome != GateOutcome.PASS:
                failures.append(gate_id)
                if outcome == GateOutcome.FAIL:
                    worst_outcome = GateOutcome.FAIL
                elif outcome == GateOutcome.QUARANTINE:
                    worst_outcome = GateOutcome.QUARANTINE

        return worst_outcome, failures

    def gate_history(self) -> List[Dict[str, Any]]:
        return list(self._history)


# Global singleton
_gate_keeper: Optional[GovernanceGateKeeper] = None


def get_gate_keeper() -> GovernanceGateKeeper:
    global _gate_keeper
    if _gate_keeper is None:
        _gate_keeper = GovernanceGateKeeper()
        _register_default_gates(_gate_keeper)
    return _gate_keeper


def _register_default_gates(gk: GovernanceGateKeeper) -> None:
    """Register default governance gates."""

    gk.register_gate(GateThreshold(
        gate_id="authority_grant_exists",
        gate_type=GateType.AUTHORITY,
        description="Authority grant must exist and be active",
        check_fn=lambda ctx: (
            "authority_grant" in ctx and
            ctx["authority_grant"] is not None and
            not ctx["authority_grant"].get("revoked", False)
        ),
        on_fail=GateOutcome.FAIL,
    ))

    gk.register_gate(GateThreshold(
        gate_id="evidence_maturity_sufficient",
        gate_type=GateType.EVIDENCE,
        description="Evidence must be sufficiently mature",
        check_fn=lambda ctx: (
            ctx.get("evidence_maturity_level", 0) >=
            ctx.get("required_maturity_level", 0)
        ),
        on_fail=GateOutcome.FAIL,
    ))

    gk.register_gate(GateThreshold(
        gate_id="witness_approved",
        gate_type=GateType.WITNESS,
        description="Witness must have approved",
        check_fn=lambda ctx: ctx.get("witness_approved", False),
        on_fail=GateOutcome.FAIL,
    ))

    gk.register_gate(GateThreshold(
        gate_id="consent_granted",
        gate_type=GateType.CONSENT,
        description="Consent must be granted",
        check_fn=lambda ctx: (
            not ctx.get("requires_consent", False) or
            ctx.get("consent_granted", False)
        ),
        on_fail=GateOutcome.FAIL,
    ))

    gk.register_gate(GateThreshold(
        gate_id="coherence_sufficient",
        gate_type=GateType.COHERENCE,
        description="Coherence must meet requirement",
        check_fn=lambda ctx: (
            ctx.get("current_coherence", 0.0) >=
            ctx.get("required_coherence", 0.0)
        ),
        on_fail=GateOutcome.QUARANTINE,
    ))

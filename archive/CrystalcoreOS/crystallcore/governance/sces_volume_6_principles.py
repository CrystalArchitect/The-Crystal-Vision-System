#!/usr/bin/env python3
"""
SCES Volume 6: Constitutional Principles & Covenants
Sentinel Constitutional Execution System v11.0

The 6 core constitutional principles that all operations must honor:

1. Authority Never Inferred — explicit grants only, from non-originating stewards
2. Evidence Matters — all claims progress through 7-stage maturity
3. Witness Discipline — independent verification is mandatory
4. Consent Required — operations need approval from affected parties
5. Coherence Bounded — operations capped at coherence of lowest input
6. Transparency Enforced — all decisions logged, auditable, verifiable
"""

from enum import Enum
from typing import Dict, List, Any, Callable
from dataclasses import dataclass


class ConstitutionalPrinciple(Enum):
    """Core constitutional principles."""
    AUTHORITY_EXPLICIT = "authority_never_inferred"
    EVIDENCE_MATURITY = "evidence_matters"
    WITNESS_REQUIRED = "witness_discipline"
    CONSENT_NEEDED = "consent_required"
    COHERENCE_BOUNDED = "coherence_bounded"
    TRANSPARENCY = "transparency_enforced"


@dataclass
class CovenantRule:
    """A specific covenant rule that enforces a principle."""
    rule_id: str
    principle: ConstitutionalPrinciple
    description: str
    enforcement_fn: Callable[[Dict[str, Any]], bool]
    penalty_on_violation: str = "operation_rejected"


class ConstitutionalCodex:
    """Repository of constitutional principles and their enforcement rules."""

    def __init__(self):
        self._principles: Dict[ConstitutionalPrinciple, List[CovenantRule]] = {
            p: [] for p in ConstitutionalPrinciple
        }

    def register_covenant(self, rule: CovenantRule) -> None:
        """Register a covenant rule for enforcement."""
        self._principles[rule.principle].append(rule)

    def get_covenants(self, principle: ConstitutionalPrinciple) -> List[CovenantRule]:
        """Get all covenants for a principle."""
        return self._principles.get(principle, [])

    def check_principle(self, principle: ConstitutionalPrinciple,
                       context: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check if all covenants of a principle are satisfied."""
        violations = []
        for rule in self._principles[principle]:
            if not rule.enforcement_fn(context):
                violations.append(rule.rule_id)
        return len(violations) == 0, violations

    def check_all_principles(self, context: Dict[str, Any]) -> tuple[bool, Dict[str, List[str]]]:
        """Check if all principles are satisfied."""
        violations = {}
        all_clear = True
        for principle in ConstitutionalPrinciple:
            passed, principle_violations = self.check_principle(principle, context)
            if not passed:
                all_clear = False
                violations[principle.value] = principle_violations
        return all_clear, violations


# Global singleton
_constitutional_codex: ConstitutionalCodex = ConstitutionalCodex()


def get_constitutional_codex() -> ConstitutionalCodex:
    return _constitutional_codex


def register_default_covenants(codex: ConstitutionalCodex) -> None:
    """Register default covenants for each principle."""

    # Authority must be explicit
    codex.register_covenant(CovenantRule(
        rule_id="authority_grant_required",
        principle=ConstitutionalPrinciple.AUTHORITY_EXPLICIT,
        description="Operation requires explicit authority grant",
        enforcement_fn=lambda ctx: "authority_grant" in ctx and ctx["authority_grant"] is not None,
    ))

    codex.register_covenant(CovenantRule(
        rule_id="grantor_must_be_non_originating",
        principle=ConstitutionalPrinciple.AUTHORITY_EXPLICIT,
        description="Grantor must be non-originating steward",
        enforcement_fn=lambda ctx: (
            ctx.get("grantor") != ctx.get("originator") if "grantor" in ctx else True
        ),
    ))

    # Evidence must mature
    codex.register_covenant(CovenantRule(
        rule_id="evidence_maturity_minimum",
        principle=ConstitutionalPrinciple.EVIDENCE_MATURITY,
        description="Evidence must reach minimum maturity level",
        enforcement_fn=lambda ctx: (
            ctx.get("evidence_maturity", 0) >= ctx.get("required_maturity", 0)
        ),
    ))

    # Witness required
    codex.register_covenant(CovenantRule(
        rule_id="witness_attestation_required",
        principle=ConstitutionalPrinciple.WITNESS_REQUIRED,
        description="Evidence must be witnessed by non-originating steward",
        enforcement_fn=lambda ctx: (
            "witness_steward" in ctx and ctx["witness_steward"] is not None
        ),
    ))

    # Consent required
    codex.register_covenant(CovenantRule(
        rule_id="consent_granted",
        principle=ConstitutionalPrinciple.CONSENT_NEEDED,
        description="Operation requires consent",
        enforcement_fn=lambda ctx: (
            not ctx.get("consent_required", False) or ctx.get("consent_granted", False)
        ),
    ))

    # Coherence bounded
    codex.register_covenant(CovenantRule(
        rule_id="coherence_sufficient",
        principle=ConstitutionalPrinciple.COHERENCE_BOUNDED,
        description="Operation coherence meets minimum requirement",
        enforcement_fn=lambda ctx: (
            ctx.get("current_coherence", 0.0) >= ctx.get("required_coherence", 0.0)
        ),
    ))

    # Transparency
    codex.register_covenant(CovenantRule(
        rule_id="decision_logged",
        principle=ConstitutionalPrinciple.TRANSPARENCY,
        description="All decisions must be logged",
        enforcement_fn=lambda ctx: (
            "decision_log_id" in ctx and ctx["decision_log_id"] is not None
        ),
    ))


# Initialize default covenants
register_default_covenants(_constitutional_codex)

#!/usr/bin/env python3
"""
Evidence State Decorators — Phase 2.3
Sentinel Constitutional Execution System v11.0

Decorators that enforce SCES framework on functions and components.
Tracks evidence maturity, authority requirements, consent, and coherence
bounds during operation execution.

@evidence_state: Mark a function as evidence-producing and enforce maturity gates
@requires_authority: Enforce authority before execution
@requires_consent: Enforce consent verification before execution
@coherence_bounded: Cap execution at coherence level of inputs
@witness_required: Require witness attestation before execution
"""

from functools import wraps
from typing import Callable, Any, Optional, Dict, List
from datetime import datetime
from enum import Enum

from .sces_volume_2_evidence import EvidenceMaturity, get_evidence_tracker
from .sces_volume_1_authority import get_authority_registry, AuthorityType
from .sces_volume_5_consent import get_consent_registry, get_coherence_tracker
from .sces_volume_4_witness import get_witness_registry
from .sces_volume_8_tracking import get_audit_trail, EventType, AuditEvent


class ExecutionContext:
    """Context for an operation execution with evidence tracking."""

    def __init__(self, function_name: str, evidence_id: Optional[str] = None):
        self.function_name = function_name
        self.evidence_id = evidence_id
        self.required_maturity = EvidenceMaturity.TESTED
        self.requires_authority = False
        self.requires_consent = False
        self.requires_witness = False
        self.coherence_required = 0.5
        self.execution_result = None
        self.execution_error = None
        self.execution_timestamp = None
        self.maturity_after_execution = EvidenceMaturity.EXISTS

    def to_audit_event(self, actor: str, passed: bool) -> AuditEvent:
        """Convert execution context to audit event."""
        return AuditEvent(
            event_id=f"exec_{self.evidence_id}_{self.execution_timestamp}",
            event_type=EventType.OPERATION_EXECUTED if passed else EventType.OPERATION_BLOCKED,
            timestamp=self.execution_timestamp or datetime.utcnow(),
            actor=actor,
            subject=self.evidence_id or self.function_name,
            previous_state={"maturity": EvidenceMaturity.TESTED.value},
            new_state={"maturity": self.maturity_after_execution.value},
            metadata={
                "function": self.function_name,
                "requires_authority": self.requires_authority,
                "requires_consent": self.requires_consent,
                "requires_witness": self.requires_witness,
                "coherence_required": self.coherence_required,
            },
        )


def evidence_state(required_maturity: EvidenceMaturity = EvidenceMaturity.TESTED,
                   evidence_type: str = "function_execution"):
    """
    Decorator: Mark function as evidence-producing with maturity requirements.

    Enforces:
    - Minimum evidence maturity before execution
    - Evidence tracking through execution
    - Audit logging of execution

    Args:
        required_maturity: Minimum EvidenceMaturity required to execute
        evidence_type: Type of evidence produced
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Generate evidence ID for this execution
            evidence_id = f"{func.__module__}:{func.__name__}:{datetime.utcnow().isoformat()}"
            context = ExecutionContext(func.__name__, evidence_id)
            context.required_maturity = required_maturity
            context.execution_timestamp = datetime.utcnow()

            tracker = get_evidence_tracker()

            # Check if evidence exists and has sufficient maturity
            existing = tracker.lookup_evidence(evidence_id)
            if existing and not (existing.maturity.value >= required_maturity.value):
                # Maturity insufficient
                audit_trail = get_audit_trail()
                audit_trail.record_event(context.to_audit_event("system", False))
                raise RuntimeError(
                    f"Evidence maturity insufficient for {func.__name__}: "
                    f"required {required_maturity.value}, have {existing.maturity.value}"
                )

            try:
                # Execute function
                result = func(*args, **kwargs)
                context.execution_result = result
                context.maturity_after_execution = EvidenceMaturity.TESTED

                # Record in audit trail
                audit_trail = get_audit_trail()
                audit_trail.record_event(context.to_audit_event(func.__name__, True))

                return result
            except Exception as e:
                context.execution_error = str(e)
                audit_trail = get_audit_trail()
                audit_trail.record_event(context.to_audit_event(func.__name__, False))
                raise

        return wrapper
    return decorator


def requires_authority(authority_type: AuthorityType, scope: str = "global"):
    """
    Decorator: Enforce authority requirement before execution.

    Args:
        authority_type: Type of authority required (EXECUTIVE, WITNESS, STEWARD, etc.)
        scope: Scope of authority (global, layer, component, session)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self_or_actor, *args, **kwargs) -> Any:
            # Extract actor from self or first argument
            actor = getattr(self_or_actor, 'name', str(self_or_actor))

            registry = get_authority_registry()
            has_auth = registry.has_authority(actor, authority_type, None, scope)

            if not has_auth:
                audit_trail = get_audit_trail()
                audit_trail.record_event(AuditEvent(
                    event_id=f"auth_check_{datetime.utcnow().isoformat()}",
                    event_type=EventType.OPERATION_BLOCKED,
                    actor=actor,
                    subject=func.__name__,
                    metadata={
                        "required_authority": authority_type.value,
                        "scope": scope,
                    },
                ))
                raise PermissionError(
                    f"Actor {actor} lacks {authority_type.value} authority for {func.__name__}"
                )

            return func(self_or_actor, *args, **kwargs)
        return wrapper
    return decorator


def requires_consent(consent_from: str = "steward"):
    """
    Decorator: Enforce consent verification before execution.

    Args:
        consent_from: Who must provide consent ("steward", "witness", "guardian")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            operation_id = f"{func.__name__}_{datetime.utcnow().isoformat()}"
            consent_registry = get_consent_registry()

            # Check if operation has consent
            if not consent_registry.operation_has_consent(operation_id):
                audit_trail = get_audit_trail()
                audit_trail.record_event(AuditEvent(
                    event_id=f"consent_check_{operation_id}",
                    event_type=EventType.OPERATION_BLOCKED,
                    subject=operation_id,
                    metadata={"consent_from": consent_from},
                ))
                raise RuntimeError(
                    f"Consent withheld for {func.__name__} (required from {consent_from})"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


def coherence_bounded(required_coherence: float = 0.5):
    """
    Decorator: Cap execution at coherence level of lowest-coherence input.

    Args:
        required_coherence: Minimum coherence level required (0.0-1.0)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            tracker = get_coherence_tracker()

            # Extract entity IDs from arguments (simple heuristic)
            entity_ids = []
            for arg in args:
                if isinstance(arg, str) and not arg.startswith('_'):
                    entity_ids.append(arg)

            # Compute minimum coherence
            min_coherence = tracker.compute_min_coherence(entity_ids)

            if min_coherence < required_coherence:
                audit_trail = get_audit_trail()
                audit_trail.record_event(AuditEvent(
                    event_id=f"coherence_check_{datetime.utcnow().isoformat()}",
                    event_type=EventType.OPERATION_BLOCKED,
                    subject=func.__name__,
                    metadata={
                        "min_coherence": min_coherence,
                        "required_coherence": required_coherence,
                    },
                ))
                raise RuntimeError(
                    f"Coherence insufficient for {func.__name__}: "
                    f"have {min_coherence}, need {required_coherence}"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


def witness_required(witness_steward: Optional[str] = None):
    """
    Decorator: Require witness attestation before execution.

    Args:
        witness_steward: If specified, require this specific steward as witness
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            witness_registry = get_witness_registry()

            # Check if operation has witness approval
            # In real usage, this would look up attestations for this specific operation
            # For now, we just verify witness registry is accessible
            attestations = witness_registry.get_witness_attestations(
                witness_steward or "default_witness"
            )

            if not attestations:
                audit_trail = get_audit_trail()
                audit_trail.record_event(AuditEvent(
                    event_id=f"witness_check_{datetime.utcnow().isoformat()}",
                    event_type=EventType.OPERATION_BLOCKED,
                    subject=func.__name__,
                    metadata={"required_witness": witness_steward or "any"},
                ))
                raise RuntimeError(
                    f"Witness attestation required for {func.__name__} "
                    f"(required from {witness_steward or 'non-originating steward'})"
                )

            return func(*args, **kwargs)
        return wrapper
    return decorator


def track_evidence_transition(old_maturity: EvidenceMaturity,
                             new_maturity: EvidenceMaturity):
    """
    Decorator: Track evidence maturity transition and record in audit trail.

    Args:
        old_maturity: Previous evidence maturity
        new_maturity: New evidence maturity after operation
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(evidence_id: str, *args, **kwargs) -> Any:
            audit_trail = get_audit_trail()

            # Record transition
            audit_trail.record_event(AuditEvent(
                event_id=f"maturity_transition_{evidence_id}_{datetime.utcnow().isoformat()}",
                event_type=EventType.EVIDENCE_MATURED,
                subject=evidence_id,
                previous_state={"maturity": old_maturity.value},
                new_state={"maturity": new_maturity.value},
            ))

            return func(evidence_id, *args, **kwargs)
        return wrapper
    return decorator

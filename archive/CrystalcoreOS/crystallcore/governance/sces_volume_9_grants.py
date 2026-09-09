#!/usr/bin/env python3
"""
SCES Volume 9: Authority Grant & Delegation Model
Sentinel Constitutional Execution System v11.0

Defines how authority is granted, delegated, and revoked. Authority can be
granted to agents, components, or layers. Delegation creates chains of
responsibility with accountability.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class DelegationStatus(Enum):
    """Status of a delegated authority."""
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    REVOKED = "revoked"


@dataclass
class AuthorityDelegation:
    """Delegation of authority from one entity to another."""
    delegation_id: str
    delegator: str                    # Who is delegating
    delegatee: str                    # Who receives delegation
    authority_type: str               # Type of authority
    scope: str                        # Scope of authority
    status: DelegationStatus = DelegationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    can_sub_delegate: bool = False    # Can delegatee delegate further
    max_sub_delegations: int = 0      # Max sub-delegations allowed
    actual_sub_delegations: int = 0   # Current sub-delegations
    notes: str = ""

    def is_active(self) -> bool:
        if self.status != DelegationStatus.ACTIVE:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

    def can_delegate_further(self) -> bool:
        if not self.can_sub_delegate:
            return False
        return self.actual_sub_delegations < self.max_sub_delegations

    def revoke(self) -> bool:
        if self.status == DelegationStatus.REVOKED:
            return False
        self.status = DelegationStatus.REVOKED
        return True


class DelegationChain:
    """Track chains of delegation for accountability."""

    def __init__(self):
        self._delegations: Dict[str, AuthorityDelegation] = {}
        self._chains: Dict[str, List[str]] = {}  # Original -> [delegation_ids]

    def register_delegation(self, delegation: AuthorityDelegation) -> bool:
        if delegation.delegation_id in self._delegations:
            return False
        self._delegations[delegation.delegation_id] = delegation
        self._chains.setdefault(delegation.delegator, []).append(
            delegation.delegation_id)
        return True

    def get_delegation_chain(self, original_authority_holder: str) -> List[AuthorityDelegation]:
        """Get full delegation chain from original authority holder."""
        delegation_ids = self._chains.get(original_authority_holder, [])
        return [self._delegations[did] for did in delegation_ids]

    def get_active_delegations(self, delegatee: str) -> List[AuthorityDelegation]:
        """Get all active delegations for a delegatee."""
        return [d for d in self._delegations.values()
                if d.delegatee == delegatee and d.is_active()]

    def trace_authority_origin(self, current_holder: str) -> List[str]:
        """Trace back to original authority holder."""
        chain = [current_holder]
        while True:
            found_parent = False
            for d in self._delegations.values():
                if d.delegatee == chain[-1] and d.is_active():
                    chain.append(d.delegator)
                    found_parent = True
                    break
            if not found_parent:
                break
        return chain

    def revoke_delegation(self, delegation_id: str) -> bool:
        """Revoke a delegation and all sub-delegations."""
        delegation = self._delegations.get(delegation_id)
        if not delegation:
            return False

        if not delegation.revoke():
            return False

        # Revoke all sub-delegations
        for d in self._delegations.values():
            if d.delegator == delegation.delegatee:
                d.revoke()

        return True


# Global singleton
_delegation_chain: Optional[DelegationChain] = None


def get_delegation_chain() -> DelegationChain:
    global _delegation_chain
    if _delegation_chain is None:
        _delegation_chain = DelegationChain()
    return _delegation_chain

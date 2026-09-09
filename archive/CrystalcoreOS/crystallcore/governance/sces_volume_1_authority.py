#!/usr/bin/env python3
"""
SCES Volume 1: Authority Model
Sentinel Constitutional Execution System v11.0

Foundational Principle: Authority is never inferred. Authority must be
explicitly granted by a non-originating steward with witness discipline.

This volume defines:
- Authority grant types and mechanisms
- Grant lifecycle (creation, verification, confirmation, revocation)
- Authority scope and delegation constraints
- Non-originating steward requirements
- Explicit vs. implicit authority distinctions
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum


class AuthorityType(Enum):
    """Types of authority that can be granted."""
    EXECUTIVE = "executive"      # Can execute operations
    WITNESS = "witness"          # Can verify and validate
    STEWARD = "steward"          # Can grant authority
    GUARDIAN = "guardian"        # Can enforce constraints
    CREATOR = "creator"          # Can initiate new components
    VISIONARY = "visionary"      # Can propose changes


class AuthorityScope(Enum):
    """Scope of granted authority."""
    GLOBAL = "global"            # Applies everywhere
    LAYER = "layer"              # Limited to a specific layer
    COMPONENT = "component"      # Limited to a component
    SESSION = "session"          # Limited to a session
    TEMPORAL = "temporal"         # Time-bounded


@dataclass
class AuthorityGrant:
    """An explicit authority grant from a steward to an agent/component."""
    grant_id: str
    grantor: str                  # Non-originating steward who grants
    grantee: str                  # Agent/component receiving authority
    authority_type: AuthorityType
    scope: AuthorityScope
    scope_target: str             # What the scope is limited to
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    evidence_maturity: str = "Verified_Local"  # Min. maturity required
    witness_signature: Optional[str] = None    # Witness verification hash
    witness_steward: Optional[str] = None      # Witness steward name
    metadata: Dict[str, Any] = field(default_factory=dict)
    active: bool = True

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def is_valid(self) -> bool:
        return self.active and not self.is_expired()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['authority_type'] = self.authority_type.value
        d['scope'] = self.scope.value
        d['created_at'] = self.created_at.isoformat()
        d['expires_at'] = self.expires_at.isoformat() if self.expires_at else None
        return d


class AuthorityRegistry:
    """Central registry of all authority grants in the system."""

    def __init__(self):
        self._grants: Dict[str, AuthorityGrant] = {}
        self._grantee_index: Dict[str, List[str]] = {}  # grantee -> [grant_ids]
        self._grantor_index: Dict[str, List[str]] = {}  # grantor -> [grant_ids]

    def register_grant(self, grant: AuthorityGrant) -> bool:
        """Register a new authority grant. Returns True if successful."""
        if grant.grant_id in self._grants:
            return False
        if not grant.witness_signature or not grant.witness_steward:
            return False  # Grant must be witnessed
        self._grants[grant.grant_id] = grant
        self._grantee_index.setdefault(grant.grantee, []).append(grant.grant_id)
        self._grantor_index.setdefault(grant.grantor, []).append(grant.grant_id)
        return True

    def revoke_grant(self, grant_id: str, revoker: str) -> bool:
        """Revoke a grant. Only the grantor can revoke."""
        if grant_id not in self._grants:
            return False
        grant = self._grants[grant_id]
        if grant.grantor != revoker:
            return False
        grant.active = False
        return True

    def lookup_grant(self, grant_id: str) -> Optional[AuthorityGrant]:
        """Look up a grant by ID."""
        return self._grants.get(grant_id)

    def lookup_grantee_authority(self, grantee: str) -> List[AuthorityGrant]:
        """Get all active authority grants for a grantee."""
        grant_ids = self._grantee_index.get(grantee, [])
        return [g for gid in grant_ids if (g := self._grants.get(gid)) and g.is_valid()]

    def lookup_grantor_authority(self, grantor: str) -> List[AuthorityGrant]:
        """Get all active authority grants granted by a steward."""
        grant_ids = self._grantor_index.get(grantor, [])
        return [g for gid in grant_ids if (g := self._grants.get(gid)) and g.is_valid()]

    def has_authority(self, agent: str, authority_type: AuthorityType,
                      scope: AuthorityScope, scope_target: str) -> bool:
        """Check if an agent has a specific authority."""
        grants = self.lookup_grantee_authority(agent)
        for grant in grants:
            if grant.authority_type != authority_type:
                continue
            if grant.scope == AuthorityScope.GLOBAL:
                return True
            if grant.scope == scope and grant.scope_target == scope_target:
                return True
        return False

    def all_grants(self) -> List[AuthorityGrant]:
        """Return all grants (including revoked)."""
        return list(self._grants.values())


# Global singleton registry
_authority_registry: Optional[AuthorityRegistry] = None


def get_authority_registry() -> AuthorityRegistry:
    global _authority_registry
    if _authority_registry is None:
        _authority_registry = AuthorityRegistry()
    return _authority_registry

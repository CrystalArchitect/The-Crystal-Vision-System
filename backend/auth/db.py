"""
Database models for authentication persistence
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import Column, String, Text, DateTime, Boolean, ARRAY, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

from ..database import Base


class StewardRecord(Base):
    """Persisted steward profile with OAuth bindings"""

    __tablename__ = "stewards"

    steward_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)

    # OAuth provider binding
    auth_provider = Column(String(50), nullable=False)  # e.g., "google", "apple", "microsoft"
    provider_subject_id = Column(String(500), nullable=False)  # sub claim from OAuth provider
    __table_args__ = (UniqueConstraint("auth_provider", "provider_subject_id", name="uq_auth_provider_subject"),)

    # Governance role and scope
    role = Column(String(50), nullable=False)  # e.g., "policy_approver", "infrastructure_maintainer"
    approval_scope = Column(ARRAY(String), nullable=False, default=[])  # List of decision types this steward can approve

    # Biometric enrollment
    biometric_enrolled = Column(Boolean, default=False)
    voice_profile_id = Column(String(500), nullable=True)  # Reference to voice recognition model

    # Audit trail
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    last_active = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    oauth_sessions = relationship("OAuthSessionRecord", back_populates="steward", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshTokenRecord", back_populates="steward", cascade="all, delete-orphan")

    def to_profile(self):
        """Convert to StewardProfile domain model"""
        from .models import StewardProfile, AuthProvider, StewardRole

        return StewardProfile(
            steward_id=self.steward_id,
            email=self.email,
            name=self.name,
            provider=AuthProvider(self.auth_provider),
            provider_subject_id=self.provider_subject_id,
            role=StewardRole(self.role),
            approval_scope=self.approval_scope or [],
            biometric_enrolled=self.biometric_enrolled,
            voice_profile_id=self.voice_profile_id,
            created_at=self.created_at,
            last_active=self.last_active,
        )


class OAuthSessionRecord(Base):
    """In-flight OAuth authorization session"""

    __tablename__ = "oauth_sessions"

    session_id = Column(String(255), primary_key=True)  # state parameter
    steward_id = Column(PG_UUID(as_uuid=True), ForeignKey("stewards.steward_id"), nullable=True, index=True)
    auth_provider = Column(String(50), nullable=False)  # e.g., "google", "apple", "microsoft"
    code_verifier = Column(Text, nullable=True)  # PKCE code verifier for mobile
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    steward = relationship("StewardRecord", back_populates="oauth_sessions")

    # Index for cleanup queries
    __table_args__ = (Index("ix_oauth_sessions_expires_at", "expires_at"),)


class RefreshTokenRecord(Base):
    """Persisted refresh tokens for token rotation"""

    __tablename__ = "refresh_tokens"

    token_id = Column(String(255), primary_key=True)  # hash of the token
    steward_id = Column(PG_UUID(as_uuid=True), ForeignKey("stewards.steward_id"), nullable=False, index=True)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    steward = relationship("StewardRecord", back_populates="refresh_tokens")

    # Indices for queries
    __table_args__ = (
        Index("ix_refresh_tokens_expires_at", "expires_at"),
        Index("ix_refresh_tokens_is_revoked", "is_revoked"),
    )


class AuditLogRecord(Base):
    """Audit trail for steward actions and decisions"""

    __tablename__ = "audit_log"

    event_id = Column(String(255), primary_key=True, default=lambda: str(uuid4()))
    steward_id = Column(PG_UUID(as_uuid=True), ForeignKey("stewards.steward_id"), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)  # e.g., "decision_approved", "login", "voice_auth"
    event_category = Column(String(100), nullable=False)  # e.g., "governance", "authentication", "audit"
    decision_id = Column(String(500), nullable=True)  # Reference to approved decision (if applicable)
    outcome = Column(String(50), nullable=False)  # "success", "failure", "partial"
    details = Column(Text, nullable=True)  # JSON-encoded event details
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Indices for querying
    __table_args__ = (
        Index("ix_audit_log_steward_created", "steward_id", "created_at"),
        Index("ix_audit_log_event_type_created", "event_type", "created_at"),
    )

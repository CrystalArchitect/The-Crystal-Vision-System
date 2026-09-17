"""
Data access layer for steward and OAuth session persistence
"""

import hashlib
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import StewardProfile, AuthProvider, StewardRole
from .db import StewardRecord, OAuthSessionRecord, RefreshTokenRecord, AuditLogRecord

logger = logging.getLogger(__name__)


class StewardRepository:
    """Database operations for steward profiles"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, steward_id: UUID) -> Optional[StewardProfile]:
        """Fetch steward profile by ID"""
        record = self.db.query(StewardRecord).filter(StewardRecord.steward_id == steward_id).first()
        return record.to_profile() if record else None

    def get_by_email(self, email: str) -> Optional[StewardProfile]:
        """Fetch steward profile by email"""
        record = self.db.query(StewardRecord).filter(StewardRecord.email == email).first()
        return record.to_profile() if record else None

    def get_by_oauth(self, provider: AuthProvider, provider_subject_id: str) -> Optional[StewardProfile]:
        """Fetch steward profile by OAuth provider and subject ID"""
        record = (
            self.db.query(StewardRecord)
            .filter(
                StewardRecord.auth_provider == provider.value,
                StewardRecord.provider_subject_id == provider_subject_id,
            )
            .first()
        )
        return record.to_profile() if record else None

    def create(
        self,
        email: str,
        name: str,
        provider: AuthProvider,
        provider_subject_id: str,
        role: StewardRole,
        approval_scope: list[str],
        biometric_enrolled: bool = False,
        voice_profile_id: Optional[str] = None,
    ) -> StewardProfile:
        """Create a new steward profile"""
        steward_id = UUID
        record = StewardRecord(
            steward_id=steward_id,
            email=email,
            name=name,
            auth_provider=provider.value,
            provider_subject_id=provider_subject_id,
            role=role.value,
            approval_scope=approval_scope,
            biometric_enrolled=biometric_enrolled,
            voice_profile_id=voice_profile_id,
        )
        try:
            self.db.add(record)
            self.db.commit()
            logger.info(f"Created steward {steward_id} with provider {provider.value}")
            return record.to_profile()
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Failed to create steward: {e}")
            raise

    def update_last_active(self, steward_id: UUID) -> bool:
        """Update steward's last_active timestamp"""
        record = self.db.query(StewardRecord).filter(StewardRecord.steward_id == steward_id).first()
        if not record:
            return False

        record.last_active = datetime.now(timezone.utc)
        record.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        return True

    def enroll_biometric(self, steward_id: UUID, voice_profile_id: Optional[str] = None) -> bool:
        """Enroll steward in biometric authentication"""
        record = self.db.query(StewardRecord).filter(StewardRecord.steward_id == steward_id).first()
        if not record:
            return False

        record.biometric_enrolled = True
        if voice_profile_id:
            record.voice_profile_id = voice_profile_id
        record.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        return True


class OAuthSessionRepository:
    """Database operations for OAuth sessions"""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        session_id: str,
        provider: AuthProvider,
        expires_in_seconds: int = 600,  # 10 minutes default
        code_verifier: Optional[str] = None,
        steward_id: Optional[UUID] = None,
    ) -> None:
        """Create a new OAuth session"""
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)

        record = OAuthSessionRecord(
            session_id=session_id,
            auth_provider=provider.value,
            code_verifier=code_verifier,
            expires_at=expires_at,
            steward_id=steward_id,
        )
        self.db.add(record)
        self.db.commit()
        logger.info(f"Created OAuth session {session_id} for provider {provider.value}")

    def get(self, session_id: str) -> Optional[OAuthSessionRecord]:
        """Fetch OAuth session by state parameter"""
        record = self.db.query(OAuthSessionRecord).filter(OAuthSessionRecord.session_id == session_id).first()

        # Check expiration
        if record and datetime.now(timezone.utc) > record.expires_at:
            self.db.delete(record)
            self.db.commit()
            logger.info(f"Expired OAuth session {session_id}")
            return None

        return record

    def delete(self, session_id: str) -> bool:
        """Delete an OAuth session (e.g., after code exchange)"""
        record = self.db.query(OAuthSessionRecord).filter(OAuthSessionRecord.session_id == session_id).first()
        if not record:
            return False

        self.db.delete(record)
        self.db.commit()
        return True

    def cleanup_expired(self) -> int:
        """Delete all expired OAuth sessions"""
        count = (
            self.db.query(OAuthSessionRecord)
            .filter(OAuthSessionRecord.expires_at < datetime.now(timezone.utc))
            .delete()
        )
        self.db.commit()
        logger.info(f"Cleaned up {count} expired OAuth sessions")
        return count


class RefreshTokenRepository:
    """Database operations for refresh tokens"""

    def __init__(self, db: Session):
        self.db = db

    def _hash_token(self, token: str) -> str:
        """Hash token for storage (never store plain tokens)"""
        return hashlib.sha256(token.encode()).hexdigest()

    def store(
        self,
        token: str,
        steward_id: UUID,
        expires_in_days: int = 30,
    ) -> str:
        """Store a refresh token and return its ID"""
        token_id = self._hash_token(token)
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        record = RefreshTokenRecord(
            token_id=token_id,
            steward_id=steward_id,
            expires_at=expires_at,
        )
        self.db.add(record)
        self.db.commit()
        return token_id

    def validate(self, token: str) -> Optional[UUID]:
        """Validate refresh token and return steward ID if valid"""
        token_id = self._hash_token(token)
        record = self.db.query(RefreshTokenRecord).filter(RefreshTokenRecord.token_id == token_id).first()

        if not record:
            return None

        # Check expiration
        if datetime.now(timezone.utc) > record.expires_at:
            self.db.delete(record)
            self.db.commit()
            return None

        # Check revocation
        if record.is_revoked:
            return None

        # Update last_used_at
        record.last_used_at = datetime.now(timezone.utc)
        self.db.commit()

        return record.steward_id

    def revoke(self, token: str) -> bool:
        """Revoke a refresh token"""
        token_id = self._hash_token(token)
        record = self.db.query(RefreshTokenRecord).filter(RefreshTokenRecord.token_id == token_id).first()
        if not record:
            return False

        record.is_revoked = True
        self.db.commit()
        return True

    def cleanup_expired(self) -> int:
        """Delete all expired refresh tokens"""
        count = (
            self.db.query(RefreshTokenRecord)
            .filter(RefreshTokenRecord.expires_at < datetime.now(timezone.utc))
            .delete()
        )
        self.db.commit()
        logger.info(f"Cleaned up {count} expired refresh tokens")
        return count


class AuditLogRepository:
    """Database operations for audit logging"""

    def __init__(self, db: Session):
        self.db = db

    def log_event(
        self,
        steward_id: UUID,
        event_type: str,
        event_category: str,
        outcome: str,
        decision_id: Optional[str] = None,
        details: Optional[str] = None,
    ) -> str:
        """Log an authentication or governance event"""
        record = AuditLogRecord(
            steward_id=steward_id,
            event_type=event_type,
            event_category=event_category,
            decision_id=decision_id,
            outcome=outcome,
            details=details,
        )
        self.db.add(record)
        self.db.commit()
        logger.info(f"Logged audit event {record.event_id} for steward {steward_id}: {event_type}/{outcome}")
        return record.event_id

    def get_steward_events(
        self,
        steward_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """Fetch audit events for a steward"""
        records = (
            self.db.query(AuditLogRecord)
            .filter(AuditLogRecord.steward_id == steward_id)
            .order_by(AuditLogRecord.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [
            {
                "event_id": r.event_id,
                "event_type": r.event_type,
                "event_category": r.event_category,
                "outcome": r.outcome,
                "decision_id": r.decision_id,
                "created_at": r.created_at.isoformat(),
                "details": r.details,
            }
            for r in records
        ]

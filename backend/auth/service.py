"""
High-level authentication service orchestrating OAuth, tokens, and database operations
"""

import logging
from typing import Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from .models import AuthProvider, StewardProfile, StewardRole, TokenResponse
from .oauth import OAuthManager
from .token import (
    generate_access_token,
    generate_refresh_token,
    validate_token,
    TokenPayload,
)
from .repository import (
    StewardRepository,
    OAuthSessionRepository,
    RefreshTokenRepository,
    AuditLogRepository,
)

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Orchestrates authentication flows: OAuth, enrollment, token management"""

    def __init__(
        self,
        db: Session,
        oauth_manager: OAuthManager,
    ):
        self.db = db
        self.oauth_manager = oauth_manager
        self.steward_repo = StewardRepository(db)
        self.oauth_session_repo = OAuthSessionRepository(db)
        self.refresh_token_repo = RefreshTokenRepository(db)
        self.audit_repo = AuditLogRepository(db)

    async def start_oauth_flow(
        self,
        provider: AuthProvider,
        mobile: bool = False,
    ) -> Tuple[str, str]:
        """
        Initiate OAuth2 authorization flow.

        Args:
            provider: OAuth provider (google, apple, microsoft)
            mobile: Whether to use PKCE flow (for mobile)

        Returns:
            Tuple of (authorization_url, state_parameter)
        """
        auth_url, state_with_verifier = self.oauth_manager.get_authorization_url(provider, mobile=mobile)

        # Extract verifier if mobile
        code_verifier = None
        state = state_with_verifier
        if mobile and "|" in state_with_verifier:
            state, code_verifier = state_with_verifier.split("|", 1)

        # Store OAuth session for later validation
        self.oauth_session_repo.create(
            session_id=state,
            provider=provider,
            code_verifier=code_verifier,
        )

        logger.info(f"Started OAuth flow for provider {provider.value}, mobile={mobile}")
        return auth_url, state

    async def complete_oauth_flow(
        self,
        provider: AuthProvider,
        code: str,
        state: str,
    ) -> Tuple[Optional[StewardProfile], Optional[dict]]:
        """
        Complete OAuth2 authorization code exchange and fetch user info.

        Args:
            provider: OAuth provider
            code: Authorization code from provider
            state: State parameter from callback

        Returns:
            Tuple of (existing_steward_profile or None, normalized_user_info)
        """
        # Validate OAuth session
        oauth_session = self.oauth_session_repo.get(state)
        if not oauth_session:
            logger.warning(f"Invalid or expired OAuth session: {state}")
            return None, None

        try:
            # Exchange code for token
            token_response = await self.oauth_manager.exchange_code_for_token(
                provider=provider,
                code=code,
                state=state if not oauth_session.code_verifier else f"{state}|{oauth_session.code_verifier}",
            )

            # Fetch user info
            access_token = token_response.get("access_token")
            user_info = await self.oauth_manager.get_userinfo(provider, access_token)

            # Look up existing steward
            existing_steward = self.steward_repo.get_by_oauth(
                provider=provider,
                provider_subject_id=user_info.get("sub"),
            )

            # Clean up OAuth session
            self.oauth_session_repo.delete(state)

            if existing_steward:
                self.steward_repo.update_last_active(existing_steward.steward_id)
                self.audit_repo.log_event(
                    steward_id=existing_steward.steward_id,
                    event_type="oauth_complete",
                    event_category="authentication",
                    outcome="success",
                    details=f"provider={provider.value}",
                )

            return existing_steward, user_info

        except Exception as e:
            logger.error(f"OAuth flow failed: {e}")
            self.oauth_session_repo.delete(state)
            return None, None

    def enroll_steward(
        self,
        email: str,
        name: str,
        provider: AuthProvider,
        provider_subject_id: str,
        role: StewardRole,
        approval_scope: list[str],
        voice_profile_id: Optional[str] = None,
    ) -> Optional[StewardProfile]:
        """
        Enroll a new steward after OAuth authentication.

        Args:
            email: Steward email (from OAuth provider)
            name: Steward display name
            provider: OAuth provider
            provider_subject_id: Subject ID from OAuth (sub claim)
            role: Steward role
            approval_scope: List of decision types they can approve
            voice_profile_id: Optional voice profile ID for voice recognition

        Returns:
            Created StewardProfile or None on failure
        """
        try:
            steward = self.steward_repo.create(
                email=email,
                name=name,
                provider=provider,
                provider_subject_id=provider_subject_id,
                role=role,
                approval_scope=approval_scope,
                voice_profile_id=voice_profile_id,
            )

            self.audit_repo.log_event(
                steward_id=steward.steward_id,
                event_type="enrollment",
                event_category="authentication",
                outcome="success",
                details=f"role={role.value},provider={provider.value}",
            )

            logger.info(f"Enrolled steward {steward.steward_id} with role {role.value}")
            return steward

        except Exception as e:
            logger.error(f"Failed to enroll steward: {e}")
            return None

    def create_tokens(
        self,
        steward: StewardProfile,
    ) -> TokenResponse:
        """
        Generate access and refresh tokens for authenticated steward.

        Args:
            steward: Authenticated StewardProfile

        Returns:
            TokenResponse with access_token and refresh_token
        """
        # Generate access token
        access_token = generate_access_token(
            steward_id=steward.steward_id,
            email=steward.email,
            name=steward.name,
            role=steward.role.value,
            approval_scope=steward.approval_scope,
        )

        # Generate refresh token
        refresh_token = generate_refresh_token(steward_id=steward.steward_id)

        # Store refresh token in database
        self.refresh_token_repo.store(refresh_token, steward.steward_id)

        self.audit_repo.log_event(
            steward_id=steward.steward_id,
            event_type="tokens_created",
            event_category="authentication",
            outcome="success",
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=3600,
        )

    def validate_access_token(self, token: str) -> Optional[TokenPayload]:
        """
        Validate an access token and return payload.

        Args:
            token: JWT access token

        Returns:
            TokenPayload if valid, None otherwise
        """
        return validate_token(token, expected_token_type="access")

    def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """
        Exchange a refresh token for a new access token.

        Args:
            refresh_token: JWT refresh token

        Returns:
            TokenResponse with new access_token, or None if refresh token is invalid
        """
        # Validate refresh token
        steward_id = self.refresh_token_repo.validate(refresh_token)
        if not steward_id:
            logger.warning("Invalid or expired refresh token")
            return None

        # Fetch steward profile
        steward = self.steward_repo.get_by_id(steward_id)
        if not steward:
            logger.error(f"Steward {steward_id} not found")
            return None

        # Generate new access token (refresh token stays the same)
        access_token = generate_access_token(
            steward_id=steward.steward_id,
            email=steward.email,
            name=steward.name,
            role=steward.role.value,
            approval_scope=steward.approval_scope,
        )

        self.audit_repo.log_event(
            steward_id=steward.steward_id,
            event_type="token_refreshed",
            event_category="authentication",
            outcome="success",
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,  # Return same refresh token
            token_type="Bearer",
            expires_in=3600,
        )

    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """
        Revoke a refresh token (logout).

        Args:
            refresh_token: JWT refresh token to revoke

        Returns:
            True if revocation succeeded, False otherwise
        """
        steward_id = self.refresh_token_repo.validate(refresh_token)
        if steward_id:
            self.audit_repo.log_event(
                steward_id=steward_id,
                event_type="logout",
                event_category="authentication",
                outcome="success",
            )

        return self.refresh_token_repo.revoke(refresh_token)

    def cleanup_expired_sessions(self) -> dict:
        """Clean up expired OAuth sessions and refresh tokens"""
        oauth_count = self.oauth_session_repo.cleanup_expired()
        token_count = self.refresh_token_repo.cleanup_expired()

        return {
            "expired_oauth_sessions": oauth_count,
            "expired_refresh_tokens": token_count,
        }

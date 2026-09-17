"""
Authentication endpoints for Celestial Portal
OAuth2 flow, token management, and steward enrollment
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from backend.database import get_db
from .service import AuthenticationService
from .models import AuthProvider, StewardRole, TokenResponse, StewardProfile
from .oauth import get_oauth_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1/auth", tags=["authentication"])


# ============================================================================
# Request/Response Models
# ============================================================================

class AuthorizeRequest(BaseModel):
    """Initiate OAuth authorization flow"""
    provider: str  # 'google', 'apple', 'microsoft'
    mobile: bool = False  # Use PKCE for mobile


class AuthorizeResponse(BaseModel):
    """OAuth authorization URL and state parameter"""
    authorization_url: str
    state: str


class CallbackRequest(BaseModel):
    """Complete OAuth callback"""
    provider: str
    code: str
    state: str


class CallbackResponse(BaseModel):
    """OAuth callback response with enrollment status"""
    existing_steward: Optional[StewardProfile] = None
    user_info: dict  # User data from OAuth provider
    requires_enrollment: bool  # True if new user, False if existing


class EnrollmentRequest(BaseModel):
    """Enroll a new steward"""
    email: EmailStr
    name: str
    provider: str
    provider_subject_id: str
    role: str  # 'policy_approver', 'infrastructure_maintainer', etc.
    approval_scope: list[str]  # Decision types this steward can approve
    voice_profile_id: Optional[str] = None


class EnrollmentResponse(BaseModel):
    """Enrollment result with tokens"""
    steward_id: UUID
    email: str
    name: str
    role: str
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh access token"""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """New access token"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class LogoutRequest(BaseModel):
    """Logout and revoke refresh token"""
    refresh_token: str


class LogoutResponse(BaseModel):
    """Logout confirmation"""
    status: str = "logged_out"


# ============================================================================
# Dependency: Get Authentication Service
# ============================================================================

def get_auth_service(db: Session = Depends(get_db)) -> AuthenticationService:
    """Dependency to get AuthenticationService instance"""
    oauth_manager = get_oauth_manager()
    return AuthenticationService(db=db, oauth_manager=oauth_manager)


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/authorize", response_model=AuthorizeResponse)
async def authorize(
    request: AuthorizeRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> AuthorizeResponse:
    """
    Initiate OAuth2 authorization flow.
    Returns authorization URL and state parameter for client to redirect to.
    """
    try:
        # Validate provider
        try:
            provider = AuthProvider(request.provider.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Must be one of: {', '.join([p.value for p in AuthProvider])}"
            )

        auth_url, state = await auth_service.start_oauth_flow(
            provider=provider,
            mobile=request.mobile
        )

        return AuthorizeResponse(
            authorization_url=auth_url,
            state=state
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authorization flow failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to start authorization flow")


@router.post("/callback", response_model=CallbackResponse)
async def callback(
    request: CallbackRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> CallbackResponse:
    """
    Complete OAuth2 authorization callback.
    Exchange authorization code for tokens and fetch user info.
    """
    try:
        # Validate provider
        try:
            provider = AuthProvider(request.provider.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid provider. Must be one of: {', '.join([p.value for p in AuthProvider])}"
            )

        existing_steward, user_info = await auth_service.complete_oauth_flow(
            provider=provider,
            code=request.code,
            state=request.state
        )

        if not user_info:
            raise HTTPException(
                status_code=400,
                detail="OAuth callback failed or expired"
            )

        return CallbackResponse(
            existing_steward=existing_steward,
            user_info=user_info,
            requires_enrollment=existing_steward is None
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OAuth callback failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to complete authorization")


@router.post("/enroll", response_model=EnrollmentResponse)
async def enroll(
    request: EnrollmentRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> EnrollmentResponse:
    """
    Enroll a new steward after OAuth authentication.
    Creates steward profile and issues access/refresh tokens.
    """
    try:
        # Validate provider and role
        try:
            provider = AuthProvider(request.provider.lower())
            role = StewardRole(request.role.lower())
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid {str(e)}")

        # Enroll steward
        steward = auth_service.enroll_steward(
            email=request.email,
            name=request.name,
            provider=provider,
            provider_subject_id=request.provider_subject_id,
            role=role,
            approval_scope=request.approval_scope,
            voice_profile_id=request.voice_profile_id
        )

        if not steward:
            raise HTTPException(status_code=400, detail="Failed to enroll steward")

        # Create tokens
        tokens = auth_service.create_tokens(steward)

        return EnrollmentResponse(
            steward_id=steward.steward_id,
            email=steward.email,
            name=steward.name,
            role=steward.role.value,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            expires_in=tokens.expires_in
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Enrollment failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to enroll steward")


@router.post("/token", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> RefreshTokenResponse:
    """
    Exchange refresh token for new access token.
    Used by clients to maintain authentication without re-authenticating.
    """
    try:
        tokens = auth_service.refresh_access_token(request.refresh_token)

        if not tokens:
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        return RefreshTokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            expires_in=tokens.expires_in
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh token")


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    request: LogoutRequest,
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> LogoutResponse:
    """
    Logout and revoke refresh token.
    Invalidates the refresh token, forcing re-authentication.
    """
    try:
        success = auth_service.revoke_refresh_token(request.refresh_token)

        if not success:
            logger.warning("Attempted logout with invalid refresh token")
            # Don't fail on logout — token may already be revoked

        return LogoutResponse(status="logged_out")

    except Exception as e:
        logger.error(f"Logout failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to logout")


@router.post("/cleanup")
async def cleanup_expired_sessions(
    auth_service: AuthenticationService = Depends(get_auth_service)
) -> dict:
    """
    Maintenance endpoint to clean up expired OAuth sessions and refresh tokens.
    Should be called periodically (e.g., every hour via scheduled task).
    """
    try:
        result = auth_service.cleanup_expired_sessions()
        return result
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to cleanup expired sessions")

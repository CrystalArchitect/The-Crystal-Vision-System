"""
Authentication and authorization system for Celestial Portal
"""

from .models import (
    AuthProvider,
    StewardRole,
    OAuthProvider,
    StewardProfile,
    OAuthSession,
    TokenResponse,
    MobileAuthRequest,
    EmailAuthRequest,
    EnrollmentRequest,
)
from .oauth import OAuthManager, get_oauth_manager
from .token import (
    TokenPayload,
    generate_access_token,
    generate_refresh_token,
    validate_token,
    extract_steward_id_from_token,
    set_jwt_secret,
    set_jwt_algorithm,
    ACCESS_TOKEN_EXPIRY_MINUTES,
    REFRESH_TOKEN_EXPIRY_DAYS,
)

__all__ = [
    # Models
    "AuthProvider",
    "StewardRole",
    "OAuthProvider",
    "StewardProfile",
    "OAuthSession",
    "TokenResponse",
    "MobileAuthRequest",
    "EmailAuthRequest",
    "EnrollmentRequest",
    # OAuth
    "OAuthManager",
    "get_oauth_manager",
    # Token
    "TokenPayload",
    "generate_access_token",
    "generate_refresh_token",
    "validate_token",
    "extract_steward_id_from_token",
    "set_jwt_secret",
    "set_jwt_algorithm",
    "ACCESS_TOKEN_EXPIRY_MINUTES",
    "REFRESH_TOKEN_EXPIRY_DAYS",
]

"""
Authentication data models for Celestial Portal
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID


class AuthProvider(str, Enum):
    """Supported OAuth providers"""
    GOOGLE = "google"
    APPLE = "apple"
    MICROSOFT = "microsoft"
    EMAIL = "email"
    MOBILE_BIOMETRIC = "mobile_biometric"


class StewardRole(str, Enum):
    """Steward roles for decision approval"""
    POLICY_APPROVER = "policy_approver"
    INFRASTRUCTURE_MAINTAINER = "infrastructure_maintainer"
    COMPLIANCE_REVIEWER = "compliance_reviewer"
    ADMIN = "admin"


@dataclass
class OAuthProvider:
    """OAuth provider configuration"""
    name: AuthProvider
    client_id: str
    client_secret: str
    redirect_uri: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str


@dataclass
class StewardProfile:
    """Steward profile after authentication"""
    steward_id: UUID
    email: str
    name: str
    provider: AuthProvider
    provider_subject_id: str  # Sub claim from OAuth
    role: StewardRole
    approval_scope: list[str]  # Decision types this steward can approve (e.g., ["ADM-001", "ADM-002"])
    biometric_enrolled: bool
    voice_profile_id: Optional[str]  # Reference to voice recognition model
    created_at: datetime
    last_active: datetime


@dataclass
class OAuthSession:
    """OAuth session for authorization code flow"""
    session_id: str  # State parameter
    provider: AuthProvider
    created_at: datetime
    expires_at: datetime
    code_verifier: Optional[str]  # PKCE code verifier for mobile


@dataclass
class TokenResponse:
    """JWT token response"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None


@dataclass
class MobileAuthRequest:
    """Mobile device biometric auth request"""
    device_id: str
    biometric_type: str  # "face_id", "fingerprint", "pin"
    nonce: str  # Cryptographic challenge
    steward_email: str  # Optional: for device without cached steward


@dataclass
class EmailAuthRequest:
    """Email/password authentication request"""
    email: str
    password: str


@dataclass
class EnrollmentRequest:
    """Steward enrollment after OAuth auth"""
    name: str
    role: StewardRole
    approval_scope: list[str]
    voice_profile_sample: Optional[bytes] = None  # Optional audio for voice recognition calibration

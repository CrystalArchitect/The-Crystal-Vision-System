"""
JWT token generation and validation for authenticated stewards
"""

import jwt
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from uuid import UUID

logger = logging.getLogger(__name__)

# Token configuration
ACCESS_TOKEN_EXPIRY_MINUTES = 60
REFRESH_TOKEN_EXPIRY_DAYS = 30
ALGORITHM = "HS256"

# These should come from environment variables in production
_jwt_secret: Optional[str] = None
_jwt_algorithm: str = ALGORITHM


def set_jwt_secret(secret: str):
    """Configure the JWT secret key (call at app startup)"""
    global _jwt_secret
    _jwt_secret = secret


def set_jwt_algorithm(algorithm: str):
    """Configure the JWT algorithm (default: HS256)"""
    global _jwt_algorithm
    _jwt_algorithm = algorithm


class TokenPayload:
    """Validated JWT token payload"""

    def __init__(
        self,
        steward_id: UUID,
        email: str,
        name: str,
        role: str,
        approval_scope: list[str],
        token_type: str,
        exp: int,
        iat: int,
    ):
        self.steward_id = steward_id
        self.email = email
        self.name = name
        self.role = role
        self.approval_scope = approval_scope
        self.token_type = token_type
        self.exp = exp
        self.iat = iat

    def is_expired(self) -> bool:
        """Check if token has expired"""
        return datetime.now(timezone.utc).timestamp() > self.exp


def generate_access_token(
    steward_id: UUID,
    email: str,
    name: str,
    role: str,
    approval_scope: list[str],
    expires_in_minutes: int = ACCESS_TOKEN_EXPIRY_MINUTES,
) -> str:
    """
    Generate a JWT access token for a steward.

    Args:
        steward_id: UUID of the authenticated steward
        email: Steward email
        name: Steward display name
        role: Steward role (e.g., "policy_approver")
        approval_scope: List of decision types this steward can approve
        expires_in_minutes: Token expiration time in minutes

    Returns:
        Encoded JWT token string
    """
    if not _jwt_secret:
        raise RuntimeError("JWT secret not configured. Call set_jwt_secret() at app startup.")

    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=expires_in_minutes)

    payload = {
        "steward_id": str(steward_id),
        "email": email,
        "name": name,
        "role": role,
        "approval_scope": approval_scope,
        "token_type": "access",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    token = jwt.encode(payload, _jwt_secret, algorithm=_jwt_algorithm)
    return token


def generate_refresh_token(
    steward_id: UUID,
    expires_in_days: int = REFRESH_TOKEN_EXPIRY_DAYS,
) -> str:
    """
    Generate a JWT refresh token for a steward.

    Args:
        steward_id: UUID of the authenticated steward
        expires_in_days: Token expiration time in days

    Returns:
        Encoded JWT token string
    """
    if not _jwt_secret:
        raise RuntimeError("JWT secret not configured. Call set_jwt_secret() at app startup.")

    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=expires_in_days)

    payload = {
        "steward_id": str(steward_id),
        "token_type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }

    token = jwt.encode(payload, _jwt_secret, algorithm=_jwt_algorithm)
    return token


def validate_token(token: str, expected_token_type: str = "access") -> Optional[TokenPayload]:
    """
    Validate and decode a JWT token.

    Args:
        token: JWT token string
        expected_token_type: Expected token type ("access" or "refresh")

    Returns:
        TokenPayload if valid, None if invalid or expired
    """
    if not _jwt_secret:
        logger.error("JWT secret not configured")
        return None

    try:
        payload = jwt.decode(token, _jwt_secret, algorithms=[_jwt_algorithm])

        # Verify token type
        if payload.get("token_type") != expected_token_type:
            logger.warning(f"Token type mismatch. Expected {expected_token_type}, got {payload.get('token_type')}")
            return None

        # Check expiration
        exp_timestamp = payload.get("exp")
        if not exp_timestamp or datetime.now(timezone.utc).timestamp() > exp_timestamp:
            logger.info("Token has expired")
            return None

        # Build TokenPayload for access tokens (refresh tokens have minimal payload)
        if expected_token_type == "access":
            return TokenPayload(
                steward_id=UUID(payload["steward_id"]),
                email=payload["email"],
                name=payload["name"],
                role=payload["role"],
                approval_scope=payload.get("approval_scope", []),
                token_type=payload["token_type"],
                exp=exp_timestamp,
                iat=payload.get("iat", 0),
            )
        else:
            # For refresh tokens, just verify it's valid
            return TokenPayload(
                steward_id=UUID(payload["steward_id"]),
                email="",
                name="",
                role="",
                approval_scope=[],
                token_type=payload["token_type"],
                exp=exp_timestamp,
                iat=payload.get("iat", 0),
            )

    except jwt.ExpiredSignatureError:
        logger.info("Token signature expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid token: {e}")
        return None
    except Exception as e:
        logger.error(f"Error validating token: {e}")
        return None


def extract_steward_id_from_token(token: str) -> Optional[UUID]:
    """
    Extract steward ID from a token without full validation (useful for audit logging).

    Args:
        token: JWT token string

    Returns:
        Steward UUID if extractable, None otherwise
    """
    if not _jwt_secret:
        return None

    try:
        payload = jwt.decode(token, _jwt_secret, algorithms=[_jwt_algorithm], options={"verify_exp": False})
        return UUID(payload.get("steward_id"))
    except Exception:
        return None

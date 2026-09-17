"""
Authentication middleware for Celestial Portal
Extracts and validates Bearer tokens from Authorization headers
"""

import logging
from typing import Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

from .token import validate_token

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract Bearer token from Authorization header and validate it.
    Injects steward context into request state for protected endpoints.
    """

    # Paths that don't require authentication
    EXEMPT_PATHS = {
        "/health",
        "/docs",
        "/openapi.json",
        "/v1/auth/authorize",
        "/v1/auth/callback",
        "/v1/auth/enroll",
        "/v1/auth/token",
        "/v1/auth/logout",
    }

    async def dispatch(self, request: Request, call_next):
        """Process request and validate authentication token if required"""
        # Skip authentication for exempt paths
        if request.url.path in self.EXEMPT_PATHS:
            return await call_next(request)

        # Extract Bearer token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.warning(f"Missing Authorization header for {request.url.path}")
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        # Parse Bearer token
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.warning(f"Invalid Authorization header format for {request.url.path}")
            raise HTTPException(status_code=401, detail="Invalid Authorization header format")

        token = parts[1]

        # Validate token
        payload = validate_token(token, expected_token_type="access")
        if not payload:
            logger.warning(f"Invalid or expired token for {request.url.path}")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Inject steward context into request state
        request.state.steward_id = payload.steward_id
        request.state.steward_email = payload.email
        request.state.steward_name = payload.name
        request.state.steward_role = payload.role
        request.state.approval_scope = payload.approval_scope

        logger.debug(f"Authenticated steward {payload.steward_id} for {request.url.path}")

        # Proceed to next middleware/endpoint
        response = await call_next(request)
        return response


def extract_steward_from_request(request: Request) -> dict:
    """
    Extract steward context from authenticated request.
    Raises HTTPException if steward context is missing.
    """
    if not hasattr(request.state, "steward_id"):
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "steward_id": request.state.steward_id,
        "email": request.state.steward_email,
        "name": request.state.steward_name,
        "role": request.state.steward_role,
        "approval_scope": request.state.approval_scope,
    }

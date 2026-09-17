"""
OAuth2 provider implementations for Google, Apple, Microsoft
"""

import base64
import hashlib
import json
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional

import httpx

from .models import AuthProvider, OAuthProvider, StewardProfile

logger = logging.getLogger(__name__)


class OAuthManager:
    """Manages OAuth2 flows for multiple providers"""

    def __init__(
        self,
        google_client_id: str,
        google_client_secret: str,
        apple_client_id: str,
        apple_client_secret: str,
        microsoft_client_id: str,
        microsoft_client_secret: str,
        redirect_uri: str,
    ):
        self.redirect_uri = redirect_uri
        self.http_client = httpx.AsyncClient(timeout=10.0)

        # Provider configurations
        self.providers = {
            AuthProvider.GOOGLE: OAuthProvider(
                name=AuthProvider.GOOGLE,
                client_id=google_client_id,
                client_secret=google_client_secret,
                redirect_uri=redirect_uri,
                authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                token_endpoint="https://oauth2.googleapis.com/token",
                userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
            ),
            AuthProvider.APPLE: OAuthProvider(
                name=AuthProvider.APPLE,
                client_id=apple_client_id,
                client_secret=apple_client_secret,
                redirect_uri=redirect_uri,
                authorization_endpoint="https://appleid.apple.com/auth/authorize",
                token_endpoint="https://appleid.apple.com/auth/token",
                userinfo_endpoint="https://appleid.apple.com/auth/userinfo",
            ),
            AuthProvider.MICROSOFT: OAuthProvider(
                name=AuthProvider.MICROSOFT,
                client_id=microsoft_client_id,
                client_secret=microsoft_client_secret,
                redirect_uri=redirect_uri,
                authorization_endpoint="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
                token_endpoint="https://login.microsoftonline.com/common/oauth2/v2.0/token",
                userinfo_endpoint="https://graph.microsoft.com/v1.0/me",
            ),
        }

    def get_authorization_url(self, provider: AuthProvider, mobile: bool = False) -> tuple[str, str]:
        """
        Generate OAuth authorization URL and state parameter.

        Args:
            provider: OAuth provider to use
            mobile: If True, use PKCE for mobile flow

        Returns:
            Tuple of (authorization_url, state_parameter)
        """
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")

        state = secrets.token_urlsafe(32)
        oauth_provider = self.providers[provider]

        params = {
            "client_id": oauth_provider.client_id,
            "redirect_uri": oauth_provider.redirect_uri,
            "response_type": "code",
            "state": state,
            "scope": self._get_scope(provider),
        }

        # Add PKCE for mobile
        if mobile:
            code_verifier = secrets.token_urlsafe(32)
            code_challenge = base64.urlsafe_b64encode(
                hashlib.sha256(code_verifier.encode()).digest()
            ).decode().rstrip("=")
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
            # Return state with embedded code_verifier (client stores separately)
            state_with_verifier = f"{state}|{code_verifier}"
        else:
            state_with_verifier = state

        # Build authorization URL
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        auth_url = f"{oauth_provider.authorization_endpoint}?{query_string}"

        return auth_url, state_with_verifier

    async def exchange_code_for_token(
        self,
        provider: AuthProvider,
        code: str,
        state: str,
    ) -> dict:
        """
        Exchange authorization code for access token.

        Args:
            provider: OAuth provider
            code: Authorization code from provider
            state: State parameter (may include PKCE verifier)

        Returns:
            Token response dict with access_token, id_token, etc.
        """
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")

        oauth_provider = self.providers[provider]

        # Extract PKCE verifier if present
        code_verifier = None
        if "|" in state:
            state, code_verifier = state.split("|", 1)

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": oauth_provider.redirect_uri,
            "client_id": oauth_provider.client_id,
            "client_secret": oauth_provider.client_secret,
        }

        if code_verifier:
            payload["code_verifier"] = code_verifier

        try:
            response = await self.http_client.post(
                oauth_provider.token_endpoint,
                data=payload,
                headers={"Accept": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Token exchange failed for {provider}: {e}")
            raise

    async def get_userinfo(self, provider: AuthProvider, access_token: str) -> dict:
        """
        Fetch user info from OAuth provider.

        Args:
            provider: OAuth provider
            access_token: Access token from exchange_code_for_token

        Returns:
            User info dict with sub, email, name, picture
        """
        if provider not in self.providers:
            raise ValueError(f"Unsupported provider: {provider}")

        oauth_provider = self.providers[provider]

        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = await self.http_client.get(
                oauth_provider.userinfo_endpoint,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

            # Normalize provider responses
            if provider == AuthProvider.GOOGLE:
                return {
                    "sub": data.get("sub"),
                    "email": data.get("email"),
                    "name": data.get("name"),
                    "picture": data.get("picture"),
                }
            elif provider == AuthProvider.APPLE:
                return {
                    "sub": data.get("sub"),
                    "email": data.get("email"),
                    "name": data.get("name"),
                    "picture": None,
                }
            elif provider == AuthProvider.MICROSOFT:
                return {
                    "sub": data.get("id"),
                    "email": data.get("userPrincipalName") or data.get("mail"),
                    "name": data.get("displayName"),
                    "picture": None,
                }
        except httpx.HTTPError as e:
            logger.error(f"Userinfo fetch failed for {provider}: {e}")
            raise

    def _get_scope(self, provider: AuthProvider) -> str:
        """Get OAuth scope string for provider"""
        scopes = {
            AuthProvider.GOOGLE: "openid email profile",
            AuthProvider.APPLE: "openid email name",
            AuthProvider.MICROSOFT: "openid email profile offline_access",
        }
        return scopes.get(provider, "openid email profile")

    async def close(self):
        """Clean up HTTP client"""
        await self.http_client.aclose()


# Singleton instance
_oauth_manager: Optional[OAuthManager] = None


async def get_oauth_manager(
    google_client_id: str = "",
    google_client_secret: str = "",
    apple_client_id: str = "",
    apple_client_secret: str = "",
    microsoft_client_id: str = "",
    microsoft_client_secret: str = "",
    redirect_uri: str = "http://localhost:8000/v1/auth/callback",
) -> OAuthManager:
    """Get or create OAuth manager singleton"""
    global _oauth_manager
    if _oauth_manager is None:
        _oauth_manager = OAuthManager(
            google_client_id=google_client_id,
            google_client_secret=google_client_secret,
            apple_client_id=apple_client_id,
            apple_client_secret=apple_client_secret,
            microsoft_client_id=microsoft_client_id,
            microsoft_client_secret=microsoft_client_secret,
            redirect_uri=redirect_uri,
        )
    return _oauth_manager

import logging

from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/admin/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    settings = get_settings()

    valid = payload.username == settings.admin_username and verify_password(
        payload.password, settings.admin_password_hash
    )
    if not valid:
        logger.warning("failed admin login attempt for username=%s", payload.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    token = create_access_token(subject=payload.username)
    logger.info("admin login succeeded for username=%s", payload.username)
    return TokenResponse(access_token=token, expires_in_minutes=settings.access_token_expire_minutes)

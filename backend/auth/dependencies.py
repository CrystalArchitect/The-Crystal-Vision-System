"""
FastAPI dependency functions for authentication
"""

import logging
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.database import get_db
from .repository import StewardRepository

logger = logging.getLogger(__name__)


async def get_current_steward(request: Request):
    """
    Dependency to extract authenticated steward from request state.
    Used in protected endpoints.
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


async def get_current_steward_strict(
    request: Request,
    db: Session = Depends(get_db),
    required_roles: list[str] = None,
    required_scope: str = None
) -> dict:
    """
    Strict dependency that validates steward exists in database and has required roles/scope.
    Used for sensitive endpoints that require specific authorization.
    """
    # Extract steward from request state (set by middleware)
    if not hasattr(request.state, "steward_id"):
        raise HTTPException(status_code=401, detail="Not authenticated")

    steward_id: UUID = request.state.steward_id

    # Verify steward exists in database
    repo = StewardRepository(db)
    steward = repo.get_by_id(steward_id)
    if not steward:
        logger.warning(f"Steward {steward_id} not found in database")
        raise HTTPException(status_code=403, detail="Steward not found")

    # Validate required roles if specified
    if required_roles and steward.role.value not in required_roles:
        logger.warning(
            f"Steward {steward_id} has role {steward.role.value}, required {required_roles}"
        )
        raise HTTPException(status_code=403, detail="Insufficient role permissions")

    # Validate required scope if specified
    if required_scope and required_scope not in steward.approval_scope:
        logger.warning(
            f"Steward {steward_id} missing required scope {required_scope}"
        )
        raise HTTPException(status_code=403, detail="Insufficient approval scope")

    return {
        "steward_id": steward.steward_id,
        "email": steward.email,
        "name": steward.name,
        "role": steward.role.value,
        "approval_scope": steward.approval_scope,
    }

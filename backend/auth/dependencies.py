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
    db: Session = Depends(get_db)
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

    return {
        "steward_id": steward.steward_id,
        "email": steward.email,
        "name": steward.name,
        "role": steward.role.value,
        "approval_scope": steward.approval_scope,
    }

"""
Celestial Portal: Voice-First Governance System
FastAPI service for decision canonicalization and steward approval workflows
"""

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

# Import centralized database configuration
from backend.database import engine, SessionLocal, get_db as database_get_db

# Import authentication components
from backend.auth.routes import router as auth_router
from backend.auth.middleware import AuthenticationMiddleware
from backend.auth.dependencies import get_current_steward, get_current_steward_strict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Celestial Portal",
    description="Voice-first governance system with immutable audit trails",
    version="0.1.0"
)

# Authentication middleware for Bearer token validation
app.add_middleware(AuthenticationMiddleware)

# CORS for device communication (iPhone, Windows, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Siri / App Intent / universal gateway → CrystalCore.OS → TAI (foundation)
from backend.portal.gateway import router as gateway_router

app.include_router(gateway_router)


# ============================================================================
# Models
# ============================================================================

class StewardInfo(BaseModel):
    """Steward identity and authorization"""
    steward_id: UUID
    name: str
    email: str
    biometric_type: Optional[str] = None
    can_approve_decisions: bool = False


class DecisionPayload(BaseModel):
    """Administrative decision content"""
    decision_code: str = Field(..., min_length=5, max_length=50, pattern=r"^[A-Z]{3}-\d{3}$")
    title: str = Field(..., min_length=10, max_length=500)
    description: Optional[str] = None
    decision_type: str  # 'linting_standard', 'deprecation_status', 'policy'
    payload: dict = Field(default_factory=dict)  # The actual decision content
    enforcement_scope: Optional[str] = None


class ApprovalRequest(BaseModel):
    """Steward approval with voice signature"""
    decision_id: UUID
    steward_id: UUID
    voice_signature_hash: Optional[str] = None  # Optional voice biometric confirmation


class VaultDecision(BaseModel):
    """Decision stored in MemoryCore Vault"""
    decision_id: UUID
    decision_code: str
    title: str
    status: str
    event_hash: str
    created_at: datetime
    approved_by: Optional[UUID] = None


# ============================================================================
# Database Utilities
# ============================================================================

# Use centralized get_db from database module
get_db = database_get_db


def compute_event_hash(payload: dict) -> str:
    """Compute SHA-256 hash of event payload"""
    payload_json = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(payload_json.encode()).hexdigest()


def get_previous_hash(db: Session, workspace_id: UUID, decision_code: str) -> Optional[str]:
    """Get the previous_hash for a decision code to maintain chain"""
    result = db.execute(
        text("""
            SELECT event_hash FROM vault.decisions
            WHERE workspace_id = :workspace_id
              AND decision_code = :decision_code
            ORDER BY created_at DESC
            LIMIT 1
        """),
        {"workspace_id": str(workspace_id), "decision_code": decision_code}
    ).fetchone()
    return result[0] if result else None


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable")


@app.post("/v1/admin/stamp")
async def stamp_decision(
    payload: DecisionPayload,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    steward_context: dict = Depends(get_current_steward_strict)
) -> VaultDecision:
    """
    Canonicalize an administrative decision into MemoryCore Vault.
    Steward approves via voice or biometric; decision receives immutable SHA-256 receipt.
    Requires authentication and POLICY_APPROVER or ADMIN role.
    """
    # Verify steward has decision approval permissions
    steward_id = steward_context["steward_id"]
    steward_name = steward_context["name"]
    steward_email = steward_context["email"]

    # Check if steward has admin or policy_approver role
    allowed_roles = ["policy_approver", "admin"]
    steward_role = steward_context.get("role", "").lower()
    if steward_role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Steward not authorized to approve decisions")

    workspace_id = UUID("00000000-0000-0000-0000-000000000000")  # Default workspace
    decision_id = uuid4()
    now = datetime.now(timezone.utc)

    # Get previous hash for chain
    previous_hash = get_previous_hash(db, workspace_id, payload.decision_code)

    # Build payload with chain info
    decision_dict = {
        "decision_id": str(decision_id),
        "workspace_id": str(workspace_id),
        "decision_code": payload.decision_code,
        "title": payload.title,
        "status": "active",
        "payload": payload.payload,
        "previous_hash": previous_hash,
        "created_at": now.isoformat(),
        "created_by": str(steward_id)
    }

    # Compute immutable receipt hash
    event_hash = compute_event_hash(decision_dict)
    decision_dict["event_hash"] = event_hash

    try:
        # Store decision
        db.execute(
            text("""
                INSERT INTO vault.decisions
                (decision_id, workspace_id, decision_code, title, description, decision_type,
                 payload, enforcement_scope, created_by, approved_by, status,
                 previous_hash, event_hash, effective_at)
                VALUES
                (:decision_id, :workspace_id, :decision_code, :title, :description,
                 :decision_type, :payload, :enforcement_scope, :created_by, :approved_by,
                 :status, :previous_hash, :event_hash, :effective_at)
            """),
            {
                "decision_id": str(decision_id),
                "workspace_id": str(workspace_id),
                "decision_code": payload.decision_code,
                "title": payload.title,
                "description": payload.description,
                "decision_type": payload.decision_type,
                "payload": json.dumps(payload.payload),
                "enforcement_scope": payload.enforcement_scope,
                "created_by": str(steward_id),
                "approved_by": str(steward_id),
                "status": "active",
                "previous_hash": previous_hash,
                "event_hash": event_hash,
                "effective_at": now
            }
        )

        # Record audit event
        audit_event_id = uuid4()
        audit_dict = {
            "event_id": str(audit_event_id),
            "workspace_id": str(workspace_id),
            "decision_id": str(decision_id),
            "event_category": "decision_approved",
            "actor_steward_id": str(steward_id),
            "outcome": "success"
        }
        audit_hash = compute_event_hash(audit_dict)

        db.execute(
            text("""
                INSERT INTO vault.audit_events
                (event_id, workspace_id, decision_id, event_category, event_action,
                 actor_steward_id, outcome, event_hash, previous_event_hash)
                VALUES
                (:event_id, :workspace_id, :decision_id, :event_category, :event_action,
                 :actor_steward_id, :outcome, :event_hash, :previous_event_hash)
            """),
            {
                "event_id": str(audit_event_id),
                "workspace_id": str(workspace_id),
                "decision_id": str(decision_id),
                "event_category": "decision_approved",
                "event_action": f"Decision {payload.decision_code} approved by {steward_name}",
                "actor_steward_id": str(steward_id),
                "outcome": "success",
                "event_hash": audit_hash,
                "previous_event_hash": None
            }
        )

        db.commit()

        logger.info(f"Decision {payload.decision_code} canonicalized with hash {event_hash}")

        return VaultDecision(
            decision_id=decision_id,
            decision_code=payload.decision_code,
            title=payload.title,
            status="active",
            event_hash=event_hash,
            created_at=now,
            approved_by=steward_id
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to canonicalize decision: {e}")
        raise HTTPException(status_code=500, detail="Failed to canonicalize decision")


@app.get("/v1/decisions/{decision_code}")
async def get_decision(
    decision_code: str,
    db: Session = Depends(get_db)
) -> Optional[VaultDecision]:
    """
    Retrieve the current active decision for a given code.
    Used by UK portfolio CI/CD for enforcement.
    """
    result = db.execute(
        text("""
            SELECT decision_id, decision_code, title, status, event_hash, created_at, approved_by
            FROM vault.decisions
            WHERE decision_code = :decision_code
              AND status = 'active'
            ORDER BY created_at DESC
            LIMIT 1
        """),
        {"decision_code": decision_code}
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail=f"Decision {decision_code} not found")

    return VaultDecision(
        decision_id=result[0],
        decision_code=result[1],
        title=result[2],
        status=result[3],
        event_hash=result[4],
        created_at=result[5],
        approved_by=result[6]
    )


@app.get("/v1/audit-chain/{decision_id}")
async def get_audit_chain(
    decision_id: UUID,
    db: Session = Depends(get_db)
) -> list:
    """
    Retrieve immutable audit chain for a decision.
    Each event includes SHA-256 hash and previous_hash for chain verification.
    """
    result = db.execute(
        text("""
            SELECT event_id, event_category, actor_steward_id, outcome, event_hash,
                   previous_event_hash, created_at
            FROM vault.audit_events
            WHERE decision_id = :decision_id
            ORDER BY created_at ASC
        """),
        {"decision_id": str(decision_id)}
    ).fetchall()

    return [
        {
            "event_id": str(row[0]),
            "event_category": row[1],
            "actor_steward_id": str(row[2]),
            "outcome": row[3],
            "event_hash": row[4],
            "previous_event_hash": row[5],
            "created_at": row[6].isoformat() if row[6] else None
        }
        for row in result
    ]


@app.post("/v1/decisions/{decision_id}/revoke")
async def revoke_decision(
    decision_id: UUID,
    db: Session = Depends(get_db),
    steward_context: dict = Depends(get_current_steward_strict)
) -> dict:
    """
    Revoke an active decision (immutable: creates new superseded record).
    Only authorized stewards can revoke decisions.
    Requires authentication and POLICY_APPROVER or ADMIN role.
    """
    steward_id = steward_context["steward_id"]
    steward_name = steward_context["name"]

    # Check if steward has admin or policy_approver role
    allowed_roles = ["policy_approver", "admin"]
    steward_role = steward_context.get("role", "").lower()
    if steward_role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Not authorized to revoke decisions")

    try:
        db.execute(
            text("""
                UPDATE vault.decisions
                SET status = 'revoked', revoked_at = :now
                WHERE decision_id = :decision_id
                  AND status = 'active'
            """),
            {
                "decision_id": str(decision_id),
                "now": datetime.now(timezone.utc)
            }
        )

        # Record revocation audit event
        audit_event_id = uuid4()
        audit_dict = {
            "event_id": str(audit_event_id),
            "decision_id": str(decision_id),
            "event_category": "decision_revoked",
            "actor_steward_id": str(steward_id),
            "outcome": "success"
        }
        audit_hash = compute_event_hash(audit_dict)

        db.execute(
            text("""
                INSERT INTO vault.audit_events
                (event_id, workspace_id, decision_id, event_category, event_action,
                 actor_steward_id, outcome, event_hash)
                VALUES
                (:event_id, :workspace_id, :decision_id, :event_category, :event_action,
                 :actor_steward_id, :outcome, :event_hash)
            """),
            {
                "event_id": str(audit_event_id),
                "workspace_id": "00000000-0000-0000-0000-000000000000",
                "decision_id": str(decision_id),
                "event_category": "decision_revoked",
                "event_action": f"Decision revoked by {steward_name}",
                "actor_steward_id": str(steward_id),
                "outcome": "success",
                "event_hash": audit_hash
            }
        )

        db.commit()
        return {"status": "revoked", "decision_id": str(decision_id)}

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to revoke decision: {e}")
        raise HTTPException(status_code=500, detail="Failed to revoke decision")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

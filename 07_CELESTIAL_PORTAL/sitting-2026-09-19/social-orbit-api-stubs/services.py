from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from threading import Lock
from uuid import UUID

from .connectors import connector_for
from .models import (
    ApprovalRequest,
    AuditCategory,
    AuditEvent,
    ConsentDecision,
    ConsentDecisionRequest,
    ConsentGrant,
    ConnectorAccount,
    ConnectorStatus,
    DataClass,
    JobStatus,
    PlatformVariant,
    PublicationJob,
    ProviderId,
    utc_now,
)


class InMemoryStore:
    def __init__(self) -> None:
        self.lock = Lock()
        self.accounts: dict[UUID, ConnectorAccount] = {}
        self.jobs: dict[UUID, PublicationJob] = {}
        self.variants: dict[UUID, PlatformVariant] = {}
        self.grants: dict[UUID, ConsentGrant] = {}
        self.audit: dict[UUID, list[AuditEvent]] = defaultdict(list)

    def add_audit(self, event: AuditEvent) -> AuditEvent:
        with self.lock:
            chain = self.audit[event.workspace_id]
            previous_hash = chain[-1].event_hash if chain else None
            unsigned = event.model_copy(update={"previous_hash": previous_hash, "event_hash": None})
            payload = unsigned.model_dump(mode="json", exclude={"event_hash"})
            digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
            stored = unsigned.model_copy(update={"event_hash": digest})
            chain.append(stored)
            return stored


store = InMemoryStore()


class ConsentService:
    def decide(self, request: ConsentDecisionRequest) -> ConsentDecision:
        # Deny-by-default: callers must explicitly create a grant in production.
        if DataClass.BIOMETRIC in request.data_classes:
            return ConsentDecision(allowed=False, reason="Biometric data requires a dedicated identity consent workflow.")
        if request.action in {"publish", "schedule", "connect"}:
            return ConsentDecision(allowed=False, reason="External actions require an explicit stored consent grant.")
        grant = ConsentGrant(
            workspace_id=request.workspace_id,
            provider=request.provider,
            action=request.action,
            data_classes=request.data_classes,
            purpose=request.purpose,
            granted=False,
        )
        return ConsentDecision(allowed=False, reason="No active consent grant exists.", grant=grant)

    def grant(self, grant: ConsentGrant) -> ConsentGrant:
        stored = grant.model_copy(update={"granted": True})
        store.grants[stored.id] = stored
        store.add_audit(AuditEvent(workspace_id=stored.workspace_id, category=AuditCategory.CONSENT, action="consent granted", outcome="success", provider=stored.provider, subject=str(stored.id), detail=stored.purpose))
        return stored

    def has_active_grant(self, workspace_id: UUID, provider: ProviderId, action: str, grant_ids: list[UUID]) -> bool:
        return any(
            (grant := store.grants.get(grant_id)) is not None
            and grant.workspace_id == workspace_id
            and grant.provider == provider
            and grant.action == action
            and grant.is_active()
            for grant_id in grant_ids
        )


consent_service = ConsentService()


def approve_job(job: PublicationJob, request: ApprovalRequest) -> PublicationJob:
    status = JobStatus.QUEUED if request.approved else JobStatus.BLOCKED
    updated = job.model_copy(update={"status": status, "updated_at": utc_now()})
    store.jobs[job.id] = updated
    store.add_audit(AuditEvent(workspace_id=job.workspace_id, category=AuditCategory.PUBLICATION, action="publication approval", outcome="success" if request.approved else "blocked", subject=str(job.id), detail=request.note or ""))
    return updated


def revoke_account(account: ConnectorAccount) -> ConnectorAccount:
    updated = connector_for(account.provider).revoke(account)
    store.accounts[account.id] = updated
    store.add_audit(AuditEvent(workspace_id=account.workspace_id, category=AuditCategory.CONNECTION, action="connector revoked", outcome="revoked", provider=account.provider, subject=str(account.id), detail="Connector access marked revoked in stub storage."))
    return updated

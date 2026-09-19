from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from .connectors import ConnectorAuthError, ConnectorNotImplemented, PROVIDER_SPECS, connector_for
from .models import (
    ApprovalRequest,
    AuditCategory,
    AuditEvent,
    ConnectCallbackRequest,
    ConnectStartResponse,
    ConsentDecision,
    ConsentDecisionRequest,
    ConsentGrant,
    ConnectorAccount,
    JobStatus,
    PlatformVariant,
    ProviderId,
    PublishRequest,
    PublicationJob,
    PublicationTarget,
    utc_now,
)
from .services import approve_job, consent_service, revoke_account, store

app = FastAPI(
    title="Celestial Portal Social Orbit API",
    version="0.1.0-stub",
    description="Safe backend stubs for cross-platform social and entertainment orchestration.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "celestial-portal-social-api", "mode": "stub"}


@app.get("/v1/providers")
def list_providers() -> list[dict]:
    return [spec.capability.model_dump(mode="json") for spec in PROVIDER_SPECS.values()]


@app.get("/v1/providers/{provider}/capabilities")
def provider_capabilities(provider: ProviderId):
    return connector_for(provider).capabilities()


@app.get("/v1/connectors/{provider}/start", response_model=ConnectStartResponse)
def start_connector(provider: ProviderId, state: str = Query(default_factory=lambda: uuid4().hex)):
    connector = connector_for(provider)
    url, scopes = connector.authorization_url(state)
    return ConnectStartResponse(provider=provider, authorization_url=url, state=state, requested_scopes=scopes)


@app.post("/v1/connectors/{provider}/callback", response_model=ConnectorAccount)
def complete_connector(provider: ProviderId, request: ConnectCallbackRequest):
    if request.state == "":
        raise HTTPException(status_code=400, detail="OAuth state is required")
    try:
        account = connector_for(provider).connect(request)
    except ConnectorAuthError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    store.accounts[account.id] = account
    store.add_audit(AuditEvent(workspace_id=account.workspace_id, category=AuditCategory.CONNECTION, action="connector connected", outcome="success", provider=provider, subject=str(account.id), detail="Stub connector account created; no provider token was stored."))
    return account


@app.get("/v1/workspaces/{workspace_id}/connectors", response_model=list[ConnectorAccount])
def list_connectors(workspace_id: UUID):
    return [account for account in store.accounts.values() if account.workspace_id == workspace_id]


@app.post("/v1/connectors/{account_id}/revoke", response_model=ConnectorAccount)
def revoke_connector(account_id: UUID):
    account = store.accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Connector account not found")
    return revoke_account(account)


@app.post("/v1/consent/decide", response_model=ConsentDecision)
def decide_consent(request: ConsentDecisionRequest):
    return consent_service.decide(request)


@app.post("/v1/consent/grants", response_model=ConsentGrant, status_code=status.HTTP_201_CREATED)
def create_consent_grant(grant: ConsentGrant):
    return consent_service.grant(grant)


@app.post("/v1/variants", response_model=PlatformVariant, status_code=status.HTTP_201_CREATED)
def create_variant(variant: PlatformVariant):
    store.variants[variant.id] = variant
    return variant


@app.post("/v1/publications", response_model=PublicationJob, status_code=status.HTTP_201_CREATED)
def create_publication(request: PublishRequest):
    if not request.targets:
        raise HTTPException(status_code=422, detail="At least one publication target is required")
    for target in request.targets:
        if target.connector_account_id not in store.accounts:
            raise HTTPException(status_code=404, detail=f"Connector account not found: {target.connector_account_id}")
        if not target.approved and request.require_manual_approval:
            continue
        if not consent_service.has_active_grant(request.workspace_id, target.provider, "publish", request.consent_grant_ids):
            raise HTTPException(status_code=403, detail=f"Active publish consent is required for {target.provider.value}")
    job = PublicationJob(
        workspace_id=request.workspace_id,
        project_id=request.project_id,
        idempotency_key=request.idempotency_key,
        targets=request.targets,
        consent_grant_ids=request.consent_grant_ids,
        status=JobStatus.AWAITING_APPROVAL if request.require_manual_approval else JobStatus.QUEUED,
    )
    store.jobs[job.id] = job
    store.add_audit(AuditEvent(workspace_id=job.workspace_id, category=AuditCategory.PUBLICATION, action="publication job created", outcome="started", subject=str(job.id), detail="No external publication was attempted by the stub."))
    return job


@app.post("/v1/publications/{job_id}/approve", response_model=PublicationJob)
def approve_publication(job_id: UUID, request: ApprovalRequest):
    job = store.jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Publication job not found")
    return approve_job(job, request)


@app.post("/v1/publications/{job_id}/execute", response_model=PublicationJob)
def execute_publication(job_id: UUID):
    job = store.jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Publication job not found")
    if job.status != JobStatus.QUEUED:
        raise HTTPException(status_code=409, detail="Job must be queued before execution")
    for target in job.targets:
        account = store.accounts.get(target.connector_account_id)
        variant = store.variants.get(target.variant_id)
        if not account or not variant:
            raise HTTPException(status_code=422, detail="Target account or variant is missing")
        try:
            connector_for(target.provider).publish(job, target, variant)
        except ConnectorNotImplemented as exc:
            updated = job.model_copy(update={"status": JobStatus.BLOCKED, "failure_code": "STUB_NOT_IMPLEMENTED", "failure_detail": str(exc), "updated_at": utc_now()})
            store.jobs[job.id] = updated
            store.add_audit(AuditEvent(workspace_id=job.workspace_id, category=AuditCategory.PUBLICATION, action="publication blocked", outcome="blocked", provider=target.provider, subject=str(job.id), detail=str(exc)))
            return updated
    updated = job.model_copy(update={"status": JobStatus.PUBLISHED, "updated_at": utc_now()})
    store.jobs[job.id] = updated
    return updated


@app.get("/v1/workspaces/{workspace_id}/audit", response_model=list[AuditEvent])
def list_audit(workspace_id: UUID):
    return store.audit.get(workspace_id, [])

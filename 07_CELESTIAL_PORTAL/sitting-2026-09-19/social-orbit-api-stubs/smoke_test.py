from __future__ import annotations

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
workspace_id = uuid4()
project_id = uuid4()

assert client.get("/health").json()["status"] == "ok"
providers = client.get("/v1/providers")
assert providers.status_code == 200
assert {item["provider"] for item in providers.json()} >= {"youtube", "instagram", "tiktok"}

start = client.get("/v1/connectors/youtube/start")
assert start.status_code == 200
assert start.json()["provider"] == "youtube"

callback = client.post(
    "/v1/connectors/youtube/callback",
    json={"workspace_id": str(workspace_id), "code": "stub_oauth_code", "state": start.json()["state"]},
)
assert callback.status_code == 200
account = callback.json()

variant_id = uuid4()
variant = client.post(
    "/v1/variants",
    json={
        "id": str(variant_id),
        "source_asset_id": str(uuid4()),
        "provider": "youtube",
        "title": "Celestial Portal launch",
        "caption": "Local-first creation.",
        "validated": True,
    },
)
assert variant.status_code == 201

job = client.post(
    "/v1/publications",
    json={
        "workspace_id": str(workspace_id),
        "project_id": str(project_id),
        "idempotency_key": "smoke-test-publish-001",
        "targets": [{
            "connector_account_id": account["id"],
            "provider": "youtube",
            "variant_id": str(variant_id),
            "approved": False,
        }],
        "require_manual_approval": True,
    },
)
assert job.status_code == 201
assert job.json()["status"] == "awaiting_approval"

approved = client.post(
    f"/v1/publications/{job.json()['id']}/approve",
    json={"approved": True, "reviewer_id": str(uuid4()), "note": "Smoke test approval"},
)
assert approved.status_code == 200
assert approved.json()["status"] == "queued"

executed = client.post(f"/v1/publications/{job.json()['id']}/execute")
assert executed.status_code == 200
assert executed.json()["status"] == "blocked"
assert executed.json()["failure_code"] == "STUB_NOT_IMPLEMENTED"

print("social_api smoke test passed")

"""
Tests for POST /api/v1/admin/generate. These mock app.core.llm so the suite
doesn't need the actual (multi-GB) model weights downloaded -- see
download_model.py / README.md for running against the real model.
"""

from test_admin_api import _token, client  # reuses the already-configured TestClient

import app.api.v1.routes.admin as admin_route
from app.core.llm import ModelNotAvailableError


def test_generate_requires_auth():
    resp = client.post("/api/v1/admin/generate", json={"prompt": "hello"})
    assert resp.status_code == 401


def test_generate_rejects_empty_prompt():
    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": ""},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


def test_generate_returns_completion(monkeypatch):
    monkeypatch.setattr(admin_route, "llm_generate", lambda prompt, max_tokens, temperature: "mock completion")

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "Summarize CrystalCore.OS.", "max_tokens": 64},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"completion": "mock completion"}


def test_generate_503_when_model_missing(monkeypatch):
    def _raise(prompt, max_tokens, temperature):
        raise ModelNotAvailableError("model file not found -- run download_model.py first")

    monkeypatch.setattr(admin_route, "llm_generate", _raise)

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 503
    assert "download_model.py" in resp.json()["error"]

"""
Tests for POST /api/v1/admin/generate. These mock app.core.llm so the suite
doesn't need the actual (multi-GB) model weights downloaded or a real
ANTHROPIC_API_KEY -- see download_model.py / README.md for running against
the real local model, and docs/architecture/THREE-TIER-GENERATE.md for the
full local -> cloud cascade this endpoint implements.
"""

from test_admin_api import _token, client  # reuses the already-configured TestClient

import app.api.v1.routes.admin as admin_route


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


def test_generate_rejects_unknown_tier():
    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "hello", "tier": "quantum"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 422


def test_generate_defaults_to_local_tier(monkeypatch):
    monkeypatch.setattr(
        admin_route,
        "llm_generate",
        lambda prompt, max_tokens, temperature, tier: ("mock completion", "local"),
    )

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "Summarize CrystalCore.OS.", "max_tokens": 64},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"completion": "mock completion", "tier_used": "local"}


def test_generate_reports_which_tier_served_it(monkeypatch):
    seen = {}

    def _fake_generate(prompt, max_tokens, temperature, tier):
        seen["tier_requested"] = tier
        return "cloud completion", "cloud"

    monkeypatch.setattr(admin_route, "llm_generate", _fake_generate)

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "hello", "tier": "cloud"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"completion": "cloud completion", "tier_used": "cloud"}
    assert seen["tier_requested"] == "cloud"


def test_generate_503_when_local_model_missing_and_no_fallback_requested(monkeypatch):
    from app.core.llm import ModelNotAvailableError

    def _raise(prompt, max_tokens, temperature, tier):
        raise ModelNotAvailableError("model file not found -- run download_model.py first")

    monkeypatch.setattr(admin_route, "llm_generate", _raise)

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "hello", "tier": "local"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 503
    assert "download_model.py" in resp.json()["error"]


def test_generate_503_when_cloud_tier_not_configured(monkeypatch):
    from app.core.llm import CloudNotConfiguredError

    def _raise(prompt, max_tokens, temperature, tier):
        raise CloudNotConfiguredError("cloud tier not configured -- set ANTHROPIC_API_KEY to enable it")

    monkeypatch.setattr(admin_route, "llm_generate", _raise)

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "hello", "tier": "cloud"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 503
    assert "ANTHROPIC_API_KEY" in resp.json()["error"]


def test_generate_503_when_every_tier_in_the_cascade_fails(monkeypatch):
    from app.core.llm import AllTiersUnavailableError

    def _raise(prompt, max_tokens, temperature, tier):
        assert tier == "auto"
        raise AllTiersUnavailableError(
            "local tier unavailable (no model); cloud tier unavailable (no key)"
        )

    monkeypatch.setattr(admin_route, "llm_generate", _raise)

    token = _token()
    resp = client.post(
        "/api/v1/admin/generate",
        json={"prompt": "hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 503
    assert "local tier unavailable" in resp.json()["error"]
    assert "cloud tier unavailable" in resp.json()["error"]

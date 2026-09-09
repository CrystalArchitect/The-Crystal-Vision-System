import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret")
os.environ.setdefault("ADMIN_USERNAME", "admin")
# bcrypt hash of "test-password", generated for this test suite only
os.environ.setdefault(
    "ADMIN_PASSWORD_HASH",
    "$2b$12$KIXQeZ8N7z0m1G6f2N4o0eYh3l1qz1s1o1s1s1s1s1s1s1s1s1s1u",
)
os.environ.setdefault("DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(__file__), 'test_cc_admin.db')}")

from fastapi.testclient import TestClient  # noqa: E402

from app.core.config import get_settings  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.main import app  # noqa: E402

# Recompute a real hash for "test-password" so login actually succeeds,
# then bust the cached Settings so the route sees it.
os.environ["ADMIN_PASSWORD_HASH"] = hash_password("test-password")
get_settings.cache_clear()

# Using TestClient as a context manager runs FastAPI's startup/shutdown
# events (table creation + seeding), matching what happens when the real
# app boots under uvicorn.
client = TestClient(app)
client.__enter__()


def _token() -> str:
    resp = client.post(
        "/api/v1/admin/login",
        json={"username": "admin", "password": "test-password"},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def test_login_rejects_bad_credentials():
    resp = client.post("/api/v1/admin/login", json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401


def test_diagnostics_requires_auth():
    resp = client.get("/api/v1/admin/diagnostics")
    assert resp.status_code == 401


def test_full_flow():
    token = _token()
    headers = {"Authorization": f"Bearer {token}"}

    diag = client.get("/api/v1/admin/diagnostics", headers=headers)
    assert diag.status_code == 200
    assert "cpu_percent" in diag.json()

    containers = client.get("/api/v1/admin/containers", headers=headers)
    assert containers.status_code == 200
    ids = [c["id"] for c in containers.json()]
    assert "cc-container-01" in ids

    terminal = client.get("/api/v1/admin/containers/cc-container-01/terminal", headers=headers)
    assert terminal.status_code == 200
    assert terminal.json()["container_id"] == "cc-container-01"


def test_terminal_404_for_unknown_container():
    token = _token()
    resp = client.get(
        "/api/v1/admin/containers/does-not-exist/terminal",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 404


def test_404_body_has_no_stack_trace():
    resp = client.get("/api/v1/does-not-exist")
    assert resp.status_code == 404
    body = resp.json()
    assert "error" in body and "request_id" in body
    assert "Traceback" not in resp.text

# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The local API is reachable from the browser already on this machine.

Binding to 127.0.0.1 keeps other machines out. It does nothing about a
page the human happens to be visiting, which can POST to a localhost port
cross-origin whenever it likes. CORS governs whether that page may *read*
the reply — never whether the request runs.

So every state-changing route has to refuse the content types a
cross-origin form can send. These tests pin that down, with particular
attention to `/api/reflect`, which reads no body at all and so was
reachable by a bodyless form POST: it called the model and appended to
the companion's memory on a stranger's say-so.

Nothing here touches Ollama — the companion is a stand-in that records
whether it was asked to do anything.
"""

import pytest

from server import create_app


class _SpyMemory:
    facts: dict = {}
    notes: list = []
    reflections: list = []


class _SpyCompanion:
    """Enough of the mind's surface for the routes under test, and a ledger of
    what was actually invoked."""

    def __init__(self):
        self.calls = []
        self.model = "test-model"
        self.embed_model = "test-embed"
        self.memory_dir = "crystalcore_memory"
        self.memory = _SpyMemory()

    def reflect(self):
        self.calls.append("reflect")
        return "an insight nobody asked for"

    def remember(self, text):
        self.calls.append(("remember", text))

    def remember_fact(self, key, text):
        self.calls.append(("remember_fact", key, text))

    def forget(self, handle):
        self.calls.append(("forget", handle))
        return handle


@pytest.fixture
def client():
    companion = _SpyCompanion()
    app = create_app(companion)
    app.config.update(TESTING=True)
    with app.test_client() as c:
        c.companion = companion
        yield c


# The three content types a cross-origin <form> can send without the
# browser first asking our permission via a preflight.
SIMPLE_CONTENT_TYPES = [
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain",
]


@pytest.mark.parametrize("content_type", SIMPLE_CONTENT_TYPES)
def test_reflect_refuses_simple_content_types(client, content_type):
    """The regression that motivated the guard: /api/reflect ignores the
    request body entirely, so nothing else stood between a cross-site
    form POST and a write to the companion's memory."""
    resp = client.post("/api/reflect", data="", content_type=content_type)
    assert resp.status_code == 415
    assert client.companion.calls == [], "a cross-origin form POST reached reflect()"


def test_reflect_refuses_a_request_with_no_content_type_at_all(client):
    resp = client.post("/api/reflect")
    assert resp.status_code == 415
    assert client.companion.calls == []


def test_reflect_still_works_for_the_real_client(client):
    """The guard must not cost the webapp anything — it speaks JSON."""
    resp = client.post("/api/reflect", json={})
    assert resp.status_code == 200
    assert resp.get_json()["insights"] == "an insight nobody asked for"
    assert client.companion.calls == ["reflect"]


@pytest.mark.parametrize("route", ["/api/teach", "/api/forget", "/api/profile/delete"])
@pytest.mark.parametrize("content_type", SIMPLE_CONTENT_TYPES)
def test_other_mutating_routes_refuse_simple_content_types(client, route, content_type):
    """These were already protected, but only by accident: they parse a
    JSON body and 400 on the None that a form body yields. Asserting the
    415 keeps that from silently regressing into a 400-shaped accident
    again if a route ever stops reading its body."""
    resp = client.post(route, data="handle=n1", content_type=content_type)
    assert resp.status_code == 415
    assert client.companion.calls == []


def test_reads_are_untouched(client):
    """GET is not state-changing and must not require a content type."""
    resp = client.get("/api/memories")
    assert resp.status_code == 200
    assert resp.get_json() == {"facts": [], "notes": [], "reflections": []}


def test_preflight_still_answers_for_a_localhost_origin(client):
    """The JSON requirement only works because the browser will ask
    permission first, so the preflight has to keep succeeding and keep
    naming the webapp's own origin."""
    origin = "http://localhost:5173"
    resp = client.options("/api/reflect", headers={"Origin": origin})
    assert resp.status_code in (200, 204)
    assert resp.headers["Access-Control-Allow-Origin"] == origin
    assert "Content-Type" in resp.headers["Access-Control-Allow-Headers"]


def test_preflight_does_not_bless_a_foreign_origin(client):
    """And it must keep refusing to name anyone else — that refusal is
    what stops the attacking page from ever sending the JSON request."""
    resp = client.options("/api/reflect", headers={"Origin": "https://evil.example"})
    assert "Access-Control-Allow-Origin" not in resp.headers

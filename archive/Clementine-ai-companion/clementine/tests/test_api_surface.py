# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The API description has to match the API.

`api_surface.ROUTES` feeds the discovery index, the OpenAPI document and
`API.md`. All three are therefore only as true as that table, and a table
maintained by hand drifts the moment someone adds a route and forgets it.

So the check runs in both directions against Flask's own url_map:

- a route registered in `server.py` with no entry here fails, so the
  index can never omit something that exists;
- an entry here for a route nobody registered fails, so the index can
  never advertise something that does not.

That second direction is the one that matters to this project. A
documented endpoint with no implementation behind it is exactly the
failure the Incognita Rule names: a line someone drew pretending it was
surveyed. It is also the failure mode a newcomer pays for, because they
build against the document and discover the gap at runtime.

Nothing here starts a model or touches Ollama; the companion is a
stand-in, as in test_server_csrf.py.
"""

import json
import pathlib

import pytest

import api_surface
from server import create_app


class _SpyMemory:
    facts: dict = {}
    notes: list = []
    reflections: list = []


class _SpyPersonality:
    name = "Clementine"
    avatar = "🍊"
    description = "a stand-in"
    human_name = ""


class _SpyCompanion:
    """Only the surface the documented routes read."""

    def __init__(self):
        self.model = "test-model"
        self.embed_model = "test-embed"
        self.memory_dir = "crystalcore_memory"
        self.memory = _SpyMemory()
        self.personality = _SpyPersonality()

    def time_since_last(self):
        return "just now"


@pytest.fixture
def client():
    app = create_app(_SpyCompanion())
    app.testing = True
    return app.test_client()


def _documented() -> set[tuple[str, str]]:
    """(method, path) pairs the table claims exist, aliases included."""
    pairs = set()
    for route in api_surface.ROUTES:
        for path in (route.path, *route.aliases):
            pairs.add((route.method, path))
    return pairs


def _registered(app) -> set[tuple[str, str]]:
    """(method, path) pairs Flask actually serves.

    Excluded, deliberately:

    - HEAD and OPTIONS, which Flask adds to every GET rule by itself and
      which no caller needs told about;
    - `/static/<path:filename>`, which Flask registers whether or not the
      app has static files;
    - the `/api/<path:_any>` preflight catch-all, which answers OPTIONS
      for every route rather than being a route of its own. It is checked
      on its own below, so excluding it here hides nothing.
    """
    pairs = set()
    for rule in app.url_map.iter_rules():
        if rule.endpoint in ("static", "preflight"):
            continue
        for method in rule.methods - {"HEAD", "OPTIONS"}:
            pairs.add((method, str(rule.rule)))
    return pairs


def test_every_registered_route_is_documented():
    app = create_app(_SpyCompanion())
    undocumented = _registered(app) - _documented()
    assert not undocumented, (
        "these routes exist but api_surface.ROUTES does not describe them, so "
        f"the index and OpenAPI document both omit them: {sorted(undocumented)}")


def test_every_documented_route_exists():
    app = create_app(_SpyCompanion())
    imaginary = _documented() - _registered(app)
    assert not imaginary, (
        "api_surface.ROUTES describes these, but nothing serves them — a "
        f"client built from the docs would 404: {sorted(imaginary)}")


def test_index_is_reachable_at_api(client):
    """`/` is deliberately NOT an alias here.

    In the monorepo fork this suite came from, `/` answered the index,
    because that server has no interface to serve. This one serves the
    built webapp from the same origin, so `/` belongs to the face: someone
    opening the printed address should meet the companion, not a JSON
    listing of endpoints.
    """
    res = client.get("/api")
    assert res.status_code == 200
    body = res.get_json()
    assert body["name"] == "Clementine"
    assert body["routes"], "the index listed no routes"


def test_root_serves_the_interface_not_the_index(client):
    res = client.get("/")
    assert not res.is_json, "/ must not answer the API index here"
    # 200 with a built webapp/dist, 503 with the "not built yet" notice.
    assert res.status_code in (200, 503)


def test_index_describes_every_route_with_a_summary(client):
    routes = client.get("/api").get_json()["routes"]
    assert len(routes) == len(api_surface.ROUTES)
    for entry in routes:
        assert entry["summary"].strip(), f"{entry['path']} has no summary"
        assert entry["method"] in ("GET", "POST")
        assert isinstance(entry["mutates"], bool)


def test_index_marks_exactly_the_writing_routes(client):
    """`mutates` is a promise to the caller, so pin which routes make it."""
    routes = client.get("/api").get_json()["routes"]
    mutating = {r["path"] for r in routes if r["mutates"]}
    assert mutating == {
        "/api/chat/stream", "/api/reflect", "/api/teach", "/api/forget",
        "/api/import", "/api/profile", "/api/profile/meta",
        "/api/profile/delete",
    }


def test_every_mutating_route_is_a_post(client):
    """The JSON-required guard in server.py only covers non-GET requests.

    A route that writes but is registered as GET would slip past it, so
    the two facts are tied together here rather than trusted to stay
    aligned on their own.
    """
    for route in api_surface.ROUTES:
        if route.mutates:
            assert route.method == "POST", (
                f"{route.path} writes but is documented as {route.method}; "
                "the require_json_for_writes guard skips GET")


def test_streaming_route_declares_it_is_not_json(client):
    """The one route whose body is not JSON has to say so.

    A client that assumes `application/json` here gets a parse error on
    the first reply, which is a miserable first experience and entirely
    avoidable.
    """
    entry = next(r for r in client.get("/api").get_json()["routes"]
                 if r["path"] == "/api/chat/stream")
    assert entry["returns"].startswith("text/plain")


def test_openapi_document_is_valid_enough_to_load(client):
    res = client.get("/api/openapi.json")
    assert res.status_code == 200
    doc = res.get_json()
    assert doc["openapi"] == "3.1.0"
    assert doc["info"]["title"].startswith("Clementine")
    # Every documented path is present, with its method under it.
    for route in api_surface.ROUTES:
        assert route.path in doc["paths"], route.path
        assert route.method.lower() in doc["paths"][route.path], route.path


def test_openapi_operation_ids_are_unique():
    """Generators produce duplicates easily, and duplicate operationIds
    break every client generator that reads the document."""
    doc = api_surface.openapi("Clementine", "test")
    ids = [op["operationId"]
           for methods in doc["paths"].values()
           for op in methods.values()]
    assert len(ids) == len(set(ids)), f"duplicate operationIds: {ids}"


def test_openapi_declares_request_bodies_for_routes_that_take_one():
    doc = api_surface.openapi("Clementine", "test")
    for route in api_surface.ROUTES:
        operation = doc["paths"][route.path][route.method.lower()]
        if route.request:
            assert "requestBody" in operation, route.path
        else:
            assert "requestBody" not in operation, route.path


def test_index_and_openapi_are_json_serialisable():
    """Both are handed to jsonify, which raises on anything exotic. Catch
    that here rather than at the first request of a newcomer's session."""
    json.dumps(api_surface.index("Clementine", "v", "1"))
    json.dumps(api_surface.openapi("Clementine", "v"))


def test_every_documented_route_answers_a_preflight(client):
    """A browser client must get a usable preflight on every route.

    Worth stating what actually serves it, because it is not the obvious
    answer: the `/api/<path:_any>` catch-all in `server.py` is *not* what
    handles preflight for these routes. Flask registers automatic OPTIONS
    on every rule, and an exact rule beats the path converter, so each
    route answers its own OPTIONS with 200. The catch-all only ever fires
    for paths that match nothing else (asserted below).

    Either way the CORS headers come from the `after_request` hook, so
    what this pins is the contract a browser depends on — a 2xx and an
    allowed origin — rather than whichever mechanism happens to produce
    it. An earlier version of this test asserted 204 everywhere, which
    described a code path that never ran.
    """
    origin = "http://127.0.0.1:5174"
    for route in api_surface.ROUTES:
        res = client.options(route.path, headers={"Origin": origin})
        assert 200 <= res.status_code < 300, (route.path, res.status_code)
        assert res.headers.get("Access-Control-Allow-Origin") == origin, route.path


def test_catch_all_preflight_covers_unmatched_paths(client):
    """What the catch-all is actually for."""
    origin = "http://127.0.0.1:5174"
    res = client.options("/api/not-a-real-route", headers={"Origin": origin})
    assert res.status_code == 204
    assert res.headers.get("Access-Control-Allow-Origin") == origin


def test_cors_refuses_a_non_localhost_origin(client):
    """Sovereignty means local only — an outside page gets no read access."""
    res = client.options("/api/teach",
                         headers={"Origin": "https://example.com"})
    assert res.headers.get("Access-Control-Allow-Origin") is None


def test_unknown_route_answers_json_and_points_at_the_index(client):
    """Being lost is when a pointer helps most, and it must still be JSON.

    Note the status code: a mistyped path under `/api/` hits the OPTIONS
    preflight catch-all, so Werkzeug rejects the method and returns 405
    rather than the 404 a typo deserves. Both are handled; the assertion
    accepts either so it pins the useful behaviour instead of freezing a
    quirk of the routing table.
    """
    # Only paths under /api/ are the API's to answer. Anything else is a
    # client-side route belonging to the interface, which this fork serves
    # itself — so /nope falls back to index.html rather than 404ing, and
    # asserting JSON there would be asserting the other fork's layout.
    res = client.get("/api/nope")
    assert res.status_code in (404, 405)
    assert res.is_json, "a mistyped /api/ path answered with a non-JSON body"
    body = res.get_json()
    assert "/api/nope" in body["detail"]
    assert "/api" in body["hint"]


def test_committed_api_md_matches_the_table():
    """The checked-in reference has to be what the generator produces.

    Without this the markdown is just a third place the truth can rot,
    and the one a newcomer is most likely to read.
    """
    committed = (pathlib.Path(__file__).resolve().parents[1] / "API.md")
    assert committed.exists(), "API.md is missing — run: python api_surface.py > API.md"
    assert committed.read_text() == api_surface.render_markdown(), (
        "API.md is out of date with api_surface.ROUTES. "
        "Regenerate it: python api_surface.py > API.md")


def test_api_md_names_every_route():
    """Cheap belt to the generator's braces: if the renderer ever stopped
    emitting a section, the equality test above would still pass once
    someone regenerated the file. This one would not."""
    text = api_surface.render_markdown()
    for route in api_surface.ROUTES:
        assert f"### `{route.method} {route.path}`" in text, route.path


def test_discovery_routes_do_not_require_json(client):
    """Discovery has to work from a bare `curl` with no headers set — that
    is the entire point of it.

    `/` is not in this list, unlike in the fork this came from. There it was
    the index and always answered 200; here it serves the built interface,
    so it answers 503 when webapp/dist has not been built. Asserting 200 on
    it would make this test pass or fail depending on whether someone had
    run `npm run build` — which is not a fact about the API.
    """
    for path in ("/api", "/api/openapi.json"):
        assert client.get(path).status_code == 200, path

# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Which of this server's capabilities a person can actually get to.

tests/test_api_surface.py asks whether a route exists and is described.
Nothing asked whether anyone could *call* it, and for a long time the answer
was mostly no: ten of fourteen working endpoints had no interface, including
seeing what the companion remembered, deleting a memory, leaving with it,
and reading the consent record. Tests answer "does this work when called";
they do not answer "can anyone call it".

That gap was found by hand and then miscounted twice, in both directions,
because the count was a substring search re-run from memory — `/api/profile`
is a substring of `/api/profile/meta`, so wiring up one silently marked two
more as reached. A number that lives in a document and is produced by an
ad-hoc grep drifts by exactly this much.

So the measurement is here instead. It fails when the set changes, in either
direction, which is the point: wiring up an endpoint should be a moment when
somebody updates content/UNBUILT.md, and quietly losing one should not be
possible at all.
"""

import pathlib
import re

import api_surface

#: Described in the surface but not provided by it — the index, the OpenAPI
#: document, and the static handler that serves the interface itself.
NOT_CAPABILITIES = {"/api", "/api/openapi.json", "/<path:asset>"}

#: Endpoints no part of the built interface calls, as of 11 August 2026.
#: Keep content/UNBUILT.md in step with this set.
KNOWN_UNREACHABLE = {
    ("POST", "/api/teach"),    # reachable by talking to them instead
    ("POST", "/api/reflect"),  # likewise
}


def _paths_in(text: str) -> set[str]:
    """Every /api path mentioned in some text, matched exactly.

    Exactly, because the bug this replaces was a substring test: a component
    that calls /api/profile/meta does not thereby call /api/profile, and
    counting it as though it did overstated what a person could reach.

    Split out from the caller so the property can be tested on a controlled
    string. It first was not, and the test pinning it compared against the
    real interface — which held only while /api/profile happened to be
    uncalled, and stopped meaning anything the moment somebody wired it up.
    A test of a matcher should not depend on what the matcher is pointed at.
    """
    # Stop at a quote, a query string, or a template placeholder.
    return {p.rstrip("/") for p in re.findall(r"/api/[A-Za-z0-9/_-]*", text)}


def _endpoints_the_interface_calls() -> set[str]:
    src_dir = pathlib.Path(__file__).resolve().parents[1] / "webapp" / "src"
    return _paths_in(" ".join(p.read_text(errors="ignore")
                              for p in src_dir.rglob("*") if p.is_file()))


def _capabilities() -> set[tuple[str, str]]:
    """Counted as (method, path), not as paths.

    GET /api/profile lists the companions on this machine and POST
    /api/profile switches between them: one address, two capabilities, and
    collapsing them undercounts what is unreached. Writing the first version
    of this in paths gave 13 where the number being quoted was 14, which is
    the same class of mistake as the substring bug and was caught by the
    same test disagreeing with a figure stated by hand.

    The interface is scanned for paths rather than for methods, so both
    verbs at one address stand or fall together. That is imprecise and is
    stated rather than papered over; no address here is half-reached.
    """
    return {(r.method, r.path) for r in api_surface.ROUTES
            if r.path not in NOT_CAPABILITIES}


def test_the_unreachable_set_is_exactly_what_is_recorded():
    """Fails in both directions on purpose.

    If something was just wired up, delete it from KNOWN_UNREACHABLE and say
    so in content/UNBUILT.md. If something appears here that was reachable
    before, an interface stopped calling it and a person quietly lost a way
    to do something.
    """
    called = _endpoints_the_interface_calls()
    unreachable = {(m, p) for m, p in _capabilities() if p not in called}

    assert unreachable == KNOWN_UNREACHABLE, (
        "the set of capabilities with no interface has changed.\n"
        f"  newly reachable: {sorted(KNOWN_UNREACHABLE - unreachable)}\n"
        f"  newly stranded : {sorted(unreachable - KNOWN_UNREACHABLE)}\n"
        "Update KNOWN_UNREACHABLE and content/UNBUILT.md together."
    )


def test_the_count_quoted_in_the_register_is_the_measured_one():
    """content/UNBUILT.md states a ratio. It is produced here rather than by
    hand, because it was miscounted by hand twice."""
    total = len(_capabilities())
    reachable = total - len(KNOWN_UNREACHABLE)

    assert (reachable, total) == (12, 14), (
        f"reachability is now {reachable} of {total}; "
        "update this and content/UNBUILT.md in the same commit"
    )


def test_a_substring_of_a_path_is_not_counted_as_that_path():
    """The exact bug this file exists to prevent, pinned on its own.

    Calling /api/profile/meta is not calling /api/profile. A substring match
    reports both as reached, which is how the ratio once jumped from 8 to 11
    when only one endpoint had been wired up.

    Asserted against a fixed string rather than against the interface. The
    first version of this test compared to the real webapp and held only
    while /api/profile happened to be uncalled — it started failing the day
    somebody wired it up, having stopped testing the matcher some time
    before that.
    """
    called = _paths_in("await fetch('/api/profile/meta', {method: 'POST'})")

    assert called == {"/api/profile/meta"}
    assert "/api/profile" not in called


def test_every_reachable_endpoint_is_a_real_route():
    """The other direction: an interface calling something the server does
    not serve would 404 in front of a person rather than in a test."""
    served = {r.path for r in api_surface.ROUTES}
    for path in _endpoints_the_interface_calls():
        if path.startswith("/api"):
            assert path in served, f"the interface calls {path}, which is not a route"

# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for CrystalBridge — the consent gate and the mind path.

    cd core && python3 -m crystalcore.selftest

Covers the two bugs this suite was written to catch and keep caught, and
the five-check gate specified in docs/CONSENT-GATE-SPEC.md:

  1. The bridge must reach the same memory the human sees. It once loaded
     the mind by file path, from core/apps/lumina/crystalcore — a
     directory that never existed — so every tool touching the companion
     (recall, teach, message) crashed at runtime. That whole class of bug
     is now gone by construction: the mind is `crystalcore.mind`, an
     ordinary subpackage of this one, imported normally. What remains
     path-dependent is only the *profiles folder*, which still lives
     beside the interface, so that is what is checked here.

  2. ConsentGate.check() enforces revocation, approval, provenance, and
     permission in that order, and require_scope() enforces the fifth
     check — visibility scope and memory types — for memory-touching
     tools. These tests pin the order — a wrong token from an approved
     guest must refuse as provenance, never as permission — and pin
     fail-closed defaults: no stored hash refuses, empty scope refuses,
     empty types refuse, memories without a visibility field are private,
     a corrupt revocation ledger refuses everyone, and the ask is on disk
     before the answer exists.

Stdlib-only except for `mcp`, which importing crystalcore.bridge
requires (see requirements-bridge.txt). The mind additionally needs
`requests`; where that isn't installed, that one sub-check reports SKIP
rather than failing.
"""

from __future__ import annotations

from pathlib import Path

from crystalcore.config import BridgeConfig, GuestGrant
from crystalcore.gate import ConsentGate, token_hash

SECRET = "selftest-secret"


def _gate(
    tools: list[str] | None = None,
    approved: bool = True,
    *,
    secret: str | None = SECRET,
    read_scope: list[str] | None = None,
    write_scope: list[str] | None = None,
    read_types: list[str] | None = None,
    write_types: list[str] | None = None,
    profile_dir: Path | None = None,
) -> ConsentGate:
    """A ConsentGate over an in-memory config for one guest 'claude'.

    By default profile_dir points nowhere real — checks that pass
    audit=False never write, and the revocation ledger read treats an
    absent file as the empty ledger. Tests exercising the ledger or the
    pending record pass a real tmp `profile_dir` instead.
    `secret=None` models a guest with no provenance configured.
    """
    config = BridgeConfig(
        profile="selftest",
        human_name="selftest",
        interactive_approval=False,
        guests={"claude": GuestGrant(
            approved=approved,
            tools=list(tools or []),
            read_scope=list(read_scope or []),
            write_scope=list(write_scope or []),
            read_types=list(read_types or []),
            write_types=list(write_types or []),
            token_hash=token_hash(secret) if secret else "",
        )},
        profile_dir=profile_dir or Path("/nonexistent-selftest-profile"),
    )
    return ConsentGate(config)


def test_bridge_refuses_to_run_without_a_nominated_memory_folder():
    """The regression test for bug #1, in the form that survives the move.

    It used to assert that a path computed inside this repository resolved
    to a real directory — the interface the profiles hung off. The companion
    no longer lives here, so there is no such path to check, and computing
    one would be the bug rather than the test for it: it would resolve
    somewhere absent, the mind would create it, and a guest would be served
    an empty companion in silence.

    What matters now is the opposite property. Unconfigured, the bridge must
    stop. Both failure modes are checked, because "set but wrong" is the one
    a person actually hits.
    """
    import os
    import tempfile

    from crystalcore.bridge import MEMORY_DIR_ENV, _profiles_root

    before = os.environ.get(MEMORY_DIR_ENV)
    try:
        os.environ.pop(MEMORY_DIR_ENV, None)
        try:
            _profiles_root()
        except SystemExit:
            pass
        else:
            raise AssertionError(
                "the bridge resolved a memory folder with nothing set; it "
                "must refuse rather than guess")

        os.environ[MEMORY_DIR_ENV] = "/nonexistent/nobody/nominated/this"
        try:
            _profiles_root()
        except SystemExit:
            pass
        else:
            raise AssertionError(
                "the bridge accepted a path that is not a directory; it "
                "must refuse rather than let the mind create one")

        with tempfile.TemporaryDirectory() as real:
            os.environ[MEMORY_DIR_ENV] = real
            assert _profiles_root() == Path(real), (
                "a nominated, existing folder must be used as given")
    finally:
        if before is None:
            os.environ.pop(MEMORY_DIR_ENV, None)
        else:
            os.environ[MEMORY_DIR_ENV] = before


def test_mind_imports_and_exposes_the_companion_class():
    """The end-to-end check for bug #1: the mind is reachable as a package.

    Skips (does not fail) when a dependency the mind imports at module
    level — currently `requests` — isn't installed, so a lightweight
    core-only environment can still run this suite. An import failure for
    any other reason is NOT skipped.
    """
    try:
        from crystalcore import mind
    except ModuleNotFoundError as exc:
        if exc.name in {"requests", "flask"}:
            print(
                f"  SKIP mind import — dep '{exc.name}' not installed "
                "(the path check above already proves the layout)"
            )
            return
        raise
    assert hasattr(mind, "CrystalCore"), (
        "crystalcore.mind imported but exposes no `CrystalCore` class."
    )


def test_approved_guest_with_allowed_tool_and_token_is_allowed():
    result = _gate(tools=["recall", "teach"]).check(
        "claude", "recall", token=SECRET, audit=False)
    assert result.allowed and result.decision == "allow" and result.check == "ok"


def test_approved_guest_with_disallowed_tool_is_refused():
    result = _gate(tools=["recall"]).check(
        "claude", "teach", token=SECRET, audit=False)
    assert not result.allowed and result.check == "permission"


def test_status_is_always_allowed_for_a_proven_approved_guest():
    """`status` is granted implicitly (gate.py's `| {"status"}`), even when
    it isn't in the guest's tool list — but only past provenance."""
    result = _gate(tools=[]).check("claude", "status", token=SECRET, audit=False)
    assert result.allowed, "status must be allowed for any proven, approved guest"


def test_status_is_refused_when_provenance_fails():
    """`status` is not a side door. Wrong token and missing token both
    refuse at provenance — the implicit tool grant is after the name is
    proven."""
    result = _gate(tools=[]).check("claude", "status", token="wrong", audit=False)
    assert not result.allowed and result.check == "provenance"
    result = _gate(tools=[]).check("claude", "status", audit=False)
    assert not result.allowed and result.check == "provenance"


def test_status_is_refused_when_revoked():
    import tempfile

    from crystalcore.revocation import append_revocation, revocations_path

    with tempfile.TemporaryDirectory() as tmp:
        append_revocation(revocations_path(Path(tmp)),
                          guest="claude", action="revoke", reason="test")
        result = _gate(tools=[], profile_dir=Path(tmp)).check(
            "claude", "status", token=SECRET, audit=False)
        assert not result.allowed and result.check == "revocation"


def test_unknown_guest_is_refused():
    result = _gate(tools=["recall"]).check(
        "stranger", "recall", token=SECRET, audit=False)
    assert not result.allowed and result.check == "approval"


def test_present_but_unapproved_guest_is_refused():
    result = _gate(tools=["recall"], approved=False).check(
        "claude", "recall", token=SECRET, audit=False)
    assert not result.allowed and result.check == "approval"


def test_missing_token_refuses_as_provenance():
    result = _gate(tools=["recall"]).check("claude", "recall", audit=False)
    assert not result.allowed and result.check == "provenance"
    assert result.decision == "refuse-provenance"


def test_wrong_token_refuses_as_provenance_not_permission():
    """Check order pinned: an approved guest presenting the wrong token
    must refuse at provenance — even for a tool it isn't permitted —
    because the later checks are meaningless against an unverified name."""
    result = _gate(tools=["recall"]).check(
        "claude", "some-unpermitted-tool", token="wrong", audit=False)
    assert not result.allowed and result.check == "provenance"


def test_guest_with_no_minted_token_refuses_fail_closed():
    """Strict provenance from day one: a grant without a stored hash
    refuses. Enforcement is never optional — an unconfigured guest is an
    unproven guest."""
    result = _gate(tools=["recall"], secret=None).check(
        "claude", "recall", token="anything", audit=False)
    assert not result.allowed and result.check == "provenance"


def test_empty_scope_refuses_even_after_the_gate_allows():
    gate = _gate(tools=["recall"])
    assert gate.check("claude", "recall", token=SECRET, audit=False).allowed
    result = gate.require_scope("claude", "recall", "read", audit=False)
    assert not result.allowed and result.check == "scope"
    assert result.decision == "refuse-scope"


def test_granted_scope_passes():
    gate = _gate(tools=["recall"], read_scope=["shared"],
                 read_types=["semantic"])
    result = gate.require_scope("claude", "recall", "read",
                                types=("semantic",), audit=False)
    assert result.allowed


def test_scope_refusal_carries_check_request_id():
    """Door 5 joins the ask check() already recorded. A scope refuse
    without that id was the hole: as_refusal_payload() carried "".
    """
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        gate = _gate(tools=["recall"], profile_dir=Path(tmp))
        checked = gate.check("claude", "recall", token=SECRET)
        assert checked.allowed
        result = gate.require_scope(
            "claude", "recall", "read", request_id=checked.request_id)
        assert not result.allowed and result.check == "scope"
        assert result.request_id == checked.request_id
        assert result.as_refusal_payload()["request_id"] == checked.request_id
        pending = [json.loads(l) for l in
                   (Path(tmp) / "pending.jsonl").read_text(
                       encoding="utf-8").splitlines()]
        assert pending[0]["detail"]["request_id"] == checked.request_id
        audit = [json.loads(l) for l in
                 (Path(tmp) / "audit.jsonl").read_text(
                     encoding="utf-8").splitlines()]
        scope_lines = [a for a in audit if a["detail"].get("check") == "scope"]
        assert scope_lines, "a scope refuse must be audited"
        assert scope_lines[-1]["detail"]["request_id"] == checked.request_id


def test_scope_allow_is_audited_with_request_id():
    """Successful require_scope used to skip the audit. An allow is a
    decision too; it carries the same id as the pending line.
    """
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        gate = _gate(tools=["recall"], read_scope=["shared"],
                     read_types=["semantic"], profile_dir=Path(tmp))
        checked = gate.check("claude", "recall", token=SECRET)
        assert checked.allowed
        result = gate.require_scope(
            "claude", "recall", "read", types=("semantic",),
            request_id=checked.request_id)
        assert result.allowed and result.request_id == checked.request_id
        audit = [json.loads(l) for l in
                 (Path(tmp) / "audit.jsonl").read_text(
                     encoding="utf-8").splitlines()]
        assert audit[-1]["detail"]["request_id"] == checked.request_id
        assert audit[-1]["detail"]["check"] == "ok"
        assert audit[-1]["decision"] == "allow"


def test_memories_without_visibility_are_private():
    """The migration default, pinned at the filter itself: an entry with no
    visibility field must not survive a shared-only view. Runs against the
    mind's real `_memory_block` when its deps are installed; otherwise the
    filter logic is pinned directly."""
    try:
        from crystalcore.mind import CrystalCore  # noqa: F401  (dep probe)
    except ModuleNotFoundError as exc:
        if exc.name in {"requests", "flask"}:
            legacy = {"text": "old private thing", "tags": []}
            shared = {"text": "shared thing", "tags": [], "visibility": "shared"}
            visible = {"shared"}
            kept = [m for m in (legacy, shared)
                    if m.get("visibility", "private") in visible]
            assert kept == [shared]
            print(f"  SKIP mind-backed check — dep '{exc.name}' not installed "
                  "(filter default pinned directly instead)")
            return
        raise
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        companion = CrystalCore(memory_dir=tmp)
        companion._embed_ok = False  # no Ollama in tests; skip embeddings
        companion.memory.notes.append(
            {"text": "old private thing", "tags": []})  # pre-migration shape
        companion.memory.notes.append(
            {"text": "shared thing", "tags": [], "visibility": "shared"})
        guest_view = companion._memory_block(visible={"shared"})
        human_view = companion._memory_block()
        assert "old private thing" not in guest_view
        assert "shared thing" in guest_view
        assert "old private thing" in human_view, (
            "the human's own unfiltered view must still see everything")


# ---- the fifth door: revocation, durable and restart-free ----


def test_revoked_guest_refuses_without_restart():
    """Revocation is a runtime property: the same gate instance that just
    allowed a guest must refuse it the moment the ledger says so, with no
    restart in between."""
    import tempfile

    from crystalcore.revocation import append_revocation, revocations_path

    with tempfile.TemporaryDirectory() as tmp:
        gate = _gate(tools=["recall"], profile_dir=Path(tmp))
        assert gate.check("claude", "recall", token=SECRET, audit=False).allowed
        append_revocation(revocations_path(Path(tmp)),
                          guest="claude", action="revoke", reason="test")
        result = gate.check("claude", "recall", token=SECRET, audit=False)
        assert not result.allowed and result.check == "revocation"
        assert result.decision == "refuse-revoked"


def test_revocation_survives_restart():
    """A revocation is durable: a brand-new gate over the same profile —
    the restart, modelled — still refuses. Hand-editing config and
    restarting used to be the only mechanism; now the restart is the case
    that must NOT clear it."""
    import tempfile

    from crystalcore.revocation import append_revocation, revocations_path

    with tempfile.TemporaryDirectory() as tmp:
        append_revocation(revocations_path(Path(tmp)),
                          guest="claude", action="revoke", reason="test")
        fresh_gate = _gate(tools=["recall"], profile_dir=Path(tmp))
        result = fresh_gate.check("claude", "recall", token=SECRET, audit=False)
        assert not result.allowed and result.check == "revocation"


def test_reinstate_restores_access():
    """Latest record per guest wins: revoke then reinstate allows again,
    and the ledger keeps both records — reinstatement is an appended act,
    never an erased one."""
    import tempfile

    from crystalcore.revocation import append_revocation, revocations_path

    with tempfile.TemporaryDirectory() as tmp:
        path = revocations_path(Path(tmp))
        append_revocation(path, guest="claude", action="revoke", reason="test")
        append_revocation(path, guest="claude", action="reinstate", reason="ok")
        gate = _gate(tools=["recall"], profile_dir=Path(tmp))
        assert gate.check("claude", "recall", token=SECRET, audit=False).allowed
        assert len(path.read_text(encoding="utf-8").splitlines()) == 2


def test_corrupt_revocation_ledger_refuses_all():
    """Fail-closed at its sharpest: a ledger that cannot be parsed refuses
    every guest — even one with a perfect token — because a gate that
    cannot know who is revoked must not guess."""
    import tempfile

    from crystalcore.revocation import revocations_path

    with tempfile.TemporaryDirectory() as tmp:
        revocations_path(Path(tmp)).write_text("not json at all\n",
                                               encoding="utf-8")
        gate = _gate(tools=["recall"], profile_dir=Path(tmp))
        result = gate.check("claude", "recall", token=SECRET, audit=False)
        assert not result.allowed and result.check == "revocation"
        assert "cannot be read" in result.reason


# ---- the observable ask: recorded before anything is decided ----


def test_ask_recorded_before_refusal():
    """The ask is on disk before the answer exists. A refused request must
    leave a `received` line in pending.jsonl, and the audit decision line
    must carry the same request id, joining ask to answer."""
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        gate = _gate(tools=["recall"], profile_dir=Path(tmp))
        result = gate.check("claude", "recall", token="wrong-token")
        assert not result.allowed
        pending_lines = [json.loads(l) for l in
                         (Path(tmp) / "pending.jsonl").read_text(
                             encoding="utf-8").splitlines()]
        assert pending_lines and pending_lines[0]["decision"] == "received"
        request_id = pending_lines[0]["detail"]["request_id"]
        audit_lines = [json.loads(l) for l in
                       (Path(tmp) / "audit.jsonl").read_text(
                           encoding="utf-8").splitlines()]
        assert audit_lines[-1]["detail"]["request_id"] == request_id
        assert result.request_id == request_id, (
            "the refusal a guest sees must carry the id of its recorded ask")
        assert result.as_refusal_payload()["request_id"] == request_id


def test_pending_and_audit_files_are_never_group_or_world_readable():
    """Guest names, tools, and request ids. Same bits as identity.json."""
    import os
    import stat
    import tempfile

    from crystalcore.audit import append_audit

    with tempfile.TemporaryDirectory() as tmp:
        pending = Path(tmp) / "pending.jsonl"
        append_audit(pending, guest="claude", tool="recall",
                     arguments={}, decision="received")
        mode = stat.S_IMODE(pending.stat().st_mode)
        assert mode & 0o077 == 0, f"pending.jsonl is {oct(mode)}"
        loose = Path(tmp) / "audit.jsonl"
        loose.write_text("{}\n", encoding="utf-8")
        os.chmod(loose, 0o644)
        append_audit(loose, guest="claude", tool="recall",
                     arguments={}, decision="refuse")
        assert stat.S_IMODE(loose.stat().st_mode) & 0o077 == 0


def test_ask_survives_evaluation_crash():
    """Even when the gate itself blows up mid-evaluation, the ask is
    already recorded — an observable ask is not conditional on the gate
    surviving to answer it."""
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        gate = _gate(tools=["recall"], profile_dir=Path(tmp))

        def explode(name):
            raise RuntimeError("config lookup exploded")

        gate.config.guest = explode
        try:
            gate.check("claude", "recall", token=SECRET)
        except RuntimeError:
            pass
        else:
            raise AssertionError("the sabotaged lookup should have raised")
        pending = (Path(tmp) / "pending.jsonl").read_text(encoding="utf-8")
        assert '"received"' in pending, (
            "the ask must be on disk even though evaluation crashed")


def test_unrecordable_ask_refuses():
    """The dual of the crash test: when the ask itself cannot be written,
    the gate refuses rather than fulfilling a request no record shows was
    ever made. Neither swallowing the error nor crashing — a stated
    refusal. profile_dir is a *file* here, so the pending write's mkdir
    fails."""
    import tempfile

    with tempfile.NamedTemporaryFile() as blocked:
        gate = _gate(tools=["recall"], profile_dir=Path(blocked.name))
        result = gate.check("claude", "recall", token=SECRET)
        assert not result.allowed and result.check == "ask-record"
        assert "could not be recorded" in result.reason


# ---- the type dimension: layers as consent, not labels ----


def test_missing_read_types_refuses():
    """A grant written before the type dimension existed has not consented
    to it. Empty read_types refuses, and the reason says what to add."""
    gate = _gate(tools=["recall"], read_scope=["shared"])
    result = gate.require_scope("claude", "recall", "read",
                                types=("semantic",), audit=False)
    assert not result.allowed and result.check == "scope"
    assert "read_types" in result.reason


def test_type_gate_refuses_layer_not_served():
    """A grant for a layer a tool does not serve is an honest refusal, not
    a silently empty result: recall serves semantic; an episodic-only
    grant finds nothing behind that door and is told so."""
    gate = _gate(tools=["recall"], read_scope=["shared"],
                 read_types=["episodic"])
    result = gate.require_scope("claude", "recall", "read",
                                types=("semantic",), audit=False)
    assert not result.allowed and result.decision == "refuse-scope"
    assert "episodic" in result.reason and "semantic" in result.reason


def test_unknown_type_name_stops_startup():
    """'mythic' is a wire-protocol fragment kind in STARLINE.md, not a
    local memory type — and no ungoverned class may enter through config.
    Loading a grant naming an unknown type stops the operator, loudly,
    before any guest is served. Told, or stopped."""
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        profile_dir = Path(tmp) / "default"
        profile_dir.mkdir()
        (profile_dir / "bridge_config.json").write_text(json.dumps({
            "profile": "default",
            "guests": {"claude": {"approved": True,
                                  "read_types": ["mythic"]}},
        }), encoding="utf-8")
        try:
            BridgeConfig.load("default", profiles_dir=Path(tmp))
        except SystemExit as exc:
            assert "mythic" in str(exc)
        else:
            raise AssertionError(
                "an unknown memory type must stop startup, not load quietly")


def test_unknown_visibility_class_stops_startup():
    """The type axis was validated at load; the visibility axis was not.
    A scope naming a class this gate does not govern loaded as a bare
    string, and teach passes write_scope[0] straight to remember(). Same
    rule as types: an unknown class stops the operator, loudly."""
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        profile_dir = Path(tmp) / "default"
        profile_dir.mkdir()
        (profile_dir / "bridge_config.json").write_text(json.dumps({
            "profile": "default",
            "guests": {"claude": {"approved": True,
                                  "read_scope": ["public"]}},
        }), encoding="utf-8")
        try:
            BridgeConfig.load("default", profiles_dir=Path(tmp))
        except SystemExit as exc:
            assert "public" in str(exc)
        else:
            raise AssertionError(
                "an unknown visibility class must stop startup, not load quietly")


def test_guest_may_never_be_configured_to_write_private():
    """CONSENT-GATE-SPEC.md states it as an absolute: a guest is never able
    to write private memories. teach() writes into write_scope[0], so a
    config putting 'private' there would hand a guest the very class the
    human's own conversation defaults to. Enforced at load, not just
    documented."""
    import json
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        profile_dir = Path(tmp) / "default"
        profile_dir.mkdir()
        (profile_dir / "bridge_config.json").write_text(json.dumps({
            "profile": "default",
            "guests": {"claude": {"approved": True,
                                  "write_scope": ["private"]}},
        }), encoding="utf-8")
        try:
            BridgeConfig.load("default", profiles_dir=Path(tmp))
        except SystemExit as exc:
            assert "private" in str(exc)
        else:
            raise AssertionError(
                "write_scope naming 'private' must stop startup")


def test_layers_beyond_semantic_never_reach_guests():
    """recall serves notes and facts — the semantic layer — and nothing
    else. Summaries (episodic) and reflections (reflective) carry no
    per-entry visibility consent yet, so no grant may surface them; the
    conversation (working memory) is never guest-readable at all. Pinned
    at `_memory_block` itself, so a future widening of the guest surface
    trips this test and becomes a decision instead of a side effect.
    Skips when the mind's deps are missing, like the other mind-backed
    check."""
    try:
        from crystalcore.mind import CrystalCore
    except ModuleNotFoundError as exc:
        if exc.name in {"requests", "flask"}:
            print(f"  SKIP mind-backed check — dep '{exc.name}' not installed")
            return
        raise
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        companion = CrystalCore(memory_dir=tmp)
        companion._embed_ok = False
        companion.memory.notes.append(
            {"text": "a shared note", "tags": [], "visibility": "shared"})
        companion.memory.summaries = "an episodic summary of private talk"
        companion.memory.reflections.append(
            {"text": "a reflective insight about the human"})
        companion.memory.conversation.append(
            {"role": "user", "content": "working memory line"})
        guest_view = companion._memory_block(visible={"shared"})
        assert "a shared note" in guest_view
        assert "episodic summary" not in guest_view
        assert "reflective insight" not in guest_view
        assert "working memory line" not in guest_view


def test_write_json_atomic_replaces_only_after_the_bytes_are_complete():
    """`--mint-token` used to write_text the grants file in place.
    A crash mid-write destroyed the previous consent document.

    Declares local so this test is the atomic write, not host trust.
    """
    import json
    import os
    import stat
    import tempfile

    from crystalcore.config import write_json_atomic

    old = os.environ.get("CRYSTAL_HOST_CLASS")
    os.environ["CRYSTAL_HOST_CLASS"] = "local"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bridge_config.json"
            path.write_text('{"keep": true}\n', encoding="utf-8")
            write_json_atomic(path, {"guests": {"claude": {"token_hash": "abc"}}})
            data = json.loads(path.read_text(encoding="utf-8"))
            assert data["guests"]["claude"]["token_hash"] == "abc"
            assert not path.with_name(path.name + ".tmp").exists()
            mode = stat.S_IMODE(path.stat().st_mode)
            assert mode & 0o077 == 0, f"grants file is {oct(mode)}"

            original = path.read_text(encoding="utf-8")

            def boom(*_a, **_k):
                raise OSError("disk full")

            real_fsync = os.fsync
            os.fsync = boom  # type: ignore[assignment]
            try:
                try:
                    write_json_atomic(path, {"destroyed": True})
                except OSError:
                    pass
                else:
                    raise AssertionError("fsync was supposed to raise")
            finally:
                os.fsync = real_fsync
            assert path.read_text(encoding="utf-8") == original
            assert "destroyed" not in path.read_text(encoding="utf-8")
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old


def test_write_json_atomic_refuses_durable_on_pool():
    """Grants file must not land on shared/unknown durable paths."""
    import os

    from crystalcore.config import write_json_atomic

    path = Path("/usr/bridge_config_host_trust_test.json")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            write_json_atomic(path, {"nope": True})
            assert False, "durable grants on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_write_json_atomic_refuses_temp_on_unknown():
    import os
    import tempfile

    from crystalcore.config import write_json_atomic

    d = Path(tempfile.mkdtemp(prefix="bridge_unknown_tmp_"))
    path = d / "bridge_config.json"
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ.pop("CRYSTAL_HOST_CLASS", None)
    os.environ.pop("GITHUB_ACTIONS", None)
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            write_json_atomic(path, {"nope": True})
            assert False, "temp grants on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
            assert "unknown" in str(exc)
        assert not path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_write_json_atomic_allows_temp_on_github_hosted():
    import os
    import tempfile

    from crystalcore.config import write_json_atomic

    d = Path(tempfile.mkdtemp(prefix="bridge_gh_tmp_"))
    path = d / "bridge_config.json"
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        write_json_atomic(path, {"ok": True})
        assert path.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def _companion_cls():
    """Load CrystalCore even when `requests` is not installed.

    save() does not use the network. CI installs mcp, not requests.
    The mind-backed filter tests skip; these pins must still run.
    """
    import sys

    try:
        from crystalcore.mind.companion import CrystalCore
        return CrystalCore
    except (ModuleNotFoundError, AttributeError):
        pass
    from types import ModuleType

    req = ModuleType("requests")
    exc = ModuleType("requests.exceptions")

    class RequestException(Exception):
        pass

    exc.RequestException = RequestException
    req.exceptions = exc
    sys.modules["requests"] = req
    sys.modules["requests.exceptions"] = exc
    for key in [k for k in sys.modules if k.startswith("crystalcore.mind")]:
        del sys.modules[key]
    from crystalcore.mind.companion import CrystalCore
    return CrystalCore


def test_companion_save_refuses_durable_on_pool():
    import os

    CrystalCore = _companion_cls()
    path = Path("/usr/crystal_memory_host_trust_test")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        companion = CrystalCore(memory_dir=str(path))
        try:
            companion.save()
            assert False, "durable memory.json on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not (path / "memory.json").exists()
        assert not (path / "config.json").exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_companion_save_refuses_temp_on_unknown():
    import os
    import tempfile

    CrystalCore = _companion_cls()
    d = Path(tempfile.mkdtemp(prefix="companion_unknown_tmp_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ.pop("CRYSTAL_HOST_CLASS", None)
    os.environ.pop("GITHUB_ACTIONS", None)
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        companion = CrystalCore(memory_dir=str(d))
        try:
            companion.save()
            assert False, "temp memory.json on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
            assert "unknown" in str(exc)
        assert not (d / "memory.json").exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_companion_save_allows_temp_on_github_hosted():
    import os
    import tempfile

    CrystalCore = _companion_cls()
    d = Path(tempfile.mkdtemp(prefix="companion_gh_tmp_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        companion = CrystalCore(memory_dir=str(d))
        companion.save()
        assert (d / "memory.json").exists()
        assert (d / "config.json").exists()
        import stat
        for name in ("memory.json", "config.json"):
            mode = stat.S_IMODE((d / name).stat().st_mode)
            assert mode & 0o077 == 0, f"{name} is {oct(mode)}"
            assert not (d / f"{name}.tmp").exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def test_companion_save_replaces_only_after_the_bytes_are_complete():
    """CrystalCore.save used to write_text memory.json in place.
    A crash mid-write destroyed the previous companion store.

    Declares local so this test is the atomic write, not host trust.
    """
    import json
    import os
    import tempfile

    CrystalCore = _companion_cls()
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    os.environ["CRYSTAL_HOST_CLASS"] = "local"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            companion = CrystalCore(memory_dir=tmp)
            companion.memory.notes.append({
                "text": "keep me",
                "tags": [],
                "visibility": "private",
            })
            companion.save()
            path = Path(tmp) / "memory.json"
            original = path.read_text(encoding="utf-8")
            assert "keep me" in original
            assert not path.with_name(path.name + ".tmp").exists()

            companion.memory.notes.append({
                "text": "destroyed",
                "tags": [],
                "visibility": "private",
            })

            def boom(*_a, **_k):
                raise OSError("disk full")

            real_fsync = os.fsync
            os.fsync = boom  # type: ignore[assignment]
            try:
                try:
                    companion.save()
                except OSError:
                    pass
                else:
                    raise AssertionError("fsync was supposed to raise")
            finally:
                os.fsync = real_fsync
            assert path.read_text(encoding="utf-8") == original
            assert "destroyed" not in path.read_text(encoding="utf-8")
            assert "keep me" in path.read_text(encoding="utf-8")
            assert not path.with_name(path.name + ".tmp").exists()
            # Personality file must also survive a failed memory write
            # (memory.json is written first).
            config = json.loads((Path(tmp) / "config.json").read_text(
                encoding="utf-8"))
            assert "name" in config
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old


def test_audit_append_refuses_durable_on_pool():
    import os

    from crystalcore.audit import append_audit
    from crystalcore.revocation import append_revocation

    audit = Path("/usr/crystal_audit_host_trust_test.jsonl")
    rev = Path("/usr/crystal_revocations_host_trust_test.jsonl")
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            append_audit(audit, guest="claude", tool="recall",
                         arguments={}, decision="received")
            assert False, "durable audit on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        try:
            append_revocation(rev, guest="claude", action="revoke")
            assert False, "durable revocation on shared must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not audit.exists()
        assert not rev.exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_audit_append_refuses_temp_on_unknown():
    import os
    import tempfile

    from crystalcore.audit import append_audit
    from crystalcore.revocation import append_revocation

    d = Path(tempfile.mkdtemp(prefix="audit_unknown_tmp_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    old_hatch = os.environ.get("CRYSTAL_HOST_ALLOW_EPHEMERAL")
    os.environ.pop("CRYSTAL_HOST_CLASS", None)
    os.environ.pop("GITHUB_ACTIONS", None)
    os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
    try:
        try:
            append_audit(d / "audit.jsonl", guest="claude", tool="recall",
                         arguments={}, decision="received")
            assert False, "temp audit on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
            assert "unknown" in str(exc)
        try:
            append_revocation(d / "revocations.jsonl", guest="claude",
                              action="revoke")
            assert False, "temp revocation on unknown must refuse"
        except PermissionError as exc:
            assert "host trust" in str(exc)
        assert not (d / "audit.jsonl").exists()
        assert not (d / "revocations.jsonl").exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga
        if old_hatch is None:
            os.environ.pop("CRYSTAL_HOST_ALLOW_EPHEMERAL", None)
        else:
            os.environ["CRYSTAL_HOST_ALLOW_EPHEMERAL"] = old_hatch


def test_audit_append_allows_temp_on_github_hosted():
    import os
    import tempfile

    from crystalcore.audit import append_audit
    from crystalcore.revocation import append_revocation

    d = Path(tempfile.mkdtemp(prefix="audit_gh_tmp_"))
    old = os.environ.get("CRYSTAL_HOST_CLASS")
    old_ga = os.environ.get("GITHUB_ACTIONS")
    os.environ["CRYSTAL_HOST_CLASS"] = "shared"
    os.environ["GITHUB_ACTIONS"] = "true"
    try:
        append_audit(d / "audit.jsonl", guest="claude", tool="recall",
                     arguments={}, decision="received")
        append_revocation(d / "revocations.jsonl", guest="claude",
                          action="revoke")
        assert (d / "audit.jsonl").exists()
        assert (d / "revocations.jsonl").exists()
    finally:
        if old is None:
            os.environ.pop("CRYSTAL_HOST_CLASS", None)
        else:
            os.environ["CRYSTAL_HOST_CLASS"] = old
        if old_ga is None:
            os.environ.pop("GITHUB_ACTIONS", None)
        else:
            os.environ["GITHUB_ACTIONS"] = old_ga


def main() -> int:
    tests = [
        test_bridge_refuses_to_run_without_a_nominated_memory_folder,
        test_mind_imports_and_exposes_the_companion_class,
        test_approved_guest_with_allowed_tool_and_token_is_allowed,
        test_approved_guest_with_disallowed_tool_is_refused,
        test_status_is_always_allowed_for_a_proven_approved_guest,
        test_status_is_refused_when_provenance_fails,
        test_status_is_refused_when_revoked,
        test_unknown_guest_is_refused,
        test_present_but_unapproved_guest_is_refused,
        test_missing_token_refuses_as_provenance,
        test_wrong_token_refuses_as_provenance_not_permission,
        test_guest_with_no_minted_token_refuses_fail_closed,
        test_empty_scope_refuses_even_after_the_gate_allows,
        test_granted_scope_passes,
        test_scope_refusal_carries_check_request_id,
        test_scope_allow_is_audited_with_request_id,
        test_memories_without_visibility_are_private,
        test_revoked_guest_refuses_without_restart,
        test_revocation_survives_restart,
        test_reinstate_restores_access,
        test_corrupt_revocation_ledger_refuses_all,
        test_ask_recorded_before_refusal,
        test_pending_and_audit_files_are_never_group_or_world_readable,
        test_ask_survives_evaluation_crash,
        test_unrecordable_ask_refuses,
        test_missing_read_types_refuses,
        test_type_gate_refuses_layer_not_served,
        test_unknown_type_name_stops_startup,
        test_unknown_visibility_class_stops_startup,
        test_guest_may_never_be_configured_to_write_private,
        test_layers_beyond_semantic_never_reach_guests,
        test_write_json_atomic_replaces_only_after_the_bytes_are_complete,
        test_write_json_atomic_refuses_durable_on_pool,
        test_write_json_atomic_refuses_temp_on_unknown,
        test_write_json_atomic_allows_temp_on_github_hosted,
        test_companion_save_refuses_durable_on_pool,
        test_companion_save_refuses_temp_on_unknown,
        test_companion_save_allows_temp_on_github_hosted,
        test_companion_save_replaces_only_after_the_bytes_are_complete,
        test_audit_append_refuses_durable_on_pool,
        test_audit_append_refuses_temp_on_unknown,
        test_audit_append_allows_temp_on_github_hosted,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. The gate keeps five doors, honestly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

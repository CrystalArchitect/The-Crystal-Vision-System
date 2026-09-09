# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Self-test for host trust classification.

    python3 -m host_trust.selftest

Does not mint identities. Does not talk to a network. Does not unshare
a vendor pool. HADES is not a HostClass.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from .classify import (
    HostClass,
    classify,
    is_ephemeral_path,
    refuse_steward_persist,
    require_steward_persist,
)


def test_override_local():
    assert classify({"CRYSTAL_HOST_CLASS": "local"}) is HostClass.LOCAL
    assert refuse_steward_persist(env={"CRYSTAL_HOST_CLASS": "local"}) is False


def test_override_shared():
    assert classify({"CRYSTAL_HOST_CLASS": "shared"}) is HostClass.SHARED
    assert refuse_steward_persist(env={"CRYSTAL_HOST_CLASS": "shared"}) is True


def test_override_delegated():
    assert classify({"CRYSTAL_HOST_CLASS": "delegated"}) is HostClass.DELEGATED
    assert refuse_steward_persist(env={"CRYSTAL_HOST_CLASS": "delegated"}) is False


def test_unknown_when_unset():
    assert classify({}) is HostClass.UNKNOWN
    assert refuse_steward_persist(env={}) is True


def test_garbage_override_is_unknown():
    assert classify({"CRYSTAL_HOST_CLASS": "hades"}) is HostClass.UNKNOWN
    assert classify({"CRYSTAL_HOST_CLASS": "HADES"}) is HostClass.UNKNOWN


def test_github_hosted_is_shared():
    env = {"GITHUB_ACTIONS": "true", "RUNNER_ENVIRONMENT": "github-hosted"}
    assert classify(env) is HostClass.SHARED
    assert refuse_steward_persist(env=env) is True


def test_github_actions_without_runner_env_is_shared():
    assert classify({"GITHUB_ACTIONS": "true"}) is HostClass.SHARED


def test_self_hosted_runner_is_delegated():
    env = {"GITHUB_ACTIONS": "true", "RUNNER_ENVIRONMENT": "self-hosted"}
    assert classify(env) is HostClass.DELEGATED
    assert refuse_steward_persist(env=env) is False


def test_override_beats_github_heuristic():
    env = {
        "GITHUB_ACTIONS": "true",
        "RUNNER_ENVIRONMENT": "github-hosted",
        "CRYSTAL_HOST_CLASS": "local",
    }
    assert classify(env) is HostClass.LOCAL


def test_ephemeral_tmp_is_allowed_on_github_hosted():
    env = {"CRYSTAL_HOST_CLASS": "shared", "GITHUB_ACTIONS": "true"}
    d = Path(tempfile.mkdtemp(prefix="host_trust_eph_"))
    require_steward_persist("identity-mint", d / "identity.json", env=env)


def test_ephemeral_tmp_refuses_on_unknown():
    env = {}
    d = Path(tempfile.mkdtemp(prefix="host_trust_unk_"))
    try:
        require_steward_persist("identity-mint", d / "identity.json", env=env)
        assert False, "tmp on unknown must refuse"
    except PermissionError as exc:
        assert "unknown" in str(exc)


def test_ephemeral_tmp_refuses_on_shared_without_github_actions():
    env = {"CRYSTAL_HOST_CLASS": "shared"}
    d = Path(tempfile.mkdtemp(prefix="host_trust_shared_no_ga_"))
    try:
        require_steward_persist("identity-mint", d / "identity.json", env=env)
        assert False, "tmp on shared without GITHUB_ACTIONS must refuse"
    except PermissionError as exc:
        assert "shared" in str(exc)


def test_durable_path_refuses_on_shared():
    env = {"CRYSTAL_HOST_CLASS": "shared"}
    path = Path("/usr/starline_identity_host_trust_test.json")
    try:
        require_steward_persist("identity-mint", path, env=env)
        assert False, "durable path on shared must refuse"
    except PermissionError as exc:
        assert "host trust" in str(exc)
        assert "shared" in str(exc)


def test_durable_path_refuses_on_unknown():
    env = {}
    path = Path("/var/crystal/identity.json")
    try:
        require_steward_persist("consent-save", path, env=env)
        assert False, "durable path on unknown must refuse"
    except PermissionError as exc:
        assert "unknown" in str(exc)


def test_hatch_allows_durable_on_shared():
    env = {"CRYSTAL_HOST_CLASS": "shared", "CRYSTAL_HOST_ALLOW_EPHEMERAL": "1"}
    require_steward_persist("identity-mint", Path("/usr/not-a-home.json"), env=env)


def test_tmp_detection():
    d = Path(tempfile.mkdtemp(prefix="host_trust_tmp_"))
    assert is_ephemeral_path(d / "x.json")
    assert not is_ephemeral_path(Path("/usr/bin"))


def main() -> int:
    tests = [
        test_override_local,
        test_override_shared,
        test_override_delegated,
        test_unknown_when_unset,
        test_garbage_override_is_unknown,
        test_github_hosted_is_shared,
        test_github_actions_without_runner_env_is_shared,
        test_self_hosted_runner_is_delegated,
        test_override_beats_github_heuristic,
        test_ephemeral_tmp_is_allowed_on_github_hosted,
        test_ephemeral_tmp_refuses_on_unknown,
        test_ephemeral_tmp_refuses_on_shared_without_github_actions,
        test_durable_path_refuses_on_shared,
        test_durable_path_refuses_on_unknown,
        test_hatch_allows_durable_on_shared,
        test_tmp_detection,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  ok  {t.__name__}")
        except Exception as exc:
            failed += 1
            print(f"  FAIL  {t.__name__}: {exc}")
    print(f"{len(tests) - failed}/{len(tests)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

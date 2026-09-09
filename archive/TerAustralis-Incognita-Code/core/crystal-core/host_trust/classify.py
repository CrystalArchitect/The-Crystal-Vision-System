# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Classify the execution host. Fail-closed when origin cannot be established.

Steward override: CRYSTAL_HOST_CLASS=local|delegated|shared|unknown
Heuristics only run when that variable is unset.
"""

from __future__ import annotations

import os
import tempfile
from enum import Enum
from pathlib import Path


class HostClass(str, Enum):
    LOCAL = "local"
    DELEGATED = "delegated"
    SHARED = "shared"
    UNKNOWN = "unknown"


_ALLOWED = {c.value: c for c in HostClass}

# Operations that must not land durable steward material on a pool.
STEWARD_PERSIST = frozenset(
    {
        "identity-mint",
        "consent-save",
        "token-mint",
        "fragment-persist",
        "memory-private-write",
        "peer-save",
        "audit-append",
    }
)


def classify(env: dict[str, str] | None = None) -> HostClass:
    e = os.environ if env is None else env
    raw = (e.get("CRYSTAL_HOST_CLASS") or "").strip().lower()
    if raw:
        return _ALLOWED.get(raw, HostClass.UNKNOWN)
    if e.get("GITHUB_ACTIONS") == "true":
        runner = (e.get("RUNNER_ENVIRONMENT") or "").strip().lower()
        if runner == "self-hosted":
            return HostClass.DELEGATED
        return HostClass.SHARED
    return HostClass.UNKNOWN


def refuse_steward_persist(
    host: HostClass | None = None,
    *,
    env: dict[str, str] | None = None,
) -> bool:
    """True when durable steward material must not be written."""
    if host is None:
        host = classify(env)
    return host in (HostClass.SHARED, HostClass.UNKNOWN)


def is_ephemeral_path(path: Path | str, *, env: dict[str, str] | None = None) -> bool:
    """True when `path` is under the process temp dir (scratch, not a home)."""
    e = os.environ if env is None else env
    tmp = Path(e.get("TMPDIR") or e.get("TEMP") or tempfile.gettempdir()).resolve()
    try:
        resolved = Path(path).resolve()
    except OSError:
        return False
    return resolved == tmp or tmp in resolved.parents


def require_steward_persist(
    operation: str,
    path: Path | str,
    *,
    env: dict[str, str] | None = None,
) -> None:
    """Refuse steward writes on shared/unknown hosts.

    Job-scoped scratch (path under the process temp dir) is allowed only
    when the host is `shared` and `GITHUB_ACTIONS=true`: GitHub-hosted
    VMs die with the job. Persistent vendor pools often mount `/tmp` on
    the same disk as the workspace; `unknown` does not get that exception.

    `CRYSTAL_HOST_ALLOW_EPHEMERAL=1` allows any path (explicit hatch).
    """
    e = os.environ if env is None else env
    host = classify(e)
    if not refuse_steward_persist(host, env=e):
        return
    if (e.get("CRYSTAL_HOST_ALLOW_EPHEMERAL") or "").strip() == "1":
        return
    if (
        host is HostClass.SHARED
        and e.get("GITHUB_ACTIONS") == "true"
        and is_ephemeral_path(path, env=e)
    ):
        return
    raise PermissionError(
        f"host trust: refuse {operation} on {host.value} host "
        f"(path {path} is not job-scoped scratch). "
        "Set CRYSTAL_HOST_CLASS=local on a machine you control. "
        "Temp dir is only allowed on GitHub-hosted shared jobs."
    )

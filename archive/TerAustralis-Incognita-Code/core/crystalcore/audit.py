# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Append-only audit log for CrystalBridge."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_private(path: Path, text: str) -> None:
    """Append one record. New files are 0600; existing files are tightened.

    Same discipline as identity.json — these lines name guests, tools, and
    request ids. Default umask left them group/world readable.
    """
    from crystalcore.config import _require_steward_persist

    _require_steward_persist("audit-append", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, text.encode("utf-8"))
    finally:
        os.close(fd)
    os.chmod(path, 0o600)


def append_audit(
    audit_path: Path,
    *,
    guest: str,
    tool: str,
    arguments: dict[str, Any] | None,
    decision: str,
    reason: str = "",
    detail: dict[str, Any] | None = None,
) -> None:
    record = {
        "timestamp": _now(),
        "guest": guest,
        "tool": tool,
        "arguments": arguments or {},
        "decision": decision,
        "reason": reason,
    }
    if detail:
        record["detail"] = detail
    _append_private(audit_path, json.dumps(record, ensure_ascii=False) + "\n")


def read_audit(audit_path: Path) -> list[dict[str, Any]]:
    if not audit_path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in audit_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows

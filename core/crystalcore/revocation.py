# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The revocation ledger — consent withdrawal as a durable runtime act.

The constitution says consent is *revocable* at runtime. Before this module,
revoking a guest meant hand-editing bridge_config.json and restarting the
bridge — not runtime, invisible to audit, and gone the moment someone restored
the file. This ledger makes revocation a first-class record:

- **Append-only JSONL** beside the profile (`revocations.jsonl`), same
  mechanics as the audit log. Nothing here rewrites history.
- **Latest record per guest wins** — a `revoke` is lifted only by a later
  `reinstate`, never by deletion.
- **Read at check time**, so a revocation bites without a bridge restart and
  survives any number of them.
- **Fail-closed**: a ledger that exists but cannot be parsed refuses every
  guest, because a gate that cannot know who is revoked must not guess.

The shape mirrors `crystal-core/consent_transport/consent.py`'s Revocation
records — the project's prior art — without importing across the package
boundary.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ACTIONS = ("revoke", "reinstate")


class RevocationLedgerUnreadable(Exception):
    """The ledger exists but cannot be trusted — refuse everyone."""


def revocations_path(profile_dir: Path) -> Path:
    return profile_dir / "revocations.jsonl"


def append_revocation(
    path: Path,
    *,
    guest: str,
    action: str,
    reason: str = "",
    by: str = "human",
) -> None:
    if action not in ACTIONS:
        raise ValueError(f"action must be one of {ACTIONS}, not {action!r}")
    from crystalcore.config import _require_steward_persist

    _require_steward_persist("audit-append", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "guest": (guest or "").strip().lower(),
        "action": action,
        "reason": reason,
        "by": by,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def revoked_guests(path: Path) -> set[str]:
    """The guests currently revoked: latest record per guest wins.

    An absent file is the empty ledger — the normal state of a profile that
    has never revoked anyone, not an ambiguity. A present file with any
    unparseable or malformed line raises `RevocationLedgerUnreadable`, and
    the gate treats that as refuse-everyone.
    """
    if not path.exists():
        return set()
    latest: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RevocationLedgerUnreadable(str(exc)) from exc
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
            guest = record["guest"]
            action = record["action"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            raise RevocationLedgerUnreadable(
                f"unparseable line in {path.name}: {line[:80]!r}"
            ) from exc
        if action not in ACTIONS:
            raise RevocationLedgerUnreadable(
                f"unknown action {action!r} in {path.name}"
            )
        latest[(guest or "").strip().lower()] = action
    return {guest for guest, action in latest.items() if action == "revoke"}

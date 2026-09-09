# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Append-only log of every ask this node has received.

Mirrors `crystalcore/audit.py`'s pattern — the same discipline the
AI-guest-facing ConsentGate already holds itself to, extended to the
peer-to-peer side. `ConsentEngine` and `TokenStore` record what the human
decided (grants, revocations, tokens); nothing before this recorded what a
peer *asked for*, whether the answer was yes or no. A closed-by-default
gate that nobody can see anyone knocking on is half-observable.

This does not let the owner interrupt the specific request that triggered
an entry — `StarlineServer._handle()` answers a request within one
connection, synchronously, and that is a deliberate design commitment
elsewhere in this package (see `protocol.py`'s docstring and
`test_stalled_connections_cannot_exhaust_the_server`), not an oversight
this module should reverse. What it gives instead: every ask becomes a
durable, human-readable record, so revocation — already proven to take
effect on the very next connection — is something the owner can act on
having actually seen what it is responding to.

One asymmetry with the guest gate is deliberate law rather than drift
(CONSENT-GATE-SPEC.md, decision 4, 2026-08-12): the guest bridge refuses
an ask it cannot record, because its pending record is part of the
consent chain; this log proceeds on a failed write, because it is knock
telemetry and every consent decision on this surface — pairing, grant,
token verify, spend — fails closed on its own. A lost line here costs
visibility of one knock, never an unaccounted movement of data.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

DEFAULT_ASK_LOG_PATH = Path("starline_asks.jsonl")


def _append_private(path: Path, text: str) -> None:
    from host_trust.classify import require_steward_persist

    require_steward_persist("audit-append", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, text.encode("utf-8"))
    finally:
        os.close(fd)
    os.chmod(path, 0o600)


def append_ask(
    log_path: Path,
    *,
    dh_public_hex: str,
    peer_fingerprint: str | None,
    peer_label: str,
    kinds_requested: list[str],
    since: float,
    kinds_granted: list[str],
    stage: str,
    decision: str,
    reason: str,
) -> None:
    record = {
        "timestamp": time.time(),
        "stage": stage,
        "decision": decision,
        "reason": reason,
        "dh_public_hex": dh_public_hex,
        "peer_fingerprint": peer_fingerprint,
        "peer_label": peer_label,
        "kinds_requested": list(kinds_requested),
        "since": since,
        "kinds_granted": list(kinds_granted),
    }
    _append_private(log_path, json.dumps(record, ensure_ascii=False) + "\n")


def read_asks(log_path: Path) -> list[dict]:
    if not log_path.exists():
        return []
    rows: list[dict] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows

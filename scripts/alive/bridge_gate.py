#!/usr/bin/env python3
"""CrystalBridge ConsentGate helpers for the Alive Weave.

Fail-closed guest door — used by pulse + weave. Does not invent a new gate;
imports the real ConsentGate from archive custody.

    python3 -c 'from scripts...'  # prefer: weave.py --gate / pulse.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "archive/TerAustralis-Incognita-Code/core"
SECRET = "alive-weave-guest-secret"


@dataclass
class GateProbe:
    label: str
    allowed: bool
    decision: str
    check: str
    reason: str


def _ensure_path() -> None:
    if str(CORE) not in sys.path:
        sys.path.insert(0, str(CORE))


def build_gate(*, tools: list[str] | None = None, approved: bool = True):
    """In-memory ConsentGate for guest 'claude' — audit off (no profile dir)."""
    _ensure_path()
    from crystalcore.config import BridgeConfig, GuestGrant
    from crystalcore.gate import ConsentGate, token_hash

    config = BridgeConfig(
        profile="alive-weave",
        human_name="Crystal",
        interactive_approval=False,
        guests={"claude": GuestGrant(
            approved=approved,
            tools=list(tools or ["status", "recall", "message"]),
            read_scope=["public", "shared"],
            write_scope=["shared"],
            read_types=["episodic", "semantic"],
            write_types=["episodic"],
            token_hash=token_hash(SECRET),
        )},
        profile_dir=Path("/nonexistent-alive-weave-profile"),
    )
    return ConsentGate(config)


def probe_gate() -> list[GateProbe]:
    """Allow with good token; refuse wrong token; refuse unapproved guest."""
    _ensure_path()
    gate = build_gate()
    ok = gate.check("claude", "status", token=SECRET, audit=False)
    bad = gate.check("claude", "status", token="wrong", audit=False)
    denied = build_gate(approved=False).check(
        "claude", "status", token=SECRET, audit=False
    )
    return [
        GateProbe("allow+token", ok.allowed, ok.decision, ok.check, ok.reason),
        GateProbe("refuse+bad-token", bad.allowed, bad.decision, bad.check, bad.reason),
        GateProbe("refuse+unapproved", denied.allowed, denied.decision, denied.check, denied.reason),
    ]


def assert_gate_law() -> None:
    probes = probe_gate()
    assert probes[0].allowed is True and probes[0].decision == "allow", probes[0]
    assert probes[1].allowed is False and "provenance" in probes[1].check, probes[1]
    assert probes[2].allowed is False and probes[2].check == "approval", probes[2]


def guest_may_speak(guest: str, tool: str = "message", token: str = SECRET) -> tuple[bool, GateProbe]:
    """Single check — True only if ConsentGate allows."""
    gate = build_gate()
    result = gate.check(guest, tool, token=token, audit=False)
    probe = GateProbe(
        f"{guest}/{tool}", result.allowed, result.decision, result.check, result.reason
    )
    return result.allowed, probe

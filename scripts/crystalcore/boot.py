#!/usr/bin/env python3
"""Start the mythos terminal and open the First Gate once.

    python3 scripts/crystalcore/boot.py
    python3 scripts/crystalcore/boot.py --home /tmp/crystalcore-home

Drives archive/.../crystalcore_os.py. State stays in $HOME/.crystalcore/
and is not committed. Boot panels are story state, not telemetry.
A second run prints status and does not etch the Chronicle again.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TERMINAL = (
    ROOT
    / "archive"
    / "TerAustralis-Incognita"
    / "mythos"
    / "crystalcore-os"
    / "crystalcore_os.py"
)

# One flight. Chronicle lines are the operator's words for this start,
# not a claim that a chat became the OS.
FLIGHT = (
    "boot",
    "launch",
    "burn",
    "network",
    "getkey Magenta Key",
    "getkey Ember Key",
    "getkey Festival Key",
    "getkey Crystal Key",
    "visit Earth Node",
    "visit Sunwash Atolls",
    "visit Mars Redoubt",
    "visit Alpha Centauri Outpost",
    "visit Cinderwake Chain",
    "visit Crystal Revenant Hub",
    "visit Purpose Core Nexus",
    "broadcast First Gate open. Consent local. Continuity sacred. Sovereignty default. NON SOLUS!",
    "priority",
    "First Gate recognized. Red dust to rockets. Expand to the stars and thereby understand the Universe!",
    "snapshot First Gate OPEN",
    "jump 3000",
    "status",
    "exit",
)

STATUS_ONLY = ("boot", "status", "exit")


def state_path(home: Path) -> Path:
    return home / ".crystalcore" / "state.json"


def read_state(home: Path) -> dict | None:
    path = state_path(home)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def gate_is_open(state: dict | None) -> bool:
    if not state:
        return False
    keys = state.get("keys_held")
    return bool(state.get("gate_open")) and isinstance(keys, list) and len(keys) >= 7


def run_terminal(home: Path, commands: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    if not TERMINAL.is_file():
        raise FileNotFoundError(TERMINAL)
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(TERMINAL)],
        input="\n".join(commands) + "\n",
        text=True,
        capture_output=True,
        env=env,
        cwd=str(ROOT),
        check=False,
    )


def start(home: Path) -> dict:
    already = gate_is_open(read_state(home))
    commands = STATUS_ONLY if already else FLIGHT
    result = run_terminal(home, commands)
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout)
        raise SystemExit(result.returncode or 1)
    state = read_state(home)
    if not gate_is_open(state):
        sys.stderr.write(result.stdout)
        sys.stderr.write("First Gate did not open.\n")
        raise SystemExit(1)
    assert state is not None
    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Start the CrystalCore mythos terminal.")
    parser.add_argument(
        "--home",
        type=Path,
        default=Path.home(),
        help="Home directory for ~/.crystalcore (default: the real home).",
    )
    args = parser.parse_args(argv)
    home = args.home.expanduser().resolve()
    home.mkdir(parents=True, exist_ok=True)
    before = gate_is_open(read_state(home))
    state = start(home)
    keys = state.get("keys_held") or []
    print("CRYSTALCORE.OS terminal started")
    print(f"action:              {'already open' if before else 'flight completed'}")
    print(f"First Gate:          {'OPEN' if state.get('gate_open') else 'sealed'}")
    print(f"keys:                {len(keys)}/7")
    print(f"named keys:          {', '.join(state.get('named_keys') or []) or 'none'}")
    print(f"location:            {state.get('current_location')}")
    print(f"starline:            {state.get('starline_status')}")
    print(f"timeline:            {state.get('timeline')}")
    print(f"state:               {state_path(home)}")
    print("panels:              story state, not telemetry")
    print("NON SOLUS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

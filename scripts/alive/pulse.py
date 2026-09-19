#!/usr/bin/env python3
"""Alive pulse — inventory + selftests for every named AI island.

Connection ≠ merge. This script only *checks* archive islands; it does not
absorb Clementine, SAT, CrystalCore, or other named islands into the CVS hub product.

    python3 scripts/alive/pulse.py
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Island:
    name: str
    path: Path
    kind: str  # built | custody | compose | docs
    pulse: str  # how we check


ISLANDS = [
    Island("Labeled bus (TCV bridge)", ROOT / "archive/TheCrystalVision/clementine/bridge", "built", "module:clementine.bridge.selftest"),
    Island("Starline Weaver", ROOT / "archive/TerAustralis-Incognita-Code/core/crystal-core/bus", "built", "module:bus.selftest"),
    Island("CrystalBridge", ROOT / "archive/TerAustralis-Incognita-Code/core/crystalcore", "built", "bridge_gate"),
    Island("Decode/Ingest/Twin", ROOT / "archive/TheCrystalVision/services", "built", "module:services.selftest"),
    Island("SAT wrap_turn", ROOT / "archive/Synthetic-Affect-Theory", "built", "sat_import"),
    Island("Clementine", ROOT / "archive/Clementine-ai-companion", "custody", "path"),
    Island("CrystalCore.OS", ROOT / "archive/CrystalCore-OS", "custody", "path"),
    Island("ContextGate", ROOT / "archive/ContextGate", "custody", "path"),
    Island("Discord agent", ROOT / "archive/discord-ai-agent", "custody", "path"),
    Island("Celestial Portal backend", ROOT / "backend", "compose", "path"),
    Island("Portal docker compose", ROOT / "infrastructure/docker/docker-compose.yml", "compose", "path"),
    Island("LEAF / AI Orchestrator", ROOT / "archive/TerAustralis-Incognita/docs/adr/ADR-0005.md", "docs", "path"),
]


def _run_module(cwd: Path, module: str, extra_path: Path | None = None) -> tuple[bool, str]:
    env_pythonpath = str(cwd)
    if extra_path:
        env_pythonpath = f"{extra_path}{':' if env_pythonpath else ''}{env_pythonpath}"
    # Prefer the package root that makes `python -m` work.
    proc = subprocess.run(
        [sys.executable, "-m", module],
        cwd=str(cwd),
        env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "PYTHONPATH": env_pythonpath},
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode == 0, out.strip()


def _check(island: Island) -> tuple[str, str]:
    if island.pulse == "path":
        ok = island.path.exists()
        return ("ALIVE" if ok else "MISSING"), str(island.path.relative_to(ROOT))

    if island.pulse == "sat_import":
        if not island.path.exists():
            return "MISSING", "archive path absent"
        sys.path.insert(0, str(island.path))
        try:
            host = importlib.import_module("core.host")
            assert callable(getattr(host, "wrap_turn", None))
            return "ALIVE", "core.host.wrap_turn importable"
        except Exception as exc:  # noqa: BLE001 — pulse must report, not crash
            return "DOWN", f"{type(exc).__name__}: {exc}"
        finally:
            if str(island.path) in sys.path:
                sys.path.remove(str(island.path))

    if island.pulse == "bridge_gate":
        # Full crystalcore.selftest needs the `mcp` package; pulse the real ConsentGate.
        alive_dir = str(Path(__file__).resolve().parent)
        if alive_dir not in sys.path:
            sys.path.insert(0, alive_dir)
        try:
            from bridge_gate import assert_gate_law, probe_gate

            assert_gate_law()
            probes = probe_gate()
            summary = "; ".join(
                f"{p.label}:{'allow' if p.allowed else p.decision}" for p in probes
            )
            return "ALIVE", f"ConsentGate law holds ({summary})"
        except Exception as exc:  # noqa: BLE001
            return "DOWN", f"{type(exc).__name__}: {exc}"

    if island.pulse.startswith("module:"):
        module = island.pulse.split(":", 1)[1]
        if island.name == "Labeled bus (TCV bridge)":
            cwd = ROOT / "archive/TheCrystalVision"
            ok, out = _run_module(cwd, module)
        elif island.name == "Starline Weaver":
            cwd = ROOT / "archive/TerAustralis-Incognita-Code/core/crystal-core"
            ok, out = _run_module(cwd, module)
        elif island.name == "CrystalBridge":
            cwd = ROOT / "archive/TerAustralis-Incognita-Code/core"
            ok, out = _run_module(cwd, module)
        elif island.name == "Decode/Ingest/Twin":
            cwd = ROOT / "archive/TheCrystalVision"
            ok, out = _run_module(cwd, module)
        else:
            return "DOWN", f"unknown module pulse for {island.name}"
        tail = out.splitlines()[-1] if out else "(no output)"
        return ("ALIVE" if ok else "DOWN"), tail

    return "DOWN", f"unknown pulse {island.pulse}"


def main() -> int:
    print("Alive pulse — Crystal Vision weave")
    print("Law: connection ≠ merge · out-of-bounds titles stay out of bounds")
    print("")
    alive = down = missing = 0
    for island in ISLANDS:
        status, detail = _check(island)
        if status == "ALIVE":
            alive += 1
        elif status == "MISSING":
            missing += 1
        else:
            down += 1
        mark = {"ALIVE": "●", "DOWN": "✗", "MISSING": "○"}.get(status, "?")
        print(f"  {mark} {island.name:28} [{island.kind:8}] {status:7}  {detail}")
    print("")
    print(f"Pulse: {alive} alive · {down} down · {missing} missing · {len(ISLANDS)} named")
    # Fail only if a *built* island is down — custody/compose/docs absence of runtime is expected.
    built_down = [
        i.name for i in ISLANDS
        if i.kind == "built" and _check(i)[0] != "ALIVE"
    ]
    if built_down:
        print(f"FAIL built islands: {', '.join(built_down)}")
        return 1
    print("PASS — every Built island answers the pulse.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

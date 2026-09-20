#!/usr/bin/env python3
"""Chaos alignment audit — registry ↔ bus ↔ provider ids ↔ Chaos seats.

    python3 scripts/chaos/align.py
    python3 scripts/chaos/align.py --strict   # exit 1 on drift

Canon: no. Fixes nothing by itself — reports drift for human / agent repair.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

from crystal_platform.chaos import DEFAULT_CHAOS_SEATS
from crystal_platform.intelligence import KNOWN_PROVIDER_IDS
from crystal_platform.intelligence.http_providers import all_http_provider_factories

BUS_TO_PROVIDER = {
    "gpt": "openai.chatgpt",
    "claude": "anthropic.claude",
    "grok": "xai.grok",
    "deepseek": "deepseek",
    "kimi": "moonshot.kimi",
    "gemini": "google.gemini",
    "manus": "manus",
}

EXPECTED_WEAVE = {
    "BOT-WEAVE-CHATGPT": ("gpt", "openai.chatgpt", "OPENAI_API_KEY"),
    "BOT-WEAVE-CLAUDE": ("claude", "anthropic.claude", "ANTHROPIC_API_KEY"),
    "BOT-WEAVE-GROK": ("grok", "xai.grok", "XAI_API_KEY"),
    "BOT-WEAVE-DEEPSEEK": ("deepseek", "deepseek", "DEEPSEEK_API_KEY"),
    "BOT-WEAVE-KIMI": ("kimi", "moonshot.kimi", "MOONSHOT_API_KEY"),
    "BOT-WEAVE-GEMINI": ("gemini", "google.gemini", "GEMINI_API_KEY"),
}


def _bus_ids() -> list[str]:
    text = (ROOT / "archive/TerAustralis-Incognita-Code/core/crystal-core/bus/run.py").read_text()
    return re.findall(r'"(\w+)":\s*\w+Adapter', text)


def audit() -> list[str]:
    drift: list[str] = []
    bus_ids = _bus_ids()
    factories = set(all_http_provider_factories())

    for bus, pid in BUS_TO_PROVIDER.items():
        if bus not in bus_ids:
            drift.append(f"bus REGISTRY missing {bus}")
        if pid not in KNOWN_PROVIDER_IDS:
            drift.append(f"KNOWN_PROVIDER_IDS missing {pid}")
        if bus != "manus" and pid not in DEFAULT_CHAOS_SEATS:
            drift.append(f"DEFAULT_CHAOS_SEATS missing {pid}")
        if bus != "manus" and pid not in factories:
            drift.append(f"http factory missing {pid}")

    if "manus" in DEFAULT_CHAOS_SEATS:
        drift.append("manus must not be in Portal Chaos seats")
    if "manus" in factories:
        drift.append("manus must not have sync Portal http factory")

    if yaml is None:
        drift.append("PyYAML missing — skip registry checks")
        return drift

    reg = yaml.safe_load((ROOT / "docs/bots/registry.yaml").read_text())
    by_id = {b["id"]: b for b in reg.get("bots", [])}
    for bot_id, (bus, pid, secret) in EXPECTED_WEAVE.items():
        row = by_id.get(bot_id)
        if not row:
            drift.append(f"registry missing {bot_id}")
            continue
        if row.get("bus_agent") != bus:
            drift.append(f"{bot_id} bus_agent={row.get('bus_agent')!r} want {bus}")
        if row.get("provider_id") != pid:
            drift.append(f"{bot_id} provider_id={row.get('provider_id')!r} want {pid}")
        secrets = row.get("secrets") or []
        if secret not in secrets and not any(secret in str(s) for s in secrets):
            # Kimi allows MOONSHOT or KIMI
            if bot_id == "BOT-WEAVE-KIMI" and (
                "MOONSHOT_API_KEY" in secrets or "KIMI_API_KEY" in secrets
            ):
                pass
            else:
                drift.append(f"{bot_id} secrets missing {secret}")

    # Build ≠ Explore
    build = by_id.get("BOT-WEAVE-GROK-BUILD")
    if build and build.get("bus_agent"):
        drift.append("BOT-WEAVE-GROK-BUILD must not have bus_agent (not a chaos seat)")

    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chaos alignment audit")
    parser.add_argument("--strict", action="store_true", help="exit 1 if drift")
    args = parser.parse_args(argv)
    drift = audit()
    print("Chaos alignment audit")
    print(f"  bus adapters: {', '.join(_bus_ids())}")
    print(f"  chaos seats:  {', '.join(DEFAULT_CHAOS_SEATS)}")
    if drift:
        print(f"  DRIFT ({len(drift)}):")
        for d in drift:
            print(f"    - {d}")
        return 1 if args.strict else 0
    print("  DRIFT: NONE — aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

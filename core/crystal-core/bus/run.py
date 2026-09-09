# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Run a conversation on the Starline Weaver.

    python3 -m bus.run --agents echo,sisters --turns 4 --topic "first water"
    python3 -m bus.run --agents claude,grok --turns 3 --topic "water care"  # needs API keys

Or fan one question out to every agent independently and cross-compare:

    python3 -m bus.run --mode matrix --agents claude,gpt,grok --topic "what is the Starline Weaver?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .adapters import AnthropicAdapter, OpenAIAdapter, XAIAdapter
from .agents import BusHub, EchoAgent, RedButtonAgent, SevenSistersAgent, UnlabeledAgent
from .bus import StarlineWeaver

REGISTRY = {
    "echo": EchoAgent,
    "sisters": SevenSistersAgent,
    "drifter": UnlabeledAgent,
    "redbutton": RedButtonAgent,
    "claude": AnthropicAdapter,
    "gpt": OpenAIAdapter,
    "grok": XAIAdapter,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bridge Starline Weaver")
    parser.add_argument("--mode", choices=["conversation", "matrix"], default="conversation",
                        help="conversation: round-robin turns. matrix: same question to every "
                             "agent independently, once each, then cross-compare.")
    parser.add_argument("--agents", default="echo,sisters",
                        help=f"comma-separated from: {', '.join(REGISTRY)}")
    parser.add_argument("--turns", type=int, default=4, help="conversation mode only")
    parser.add_argument("--topic", default="first water", help="topic (conversation) or question (matrix)")
    parser.add_argument("--out", default="",
                        help="transcript path (default: bus/transcripts/<slug>.md)")
    args = parser.parse_args(argv)

    try:
        agents = [REGISTRY[n.strip()]() for n in args.agents.split(",") if n.strip()]
    except KeyError as bad:
        parser.error(f"unknown agent {bad}; choose from: {', '.join(REGISTRY)}")

    hub = BusHub()
    bus = StarlineWeaver(hub, agents)
    matrix = args.mode == "matrix"
    transcript = bus.run_matrix(args.topic) if matrix else bus.run(args.topic, args.turns)

    for e in transcript:
        status = "" if e["delivered"] else f"  [REJECTED: {e.get('rejected_because', '')}]"
        print(f"{e['from']:>10} → {e['to']:<4} [{e['layer'] or '-'}] {e['content']}{status}")

    if matrix:
        compare = bus.cross_compare()
        print(f"\nCross-compare: {compare['agents_delivered']}/{compare['agents_asked']} delivered, "
              f"layers={compare['layer_counts']}, unanimous={compare['layer_unanimous']}")

    if args.out:
        out = Path(args.out)
    else:
        slug = "-".join(args.topic.lower().split())[:40] or "run"
        out = Path(__file__).resolve().parent.parent / "transcripts" / f"{slug}.md"
    saved = bus.save_matrix_markdown(out, args.topic) if matrix else bus.save_markdown(out, args.topic)
    print(f"\nTranscript saved: {saved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

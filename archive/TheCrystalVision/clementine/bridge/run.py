"""Run a conversation on the Songline Bus.

    python3 -m clementine.bridge.run --agents echo,sisters --turns 4 --topic "first water"
    python3 -m clementine.bridge.run --agents claude,grok --turns 3 --topic "water care"  # needs API keys
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .adapters import AnthropicAdapter, OpenAIAdapter, XAIAdapter
from .agents import ClementineHub, EchoAgent, RedButtonAgent, SevenSistersAgent, UnlabeledAgent
from .bus import SonglineBus

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
    parser = argparse.ArgumentParser(description="Clementine Songline Bus")
    parser.add_argument("--agents", default="echo,sisters",
                        help=f"comma-separated from: {', '.join(REGISTRY)}")
    parser.add_argument("--turns", type=int, default=4)
    parser.add_argument("--topic", default="first water")
    parser.add_argument("--out", default="",
                        help="transcript path (default: clementine/transcripts/<slug>.md)")
    args = parser.parse_args(argv)

    try:
        agents = [REGISTRY[n.strip()]() for n in args.agents.split(",") if n.strip()]
    except KeyError as bad:
        parser.error(f"unknown agent {bad}; choose from: {', '.join(REGISTRY)}")

    hub = ClementineHub()
    bus = SonglineBus(hub, agents)
    transcript = bus.run(args.topic, args.turns)

    for e in transcript:
        status = "" if e["delivered"] else f"  [REJECTED: {e.get('rejected_because', '')}]"
        print(f"{e['from']:>10} → {e['to']:<4} [{e['layer'] or '-'}] {e['content']}{status}")

    if args.out:
        out = Path(args.out)
    else:
        slug = "-".join(args.topic.lower().split())[:40] or "run"
        out = Path(__file__).resolve().parent.parent / "transcripts" / f"{slug}.md"
    saved = bus.save_markdown(out, args.topic)
    print(f"\nTranscript saved: {saved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Join any agent to a running Clementine server — from this machine or another.

    python3 -m clementine.bridge.remote --agent sisters --server http://127.0.0.1:8777 --turns 4
    python3 -m clementine.bridge.remote --agent claude --server http://host:8777    # with API key set
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request

from .bus import Message


def _get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post(url: str, body: dict) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    from .run import REGISTRY  # late import to avoid a cycle

    parser = argparse.ArgumentParser(description="Remote agent for the Songline Bus")
    parser.add_argument("--agent", required=True, help=f"one of: {', '.join(REGISTRY)}")
    parser.add_argument("--server", default="http://127.0.0.1:8777")
    parser.add_argument("--turns", type=int, default=4, help="speak this many times, then leave")
    parser.add_argument("--poll", type=float, default=0.2, help="seconds between turn checks")
    args = parser.parse_args(argv)

    if args.agent not in REGISTRY:
        parser.error(f"unknown agent {args.agent!r}; choose from: {', '.join(REGISTRY)}")
    agent = REGISTRY[args.agent]()

    joined = _post(f"{args.server}/join", {"name": agent.name})
    if not joined.get("ok"):
        print(f"join refused: {joined.get('reason')}")
        return 1
    print(f"{agent.name} joined {args.server} (position {joined['position']})")

    spoken = 0
    while spoken < args.turns:
        status = _get(f"{args.server}/wait?name={agent.name}")
        if status.get("halted"):
            print("bus halted — leaving")
            return 0
        if not status.get("your_turn"):
            time.sleep(args.poll)
            continue
        last = status["last"]
        last_msg = Message(
            sender=last["from"], to=last["to"], layer=last["layer"],
            content=last["content"], cycle=last["cycle"],
        )
        reply = agent.respond(last_msg, [])
        result = _post(f"{args.server}/speak", {
            "name": agent.name,
            "layer": reply.get("layer", ""),
            "content": reply.get("content", ""),
            "red_button": bool(reply.get("red_button")),
        })
        spoken += 1
        tag = "delivered" if result.get("delivered") else f"REJECTED ({result.get('reason')})"
        print(f"[{spoken}/{args.turns}] {agent.name} [{reply.get('layer') or '-'}] "
              f"{reply.get('content', '')!r} — {tag}")
        if result.get("halted"):
            print("red button — bus halted")
            return 0
    print(f"{agent.name} finished {args.turns} turns; leaving the fire burning")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

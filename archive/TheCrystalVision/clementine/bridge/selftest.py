"""Self-test for the Songline Bus — proves the law is real, not decorative.

    python3 -m clementine.bridge.selftest
"""

from __future__ import annotations

from .agents import ClementineHub, EchoAgent, RedButtonAgent, SevenSistersAgent, UnlabeledAgent
from .bus import SonglineBus


def test_conversation_flows():
    bus = SonglineBus(ClementineHub(), [EchoAgent(), SevenSistersAgent()])
    transcript = bus.run("first water", 4)
    delivered = [e for e in transcript if e["delivered"]]
    assert len(delivered) == 1 + 4 * 2, "opening + 2 agents x 4 turns should all deliver"
    assert all(e["layer"] in ("science", "story", "vision") for e in delivered)


def test_unlabeled_speech_is_rejected():
    bus = SonglineBus(ClementineHub(), [UnlabeledAgent()])
    transcript = bus.run("drift check", 3)
    rejected = [e for e in transcript if not e["delivered"]]
    assert len(rejected) == 3, "every unlabeled message must be rejected"
    assert all("label" in e["rejected_because"] for e in rejected)


def test_red_button_halts_bus():
    bus = SonglineBus(ClementineHub(), [RedButtonAgent(after=2), SevenSistersAgent()])
    transcript = bus.run("halt check", 10)
    assert transcript[-1]["content"].startswith("RED BUTTON"), "bus must close with a halt notice"
    cycles = [e["cycle"] for e in transcript if e["cycle"] > 0]
    assert max(cycles) < 10, "bus must stop early, not run all requested turns"


def main() -> int:
    tests = [test_conversation_flows, test_unlabeled_speech_is_rejected, test_red_button_halts_bus]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. Belt-Three law holds in code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

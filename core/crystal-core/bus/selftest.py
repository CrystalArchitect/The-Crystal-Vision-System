# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for the Starline Weaver — proves the law is real, not decorative.

    python3 -m bus.selftest
"""

from __future__ import annotations

from .agents import BusHub, EchoAgent, RedButtonAgent, SevenSistersAgent, UnlabeledAgent
from .bus import StarlineWeaver


def test_conversation_flows():
    bus = StarlineWeaver(BusHub(), [EchoAgent(), SevenSistersAgent()])
    transcript = bus.run("first water", 4)
    delivered = [e for e in transcript if e["delivered"]]
    assert len(delivered) == 1 + 4 * 2, "opening + 2 agents x 4 turns should all deliver"
    assert all(e["layer"] in ("science", "story", "vision") for e in delivered)


def test_unlabeled_speech_is_rejected():
    bus = StarlineWeaver(BusHub(), [UnlabeledAgent()])
    transcript = bus.run("drift check", 3)
    rejected = [e for e in transcript if not e["delivered"]]
    assert len(rejected) == 3, "every unlabeled message must be rejected"
    assert all("label" in e["rejected_because"] for e in rejected)


def test_red_button_halts_bus():
    bus = StarlineWeaver(BusHub(), [RedButtonAgent(after=2), SevenSistersAgent()])
    transcript = bus.run("halt check", 10)
    assert transcript[-1]["content"].startswith("RED BUTTON"), "bus must close with a halt notice"
    cycles = [e["cycle"] for e in transcript if e["cycle"] > 0]
    assert max(cycles) < 10, "bus must stop early, not run all requested turns"


def test_matrix_gives_independent_answers():
    bus = StarlineWeaver(BusHub(), [EchoAgent(), EchoAgent()])
    transcript = bus.run_matrix("what is water")
    replies = [e for e in transcript if e["cycle"] == 1]
    assert len(replies) == 2, "every agent should be asked exactly once"
    expected = "Echo of hub: Matrix question: what is water"
    assert all(e["content"] == expected for e in replies), \
        "each agent must answer the hub's question, not another agent's reply"


def test_matrix_rejects_unlabeled_without_blocking_others():
    bus = StarlineWeaver(BusHub(), [UnlabeledAgent(), EchoAgent()])
    transcript = bus.run_matrix("drift check")
    replies = [e for e in transcript if e["cycle"] == 1]
    assert replies[0]["delivered"] is False, "unlabeled speech is still rejected in matrix mode"
    assert replies[1]["delivered"] is True, "one agent's rejection must not silence the next"


def test_matrix_cross_compare_counts_not_judges():
    bus = StarlineWeaver(BusHub(), [EchoAgent(), EchoAgent()])
    bus.run_matrix("what is water")
    compare = bus.cross_compare()
    assert compare == {
        "agents_asked": 2, "agents_delivered": 2, "agents_rejected": 0,
        "layer_counts": {"vision": 2}, "layer_unanimous": True,
    }


def test_matrix_red_button_stops_remaining_agents():
    bus = StarlineWeaver(BusHub(), [RedButtonAgent(after=1), EchoAgent()])
    transcript = bus.run_matrix("halt check")
    assert transcript[-1]["content"].startswith("RED BUTTON")
    replies = [e for e in transcript if e["cycle"] == 1]
    assert len(replies) == 1, "the agent after the one that pressed the button must never be asked"


def main() -> int:
    tests = [
        test_conversation_flows, test_unlabeled_speech_is_rejected, test_red_button_halts_bus,
        test_matrix_gives_independent_answers, test_matrix_rejects_unlabeled_without_blocking_others,
        test_matrix_cross_compare_counts_not_judges, test_matrix_red_button_stops_remaining_agents,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. Belt-Three law holds in code.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

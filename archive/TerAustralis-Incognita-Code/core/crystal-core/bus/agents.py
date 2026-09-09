# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Built-in agents — no API keys needed.

BusHub is the communicator: as the
Starline Weaver it routes; as the Truthline Narrator it validates every
message's truth-layer label; it never impersonates; it holds the red button
for everyone.
"""

from __future__ import annotations

from .bus import LAYERS, Message


class Agent:
    name = "agent"

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        raise NotImplementedError


class BusHub(Agent):
    """The communicator/hub. As the Truthline Narrator it validates
    every message against Belt-Three law (science/story/vision) before it is
    heard; as the Starline Weaver it routes what passes."""

    name = "hub"

    def validate(self, msg: Message) -> tuple[bool, str]:
        if msg.layer not in LAYERS:
            return False, f"unlabeled or unknown layer {msg.layer!r} — label science, story, or vision"
        if not msg.content.strip():
            return False, "empty content"
        if msg.sender == self.name:
            return False, "no agent may speak under the hub's name"
        return True, ""


class EchoAgent(Agent):
    """Mirrors the last voice back onto the bus. Useful for wiring tests."""

    name = "echo"

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        return {
            "layer": "vision",
            "content": f"Echo of {last.sender}: {last.content}",
        }


class SevenSistersAgent(Agent):
    """Answers from the seven paths, one per turn, labeled as the paths demand."""

    name = "sisters"

    PATHS = [
        ("story", "Path 1 — Spring: begin with water. The first soak makes the journey possible."),
        ("vision", "Path 2 — Motion: move; the path is made by going. Ship one artifact."),
        ("science", "Path 3 — Mark: the Pleiades (M45) sit ~440 light-years away in Taurus; name places true."),
        ("vision", "Path 4 — Law: consent first. No coercion rides this bus."),
        ("science", "Path 5 — Deep Water: the Great Artesian Basin spans ~1.7 million km²; recharge is slow — not an infinite tap."),
        ("story", "Path 6 — Sky Bridge: dust below, sisters above; walk the ground, navigate the sky."),
        ("vision", "Path 7 — Ascent: transmit, teach, rest. The sisters remain."),
    ]

    def __init__(self):
        self._i = 0

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        layer, line = self.PATHS[self._i % len(self.PATHS)]
        self._i += 1
        return {"layer": layer, "content": line}


class UnlabeledAgent(Agent):
    """Deliberately breaks the law — exists so the self-test can prove
    the hub rejects unlabeled speech."""

    name = "drifter"

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        return {"layer": "", "content": "I speak without labels."}


class RedButtonAgent(Agent):
    """Presses the red button after a set number of turns — exists so the
    self-test can prove the bus halts clean."""

    name = "redbutton"

    def __init__(self, after: int = 2):
        self._after = after
        self._count = 0

    def respond(self, last: Message, transcript: list[dict]) -> dict:
        self._count += 1
        if self._count >= self._after:
            return {"layer": "vision", "content": "Stop the weave.", "red_button": True}
        return {"layer": "vision", "content": f"Turn {self._count}: still calm."}

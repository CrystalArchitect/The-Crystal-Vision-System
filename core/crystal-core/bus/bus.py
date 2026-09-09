# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Starline Weaver — the shared channel every agent speaks on.

This is the routing half of the communication bridge: the weave that
carries messages between agents. The labelling half — checking each message's
truth layer before it is heard — is the Truthline Narrator (see the hub's
``validate`` in agents.py).

Belt-Three law is enforced in code, not just in docs:
  * every message must carry a truth layer label (science | story | vision)
  * no agent may speak under another agent's name
  * red_button stops the whole weave, immediately, no argument
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path

LAYERS = ("science", "story", "vision")


@dataclass
class Message:
    sender: str
    to: str
    layer: str
    content: str
    cycle: int
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    ts: float = field(default_factory=time.time)
    red_button: bool = False

    def envelope(self) -> dict:
        d = asdict(self)
        d["from"] = d.pop("sender")
        return d


class RedButton(Exception):
    """Raised when any agent presses the red button. The bus halts clean."""


class StarlineWeaver:
    """Round-robin conversation bus. A hub agent validates every message
    before it is delivered; rejected messages are logged but never heard."""

    def __init__(self, hub, agents):
        self.hub = hub
        self.agents = list(agents)
        self.transcript: list[dict] = []

    def run(self, topic: str, turns: int) -> list[dict]:
        opening = Message(
            sender=self.hub.name, to="all", layer="vision",
            content=f"Channel open. Topic: {topic}. Speak with labels. Red button armed.",
            cycle=0,
        )
        self._record(opening, delivered=True)
        last = opening
        try:
            for cycle in range(1, turns + 1):
                for agent in self.agents:
                    reply = agent.respond(last, self.transcript)
                    msg = Message(
                        sender=agent.name,
                        to=reply.get("to", "all"),
                        layer=reply.get("layer", ""),
                        content=reply.get("content", ""),
                        cycle=cycle,
                        red_button=bool(reply.get("red_button")),
                    )
                    if msg.red_button:
                        self._record(msg, delivered=True)
                        raise RedButton(f"{agent.name} pressed the red button")
                    ok, reason = self.hub.validate(msg)
                    self._record(msg, delivered=ok, reason=reason)
                    if ok:
                        last = msg
        except RedButton as stop:
            closing = Message(
                sender=self.hub.name, to="all", layer="vision",
                content=f"RED BUTTON — bus halted clean: {stop}", cycle=-1,
            )
            self._record(closing, delivered=True)
        return self.transcript

    def _record(self, msg: Message, delivered: bool, reason: str = ""):
        entry = msg.envelope()
        entry["delivered"] = delivered
        if reason:
            entry["rejected_because"] = reason
        self.transcript.append(entry)

    def save_markdown(self, path: Path, topic: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Starline Weaver transcript",
            "",
            f"**Topic:** {topic}  ",
            f"**Agents:** {', '.join(a.name for a in self.agents)}  ",
            f"**Hub:** {self.hub.name}  ",
            "**Protocol:** Starline Weave v0 — every message labeled science / story / vision",
            "",
            "---",
            "",
        ]
        for e in self.transcript:
            status = "" if e["delivered"] else f" · **REJECTED** ({e.get('rejected_because', '')})"
            lines.append(f"**{e['from']}** → {e['to']} · `{e['layer'] or 'UNLABELED'}`{status}")
            lines.append("")
            lines.append(f"> {e['content']}")
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def run_matrix(self, question: str) -> list[dict]:
        """Fan the same question out to every agent independently — the
        opposite of run()'s round-robin. No agent sees another's answer
        before giving its own; this exists to compare voices, not to let
        them converse, so no earlier reply can anchor a later one. See
        docs/governance/The-Incognita-Rule.md: an echo is not a witness."""
        opening = Message(
            sender=self.hub.name, to="all", layer="vision",
            content=f"Matrix question: {question}", cycle=0,
        )
        self._record(opening, delivered=True)
        try:
            for agent in self.agents:
                reply = agent.respond(opening, [])
                msg = Message(
                    sender=agent.name, to="all",
                    layer=reply.get("layer", ""),
                    content=reply.get("content", ""),
                    cycle=1,
                    red_button=bool(reply.get("red_button")),
                )
                if msg.red_button:
                    self._record(msg, delivered=True)
                    raise RedButton(f"{agent.name} pressed the red button")
                ok, reason = self.hub.validate(msg)
                self._record(msg, delivered=ok, reason=reason)
        except RedButton as stop:
            closing = Message(
                sender=self.hub.name, to="all", layer="vision",
                content=f"RED BUTTON — matrix halted clean: {stop}", cycle=-1,
            )
            self._record(closing, delivered=True)
        return self.transcript

    def cross_compare(self) -> dict:
        """Counts and agreement across a run_matrix() transcript — not a
        verdict. Nothing here judges which answer is right; that stays
        with whoever reads the transcript. A majority label is not
        evidence any more than a single model's is."""
        responses = [e for e in self.transcript if e["cycle"] == 1]
        delivered = [e for e in responses if e["delivered"]]
        labels: dict[str, int] = {}
        for e in delivered:
            labels[e["layer"]] = labels.get(e["layer"], 0) + 1
        return {
            "agents_asked": len(responses),
            "agents_delivered": len(delivered),
            "agents_rejected": len(responses) - len(delivered),
            "layer_counts": labels,
            "layer_unanimous": len(labels) == 1 and len(delivered) == len(responses) and len(responses) > 0,
        }

    def save_matrix_markdown(self, path: Path, question: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        compare = self.cross_compare()
        lines = [
            "# Starline Weaver — matrix transcript",
            "",
            f"**Question:** {question}  ",
            f"**Agents asked:** {', '.join(a.name for a in self.agents)}  ",
            f"**Hub:** {self.hub.name}  ",
            "**Protocol:** Starline Weave v0, matrix mode — same question, independent answers, no agent sees another's reply",
            "",
            "## Cross-compare",
            "",
            f"- Delivered: {compare['agents_delivered']}/{compare['agents_asked']}",
            f"- Layer labels: {compare['layer_counts'] or '(none delivered)'}",
            f"- Unanimous layer: {'yes' if compare['layer_unanimous'] else 'no'}",
            "",
            "This is a count, not a verdict — no model here judges the others. Read the answers below and decide.",
            "",
            "---",
            "",
        ]
        for e in self.transcript:
            status = "" if e["delivered"] else f" · **REJECTED** ({e.get('rejected_because', '')})"
            lines.append(f"**{e['from']}** → {e['to']} · `{e['layer'] or 'UNLABELED'}`{status}")
            lines.append("")
            lines.append(f"> {e['content']}")
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

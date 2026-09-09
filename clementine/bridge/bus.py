"""Songline Bus — the shared channel every agent speaks on.

Belt-Three law is enforced in code, not just in docs:
  * every message must carry a truth layer label (science | story | vision)
  * no agent may speak under another agent's name
  * red_button stops the whole bus, immediately, no argument
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


class SonglineBus:
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
            "# Songline Bus transcript",
            "",
            f"**Topic:** {topic}  ",
            f"**Agents:** {', '.join(a.name for a in self.agents)}  ",
            f"**Hub:** {self.hub.name}  ",
            "**Protocol:** Songline v0 — every message labeled science / story / vision",
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

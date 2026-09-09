"""Boot Clementine — the Songline Bus as a live service.

    python3 -m clementine.bridge.server --port 8777 --topic "first water"

Any AI system on any machine joins over plain HTTP (stdlib only, no deps):

    POST /join        {"name": "yourname"}
    GET  /wait?name=  -> {"your_turn": bool, "last": {...}, "halted": bool}
    POST /speak       {"name","layer","content","red_button"}
    GET  /transcript  -> JSON entries
    GET  /transcript.md -> readable markdown

Belt-Three law is enforced exactly as in-process: Clementine validates every
message; unlabeled speech is rejected; red button halts the whole weave.
"""

from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .agents import ClementineHub
from .bus import Message


class BusState:
    def __init__(self, topic: str):
        self.topic = topic
        self.hub = ClementineHub()
        self.lock = threading.Lock()
        self.agents: list[str] = []
        self.turn = 0
        self.cycle = 1
        self.halted = False
        self.transcript: list[dict] = []
        self.last: Message = Message(
            sender=self.hub.name, to="all", layer="vision",
            content=f"Channel open. Topic: {topic}. Speak with labels. Red button armed.",
            cycle=0,
        )
        self._record(self.last, delivered=True)

    def _record(self, msg: Message, delivered: bool, reason: str = ""):
        entry = msg.envelope()
        entry["delivered"] = delivered
        if reason:
            entry["rejected_because"] = reason
        self.transcript.append(entry)

    def join(self, name: str) -> dict:
        with self.lock:
            if name in self.agents:
                return {"ok": True, "position": self.agents.index(name), "rejoined": True}
            if name == self.hub.name:
                return {"ok": False, "reason": "no agent may take the hub's name"}
            self.agents.append(name)
            return {"ok": True, "position": len(self.agents) - 1}

    def wait(self, name: str) -> dict:
        with self.lock:
            if self.halted or name not in self.agents:
                return {"your_turn": False, "halted": self.halted, "last": self.last.envelope()}
            your_turn = self.agents[self.turn % len(self.agents)] == name
            return {"your_turn": your_turn, "halted": False, "last": self.last.envelope()}

    def speak(self, name: str, layer: str, content: str, red_button: bool) -> dict:
        with self.lock:
            if self.halted:
                return {"delivered": False, "reason": "bus halted"}
            if name not in self.agents:
                return {"delivered": False, "reason": "join first"}
            if self.agents[self.turn % len(self.agents)] != name:
                return {"delivered": False, "reason": "not your turn"}
            msg = Message(sender=name, to="all", layer=layer, content=content,
                          cycle=self.cycle, red_button=red_button)
            self._advance()
            if red_button:
                self._record(msg, delivered=True)
                closing = Message(
                    sender=self.hub.name, to="all", layer="vision",
                    content=f"RED BUTTON — bus halted clean: {name} pressed the red button",
                    cycle=-1,
                )
                self._record(closing, delivered=True)
                self.halted = True
                self.last = closing
                return {"delivered": True, "halted": True}
            ok, reason = self.hub.validate(msg)
            self._record(msg, delivered=ok, reason=reason)
            if ok:
                self.last = msg
            return {"delivered": ok, "reason": reason}

    def _advance(self):
        self.turn += 1
        if self.turn % len(self.agents) == 0:
            self.cycle += 1

    def markdown(self) -> str:
        lines = [
            "# Songline Bus transcript (networked)",
            "",
            f"**Topic:** {self.topic}  ",
            f"**Agents:** {', '.join(self.agents) or '(none joined)'}  ",
            f"**Hub:** {self.hub.name} · live service",
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
        return "\n".join(lines)


def make_handler(state: BusState):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):  # keep the console clean
            pass

        def _send(self, code: int, body: str, ctype: str = "application/json"):
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", f"{ctype}; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _json(self, code: int, obj: dict):
            self._send(code, json.dumps(obj))

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/state":
                with state.lock:
                    self._json(200, {
                        "topic": state.topic, "agents": state.agents,
                        "cycle": state.cycle, "halted": state.halted,
                        "messages": len(state.transcript),
                    })
            elif url.path == "/wait":
                name = parse_qs(url.query).get("name", [""])[0]
                self._json(200, state.wait(name))
            elif url.path == "/transcript":
                with state.lock:
                    self._json(200, {"entries": state.transcript})
            elif url.path == "/transcript.md":
                with state.lock:
                    self._send(200, state.markdown(), ctype="text/markdown")
            else:
                self._json(404, {"error": "unknown path"})

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self._json(400, {"error": "bad json"})
                return
            if self.path == "/join":
                self._json(200, state.join(str(body.get("name", "")).strip()))
            elif self.path == "/speak":
                self._json(200, state.speak(
                    str(body.get("name", "")).strip(),
                    str(body.get("layer", "")),
                    str(body.get("content", "")),
                    bool(body.get("red_button")),
                ))
            else:
                self._json(404, {"error": "unknown path"})

    return Handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Boot Clementine (Songline Bus server)")
    parser.add_argument("--port", type=int, default=8777)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--topic", default="first water")
    args = parser.parse_args(argv)

    state = BusState(args.topic)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(state))
    print(f"Clementine is awake on http://{args.host}:{args.port}  topic: {args.topic!r}")
    print("Agents join with: python3 -m clementine.bridge.remote --agent sisters "
          f"--server http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nClementine rests. The sisters remain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

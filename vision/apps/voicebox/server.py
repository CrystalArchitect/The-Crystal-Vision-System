# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Voicebox — a tiny local MCP server that gives Claude Code a voice.

Runs on YOUR machine and speaks through the operating system's own
text-to-speech. Nothing leaves the machine; no cloud, no accounts.

Start it:

    python server.py                # listens on 127.0.0.1:17493

Then register it with Claude Code (one time):

    claude mcp add voicebox --transport http \
        --header "X-Voicebox-Client-Id: claude-code" \
        http://127.0.0.1:17493/mcp

Claude then has a `speak` tool: speak(text) → the machine says it aloud.

TTS backends, picked automatically:
  - Windows:  PowerShell + System.Speech (built in)
  - macOS:    `say` (built in)
  - Linux:    `espeak` or `spd-say` (install one: apt install espeak)

Stdlib only. Implements the minimum of MCP streamable-HTTP that Claude
Code needs: initialize / notifications / tools/list / tools/call over
JSON-RPC POSTs to /mcp.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "voicebox", "version": "0.1.0"}

TOOLS = [
    {
        "name": "speak",
        "description": (
            "Speak text aloud on this machine using the local OS text-to-speech. "
            "Use for short spoken updates; keep it under a few sentences."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "What to say aloud."},
            },
            "required": ["text"],
        },
    },
    {
        "name": "stop_speaking",
        "description": "Stop any speech currently playing.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]

_current: subprocess.Popen | None = None


def _backend() -> list[str] | None:
    """Return the argv prefix for the platform's TTS, or None if unavailable."""
    system = platform.system()
    if system == "Windows":
        return [
            "powershell",
            "-NoProfile",
            "-Command",
            "Add-Type -AssemblyName System.Speech; "
            "(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak($args[0])",
        ]
    if system == "Darwin" and shutil.which("say"):
        return ["say"]
    for cmd in ("espeak", "spd-say"):
        if shutil.which(cmd):
            return [cmd]
    return None


def do_speak(text: str) -> str:
    global _current
    text = " ".join(text.split()).strip()
    if not text:
        return "Nothing to say."
    prefix = _backend()
    if prefix is None:
        return (
            "No local TTS found. Install one (Linux: apt install espeak) "
            "and try again."
        )
    do_stop()
    _current = subprocess.Popen(
        prefix + [text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return f"Speaking ({len(text)} chars)."


def do_stop() -> str:
    global _current
    if _current is not None and _current.poll() is None:
        _current.terminate()
        _current = None
        return "Stopped."
    _current = None
    return "Nothing was speaking."


def handle_rpc(req: dict) -> dict | None:
    """Handle one JSON-RPC message; None means notification (no response)."""
    method = req.get("method", "")
    rpc_id = req.get("id")
    if method.startswith("notifications/"):
        return None
    if method == "initialize":
        result = {
            "protocolVersion": req.get("params", {}).get(
                "protocolVersion", PROTOCOL_VERSION
            ),
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {}) or {}
        if name == "speak":
            text_out = do_speak(str(args.get("text", "")))
        elif name == "stop_speaking":
            text_out = do_stop()
        else:
            return {
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32602, "message": f"unknown tool: {name}"},
            }
        result = {"content": [{"type": "text", "text": text_out}], "isError": False}
    elif method == "ping":
        result = {}
    else:
        return {
            "jsonrpc": "2.0",
            "id": rpc_id,
            "error": {"code": -32601, "message": f"unknown method: {method}"},
        }
    return {"jsonrpc": "2.0", "id": rpc_id, "result": result}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # quiet unless asked
        if self.server.verbose:  # type: ignore[attr-defined]
            sys.stderr.write("voicebox: " + fmt % args + "\n")

    def _send(self, code: int, body: bytes = b"", ctype: str = "application/json"):
        self.send_response(code)
        if body:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_POST(self):
        if self.path.rstrip("/") != "/mcp":
            self._send(404, b'{"error":"not found"}')
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            req = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send(400, b'{"error":"bad json"}')
            return
        resp = handle_rpc(req)
        if resp is None:
            self._send(202)
        else:
            self._send(200, json.dumps(resp).encode())

    def do_GET(self):
        # No server-initiated stream; Claude Code polls with POSTs.
        self._send(405)

    def do_DELETE(self):
        self._send(200)


def main() -> None:
    ap = argparse.ArgumentParser(description="Voicebox local MCP TTS server")
    ap.add_argument("--host", default="127.0.0.1", help="bind address (keep local)")
    ap.add_argument("--port", type=int, default=17493)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    srv.verbose = args.verbose  # type: ignore[attr-defined]
    backend = _backend()
    print(f"voicebox listening on http://{args.host}:{args.port}/mcp")
    print(f"TTS backend: {' '.join(backend[:1]) if backend else 'NONE FOUND'}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        do_stop()


if __name__ == "__main__":
    main()

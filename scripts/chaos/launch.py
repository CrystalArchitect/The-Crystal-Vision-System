#!/usr/bin/env python3
"""Launch Chaos Engine — align, fan-out, optional HTTP surface.

    python3 scripts/chaos/launch.py
    python3 scripts/chaos/launch.py --serve --port 8765
    python3 scripts/chaos/launch.py --serve --no-run   # HTTP only

Canon: no. Counts ≠ verdicts. Human publishes.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crystal_platform.chaos import DEFAULT_CHAOS_SEATS, ChaosEngine
from crystal_platform.orchestration import build_live_stack

# Reuse align audit
sys.path.insert(0, str(ROOT / "scripts" / "chaos"))
import align as chaos_align  # noqa: E402


def _ledger_path(run_id: str) -> Path:
    stamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return ROOT / "14_AI_INTERACTIONS" / "chaos-ledger" / f"{stamp}-LAUNCH-{run_id[:8]}.md"


def run_fanout(topic: str, seats: tuple[str, ...] | None, out: Path | None) -> object:
    engine = ChaosEngine(stack=build_live_stack(provider_ids=("local.open",)))
    result = engine.run(topic, seats=seats)
    path = out or _ledger_path(result.run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.markdown(), encoding="utf-8")
    print(f"Chaos Engine LAUNCHED run={result.run_id}")
    print(
        f"  asked={result.cross_compare['seats_asked']} "
        f"ok={result.cross_compare['seats_ok']} "
        f"silent={result.cross_compare['seats_silent']}"
    )
    for r in result.replies:
        mark = "SILENT" if r.silent else r.status
        print(f"  {r.provider_id:>20} [{mark}]")
    print(f"  ledger={path}")
    return result


def make_handler(engine: ChaosEngine) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: object) -> None:
            sys.stderr.write("chaos-http: " + (fmt % args) + "\n")

        def _json(self, code: int, payload: dict) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in ("/", "/health", "/v1/gateway/chaos/health"):
                self._json(
                    200,
                    {
                        "status": "launched",
                        "engine": "chaos",
                        "canon": False,
                        "seats": list(DEFAULT_CHAOS_SEATS),
                        "note": "count not verdict",
                    },
                )
                return
            self._json(404, {"error": "not found"})

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path not in ("/v1/gateway/chaos", "/chaos"):
                self._json(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                body = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._json(400, {"error": "invalid json"})
                return
            text = body.get("text") or body.get("topic")
            if not text or not isinstance(text, str):
                self._json(400, {"error": "text required"})
                return
            seats = body.get("seats")
            seat_t = tuple(seats) if isinstance(seats, list) and seats else None
            result = engine.run(text, seats=seat_t)
            self._json(
                200,
                {
                    "run_id": result.run_id,
                    "question": result.question,
                    "seats": list(result.seats),
                    "replies": [
                        {
                            "provider_id": r.provider_id,
                            "status": r.status,
                            "text": r.text,
                            "silent": r.silent,
                            "correlation_id": r.correlation_id,
                        }
                        for r in result.replies
                    ],
                    "cross_compare": dict(result.cross_compare),
                    "note": "count not verdict — Canon: no",
                },
            )

    return Handler


def serve(host: str, port: int) -> None:
    engine = ChaosEngine(stack=build_live_stack(provider_ids=("local.open",)))
    httpd = ThreadingHTTPServer((host, port), make_handler(engine))
    print(f"Chaos Engine HTTP LAUNCHED on http://{host}:{port}")
    print(f"  GET  /health")
    print(f"  POST /v1/gateway/chaos  JSON {{\"text\": \"...\"}}")
    print("  Canon: no · Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nChaos Engine HTTP stopped.")
        httpd.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch Chaos Engine")
    parser.add_argument(
        "--topic",
        default="CHAOS ENGINE LAUNCH. Seats on Portal path. Core≠TAI. Canon: no.",
    )
    parser.add_argument("--seats", default="", help="comma-separated provider ids")
    parser.add_argument("--out", default="", help="ledger markdown path")
    parser.add_argument("--serve", action="store_true", help="start HTTP surface")
    parser.add_argument("--no-run", action="store_true", help="skip one-shot fan-out")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--skip-align", action="store_true")
    args = parser.parse_args(argv)

    if not args.skip_align:
        drift = chaos_align.audit()
        if drift:
            print("ALIGN DRIFT — refuse launch:")
            for d in drift:
                print(f"  - {d}")
            return 2
        print("align: DRIFT NONE — launch cleared")

    if not args.no_run:
        seats = tuple(s.strip() for s in args.seats.split(",") if s.strip()) or None
        out = Path(args.out) if args.out else None
        run_fanout(args.topic, seats, out)

    if args.serve:
        serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

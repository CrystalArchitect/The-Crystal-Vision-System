"""API — the blueprint §6 MVP surface for the pipeline (stdlib HTTP).

    python3 -m services.api --port 8899

    POST /v1/decode/preview   body: {"events": [...]} → accepted/quarantined (no storage)
    POST /v1/ingest/events    body: {"events": [...]} → decode + store, report both
    GET  /v1/twin/flows?h3=&class=                    → aggregated flows
"""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .decode import decode_batch
from .ingest import DEFAULT_DB, connect, ingest_events
from .twin import flows


def make_handler(db_path: Path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _json(self, code: int, obj: dict):
            data = json.dumps(obj).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/v1/twin/flows":
                q = parse_qs(url.query)
                conn = connect(db_path)
                try:
                    result = flows(conn, q.get("h3", [""])[0], q.get("class", [""])[0])
                finally:
                    conn.close()
                self._json(200, {"flows": result})
            else:
                self._json(404, {"error": "unknown path"})

        def do_POST(self):
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except json.JSONDecodeError:
                self._json(400, {"error": "bad json"})
                return
            events = body.get("events", [])
            if not isinstance(events, list):
                self._json(400, {"error": "events must be a list"})
                return
            accepted, quarantined = decode_batch(events)
            if self.path == "/v1/decode/preview":
                self._json(200, {"accepted": accepted, "quarantined": quarantined})
            elif self.path == "/v1/ingest/events":
                conn = connect(db_path)
                try:
                    written = ingest_events(conn, accepted)
                finally:
                    conn.close()
                self._json(200, {
                    "decoded": len(accepted),
                    "stored": written,
                    "quarantined": quarantined,
                })
            else:
                self._json(404, {"error": "unknown path"})

    return Handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Crystal Core pipeline API")
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    args = parser.parse_args(argv)

    server = ThreadingHTTPServer((args.host, args.port), make_handler(Path(args.db)))
    print(f"Pipeline API on http://{args.host}:{args.port}  twin store: {args.db}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPipeline API down.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Serve adapter-static output the way GitHub Pages does.

/atlas  -> atlas.html
/atlas/ -> atlas/index.html if present, else atlas.html
/       -> index.html

Used by Lighthouse CI so audits hit the local build, not production.
Not a product claim and not a second host.
"""
from __future__ import annotations

import http.server
import os
import sys
import urllib.parse

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
PORT = int(sys.argv[2] if len(sys.argv) > 2 else 4173)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = urllib.parse.unquote(parsed.path)
        suffix = f"?{parsed.query}" if parsed.query else ""
        mapped = self._map(path)
        if mapped is not None:
            self.path = mapped + suffix
        return super().do_GET()

    def _map(self, path: str) -> str | None:
        if path == "/":
            return "/index.html" if os.path.isfile(os.path.join(ROOT, "index.html")) else None
        if os.path.splitext(path)[1]:
            return None
        rel = path.strip("/")
        if path.endswith("/"):
            indexed = os.path.join(rel, "index.html")
            if os.path.isfile(os.path.join(ROOT, indexed)):
                return "/" + indexed
            html = rel + ".html"
            if os.path.isfile(os.path.join(ROOT, html)):
                return "/" + html
            return None
        html = rel + ".html"
        if os.path.isfile(os.path.join(ROOT, html)):
            return "/" + html
        indexed = os.path.join(rel, "index.html")
        if os.path.isfile(os.path.join(ROOT, indexed)):
            return "/" + indexed
        return None

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    if not os.path.isdir(ROOT):
        sys.stderr.write(f"not a directory: {ROOT}\n")
        sys.exit(1)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"serving static build on 127.0.0.1:{PORT} from {ROOT}", flush=True)
    httpd.serve_forever()

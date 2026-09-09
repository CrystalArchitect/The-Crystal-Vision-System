# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""A small client for the local API, so other clients need not hand-roll one.

`server.py` describes itself at `GET /api`, which tells you what exists.
This turns that surface into Python, so a second interface — the Discord
bot next door, a script, a shell one-liner — is a few lines rather than a
pile of `requests` boilerplate re-derived each time.

It talks HTTP to the running server rather than importing `CrystalCore`
directly, and that is the important decision. Two processes holding the
same companion would both write `memory.json`, and the loser of that race
loses memories. Going through the API keeps exactly one owner of the
files, whatever else is talking to them.

Every method maps onto a route in `api_surface.ROUTES`, and the test suite
holds this client against that table — a method here for a route that does
not exist fails, exactly as a documented-but-unbuilt route does.
"""

from __future__ import annotations

import json
from typing import Iterator

import requests

DEFAULT_BASE = "http://127.0.0.1:5000"


class ClementineOffline(RuntimeError):
    """The server is not running, or not where we were told to look.

    Given its own type because it is far and away the most common failure
    and it is not the caller's fault: the machine was asleep, or nobody
    ran `python server.py`. Anything that surfaces this to a human should
    say that rather than print a connection error.
    """


class ClementineAPIError(RuntimeError):
    """The server answered, and the answer was a refusal."""

    def __init__(self, status: int, body: str):
        self.status = status
        self.body = body
        super().__init__(f"{status}: {body}")


class Clementine:
    """The local companion, over HTTP."""

    def __init__(self, base: str = DEFAULT_BASE, timeout: float = 30.0,
                 session: requests.Session | None = None):
        self.base = base.rstrip("/")
        self.timeout = timeout
        # Injectable so the tests can drive the real code path against a
        # stub transport instead of a live server.
        self.session = session or requests.Session()

    # ---------- plumbing ----------

    def _url(self, path: str) -> str:
        return f"{self.base}{path}"

    def _request(self, method: str, path: str, payload: dict | None = None,
                 stream: bool = False) -> requests.Response:
        try:
            res = self.session.request(
                method, self._url(path),
                json=payload if payload is not None else None,
                # Every POST needs this header or the server answers 415;
                # the rule exists so a cross-origin form cannot reach the
                # write routes. Set explicitly rather than relying on
                # requests inferring it from `json=`, because the bodyless
                # writes (/api/reflect) pass no json at all.
                headers={"Content-Type": "application/json"}
                if method != "GET" else None,
                timeout=self.timeout, stream=stream)
        except requests.exceptions.RequestException as exc:
            raise ClementineOffline(
                f"no Clementine answering at {self.base} — is `python "
                f"server.py` running on that machine?") from exc
        if res.status_code >= 400:
            raise ClementineAPIError(res.status_code, res.text[:500])
        return res

    # ---------- the surface ----------

    def index(self) -> dict:
        """Everything the server says it can do."""
        return self._request("GET", "/api").json()

    def status(self) -> dict:
        return self._request("GET", "/api/status").json()

    def chat_stream(self, message: str) -> Iterator[str]:
        """Say something; yield their reply as it is written.

        Decoded incrementally rather than by lines: the server streams
        prose, not newline-delimited records, so waiting for a newline
        would hold most of a reply in the buffer and undo the streaming.
        """
        res = self._request("POST", "/api/chat/stream",
                            {"message": message}, stream=True)
        for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
            if not chunk:
                continue
            yield chunk if isinstance(chunk, str) else chunk.decode("utf-8", "replace")

    def chat(self, message: str) -> str:
        """The whole reply, for callers that cannot use a stream."""
        return "".join(self.chat_stream(message))

    def memories(self) -> dict:
        return self._request("GET", "/api/memories").json()

    def teach(self, text: str, key: str = "") -> dict:
        return self._request("POST", "/api/teach",
                             {"text": text, "key": key}).json()

    def forget(self, handle: str) -> dict:
        return self._request("POST", "/api/forget", {"handle": handle}).json()

    def reflect(self) -> str:
        # Sends `{}` rather than nothing: the route reads no body, but the
        # server's JSON requirement applies to it all the same — that was
        # the hole /api/reflect had before, reachable by a bodyless
        # cross-site form POST.
        return self._request("POST", "/api/reflect", {}).json().get("insights", "")

    def export(self) -> dict:
        return self._request("GET", "/api/export").json()

    def profiles(self) -> dict:
        return self._request("GET", "/api/profile").json()

    def switch_profile(self, name: str) -> dict:
        return self._request("POST", "/api/profile", {"profile": name}).json()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Clementine(base={self.base!r})"


def describe_offline(base: str) -> str:
    """One sentence a human interface can print when the server is down."""
    return (f"I can't reach Clementine at {base}. She runs on your own "
            f"machine, so this usually means that machine is asleep or "
            f"`python server.py` isn't running on it.")


if __name__ == "__main__":  # pragma: no cover - a smoke check by hand
    c = Clementine()
    try:
        print(json.dumps(c.status(), indent=2))
    except ClementineOffline as exc:
        raise SystemExit(str(exc))

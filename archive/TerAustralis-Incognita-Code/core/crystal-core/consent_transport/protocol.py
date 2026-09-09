# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The wire protocol — what gets said, once the Noise channel is open.

Deliberately tiny: three message types, because pull-based 1:1 exchange
doesn't need more than "ask", "here", and "no."

    REQUEST   {"type": "request", "kinds": [...], "since": ts}
    FRAGMENTS {"type": "fragments", "fragments": [...]}
    DENIED    {"type": "denied", "reason": "..."}

Every message is length-prefixed JSON, encrypted with the Noise session's
per-direction cipher state. Framing is separate from the handshake so the
same framing code serves both directions once split() has happened.
"""

from __future__ import annotations

import json
import socket
import struct
import time

from .noise import CipherState

MAX_FRAME_LEN = 4 * 1024 * 1024  # 4 MiB — fragments are meant to be small


class ProtocolError(Exception):
    """A peer sent something malformed, oversized, or out of sequence."""


def remaining(deadline: float | None) -> None:
    """Raise if the connection's wall-clock budget is gone.

    Per-recv socket timeouts reset on every successful read. A 1-byte
    drip would never hit them. The deadline is monotonic time from
    accept/connect and does not reset.
    """
    if deadline is None:
        return
    if time.monotonic() >= deadline:
        raise ProtocolError("connection lifetime budget exhausted")


def _arm(sock: socket.socket, deadline: float | None) -> None:
    remaining(deadline)
    if deadline is not None:
        sock.settimeout(max(deadline - time.monotonic(), 1e-3))


def send_frame(
    sock: socket.socket, cs: CipherState, obj: dict, deadline: float | None = None
) -> None:
    plaintext = json.dumps(obj, separators=(",", ":")).encode()
    ciphertext = cs.encrypt_with_ad(b"", plaintext)
    if len(ciphertext) > MAX_FRAME_LEN:
        raise ProtocolError("frame too large")
    _arm(sock, deadline)
    sock.sendall(struct.pack(">I", len(ciphertext)) + ciphertext)


def _recv_exact(sock: socket.socket, n: int, deadline: float | None = None) -> bytes:
    buf = bytearray()
    while len(buf) < n:
        _arm(sock, deadline)
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ProtocolError("connection closed mid-frame")
        buf += chunk
    return bytes(buf)


def recv_frame(
    sock: socket.socket, cs: CipherState, deadline: float | None = None
) -> dict:
    (length,) = struct.unpack(">I", _recv_exact(sock, 4, deadline))
    if length > MAX_FRAME_LEN:
        raise ProtocolError("peer announced an oversized frame")
    ciphertext = _recv_exact(sock, length, deadline)
    plaintext = cs.decrypt_with_ad(b"", ciphertext)
    try:
        obj = json.loads(plaintext)
    except json.JSONDecodeError as exc:
        raise ProtocolError("malformed JSON in frame") from exc
    if not isinstance(obj, dict) or "type" not in obj:
        raise ProtocolError("frame missing 'type'")
    return obj


def request(kinds: list[str], since: float = 0.0) -> dict:
    return {"type": "request", "kinds": kinds, "since": since}


def fragments(items: list[dict]) -> dict:
    return {"type": "fragments", "fragments": items}


def denied(reason: str) -> dict:
    return {"type": "denied", "reason": reason}

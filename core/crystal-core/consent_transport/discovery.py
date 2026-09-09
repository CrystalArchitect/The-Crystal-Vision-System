# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Same-LAN discovery — a UDP broadcast, nothing fancier.

This is not full mDNS/Bonjour protocol compliance; it's a small, honest
"who's on this network" broadcast, roughly the same idea. It announces a
public key and a port — never anything else, and never automatically
pairs. Discovery only makes an agent visible; a human still has to accept
the peer before pairing happens, and consent is a separate step again
after that.
"""

from __future__ import annotations

import json
import socket
import time
from dataclasses import dataclass

from .identity import Identity

DISCOVERY_PORT = 8891
ANNOUNCE_TYPE = "starline-hello"

# A beacon carrying a hybrid signing key is ~4.2 KB, up from ~330 bytes when
# the signing key was Ed25519 alone. Two consequences, and the second is not
# fixed here:
#
#   * the read buffer has to be bigger than the beacon, or the datagram is
#     silently truncated and every announcement is discarded as bad JSON;
#   * 4.2 KB exceeds a 1500-byte MTU, so the datagram is IP-fragmented on a
#     real LAN. Loopback (MTU 65536) never shows this, so the self-test
#     passes either way — fragment loss would make LAN discovery flaky in a
#     way no test here would catch.
#
# The real fix is to stop putting the signing key in the beacon at all:
# announce fingerprint, address, port and the small X25519 key, then carry
# the signing key over the TCP connection at pairing. That needs a new
# protocol frame, so it is recorded as known follow-up work rather than
# half-done here. Discovery grants no trust in either design.
ANNOUNCE_BUFFER = 16384


@dataclass
class Announcement:
    from_addr: str
    fingerprint: str
    sign_public_hex: str
    dh_public_hex: str
    label: str
    tcp_port: int


def announce_once(
    identity: Identity,
    tcp_port: int,
    label: str = "",
    broadcast_addr: str = "255.255.255.255",
    discovery_port: int = DISCOVERY_PORT,
) -> None:
    """Send one broadcast packet saying 'here is my public key, on this
    port'. Call this whenever the Starline server starts, or on demand
    when the human asks to be discoverable."""
    payload = json.dumps({
        "type": ANNOUNCE_TYPE,
        "fingerprint": identity.fingerprint,
        "sign_public_hex": identity.sign_public_bytes.hex(),
        "dh_public_hex": identity.dh_public_bytes.hex(),
        "label": label,
        "tcp_port": tcp_port,
    }).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(payload, (broadcast_addr, discovery_port))
    finally:
        sock.close()


def listen_for_peers(
    duration: float = 2.0,
    bind_host: str = "0.0.0.0",
    discovery_port: int = DISCOVERY_PORT,
    own_fingerprint: str | None = None,
) -> list[Announcement]:
    """Listen for announcements for `duration` seconds and return whatever
    was heard, deduplicated by fingerprint. Purely informational — nothing
    here touches the peer store or grants any trust."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind_host, discovery_port))
    sock.settimeout(0.2)

    found: dict[str, Announcement] = {}
    deadline = time.monotonic() + duration
    try:
        while time.monotonic() < deadline:
            try:
                data, addr = sock.recvfrom(ANNOUNCE_BUFFER)
            except socket.timeout:
                continue
            try:
                msg = json.loads(data)
            except json.JSONDecodeError:
                continue
            if msg.get("type") != ANNOUNCE_TYPE:
                continue
            if own_fingerprint and msg.get("fingerprint") == own_fingerprint:
                continue  # don't discover yourself
            ann = Announcement(
                from_addr=addr[0],
                fingerprint=msg["fingerprint"],
                sign_public_hex=msg["sign_public_hex"],
                dh_public_hex=msg["dh_public_hex"],
                label=msg.get("label", ""),
                tcp_port=msg["tcp_port"],
            )
            found[ann.fingerprint] = ann
    finally:
        sock.close()
    return list(found.values())

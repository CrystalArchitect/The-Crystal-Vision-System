# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Watch Consent Transport actually work — two agents, one process, real sockets.

    python3 -m consent_transport.run demo

Runs two agents (in throwaway temp directories, never touching real
identity files), pairs them, shows a request being denied before consent,
grants consent, shows the request succeeding, then revokes and shows the
very next request being denied again. Every step uses the real TCP +
Noise transport — nothing here is simulated.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from .agent import StarlineAgent
from .transport import Denied


def demo() -> None:
    a = StarlineAgent(Path(tempfile.mkdtemp(prefix="starline_demo_a_")))
    b = StarlineAgent(Path(tempfile.mkdtemp(prefix="starline_demo_b_")))
    print(f"Agent A: {a.fingerprint}")
    print(f"Agent B: {b.fingerprint}")

    print("\n-- pairing (like scanning each other's QR code) --")
    a.pair_manual(b.identity.sign_public_bytes.hex(), b.identity.dh_public_bytes.hex(), "b")
    b.pair_manual(a.identity.sign_public_bytes.hex(), a.identity.dh_public_bytes.hex(), "a")
    print("paired.")

    b.add_local_fragment("mythic", "The gate opens by sovereign recognition, not force.")
    print("\nAgent B holds one memory fragment. Agent A has not been granted access.")

    port = b.serve()
    print(f"Agent B is serving on 127.0.0.1:{port} (localhost only).")

    print("\n-- Agent A requests, before consent --")
    try:
        a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        print("UNEXPECTED: request should have been denied")
    except Denied as exc:
        print(f"Denied, as expected: {exc}")

    print("\n-- The human running Agent B grants consent to A --")
    b.grant(a.fingerprint)

    print("-- Agent A requests again --")
    fragments = a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
    for f in fragments:
        verified = f.verify(bytes.fromhex(b.identity.sign_public_bytes.hex()))
        print(f'Received ({f.kind}, signature verified={verified}): "{f.content}"')

    print("\n-- The human running Agent B revokes consent --")
    b.revoke(a.fingerprint)

    print("-- Agent A requests a third time --")
    try:
        a.request_fragments(a.peers.get(b.fingerprint), "127.0.0.1", port)
        print("UNEXPECTED: request should have been denied after revocation")
    except Denied as exc:
        print(f"Denied, as expected: {exc}")

    b.stop_serving()
    print("\nNON SOLUS — but never without consent.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consent Transport demo")
    parser.add_argument(
        "command",
        choices=["demo", "start", "start-ya-bastard"],
        nargs="?",
        default="demo",
    )
    args = parser.parse_args(argv)
    if args.command in ("start", "start-ya-bastard"):
        from .start import main as start_main

        return start_main()
    demo()
    return 0



if __name__ == "__main__":
    raise SystemExit(main())

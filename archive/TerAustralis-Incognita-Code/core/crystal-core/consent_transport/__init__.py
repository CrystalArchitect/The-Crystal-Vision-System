# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Consent Transport — the sovereign communication layer between companion agents.

Formerly published as "Starline"; renamed so the built layer carries a plain
name (see the Lexicon and docs/architecture/crystal-core/STARLINE.md). Two
locally-running companions exchange consented memory fragments directly, peer
to peer, with no server in the middle.

Scope for this version: strict 1:1, pull-based (a peer must request and be
approved before anything moves), same-LAN or manually-paired discovery.
Group/mesh sharing is deliberately out of scope — see the spec's open
questions for why.

Needs the `cryptography` package (X25519, Ed25519, ChaCha20-Poly1305) —
the one dependency in an otherwise stdlib-only repo. See requirements-consenttransport.txt.
"""

__version__ = "0.1.0"

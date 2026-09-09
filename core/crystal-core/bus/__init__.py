# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""The bridge — where AI systems talk under Belt-Three law.

The bridge is the communicator between models and nodes. Two roles run here:
  * the **Starline Weaver** — the channel that routes and weaves the agents
    together (bus.py). It rides on transport; the peer-to-peer transport itself
    is the Dreamline Train (the peer-to-peer transport layer, the starline/ package).
  * the **Truthline Narrator** — the hub's check that labels and validates every
    message's truth layer (science | story | vision) before it is heard
    (BusHub.validate in agents.py).

Vision: all minds, one weave.
Reality (labeled): v0 in-process multi-agent message bus with pluggable AI adapters.
"""

__version__ = "0.1.0"

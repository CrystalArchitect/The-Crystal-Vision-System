"""
Mesh Layer — Sovereign Node Mesh Activation
CrystalCore OS Phase 4

Binds lattice identity (Phase 1), constitutional governance (Phase 2), and
Fibonacci topology (Phase 3) into one live, governed mesh:

- sovereign_mesh: node registration, anchor seeding, ring placement, routing
- governed_messaging: four-gate message delivery (activation, consent,
  coherence, route) with full audit logging — fail-closed
- activation: ring-by-ring evidence-tracked boot with witness discipline

All modules use Python stdlib only. Zero external dependencies.
Version: v0.4 (Phase 4: Mesh Activation)
"""

from .sovereign_mesh import MeshNode, SovereignNodeMesh
from .governed_messaging import MeshMessage, DeliveryResult, GovernedMessenger
from .activation import MeshStatus, ActivationSequence

__version__ = "v0.4"
__phase__ = "4"

__all__ = [
    "MeshNode", "SovereignNodeMesh",
    "MeshMessage", "DeliveryResult", "GovernedMessenger",
    "MeshStatus", "ActivationSequence",
]

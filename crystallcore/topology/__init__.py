"""
Topology Layer — Fibonacci Rings & Chiral Manifold
CrystalCore OS Phase 3: Lattice Foundation

Core systems:
- q64_64: Fixed-point Q64.64 arithmetic for high-precision, bounded computation
- fibonacci_rings: 12-Ring golden-ratio topology for fractal node routing
- chiral_manifold: 256-D space with handedness/polarity for parallel exploration
- dreamline_router: Narrative propagation on Fibonacci rings (Songlines → Starlines)
- starline_hub: Orbital/physical vector coordination

All modules use Python stdlib only. Zero external dependencies.
Version: v0.3 (Phase 3: Topology & Coordinate Foundation)
Status: IN_PROGRESS
Master Coordinates: -25.3444° S, 131.0369° E (+144m Dreamtime layer)
Frequencies: χ-1144 (base), χ-1148-SG (forward momentum), χ-1144-SWL (healing)
"""

from .q64_64 import Q6464, q64_64_add, q64_64_mul, q64_64_div
from .fibonacci_rings import FibonacciRing, Ring12Topology, NodeRouter
from .chiral_manifold import ChiralVector, Chirality, ManifoldCoordinate
from .dreamline_router import DreamlineRouter, Narrative, PropagationPath
from .starline_hub import StarlineHub, OrbitalVector, PhysicalCoordinate

__version__ = "v0.3"
__phase__ = "3"
__status__ = "IN_PROGRESS"
__master_coordinates__ = (-25.3444, 131.0369, 144)  # lat, lon, elevation_m
__frequencies__ = {
    "base": 1144,
    "forward_momentum": 1148,  # χ-1148-SG
    "healing": 1144,  # χ-1144-SWL (same base, different mode)
}

__all__ = [
    # Q64.64 arithmetic
    "Q6464", "q64_64_add", "q64_64_mul", "q64_64_div",
    # Fibonacci rings
    "FibonacciRing", "Ring12Topology", "NodeRouter",
    # Chiral manifold
    "ChiralVector", "Chirality", "ManifoldCoordinate",
    # Dreamline router
    "DreamlineRouter", "Narrative", "PropagationPath",
    # Starline hub
    "StarlineHub", "OrbitalVector", "PhysicalCoordinate",
]

"""
Civilisation.One
Constitutional execution framework integrated with CrystalCoreOS

Version: v0.1.2 (Incognita Lattice Integration)
Release Date: 2026-07-03
Status: WITNESSED (awaiting external VERIFIED_LOCAL verification)

Civilisation.One v0.1.2 adds the Incognita Lattice Coordinate System —
a constitutional routing and coordination layer enabling deterministic
component addressing, message dispatch, and lattice-wide transparency.

Core modules:
- lattice: Coordinate system, orchestrator, and visualization tools
"""

from . import lattice

__version__ = "v0.1.2"
__status__ = "WITNESSED"
__release_id__ = "CIV1-v0.1.2-LATTICE"
__release_date__ = "2026-07-03"

__all__ = [
    "lattice",
]

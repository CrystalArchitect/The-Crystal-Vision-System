"""
Incognita Lattice Coordinate System
Part of Civilisation.One + CrystalCoreOS integration

Version: v0.1
Status: PROPOSED (awaiting external verification)

Core modules for lattice-based component addressing, routing, and coordination.
"""

from .coordinate import (
    LatticeCoordinate,
    CoordinateRegistry,
    get_global_registry,
    register_coordinate,
    lookup_coordinate
)

from .orchestrator import (
    RoutingTable,
    MessageEnvelope,
    LatticeOrchestrator,
    OrchestratorFactory
)

from .graph_utils import (
    LatticeGraph,
    LayerVisualizer,
    ConformanceVisualizer,
    ComplianceReport,
    format_coordinate_table
)

__version__ = "v0.1"
__status__ = "PROPOSED"

__all__ = [
    "LatticeCoordinate",
    "CoordinateRegistry",
    "get_global_registry",
    "register_coordinate",
    "lookup_coordinate",
    "RoutingTable",
    "MessageEnvelope",
    "LatticeOrchestrator",
    "OrchestratorFactory",
    "LatticeGraph",
    "LayerVisualizer",
    "ConformanceVisualizer",
    "ComplianceReport",
    "format_coordinate_table",
]

"""
Incognita Lattice Coordinate System
Part of Civilisation.One + CrystalCoreOS integration
Version: v0.1 (Addressing & Registry)

Provides deterministic component identification, routing, and verification
for the Incognita Lattice — a constitutional routing layer enabling
component addressing, message dispatch, and lattice-wide transparency.

Format: (Layer, Agent, Session, Version)
Route key: Layer:Agent:Session (for message routing)
Full key: Layer:Agent:Session:Version (for versioned identification)
Hash: SHA256 deterministic hash for replay verification
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid
import hashlib
import json


class LatticeCoordinate:
    """
    Represents a unique position in the lattice.

    Every component (Mind agent, Memory layer, Flow processor) has a
    coordinate that identifies it unambiguously and enables routing.

    Attributes:
        layer: Lattice layer (Mind, Memory, Flow, Evolve, Lattice, etc.)
        agent: Agent/component name within the layer
        session: Session identifier (instance, deployment, environment)
        version: Version string (e.g., v0.1, v1.2, prod-v0.1)
    """

    def __init__(self, layer: str, agent: str, session: str, version: str):
        """
        Initialize a lattice coordinate.

        Args:
            layer: Lattice layer name
            agent: Component/agent name
            session: Session or instance identifier
            version: Version identifier
        """
        self.layer = layer
        self.agent = agent
        self.session = session
        self.version = version
        self.coordinate_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow().isoformat()

    def __str__(self) -> str:
        """String representation."""
        return f"({self.layer}, {self.agent}, {self.session}, {self.version})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"LatticeCoordinate{self}"

    def __eq__(self, other: object) -> bool:
        """Equality based on full key."""
        if not isinstance(other, LatticeCoordinate):
            return NotImplemented
        return self.full_key() == other.full_key()

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.full_key())

    def route_key(self) -> str:
        """
        Get the route key for message routing.

        Format: Layer:Agent:Session
        """
        return f"{self.layer}:{self.agent}:{self.session}"

    def full_key(self) -> str:
        """
        Get the full key including version.

        Format: Layer:Agent:Session:Version
        """
        return f"{self.layer}:{self.agent}:{self.session}:{self.version}"

    def compute_hash(self) -> str:
        """
        Compute deterministic SHA256 hash of the coordinate.

        Returns:
            40-character hex digest for integrity verification
        """
        key_string = self.full_key()
        return hashlib.sha256(key_string.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize to dictionary.

        Returns:
            Dictionary with all coordinate data including derived fields
        """
        return {
            "layer": self.layer,
            "agent": self.agent,
            "session": self.session,
            "version": self.version,
            "route_key": self.route_key(),
            "full_key": self.full_key(),
            "hash": self.compute_hash(),
            "coordinate_id": self.coordinate_id,
            "created_at": self.created_at
        }

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_route_key(cls, route_key: str, version: str) -> "LatticeCoordinate":
        """
        Parse coordinate from route key.

        Args:
            route_key: String in format "Layer:Agent:Session"
            version: Version string

        Returns:
            LatticeCoordinate instance

        Raises:
            ValueError: If route_key is not in correct format
        """
        parts = route_key.split(":")
        if len(parts) != 3:
            raise ValueError(f"Route key must be Layer:Agent:Session, got {route_key}")
        return cls(parts[0], parts[1], parts[2], version)

    @classmethod
    def from_full_key(cls, full_key: str) -> "LatticeCoordinate":
        """
        Parse coordinate from full key.

        Args:
            full_key: String in format "Layer:Agent:Session:Version"

        Returns:
            LatticeCoordinate instance

        Raises:
            ValueError: If full_key is not in correct format
        """
        parts = full_key.split(":")
        if len(parts) != 4:
            raise ValueError(f"Full key must be Layer:Agent:Session:Version, got {full_key}")
        return cls(parts[0], parts[1], parts[2], parts[3])

    def same_component(self, other: "LatticeCoordinate") -> bool:
        """
        Check if another coordinate represents the same component (ignoring version).

        Args:
            other: LatticeCoordinate to compare

        Returns:
            True if layer, agent, and session match
        """
        return (self.layer == other.layer and
                self.agent == other.agent and
                self.session == other.session)

    def is_newer_version(self, other: "LatticeCoordinate") -> bool:
        """
        Check if this coordinate's version is newer than another.

        Simple string comparison; assumes semantic versioning.
        Args:
            other: LatticeCoordinate to compare

        Returns:
            True if this version is greater than other's version
        """
        return self.version > other.version


class CoordinateRegistry:
    """
    Central registry for all coordinates in the lattice.

    Tracks registered coordinates, prevents collisions, and enables
    lookup by layer, agent, or full key.
    """

    def __init__(self):
        """Initialize empty registry."""
        self.coordinates: Dict[str, LatticeCoordinate] = {}
        self.by_layer: Dict[str, List[str]] = {}
        self.by_agent: Dict[str, List[str]] = {}
        self.creation_log: List[Dict[str, Any]] = []

    def register(self, coord: LatticeCoordinate) -> bool:
        """
        Register a coordinate.

        Args:
            coord: LatticeCoordinate to register

        Returns:
            True if registered; False if collision (duplicate)
        """
        full_key = coord.full_key()

        if full_key in self.coordinates:
            return False

        self.coordinates[full_key] = coord

        if coord.layer not in self.by_layer:
            self.by_layer[coord.layer] = []
        self.by_layer[coord.layer].append(full_key)

        if coord.agent not in self.by_agent:
            self.by_agent[coord.agent] = []
        self.by_agent[coord.agent].append(full_key)

        self.creation_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": "REGISTER",
            "full_key": full_key,
            "layer": coord.layer,
            "agent": coord.agent
        })

        return True

    def lookup(self, full_key: str) -> Optional[LatticeCoordinate]:
        """
        Look up a coordinate by full key.

        Args:
            full_key: Full key to look up

        Returns:
            LatticeCoordinate if found; None otherwise
        """
        return self.coordinates.get(full_key)

    def list_layer(self, layer: str) -> List[LatticeCoordinate]:
        """
        List all coordinates in a layer.

        Args:
            layer: Layer name

        Returns:
            List of LatticeCoordinates in that layer
        """
        keys = self.by_layer.get(layer, [])
        return [self.coordinates[key] for key in keys]

    def list_agent(self, agent: str) -> List[LatticeCoordinate]:
        """
        List all coordinates for an agent (across all layers).

        Args:
            agent: Agent name

        Returns:
            List of LatticeCoordinates for that agent
        """
        keys = self.by_agent.get(agent, [])
        return [self.coordinates[key] for key in keys]

    def lookup_by_route(self, route_key: str) -> List[LatticeCoordinate]:
        """
        Find all versions of a component by route key.

        Args:
            route_key: Route key (Layer:Agent:Session)

        Returns:
            List of all coordinates matching that route key
        """
        results = []
        for coord in self.coordinates.values():
            if coord.route_key() == route_key:
                results.append(coord)
        return results

    def get_creation_log(self) -> List[Dict[str, Any]]:
        """Get the registration log."""
        return self.creation_log.copy()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize registry state."""
        return {
            "total_registered": len(self.coordinates),
            "layers": sorted(self.by_layer.keys()),
            "agents": sorted(self.by_agent.keys()),
            "coordinates": {k: v.to_dict() for k, v in self.coordinates.items()}
        }


_global_registry: Optional[CoordinateRegistry] = None


def get_global_registry() -> CoordinateRegistry:
    """
    Get the global coordinate registry singleton.

    Returns:
        Global CoordinateRegistry instance
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = CoordinateRegistry()
    return _global_registry


def register_coordinate(coord: LatticeCoordinate) -> bool:
    """
    Register a coordinate in the global registry.

    Args:
        coord: LatticeCoordinate to register

    Returns:
        True if registered; False if collision
    """
    return get_global_registry().register(coord)


def lookup_coordinate(full_key: str) -> Optional[LatticeCoordinate]:
    """
    Look up a coordinate in the global registry.

    Args:
        full_key: Full key to look up

    Returns:
        LatticeCoordinate if found; None otherwise
    """
    return get_global_registry().lookup(full_key)

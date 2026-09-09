#!/usr/bin/env python3
"""
Starline Hub — Orbital/Physical Vector Coordination
Phase 3: Red Dust to Rockets

Starline Hub manages physical/orbital coordinates and logistics:
- Pilbara Starbase South (ground anchor)
- Starship/Optimus deployment vectors
- Orbital mesh (Starlink + sovereign satellites)
- Cross-planetary coordination
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math


class VectorType(Enum):
    """Types of physical vectors."""
    GROUND = "ground"               # Terrestrial (Pilbara, Outback)
    ORBITAL = "orbital"             # Satellite/LEO
    TRANSFER = "transfer"           # Interplanetary
    LAUNCH = "launch"               # Launch vehicle
    LOGISTICS = "logistics"         # Supply/coordination


@dataclass
class OrbitalVector:
    """Orbital trajectory or position vector."""
    vector_id: str
    vector_type: VectorType
    latitude: float
    longitude: float
    altitude_m: float  # Altitude in meters
    velocity_ms: float = 0.0  # Velocity in m/s
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)

    def distance_to(self, other: "OrbitalVector") -> float:
        """Haversine distance on ellipsoid."""
        R_EARTH = 6371000.0  # Earth radius in meters
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        distance_m = R_EARTH * c

        # Add altitude difference
        alt_diff = abs(self.altitude_m - other.altitude_m)
        return math.sqrt(distance_m**2 + alt_diff**2)

    def is_in_range(self, other: "OrbitalVector", range_m: float) -> bool:
        """Check if another vector is within range."""
        return self.distance_to(other) <= range_m


@dataclass
class PhysicalCoordinate:
    """A physical location with orbital implications."""
    coordinate_id: str
    name: str
    latitude: float
    longitude: float
    elevation_m: float
    vectors: Dict[str, OrbitalVector] = field(default_factory=dict)
    capacity: int = 1  # Node capacity
    operational: bool = True
    metadata: Dict = field(default_factory=dict)

    def add_vector(self, vector: OrbitalVector) -> bool:
        if vector.vector_id in self.vectors:
            return False
        self.vectors[vector.vector_id] = vector
        return True

    def get_active_vectors(self) -> List[OrbitalVector]:
        """Get all active vectors at this coordinate."""
        return list(self.vectors.values())


class StarlineHub:
    """Coordinate physical/orbital infrastructure."""

    def __init__(self):
        self.coordinates: Dict[str, PhysicalCoordinate] = {}
        self.vectors: Dict[str, OrbitalVector] = {}
        self.routes: Dict[Tuple[str, str], List[OrbitalVector]] = {}

        # Initialize key Australian locations
        self._init_anchor_coordinates()

    def _init_anchor_coordinates(self):
        """Initialize key Australian coordinates."""
        # Uluru (Dreamtime anchor, -25.3444° S, 131.0369° E, +144m)
        self.add_coordinate(PhysicalCoordinate(
            coordinate_id="uluru_anchor",
            name="Uluru Dreamtime Anchor",
            latitude=-25.3444,
            longitude=131.0369,
            elevation_m=144,
            capacity=10,
            metadata={"type": "dreamtime_anchor", "sacred": True}
        ))

        # Pilbara Starbase South (proposed)
        self.add_coordinate(PhysicalCoordinate(
            coordinate_id="pilbara_starbase",
            name="Pilbara Starbase South",
            latitude=-22.5,
            longitude=118.3,
            elevation_m=50,
            capacity=50,
            metadata={"type": "launch_facility", "sovereign": True}
        ))

        # Alice Springs (coordination hub)
        self.add_coordinate(PhysicalCoordinate(
            coordinate_id="alice_springs",
            name="Alice Springs Hub",
            latitude=-23.7,
            longitude=133.9,
            elevation_m=546,
            capacity=30,
            metadata={"type": "coordination_hub"}
        ))

    def add_coordinate(self, coord: PhysicalCoordinate) -> bool:
        """Add physical coordinate to hub."""
        if coord.coordinate_id in self.coordinates:
            return False
        self.coordinates[coord.coordinate_id] = coord
        return True

    def add_vector(self, coord_id: str, vector: OrbitalVector) -> bool:
        """Add orbital vector to coordinate."""
        coord = self.coordinates.get(coord_id)
        if not coord:
            return False
        self.vectors[vector.vector_id] = vector
        return coord.add_vector(vector)

    def compute_coverage(self, range_m: float) -> Dict[str, List[str]]:
        """Compute what vectors cover which coordinates."""
        coverage = {}
        for vector_id, vector in self.vectors.items():
            coverage[vector_id] = []
            for coord in self.coordinates.values():
                check_vector = OrbitalVector(
                    vector_id="check",
                    vector_type=coord.vectors.get("ground", vector).vector_type if coord.vectors else vector.vector_type,
                    latitude=coord.latitude,
                    longitude=coord.longitude,
                    altitude_m=coord.elevation_m
                )
                if vector.is_in_range(check_vector, range_m):
                    coverage[vector_id].append(coord.coordinate_id)
        return coverage

    def optimal_launch_window(self, from_coord: str, to_coord: str) -> Optional[OrbitalVector]:
        """Compute optimal launch vector from source to destination."""
        source = self.coordinates.get(from_coord)
        target = self.coordinates.get(to_coord)
        if not source or not target:
            return None

        distance = math.sqrt(
            (target.latitude - source.latitude)**2 +
            (target.longitude - source.longitude)**2 +
            ((target.elevation_m - source.elevation_m) / 1000.0)**2
        )

        # Estimate required velocity (simplified)
        required_velocity = distance * 100  # Placeholder

        launch_vector = OrbitalVector(
            vector_id=f"launch_{from_coord}_to_{to_coord}",
            vector_type=VectorType.LAUNCH,
            latitude=source.latitude,
            longitude=source.longitude,
            altitude_m=source.elevation_m,
            velocity_ms=required_velocity,
            metadata={
                "source": from_coord,
                "target": to_coord,
                "distance_km": distance
            }
        )

        return launch_vector

    def mesh_connectivity(self) -> Dict[str, List[str]]:
        """Compute connectivity between coordinates."""
        connectivity = {}
        COMMS_RANGE = 50000000  # 50,000 km

        for coord_id, coord in self.coordinates.items():
            connectivity[coord_id] = []
            for other_id, other in self.coordinates.items():
                if coord_id != other_id:
                    check_vector_a = OrbitalVector(
                        vector_id="check_a",
                        vector_type=VectorType.ORBITAL,
                        latitude=coord.latitude,
                        longitude=coord.longitude,
                        altitude_m=coord.elevation_m
                    )
                    check_vector_b = OrbitalVector(
                        vector_id="check_b",
                        vector_type=VectorType.ORBITAL,
                        latitude=other.latitude,
                        longitude=other.longitude,
                        altitude_m=other.elevation_m
                    )
                    if check_vector_a.is_in_range(check_vector_b, COMMS_RANGE):
                        connectivity[coord_id].append(other_id)

        return connectivity

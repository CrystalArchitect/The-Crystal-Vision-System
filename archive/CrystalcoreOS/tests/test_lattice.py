"""
Comprehensive test suite for Incognita Lattice Coordinate System

Tests cover:
- Coordinate creation and string representation
- Routing and key generation
- Hash determinism
- Parsing and serialization
- Registry operations
- Version comparison
- Collision detection
"""

import pytest
from civilisation_one.lattice.coordinate import (
    LatticeCoordinate,
    CoordinateRegistry,
    get_global_registry
)


class TestLatticeCoordinateCreation:
    """Test coordinate creation and basic operations."""

    def test_coordinate_creation(self):
        """Test basic coordinate instantiation."""
        coord = LatticeCoordinate("Mind", "TruthSeeker", "session-001", "v0.1")
        assert coord.layer == "Mind"
        assert coord.agent == "TruthSeeker"
        assert coord.session == "session-001"
        assert coord.version == "v0.1"

    def test_coordinate_str(self):
        """Test string representation."""
        coord = LatticeCoordinate("Mind", "Guardian", "sess-2", "v0.2")
        assert str(coord) == "(Mind, Guardian, sess-2, v0.2)"

    def test_coordinate_repr(self):
        """Test developer-friendly repr."""
        coord = LatticeCoordinate("Memory", "Layer1", "inst", "v1")
        assert repr(coord).startswith("LatticeCoordinate")
        assert "(Memory, Layer1, inst, v1)" in repr(coord)


class TestCoordinateKeys:
    """Test route and full key generation."""

    def test_route_key(self):
        """Test route key format (Layer:Agent:Session)."""
        coord = LatticeCoordinate("Mind", "Visionary", "s1", "v0.1")
        assert coord.route_key() == "Mind:Visionary:s1"

    def test_full_key(self):
        """Test full key format (Layer:Agent:Session:Version)."""
        coord = LatticeCoordinate("Lattice", "Creator", "s99", "v2.0")
        assert coord.full_key() == "Lattice:Creator:s99:v2.0"

    def test_route_key_consistency(self):
        """Test that route key is consistent across multiple calls."""
        coord = LatticeCoordinate("X", "Y", "Z", "v1")
        key1 = coord.route_key()
        key2 = coord.route_key()
        assert key1 == key2


class TestCoordinateHash:
    """Test hash computation and determinism."""

    def test_hash_computation(self):
        """Test that hash is computed correctly."""
        coord = LatticeCoordinate("Layer1", "Agent1", "Session1", "v0.1")
        hash_val = coord.compute_hash()
        assert isinstance(hash_val, str)
        assert len(hash_val) == 64

    def test_hash_determinism(self):
        """Test that identical coordinates produce identical hashes."""
        coord1 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord2 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        assert coord1.compute_hash() == coord2.compute_hash()

    def test_hash_differences(self):
        """Test that different coordinates produce different hashes."""
        coord1 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord2 = LatticeCoordinate("Mind", "TruthSeeker", "s1", "v0.1")
        assert coord1.compute_hash() != coord2.compute_hash()


class TestCoordinateSerialization:
    """Test serialization to dict and JSON."""

    def test_to_dict(self):
        """Test dictionary serialization."""
        coord = LatticeCoordinate("Mind", "Visionary", "s100", "v1.5")
        d = coord.to_dict()
        assert d["layer"] == "Mind"
        assert d["agent"] == "Visionary"
        assert d["session"] == "s100"
        assert d["version"] == "v1.5"
        assert "hash" in d
        assert "created_at" in d
        assert "coordinate_id" in d

    def test_to_json(self):
        """Test JSON serialization."""
        coord = LatticeCoordinate("Memory", "CrystalMemory", "inst", "v0.8")
        json_str = coord.to_json()
        assert isinstance(json_str, str)
        assert '"layer": "Memory"' in json_str
        assert '"agent": "CrystalMemory"' in json_str

    def test_dict_contains_route_key(self):
        """Test that to_dict includes route_key."""
        coord = LatticeCoordinate("X", "Y", "Z", "v1")
        d = coord.to_dict()
        assert d["route_key"] == "X:Y:Z"

    def test_dict_contains_full_key(self):
        """Test that to_dict includes full_key."""
        coord = LatticeCoordinate("X", "Y", "Z", "v1")
        d = coord.to_dict()
        assert d["full_key"] == "X:Y:Z:v1"


class TestCoordinateParsing:
    """Test parsing from route and full keys."""

    def test_from_route_key(self):
        """Test parsing from route key."""
        coord = LatticeCoordinate.from_route_key("Mind:Guardian:session-1", "v0.2")
        assert coord.layer == "Mind"
        assert coord.agent == "Guardian"
        assert coord.session == "session-1"
        assert coord.version == "v0.2"

    def test_from_route_key_invalid(self):
        """Test that invalid route key raises error."""
        with pytest.raises(ValueError):
            LatticeCoordinate.from_route_key("Invalid:Format")

    def test_from_full_key(self):
        """Test parsing from full key."""
        coord = LatticeCoordinate.from_full_key("Lattice:Incognita:prod:v1.0")
        assert coord.layer == "Lattice"
        assert coord.agent == "Incognita"
        assert coord.session == "prod"
        assert coord.version == "v1.0"

    def test_from_full_key_invalid(self):
        """Test that invalid full key raises error."""
        with pytest.raises(ValueError):
            LatticeCoordinate.from_full_key("Too:Many:Parts:Here:Extra")

    def test_round_trip_full_key(self):
        """Test parsing and re-serializing full key."""
        original_key = "Mind:TruthSeeker:session-1:v0.5"
        coord = LatticeCoordinate.from_full_key(original_key)
        reconstructed_key = coord.full_key()
        assert original_key == reconstructed_key


class TestCoordinateComparison:
    """Test equality and version comparison."""

    def test_equality(self):
        """Test coordinate equality."""
        coord1 = LatticeCoordinate("Layer", "Agent", "Session", "v1")
        coord2 = LatticeCoordinate("Layer", "Agent", "Session", "v1")
        assert coord1 == coord2

    def test_inequality(self):
        """Test coordinate inequality."""
        coord1 = LatticeCoordinate("Layer1", "Agent", "Session", "v1")
        coord2 = LatticeCoordinate("Layer2", "Agent", "Session", "v1")
        assert coord1 != coord2

    def test_hash_usable_in_set(self):
        """Test that coordinates can be used in sets."""
        coord1 = LatticeCoordinate("L", "A", "S", "v1")
        coord2 = LatticeCoordinate("L", "A", "S", "v1")
        coord3 = LatticeCoordinate("L", "A", "S", "v2")
        s = {coord1, coord2, coord3}
        assert len(s) == 2

    def test_same_component(self):
        """Test same_component (ignoring version)."""
        coord1 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord2 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.2")
        assert coord1.same_component(coord2)

    def test_is_newer_version(self):
        """Test version comparison."""
        coord_old = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord_new = LatticeCoordinate("Mind", "Guardian", "s1", "v0.2")
        assert coord_new.is_newer_version(coord_old)
        assert not coord_old.is_newer_version(coord_new)


class TestCoordinateRegistry:
    """Test registry operations."""

    def test_registry_register(self):
        """Test registering a coordinate."""
        registry = CoordinateRegistry()
        coord = LatticeCoordinate("Mind", "Visionary", "test", "v0.1")
        result = registry.register(coord)
        assert result is True

    def test_registry_collision_detection(self):
        """Test that duplicate registrations are rejected."""
        registry = CoordinateRegistry()
        coord1 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord2 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        assert registry.register(coord1) is True
        assert registry.register(coord2) is False

    def test_registry_lookup(self):
        """Test looking up a coordinate."""
        registry = CoordinateRegistry()
        coord = LatticeCoordinate("Memory", "Layer", "test", "v0.8")
        registry.register(coord)
        found = registry.lookup(coord.full_key())
        assert found == coord

    def test_registry_lookup_not_found(self):
        """Test lookup of non-existent coordinate."""
        registry = CoordinateRegistry()
        found = registry.lookup("nonexistent:key:here:v1")
        assert found is None

    def test_registry_list_layer(self):
        """Test listing all coordinates in a layer."""
        registry = CoordinateRegistry()
        coord1 = LatticeCoordinate("Mind", "TruthSeeker", "s1", "v0.1")
        coord2 = LatticeCoordinate("Mind", "Guardian", "s2", "v0.1")
        coord3 = LatticeCoordinate("Memory", "Layer", "s3", "v0.8")

        registry.register(coord1)
        registry.register(coord2)
        registry.register(coord3)

        mind_coords = registry.list_layer("Mind")
        assert len(mind_coords) == 2
        assert coord1 in mind_coords
        assert coord2 in mind_coords

    def test_registry_list_agent(self):
        """Test listing all coordinates for an agent."""
        registry = CoordinateRegistry()
        coord1 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord2 = LatticeCoordinate("Memory", "Guardian", "s2", "v0.1")
        coord3 = LatticeCoordinate("Mind", "TruthSeeker", "s3", "v0.1")

        registry.register(coord1)
        registry.register(coord2)
        registry.register(coord3)

        guardian_coords = registry.list_agent("Guardian")
        assert len(guardian_coords) == 2
        assert coord1 in guardian_coords
        assert coord2 in guardian_coords

    def test_registry_lookup_by_route(self):
        """Test finding all versions of a component."""
        registry = CoordinateRegistry()
        coord1 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.1")
        coord2 = LatticeCoordinate("Mind", "Guardian", "s1", "v0.2")

        registry.register(coord1)
        registry.register(coord2)

        results = registry.lookup_by_route("Mind:Guardian:s1")
        assert len(results) == 2

    def test_registry_creation_log(self):
        """Test that creation log is maintained."""
        registry = CoordinateRegistry()
        coord = LatticeCoordinate("X", "Y", "Z", "v1")
        registry.register(coord)

        log = registry.get_creation_log()
        assert len(log) == 1
        assert log[0]["full_key"] == "X:Y:Z:v1"

    def test_registry_to_dict(self):
        """Test serializing registry to dictionary."""
        registry = CoordinateRegistry()
        coord = LatticeCoordinate("Mind", "TruthSeeker", "s1", "v0.1")
        registry.register(coord)

        d = registry.to_dict()
        assert d["total_registered"] == 1
        assert "Mind" in d["layers"]
        assert "TruthSeeker" in d["agents"]


class TestGlobalRegistry:
    """Test the global singleton registry."""

    def test_get_global_registry(self):
        """Test accessing the global registry."""
        registry = get_global_registry()
        assert isinstance(registry, CoordinateRegistry)

    def test_global_registry_singleton(self):
        """Test that get_global_registry returns the same instance."""
        reg1 = get_global_registry()
        reg2 = get_global_registry()
        assert reg1 is reg2


class TestCoordinateIntegration:
    """Integration tests combining multiple features."""

    def test_full_workflow(self):
        """Test a complete workflow: create, hash, serialize, parse, lookup."""
        coord = LatticeCoordinate("Mind", "Guardian", "workflow-test", "v0.3")

        hash_val = coord.compute_hash()
        assert len(hash_val) == 64

        d = coord.to_dict()
        assert d["hash"] == hash_val

        parsed = LatticeCoordinate.from_full_key(coord.full_key())
        assert parsed.compute_hash() == hash_val

        registry = CoordinateRegistry()
        registry.register(coord)
        found = registry.lookup(coord.full_key())
        assert found == coord

    def test_version_migration_workflow(self):
        """Test upgrading from v0.1 to v0.2 of an agent."""
        old_coord = LatticeCoordinate("Mind", "TruthSeeker", "prod", "v0.1")
        new_coord = LatticeCoordinate("Mind", "TruthSeeker", "prod", "v0.2")

        assert old_coord.same_component(new_coord)
        assert new_coord.is_newer_version(old_coord)
        assert old_coord.compute_hash() != new_coord.compute_hash()

        registry = CoordinateRegistry()
        assert registry.register(old_coord)
        assert registry.register(new_coord)

        matches = registry.lookup_by_route("Mind:TruthSeeker:prod")
        assert len(matches) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

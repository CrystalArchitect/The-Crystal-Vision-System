#!/usr/bin/env python3
"""
Sovereign Node Mesh — Phase 4: Mesh Activation
CrystalCore OS

Binds the three lower layers into one operating mesh:
- Phase 1 lattice: coordinate identity for every node
- Phase 2 governance: constitutional gates (enforced by GovernedMessenger)
- Phase 3 topology: 12-Ring Fibonacci placement and routing

A MeshNode is a physical-or-logical participant with a ring placement and
optional geographic anchor. The mesh starts DORMANT; nodes are activated by
the ActivationSequence and messages only flow between activated nodes.

Standard library only.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field

from crystallcore.topology.fibonacci_rings import Ring12Topology, NodeRouter, RINGS
from crystallcore.topology.starline_hub import StarlineHub


@dataclass
class MeshNode:
    """A participant in the Sovereign Node Mesh."""
    node_id: str
    name: str
    ring: int
    position: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_m: Optional[float] = None
    coherence: float = 1.0
    activated: bool = False
    metadata: Dict = field(default_factory=dict)

    def is_anchored(self) -> bool:
        """True if node has a physical geographic anchor."""
        return self.latitude is not None and self.longitude is not None


class SovereignNodeMesh:
    """The unified mesh: lattice identity + Fibonacci topology + anchors."""

    def __init__(self):
        self.topology = Ring12Topology()
        self.router = NodeRouter(self.topology)
        self.hub = StarlineHub()
        self.nodes: Dict[str, MeshNode] = {}

    # ------------------------------------------------------------------ #
    # Node registration & linking
    # ------------------------------------------------------------------ #
    def register_node(self, node_id: str, name: str, ring: int, position: int,
                      latitude: Optional[float] = None,
                      longitude: Optional[float] = None,
                      elevation_m: Optional[float] = None,
                      coherence: float = 1.0) -> Optional[MeshNode]:
        """Register a node in the mesh. Returns the node, or None on conflict."""
        if node_id in self.nodes:
            return None
        if not self.topology.add_node(node_id, ring, position, coherence):
            return None

        node = MeshNode(
            node_id=node_id, name=name, ring=ring, position=position,
            latitude=latitude, longitude=longitude, elevation_m=elevation_m,
            coherence=coherence,
        )
        self.nodes[node_id] = node
        return node

    def link(self, node_id_a: str, node_id_b: str) -> bool:
        """Create a bidirectional mesh link."""
        if node_id_a not in self.nodes or node_id_b not in self.nodes:
            return False
        return self.topology.connect_nodes(node_id_a, node_id_b)

    def seed_anchors(self) -> List[str]:
        """Seed the mesh with the StarlineHub anchor coordinates.

        Ring 0: Uluru (Dreamtime anchor, mesh root)
        Ring 1: Alice Springs (coordination), Pilbara Starbase (launch)
        All anchors are linked to the root and to each other.
        """
        placements = {
            "uluru_anchor": (0, 0),
            "alice_springs": (1, 0),
            "pilbara_starbase": (1, 1),
        }
        seeded = []
        for coord_id, (ring, position) in placements.items():
            coord = self.hub.coordinates.get(coord_id)
            if not coord:
                continue
            node = self.register_node(
                node_id=coord_id, name=coord.name, ring=ring, position=position,
                latitude=coord.latitude, longitude=coord.longitude,
                elevation_m=coord.elevation_m,
            )
            if node:
                seeded.append(coord_id)

        # Fully connect the anchor triangle
        self.link("uluru_anchor", "alice_springs")
        self.link("uluru_anchor", "pilbara_starbase")
        self.link("alice_springs", "pilbara_starbase")
        self.topology.set_root("uluru_anchor")
        return seeded

    # ------------------------------------------------------------------ #
    # Routing & inspection
    # ------------------------------------------------------------------ #
    def route(self, from_node: str, to_node: str) -> List[str]:
        """Shortest mesh route between two nodes."""
        return self.router.route(from_node, to_node)

    def get_ring_nodes(self, ring: int) -> List[MeshNode]:
        """All mesh nodes placed on a ring."""
        return [n for n in self.nodes.values() if n.ring == ring]

    def activated_nodes(self) -> List[MeshNode]:
        return [n for n in self.nodes.values() if n.activated]

    def mesh_report(self) -> Dict:
        """Summary of mesh state."""
        health = self.topology.network_health()
        return {
            "total_nodes": len(self.nodes),
            "activated_nodes": len(self.activated_nodes()),
            "anchored_nodes": sum(1 for n in self.nodes.values() if n.is_anchored()),
            "rings_populated": len({n.ring for n in self.nodes.values()}),
            "rings_total": RINGS,
            "root": self.topology.root_node,
            **health,
        }

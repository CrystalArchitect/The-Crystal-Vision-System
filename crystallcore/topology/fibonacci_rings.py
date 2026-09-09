#!/usr/bin/env python3
"""
12-Ring Fibonacci Topology
Phase 3: Fractal Resilience & Golden-Ratio Routing

The 12-Ring topology uses Fibonacci sequences to create self-similar,
scale-free networks. Each ring contains φ^n nodes (where φ = golden ratio).
Rings tessellate via Fibonacci recursion, enabling efficient routing and
natural load balancing through golden-ratio scaling.

Applications:
- Sovereign Node Mesh: Uluru-centric to Pilbara/orbit
- Dreamline propagation: Narrative through nested Fibonacci rings
- Fractal resilience: Damage to one ring doesn't collapse the mesh
"""

from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from math import sqrt


# Golden ratio
PHI = (1 + sqrt(5)) / 2
RINGS = 12
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]  # First 12 Fibonacci numbers


@dataclass
class Node:
    """A node in the Fibonacci ring topology."""
    node_id: str
    ring: int                          # Ring number (0-11)
    position: int                      # Position within ring
    neighbors: Set[str] = field(default_factory=set)
    coherence: float = 1.0             # Node coherence (0.0-1.0)
    data: Dict = field(default_factory=dict)

    def distance_to(self, other: "Node") -> float:
        """Golden-ratio distance metric."""
        ring_diff = abs(self.ring - other.ring)
        pos_diff = abs(self.position - other.position)
        return ring_diff + (pos_diff / PHI)


@dataclass
class FibonacciRing:
    """A single Fibonacci ring in the topology."""
    ring_num: int
    nodes: Dict[str, Node] = field(default_factory=dict)
    size: int = 0

    def __post_init__(self):
        self.size = FIBONACCI[self.ring_num] if self.ring_num < len(FIBONACCI) else 144

    def add_node(self, node: Node) -> bool:
        if node.node_id in self.nodes:
            return False
        if node.ring != self.ring_num:
            return False
        self.nodes[node.node_id] = node
        return True

    def get_nodes_by_position(self, position: int) -> List[Node]:
        """Get all nodes at a specific position in ring."""
        return [n for n in self.nodes.values() if n.position == position]

    def ring_neighbors(self, node_id: str) -> List[str]:
        """Get neighbors within the ring (adjacency in ring)."""
        node = self.nodes.get(node_id)
        if not node:
            return []
        neighbors = []
        pos = node.position
        for candidate in self.nodes.values():
            if candidate.node_id == node_id:
                continue
            if abs(candidate.position - pos) <= 1 or (pos == 0 and candidate.position == self.size - 1):
                neighbors.append(candidate.node_id)
        return neighbors


class Ring12Topology:
    """12-ring Fibonacci topology for Sovereign Node Mesh."""

    def __init__(self):
        self.rings: Dict[int, FibonacciRing] = {}
        self.all_nodes: Dict[str, Node] = {}
        self.root_node: Optional[str] = None

        # Initialize empty rings
        for i in range(RINGS):
            self.rings[i] = FibonacciRing(i)

    def add_node(self, node_id: str, ring: int, position: int,
                coherence: float = 1.0) -> bool:
        """Add node to topology at specified ring and position."""
        if node_id in self.all_nodes:
            return False
        if ring < 0 or ring >= RINGS:
            return False

        node = Node(node_id=node_id, ring=ring, position=position, coherence=coherence)
        self.all_nodes[node_id] = node
        return self.rings[ring].add_node(node)

    def set_root(self, node_id: str) -> bool:
        """Set root node (typically Uluru-adjacent coordinate)."""
        if node_id not in self.all_nodes:
            return False
        self.root_node = node_id
        return True

    def connect_nodes(self, node_id_a: str, node_id_b: str) -> bool:
        """Create bidirectional edge between two nodes."""
        node_a = self.all_nodes.get(node_id_a)
        node_b = self.all_nodes.get(node_id_b)
        if not node_a or not node_b:
            return False
        node_a.neighbors.add(node_id_b)
        node_b.neighbors.add(node_id_a)
        return True

    def shortest_path(self, from_node: str, to_node: str) -> List[str]:
        """BFS shortest path using golden-ratio distance."""
        if from_node not in self.all_nodes or to_node not in self.all_nodes:
            return []
        if from_node == to_node:
            return [from_node]

        visited = {from_node}
        queue = [(from_node, [from_node])]

        while queue:
            current, path = queue.pop(0)
            if current == to_node:
                return path

            current_node = self.all_nodes[current]
            for neighbor_id in current_node.neighbors:
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, path + [neighbor_id]))

        return []

    def get_ring_nodes(self, ring: int) -> List[Node]:
        """Get all nodes in a specific ring."""
        return list(self.rings[ring].nodes.values())

    def get_all_nodes(self) -> List[Node]:
        """Get all nodes in topology."""
        return list(self.all_nodes.values())

    def network_health(self) -> Dict[str, float]:
        """Compute network health metrics."""
        if not self.all_nodes:
            return {"density": 0.0, "avg_coherence": 0.0, "connectivity": 0.0}

        total_edges = sum(len(n.neighbors) for n in self.all_nodes.values()) / 2
        max_edges = len(self.all_nodes) * (len(self.all_nodes) - 1) / 2
        density = total_edges / max_edges if max_edges > 0 else 0.0

        avg_coherence = sum(n.coherence for n in self.all_nodes.values()) / len(self.all_nodes)

        connected_count = 0
        for node in self.all_nodes.values():
            if self.shortest_path(self.root_node or node.node_id, node.node_id):
                connected_count += 1
        connectivity = connected_count / len(self.all_nodes) if self.all_nodes else 0.0

        return {
            "density": round(density, 3),
            "avg_coherence": round(avg_coherence, 3),
            "connectivity": round(connectivity, 3),
        }


class NodeRouter:
    """Route messages through Fibonacci rings."""

    def __init__(self, topology: Ring12Topology):
        self.topology = topology
        self.routing_table: Dict[Tuple[str, str], List[str]] = {}

    def precompute_routes(self) -> None:
        """Precompute all shortest paths."""
        nodes = self.topology.get_all_nodes()
        for src in nodes:
            for dst in nodes:
                if src.node_id != dst.node_id:
                    path = self.topology.shortest_path(src.node_id, dst.node_id)
                    self.routing_table[(src.node_id, dst.node_id)] = path

    def route(self, from_node: str, to_node: str) -> List[str]:
        """Get route from source to destination."""
        key = (from_node, to_node)
        if key in self.routing_table:
            return self.routing_table[key]
        return self.topology.shortest_path(from_node, to_node)

    def broadcast(self, from_node: str) -> Dict[str, List[str]]:
        """Get routes from one node to all others."""
        routes = {}
        for node in self.topology.get_all_nodes():
            if node.node_id != from_node:
                routes[node.node_id] = self.route(from_node, node.node_id)
        return routes

"""
Lattice Visualization & Graph Utilities
Part of Civilisation.One + CrystalCoreOS integration
Version: v0.1 (Graph Export & Visualization Stub)

Generates graph representations of the lattice for visualization,
audit trails, and debugging.

Supports:
- Mermaid diagram export (for documentation)
- DOT format (Graphviz)
- JSON graph representation
- ASCII art (terminal-friendly)
"""

from typing import Dict, List, Set, Tuple, Optional, Any
from .coordinate import LatticeCoordinate, CoordinateRegistry
from datetime import datetime


class LatticeGraph:
    """
    Represents the lattice as a directed graph.

    Nodes = Coordinates
    Edges = Message flows or logical dependencies
    """

    def __init__(self, registry: CoordinateRegistry):
        """
        Initialize graph from registry.

        Args:
            registry: Populated coordinate registry
        """
        self.registry = registry
        self.edges: List[Tuple[str, str, Dict[str, Any]]] = []

    def add_edge(self, source: LatticeCoordinate, dest: LatticeCoordinate,
                 label: str = "", edge_type: str = "default") -> bool:
        """
        Add a directed edge between two coordinates.

        Args:
            source: Source coordinate
            dest: Destination coordinate
            label: Optional edge label
            edge_type: Type of relationship (default, depends_on, sends_to, etc.)

        Returns:
            True if edge added; False if coordinates not registered
        """
        if (source.full_key() not in self.registry.coordinates or
            dest.full_key() not in self.registry.coordinates):
            return False

        self.edges.append((
            source.full_key(),
            dest.full_key(),
            {"label": label, "type": edge_type}
        ))
        return True

    def get_nodes(self) -> List[LatticeCoordinate]:
        """Get all nodes in the graph."""
        return list(self.registry.coordinates.values())

    def get_edges(self) -> List[Tuple[str, str, Dict[str, Any]]]:
        """Get all edges in the graph."""
        return self.edges.copy()

    def get_incoming_edges(self, coord: LatticeCoordinate) -> List[Tuple[str, Dict[str, Any]]]:
        """Get all edges pointing to a coordinate."""
        dest_key = coord.full_key()
        return [(src, meta) for src, dest, meta in self.edges if dest == dest_key]

    def get_outgoing_edges(self, coord: LatticeCoordinate) -> List[Tuple[str, Dict[str, Any]]]:
        """Get all edges originating from a coordinate."""
        src_key = coord.full_key()
        return [(dest, meta) for src, dest, meta in self.edges if src == src_key]

    def to_mermaid(self) -> str:
        """
        Export graph as Mermaid diagram.

        Returns:
            Mermaid diagram code (can be rendered in markdown or mermaid.live)
        """
        lines = ["graph TD"]

        layer_colors = {
            "Mind": "A1D99B",
            "Memory": "FD8D3C",
            "Flow": "FB6A4A",
            "Evolve": "636363",
            "Lattice": "3182BD",
            "Sensor": "9467BD",
            "Governance": "FF7F0E"
        }

        for coord in self.get_nodes():
            node_id = coord.full_key().replace(":", "_")
            label = f"{coord.agent}<br/>{coord.version}"
            color = layer_colors.get(coord.layer, "CCCCCC")
            lines.append(f'    {node_id}["<b>{label}</b>"]')
            lines.append(f'    style {node_id} fill:#{color},stroke:#333,color:#000')

        for src, dest, meta in self.get_edges():
            src_id = src.replace(":", "_")
            dest_id = dest.replace(":", "_")
            label = meta.get("label", "")
            edge_type = meta.get("type", "default")

            if label:
                lines.append(f'    {src_id} -->|{label}| {dest_id}')
            else:
                lines.append(f'    {src_id} --> {dest_id}')

        return "\n".join(lines)

    def to_dot(self) -> str:
        """
        Export graph as Graphviz DOT format.

        Returns:
            DOT format string (can be rendered with Graphviz)
        """
        lines = ["digraph Lattice {"]
        lines.append('    rankdir=LR;')
        lines.append('    node [shape=box, style=rounded];')

        for coord in self.get_nodes():
            node_id = coord.full_key().replace(":", "_")
            label = f"{coord.agent}\\n{coord.version}\\n({coord.layer})"
            lines.append(f'    {node_id} [label="{label}"];')

        for src, dest, meta in self.get_edges():
            src_id = src.replace(":", "_")
            dest_id = dest.replace(":", "_")
            label = meta.get("label", "")
            if label:
                lines.append(f'    {src_id} -> {dest_id} [label="{label}"];')
            else:
                lines.append(f'    {src_id} -> {dest_id};')

        lines.append("}")
        return "\n".join(lines)

    def to_json(self) -> Dict[str, Any]:
        """
        Export graph as JSON representation.

        Returns:
            Dictionary with nodes and edges
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "nodes": [coord.to_dict() for coord in self.get_nodes()],
            "edges": [
                {
                    "source": src,
                    "destination": dest,
                    "metadata": meta
                }
                for src, dest, meta in self.get_edges()
            ],
            "statistics": {
                "total_nodes": len(self.get_nodes()),
                "total_edges": len(self.edges),
                "layers": list(self.registry.by_layer.keys())
            }
        }

    def to_ascii_tree(self, root: Optional[LatticeCoordinate] = None) -> str:
        """
        Export graph as ASCII tree (terminal-friendly).

        Args:
            root: Starting coordinate (uses first if None)

        Returns:
            ASCII art tree representation
        """
        nodes = self.get_nodes()
        if not nodes:
            return "(empty graph)"

        if root is None:
            root = nodes[0]

        lines = []
        visited: Set[str] = set()

        def add_branch(coord: LatticeCoordinate, prefix: str = "", is_last: bool = True):
            coord_str = f"{coord.agent} [{coord.version}]"
            lines.append(prefix + ("└── " if is_last else "├── ") + coord_str)

            visited.add(coord.full_key())

            outgoing = self.get_outgoing_edges(coord)
            for dest_key, meta in outgoing:
                dest = self.registry.lookup(dest_key)
                if dest and dest.full_key() not in visited:
                    extension = "    " if is_last else "│   "
                    add_branch(dest, prefix + extension, dest_key == outgoing[-1][0])

        lines.append(f"Lattice [{root.layer}]")
        add_branch(root, "")
        return "\n".join(lines)


class LayerVisualizer:
    """Generate visualizations focused on layers."""

    @staticmethod
    def layer_summary(registry: CoordinateRegistry) -> str:
        """
        Generate a summary of components by layer.

        Args:
            registry: Coordinate registry

        Returns:
            Formatted summary string
        """
        lines = ["LATTICE LAYER SUMMARY", "=" * 40]

        for layer in sorted(registry.by_layer.keys()):
            coords = registry.list_layer(layer)
            lines.append(f"\n{layer} ({len(coords)} components):")
            for coord in coords:
                lines.append(f"  • {coord.agent} [{coord.version}]")

        return "\n".join(lines)

    @staticmethod
    def agent_network(registry: CoordinateRegistry) -> str:
        """
        Generate a network diagram of agents.

        Args:
            registry: Coordinate registry

        Returns:
            ASCII network diagram
        """
        lines = ["AGENT NETWORK", "=" * 40]

        by_layer = {}
        for coord in registry.coordinates.values():
            if coord.layer not in by_layer:
                by_layer[coord.layer] = []
            by_layer[coord.layer].append(coord)

        for layer in sorted(by_layer.keys()):
            coords = by_layer[layer]
            lines.append(f"\n[{layer}]")
            for i, coord in enumerate(coords):
                prefix = "└─" if i == len(coords) - 1 else "├─"
                lines.append(f"{prefix} {coord.agent:20} v{coord.version}")

        return "\n".join(lines)


class ConformanceVisualizer:
    """Generate conformance and evidence status visualizations."""

    @staticmethod
    def evidence_status_grid(registry: CoordinateRegistry,
                             evidence_state_map: Dict[str, str]) -> str:
        """
        Generate a grid showing evidence status of all components.

        Args:
            registry: Coordinate registry
            evidence_state_map: Mapping from full_key to evidence state

        Returns:
            Formatted status grid
        """
        lines = ["EVIDENCE STATUS", "=" * 60]
        lines.append(f"{'Component':<40} {'State':<15}")
        lines.append("-" * 60)

        for full_key, coord in registry.coordinates.items():
            state = evidence_state_map.get(full_key, "UNKNOWN")
            label = f"{coord.agent} [{coord.version}]"
            lines.append(f"{label:<40} {state:<15}")

        return "\n".join(lines)


class ComplianceReport:
    """Generate comprehensive compliance and audit reports."""

    @staticmethod
    def full_report(registry: CoordinateRegistry, graph: Optional[LatticeGraph] = None,
                   evidence_map: Optional[Dict[str, str]] = None) -> str:
        """
        Generate a comprehensive lattice compliance report.

        Args:
            registry: Coordinate registry
            graph: Optional graph for topology analysis
            evidence_map: Optional evidence status map

        Returns:
            Formatted report
        """
        report = []
        report.append("=" * 70)
        report.append("INCOGNITA LATTICE CONFORMANCE REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.utcnow().isoformat()}")

        report.append("\nSUMMARY STATISTICS")
        report.append("-" * 70)
        report.append(f"Total Coordinates: {len(registry.coordinates)}")
        report.append(f"Total Layers: {len(registry.by_layer)}")
        report.append(f"Total Agents: {len(registry.by_agent)}")

        report.append("\nLAYER BREAKDOWN")
        report.append("-" * 70)
        for layer in sorted(registry.by_layer.keys()):
            count = len(registry.list_layer(layer))
            report.append(f"{layer:<20} {count:>3} components")

        if evidence_map:
            report.append("\nEVIDENCE STATUS")
            report.append("-" * 70)
            status_counts = {}
            for state in evidence_map.values():
                status_counts[state] = status_counts.get(state, 0) + 1
            for state, count in sorted(status_counts.items()):
                report.append(f"{state:<20} {count:>3} components")

        if graph:
            report.append("\nTOPOLOGY")
            report.append("-" * 70)
            report.append(f"Edges: {len(graph.get_edges())}")

        report.append("\n" + "=" * 70)
        return "\n".join(report)


def format_coordinate_table(coords: List[LatticeCoordinate]) -> str:
    """Format a list of coordinates as a table."""
    lines = ["┌─────────────────────────────────────────────────────────────┐"]
    lines.append("│ Coordinate                                  │ Hash             │")
    lines.append("├─────────────────────────────────────────────────────────────┤")

    for coord in coords:
        coord_str = str(coord)[:40].ljust(40)
        hash_str = coord.compute_hash()[:15]
        lines.append(f"│ {coord_str} │ {hash_str} │")

    lines.append("└─────────────────────────────────────────────────────────────┘")
    return "\n".join(lines)

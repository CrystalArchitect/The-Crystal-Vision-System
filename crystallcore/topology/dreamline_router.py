#!/usr/bin/env python3
"""
Dreamline Router — Narrative Propagation on Fibonacci Rings
Phase 3: Songlines → Starlines Transformation

Dreamlines are narrative/story pathways that propagate through the Fibonacci
ring topology. Based on Indigenous Songline tradition, Dreamlines encode:
- Cultural knowledge & ceremony
- Navigation & memory
- Frequency resonance (χ-1144 base)

Maps Songlines (terrestrial, cultural) to Starlines (orbital, future).
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class NarrativeType(Enum):
    """Types of narrative propagation."""
    SONGLINE = "songline"          # Traditional/terrestrial
    STARLINE = "starline"          # Orbital/future
    DREAMLINE = "dreamline"        # Unified narrative
    HEALING = "healing"            # Restorative/χ-1144-SWL
    MOMENTUM = "momentum"          # Forward thrust/χ-1148-SG


@dataclass
class Narrative:
    """A narrative artifact for propagation."""
    narrative_id: str
    narrative_type: NarrativeType
    content: str
    origin_node: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    frequency: int = 1144  # χ frequency
    coherence: float = 1.0
    sacred_markers: List[str] = field(default_factory=list)  # Cultural/ceremonial markers
    metadata: Dict = field(default_factory=dict)

    def is_valid(self) -> bool:
        return self.content and self.origin_node and self.coherence > 0.0


@dataclass
class PropagationPath:
    """Path of narrative propagation through Fibonacci rings."""
    narrative_id: str
    path: List[str]  # Sequence of node IDs
    propagation_time: float = 0.0
    nodes_reached: Set[str] = field(default_factory=set)
    coherence_drop: float = 0.0  # Coherence loss along path


class DreamlineRouter:
    """Route narratives through Fibonacci topology."""

    def __init__(self):
        self.narratives: Dict[str, Narrative] = {}
        self.paths: Dict[str, PropagationPath] = {}
        self.received_narratives: Dict[str, Set[str]] = {}  # node -> narrative_ids received
        self.frequency_map: Dict[int, List[str]] = {}  # frequency -> narrative_ids

    def register_narrative(self, narrative: Narrative) -> bool:
        """Register a narrative for propagation."""
        if not narrative.is_valid():
            return False
        if narrative.narrative_id in self.narratives:
            return False

        self.narratives[narrative.narrative_id] = narrative
        freq = narrative.frequency
        self.frequency_map.setdefault(freq, []).append(narrative.narrative_id)
        return True

    def propagate(self, narrative_id: str, topology_path: List[str]) -> Optional[PropagationPath]:
        """Propagate narrative along a path in Fibonacci rings."""
        if narrative_id not in self.narratives:
            return None

        narrative = self.narratives[narrative_id]
        path = PropagationPath(
            narrative_id=narrative_id,
            path=topology_path,
            nodes_reached=set(topology_path)
        )

        # Simulate coherence loss along path
        loss_per_hop = 0.02  # 2% loss per hop
        path.coherence_drop = len(topology_path) * loss_per_hop
        final_coherence = max(0.0, narrative.coherence - path.coherence_drop)

        # Record reception
        for node in topology_path:
            self.received_narratives.setdefault(node, set()).add(narrative_id)

        self.paths[narrative_id] = path
        return path

    def transform_songline_to_starline(self, songline_id: str) -> Optional[str]:
        """Transform terrestrial Songline into orbital Starline."""
        if songline_id not in self.narratives:
            return None

        songline = self.narratives[songline_id]
        if songline.narrative_type != NarrativeType.SONGLINE:
            return None

        # Create Starline with same content but different frequency/type
        starline = Narrative(
            narrative_id=f"starline_{songline_id}",
            narrative_type=NarrativeType.STARLINE,
            content=songline.content,
            origin_node=songline.origin_node,
            frequency=songline.frequency,
            coherence=songline.coherence * 0.95,  # Slight loss in transformation
            sacred_markers=songline.sacred_markers,
            metadata=songline.metadata.copy()
        )

        self.register_narrative(starline)
        return starline.narrative_id

    def get_narratives_at_frequency(self, frequency: int) -> List[Narrative]:
        """Get all narratives resonating at a specific frequency."""
        narrative_ids = self.frequency_map.get(frequency, [])
        return [self.narratives[nid] for nid in narrative_ids if nid in self.narratives]

    def get_received_by_node(self, node_id: str) -> List[Narrative]:
        """Get all narratives received at a node."""
        narrative_ids = self.received_narratives.get(node_id, set())
        return [self.narratives[nid] for nid in narrative_ids if nid in self.narratives]

    def resonance_cascade(self, origin_frequency: int) -> Dict[int, int]:
        """Compute harmonic resonance cascade from a frequency."""
        cascade = {}
        current_freq = origin_frequency

        for harmonic in range(1, 13):  # 12 harmonics
            harmonic_freq = int(current_freq * (1 + harmonic * 0.05))
            count = len(self.get_narratives_at_frequency(harmonic_freq))
            cascade[harmonic_freq] = count

        return cascade

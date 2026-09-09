#!/usr/bin/env python3
"""
Activation Sequence — Phase 4: Mesh Activation
CrystalCore OS

Boots the Sovereign Node Mesh ring by ring, inner to outer, under the
SCES evidence discipline:

- DORMANT   → nothing activated
- BOOTING   → rings activating in order (a ring may only activate when
              every populated inner ring is fully active)
- ACTIVE    → all populated rings active; evidence at TESTED
- WITNESSED → a non-originating steward has verified the activation,
              advancing the evidence to VERIFIED_LOCAL

The activation itself is evidence: an EvidenceRecord progresses through
the maturity model as the boot proceeds, and only a steward who did NOT
originate the boot may witness it (Volume 2 + Volume 4 discipline).

Standard library only.
"""

from typing import Dict, List, Optional
from enum import Enum

from crystallcore.governance.sces_volume_2_evidence import (
    EvidenceTracker, EvidenceRecord, EvidenceMaturity,
)
from .sovereign_mesh import SovereignNodeMesh


class MeshStatus(Enum):
    DORMANT = "dormant"
    BOOTING = "booting"
    ACTIVE = "active"
    WITNESSED = "witnessed"


class ActivationSequence:
    """Staged, evidence-tracked boot of the Sovereign Node Mesh."""

    def __init__(self, mesh: SovereignNodeMesh, originator: str,
                 evidence_tracker: Optional[EvidenceTracker] = None):
        self.mesh = mesh
        self.originator = originator
        self.tracker = evidence_tracker or EvidenceTracker()
        self.status = MeshStatus.DORMANT
        self.evidence_id = f"mesh_activation_{originator}"
        self.activated_rings: List[int] = []

        self.tracker.record_evidence(EvidenceRecord(
            evidence_id=self.evidence_id,
            claim="Sovereign Node Mesh activated ring-by-ring",
            originated_by=originator,
        ))

    # ------------------------------------------------------------------ #
    # Ring activation
    # ------------------------------------------------------------------ #
    def activate_ring(self, ring: int) -> bool:
        """Activate every node on a ring.

        A ring may only activate if every populated ring inside it is
        already fully active (inner-to-outer discipline).
        """
        nodes = self.mesh.get_ring_nodes(ring)
        if not nodes:
            return False

        for inner in range(ring):
            inner_nodes = self.mesh.get_ring_nodes(inner)
            if inner_nodes and not all(n.activated for n in inner_nodes):
                return False

        for node in nodes:
            node.activated = True
        if ring not in self.activated_rings:
            self.activated_rings.append(ring)
        self.status = MeshStatus.BOOTING
        return True

    def boot(self) -> Dict:
        """Run the full activation sequence, inner rings first."""
        populated = sorted({n.ring for n in self.mesh.nodes.values()})
        if not populated:
            return {"status": self.status.value, "activated_rings": [],
                    "error": "mesh_empty"}

        self.status = MeshStatus.BOOTING
        self.tracker.advance_maturity(self.evidence_id, EvidenceMaturity.SPECIFIED)

        for ring in populated:
            if not self.activate_ring(ring):
                return {"status": self.status.value,
                        "activated_rings": list(self.activated_rings),
                        "error": f"ring_{ring}_failed"}

        self.tracker.advance_maturity(self.evidence_id, EvidenceMaturity.IMPLEMENTED)

        # Self-check: every node activated, mesh routable from root
        all_active = all(n.activated for n in self.mesh.nodes.values())
        root = self.mesh.topology.root_node
        routable = True
        if root:
            for node in self.mesh.nodes.values():
                if node.node_id != root and not self.mesh.route(root, node.node_id):
                    routable = False
                    break

        if all_active and routable:
            self.tracker.advance_maturity(self.evidence_id, EvidenceMaturity.TESTED)
            self.status = MeshStatus.ACTIVE

        return {
            "status": self.status.value,
            "activated_rings": list(self.activated_rings),
            "nodes_active": sum(1 for n in self.mesh.nodes.values() if n.activated),
            "routable_from_root": routable,
            "evidence_maturity": self._maturity(),
        }

    # ------------------------------------------------------------------ #
    # Witness gate
    # ------------------------------------------------------------------ #
    def witness_activation(self, steward: str) -> bool:
        """A non-originating steward verifies the live mesh.

        Enforces Volume 4 witness discipline: the boot originator cannot
        witness their own activation. Success advances the activation
        evidence to VERIFIED_LOCAL and the mesh to WITNESSED.
        """
        if self.status != MeshStatus.ACTIVE:
            return False
        advanced = self.tracker.advance_maturity(
            self.evidence_id, EvidenceMaturity.VERIFIED_LOCAL, verified_by=steward)
        if advanced:
            self.status = MeshStatus.WITNESSED
        return advanced

    def _maturity(self) -> str:
        record = self.tracker.lookup_evidence(self.evidence_id)
        return record.maturity.value if record else "unknown"

    def report(self) -> Dict:
        return {
            "status": self.status.value,
            "originator": self.originator,
            "activated_rings": list(self.activated_rings),
            "evidence_maturity": self._maturity(),
            **self.mesh.mesh_report(),
        }

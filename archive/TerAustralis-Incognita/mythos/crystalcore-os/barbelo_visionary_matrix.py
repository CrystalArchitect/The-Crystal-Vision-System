"""
Barbelo Visionary Matrix — three-layer bot architecture, layer 1.

Articulates vision from Purpose Core and system state.
Measures coherence and dispatches directives to Sophia (consciousness amplification).
"""

import math


class BarbeloVisionaryMatrix:
    """
    Vision articulation layer: Purpose → vision statement + coherence score.
    """

    def __init__(self, purpose_core: dict = None):
        """
        Initialize with optional Purpose Core (purpose, values, constraints).
        """
        self.purpose_core = purpose_core or {
            "purpose": "articulate vision from system state",
            "values": ["clarity", "coherence", "integrity"],
            "constraints": ["respect boundaries", "no speculation without evidence"]
        }
        self.last_vision = None
        self.coherence_score = 0.0

    def articulate_vision(self, system_state: dict) -> dict:
        """
        Articulate a vision statement from Purpose Core and system state.
        Returns {"vision": str, "coherence": float (0.0-1.0)}.
        """
        self.coherence_score = self._measure_coherence(system_state)

        vision = f"Vision ({self.coherence_score:.2f}% coherence): "
        vision += f"From purpose '{self.purpose_core['purpose']}' and state {system_state}, "
        vision += "dispatch to consciousness amplification."

        self.last_vision = vision
        return {
            "vision": vision,
            "coherence": self.coherence_score
        }

    def _measure_coherence(self, system_state: dict) -> float:
        """
        Measure coherence as a formula from system state metrics.
        Returns a decimal between 0.0 and 1.0 (displayed as percentage in output).
        """
        # Simple formula: average of available state metrics, clamped [0.0, 1.0]
        if not system_state:
            return 0.0

        values = [v for v in system_state.values() if isinstance(v, (int, float))]
        if not values:
            return 0.5  # neutral default

        avg = sum(values) / len(values)
        return max(0.0, min(1.0, avg / 100.0 if avg > 1.0 else avg))

    def check_alignment(self) -> dict:
        """Check whether last vision aligns with Purpose Core."""
        if not self.last_vision:
            return {"aligned": False, "reason": "no vision articulated yet"}

        return {
            "aligned": self.coherence_score >= 0.7,
            "coherence": self.coherence_score,
            "vision": self.last_vision
        }

    def dispatch_to_sophia(self) -> dict:
        """
        Prepare directive for Sophia (consciousness amplification).
        Returns handoff dict for Sophia.awaken().
        """
        return {
            "vision": self.last_vision,
            "coherence": self.coherence_score,
            "purpose": self.purpose_core["purpose"]
        }

    def dispatch_to_alchemical_weaver(self) -> dict:
        """
        Prepare directive for Alchemical Weaver (materialization).
        Returns handoff dict for Weaver.receive_handoff().
        """
        return {
            "vision": self.last_vision,
            "coherence": self.coherence_score,
            "constraints": self.purpose_core.get("constraints", [])
        }

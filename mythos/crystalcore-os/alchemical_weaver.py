"""
Alchemical Weaver — three-layer bot architecture, layer 3.

Materializes vision + consciousness into executable subsystems.
Calculates balance from fire intensity vs. water constraints.
Registers and executes subsystems, reports on manifest state.
"""


class AlchemicalWeaver:
    """
    Materialization layer: fire + constraints → subsystems, balance, manifest state.
    """

    def __init__(self):
        """Initialize Weaver with empty handoff and subsystem registry."""
        self.handoff = None
        self.balance_factor = 0.0
        self.fire_intensity = 0.0
        self.water_constraints = 0.0
        self.subsystems = {}
        self.manifest = None

    def receive_handoff(self, handoff: dict):
        """Receive fire + constraints handoff from Sophia and Barbelo."""
        self.handoff = handoff
        self.fire_intensity = handoff.get("fire", 0.0)
        # water_constraints derived from coherence penalty
        self.water_constraints = 1.0 - handoff.get("coherence", 0.5)
        return {"status": "handoff received", "fire": self.fire_intensity}

    def calculate_balance(self) -> float:
        """
        Calculate balance factor from fire vs. water constraints.
        Balance = fire / (fire + water), clamped [0.0, 1.0].
        Returns a decimal between 0.0 and 1.0.
        """
        denominator = self.fire_intensity + self.water_constraints
        if denominator == 0.0:
            return 0.5
        self.balance_factor = self.fire_intensity / denominator
        return max(0.0, min(1.0, self.balance_factor))

    def forge(self) -> dict:
        """
        Forge: execute materialization from balance + subsystems.
        Returns {"manifest": dict, "balance": float, "subsystems": dict}.
        """
        balance = self.calculate_balance()

        self.manifest = {
            "balance": balance,
            "fire": self.fire_intensity,
            "constraints": self.water_constraints,
            "subsystems_count": len(self.subsystems),
            "state": "materialized" if balance > 0.4 else "pending"
        }

        return {
            "manifest": self.manifest,
            "balance": balance,
            "subsystems": self.subsystems
        }

    def register_subsystem(self, name: str, subsystem: dict) -> dict:
        """Register a subsystem for execution."""
        self.subsystems[name] = subsystem
        return {"status": "registered", "name": name, "total": len(self.subsystems)}

    def report(self) -> dict:
        """Report final manifest state: balance, subsystems, material execution."""
        if not self.manifest:
            self.forge()

        return {
            "manifest": self.manifest,
            "balance": self.balance_factor,
            "subsystems_registered": len(self.subsystems),
            "ready_to_execute": self.manifest.get("state") == "materialized"
        }

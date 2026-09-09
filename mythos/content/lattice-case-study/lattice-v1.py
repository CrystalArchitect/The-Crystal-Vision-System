# Round 1 (v1) — delivered by Grok in the maintainer's session, 2026-08-08.
# Parity-bit integrity, three-site chain. Class code verbatim as delivered.
# The demonstration section is instrumented from the delivered original so
# silent non-events print: a result print on the integrity check, and
# parenthesised trace lines where a hop or correction did not proceed.
# Grok's original demonstration, with its claim comments, is quoted in
# ../QUANTUM-LATTICE-CASE-STUDY.md. Output is deterministic.

class Site:
    def __init__(self, name):
        self.name = name
        self.occupation = None
        self.U = 1.0
        self.neighbours = []
        self.parity_bit = 0

    def __repr__(self):
        return f"{self.name}[occ={self.occupation}, U={self.U}, parity={self.parity_bit}]"

class QuantumLattice1D:
    def __init__(self):
        self.site1 = Site("Input")
        self.site2 = Site("Holding")
        self.site3 = Site("Output")
        self.site1.neighbours = [self.site2]
        self.site2.neighbours = [self.site1, self.site3]
        self.site3.neighbours = [self.site2]
        self.t = 0.3
        self.error_log = []

    def load(self, site, state):
        site.occupation = state
        site.parity_bit = self._calc_parity(state)
        print(f"Loaded '{state}' onto {site.name} (parity={site.parity_bit})")

    def set_localisation(self, site, strength):
        site.U = strength
        print(f"{site.name} localisation strength set to {strength}")

    def _calc_parity(self, state):
        if state is None:
            return 0
        return len(str(state)) % 2

    def check_integrity(self, site):
        if site.occupation is None:
            return True
        expected = self._calc_parity(site.occupation)
        if site.parity_bit != expected:
            self.error_log.append(f"Integrity fail on {site.name}")
            return False
        return True

    def can_tunnel(self, source, target):
        if source.occupation is None:
            return False
        if not self.check_integrity(source):
            print(f"Tunnel blocked: integrity error on {source.name}")
            return False
        effective_t = self.t / (1 + source.U)
        return effective_t > 0.15

    def attempt_hop(self, source, target):
        if not self.can_tunnel(source, target):
            print(f"(hop from {source.name} did not proceed)")
            return False
        if target.occupation is not None:
            print(f"Hop blocked: {target.name} already occupied")
            return False
        target.occupation = source.occupation
        target.parity_bit = self._calc_parity(target.occupation)
        source.occupation = None
        source.parity_bit = 0
        print(f"Hopped '{target.occupation}' from {source.name} -> {target.name}")
        return True

    def correct_error(self, site, trusted_value=None):
        if not self.check_integrity(site):
            print(f"Error detected on {site.name}")
            if trusted_value is not None:
                site.occupation = trusted_value
                site.parity_bit = self._calc_parity(trusted_value)
                print(f"Corrected {site.name} to trusted value '{trusted_value}'")
            else:
                site.occupation = None
                site.parity_bit = 0
                print(f"Cleared {site.name} (safe correction)")
            return True
        print(f"(no error detected on {site.name} — correction not triggered)")
        return False

    def release(self, site):
        site.occupation = None
        site.U = 1.0
        site.parity_bit = 0
        print(f"{site.name} released to neutral")

lattice = QuantumLattice1D()
lattice.load(lattice.site2, "sensitive_decision_v1")
lattice.set_localisation(lattice.site2, 8.0)
print("\n--- Simulating corruption ---")
lattice.site2.occupation = "sensitive_decision_v1_CORRUPTED"
print("integrity check result:", lattice.check_integrity(lattice.site2))
lattice.attempt_hop(lattice.site2, lattice.site3)
lattice.correct_error(lattice.site2, trusted_value="sensitive_decision_v1")
lattice.set_localisation(lattice.site2, 1.0)
lattice.attempt_hop(lattice.site2, lattice.site3)
lattice.release(lattice.site2)
print("\nError log:", lattice.error_log)
print(lattice.site1); print(lattice.site2); print(lattice.site3)

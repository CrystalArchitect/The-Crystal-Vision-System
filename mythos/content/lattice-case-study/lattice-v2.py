# Round 2 (v2) — delivered by Grok in the maintainer's session, 2026-08-08.
# SHA-256 content hash + shadow copy replace the parity bit. Class code
# verbatim as delivered. The demonstration section is instrumented from the
# delivered original: hop return values are captured and printed in one
# bracketed line. Grok's original demonstration, with its claim comments,
# is quoted in ../QUANTUM-LATTICE-CASE-STUDY.md. Output is deterministic.

import hashlib

class Site:
    def __init__(self, name):
        self.name = name
        self.occupation = None
        self.U = 1.0
        self.neighbours = []
        self.content_hash = None
        self.shadow = None

    def __repr__(self):
        return f"{self.name}[occ={self.occupation}, U={self.U}, hash={self.content_hash}]"

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

    def _hash(self, value):
        if value is None:
            return None
        return hashlib.sha256(str(value).encode()).hexdigest()[:12]

    def load(self, site, state):
        site.occupation = state
        site.content_hash = self._hash(state)
        site.shadow = state
        print(f"Loaded '{state}' onto {site.name} (hash={site.content_hash})")

    def set_localisation(self, site, strength):
        site.U = strength
        print(f"{site.name} localisation strength set to {strength}")

    def check_integrity(self, site):
        if site.occupation is None:
            return site.content_hash is None
        current = self._hash(site.occupation)
        if current != site.content_hash:
            self.error_log.append(f"Integrity fail on {site.name}: expected {site.content_hash}, got {current}")
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
            return False
        if target.occupation is not None:
            print(f"Hop blocked: {target.name} already occupied")
            return False
        target.occupation = source.occupation
        target.content_hash = source.content_hash
        target.shadow = source.shadow
        source.occupation = None
        source.content_hash = None
        source.shadow = None
        print(f"Hopped '{target.occupation}' from {source.name} -> {target.name}")
        return True

    def correct_error(self, site, trusted_value=None):
        if self.check_integrity(site):
            return False
        print(f"Error detected on {site.name}")
        if trusted_value is not None:
            site.occupation = trusted_value
            site.content_hash = self._hash(trusted_value)
            site.shadow = trusted_value
            print(f"Corrected {site.name} from trusted value")
            return True
        if site.shadow is not None:
            site.occupation = site.shadow
            site.content_hash = self._hash(site.shadow)
            print(f"Corrected {site.name} from shadow copy")
            return True
        site.occupation = None
        site.content_hash = None
        site.shadow = None
        print(f"Cleared {site.name} (no recoverable copy)")
        return True

    def release(self, site):
        site.occupation = None
        site.U = 1.0
        site.content_hash = None
        site.shadow = None
        print(f"{site.name} released to neutral")

lattice = QuantumLattice1D()
lattice.load(lattice.site2, "sensitive_decision_v1")
lattice.set_localisation(lattice.site2, 8.0)
print("\n--- Simulating corruption ---")
lattice.site2.occupation = "sensitive_decision_v1_CORRUPTED"
lattice.check_integrity(lattice.site2)
r1 = lattice.attempt_hop(lattice.site2, lattice.site3)
lattice.correct_error(lattice.site2)
lattice.set_localisation(lattice.site2, 1.0)
r2 = lattice.attempt_hop(lattice.site2, lattice.site3)
lattice.release(lattice.site2)
print(f"\n[verbatim run — hop results: blocked_hop={r1}, 'clean' final hop={r2}]")
print("Error log:", lattice.error_log)
print(lattice.site1); print(lattice.site2); print(lattice.site3)

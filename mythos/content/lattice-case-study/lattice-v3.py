# Round 3 (v3) — delivered by Grok in the maintainer's session, 2026-08-08.
# Adds non-local (Majorana-inspired) pair encoding. Class code verbatim as
# delivered, plus one added trace line in attempt_hop (the parenthesised
# "did not proceed" print) so a silently refused hop is visible. The
# delivered demonstration carried three claim comments — "# should block",
# "# recover from shadow", "# now succeeds" — quoted and tested in
# ../QUANTUM-LATTICE-CASE-STUDY.md. Output is deterministic.

import hashlib
from typing import Optional, List, Dict

class Site:
    def __init__(self, name: str):
        self.name = name
        self.occupation: Optional[str] = None
        self.U: float = 1.0
        self.neighbours: List["Site"] = []
        self.content_hash: Optional[str] = None
        self.shadow: Optional[str] = None
        self.pair_partner: Optional["Site"] = None
        self.is_logical_half: bool = False

    def __repr__(self):
        partner = self.pair_partner.name if self.pair_partner else None
        return (f"{self.name}[occ={self.occupation}, U={self.U}, "
                f"hash={self.content_hash}, partner={partner}]")

class QuantumLattice:
    def __init__(self, site_names: List[str] = None):
        if site_names is None:
            site_names = ["Input", "Holding", "Output", "Reserve"]
        self.sites: Dict[str, Site] = {name: Site(name) for name in site_names}
        self._wire_linear()
        self.t: float = 0.3
        self.error_log: List[str] = []

    def _wire_linear(self):
        names = list(self.sites.keys())
        for i, name in enumerate(names):
            site = self.sites[name]
            if i > 0:
                site.neighbours.append(self.sites[names[i-1]])
            if i < len(names) - 1:
                site.neighbours.append(self.sites[names[i+1]])

    def _hash(self, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return hashlib.sha256(str(value).encode()).hexdigest()[:12]

    def check_integrity(self, site: Site) -> bool:
        if site.occupation is None:
            return site.content_hash is None
        current = self._hash(site.occupation)
        if current != site.content_hash:
            self.error_log.append(f"Integrity fail on {site.name}: expected {site.content_hash}, got {current}")
            return False
        return True

    def load(self, site_name: str, state: str):
        site = self.sites[site_name]
        site.occupation = state
        site.content_hash = self._hash(state)
        site.shadow = state
        site.is_logical_half = False
        site.pair_partner = None
        print(f"Loaded '{state}' onto {site.name} (hash={site.content_hash})")

    def set_localisation(self, site_name: str, strength: float):
        site = self.sites[site_name]
        site.U = strength
        print(f"{site.name} localisation set to {strength}")

    def encode_nonlocal(self, site_a_name: str, site_b_name: str, logical_state: str):
        a = self.sites[site_a_name]
        b = self.sites[site_b_name]
        a.occupation = f"HALF_A:{logical_state}"
        b.occupation = f"HALF_B:{logical_state}"
        a.content_hash = self._hash(a.occupation)
        b.content_hash = self._hash(b.occupation)
        a.shadow = a.occupation
        b.shadow = b.occupation
        a.pair_partner = b
        b.pair_partner = a
        a.is_logical_half = True
        b.is_logical_half = True
        print(f"Non-local encoding of '{logical_state}' across {a.name} <-> {b.name}")

    def read_nonlocal(self, site_a_name: str) -> Optional[str]:
        a = self.sites[site_a_name]
        if not a.is_logical_half or a.pair_partner is None:
            print("Not a non-local pair")
            return None
        b = a.pair_partner
        if not (self.check_integrity(a) and self.check_integrity(b)):
            print("Non-local read failed: integrity error on one or both halves")
            return None
        logical = a.occupation.replace("HALF_A:", "")
        print(f"Non-local read successful: '{logical}'")
        return logical

    def can_tunnel(self, source: Site, target: Site) -> bool:
        if source.occupation is None:
            return False
        if source.is_logical_half:
            print(f"Tunnel blocked: {source.name} is part of a non-local pair")
            return False
        if not self.check_integrity(source):
            print(f"Tunnel blocked: integrity error on {source.name}")
            return False
        effective_t = self.t / (1 + source.U)
        return effective_t > 0.15

    def attempt_hop(self, source_name: str, target_name: str) -> bool:
        source = self.sites[source_name]
        target = self.sites[target_name]
        if not self.can_tunnel(source, target):
            print(f"(hop {source_name} -> {target_name} did not proceed)")
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

    def correct_error(self, site_name: str, trusted_value: Optional[str] = None) -> bool:
        site = self.sites[site_name]
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
        if site.pair_partner:
            site.pair_partner.pair_partner = None
            site.pair_partner.is_logical_half = False
            site.pair_partner = None
            site.is_logical_half = False
        print(f"Cleared {site.name} (no recoverable copy)")
        return True

    def release(self, site_name: str):
        site = self.sites[site_name]
        if site.pair_partner:
            partner = site.pair_partner
            partner.pair_partner = None
            partner.is_logical_half = False
        site.occupation = None
        site.U = 1.0
        site.content_hash = None
        site.shadow = None
        site.pair_partner = None
        site.is_logical_half = False
        print(f"{site.name} released to neutral")

    def status(self):
        print("\n=== Lattice Status ===")
        for site in self.sites.values():
            print(site)
        if self.error_log:
            print("Error log:", self.error_log)

if __name__ == "__main__":
    lattice = QuantumLattice()
    print("=== 1. Ordinary local load + isolation ===")
    lattice.load("Holding", "sensitive_decision_v1")
    lattice.set_localisation("Holding", 8.0)
    print("\n=== 2. Simulate corruption & recover ===")
    lattice.sites["Holding"].occupation = "CORRUPTED_DATA"
    lattice.attempt_hop("Holding", "Output")
    lattice.correct_error("Holding")
    lattice.set_localisation("Holding", 1.0)
    lattice.attempt_hop("Holding", "Output")
    print("\n=== 3. Non-local (Majorana-inspired) encoding ===")
    lattice.encode_nonlocal("Input", "Reserve", "logical_state_X")
    lattice.read_nonlocal("Input")
    print("\n=== 4. Attempt to hop a non-local half (should block) ===")
    lattice.attempt_hop("Input", "Holding")
    print("\n=== 5. Final status ===")
    lattice.status()

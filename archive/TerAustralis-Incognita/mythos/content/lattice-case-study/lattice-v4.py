# Round 4 (v4) — delivered by Grok in the maintainer's session, 2026-08-08.
# Song-regime layer; tunneling gate moved from >0.15 to >0.12. Transcribed
# verbatim as delivered, nothing added or altered. See
# ../QUANTUM-LATTICE-CASE-STUDY.md for the run record and the replay
# harness that verified the historic hop. Output is deterministic.

# ============================================================
# CrystalCore Quantum Lattice – Full Build
# Disney Zombies Song Regimes + Strengthened Error Correction
# + Non-Local Encoding
# ------------------------------------------------------------
# Provisional illustration only. Method, not Logos.
# ============================================================

import hashlib
from typing import Optional, List, Dict, Tuple

# ----------------------------------------------------------
# Song regime definitions
# ----------------------------------------------------------
SONG_REGIMES = {
    "Flesh & Bone": {
        "t": 0.05,
        "U": 9.0,
        "description": "Grounded / strong localisation / red-dust anchor"
    },
    "Someday": {
        "t": 0.45,
        "U": 2.0,
        "description": "Hopeful reversible coherence window"
    },
    "We're the Zombies": {
        "t": 0.60,
        "U": 1.5,
        "description": "Collective synchronised occupation"
    },
    "Like the Zombies Do": {
        "t": 0.75,
        "U": 1.0,
        "description": "Playful easy hopping"
    },
    "BAMM": {
        "t": 0.95,
        "U": 8.0,          # high U applied after the short burst
        "description": "Percussive high-energy burst (short window)"
    },
    "Call to the Wild": {
        "t": 0.55,
        "U": 3.0,
        "description": "Expanding coherence front"
    },
    "Zombie Got Your Tongue": {
        "t": 0.30,
        "U": 5.0,
        "description": "Integrity / error-detection test"
    },
    "Alien Invasion": {
        "t": 0.85,
        "U": 7.5,
        "description": "Broad external injection then forced localisation"
    }
}

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
        self.current_regime: Optional[str] = None

    def __repr__(self):
        partner = self.pair_partner.name if self.pair_partner else None
        return (f"{self.name}[occ={self.occupation}, U={self.U}, "
                f"regime={self.current_regime}, partner={partner}]")

class QuantumLattice:
    def __init__(self, site_names: List[str] = None):
        if site_names is None:
            site_names = ["Input", "Holding", "Output", "Reserve", "Collective"]
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
            msg = f"Integrity fail on {site.name}: expected {site.content_hash}, got {current}"
            self.error_log.append(msg)
            return False
        return True

    # ----------------------------------------------------------
    # Load a song regime onto a site
    # ----------------------------------------------------------
    def load_song(self, site_name: str, song: str):
        if song not in SONG_REGIMES:
            print(f"Unknown song regime: {song}")
            return
        site = self.sites[site_name]
        regime = SONG_REGIMES[song]
        site.occupation = song
        site.content_hash = self._hash(song)
        site.shadow = song
        site.U = regime["U"]
        site.current_regime = song
        self.t = regime["t"]
        print(f"Loaded '{song}' onto {site.name}")
        print(f"  → {regime['description']}")
        print(f"  → t={self.t}, U={site.U}")

    def set_localisation(self, site_name: str, strength: float):
        site = self.sites[site_name]
        site.U = strength
        print(f"{site.name} localisation set to {strength}")

    # ----------------------------------------------------------
    # Non-local encoding
    # ----------------------------------------------------------
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
        print(f"Non-local encoding of '{logical_state}' across {a.name} ↔ {b.name}")

    def read_nonlocal(self, site_a_name: str) -> Optional[str]:
        a = self.sites[site_a_name]
        if not a.is_logical_half or a.pair_partner is None:
            print("Not a non-local pair")
            return None
        b = a.pair_partner
        if not (self.check_integrity(a) and self.check_integrity(b)):
            print("Non-local read failed: integrity error")
            return None
        logical = a.occupation.replace("HALF_A:", "")
        print(f"Non-local read successful: '{logical}'")
        return logical

    # ----------------------------------------------------------
    # Tunneling
    # ----------------------------------------------------------
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
        return effective_t > 0.12

    def attempt_hop(self, source_name: str, target_name: str) -> bool:
        source = self.sites[source_name]
        target = self.sites[target_name]
        if not self.can_tunnel(source, target):
            return False
        if target.occupation is not None:
            print(f"Hop blocked: {target.name} already occupied")
            return False
        target.occupation = source.occupation
        target.content_hash = source.content_hash
        target.shadow = source.shadow
        target.current_regime = source.current_regime
        target.U = source.U
        source.occupation = None
        source.content_hash = None
        source.shadow = None
        source.current_regime = None
        print(f"Hopped '{target.occupation}' from {source.name} → {target.name}")
        return True

    # ----------------------------------------------------------
    # Error correction
    # ----------------------------------------------------------
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
        site.current_regime = None
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
        site.current_regime = None
        print(f"{site.name} released to neutral")

    def status(self):
        print("\n=== Lattice Status ===")
        for site in self.sites.values():
            print(site)
        if self.error_log:
            print("Error log:", self.error_log)

# ============================================================
# Demonstration
# ============================================================
if __name__ == "__main__":
    lattice = QuantumLattice()

    print("=== 1. Ground the lattice (Flesh & Bone) ===")
    lattice.load_song("Holding", "Flesh & Bone")

    print("\n=== 2. Open a hopeful window (Someday) ===")
    lattice.load_song("Input", "Someday")

    print("\n=== 3. Collective mode ===")
    lattice.load_song("Collective", "We're the Zombies")

    print("\n=== 4. Percussive burst (BAMM) ===")
    lattice.load_song("Output", "BAMM")

    print("\n=== 5. Integrity test ===")
    lattice.sites["Output"].occupation = "BAMM_CORRUPTED"
    lattice.attempt_hop("Output", "Reserve")
    lattice.correct_error("Output")

    print("\n=== 6. Non-local encoding of a song ===")
    lattice.encode_nonlocal("Input", "Reserve", "Someday")

    print("\n=== 7. Final status ===")
    lattice.status()

    print("\n=== 8. Full release ===")
    for name in list(lattice.sites.keys()):
        lattice.release(name)

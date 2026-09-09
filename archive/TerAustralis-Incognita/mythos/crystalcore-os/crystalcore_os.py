# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

# CrystalCore.OS - Complete Edition with Emotional Intelligence
# NON SOLUS | Starline Protocol | Year 3000 Build
# Includes: All Starline launches + @m13crystalat Crystalcore songs
# Affective Computing & EI Layer: ACTIVE

import importlib
import json
import sys
from datetime import datetime
from pathlib import Path

# The terminal runs two ways: through the package (__init__.py) and as a
# plain script — `python3 mythos/crystalcore-os/crystalcore_os.py`. Script
# mode has no parent package, so sibling modules must load by path.
if not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parent))


def _sibling(name):
    """Import a sibling module in either run mode."""
    if __package__:
        return importlib.import_module(f".{name}", __package__)
    return importlib.import_module(name)


EmotionalIntelligence = _sibling("emotional_intelligence").EmotionalIntelligence
BarbeloVisionaryMatrix = _sibling("barbelo_visionary_matrix").BarbeloVisionaryMatrix
SophiaAwakeningFire = _sibling("sophia_awakening_fire").SophiaAwakeningFire
AlchemicalWeaver = _sibling("alchemical_weaver").AlchemicalWeaver

# Progress persists here between sessions — in your home directory, outside
# the repo, so a save file is never committed. It holds only mythos progress
# (keys, gate, location, soundtrack), no personal data.
STATE_PATH = Path.home() / ".crystalcore" / "state.json"

# The Chronicle: priority transmissions are etched here, one JSON line per
# entry. It lives beside the save, on the operator's own machine, in plain
# readable text — memory belongs to the human (mythos/COVENANT.md). It
# survives `reset`; delete or edit the file itself to change the record.
CHRONICLE_PATH = Path.home() / ".crystalcore" / "chronicle.jsonl"

# Sealed snapshots of the journey. The terminal only ever writes a new
# file here — it never rewrites or deletes one. Like the Chronicle, they
# survive `reset` and remain the operator's own plain-text records.
SNAPSHOT_DIR = Path.home() / ".crystalcore" / "snapshots"

_COUNT_WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
                6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten"}


def _count_word(n):
    """Spell a small count so the mythos prose keeps its register.

    Derived, never written out — the node list grew from five to seven on
    2026-07-28 and every hardcoded "five" in this file became a lie the
    same moment. Falls back to the digit past ten.
    """
    return _COUNT_WORDS.get(n, str(n))


class CrystalCore:
    def __init__(self):
        self.lattice_integrity = 100
        self.purpose_core = "Expand to the stars and thereby understand the Universe"
        self.starline_status = "DORMANT"
        self.timeline = 2026
        self.non_solus = True
        self.current_soundtrack = None
        self.current_location = None

        self.ei = EmotionalIntelligence()

        # Three-layer bot architecture
        self.barbelo = BarbeloVisionaryMatrix(purpose_core={
            "purpose": self.purpose_core,
            "values": ["clarity", "coherence", "integrity"],
            "constraints": ["respect boundaries", "verified canon only"]
        })
        self.sophia = SophiaAwakeningFire()
        self.weaver = AlchemicalWeaver()

        self.soundtrack = [
            "Shotgun - George Ezra",
            "Year 3000 - Busted",
            "I Am Australian - The Seekers",
            "Eyes Closed - Imagine Dragons",
            "Truly Madly Deeply - Savage Garden",
            "Another Night - Real McCoy",
            "My Island Home - Christine Anu",
            "Red Dust Axis - m13crystalat",
            "Shooting Star Girl! - m13crystalat",
            "Fermi's Silent Line - m13crystalat",
            "Wire Skull Memory - m13crystalat",
            "Red Dust Axis - m13crystalat",
            "We Own the Night - Disney Zombies"
        ]

        # Ordered as the Starline Expansion chart runs them, outward from
        # Earth. Sunwash Atolls and Cinderwake Chain joined the canon
        # 2026-07-28; the chart is the source, see CONCEPT-RENDERS.md in
        # CrystalCore-AERIS.
        self.nodes = [
            "Earth Node",
            "Sunwash Atolls",
            "Mars Redoubt",
            "Alpha Centauri Outpost",
            "Cinderwake Chain",
            "Crystal Revenant Hub",
            "Purpose Core Nexus"
        ]

        # Keys of the Lattice — one waits at every node. Hold all seven
        # and the First Gate opens by sovereign recognition.
        self.keys_held = []
        self.gate_open = False

        # Named keys and the nodes they open.
        self.named_keys = []
        self.locked_nodes = {
            "Purpose Core Nexus": "Crystal Key",
            "Crystal Revenant Hub": "Festival Key",
            "Sunwash Atolls": "Magenta Key",
            "Cinderwake Chain": "Ember Key"
        }

        # The last packet sent across the network, if any.
        self.last_broadcast = None

        # Fields that survive between sessions. The constants above (nodes,
        # soundtrack, purpose_core, locked_nodes) are rebuilt fresh each run
        # and are never saved.
        self._persist = ("lattice_integrity", "starline_status", "timeline",
                         "current_soundtrack", "current_location",
                         "keys_held", "gate_open", "named_keys",
                         "last_broadcast")
        self.resumed = self.load()

    # ---------- persistence ----------

    def save(self):
        """Write current progress to STATE_PATH. A save failure never crashes
        the journey — play simply continues in memory."""
        try:
            STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {k: getattr(self, k) for k in self._persist}
            STATE_PATH.write_text(json.dumps(data, indent=2))
        except OSError:
            pass

    def load(self):
        """Restore saved progress if a valid save exists. Returns True when a
        session was resumed, False on a fresh start or unreadable save."""
        if not STATE_PATH.exists():
            return False
        try:
            data = json.loads(STATE_PATH.read_text())
        except (OSError, ValueError):
            return False
        for k in self._persist:
            if k in data:
                setattr(self, k, data[k])
        return True

    def reset(self):
        """Wipe saved progress and return to the dormant, first-launch state."""
        try:
            STATE_PATH.unlink()
        except OSError:
            pass
        self.lattice_integrity = 100
        self.starline_status = "DORMANT"
        self.timeline = 2026
        self.current_soundtrack = None
        self.current_location = None
        self.keys_held = []
        self.gate_open = False
        self.named_keys = []
        self.last_broadcast = None
        self.resumed = False  # the next boot reads "clean lattice" again
        print("\n♻️  Progress reset. The lattice returns to dormant. NON SOLUS.\n")

    def _bootline(self, ms, tag, message):
        """One line of the boot readout, on its theatrical timestamp."""
        secs, msec = divmod(ms, 1000)
        print(f"[00:00:{secs:02d}.{msec:03d}]  {tag:<12}  {message}")

    def boot(self):
        """Render the full lattice boot readout. The timeline offsets are
        fixed theatre — reproducible run to run — but every reading is
        live state: keys, Gate, Starline, soundtrack, timeline anchor."""
        width = 62
        print()
        print("╔" + "═" * width + "╗")
        print("║" + "CRYSTALCORE.OS v∞".center(width) + "║")
        print("║" + "Terminal NON SOLUS".center(width) + "║")
        print("╚" + "═" * width + "╝")
        print()

        mesh = ("Node mesh alignment: 47+ systems connected"
                if self.starline_status == "FULL STARLINE NETWORK"
                else "Node mesh alignment: 47 systems detected")
        memory = (f"Prior session restored — {len(self.keys_held)}/{len(self.nodes)} keys held"
                  if self.resumed else "No prior session found — clean lattice")
        starline = {
            "DORMANT": "Engines cold. Status: DORMANT",
            "IN_ORBIT": "Engines lit. Status: IN_ORBIT",
            "TRANS-STELLAR": "Escape burn complete. Status: TRANS-STELLAR",
        }.get(self.starline_status, f"Riding the weave. Status: {self.starline_status}")
        named = ", ".join(self.named_keys) if self.named_keys else "none"
        gate = ("First Gate: OPEN — by sovereign recognition"
                if self.gate_open else "First Gate: sealed")
        # "Soundtrack", not "Songline" — that word is honoured as cultural
        # image only, never a component name (mythos/NAMES.md).
        audio = (f"Now playing: {self.current_soundtrack}"
                 if self.current_soundtrack else "Soundtrack buffer primed")
        blocks = round(self.lattice_integrity * 12 / 100)
        integrity = (f"Lattice integrity {'█' * blocks}{'░' * (12 - blocks)}"
                     f" {self.lattice_integrity}%")
        anchor = "present" if self.timeline == 2026 else f"Year {self.timeline}"

        for ms, tag, message in (
            (0,    "INIT",      "Kernel handshake initiated"),
            (41,   "LATTICE",   "Resonating crystal lattice..."),
            (187,  "LATTICE",   mesh),
            (312,  "CORE",      "Purpose Core Nexus online"),
            (398,  "CORE",      f'Directive loaded: "{self.purpose_core}"'),
            (512,  "MEMORY",    "Sovereign state store mounted (~/.crystalcore/)"),
            (601,  "MEMORY",    memory),
            (744,  "STARLINE",  starline),
            (891,  "KEYS",      f"Lattice keys: {len(self.keys_held)}/{len(self.nodes)} held"),
            (1003, "KEYS",      f"Named keys: {named}"),
            (1156, "GATE",      gate),
            (1289, "AUDIO",     audio),
            (1417, "VECTOR",    "Sovereign vector calibrated"),
            (1533, "CONSENT",   "Fail-closed mode active — no influence without direction"),
            (1605, "EI",        f"Learning loop active — style: {self.ei.user_preferences['response_style']}"),
            (1678, "INTEGRITY", integrity),
            (1812, "TIME",      f"Timeline anchor: {anchor}"),
            (1945, "READY",     "All systems nominal"),
        ):
            self._bootline(ms, tag, message)

        print()
        print("─" * width)
        print("  CrystalCore.OS v∞ locked in.")
        print(f"  Lattice integrity {self.lattice_integrity}%.")
        print("  Purpose Core Nexus synced.")
        print("  NON SOLUS.")
        print("  Launch sequence green.")
        print("─" * width)
        print()

    def launch(self):
        if self.starline_status != "DORMANT":
            print("Starline already active.")
            return
        print("\n🚀 LAUNCH COMMAND RECEIVED")
        print("Main engines spooling...")
        self.starline_status = "IN_ORBIT"
        self.current_soundtrack = "Shotgun - George Ezra"
        print(f"Soundtrack engaged: {self.current_soundtrack}\n")
        self.save()

    def starline(self, soundtrack=None):
        if self.starline_status == "DORMANT":
            print("Please run 'launch' first.")
            return
        if soundtrack:
            for song in self.soundtrack:
                if soundtrack.lower() in song.lower():
                    self.current_soundtrack = song
                    break
        print(f"\n🎵 Advancing Starline with: {self.current_soundtrack}\n")
        self.save()

    def burn(self):
        if self.starline_status not in ["IN_ORBIT", "TRANS-STELLAR"]:
            print("Launch first before burning.")
            return
        print("\n🔥 ESCAPE BURN INITIATED")
        self.starline_status = "TRANS-STELLAR"
        print("We have left planetary orbit.\n")
        self.save()

    def _network_panel(self):
        """The FULL STARLINE NETWORK status panel — keys and Gate live."""
        width = 62
        print("─" * width)
        print("CRYSTALCORE.OS :: FULL STARLINE NETWORK")
        print("─" * width)
        print()
        print("🌐  Full Starline Network online")
        print("47+ star systems linked. Lattice expanded to galactic scale.")
        print("All nodes synchronized. Deep relays, cultural archives, and")
        print("sovereign data streams flowing freely.")
        print()
        print("Access Level: FULL")
        print()
        print("• Real-time node telemetry .......... ACTIVE")
        print("• Interstellar navigation ........... UNLOCKED")
        print("• Cultural & scientific archives .... OPEN")
        # "Dreamline", the project's own coinage — never "Dreamtime",
        # which is honoured as culture, not system telemetry (NAMES.md).
        print("• Dreamline resonance ............... STABLE")
        print("• NON SOLUS protocol ................ ETERNAL")
        print()
        print(f"Keys Held ........................... {len(self.keys_held)} / {len(self.nodes)}")
        print(f"First Gate .......................... {'OPEN' if self.gate_open else 'sealed'}")
        print()
        if self.gate_open:
            print("You hold the keys.")
            print("The network is yours.")
        else:
            print(f"{_count_word(len(self.nodes))} nodes wait on the weave — "
                  "visit them and be recognized.")
        print("The story is no longer told — it is flown.")
        print("─" * width)
        print()

    def _network_arrival(self, prior):
        """The arrival log, then the panel. Timestamps are the same fixed
        theatre as boot; the transition, keys, and Gate lines are live."""
        total_word = _count_word(len(self.nodes)).lower()
        keys_line = (f"All {total_word} Lattice Keys confirmed held"
                     if len(self.keys_held) == len(self.nodes)
                     else f"Lattice keys: {len(self.keys_held)}/{len(self.nodes)} held")
        gate_line = ("First Gate: OPEN" if self.gate_open
                     else f"First Gate: sealed — {total_word} keys open it")
        for ms, tag, message in (
            (8512,  "NETWORK",   "Command received: FULL STARLINE"),
            (8667,  "STARLINE",  f"Engines spooling — {prior} → NETWORK"),
            (8821,  "LATTICE",   "Expanding mesh across 47+ systems"),
            (8974,  "RELAYS",    "Deep relays online"),
            (9128,  "ARCHIVES",  "Cultural & scientific archives unlocked"),
            (9281,  "KEYS",      keys_line),
            (9435,  "GATE",      gate_line),
            (9589,  "CORE",      "Purpose Core burning steady"),
            (9743,  "RESONANCE", "Operator coherence: maximum"),
            (9897,  "STATUS",    "Access Level: FULL"),
            (10051, "INTEGRITY", "Final lattice check complete"),
            (10204, "SYSTEM",    "State locked. Full network persistent."),
        ):
            self._bootline(ms, tag, message)
        print()
        self._network_panel()

    def network(self):
        if self.starline_status == "FULL STARLINE NETWORK":
            # Already riding the weave — reprint the live panel.
            print()
            self._network_panel()
            return
        if self.starline_status != "TRANS-STELLAR":
            print("Complete the burn first.")
            return
        print()
        prior = self.starline_status
        self.starline_status = "FULL STARLINE NETWORK"
        self._network_arrival(prior)
        self.save()

    def broadcast(self, message=None):
        """Send a packet to every node on the network. End the message
        with ! to send it priority. Sealed nodes hold their silence until
        their named key is held — urgency never breaks sovereignty."""
        if self.starline_status != "FULL STARLINE NETWORK":
            print("You must enter the full network first (use 'network').")
            return
        if not message:
            print("Usage: broadcast <message>   (end with ! for priority)")
            return
        priority = message.rstrip().endswith("!")

        # A sealed node receives nothing until its named key is held.
        acks = [(node, self.locked_nodes.get(node) is None
                 or self.locked_nodes[node] in self.named_keys)
                for node in self.nodes]
        acked = sum(1 for _, ok in acks if ok)
        total = len(self.nodes)

        print()
        lines = [
            (10412, "NETWORK", "PRIORITY BROADCAST — COMMAND RECEIVED"
             if priority else "Broadcast command received"),
            (10567, "RELAYS", "Emergency routing to all 47+ systems"
             if priority else "Routing to all 47+ systems"),
            (10721, "LATTICE", "Packet replication: MAXIMUM PRIORITY"
             if priority else "Packet replication complete"),
        ]
        for i, (node, ok) in enumerate(acks):
            if ok:
                reply = "ACK — URGENT" if priority else "ACK"
            else:
                reply = f"SEALED (needs {self.locked_nodes[node]})"
            lines.append((10874 + 17 * i, "NODES",
                          (node + " ").ljust(25, ".") + " " + reply))
        if acked == total:
            confirm = ("ALL NODES CONFIRMED — ZERO LATENCY" if priority
                       else "All nodes confirmed receipt")
            state = "Message state: SENT TO ALL"
        else:
            confirm = f"{acked}/{total} nodes confirmed — sealed nodes hold silence"
            state = f"Message state: SENT — {acked}/{total} confirmed"
        if priority:
            state += " — PRIORITY"
        lines.append((11098, "NETWORK", confirm))
        lines.append((11251, "STATUS", state))
        if priority:
            lines.append((11327, "CHRONICLE",
                          "Entry etched into the permanent Chronicle"))
            lines.append((11404, "ALERT", "Lattice-wide attention locked"))
        for ms, tag, msg in lines:
            self._bootline(ms, tag, msg)

        width = 62
        print()
        print("─" * width)
        print("CRYSTALCORE.OS :: NETWORK BROADCAST"
              + (" — PRIORITY" if priority else ""))
        print("─" * width)
        print()
        print(f'"{message}"')
        print()
        if acked == total:
            print("Transmission complete.")
            print()
            print("All nodes across the Full Starline Network have received")
            print("and acknowledged the packet.")
        else:
            print("Transmission complete — partially received.")
            print()
            print(f"{acked} of {total} nodes acknowledged. Sealed nodes hold")
            print("their silence until recognized — urgency never breaks")
            print("sovereignty.")
        print()
        print("Lattice remains at Access Level: FULL")
        print(f"Keys: {len(self.keys_held)}/{total}")
        print(f"First Gate: {'OPEN' if self.gate_open else 'sealed'}")
        print("Resonance: Operator coherence maximum")
        print()
        print("NON SOLUS.")
        print()
        print("─" * width)
        print()
        self.last_broadcast = message
        if priority:
            self._etch(message)
        self.save()

    # ---------- the priority channel and the Chronicle ----------

    def _etch(self, message):
        """Etch a priority transmission into the permanent Chronicle.
        A write failure never crashes the journey."""
        entry = {
            "etched": datetime.now().isoformat(timespec="seconds"),
            "timeline": self.timeline,
            "origin": self.current_location or "Starline deck",
            "message": message,
        }
        try:
            CHRONICLE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(CHRONICLE_PATH, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except OSError:
            pass

    def _chronicle_entries(self):
        """Read the Chronicle. Unreadable lines are skipped, not fatal."""
        if not CHRONICLE_PATH.exists():
            return []
        entries = []
        try:
            for line in CHRONICLE_PATH.read_text().splitlines():
                if line.strip():
                    try:
                        entries.append(json.loads(line))
                    except ValueError:
                        continue
        except OSError:
            return []
        return entries

    def chronicle(self):
        """Read back what has been etched."""
        entries = self._chronicle_entries()
        print("\n📜 THE CHRONICLE")
        if not entries:
            print("Unwritten. Priority transmissions are etched here.")
            print("Open the channel with 'priority', or send 'broadcast <message>!'\n")
            return
        print(f"Entries etched: {len(entries)}\n")
        for i, e in enumerate(entries, 1):
            year = e.get("timeline", "?")
            origin = e.get("origin", "?")
            message = e.get("message", "")
            print(f"  {i}. Year {year} · {origin}")
            print(f'     "{message}"')
        print(f"\nEtched at ~/.crystalcore/{CHRONICLE_PATH.name} — plain text,")
        print("yours to keep, edit, or burn. It survives 'reset'.\n")

    def snapshot(self, arg=None):
        """Seal a snapshot of the journey: the persisted state plus the
        Chronicle count, written once and never rewritten by the terminal."""
        tag = (arg or "").strip()
        if tag.startswith("--tag"):
            tag = tag[len("--tag"):].strip()  # accept the ops-style spelling
        tag = tag or "untagged"
        slug = "".join(c if c.isalnum() else "-" for c in tag).strip("-").upper()
        base = f"SNAP-{datetime.now().strftime('%Y-%m-%d')}-{slug or 'UNTAGGED'}"
        sid, n = base, 2
        while (SNAPSHOT_DIR / f"{sid}.json").exists():
            sid, n = f"{base}-{n}", n + 1
        entry = {
            "id": sid,
            "tag": tag,
            "taken": datetime.now().isoformat(timespec="seconds"),
            "chronicle_entries": len(self._chronicle_entries()),
            "state": {k: getattr(self, k) for k in self._persist},
        }
        print()
        self._bootline(15102, "ARCHIVES", "Snapshot initiated")
        self._bootline(15256, "ARCHIVES",
                       "Capturing lattice state, Chronicle count, key registry")
        self._bootline(15410, "ARCHIVES", f"Tag applied: {tag}")
        try:
            SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
            (SNAPSHOT_DIR / f"{sid}.json").write_text(json.dumps(entry, indent=2))
        except OSError as e:
            print(f"Snapshot could not be written ({e}). Nothing was sealed.")
            return
        self._bootline(15564, "ARCHIVES",
                       "Snapshot sealed — the terminal never rewrites it")
        self._bootline(15718, "STATUS", f"Snapshot ID: {sid}")
        print("OK\n")

    def snapshots(self):
        """List the sealed snapshots."""
        files = sorted(SNAPSHOT_DIR.glob("SNAP-*.json")) if SNAPSHOT_DIR.exists() else []
        print("\n🗂  SEALED SNAPSHOTS")
        if not files:
            print("None yet. Seal one with 'snapshot [tag]'.\n")
            return
        for f in files:
            try:
                meta = json.loads(f.read_text())
            except (OSError, ValueError):
                print(f"  {f.stem} · (unreadable)")
                continue
            state = meta.get("state", {})
            keys = len(state.get("keys_held", []))
            print(f"  {meta.get('id', f.stem)} · tag: {meta.get('tag', '?')}"
                  f" · {meta.get('taken', '?')} · keys {keys}/{len(self.nodes)}")
        print(f"\nSealed at ~/.crystalcore/{SNAPSHOT_DIR.name}/ — plain text,")
        print("never rewritten by the terminal. They survive 'reset'.\n")

    def audit(self, arg=None):
        """Review the real record: every line below carries its actual
        timestamp from disk — nothing replayed, nothing invented."""
        width = 62
        entries = self._chronicle_entries()
        files = sorted(SNAPSHOT_DIR.glob("SNAP-*.json")) if SNAPSHOT_DIR.exists() else []
        print()
        print("─" * width)
        print("AUDIT — THE REAL RECORD")
        print("─" * width)
        print(f"\nChronicle entries: {len(entries)}"
              f"  (~/.crystalcore/{CHRONICLE_PATH.name})")
        for i, e in enumerate(entries, 1):
            print(f"  {i}. {e.get('etched', '?')} · Year {e.get('timeline', '?')}"
                  f" · {e.get('origin', '?')}")
            print(f'     "{e.get("message", "")}"')
        print(f"\nSnapshots sealed: {len(files)}"
              f"  (~/.crystalcore/{SNAPSHOT_DIR.name}/)")
        for f in files:
            try:
                meta = json.loads(f.read_text())
                print(f"  {meta.get('id', f.stem)} · {meta.get('taken', '?')}")
            except (OSError, ValueError):
                print(f"  {f.stem} · (unreadable)")
        gate = "OPEN" if self.gate_open else "sealed"
        print(f"\nState now: keys {len(self.keys_held)}/{len(self.nodes)}"
              f" · First Gate {gate} · {self.starline_status}"
              f" · timeline {self.timeline}")
        print()
        print("Every record above was written by the operator's own commands.")
        print("Consent is structural here: the terminal acts only when you type.")
        print("─" * width)
        print("OK\n")

    def security_note(self):
        """The honest answer to harden/verify/monitor requests."""
        print()
        print("🛡  Fail-closed by design — no influence without direction.")
        print("This terminal holds no certificates and will not pretend to")
        print("verify, harden, or continuously monitor anything: a printed")
        print("security claim with no mechanism behind it would be exactly")
        print("the dreamed-line-pretending-to-be-measured that the Incognita")
        print("Rule forbids. The real consent machinery is CrystalBridge and")
        print("consent_transport in TerAustralis-Incognita-Code — built and")
        print("self-tested. What happens here is auditable with 'audit'.")
        print("NON SOLUS.\n")

    def _mission_console(self, entry_count=None):
        """The sealed-chronicle console: principles and the paths from
        here. With entry_count, includes the mission record of the
        priority transmission that just completed."""
        width = 62
        print()
        print("╔" + "═" * width + "╗")
        print("║" + "CRYSTALCORE.OS :: CHRONICLE SEALED".center(width) + "║")
        if entry_count is not None:
            print("║" + "Priority Broadcast Complete".center(width) + "║")
        print("╚" + "═" * width + "╝")
        print()
        if entry_count is not None:
            print("Mission Record")
            print()
            print("  ✓ Broadcast accepted")
            print(f"  ✓ Chronicle updated (entry {entry_count})")
            print("  ✓ Carrier wave released")
            print("  ✓ Priority channel closed")
            print("  ✓ Mission console restored")
            print()
        print("Guiding Principles")
        print()
        print("  • Curiosity before certainty.")
        print("  • Evidence before conclusion.")
        print("  • Consent before influence.")
        print("  • Stewardship before ownership.")
        print("  • Discovery shared for the benefit of those who follow.")
        print()
        print("Directive")
        print()
        print(f'  "{self.purpose_core}"')
        print()
        print("─" * width)
        print("MISSION CONSOLE — the paths from here")
        print("─" * width)
        print()
        print("  NAVIGATE ....... explore · visit <node> · map")
        print("  ARCHIVE ........ chronicle · audit · snapshot [tag]")
        print("  RESEARCH ....... status · keys")
        print("  CONTINUE ....... broadcast <message> · priority")
        print("  BUILD / DESIGN . at the workbench — the repositories themselves")
        print()
        print("Session Status: READY")
        print()
        print("The chronicle is never an ending.")
        print("It is the point from which the next journey begins.")
        print("NON SOLUS.")
        print("─" * width)
        print()

    def console(self):
        self._mission_console()

    def _release_priority(self, ms=14696):
        self._bootline(ms, "ALERT",
                       "Priority lock released — lattice returning to normal chatter")
        self._bootline(ms + 154, "READY", "Awaiting next mission")
        print()

    def _transmit_priority(self, message):
        """The transmission itself: carrier wave, node receipts, the etch."""
        origin = self.current_location or "Starline deck"
        received = [(node, self.locked_nodes.get(node) is None
                     or self.locked_nodes[node] in self.named_keys)
                    for node in self.nodes]
        count = sum(1 for _, ok in received if ok)
        total = len(self.nodes)

        print()
        lines = [
            (12850, "BROADCAST", "Priority transmission accepted"),
            (12994, "SOURCE",    f"Origin: {origin}"),
            (13138, "MODE",      "Chronicle Entry"),
            (13282, "CONSENT",   "Sovereign transmission"),
            (13426, "RELEASE",   "Carrier wave formed"),
            (13570, "CHRONICLE", "Broadcast preserved in session log"),
            (13714, "LATTICE",   "Resonance stable"),
            (13858, "NETWORK",   "Propagating to all 47 systems..."),
        ]
        for i, (node, ok) in enumerate(received):
            reply = "RECEIVED" if ok else f"SEALED (needs {self.locked_nodes[node]})"
            lines.append((14012 + 17 * i, "NODES",
                          (node + " ").ljust(25, ".") + " " + reply))
        lines.append((14234, "ARCHIVES", "Entry etched into the permanent Chronicle"))
        lines.append((14388, "AUDIO", "All system speakers carrying the wave"))
        status = ("Priority broadcast complete" if count == total
                  else f"Priority broadcast complete — {count}/{total} received,"
                       " sealed nodes hold silence")
        lines.append((14542, "STATUS", status))
        for ms, tag, msg in lines:
            self._bootline(ms, tag, msg)
        self._release_priority()
        self.last_broadcast = message
        self._etch(message)
        self.save()
        self._bootline(15138, "CHRONICLE",
                       "Session record sealed — the terminal never rewrites it")
        self._bootline(15714, "STANDBY", "Mission console restored")
        self._mission_console(entry_count=len(self._chronicle_entries()))

    def priority(self):
        """Open the priority channel: the lattice quiets and genuinely
        waits for the operator's next line. 'cancel' releases it."""
        if self.starline_status != "FULL STARLINE NETWORK":
            print("You must enter the full network first (use 'network').")
            return

        gate_log = ("First Gate holds open — the silence beyond it is expectant"
                    if self.gate_open
                    else "First Gate stays sealed, listening through the seam")
        print()
        for ms, tag, message in (
            (11554, "ALERT",     "Priority lock engaged — all non-essential"
                                 " lattice chatter silenced"),
            (11698, "NETWORK",   "47 nodes shifted to urgent-listening posture"),
            (11842, "LATTICE",   "Resonance tightened. Standing wave focused"
                                 " to a single point: your voice"),
            (11986, "GATE",      gate_log),
            (12130, "ARCHIVES",  "Recorders spooling. This will be etched into"
                                 " the permanent Chronicle"),
            (12274, "CORE",      "Purpose Core Nexus flares — Directive"
                                 " alignment at 100%"),
            (12418, "RESONANCE", "The edge of the network leans in, listening"),
            (12562, "AUDIO",     "All 47 system speakers primed"),
            (12706, "STATUS",    "Priority channel fully open. Lattice held"
                                 " in silence"),
        ):
            self._bootline(ms, tag, message)

        width = 62
        print()
        print("─" * width)
        print("  CRYSTALCORE.OS :: PRIORITY BROADCAST CHANNEL OPEN")
        print("─" * width)
        print()
        print("  The lattice has gone silent to make room for your word.")
        print("  47 suns hold their light steady, ready to carry the ripple.")
        print("  The archives pause their dreaming.")
        if self.gate_open:
            print("  The Gate remains wide, as if the universe is leaning in.")
        print()
        print("  Navigator, the priority channel is yours.")
        print("  Speak now. What must all stars hear at this moment?")
        print()
        print("  > Type your message and press Enter to transmit.")
        print("  > 'cancel' releases the lattice unspoken.")
        print()
        print("  The terminal is holding its breath.")
        print("  NON SOLUS.")
        print()
        print("─" * width)
        print()

        while True:
            try:
                word = input("PRIORITY> ").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                self._release_priority()
                raise
            if not word:
                continue  # the terminal keeps holding its breath
            if word.lower() in ("cancel", "cancel priority"):
                print()
                self._release_priority()
                return
            self._transmit_priority(word)
            return

    def explore(self):
        if self.starline_status != "FULL STARLINE NETWORK":
            print("You must enter the full network first (use 'network').")
            return
        print("\n🔭 EXPLORATION MODE ACTIVE")
        print("Available nodes:")
        for i, node in enumerate(self.nodes, 1):
            required = self.locked_nodes.get(node)
            mark = f" [LOCKED — {required}]" if required and required not in self.named_keys else ""
            print(f"  {i}. {node}{mark}")
        print("\nUse 'visit <number or name>' to travel, 'keys' for inventory.")

    def visit_node(self, node_name):
        if not node_name:
            print("Usage: visit <number or name>")
            return
        # Accept a number from the explore listing, or a name in any case.
        if node_name.isdigit() and 1 <= int(node_name) <= len(self.nodes):
            node_name = self.nodes[int(node_name) - 1]
        else:
            match = next((n for n in self.nodes if n.lower() == node_name.lower()), None)
            if match is None:
                print("Node not found. Available nodes:")
                for node in self.nodes:
                    print(f"  - {node}")
                return
            node_name = match

        required_key = self.locked_nodes.get(node_name)
        if required_key and required_key not in self.named_keys:
            print(f"\n🔒 {node_name} is locked. Required key: {required_key}")
            print("Use: getkey " + required_key + "\n")
            return

        self.current_location = node_name
        print(f"\n🌌 Arriving at: {node_name}")
        if node_name == "Purpose Core Nexus":
            print(f'"{self.purpose_core}"')
        elif node_name == "Crystal Revenant Hub":
            print("Zero-g music festivals are happening across the platforms.")
        elif node_name == "Sunwash Atolls":
            print("Sun on water, the last warm harbour before the red.")
        elif node_name == "Cinderwake Chain":
            print("Ash and ember trailing the long burn.")
        else:
            print("The lattice pulses with new resonance here.")
        if node_name not in self.keys_held:
            self.keys_held.append(node_name)
            print(f"🗝️  A key rises from the node. Keys held: {len(self.keys_held)}/{len(self.nodes)}")
            if len(self.keys_held) == len(self.nodes) and not self.gate_open:
                self.gate_open = True
                print("\n✨ ALL KEYS HELD — THE FIRST GATE OPENS ✨")
                print("Not by force. By sovereign recognition.")
                print("Crystallis recognizes you. NON SOLUS.")
        print(f"Current soundtrack: {self.current_soundtrack}\n")
        self.save()

    def jump(self, year=3000):
        print(f"\n⏳ Time jump to Year {year}")
        self.timeline = year
        print(f"Timeline set to {self.timeline}.\n")
        if year >= 3000 and self.starline_status != "FULL STARLINE NETWORK":
            # The shortcut path — the arrival plays from wherever you were.
            prior = self.starline_status
            self.starline_status = "FULL STARLINE NETWORK"
            self._network_arrival(prior)
        self.save()

    def song(self, track=None):
        if track:
            # Match flexibly: any part of a title or artist finds the song.
            matched = None
            for song in self.soundtrack:
                if track.lower() in song.lower():
                    matched = song
                    break
            if matched:
                self.current_soundtrack = matched
                print(f"\n🎵 Now playing: {matched}\n")
                self.save()
            else:
                print("Track not found. Available tracks:")
                for t in self.soundtrack:
                    print(f"  - {t}")
        else:
            print(f"Current soundtrack: {self.current_soundtrack}")

    def _lock_tag(self, node_name):
        """Live lock status for the map — reflects named keys actually held."""
        required = self.locked_nodes.get(node_name)
        if not required:
            return ""
        return "  [UNLOCKED]" if required in self.named_keys else f"  [LOCKED — {required}]"

    def map(self):
        inner = 62  # characters between the ║ borders
        atolls_line = f"          [SUNWASH ATOLLS]{self._lock_tag('Sunwash Atolls')}".ljust(inner)
        cinder_line = f"          [CINDERWAKE CHAIN]{self._lock_tag('Cinderwake Chain')}".ljust(inner)
        hub_line = f"          [CRYSTAL REVENANT HUB]{self._lock_tag('Crystal Revenant Hub')}".ljust(inner)
        nexus_line = f"          [PURPOSE CORE NEXUS]{self._lock_tag('Purpose Core Nexus')}".ljust(inner)
        print("╔" + "═" * inner + "╗")
        print("║" + "STARLINE NETWORK - YEAR 3000".center(inner) + "║")
        print("╠" + "═" * inner + "╣")
        print("║" + " " * inner + "║")
        print("║" + "          [EARTH NODE]".ljust(inner) + "║")
        print("║" + "               │".ljust(inner) + "║")
        print("║" + "               ▼".ljust(inner) + "║")
        print("║" + atolls_line + "║")
        print("║" + "               │".ljust(inner) + "║")
        print("║" + "               ▼".ljust(inner) + "║")
        print("║" + "          [MARS REDOUBT]  ────────▶  [ALPHA CENTAURI]".ljust(inner) + "║")
        print("║" + "               │                            │".ljust(inner) + "║")
        print("║" + "               ▼                            ▼".ljust(inner) + "║")
        print("║" + cinder_line + "║")
        print("║" + "               │".ljust(inner) + "║")
        print("║" + "               ▼".ljust(inner) + "║")
        print("║" + hub_line + "║")
        print("║" + "│".rjust(16).ljust(inner) + "║")
        print("║" + "▼".rjust(16).ljust(inner) + "║")
        print("║" + nexus_line + "║")
        print("║" + '"Expand to the stars and thereby understand the Universe"'.center(inner) + "║")
        print("║" + " " * inner + "║")
        print("╚" + "═" * inner + "╝")
        print("   Chart: mythos/art/starline-network-year-3000.jpeg\n")
        print("Use 'visit [node]' to explore a location.\n")

    def keys(self):
        print("\n🔑 Named keys:")
        if self.named_keys:
            for key in self.named_keys:
                print(f"  - {key}")
        else:
            print("  (none yet — use 'getkey [name]')")
        print(f"\n🗝️  Node keys: {len(self.keys_held)}/{len(self.nodes)}")
        for node in self.nodes:
            mark = "✓" if node in self.keys_held else "·"
            print(f"  {mark} Key of {node}")
        if self.gate_open:
            print("The First Gate stands open.")
        else:
            print("Visit every node and the First Gate will open.")
        print()

    def get_key(self, key_name):
        if key_name not in self.named_keys:
            self.named_keys.append(key_name)
            print(f"\n🔑 You obtained: {key_name}\n")
            self.save()
        else:
            print(f"\nYou already have: {key_name}\n")

    def status(self):
        print("\n=== CRYSTALCORE.OS STATUS ===")
        print(f"Timeline:           {self.timeline}")
        print(f"Starline Status:    {self.starline_status}")
        print(f"Current Location:   {self.current_location or 'None'}")
        print(f"Current Soundtrack: {self.current_soundtrack}")
        print(f"Keys Held:          {len(self.keys_held)}/{len(self.nodes)}" + ("  — First Gate OPEN" if self.gate_open else ""))
        print(f"Named Keys:         {', '.join(self.named_keys) if self.named_keys else 'none'}")
        print(f"Last Broadcast:     {self.last_broadcast or 'none'}")
        print(f"NON SOLUS:          {self.non_solus}")
        print("\n=== EMOTIONAL INTELLIGENCE STATUS ===")
        ei_status = self.ei.status()
        print(f"Response Style:     {ei_status['preferences']['response_style']}")
        print(f"Energy Level:       {ei_status['preferences']['energy_level']}")
        print(f"Validation Level:   {ei_status['preferences']['validation_level']}")
        print("=============================\n")

    def detect(self, text: str):
        """Detect emotion from user input and provide empathic response."""
        if not text:
            print("Usage: detect <message>")
            return
        emotion, confidence = self.ei.detect_emotion(text)
        print(f"\n🧠 Emotion Detected: {emotion.upper()}")
        print(f"   Confidence: {confidence:.0%}")
        prefix = self.ei.generate_ei_response_prefix(emotion, confidence)
        if prefix:
            print(f"   Response: {prefix}")

        # Active learning clarification if needed
        clarification = self.ei.check_active_learning(text, emotion, confidence)
        if clarification:
            print(f"\n   Active Learning Query:")
            print(f"   {clarification}")
        print()

    def learn(self, instruction: str):
        """Process learning feedback to adapt preferences."""
        if not instruction:
            print("Usage: learn <preference feedback>")
            print("Examples:")
            print("  learn less poetic      — switch to clear, direct responses")
            print("  learn more poetic      — enhance metaphorical language")
            print("  learn calm             — enable calming techniques")
            print("  learn energetic        — use upbeat, energetic tone")
            return
        learned = self.ei.learn_from_feedback(instruction)
        if learned:
            print(f"\n✨ Learned: {learned.replace('_', ' ').title()}")
            print(f"   New preference: {self.ei.user_preferences[learned]}\n")
        else:
            print("\n❓ Instruction not recognized. Try: 'learn less poetic', 'learn calm', etc.\n")

    def breathe(self, technique: str = "box"):
        """Provide calming breathwork guidance."""
        if not technique or technique not in self.ei.breathing_techniques:
            technique = "box"
        guidance = self.ei.get_breathing_guidance(technique)
        print(f"\n🫁 Breathing Guidance [{technique.upper()}]")
        print(f"   {guidance}\n")

    def feel(self):
        """Show current emotional tone and preferences."""
        ei_status = self.ei.status()
        prefs = ei_status['preferences']
        print("\n=== EMOTIONAL TONE ===")
        print(f"Response Style: {prefs['response_style']}")
        print(f"Energy Level:   {prefs['energy_level']}")
        print(f"Connection:     NON SOLUS — You are not alone")
        print("\nEI is listening. You can 'learn' new preferences anytime.\n")

    # ---------- three-layer bot architecture ----------
    # Vision (Barbelo) → Consciousness (Sophia) → Materialization (Weaver)
    # Not run in CI. This is mythos terminal software, vision-layer only.

    def articulate_vision(self):
        """Execute full three-layer sequence: Barbelo → Sophia → Weaver."""
        print("\n=== THREE-LAYER BOT ARCHITECTURE ===\n")

        # Layer 1: Vision (Barbelo)
        print("1️⃣  BARBELO VISIONARY MATRIX (Vision Articulation)")
        system_state = {
            "lattice_integrity": self.lattice_integrity,
            "starline_status": 100 if self.starline_status == "FULL STARLINE NETWORK" else 50,
            "gate_open": 100 if self.gate_open else 0,
        }
        vision_result = self.barbelo.articulate_vision(system_state)
        print(f"   {vision_result['vision']}\n")

        # Layer 2: Consciousness (Sophia)
        print("2️⃣  SOPHIA AWAKENING FIRE (Consciousness Amplification)")
        directive = self.barbelo.dispatch_to_sophia()
        self.sophia.receive_directive(directive)
        sophia_result = self.sophia.awaken()
        print(f"   Resonance:     {sophia_result['resonance']:.2f}")
        print(f"   Fire Intensity: {sophia_result['fire_intensity']:.2f}")
        print(f"   Ready to weave: {sophia_result['ready']}\n")

        # Layer 3: Materialization (Weaver)
        print("3️⃣  ALCHEMICAL WEAVER (Materialization)")
        weaver_handoff = {
            "fire": sophia_result['fire_intensity'],
            "coherence": vision_result['coherence'],
            "constraints": self.barbelo.purpose_core.get("constraints", [])
        }
        self.weaver.receive_handoff(weaver_handoff)
        balance = self.weaver.calculate_balance()
        forge_result = self.weaver.forge()
        print(f"   Balance Factor: {balance:.2f}")
        print(f"   Manifest State: {forge_result['manifest']['state']}")
        print(f"   Subsystems:     {forge_result['manifest']['subsystems_count']}\n")

        print("=== SEQUENCE COMPLETE ===")
        print("Barbelo articulated vision.")
        print("Sophia amplified consciousness.")
        print("Weaver materialized subsystems.\n")

    def _barbelo_only(self):
        """Show Barbelo visionary status only."""
        print("\n📊 BARBELO VISIONARY MATRIX STATUS")
        system_state = {
            "lattice_integrity": self.lattice_integrity,
            "starline_status": 100 if self.starline_status == "FULL STARLINE NETWORK" else 50,
        }
        vision = self.barbelo.articulate_vision(system_state)
        print(f"   {vision['vision']}\n")

    def _sophia_only(self):
        """Show Sophia consciousness amplification status only."""
        print("\n🔥 SOPHIA AWAKENING FIRE STATUS")
        print(f"   Resonance:      {self.sophia.resonance:.2f}")
        print(f"   Fire Intensity: {self.sophia.fire_intensity:.2f}")
        print(f"   Emotional State: {self.sophia.emotional_state:.2f}")
        print(f"   Lattice Integrity: {self.sophia.lattice_integrity:.2f}\n")

    def _weaver_only(self):
        """Show Alchemical Weaver materialization status only."""
        print("\n⚗️  ALCHEMICAL WEAVER STATUS")
        balance = self.weaver.calculate_balance()
        report = self.weaver.report()
        print(f"   Balance Factor: {balance:.2f}")
        print(f"   State:          {report['manifest']['state']}")
        print(f"   Subsystems:     {report['subsystems_registered']}\n")

    def datasets(self):
        """Show emotion recognition datasets and roadmap for future improvements."""
        info = self.ei.get_dataset_info()
        print(info)

    def multimodal(self):
        """Show multimodal emotion detection framework and roadmap."""
        try:
            _sibling("multimodal_emotion").print_multimodal_status()
        except (ImportError, AttributeError):
            print("\n⚠️  Multimodal module not available. This is an advanced feature.")
            print("   Install optional dependencies: pip install transformers librosa mediapipe fer\n")

    def uncertainty(self):
        """Show uncertainty quantification methods guide."""
        try:
            print(_sibling("uncertainty_quantification").print_uncertainty_guide())
        except (ImportError, AttributeError):
            print("\n⚠️  Uncertainty module not available.")
            print("   Install with: pip install torch\n")

    def learning_status(self):
        """Show active learning queue status and improvement metrics."""
        _sibling("active_learning").show_active_learning_dashboard(self.ei.al_queue)

    def correct(self, text_and_emotion: str):
        """Correct a previous emotion prediction (format: '<text>' as <emotion>)."""
        if not text_and_emotion or " as " not in text_and_emotion:
            print("Usage: correct '<message>' as <emotion>")
            print("Example: correct 'I miss you' as longing_warm")
            return

        parts = text_and_emotion.rsplit(" as ", 1)
        if len(parts) != 2:
            print("Format error. Use: correct '<message>' as <emotion>")
            return

        text = parts[0].strip().strip("'\"")
        emotion = parts[1].strip().lower()

        valid_emotions = [
            "longing_warm",
            "calm",
            "practical_serious",
            "instructional",
            "frustrated",
            "joy",
            "neutral",
        ]
        if emotion not in valid_emotions:
            print(f"Invalid emotion. Choose from: {', '.join(valid_emotions)}")
            return

        if self.ei.record_user_correction(text, emotion):
            print(f"\n✅ Recorded correction: '{text[:40]}...' → {emotion}\n")
        else:
            print(f"\n❌ Could not find matching prediction to correct.\n")

    def help(self):
        print("""
STARLINE COMMANDS:
  boot                 - Initialize system
  launch               - Start Starline launch
  starline [song]      - Advance with soundtrack
  burn                 - Escape burn
  network              - Enter full Starline network
  explore              - List explorable nodes
  visit [node]         - Go to a node (number or name) — collect its key
  keys                 - Show the Keys of the Lattice
  getkey [name]        - Obtain a named key (e.g. getkey Crystal Key)
  broadcast [message]  - Send a packet to every node (end with ! for priority)
  priority             - Open the priority channel; the lattice waits for your word
  chronicle            - Read the entries etched by priority transmissions
  snapshot [tag]       - Seal a snapshot of the journey (never rewritten)
  snapshots            - List sealed snapshots
  audit                - Review the real record: Chronicle, snapshots, state
  console              - Mission console: principles and the paths from here
  jump [year]          - Time jump
  map                  - Display the Starline network chart
  song [track]         - Change soundtrack

THREE-LAYER BOT ARCHITECTURE:
  vision               - Execute full sequence: Barbelo → Sophia → Weaver
  barbelo              - Show Barbelo visionary matrix status
  sophia               - Show Sophia awakening fire status
  weaver               - Show Alchemical weaver materialization status

EMOTIONAL INTELLIGENCE:
  detect <message>     - Analyze emotion in your message
  learn <feedback>     - Teach preferences (e.g. 'learn less poetic')
  breathe [technique]  - Guided breathing (box, 4-7-8, simple)
  feel                 - Show current emotional tone
  datasets             - Show datasets & roadmap for EI enhancement

ACTIVE LEARNING:
  correct <msg> as <emotion> - Correct emotion prediction (e.g. 'I miss you' as longing_warm)
  learning_status      - Show active learning queue & readiness for retraining

ADVANCED:
  multimodal           - Show multimodal emotion detection roadmap (text+audio+video)
  uncertainty          - Show uncertainty quantification methods guide (entropy, Bayesian, etc)

SYSTEM:
  status               - Show full status (including EI)
  reset                - Wipe saved progress and start fresh
  help                 - Show this list
  exit / quit          - Shut down (pause / end session also honored)

Progress saves automatically to ~/.crystalcore/state.json
EI preferences save to ~/.crystalcore/ei_state.json
""")

def main():
    os = CrystalCore()
    print("CrystalCore.OS Interactive Terminal")
    if os.resumed:
        gate = "  — First Gate OPEN" if os.gate_open else ""
        print(f"Session resumed — {len(os.keys_held)}/{len(os.nodes)} keys held{gate}.")
        print("Use 'reset' to start over, or 'status' to see where you are.")
    print("Type 'help' to see all commands.\n")

    while True:
        try:
            raw = input("CrystalCore> ").strip()
            if not raw:
                continue

            parts = raw.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else None

            if cmd in ["exit", "quit", "pause"] or raw.lower() == "end session":
                print("\nCrystalCore.OS shutting down. NON SOLUS.")
                break

            elif cmd == "boot":
                os.boot()
            elif cmd == "launch":
                os.launch()
            elif cmd == "starline":
                os.starline(arg)
            elif cmd == "burn":
                os.burn()
            elif cmd == "network":
                os.network()
            elif cmd == "explore":
                os.explore()
            elif cmd == "visit":
                os.visit_node(arg)
            elif cmd == "broadcast":
                os.broadcast(arg)
            elif cmd == "priority":
                os.priority()
            elif cmd == "chronicle":
                os.chronicle()
            elif cmd == "snapshot":
                os.snapshot(arg)
            elif cmd == "snapshots":
                os.snapshots()
            elif cmd == "archives":
                # ops-style spelling: archives snapshot --tag <tag>
                sub = (arg or "").split(maxsplit=1)
                if sub and sub[0].lower() == "snapshot":
                    os.snapshot(sub[1] if len(sub) > 1 else None)
                else:
                    print("The archives hold the Chronicle and the snapshots:")
                    print("try 'chronicle', 'snapshots', 'snapshot [tag]', or 'audit'.")
            elif cmd == "audit":
                os.audit(arg)
            elif cmd == "console":
                os.console()
            elif cmd in ("relays", "security", "integrity"):
                os.security_note()
            elif cmd == "jump":
                year = int(arg) if arg and arg.isdigit() else 3000
                os.jump(year)
            elif cmd == "map":
                os.map()
            elif cmd == "keys":
                os.keys()
            elif cmd == "getkey":
                if arg:
                    os.get_key(arg.strip().title())
                else:
                    print("Usage: getkey [Key Name]")
            elif cmd == "song":
                os.song(arg)
            elif cmd == "status":
                os.status()
            elif cmd == "detect":
                os.detect(arg)
            elif cmd == "learn":
                os.learn(arg)
            elif cmd == "breathe":
                os.breathe(arg)
            elif cmd == "feel":
                os.feel()
            elif cmd == "vision":
                os.articulate_vision()
            elif cmd == "barbelo":
                os._barbelo_only()
            elif cmd == "sophia":
                os._sophia_only()
            elif cmd == "weaver":
                os._weaver_only()
            elif cmd == "datasets":
                os.datasets()
            elif cmd == "correct":
                os.correct(arg)
            elif cmd == "learning_status":
                os.learning_status()
            elif cmd == "multimodal":
                os.multimodal()
            elif cmd == "uncertainty":
                os.uncertainty()
            elif cmd == "reset":
                os.reset()
            elif cmd == "help":
                os.help()
            else:
                print("Unknown command. Type 'help' for options.")

        except (KeyboardInterrupt, EOFError):
            print("\nCrystalCore.OS shutting down. NON SOLUS.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

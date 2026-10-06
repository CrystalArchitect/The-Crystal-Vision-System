"""The start command opens the First Gate once and does not etch twice."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOT = ROOT / "scripts" / "crystalcore" / "boot.py"
TERMINAL = (
    ROOT
    / "archive"
    / "TerAustralis-Incognita"
    / "mythos"
    / "crystalcore-os"
    / "crystalcore_os.py"
)


class BootTests(unittest.TestCase):
    def test_flight_opens_gate_and_second_start_keeps_one_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            first = subprocess.run(
                [sys.executable, str(BOOT), "--home", str(home)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertIn("flight completed", first.stdout)
            state_path = home / ".crystalcore" / "state.json"
            state = json.loads(state_path.read_text())
            self.assertTrue(state["gate_open"])
            self.assertEqual(len(state["keys_held"]), 7)
            self.assertEqual(state["current_location"], "Colossus")
            self.assertEqual(state["timeline"], 3000)
            chronicle = (home / ".crystalcore" / "chronicle.jsonl").read_text().strip().splitlines()
            self.assertEqual(len(chronicle), 2)
            snaps = list((home / ".crystalcore" / "snapshots").glob("*.json"))
            self.assertEqual(len(snaps), 1)

            second = subprocess.run(
                [sys.executable, str(BOOT), "--home", str(home)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("already open", second.stdout)
            chronicle_again = (home / ".crystalcore" / "chronicle.jsonl").read_text().strip().splitlines()
            self.assertEqual(len(chronicle_again), 2)
            snaps_again = list((home / ".crystalcore" / "snapshots").glob("*.json"))
            self.assertEqual(len(snaps_again), 1)

    def test_colossus_stays_shut_until_the_gate_is_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            env = dict(**{k: v for k, v in __import__("os").environ.items()})
            env["HOME"] = str(home)
            result = subprocess.run(
                [sys.executable, str(TERMINAL)],
                input="visit Colossus\nexit\n",
                text=True,
                capture_output=True,
                check=False,
                env=env,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Colossus waits beyond the First Gate", result.stdout)
            state_path = home / ".crystalcore" / "state.json"
            if state_path.is_file():
                state = json.loads(state_path.read_text())
                self.assertNotEqual(state.get("current_location"), "Colossus")
                self.assertFalse(state.get("gate_open"))


if __name__ == "__main__":
    unittest.main()

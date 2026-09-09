"""CrystalCore mini CLI — cross-platform (Linux, macOS, Windows).

    python3 cli/crystalcore.py status
    python3 cli/crystalcore.py paths
    python3 cli/crystalcore.py transmit

Files resolve from the repository checkout first, so a fresh clone works with
no install step. Set CRYSTALCORE_HOME to point somewhere else.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

CHECKLIST = [
    ("FULL manual", "crystalcore-seven-sisters-FULL.md"),
    ("One-pagers", "crystalcore-seven-sisters-paths.md"),
    ("Atlas (path 3)", "crystalcore-atlas-path3.md"),
    ("Audit (path 4)", "crystalcore-path4-audit.md"),
    ("Deep water (5)", "crystalcore-path5-deep-water.md"),
    ("Sky bridge (6)", "crystalcore-path6-sky-bridge.md"),
    ("Ascent (7)", "crystalcore-path7-ascent.md"),
    ("Transmit A", "crystalcore-TRANSMIT-A.txt"),
    ("Landing page", "index.html"),
    ("Water brief", "WATER-BRIEF.md"),
    ("Accel plan", "FIRST-ACCELERATION-PLAN.md"),
]

PATHS_TEXT = """
Seven Sisters paths
  1 Spring      first water; begin
  2 Motion      move; ship; no stagnation
  3 Mark        name true; atlas
  4 Law         consent; audit
  5 Deep water  GAB care; science/vision split
  6 Sky bridge  dust <-> Pleiades (symbolic)
  7 Ascent      transmit; teach; rest

Companion: Orion guardian = protect / propel / prevent_drift
"""

CYAN, GREEN, YELLOW, RED, GREY = "36", "32", "33", "31", "90"


def _use_colour() -> bool:
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def paint(text: str, colour: str) -> str:
    return f"\033[{colour}m{text}\033[0m" if _use_colour() else text


def search_roots() -> list[Path]:
    """Directories searched for CrystalCore files, in precedence order.

    The checkout comes before ~/.grok so the documented quick start works
    without an install; the ~/.grok entries keep older PowerShell setups working.
    """
    roots = []
    override = os.environ.get("CRYSTALCORE_HOME", "").strip()
    if override:
        roots.append(Path(override).expanduser())
    roots.append(REPO_ROOT)

    grok = os.environ.get("GROK_HOME", "").strip()
    grok_home = Path(grok).expanduser() if grok else Path.home() / ".grok"
    roots.extend([grok_home / "crystalcore", grok_home])

    seen, ordered = set(), []
    for root in roots:
        if root not in seen:
            seen.add(root)
            ordered.append(root)
    return ordered


def resolve(name: str) -> Path | None:
    for root in search_roots():
        candidate = root / name
        if candidate.is_file():
            return candidate
    return None


def open_externally(path: Path) -> bool:
    """Hand a file to the desktop viewer. False if there is no opener (headless)."""
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=True)
        elif os.name == "nt":
            os.startfile(str(path))  # type: ignore[attr-defined]
        else:
            subprocess.run(["xdg-open", str(path)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


def cmd_status() -> int:
    print()
    print(paint("=== CrystalCore STATUS ===", CYAN))
    print(f"Root: {REPO_ROOT}")
    print(f"Searching: {', '.join(str(r) for r in search_roots())}")
    print()
    print(paint("Paths (session cycle): 1-7 marked DONE in chat run", GREEN))
    print(paint("Red button: OFF | Belt-Three: Honour / Label / No coerce", YELLOW))
    print()
    print(paint("Files:", CYAN))
    missing = 0
    for label, name in CHECKLIST:
        found = resolve(name)
        if found:
            print(paint(f"  [OK] {label:<16} {found}", GREEN))
        else:
            missing += 1
            print(paint(f"  [--] {label:<16} missing ({name})", GREY))
    print()
    print("Water rails: LEB | GAB | MDB_care (see water brief)")
    print(paint("Not claimed: Elon endorsement, physical sea fill, Songline ownership", GREY))
    print()
    return 1 if missing else 0


def cmd_paths() -> int:
    print(PATHS_TEXT)
    return 0


def cmd_transmit() -> int:
    found = resolve("crystalcore-TRANSMIT-A.txt")
    if not found:
        print(paint("Transmit file missing: crystalcore-TRANSMIT-A.txt", RED), file=sys.stderr)
        return 1
    print()
    print(paint("=== TRANSMIT OPTION A (paste on X) ===", CYAN))
    print()
    print(found.read_text(encoding="utf-8").rstrip())
    print()
    print(paint("You must post this yourself. CLI does not send to X.", YELLOW))
    return 0


def open_command(name: str, label: str) -> int:
    found = resolve(name)
    if not found:
        print(paint(f"Missing: {name}", RED), file=sys.stderr)
        return 1
    if open_externally(found):
        print(paint(f"Opening {label}: {found}", CYAN))
    else:
        print(f"No desktop opener available. {label} is at: {found}")
    return 0


COMMANDS = {
    "status": "Path cycle + file checklist",
    "paths": "List seven paths",
    "atlas": "Open the atlas (path 3)",
    "transmit": "Show Option A post text",
    "water": "Open water brief",
    "plan": "Open first-acceleration plan",
    "open": "Open landing page in browser",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="crystalcore",
        description="CrystalCore mini CLI",
        epilog="commands:\n" + "\n".join(f"  {k:<9} {v}" for k, v in COMMANDS.items()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", nargs="?", default="status", choices=list(COMMANDS))
    args = parser.parse_args(argv)

    if args.command == "status":
        return cmd_status()
    if args.command == "paths":
        return cmd_paths()
    if args.command == "transmit":
        return cmd_transmit()
    targets = {
        "atlas": ("crystalcore-atlas-path3.md", "atlas"),
        "water": ("WATER-BRIEF.md", "water brief"),
        "plan": ("FIRST-ACCELERATION-PLAN.md", "plan"),
        "open": ("index.html", "landing page"),
    }
    return open_command(*targets[args.command])


if __name__ == "__main__":
    raise SystemExit(main())

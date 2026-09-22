#!/usr/bin/env python3
"""Thin launcher: Celestial Portal framing → Lemuria sandbox."""

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "10_ORIGINAL_CREATIVE" / "ahs-lemuria" / "ahs_lemuria.py"

if not SCRIPT.is_file():
    print(f"[ERROR] Lemuria sandbox not found: {SCRIPT}", file=sys.stderr)
    sys.exit(1)

runpy.run_path(str(SCRIPT), run_name="__main__")

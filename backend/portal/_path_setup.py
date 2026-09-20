# Ensure repo root (containing crystal_platform/) is importable.
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
for parent in _HERE.parents:
    if (parent / "crystal_platform").is_dir():
        root = str(parent)
        if root not in sys.path:
            sys.path.insert(0, root)
        break

# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Preflight for the Clementine starter: says what will work before you run.

    python doctor.py

Checks, in the order a fresh machine fails them:
  1. Python version (3.9+)
  2. The one required package for the terminal app (`requests`)
  3. The mind imports from ./core
  4. Memory round-trips offline (no network involved)
  5. Ollama reachable — OPTIONAL; everything except model chat works without it

Exit code 0 when the required checks pass, 1 otherwise. Ollama being absent
never fails the doctor: the companion runs offline, remembers offline, and
tells you plainly when it cannot reach a model.
"""

import pathlib
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "core"))

OK, WARN, FAIL = "[ ok ]", "[warn]", "[FAIL]"
failures = 0


def report(status: str, message: str) -> None:
    print(f"{status} {message}")


# 1. Python
if sys.version_info >= (3, 9):
    report(OK, f"Python {sys.version.split()[0]}")
else:
    report(FAIL, f"Python {sys.version.split()[0]} — need 3.9 or newer")
    failures += 1

# 2. requests
try:
    import requests  # noqa: F401
    report(OK, "requests installed")
except ImportError:
    report(FAIL, "requests missing — run:  pip install -r requirements.txt")
    failures += 1

# 3. the mind
try:
    from crystalcore.mind import CrystalCore  # noqa: E402
    report(OK, "the mind imports (crystalcore.mind)")
except Exception as exc:  # noqa: BLE001 — any import failure is the finding
    report(FAIL, f"the mind failed to import: {exc}")
    failures += 1
    CrystalCore = None

# 4. offline memory round trip
if CrystalCore is not None and failures == 0:
    try:
        with tempfile.TemporaryDirectory() as td:
            first = CrystalCore(memory_dir=td)
            first.memory.facts["doctor_check"] = "passed"
            first.save()
            second = CrystalCore(memory_dir=td)
            assert second.memory.facts.get("doctor_check") == "passed"
        report(OK, "memory persists offline (write, save, fresh load)")
    except Exception as exc:  # noqa: BLE001
        report(FAIL, f"offline memory round trip failed: {exc}")
        failures += 1

# 5. Ollama — optional by design
try:
    import requests as _r
    _r.get("http://127.0.0.1:11434/api/tags", timeout=2).raise_for_status()
    report(OK, "Ollama reachable — model chat will work")
except Exception:  # noqa: BLE001 — absence is a state, not an error
    report(WARN, "Ollama not reachable — memory and commands still work; "
                 "chat will say it cannot reach a model. To enable chat: "
                 "install from ollama.com, then `ollama pull llama3.2:1b` "
                 "(small hardware) or `llama3.1:8b` (better answers).")

print()
if failures:
    print(f"doctor: {failures} required check(s) failed")
    sys.exit(1)
print("doctor: ready — run it with:  python clementine.py")

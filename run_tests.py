#!/usr/bin/env python3
"""
Minimal, dependency-free test runner for CrystalCore.

Why this exists: edge/offline deployment means we cannot assume pytest is
installed on a bare Raspberry Pi. This shim runs the existing test_*.py files
using only the standard library. It emulates the small subset of pytest we use:
  - test discovery (module-level test_* functions)
  - the `tmp_path` fixture (a pathlib.Path to a fresh temp dir)
  - the `monkeypatch` fixture (setattr that is undone after the test)

Usage:
    python3 run_tests.py            # run tests/test_crystal_memory.py
    python3 run_tests.py path.py    # run a specific test file
"""

import importlib.util
import inspect
import os
import sys
import tempfile
import traceback
import shutil
from pathlib import Path


class _MonkeyPatch:
    def __init__(self):
        self._undo = []

    def setattr(self, target, name, value):
        old = getattr(target, name)
        self._undo.append((target, name, old))
        setattr(target, name, value)

    def undo(self):
        for target, name, old in reversed(self._undo):
            setattr(target, name, old)
        self._undo.clear()


def _make_fixture(param, tmp_root):
    if param == "tmp_path":
        d = tempfile.mkdtemp(dir=tmp_root)
        return Path(d), None
    if param == "monkeypatch":
        mp = _MonkeyPatch()
        return mp, mp
    raise RuntimeError(f"Unsupported fixture: {param}")


def run_file(path):
    mod_name = "testmod_" + os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    tests = [
        (name, fn)
        for name, fn in inspect.getmembers(mod, inspect.isfunction)
        if name.startswith("test_") and fn.__module__ == mod_name
    ]
    tests.sort(key=lambda t: inspect.getsourcelines(t[1])[1])

    passed, failed = 0, 0
    failures = []
    tmp_root = tempfile.mkdtemp(prefix="crystalcore_tests_")

    try:
        for name, fn in tests:
            params = [
                p.name for p in inspect.signature(fn).parameters.values()
                if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
            ]
            kwargs = {}
            teardowns = []
            try:
                for p in params:
                    val, teardown = _make_fixture(p, tmp_root)
                    kwargs[p] = val
                    if teardown:
                        teardowns.append(teardown)
                fn(**kwargs)
                print(f"  PASS  {name}")
                passed += 1
            except Exception:
                print(f"  FAIL  {name}")
                failures.append((name, traceback.format_exc()))
                failed += 1
            finally:
                for t in teardowns:
                    t.undo()
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)

    print(f"\n{passed} passed, {failed} failed")
    if failures:
        print("\n" + "=" * 60 + "\nFAILURES\n" + "=" * 60)
        for name, tb in failures:
            print(f"\n--- {name} ---\n{tb}")
    return failed == 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        # Discover all test_*.py under tests/.
        tests_dir = os.path.join(os.path.dirname(__file__), "tests")
        targets = sorted(
            os.path.join("tests", f)
            for f in os.listdir(tests_dir)
            if f.startswith("test_") and f.endswith(".py")
        )

    all_ok = True
    for target in targets:
        print(f"Running {target}\n" + "-" * 60)
        ok = run_file(target)
        all_ok = all_ok and ok
        print()
    sys.exit(0 if all_ok else 1)

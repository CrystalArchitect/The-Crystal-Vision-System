# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""CycleLogger truncates on construction so a re-run is byte-identical
(see log.py's module docstring) — which means two loggers sharing a path
would silently corrupt each other's log unless the second construction is
refused outright. Loop's log_path defaults to the same literal string for
every default-constructed Loop, so this was reachable with zero arguments."""
import os
import pathlib
import sys
import tempfile

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.log import CycleLogger
from core.loop import Loop


def test_second_logger_on_same_path_raises_instead_of_truncating():
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "shared.jsonl")
        first = CycleLogger(path)
        first.log("track", {"n": 1}, cycle=1)

        with pytest.raises(RuntimeError, match="already writing"):
            CycleLogger(path)

        # The first logger's line must survive the failed second construction.
        assert len(first.read_all()) == 1


def test_two_default_constructed_loops_no_longer_collide():
    with tempfile.TemporaryDirectory() as td:
        cwd = os.getcwd()
        os.chdir(td)
        try:
            loop1 = Loop(store_path=":memory:")
            loop1.run_cycle(expected="a", actual="b", event={"owner": "loop1"})

            with pytest.raises(RuntimeError, match="already writing"):
                Loop(store_path=":memory:")

            # loop1's log is intact, not truncated or interleaved by the
            # rejected loop2 construction attempt.
            entries = loop1.logger.read_all()
            assert len(entries) == 4
            assert entries[0]["data"] == {"owner": "loop1"}
        finally:
            os.chdir(cwd)


def test_logger_path_freed_once_owner_is_garbage_collected():
    with tempfile.TemporaryDirectory() as td:
        path = os.path.join(td, "reused.jsonl")
        first = CycleLogger(path)
        first.log("track", {"n": 1}, cycle=1)
        del first  # CPython: refcount drops to zero, releases the claim

        # A fresh logger may now legitimately claim the same path — and,
        # per the truncate-on-construct contract, starts that path over.
        second = CycleLogger(path)
        assert second.read_all() == []

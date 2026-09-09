# Copyright (c) 2026 TerAustralis Incognita — ABN 70 741 068 059
# SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""GapDetector's dict-magnitude comparison must distinguish a key that is
absent from a key that is present with value None — plain dict.get(k)
returns None for both, so {} and {"a": None} compared that way read as
equal when they are not."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from core.gap import GapDetector


def test_missing_key_differs_from_explicit_none():
    gd = GapDetector()
    gap = gd.detect(expected={}, actual={"a": None})
    assert gap is not None
    assert gap.magnitude == 1.0


def test_shared_explicit_none_is_not_a_diff():
    gd = GapDetector()
    assert gd.detect(expected={"a": None}, actual={"a": None}) is None


def test_partial_dict_match_still_scores_correctly():
    gd = GapDetector()
    gap = gd.detect(expected={"a": 1, "b": 2}, actual={"a": 1, "b": 3})
    assert gap is not None
    assert gap.magnitude == 0.5

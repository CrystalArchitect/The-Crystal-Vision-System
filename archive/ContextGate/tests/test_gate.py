#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gate import gate, load_rules

RULES = load_rules(ROOT / "rules" / "v0.1.0.json")


def test_green_short_sourced():
    text = "Magellan HQ is in Mississauga. source: https://magellan.aero/contact/"
    r = gate(text, RULES)
    assert r.colour == "GREEN", r


def test_red_unsourced_hub():
    text = "Magellan is the Australian manufacturing hub with multi-facility presence in VIC."
    r = gate(text, RULES)
    assert r.colour == "RED", r
    assert any(f["rule_id"] == "R1_unsourced_hard_claim" for f in r.findings)


def test_yellow_filler():
    text = "Certainly, I would be happy to help you with that request about minerals."
    r = gate(text, RULES, session_used=0)
    assert r.colour in ("YELLOW", "ORANGE", "RED")
    assert any(f["rule_id"] == "R3_filler_opener" for f in r.findings)


def test_orange_long_draft():
    text = ("word " * 900).strip()  # ~900 tokens at 4 chars? word+space=5 → ~1125 tokens
    r = gate(text, RULES)
    assert r.colour == "ORANGE", (r.colour, r.estimated_draft_tokens)


def test_same_input_same_colour():
    text = "We verified that the Statement of Engagement will publicly verify the chain."
    a = gate(text, RULES)
    b = gate(text, RULES)
    assert a.colour == b.colour == "RED"


if __name__ == "__main__":
    tests = [
        test_green_short_sourced,
        test_red_unsourced_hub,
        test_yellow_filler,
        test_orange_long_draft,
        test_same_input_same_colour,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    raise SystemExit(failed)

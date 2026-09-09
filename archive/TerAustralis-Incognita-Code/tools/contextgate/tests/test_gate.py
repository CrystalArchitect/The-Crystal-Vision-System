#!/usr/bin/env python3
"""ContextGate v0.1.0 self-tests. Stdlib only — no network, no LLM.

Run: python3 tests/test_gate.py
"""

import os
import sys
import unittest

_TOOL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXAMPLES_DIR = os.path.join(_TOOL_DIR, "examples")
sys.path.insert(0, _TOOL_DIR)

from gate import evaluate, Verdict  # noqa: E402


def _read_example(name: str) -> str:
    with open(os.path.join(_EXAMPLES_DIR, name), "r", encoding="utf-8") as handle:
        return handle.read()


class ContextGateTests(unittest.TestCase):
    def test_bad_magellan_example_is_red(self):
        report = evaluate(_read_example("bad-magellan.txt"))
        self.assertEqual(report.verdict, Verdict.RED)
        rules_hit = {finding.rule for finding in report.findings}
        self.assertIn("positioning-needs-source", rules_hit)
        self.assertIn("quote-needs-source", rules_hit)
        self.assertIn("figure-needs-warrant-or-source", rules_hit)

    def test_good_sourced_example_is_green(self):
        report = evaluate(_read_example("good-sourced-brief.txt"))
        self.assertEqual(report.verdict, Verdict.GREEN)
        self.assertEqual(report.findings, [])

    def test_positioning_rule_flags_unsourced_hub_claim(self):
        report = evaluate("Foo Corp as the Tier 2 Hub for engines.")
        self.assertEqual(report.verdict, Verdict.RED)
        self.assertEqual(len(report.findings), 1)
        self.assertEqual(report.findings[0].rule, "positioning-needs-source")

    def test_positioning_rule_passes_when_sourced(self):
        report = evaluate(
            "Foo Corp as the Tier 2 Hub for engines (source: https://example.com/foo)."
        )
        self.assertEqual(report.verdict, Verdict.GREEN)
        self.assertEqual(report.findings, [])

    def test_human_override_forces_green_despite_violations(self):
        text = (
            "Foo Corp as the Tier 2 Hub for engines.\n"
            "[HUMAN-OVERRIDE: GREEN — Crystal reviewed and approved manually]\n"
        )
        report = evaluate(text)
        self.assertEqual(report.verdict, Verdict.GREEN)
        self.assertTrue(report.findings)  # rule findings are kept for the record
        self.assertIsNotNone(report.override)
        self.assertEqual(report.override[0], Verdict.GREEN)
        self.assertEqual(report.override[1], "Crystal reviewed and approved manually")


if __name__ == "__main__":
    unittest.main()

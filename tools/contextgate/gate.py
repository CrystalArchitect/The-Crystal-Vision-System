#!/usr/bin/env python3
"""ContextGate v0.1.0 — deterministic RED/GREEN gate for draft text.

No LLM call, no judgment call, no "looks fine to me." Same input produces
the same verdict every time, because the rules are fixed pattern checks,
not a model reading the text. What the rules are and why: see SURFACE.md
in this directory.

Usage:
    python3 gate.py <path-to-text-file>

Exit code is 0 for a final GREEN verdict, 1 for a final RED verdict (a
human override can force either regardless of what the rules found).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple


class Verdict(Enum):
    GREEN = "GREEN"
    RED = "RED"


# A role a draft assigns to a named entity — "X as Manufacturing Hub",
# "X as Tier 3", "X as Integration Anchor" — the exact positioning-claim
# shape used in the fabricated Small Council briefings caught in PR #146.
_ROLE_WORDS = (
    r"(?:manufacturing\s+)?hub"
    r"|(?:integration\s+)?anchor"
    r"|foundation"
    r"|endpoint"
    r"|tier\s*(?:[1-4]|one|two|three|four)"
)

POSITIONING_RE = re.compile(
    r"\b[A-Z][A-Za-z0-9&.'-]*(?:\s+[A-Z][A-Za-z0-9&.'-]*){0,3}\s+as\s+"
    r"(?:a\s+|an\s+|the\s+)?(?:[A-Za-z][\w-]*\s+){0,3}?(" + _ROLE_WORDS + r")\b",
    re.IGNORECASE,
)

# A styled quotation followed by a dash/paren/"said"-style attribution —
# the "closing lines styled as attributed company quotes" pattern from
# the same reconciliation.
QUOTE_ATTRIBUTION_RE = re.compile(
    r'"[^"]{3,}"\s*(?:[-—]{1,2}\s*[A-Z]|\(\s*[A-Z]|,?\s*said\b)',
    re.IGNORECASE,
)

# A specific dollar figure or percentage presented as a fact — the
# "invented ... staff-hour estimates, a cost-coverage promise" pattern.
BARE_NUMBER_RE = re.compile(
    r"\$\s?\d[\d,.]*\s?(?:million|billion|thousand|k|m|b)?\b"
    r"|\b\d{1,3}(?:\.\d+)?\s?%",
    re.IGNORECASE,
)

# Any of these on the same line is treated as evidence the claim is
# sourced. Deliberately loose — this is a formatting check, not a fact
# checker; see SURFACE.md non-goals.
SOURCE_MARKERS_RE = re.compile(
    r"https?://"
    r"|source\s*:"
    r"|(?<!\w)per\b"
    r"|\bconfirmed\b"
    r"|\bverified\b"
    r"|\bciting\b"
    r"|according to"
    r"|\[\d+\]"
    r"|\[\^"
    r"|\b(?:email|interview|transcript)\b",
    re.IGNORECASE,
)

# This project's own warrant-labelling covenant
# (mythos/teraustralis/publish/pathway-log-framework.md): [Fact],
# [Inference], [Assumption], [Vision].
WARRANT_LABEL_RE = re.compile(r"\[\s*(fact|inference|assumption|vision)\s*\]", re.IGNORECASE)

# A human override line, consumed whole and not treated as content:
#   [HUMAN-OVERRIDE: GREEN — Crystal reviewed and approved manually]
OVERRIDE_RE = re.compile(
    r"\[\s*HUMAN-OVERRIDE\s*:\s*(GREEN|RED)\s*(?:[-—]\s*(.*))?\]",
    re.IGNORECASE,
)

# Template scaffolding like "[Person/organization name, role, context]" —
# skipped so an empty template isn't mistaken for a claim. Distinguished
# from a warrant label by containing "/", "...", or " or " inside the
# brackets, which no warrant label does.
PLACEHOLDER_RE = re.compile(r"\[[^\]]*(?:/|\.\.\.| or )[^\]]*\]")


@dataclass
class Finding:
    rule: str
    line_no: int
    line: str
    reason: str


@dataclass
class Report:
    verdict: Verdict
    findings: List[Finding] = field(default_factory=list)
    override: Optional[Tuple[Verdict, str]] = None


def _is_checkable(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith("#"):
        return False
    return True


def check_positioning(line: str, line_no: int) -> Optional[Finding]:
    match = POSITIONING_RE.search(line)
    if not match:
        return None
    if SOURCE_MARKERS_RE.search(line):
        return None
    return Finding(
        rule="positioning-needs-source",
        line_no=line_no,
        line=line.strip(),
        reason=f"assigns a role ('{match.group(1)}') to a named entity with no source marker on the line",
    )


def check_quote_attribution(line: str, line_no: int) -> Optional[Finding]:
    if not QUOTE_ATTRIBUTION_RE.search(line):
        return None
    if SOURCE_MARKERS_RE.search(line):
        return None
    return Finding(
        rule="quote-needs-source",
        line_no=line_no,
        line=line.strip(),
        reason="attributes a quoted line to a named entity with no source marker",
    )


def check_bare_number(line: str, line_no: int) -> Optional[Finding]:
    if not BARE_NUMBER_RE.search(line):
        return None
    if SOURCE_MARKERS_RE.search(line) or WARRANT_LABEL_RE.search(line):
        return None
    return Finding(
        rule="figure-needs-warrant-or-source",
        line_no=line_no,
        line=line.strip(),
        reason="states a specific figure with neither a warrant label nor a source marker",
    )


RULES = (check_positioning, check_quote_attribution, check_bare_number)


def evaluate(text: str) -> Report:
    """Run all three rules over every checkable line. Deterministic:
    same text in, same Report out, every time — no state, no network,
    no model call."""
    findings: List[Finding] = []
    override: Optional[Tuple[Verdict, str]] = None

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        override_match = OVERRIDE_RE.search(raw_line)
        if override_match:
            verdict_word = override_match.group(1).upper()
            reason = (override_match.group(2) or "").strip() or "no reason given"
            override = (Verdict[verdict_word], reason)
            continue
        if not _is_checkable(raw_line):
            continue
        if PLACEHOLDER_RE.search(raw_line):
            continue
        for rule in RULES:
            finding = rule(raw_line, line_no)
            if finding:
                findings.append(finding)

    rule_verdict = Verdict.RED if findings else Verdict.GREEN
    verdict = override[0] if override else rule_verdict
    return Report(verdict=verdict, findings=findings, override=override)


def format_report(report: Report, source_name: str) -> str:
    lines = [f"ContextGate v0.1.0 — {source_name}"]
    rule_verdict = Verdict.RED if report.findings else Verdict.GREEN
    lines.append(f"rule verdict: {rule_verdict.value}")
    if report.findings:
        for finding in report.findings:
            lines.append(f"  [{finding.rule}] line {finding.line_no}: {finding.reason}")
            lines.append(f"    > {finding.line}")
    else:
        lines.append("  no violations")
    if report.override:
        forced, reason = report.override
        lines.append(f"HUMAN OVERRIDE -> {forced.value} ({reason})")
    lines.append(f"FINAL: {report.verdict.value}")
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    if len(argv) != 2:
        print("usage: gate.py <path-to-text-file>", file=sys.stderr)
        return 2
    path = argv[1]
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    report = evaluate(text)
    print(format_report(report, path))
    return 0 if report.verdict == Verdict.GREEN else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

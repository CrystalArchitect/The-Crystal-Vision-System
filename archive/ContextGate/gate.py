#!/usr/bin/env python3
"""ContextGate v0 — deterministic triage for AI drafts. No LLM at runtime."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_RULES = ROOT / "rules" / "v0.1.0.json"


@dataclass
class Finding:
    colour: str
    rule_id: str
    message: str
    evidence: str


@dataclass
class GateResult:
    colour: str
    rules_version: str
    findings: list
    estimated_draft_tokens: int
    next_step: str
    override_allowed_down: bool = False  # only operator may downgrade RED


PRIORITY = {"GREEN": 0, "YELLOW": 1, "ORANGE": 2, "RED": 3}

NEXT = {
    "RED": "Stop. Attach a source marker or mark the claim as hypothesis before shipping as Built.",
    "ORANGE": "Compress, split, or drop restatement before continue.",
    "YELLOW": "Trim filler opener; lead with the result.",
    "GREEN": "Passes v0 gate. May send.",
}


def load_rules(path: Path) -> dict:
    return json.loads(path.read_text())


def estimate_tokens(text: str, chars_per_token: float) -> int:
    return max(1, int(len(text) / chars_per_token)) if text.strip() else 0


def has_source(block: str, markers: list[str]) -> bool:
    lower = block.lower()
    return any(m.lower() in lower for m in markers)


def check_red(text: str, rules: dict) -> list[Finding]:
    findings: list[Finding] = []
    markers = rules["source_markers"]
    # Split into rough sentences
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    for part in parts:
        if not part.strip():
            continue
        for pat in rules["hard_claim_patterns"]:
            if re.search(pat, part, flags=re.IGNORECASE):
                if not has_source(part, markers) and not has_source(text, markers):
                    findings.append(
                        Finding(
                            "RED",
                            "R1_unsourced_hard_claim",
                            "Hard claim without source marker in draft.",
                            part[:200],
                        )
                    )
                    break
    return findings


def check_orange(text: str, rules: dict, session_used: int) -> list[Finding]:
    findings: list[Finding] = []
    draft_tok = estimate_tokens(text, rules["approx_chars_per_token"])
    if draft_tok > rules["max_draft_tokens"]:
        findings.append(
            Finding(
                "ORANGE",
                "R2_draft_over_max",
                f"Draft ~{draft_tok} tokens > max_draft_tokens={rules['max_draft_tokens']}.",
                f"draft_tokens={draft_tok}",
            )
        )
    window = rules["window_tokens"]
    budget = int(window * rules["budget_ratio"])
    total = session_used + draft_tok
    if total > budget:
        findings.append(
            Finding(
                "ORANGE",
                "R2_session_budget",
                f"Session used ({session_used}) + draft ({draft_tok}) > {budget} ({rules['budget_ratio']*100:.0f}% of {window}).",
                f"total={total} budget={budget}",
            )
        )
    return findings


def check_yellow(text: str, rules: dict) -> list[Finding]:
    findings: list[Finding] = []
    stripped = text.lstrip()
    lower = stripped.lower()
    for opener in rules["filler_openers"]:
        if lower.startswith(opener):
            findings.append(
                Finding(
                    "YELLOW",
                    "R3_filler_opener",
                    f"Opens with filler ({opener!r}).",
                    stripped.split("\n", 1)[0][:120],
                )
            )
            break
    return findings


def gate(text: str, rules: dict, session_used: int = 0) -> GateResult:
    findings = (
        check_red(text, rules)
        + check_orange(text, rules, session_used)
        + check_yellow(text, rules)
    )
    colour = "GREEN"
    for f in findings:
        if PRIORITY[f.colour] > PRIORITY[colour]:
            colour = f.colour
    draft_tok = estimate_tokens(text, rules["approx_chars_per_token"])
    return GateResult(
        colour=colour,
        rules_version=rules["rules_version"],
        findings=[asdict(f) for f in findings],
        estimated_draft_tokens=draft_tok,
        next_step=NEXT[colour],
        override_allowed_down=(colour == "RED"),
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="ContextGate — deterministic draft triage")
    p.add_argument("path", nargs="?", help="File to gate (default: stdin)")
    p.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    p.add_argument("--session-used", type=int, default=0, help="Tokens already in session")
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    args = p.parse_args(argv)

    if args.path:
        text = Path(args.path).read_text()
    else:
        text = sys.stdin.read()

    rules = load_rules(args.rules)
    result = gate(text, rules, session_used=args.session_used)

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"ContextGate {result.rules_version} → {result.colour}")
        print(f"Draft tokens ~{result.estimated_draft_tokens}")
        print(f"Next: {result.next_step}")
        for f in result.findings:
            print(f"  [{f['colour']}] {f['rule_id']}: {f['message']}")
            print(f"           evidence: {f['evidence']!r}")
    return 0 if result.colour == "GREEN" else PRIORITY[result.colour]


if __name__ == "__main__":
    raise SystemExit(main())

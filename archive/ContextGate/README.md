# ContextGate

Deterministic triage for AI drafts — context budgets, unsourced claims, filler.
Built product, not Vision. See `SURFACE.md`.

## Run

```bash
python3 gate.py examples/bad-magellan.txt
python3 gate.py examples/good-brief.txt
python3 gate.py --session-used 90000 examples/good-brief.txt
python3 tests/test_gate.py
```

Exit codes: 0 GREEN, 1 YELLOW, 2 ORANGE, 3 RED.

## Override

Downgrading RED is operator-only. Log the reason beside the original trigger. The gate itself never auto-downgrades.

# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Watch the RDP decision kernel work — every precedence tier, recorded.

    python3 -m rdp.run demo          # the decision kernel, all five tiers
    python3 -m rdp.run gate-demo     # the REAL ConsentGate, wrapped + witnessed
    python3 -m rdp.run matrix-demo   # the REAL Starline Weaver matrix mode, witnessed

`demo` runs five decisions, one per precedence tier plus a clean allow, printing
the verdict and which rule decided it. Each decision is written to a single
hash-chained record; at the end the chain is verified, and then one entry is
tampered with to show the verification catch it. Nothing here is simulated —
it calls the same `decide` and `record` code the tests cover.

`gate-demo` wires the *actual* CrystalBridge `ConsentGate` (not a stub) through
the `recording_gate` wrapper: the gate enforces, the wrapper witnesses. See
`gate_demo()` below.

`matrix-demo` wires the *actual* Starline Weaver (not a stub) in matrix mode —
one question, three built-in agents, independent answers — through
`record_matrix_result`: the Weaver asks and compares, RDP only witnesses. See
`matrix_demo()` below.
"""

from __future__ import annotations

import argparse

from .kernel import decide_and_record
from .record import new_chain, verify

# Five decision contexts, chosen so each precedence tier fires in turn.
CASES = [
    ("clean, low risk", {
        "risk": 0.1,
        "constraints": [{"id": "consent_present", "satisfied": True}],
    }),
    ("elevated risk", {
        "risk": [0.3, 0.3],  # factors sum to 0.6 → ELEVATED → HOLD
    }),
    ("single-source evidence", {
        "witnesses": [
            {"id": "w1", "source": "hub-a"},
            {"id": "w2", "source": "hub-a"},
        ],
    }),
    ("an unsatisfiable dilemma", {
        "options": ["keep_promise", "prevent_harm"],
        "obligations": [
            {"id": "promise", "satisfied_by": ["keep_promise"]},
            {"id": "safety", "satisfied_by": ["prevent_harm"]},
        ],
    }),
    ("a broken hard constraint", {
        "constraints": [{"id": "no_coercion", "satisfied": False}],
        "risk": 0.9,  # would be DENY on risk too, but the constraint decides first
    }),
]


def demo() -> None:
    chain = new_chain()
    print("RDP decision kernel — precedence: constraint > dilemma > bias > risk\n")
    for label, ctx in CASES:
        verdict = decide_and_record(chain, ctx)
        print(f"  {label:26} → {verdict['outcome']:8} [{verdict['rule']}]")
        print(f"  {'':26}   {verdict['reason']}")

    print(f"\nRecorded {len(chain)} verdicts to a hash-chained log.")
    ok, broken = verify(chain)
    print(f"verify() → intact={ok}" + ("" if ok else f", first break at {broken}"))

    print("\nNow tamper with the first recorded verdict's reason...")
    tampered = [dict(e) for e in chain]
    tampered[0]["reason"] = "quietly changed"
    ok, broken = verify(tampered)
    print(f"verify() → intact={ok}, first break at index {broken}")

    print("\nEvery verdict explains itself, and the record cannot be edited unseen.")
    print("Non Solus.")


def gate_demo() -> None:
    """Run the real CrystalBridge ConsentGate through the recording_gate wrapper.

    Unlike the stub in selftest.py, this imports and drives the *actual* gate —
    proof that the wiring is real, not a mock. The import is lazy (inside this
    function) and adds the repo root to sys.path, so `rdp.run demo` never has to
    touch CrystalBridge, and this subcommand works whether run from `crystal-core`
    or the repo root.
    """
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from crystalcore.config import BridgeConfig, GuestGrant
    from crystalcore.gate import ConsentGate

    from .adapters import recording_gate

    # An in-memory config: one approved guest, two granted tools. No files touched.
    config = BridgeConfig(
        profile="gate-demo",
        human_name="the architect",
        interactive_approval=False,
        guests={"hub-a": GuestGrant(approved=True, tools=["recall", "teach"])},
        profile_dir=repo_root / "profiles" / "gate-demo",  # never written: audit=False below
    )

    # A deterministic clock so the printed record is reproducible run-to-run.
    ticks = iter([f"2026-07-21T09:00:0{i}Z" for i in range(9)])

    chain = new_chain()
    gate = recording_gate(ConsentGate(config), chain, clock=lambda: next(ticks))

    print("CrystalBridge ConsentGate — enforced, then witnessed by RDP\n")
    print("  guest 'hub-a' is approved for tools: recall, teach (+ status)\n")

    # Three real checks. audit=False keeps the gate's own file-audit out of the
    # way — we're demonstrating the RDP record, not the gate's JSONL log.
    calls = [
        ("hub-a",    "recall", {"query": "who witnessed the dawn?"}),  # approved  → allow
        ("stranger", "recall", {"query": "let me in"}),                # unapproved → refuse
        ("hub-a",    "delete", {"target": "everything"}),              # no grant   → refuse
    ]
    for guest, tool, arguments in calls:
        result = gate.check(guest, tool, arguments, audit=False)
        event = chain[-1]
        mark = "✓" if result.allowed else "✗"
        print(f"  {mark} check({guest!r}, {tool!r}) → {result.decision.upper():7} — {result.reason}")
        print(f"      recorded: args_fingerprint={event['args_fingerprint'][:16]}…  ts={event['ts']}")

    print(f"\nRecorded {len(chain)} real gate decisions to a hash-chained log.")
    ok, broken = verify(chain)
    print(f"verify() → intact={ok}" + ("" if ok else f", first break at {broken}"))

    print("\nNow forge an approval onto the recorded refusal of 'stranger'...")
    tampered = [dict(e) for e in chain]
    tampered[1] = {**tampered[1], "decision": "allow", "allowed": True}
    ok, broken = verify(tampered)
    print(f"verify() → intact={ok}, first break at index {broken}")

    print("\nThe gate decided; RDP only remembered. The record is a ledger, not a lock.")
    print("Non Solus.")


def matrix_demo() -> None:
    """Run the *real* Starline Weaver matrix mode, recorded onto a real RDP chain.

    Unlike `demo()` (synthetic decision contexts) this imports and drives the
    actual `bus` package — proof the wiring is real, not a mock.
    The import is lazy (inside this function, with the repo root added to
    sys.path) so `rdp.run demo` never has to touch the bridge, and this
    subcommand works whether run from `crystal-core` or the repo root.
    """
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from bus.agents import BusHub, EchoAgent, SevenSistersAgent, UnlabeledAgent
    from bus.bus import StarlineWeaver

    from .adapters import record_matrix_result

    print("Starline Weaver matrix mode — witnessed by RDP\n")

    bus = StarlineWeaver(BusHub(), [EchoAgent(), SevenSistersAgent(), UnlabeledAgent()])
    question = "what is the Starline Weaver?"
    transcript = bus.run_matrix(question)
    compare = bus.cross_compare()

    for e in transcript:
        if e["cycle"] != 1:
            continue
        mark = "✓" if e["delivered"] else "✗"
        print(f"  {mark} {e['from']:>10} [{e['layer'] or '-'}] {e['content']}")

    print(f"\n  cross-compare: {compare['agents_delivered']}/{compare['agents_asked']} delivered, "
          f"layers={compare['layer_counts']}, unanimous={compare['layer_unanimous']}")

    chain = new_chain()
    responses = [e for e in transcript if e["cycle"] == 1]
    record_matrix_result(chain, question=question, responses=responses, compare=compare,
                          ts="2026-07-22T09:00:00Z")

    print(f"\nRecorded 1 matrix result ({len(responses)} responses) to a hash-chained log.")
    ok, broken = verify(chain)
    print(f"verify() → intact={ok}" + ("" if ok else f", first break at {broken}"))

    print("\nNow forge the rejected reply into a delivered one...")
    tampered = [dict(e) for e in chain]
    tampered[0] = {**tampered[0], "responses": [
        {**r, "delivered": True} if not r["delivered"] else r for r in responses
    ]}
    ok, broken = verify(tampered)
    print(f"verify() → intact={ok}, first break at index {broken}")

    print("\nThe Weaver asked and compared; RDP only remembered. The record is a ledger, not a lock.")
    print("Non Solus.")


def chain_inspect(path: str | None) -> int:
    """Load a hash-chained record (JSON list of events) from *path* or stdin,
    verify it, and print each event with a verdict. Read-only — a way to audit a
    chain someone hands you without trusting anything but the math.

        python3 -m rdp.run chain-inspect record.json
        cat record.json | python3 -m rdp.run chain-inspect
    """
    import json
    import sys

    raw = open(path, encoding="utf-8").read() if path else sys.stdin.read()
    chain = json.loads(raw)
    if not isinstance(chain, list):
        print("error: expected a JSON list of events (a chain)", file=sys.stderr)
        return 2

    source = path or "stdin"
    print(f"Loaded {len(chain)} event(s) from {source}\n")
    for i, event in enumerate(chain):
        if not isinstance(event, dict):
            print(f"  [{i}] (not an object — {type(event).__name__})")
            continue
        kind = event.get("kind", "?")
        digest = str(event.get("event_hash", ""))[:16]
        fields = ", ".join(
            f"{k}={event[k]!r}" for k in event if k not in ("kind", "event_hash")
        )
        print(f"  [{i}] {kind}  hash={digest}…")
        if fields:
            print(f"        {fields}")

    ok, broken = verify(chain)
    print(f"\nverify() → intact={ok}" + ("" if ok else f", first break at index {broken}"))
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="RDP decision kernel demo + tools")
    parser.add_argument(
        "command", choices=["demo", "gate-demo", "matrix-demo", "chain-inspect"], nargs="?", default="demo"
    )
    parser.add_argument(
        "path", nargs="?", default=None,
        help="chain-inspect: path to a chain JSON file (default: read stdin)",
    )
    args = parser.parse_args(argv)
    if args.command == "gate-demo":
        gate_demo()
        return 0
    if args.command == "matrix-demo":
        matrix_demo()
        return 0
    if args.command == "chain-inspect":
        return chain_inspect(args.path)
    demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# RDP and the consent gates — how they relate

**Read this if you've heard RDP called a "governance layer."** It isn't one, and
this doc is here to say so precisely, then show how RDP *does* relate to the
parts of the project that actually govern anything.

## What RDP is, and is not

RDP is a **record + decision kernel**:

- a canonical form (`canonical.py`) and a tamper-evident hash chain (`record.py`),
- a deterministic decision engine (`kernel.py`) that resolves a context to one
  explainable verdict through a fixed precedence order.

RDP is **not**:

- **not a consent enforcer.** It does not hold grants, check permissions, or
  block anything. It has no authority over any action.
- **not a governance layer.** It governs nothing. It decides — deterministically,
  when handed a context — and it records.

The things that *do* enforce consent in this project are already built, and they
are separate from RDP:

| Mechanism | Where | What it does |
|---|---|---|
| **CrystalBridge ConsentGate** | [`src/crystalcore/gate.py`](../../../src/crystalcore/gate.py) | Fail-closed gate; five doors in order — revocation → approval → provenance → permission → scope. Every decision audited ([`src/crystalcore/audit.py`](../../../src/crystalcore/audit.py)). |
| **Consent Transport consent** | [`consent_transport/consent.py`](../../../src/crystal-core/consent_transport/consent.py) | Signed `ConsentReceipt`s; `is_granted()`. Revocation stops *future* requests at once; it cannot retract data a peer already holds, and says so. |
| **The Covenant** | [`../../../mythos/COVENANT.md`](../../../mythos/COVENANT.md) | The five commitments those gates exist to keep. |

**These are separate modules today.** What follows is *correspondence* — how the
gates' logic lines up with RDP's — and possible future composition. It is **not**
a description of an existing wiring. Nothing currently feeds RDP from the gates.

## Why they correspond

The gates and RDP's kernel share a shape, because they answer the same kind of
question the same way: **legitimacy before prudence, and fail closed.**

- ConsentGate is fail-closed: any failing check refuses, and refusal is the
  default. That is exactly RDP's **tier 1** — a violated hard constraint ends the
  decision with `DENY`, and it outranks every softer consideration below it.
- The Covenant's absolute pause and "no influence without direction" are not
  risk trade-offs; they're hard limits. In RDP terms they are **constraints**, not
  risk inputs — a `HOLD`/`DENY` that no amount of low risk can override.
- "Support is offered, never imposed" is the shape of RDP's **`ESCALATE`/`HOLD`**:
  when acting unbidden would be overreach, the right move is to stop and hand the
  choice back, not to proceed.

So ConsentGate is, in effect, a concrete instance of RDP's constraint tier; a
Consent Transport grant/revocation is a signed record of the kind RDP's chain is built to
hold; the Covenant is the source of the constraints themselves.

## Worked examples

Each of these is real — run them yourself; the verdicts below are the actual
output of `rdp.kernel`, not illustrations.

**1 — a ConsentGate refusal (guest not approved).** The gate's failing `approval`
check becomes an unsatisfied constraint:

```python
from rdp.kernel import decide
decide({"constraints": [{"id": "gate.approval", "satisfied": False}]})
# → {'outcome': 'DENY', 'rule': 'constraint_violation', ...}
```

**2 — a Consent Transport request after revocation.** `is_granted() == False` is a
constraint violation:

```python
decide({"constraints": [{"id": "consent_transport.consent_granted", "satisfied": False}]})
# → {'outcome': 'DENY', 'rule': 'constraint_violation', ...}
```

**3 — a clean action, consent present, low risk.** No constraint broken, so the
decision falls through to the risk tier:

```python
decide({
    "constraints": [
        {"id": "gate.approval",                    "satisfied": True},
        {"id": "consent_transport.consent_granted", "satisfied": True},
    ],
    "risk": 0.1,
})
# → {'outcome': 'ALLOW', 'rule': 'risk_band', ...}
```

**Recording it.** Any of these can be written to a tamper-evident chain:

```python
from rdp.record import new_chain, verify
from rdp.kernel import decide_and_record

chain = new_chain()
decide_and_record(chain, {"constraints": [{"id": "gate.approval", "satisfied": False}]})
verify(chain)   # (True, -1) — intact; chain[0]["kind"] == "rdp.verdict"
```

## Wiring a real gate to the chain — the adapter

The correspondence above is now backed by a small, decoupled adapter:
[`adapters.py`](../../../src/crystal-core/rdp/adapters.py). It is the honest minimum — nothing in `gate.py` or
`consent.py` imports RDP, and `adapters.py` imports neither of them. The gate
enforces; afterwards it hands the *outcome* to the adapter to be witnessed.

**What gets written.** When a `ConsentGate.check()` returns a `GateResult`, the
adapter records one canonical event per decision:

```python
from rdp.record import new_chain, verify
from rdp.adapters import record_gate_decision

chain = new_chain()
result = gate.check(guest, tool, arguments)      # enforcement — unchanged, elsewhere
record_gate_decision(                            # witnessing — after the fact
    chain,
    guest=guest, tool=tool,
    decision=result.decision, allowed=result.allowed, reason=result.reason,
    arguments=arguments, ts="2026-07-21T10:00:00Z",
)
# chain[-1] == {"kind": "consent.gate.decision", "guest", "tool", "decision",
#               "allowed", "reason", "args_fingerprint", "ts", "event_hash"}
verify(chain)   # (True, -1) — and it pinpoints the first tampered decision if not
```

The **arguments are stored as a fingerprint** (`sha256_hex` of the canonical
arguments), never the raw payload — so a consent input that carries sensitive
data doesn't leak into the ledger, while anyone holding the original arguments
can still prove they match.

**A wrapper, and a runnable demo with the real gate.** For the common case there's
[`recording_gate`](../../../src/crystal-core/rdp/adapters.py) — a thin, duck-typed wrapper around *any* gate
whose `check()` returns a `GateResult`-shaped object. It calls the wrapped gate
first (enforcement, unchanged), then records the outcome *after* the result
exists; if the gate raises, nothing is recorded. Timestamps come from an injected
`clock` so the canonical record stays reproducible. To watch it drive the **real**
CrystalBridge `ConsentGate` — an approved allow, an unapproved refuse, a
no-permission refuse, then a verified chain and a caught tamper:

```
python3 -m rdp.run gate-demo
```

That subcommand imports `crystalcore.gate.ConsentGate` for real (lazily, so
`rdp.run demo` stays dependency-free); it is *not* a stub. The one-line reminder
it prints is the whole point: **the gate decided; RDP only remembered.**

**Keeping the separation clean.** The adapter is called *after* the gate decides
and can never sit between the gate and its verdict. If recording failed
entirely, the allow/deny would stand unchanged — RDP is the ledger, not the lock.
That's the whole design: two policies are available depending on how strong a
guarantee you want —

- *Best-effort audit* (what the adapter does): record after enforcing; a record
  failure is logged, not fatal. The gate stays independent.
- *Mandatory witness* ("no action without a recorded decision"): append first and
  treat an append failure as a refuse. Stronger, but it couples the two — a
  deliberate choice, not the default. This is now real too: `witnessing_gate`
  (sibling of `recording_gate`) lets the gate decide, records the decision, and if
  that record **fails**, downgrades the verdict to a fail-closed refusal — so no
  allow ever stands unwitnessed. The ledger is deliberately in the critical path;
  use it only when you want that trade-off.

**Recording Starline consent, not just gate decisions.** A signed
`ConsentReceipt` (grant *or* revoke) records the same way, via
`record_consent_receipt(chain, receipt)`. It is duck-typed (no Starline import),
the signature rides canonicalization untouched, and the chain then holds a
tamper-evident, ordered proof of the exact grant→revoke history for a peer.

**Auditing a chain someone hands you.** `python3 -m rdp.run chain-inspect
record.json` (or piped via stdin) loads a chain, prints each event, and runs
`verify()` — exiting non-zero and pointing at the first broken index if the
record was disturbed. Read-only; it trusts nothing but the hashes.

**Recording a Starline Weaver matrix result.** The Weaver's matrix mode
(`bus.bus.StarlineWeaver.run_matrix()` — one question, every
agent independently, no agent sees another's reply) produces a transcript and
a `cross_compare()` summary that are exactly the kind of thing RDP exists to
witness: a permanent, tamper-evident record of what was asked, what each
independent voice said, and whether they agreed. `record_matrix_result(chain,
question=..., responses=..., compare=...)` records the same way the gate
decisions do — after the fact, one canonical event, nothing here decides
anything. Unlike gate arguments, response *content* is stored in full, not
fingerprinted: the whole point of witnessing a matrix run is being able to
read back what each agent actually said, and a hash alone can't do that. To
watch it drive the **real** Starline Weaver — three built-in agents answering
independently, a delivered/rejected/delivered mix, a cross-compare, a verified
chain, and a caught tamper:

```
python3 -m rdp.run matrix-demo
```

That subcommand imports `bus` for real (lazily, so `rdp.run
demo` stays dependency-free); it is *not* a stub. Same reminder as the gate
demo, same reason: **the Weaver asked and compared; RDP only remembered.**
Nothing here — not RDP, not the adapter — judges which agent's answer was
right. `cross_compare()`'s layer-agreement count already refuses to do that;
recording it doesn't change that refusal into a verdict.

**Edge cases that matter once real consent events flow:**

- **Numeric precision.** The RDP-JCS profile quantizes numbers to 6 decimals, so
  the `args_fingerprint` collapses differences below 1e-6. Fine for string/ID
  arguments; if an argument carries values that must be bit-exact, pass your own
  `args_fingerprint` computed with a non-quantizing serialization.
- **JSON-only inputs.** Canonicalization rejects non-string keys and non-JSON
  types (`bytes`, `datetime`, …). Normalize arguments to JSON-safe values before
  recording, or `gate_event` will raise — which is honest, but must be handled.
- **Concurrency.** The chain is linear and `append` reads-the-tip-then-writes, so
  it is **not** thread-safe. Serialize appends (one writer, or a lock) when a live
  gate is deciding concurrently, or the tip will race.
- **Timestamps are data, supplied by the caller** — the adapter never generates
  them, so the canonical form stays deterministic and reproducible.
- **Revocation.** A Starline `ConsentReceipt` (signed grant *or* revoke) records
  the same way; the signature is a string and rides through canonicalization
  untouched, so the chain proves the exact grant→revoke sequence.

There is no "governance," no "firewall," and no mythic framing in any of this.
RDP records and decides; the gates enforce; the Covenant is the law they keep.

---

*Non Solus.*

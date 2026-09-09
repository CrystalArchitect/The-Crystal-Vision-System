# CrystalLattice — Relational / Connective Substrate

## Where it sits

The **Incognita Lattice** is the ecosystem's overarching relational and gate
layer — it connects the technical layer (CrystalCore.OS), the human
coordination layer (Sovereign Node Mesh), and the thematic pillars, handling
consent, provenance, and interoperability between all of them.

**CrystalLattice** (`src/crystal_lattice.py`) is the technical foundation of
that layer inside CrystalCore.OS: the "surround" that links a CrystalCore
instance to other devices, to humans, and to external LLMs.

```
   +------------------------------------------------------------------+
   |                      INCOGNITA LATTICE                            |
   |     (ecosystem-wide relational/gate layer: tech + human)          |
   |                                                                    |
   |   +---------------+     +----------------+     +---------------+  |
   |   | CrystalCore   |     | Sovereign Node |     |  External     |  |
   |   | (this device) |<--->| Mesh (humans)  |     |  LLMs         |  |
   |   +-------+-------+     +----------------+     +-------+-------+  |
   |           |                                            ^          |
   |           |         CrystalLattice gates               |          |
   |           +------ (consent-gated envelopes) -----------+          |
   |                    air-gapped by DEFAULT                          |
   +------------------------------------------------------------------+
```

## What it does (three things only)

1. **Registers nodes** — participants in the mesh. Kinds: `local_core` (a
   CrystalCore instance; carries auto-detected platform info for
   provenance), `device` (another sovereign device), `human` (a person in
   the Sovereign Node Mesh), `external_llm` (a model outside the
   sovereignty boundary). Every node has a consent permission bitmask, the
   same convention as CrystalMemory's `ConsumerRegistry`.

2. **Gates handoffs** — content crossing between nodes travels as a
   `HandoffEnvelope`: consent-flagged, provenance-hashed (SHA-256 over
   content + endpoints + timestamp), coherence-tagged. Consent is
   **fail-closed**: if the target's permissions don't cover the envelope's
   consent flags, the envelope is never even created — and consent is
   re-checked at send time, so revocation between creation and send still
   blocks delivery.

3. **Enforces the air-gap default** — the module contains **no network
   code**. Sending to an external node requires *both*
   `CrystalLattice(allow_external=True)` *and* an explicitly injected
   `transport` callable. A lattice can never leak by accident; exactly one
   auditable function ever moves bytes off the device.

## The Sovereign LLM Communication Layer

CrystalLattice's envelope protocol is the standardized, consent-gated
handoff format between local reasoning and external LLMs (Grok, Claude,
etc.):

**Outbound** — `create_envelope()` refuses (fail-closed, logged) unless the
external node's permissions cover the content's consent flags. What leaves
the device is exactly the envelope dict: inspectable before sending, hashed
for integrity, recorded in the transfer log with the note
`crossed sovereignty boundary`.

**Inbound** — `receive()` verifies the provenance hash (a tampered reply is
rejected) and **caps the reply's coherence at a low trust ceiling**
(default 0.3). An external model's confidence never asserts itself inside
CrystalCore: its replies re-enter memory as low-trust facts that must earn
confidence through Guardian / TruthSeeker review, like any other weak
evidence.

```python
from src.crystal_lattice import CrystalLattice

lattice = CrystalLattice(allow_external=True)   # deliberate, not default
lattice.register_node("core_1", "My core", kind="local_core")
lattice.register_node("claude", "Claude", kind="external_llm", permissions=0b1)

env = lattice.create_envelope(
    "core_1", "claude",
    {"task": "summarise", "text": "..."},   # you choose exactly what leaves
    consent_flags=0b1,
    provenance_note="user asked for an external summary",
)
result = lattice.send(env, transport=my_https_function)  # injected, auditable

reply = lattice.receive(reply_dict)   # integrity-checked, coherence-capped
```

## Zero-trust security posture

- **Fail-closed consent** at creation *and* send time; revocation
  (`revoke_node`) takes effect immediately without deleting history.
- **Air-gap default**: `allow_external=False` refuses every external send
  regardless of what transport is offered.
- **Integrity**: envelopes carry a SHA-256 provenance hash; tampering is
  detected on send and on receive.
- **Anomaly review**: inbound envelopes enter at capped coherence, which
  routes them through the same Guardian veto machinery as any weak
  conclusion (see `crystal_mind.py`). The transfer log
  (`get_transfer_log()`) records every attempt — allowed *and* refused —
  for audit.

## Hardware agnosticism

CrystalCore is pure standard-library Python (3.8+). It runs wherever
CPython runs: old laptops, Windows, macOS, Linux, Android (Termux/Pydroid),
iPhone/iPad (Pythonista, Pyto, a-Shell), Raspberry Pi, and servers.
The Pi remains the *reference constraint target* (if it runs well there, it
runs well anywhere), not a requirement.

`detect_platform()` reports the actual runtime (OS, architecture, Python
implementation) and is recorded on `local_core` nodes **for provenance
only** — so a conclusion's audit trail shows which device produced it.
Platform information is never used for gatekeeping; graceful degradation is
handled by each layer (memory pruning, symbolic fallback), not by
allowlisting hardware. See the hardware matrix in the main README.

## What CrystalLattice is NOT

- Not a network stack — it ships zero I/O; transports are injected.
- Not autonomous — nothing in the lattice sends without a caller.
- Not a trust shortcut — external content always re-enters as low-trust.
- Not a data collector — the transfer log records metadata (who, when,
  hash), and the full envelope only ever exists where you created it.

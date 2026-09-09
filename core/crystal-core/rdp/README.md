# Reciprocal Dawn Protocol (RDP) — the record + decision kernel
## A tamper-evident log, a reproducible canonical form, and an explainable decision engine

**Status:** BUILT · v0.2 · record layer + decision kernel (see *What's here / not here*)
**Layer:** Science — running, tested code. Run the proof yourself below.

---

## What this is

RDP is the part of the protocol pack that answers one question: *how do you keep
a record that no one — not even the person holding it — can quietly rewrite?*

The answer is old and boring and works: hash each entry together with the hash
of the one before it. Change any past entry and every hash downstream stops
matching, so the tampering is obvious to anyone who re-checks the math. There is
no authority to trust; the chain checks itself.

The one hard part is agreement on *bytes*. Two parties who serialize the same
event differently compute different hashes and think each other's records are
forged. So RDP pins a **canonical JSON** form — same event, same bytes, on any
machine, in any language.

## An honest note on "conformance"

An earlier RDP handoff described a frozen reference kernel and a conformance
fixture suite to match. Those files never actually existed — only the prose did.
So this is **not** "conformant to an external frozen suite," because there isn't
one. It is a correct, self-contained implementation whose own
[`selftest.py`](selftest.py) is the ground truth. Where the underlying standard
(RFC 8785 / JCS) is precise, we follow it; the number handling is our own
stated profile, below. We'd rather say that plainly than imply a pedigree that
isn't there.

## The link rule

```
EventHash = SHA256( canonical(Event \ event_hash) || PrevHashBytes )
```

- `canonical(...)` — the event's canonical JSON (below), UTF-8 encoded, with the
  event's own `event_hash` field removed first (an entry can't commit to its own
  hash).
- `PrevHashBytes` — the 32 raw bytes of the previous entry's hash.
- The first entry links to **genesis**: 32 zero bytes.

A chain is just a list of plain dicts, each with an `event_hash` hex string. It's
ordinary JSON once written out; the integrity is in the hashes, not the storage.

## RDP-JCS Profile v1 (the canonical form)

Standard JSON canonicalization, plus one deliberate profile for numbers — call
it **decimal-6**:

| Rule | |
|------|--|
| Object keys | sorted (by Unicode code point) |
| Arrays | left in order |
| Strings | standard JSON escaping, UTF-8 passed through |
| Whitespace | none that isn't significant |
| **Numbers** | quantized to exactly **6 fractional digits**, halves rounded **away from zero**, rendered **unquoted** |
| Rejected | `NaN`, `±Infinity`, and any magnitude `> 2**53 − 1` |

So `1` serializes as `1.000000`, `0.5` as `0.500000`, and `{"b":1,"a":2}` as
`{"a":2.000000,"b":1.000000}`. The `2**53 − 1` ceiling is the largest integer a
double holds exactly — beyond it we can't guarantee another language's JSON
parser reproduces the value, so the profile refuses to record it.

(Key sorting follows Unicode code point rather than JCS's UTF-16 code-unit order.
The two differ only for characters outside the Basic Multilingual Plane; for the
ASCII-ish keys these records use they are identical. This is a stated choice of
the profile, not an oversight.)

## Run the proof

```bash
cd crystal-core
python3 -m rdp.selftest
```

Twenty-five tests, no dependencies (standard library only). They pin the
empty-string SHA-256 as a fixed anchor, check the canonical form against the
rules above, prove the chain both verifies a clean log and pinpoints the first
tampered entry in a dirty one, and exercise every tier of the decision kernel
below. That total includes seven **property checks** — seeded generation
(stdlib `random`, no external dependency) that runs each invariant over hundreds
of random inputs: precedence dominance, risk monotonicity, `decide` purity,
canonical key-order independence, and single-mutation chain detection. Fixed
seeds keep them reproducible; it's broad invariant coverage, not full
shrinking-search.

Watch the decision kernel run, one verdict per precedence tier, all recorded:

```bash
python3 -m rdp.run demo
```

## Interop: conformance vectors

If a second implementation (another language, another codebase) is going to
share a chain with this one, the two must agree on the canonical bytes exactly —
otherwise their hashes diverge and neither can verify the other's record.

[`vectors.json`](vectors.json) is the **authoritative, language-neutral
definition** of the canonical form. Each entry gives a raw-JSON input, the exact
canonical string it must serialize to, and that string's SHA-256:

| input | canonical | sha256 |
|---|---|---|
| `1` | `1.000000` | `b42a73…` |
| `{"b":1,"a":2,"c":3}` | `{"a":2.000000,"b":1.000000,"c":3.000000}` | `7deaf8…` |
| `{"kind":"grant","subject":"did:crystal:a","amount":12.5}` | `{"amount":12.500000,"kind":"grant","subject":"did:crystal:a"}` | `96aef8…` |

An implementation is conformant **iff** it reproduces every `canonical` string
and `sha256` in that file. Note the consequence of the fixed-6-dp, unquoted rule:
a renderer that strips trailing zeros (`12.5` → `12.5` instead of `12.500000`)
fails these vectors *by design* — that's the point of pinning them. `vectors.json`
is checked against the code on every CI run (see `selftest.py`), so it can never
quietly drift from the implementation.

## Using it

```python
from rdp.record import new_chain, append, verify

chain = new_chain()
append(chain, {"kind": "grant",  "subject": "did:crystal:a"})
append(chain, {"kind": "revoke", "subject": "did:crystal:a"})

ok, broken_at = verify(chain)   # (True, -1) when intact;
                                # (False, i) at the first disturbed entry
```

## The decision kernel

The record layer proves *what* was decided. The decision kernel (`kernel.py`) is
about *how* a verdict is reached — deterministically, and always for a reason you
can name. It never blends everything into one opaque score; it runs four checks
in a fixed order of authority and returns the first that fires:

| Tier | Check | Fires when | Verdict |
|---|---|---|---|
| 1 | **Constraint violation** | a hard rule is broken | `DENY` |
| 2 | **Unsatisfiable ∧ dilemma** | obligations conflict and can't all be met | `ESCALATE` |
| 3 | **Witness bias** | evidence isn't independently trustworthy | `REVIEW` |
| 4 | **Risk band** | nothing above fired — judge by risk | `ALLOW` / `HOLD` / `DENY` |

The order *is* the design: higher tiers ask *may we act at all?* (legitimacy),
lower tiers ask *how much do we trust this?* (prudence), and legitimacy wins.
Risk bands over a `[0,1]` score: `LOW`/`GUARDED` → `ALLOW`, `ELEVATED` → `HOLD`,
`SEVERE` → `DENY` (boundaries `0.25 / 0.50 / 0.75` belong to the higher band).

```python
from rdp.record import new_chain
from rdp.kernel import decide, decide_and_record

decide({"constraints": [{"id": "no_coercion", "satisfied": False}]})
# {'outcome': 'DENY', 'rule': 'constraint_violation', 'reason': ..., 'details': ...}

chain = new_chain()
decide_and_record(chain, {"risk": 0.6})   # verdict returned AND appended to the
                                          # chain, stamped with the decision's hash
```

As with the canonical form, there is no external reference for this precedence —
the RDP handoff described it in prose only. So it's a faithful, self-contained
interpretation, and `selftest.py` is its ground truth (including a test that a
context tripping *every* tier returns the highest, then the next as each is
removed — proving the ordering is strict).

## Where RDP sits in the pack

RDP is a **record + decision** layer — it reaches a verdict deterministically and
proves *what was decided, why, and in what order*. It does **not** replace the
pack's consent machinery, and shouldn't be read as doing so:

- **Consent** still lives in Starline's `consent.py` (`core/crystal-core/consent_transport/`)
  and CrystalBridge's fail-closed ConsentGate (`core/crystalcore/`) — nothing moves
  without a grant.
- **The Covenant** (`mythos/COVENANT.md`) is still the law those gates enforce.

RDP's job is to be the ledger they can write to and later prove wasn't edited.
For how the kernel's precedence lines up with those gates — with worked examples,
and an honest note that they are separate modules today — see
[`RDP-INTEGRATION.md`](../../../docs/architecture/crystal-core/RDP-INTEGRATION.md).

## What's here / not here

**Here (v0.2):** the canonical form (`canonical.py`), the hash chain
(`record.py`), the language-neutral conformance vectors (`vectors.json`), and the
decision kernel (`kernel.py`) with its demo (`run.py`) — all with real tests.

**Not here yet:** a document mapping RDP onto the pack's real consent mechanisms
(Starline consent, CrystalBridge's ConsentGate, the Covenant) with worked
examples, and richer constraint/obligation modelling beyond the pre-evaluated
inputs the kernel takes today. Those build on this foundation in a later pass.
This README only claims what the code actually does.

---

*Non Solus.*

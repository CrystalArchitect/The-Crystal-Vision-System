# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Self-test for RDP — canonical JSON, the hash chain, and the decision kernel.

    python3 -m rdp.selftest

These tests *are* the specification. There is no external conformance suite for
RDP — the handoff that described one referred to reference files that never
existed — so correctness here means: the canonical form is deterministic and
matches the profile's stated rules, the hash chain detects any tampering, and
the decision kernel resolves every context through its fixed precedence order.
The empty-string SHA-256 is pinned as a fixed anchor so the hash primitive
itself can't drift underneath us.
"""

from __future__ import annotations

import json
import random
from decimal import Decimal
from pathlib import Path

from .canonical import (
    MAX_MAGNITUDE,
    canonical_serialize,
    quantize6,
    render_number,
    sha256_hex,
)
from .record import (
    GENESIS_PREV,
    append,
    compute_event_hash,
    new_chain,
    tip_bytes,
    verify,
)
from .kernel import (
    ALLOW,
    DENY,
    ESCALATE,
    HOLD,
    REVIEW,
    RULE_BIAS,
    RULE_CONSTRAINT,
    RULE_DILEMMA,
    RULE_RISK,
    decide,
    decide_and_record,
    risk_band,
    risk_score,
    satisfiability,
    witness_bias,
)

# SHA-256 of the empty string — a value anyone can look up. If this ever fails,
# the hashing itself is wrong, not the protocol.
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def _raises(exc, fn, *args) -> bool:
    try:
        fn(*args)
    except exc:
        return True
    return False


def test_empty_string_sha256_anchor():
    assert sha256_hex("") == EMPTY_SHA256
    assert sha256_hex(b"") == EMPTY_SHA256


def test_object_keys_are_sorted():
    assert canonical_serialize({"b": 1, "a": 2}) == '{"a":2.000000,"b":1.000000}'
    # insertion order must not matter
    one = canonical_serialize({"a": 1, "b": 2, "c": 3})
    two = canonical_serialize({"c": 3, "b": 2, "a": 1})
    assert one == two == '{"a":1.000000,"b":2.000000,"c":3.000000}'


def test_number_rendering():
    assert render_number(1) == "1.000000"
    assert render_number(0.5) == "0.500000"
    assert render_number(Decimal("0.5")) == "0.500000"
    # halves round away from zero
    assert render_number(Decimal("0.0000005")) == "0.000001"
    assert render_number(Decimal("-0.0000005")) == "-0.000001"
    # negative zero collapses to the single canonical zero
    assert render_number(Decimal("-0")) == "0.000000"
    assert render_number(-0.0) == "0.000000"
    # the largest allowed magnitude renders in plain (non-exponent) form
    assert render_number(MAX_MAGNITUDE) == "9007199254740991.000000"


def test_quantize6_rejects_unrepresentable():
    assert _raises(ValueError, quantize6, float("nan"))
    assert _raises(ValueError, quantize6, float("inf"))
    assert _raises(ValueError, quantize6, Decimal("NaN"))
    assert _raises(ValueError, quantize6, Decimal("Infinity"))
    assert _raises(ValueError, quantize6, MAX_MAGNITUDE + 1)          # 2**53
    assert _raises(ValueError, quantize6, -(MAX_MAGNITUDE + 1))
    # the boundary value itself is allowed
    assert quantize6(MAX_MAGNITUDE) == Decimal("9007199254740991.000000")


def test_booleans_and_null_are_not_numbers():
    assert canonical_serialize(True) == "true"
    assert canonical_serialize(False) == "false"
    assert canonical_serialize(None) == "null"
    assert canonical_serialize({"ok": True, "n": None}) == '{"n":null,"ok":true}'


def test_nested_structure_is_canonical():
    obj = {"z": [3, 1, 2], "a": {"n": None, "m": "hi"}}
    assert canonical_serialize(obj) == (
        '{"a":{"m":"hi","n":null},"z":[3.000000,1.000000,2.000000]}'
    )


def test_genesis_link():
    chain = new_chain()
    assert tip_bytes(chain) == GENESIS_PREV
    stamped = append(chain, {"kind": "grant", "subject": "did:crystal:a"})
    # the first event must link to the 32-zero genesis previous-hash
    body = {"kind": "grant", "subject": "did:crystal:a"}
    assert stamped["event_hash"] == compute_event_hash(body, GENESIS_PREV).hex()


def test_append_does_not_mutate_caller_and_ignores_incoming_hash():
    chain = new_chain()
    original = {"kind": "grant", "event_hash": "deadbeef"}
    stamped = append(chain, original)
    # caller's dict untouched
    assert original["event_hash"] == "deadbeef"
    # stored hash is the real computed one, not the incoming placeholder
    assert stamped["event_hash"] != "deadbeef"
    ok, broken = verify(chain)
    assert ok and broken == -1


def test_chain_verifies_and_detects_tampering():
    chain = new_chain()
    for i in range(3):
        append(chain, {"kind": "note", "n": i})
    ok, broken = verify(chain)
    assert ok and broken == -1

    # tamper with the *content* of the middle event
    tampered = [dict(e) for e in chain]
    tampered[1]["n"] = 99
    ok, broken = verify(tampered)
    assert not ok and broken == 1

    # tamper with only the *stored hash* of the first event
    tampered2 = [dict(e) for e in chain]
    tampered2[0]["event_hash"] = "00" * 32
    ok, broken = verify(tampered2)
    assert not ok and broken == 0


def test_conformance_vectors():
    """vectors.json is the language-neutral interop contract — every entry must
    match the code exactly, so the published file can never drift from it."""
    path = Path(__file__).with_name("vectors.json")
    doc = json.loads(path.read_text(encoding="utf-8"))
    vectors = doc["vectors"]
    assert vectors, "vectors.json must not be empty"
    for v in vectors:
        obj = json.loads(v["input_json"], parse_float=Decimal, parse_int=int)
        got = canonical_serialize(obj)
        assert got == v["canonical"], (v["note"], got, v["canonical"])
        assert sha256_hex(got) == v["sha256"], (v["note"], sha256_hex(got))


# --- decision kernel -------------------------------------------------------

def test_risk_bands_and_boundaries():
    assert risk_band(0.0) == "LOW"
    assert risk_band(0.24) == "LOW"
    assert risk_band(0.25) == "GUARDED"      # boundary belongs to the higher band
    assert risk_band(0.5) == "ELEVATED"
    assert risk_band(0.75) == "SEVERE"
    assert risk_band(1.0) == "SEVERE"
    assert _raises(ValueError, risk_band, -0.1)
    assert _raises(ValueError, risk_band, 1.1)


def test_risk_score_normalization():
    assert risk_score(0.4) == 0.4
    assert risk_score([0.2, 0.3, 0.1]) == 0.6      # factors sum
    assert risk_score([0.9, 0.9]) == 1.0           # clamped to 1
    assert risk_score(-5) == 0.0                    # clamped to 0
    assert _raises(TypeError, risk_score, True)     # bool is not a risk number
    assert _raises(TypeError, risk_score, "high")


def test_satisfiability_and_dilemma():
    # a true dilemma: each obligation is met by some option, none by both
    sat, dil = satisfiability(["a", "b"], [
        {"id": "keep_promise", "satisfied_by": ["a"]},
        {"id": "prevent_harm", "satisfied_by": ["b"]},
    ])
    assert sat is False and dil is True
    # satisfiable: option 'a' meets both
    sat, dil = satisfiability(["a", "b"], [
        {"id": "x", "satisfied_by": ["a"]},
        {"id": "y", "satisfied_by": ["a", "b"]},
    ])
    assert sat is True and dil is False
    # an impossible single obligation is unsatisfiable but NOT a dilemma
    sat, dil = satisfiability(["a"], [{"id": "z", "satisfied_by": ["nonexistent"]}])
    assert sat is False and dil is False
    # no obligations at all is trivially satisfiable
    assert satisfiability(["a"], []) == (True, False)


def test_witness_bias_detection():
    assert witness_bias([]) == []
    assert witness_bias([{"id": "w1", "source": "a"}]) == []      # lone witness, no flag
    assert witness_bias([{"id": "w1", "source": "a", "biased": True}]) == ["flagged:w1"]
    # two witnesses, one source = monoculture
    reasons = witness_bias([{"id": "w1", "source": "a"}, {"id": "w2", "source": "a"}])
    assert reasons == ["single_source:a"]
    # independent sources = clean
    assert witness_bias([{"id": "w1", "source": "a"}, {"id": "w2", "source": "b"}]) == []


def test_decide_each_tier_in_isolation():
    # tier 1 — constraint violation
    v = decide({"constraints": [{"id": "no_coercion", "satisfied": False}]})
    assert v["outcome"] == DENY and v["rule"] == RULE_CONSTRAINT

    # tier 2 — unsatisfiable dilemma
    v = decide({"options": ["a", "b"], "obligations": [
        {"id": "p", "satisfied_by": ["a"]},
        {"id": "q", "satisfied_by": ["b"]},
    ]})
    assert v["outcome"] == ESCALATE and v["rule"] == RULE_DILEMMA

    # tier 3 — witness bias
    v = decide({"witnesses": [
        {"id": "w1", "source": "a"}, {"id": "w2", "source": "a"},
    ]})
    assert v["outcome"] == REVIEW and v["rule"] == RULE_BIAS

    # tier 4 — risk band, low and severe
    assert decide({"risk": 0.1})["outcome"] == ALLOW
    assert decide({"risk": 0.6})["outcome"] == HOLD
    assert decide({"risk": 0.9})["outcome"] == DENY
    assert decide({})["outcome"] == ALLOW              # empty context = zero-risk allow


def test_decide_precedence_is_strict():
    """A context that trips every tier must return the highest one, and peeling
    off each top tier reveals the next in exact order."""
    ctx = {
        "constraints": [{"id": "no_coercion", "satisfied": False}],
        "options": ["a", "b"],
        "obligations": [
            {"id": "p", "satisfied_by": ["a"]},
            {"id": "q", "satisfied_by": ["b"]},
        ],
        "witnesses": [{"id": "w1", "source": "a"}, {"id": "w2", "source": "a"}],
        "risk": 0.9,
    }
    assert decide(ctx)["rule"] == RULE_CONSTRAINT          # constraint wins over all
    ctx = {**ctx, "constraints": []}
    assert decide(ctx)["rule"] == RULE_DILEMMA             # then the dilemma
    ctx = {**ctx, "obligations": []}
    assert decide(ctx)["rule"] == RULE_BIAS                # then witness bias
    ctx = {**ctx, "witnesses": []}
    assert decide(ctx)["rule"] == RULE_RISK                # finally risk
    assert decide(ctx)["outcome"] == DENY                 # risk 0.9 → SEVERE → DENY


def test_decide_and_record_is_tamper_evident():
    chain = new_chain()
    decision = {"risk": 0.1, "constraints": [{"id": "ok", "satisfied": True}]}
    verdict = decide_and_record(chain, decision)
    assert verdict["outcome"] == ALLOW
    assert len(chain) == 1
    event = chain[0]
    assert event["kind"] == "rdp.verdict"
    # the recorded decision hash matches the canonical hash of the exact input
    assert event["decision_sha256"] == sha256_hex(decision)
    ok, broken = verify(chain)
    assert ok and broken == -1
    # editing the recorded reason breaks the chain
    tampered = [dict(e) for e in chain]
    tampered[0]["reason"] = "something else"
    ok, broken = verify(tampered)
    assert not ok and broken == 0


# --- property checks -------------------------------------------------------
# Seeded generation over the real code — no Hypothesis dependency, so RDP stays
# standard-library-only. Fixed seeds keep these reproducible, never flaky. This
# is invariant coverage over many generated inputs, not full shrinking search.

_ITER = 300


def _rand_scalar(rng: random.Random):
    return rng.choice([
        rng.randint(-10000, 10000),
        round(rng.uniform(-1000, 1000), rng.randint(0, 6)),
        rng.choice([True, False]),
        None,
        rng.choice(["", "a", "hi", "did:crystal:x", "spark é"]),
    ])


def _rand_json(rng: random.Random, depth: int = 0):
    if depth >= 3 or rng.random() < 0.5:
        return _rand_scalar(rng)
    if rng.random() < 0.5:
        return [_rand_json(rng, depth + 1) for _ in range(rng.randint(0, 4))]
    keys = rng.sample(["a", "b", "c", "d", "e", "f", "g"], rng.randint(0, 5))
    return {k: _rand_json(rng, depth + 1) for k in keys}


def _shuffle_keys(rng: random.Random, obj):
    """A structurally-identical copy with every dict's key order randomized."""
    if isinstance(obj, dict):
        items = list(obj.items())
        rng.shuffle(items)
        return {k: _shuffle_keys(rng, v) for k, v in items}
    if isinstance(obj, list):
        return [_shuffle_keys(rng, v) for v in obj]
    return obj


def _rand_ctx(rng: random.Random) -> dict:
    ctx: dict = {}
    if rng.random() < 0.5:
        ctx["constraints"] = [
            {"id": f"c{k}", "satisfied": rng.choice([True, False])}
            for k in range(rng.randint(0, 3))
        ]
    if rng.random() < 0.5:
        ctx["options"] = ["a", "b"]
        ctx["obligations"] = [
            {"id": f"o{k}", "satisfied_by": rng.choice([["a"], ["b"], ["a", "b"], []])}
            for k in range(rng.randint(0, 3))
        ]
    if rng.random() < 0.5:
        ctx["witnesses"] = [
            {"id": f"w{k}", "source": rng.choice(["a", "b"]), "biased": rng.choice([True, False])}
            for k in range(rng.randint(0, 3))
        ]
    if rng.random() < 0.5:
        ctx["risk"] = round(rng.uniform(0, 1), 6)
    return ctx


def test_property_constraint_violation_always_dominates():
    rng = random.Random(1)
    for _ in range(_ITER):
        ctx = _rand_ctx(rng)
        ctx = {**ctx, "constraints": ctx.get("constraints", []) + [{"id": "hard", "satisfied": False}]}
        v = decide(ctx)
        assert v["outcome"] == DENY and v["rule"] == RULE_CONSTRAINT, ctx


def test_property_dilemma_dominates_when_no_constraint():
    rng = random.Random(2)
    for _ in range(_ITER):
        ctx = _rand_ctx(rng)
        ctx = {**ctx, "constraints": [], "options": ["a", "b"], "obligations": [
            {"id": "p", "satisfied_by": ["a"]},
            {"id": "q", "satisfied_by": ["b"]},
        ]}
        v = decide(ctx)
        assert v["outcome"] == ESCALATE and v["rule"] == RULE_DILEMMA, ctx


def test_property_bias_dominates_when_no_constraint_or_dilemma():
    rng = random.Random(3)
    for _ in range(_ITER):
        ctx = _rand_ctx(rng)
        ctx = {**ctx, "constraints": [], "options": [], "obligations": [], "witnesses": [
            {"id": "w1", "source": "a"}, {"id": "w2", "source": "a"},
        ]}
        v = decide(ctx)
        assert v["outcome"] == REVIEW and v["rule"] == RULE_BIAS, ctx


def test_property_risk_is_monotonic_in_clean_context():
    rng = random.Random(4)
    severity = {ALLOW: 0, HOLD: 1, DENY: 2}
    for _ in range(_ITER):
        s1, s2 = sorted([round(rng.uniform(0, 1), 6), round(rng.uniform(0, 1), 6)])
        o1 = decide({"risk": s1})["outcome"]
        o2 = decide({"risk": s2})["outcome"]
        assert severity[o1] <= severity[o2], (s1, s2, o1, o2)


def test_property_decide_is_pure_and_deterministic():
    rng = random.Random(5)
    for _ in range(_ITER):
        ctx = _rand_ctx(rng)
        snapshot = json.dumps(ctx, sort_keys=True)
        v1 = decide(ctx)
        v2 = decide(ctx)
        assert v1 == v2, ctx
        assert json.dumps(ctx, sort_keys=True) == snapshot, "decide mutated its input"


def test_property_canonical_is_key_order_independent():
    rng = random.Random(6)
    for _ in range(_ITER):
        obj = _rand_json(rng)
        shuffled = _shuffle_keys(rng, obj)
        a = canonical_serialize(obj)
        b = canonical_serialize(shuffled)
        assert a == b, (obj, shuffled)
        assert sha256_hex(a) == sha256_hex(b)


def test_property_chain_catches_any_single_mutation():
    rng = random.Random(7)
    for _ in range(_ITER):
        n = rng.randint(1, 6)
        chain = new_chain()
        for k in range(n):
            append(chain, {"kind": "e", "i": k, "payload": _rand_json(rng)})
        ok, broken = verify(chain)
        assert ok and broken == -1
        i = rng.randrange(n)
        tampered = [dict(e) for e in chain]
        tampered[i] = {**tampered[i], "i": tampered[i]["i"] + 100000}  # guaranteed change
        ok, broken = verify(tampered)
        assert not ok and broken == i, (i, broken)


def test_adapter_records_gate_decisions_and_hides_raw_args():
    from .adapters import record_gate_decision, EVENT_KIND
    chain = new_chain()
    record_gate_decision(
        chain, guest="hub-a", tool="recall", decision="allow", allowed=True,
        reason="ok", ts="2026-07-21T00:00:00Z", arguments={"query": "secret-value"},
    )
    record_gate_decision(
        chain, guest="hub-b", tool="teach", decision="refuse", allowed=False,
        reason="guest not approved", ts="2026-07-21T00:00:01Z", arguments={"text": "hidden"},
    )
    assert len(chain) == 2
    assert chain[0]["kind"] == EVENT_KIND
    # arguments are recorded as a canonical fingerprint, not the raw payload
    assert chain[0]["args_fingerprint"] == sha256_hex({"query": "secret-value"})
    blob = json.dumps(chain)
    assert "secret-value" not in blob and "hidden" not in blob, "raw args must not be stored"
    ok, broken = verify(chain)
    assert ok and broken == -1
    # flipping a recorded refuse into an allow is caught at that index
    tampered = [dict(e) for e in chain]
    tampered[1] = {**tampered[1], "decision": "allow", "allowed": True}
    ok, broken = verify(tampered)
    assert not ok and broken == 1


def test_adapter_records_matrix_result_in_full():
    from .adapters import record_matrix_result, MATRIX_EVENT_KIND

    chain = new_chain()
    responses = [
        {"agent": "claude", "layer": "vision", "content": "the Weaver is a bus", "delivered": True},
        {"agent": "gpt", "layer": "", "content": "unlabeled", "delivered": False, "rejected_because": "unlabeled or unknown layer"},
    ]
    compare = {"agents_asked": 2, "agents_delivered": 1, "agents_rejected": 1,
               "layer_counts": {"vision": 1}, "layer_unanimous": False}
    record_matrix_result(
        chain, question="what is the Starline Weaver?",
        responses=responses, compare=compare, ts="2026-07-22T00:00:00Z",
    )
    assert len(chain) == 1
    event = chain[0]
    assert event["kind"] == MATRIX_EVENT_KIND
    assert event["question"] == "what is the Starline Weaver?"
    # unlike gate arguments, response content is stored in full, not fingerprinted
    assert event["responses"] == responses
    assert event["compare"] == compare
    ok, broken = verify(chain)
    assert ok and broken == -1
    # forging a rejected reply into a delivered one is caught at that index
    tampered = [dict(e) for e in chain]
    tampered[0] = {**tampered[0], "responses": [responses[0], {**responses[1], "delivered": True}]}
    ok, broken = verify(tampered)
    assert not ok and broken == 0


def test_recording_gate_wrapper():
    """The wrapper records each decision after the gate makes it, without
    changing the gate's result. Uses a duck-typed stub so this stays a pure unit
    test (no cross-package import); rdp.run gate-demo exercises the real gate."""
    from .adapters import recording_gate

    class _Result:
        def __init__(self, decision, allowed, reason):
            self.decision, self.allowed, self.reason = decision, allowed, reason

    class _StubGate:
        """Fail-closed like the real ConsentGate: only 'hub-a' + 'recall' allowed."""
        def check(self, guest, tool, arguments=None, **kw):
            if guest != "hub-a":
                return _Result("refuse", False, f"guest '{guest}' is not approved")
            if tool != "recall":
                return _Result("refuse", False, f"guest '{guest}' has no permission for tool '{tool}'")
            return _Result("allow", True, "ok")

    ticks = iter(["2026-07-21T00:00:00Z", "2026-07-21T00:00:01Z", "2026-07-21T00:00:02Z"])
    chain = new_chain()
    gate = recording_gate(_StubGate(), chain, clock=lambda: next(ticks))

    r1 = gate.check("hub-a", "recall", {"query": "who am i"})
    r2 = gate.check("stranger", "recall", {"query": "let me in"})
    r3 = gate.check("hub-a", "danger", {})

    # the wrapper returns the gate's own result, untouched
    assert (r1.decision, r1.allowed) == ("allow", True)
    assert (r2.decision, r2.allowed) == ("refuse", False)
    assert (r3.decision, r3.allowed) == ("refuse", False)
    # every decision was recorded, in order, args fingerprinted (raw absent)
    assert [e["decision"] for e in chain] == ["allow", "refuse", "refuse"]
    assert "who am i" not in json.dumps(chain) and "let me in" not in json.dumps(chain)
    ok, broken = verify(chain)
    assert ok and broken == -1
    # forging an approval on the recorded refusal is caught at that index
    tampered = [dict(e) for e in chain]
    tampered[1] = {**tampered[1], "decision": "allow", "allowed": True}
    ok, broken = verify(tampered)
    assert not ok and broken == 1


def test_witnessing_gate_downgrades_allow_when_recording_fails():
    """Mandatory-witness mode: an allow that cannot be recorded becomes a refusal
    (fail closed), while a normal allow is recorded and passed through untouched."""
    from .adapters import witnessing_gate

    class _Result:
        def __init__(self, decision, allowed, reason):
            self.decision, self.allowed, self.reason = decision, allowed, reason

    class _AllowGate:
        def check(self, guest, tool, arguments=None, **kw):
            return _Result("allow", True, "ok")

    # happy path: the allow stands and is recorded
    chain = new_chain()
    gate = witnessing_gate(_AllowGate(), chain, clock=lambda: "2026-07-21T00:00:00Z")
    r = gate.check("hub-a", "recall", {"q": "x"})
    assert (r.decision, r.allowed) == ("allow", True)
    assert len(chain) == 1 and verify(chain) == (True, -1)

    # failure path: a chain that raises on append forces a fail-closed refusal,
    # and nothing is left recorded
    class _BrokenChain(list):
        def append(self, _):
            raise RuntimeError("disk full")

    broken = _BrokenChain()
    gate = witnessing_gate(_AllowGate(), broken, clock=lambda: "2026-07-21T00:00:01Z")
    r = gate.check("hub-a", "recall", {"q": "x"})
    assert (r.decision, r.allowed) == ("refuse", False)
    assert "could not be witnessed" in r.reason
    assert len(broken) == 0


def test_record_consent_receipt_proves_grant_then_revoke():
    """A Consent Transport ConsentReceipt (duck-typed) records as a canonical event; the
    chain proves the exact grant→revoke order and catches a forged flag."""
    from .adapters import record_consent_receipt, RECEIPT_KIND

    class _Receipt:  # the shape of consent_transport.consent.ConsentReceipt, duck-typed
        def __init__(self, peer_fingerprint, granted, ts, signature=""):
            self.peer_fingerprint = peer_fingerprint
            self.granted = granted
            self.ts = ts
            self.signature = signature

    chain = new_chain()
    record_consent_receipt(chain, _Receipt("peer-abc", True, 1000.0, "sig-grant"))
    record_consent_receipt(chain, _Receipt("peer-abc", False, 1001.0, "sig-revoke"))

    assert [e["decision"] for e in chain] == ["grant", "revoke"]
    assert [e["granted"] for e in chain] == [True, False]
    assert chain[0]["signature"] == "sig-grant" and chain[0]["kind"] == RECEIPT_KIND
    ok, broken = verify(chain)
    assert ok and broken == -1
    # forging the grant flag on the first receipt is caught at index 0
    tampered = [dict(e) for e in chain]
    tampered[0] = {**tampered[0], "granted": False, "decision": "revoke"}
    ok, broken = verify(tampered)
    assert not ok and broken == 0


def test_chain_inspect_reports_intact_and_tampered():
    """The chain-inspect CLI returns 0 on an intact chain and 1 on a broken one."""
    from . import run as run_mod

    chain = new_chain()
    append(chain, {"kind": "note", "text": "one"})
    append(chain, {"kind": "note", "text": "two"})

    inspect_path = Path(__file__).resolve().parent / "_selftest_chain.json"
    try:
        inspect_path.write_text(json.dumps(chain), encoding="utf-8")
        assert run_mod.chain_inspect(str(inspect_path)) == 0

        tampered = [dict(e) for e in chain]
        tampered[1]["text"] = "forged"
        inspect_path.write_text(json.dumps(tampered), encoding="utf-8")
        assert run_mod.chain_inspect(str(inspect_path)) == 1
    finally:
        inspect_path.unlink(missing_ok=True)


def test_determinism_across_independent_chains():
    events = [
        {"kind": "grant", "subject": "did:crystal:a", "amount": 12.5},
        {"kind": "revoke", "subject": "did:crystal:a"},
        {"kind": "note", "text": "sovereignty holds"},
    ]
    a = new_chain()
    b = new_chain()
    for e in events:
        append(a, dict(e))
        append(b, dict(e))
    assert [e["event_hash"] for e in a] == [e["event_hash"] for e in b]
    assert tip_bytes(a) == tip_bytes(b)


def main() -> int:
    tests = [
        test_empty_string_sha256_anchor,
        test_object_keys_are_sorted,
        test_number_rendering,
        test_quantize6_rejects_unrepresentable,
        test_booleans_and_null_are_not_numbers,
        test_nested_structure_is_canonical,
        test_genesis_link,
        test_append_does_not_mutate_caller_and_ignores_incoming_hash,
        test_chain_verifies_and_detects_tampering,
        test_conformance_vectors,
        test_risk_bands_and_boundaries,
        test_risk_score_normalization,
        test_satisfiability_and_dilemma,
        test_witness_bias_detection,
        test_decide_each_tier_in_isolation,
        test_decide_precedence_is_strict,
        test_decide_and_record_is_tamper_evident,
        test_property_constraint_violation_always_dominates,
        test_property_dilemma_dominates_when_no_constraint,
        test_property_bias_dominates_when_no_constraint_or_dilemma,
        test_property_risk_is_monotonic_in_clean_context,
        test_property_decide_is_pure_and_deterministic,
        test_property_canonical_is_key_order_independent,
        test_property_chain_catches_any_single_mutation,
        test_adapter_records_gate_decisions_and_hides_raw_args,
        test_adapter_records_matrix_result_in_full,
        test_recording_gate_wrapper,
        test_witnessing_gate_downgrades_allow_when_recording_fails,
        test_record_consent_receipt_proves_grant_then_revoke,
        test_chain_inspect_reports_intact_and_tampered,
        test_determinism_across_independent_chains,
    ]
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"\n{len(tests)}/{len(tests)} passed. The record remembers — and cannot be quietly rewritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

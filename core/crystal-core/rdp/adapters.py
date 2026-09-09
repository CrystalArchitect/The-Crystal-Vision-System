# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Adapters that record outcomes from the pack's real gates and buses onto an
RDP chain — the honest wiring sketched in docs/architecture/crystal-core/RDP-INTEGRATION.md, made concrete.

The whole point is *clean separation*, so note what this module does NOT do:

  * It does not import ConsentGate, Consent Transport, the Starline Weaver, or any
    enforcement/routing code.
  * It never decides anything. It accepts the *fields of an outcome that has
    already happened* and turns them into a canonical, hash-chained record.

So the direction is strictly one-way and the coupling is zero: the gate enforces,
then (afterwards) hands the outcome here to be witnessed. If this recording
failed entirely, the gate's allow/deny would be unaffected — RDP is the ledger,
not the lock.

    from rdp.record import new_chain, verify
    from rdp.adapters import record_gate_decision

    chain = new_chain()
    result = gate.check(guest, tool, arguments)          # enforcement (elsewhere)
    record_gate_decision(                                # witnessing (here)
        chain,
        guest=guest, tool=tool,
        decision=result.decision, allowed=result.allowed, reason=result.reason,
        arguments=arguments, ts=now_iso8601(),
    )
"""

from __future__ import annotations

from collections import namedtuple
from typing import Any

from .canonical import sha256_hex
from .record import append

EVENT_KIND = "consent.gate.decision"
RECEIPT_KIND = "consent_transport.receipt"
MATRIX_EVENT_KIND = "starline.matrix.result"


def gate_event(
    *,
    guest: str,
    tool: str,
    decision: str,          # "allow" | "refuse"
    allowed: bool,
    reason: str,
    ts: Any,                # caller-supplied timestamp (str or number) — never generated here
    arguments: dict[str, Any] | None = None,
    args_fingerprint: str | None = None,
) -> dict[str, Any]:
    """Build the canonical consent-decision event (does not append it).

    The tool arguments are recorded as a *fingerprint* — the canonical SHA-256 of
    the arguments — not as the raw payload. That keeps potentially-sensitive
    inputs out of the ledger while still letting anyone who holds the original
    arguments prove they match. Pass ``args_fingerprint`` yourself if you need a
    different hashing rule (see the note in docs/architecture/crystal-core/RDP-INTEGRATION.md about numeric
    precision under the decimal-6 canonical profile).
    """
    if args_fingerprint is None and arguments is not None:
        args_fingerprint = sha256_hex(arguments)
    return {
        "kind": EVENT_KIND,
        "guest": guest,
        "tool": tool,
        "decision": decision,
        "allowed": bool(allowed),
        "reason": reason,
        "args_fingerprint": args_fingerprint or "",
        "ts": ts,
    }


def record_gate_decision(chain: list[dict[str, Any]], **fields: Any) -> dict[str, Any]:
    """Append a gate decision to *chain* and return the stamped event.

    Call this *after* the gate has decided — never before — so RDP can never sit
    between the gate and its own verdict. Takes the same keyword fields as
    ``gate_event``.
    """
    return append(chain, gate_event(**fields))


def _utc_now_iso() -> str:
    """Default clock — a UTC ISO-8601 timestamp. Injectable so tests stay
    deterministic (the canonical form must not depend on wall-clock)."""
    import datetime

    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class recording_gate:
    """Wrap any consent gate so each decision is written to an RDP chain.

    This is the thin glue that keeps RDP a *ledger, not a lock*:

      * It does not import ConsentGate — it wraps any object whose ``check()``
        returns a result with ``.decision``, ``.allowed`` and ``.reason`` (the
        shape of CrystalBridge's ``GateResult``). Duck-typed on purpose.
      * On each call it lets the wrapped gate decide *first* (enforcement,
        unchanged), then records the outcome *after* the result exists. RDP never
        sits between the gate and its verdict — if the gate raises, nothing is
        recorded; if recording somehow failed, the allow/deny already stands.

    Timestamps come from *clock* (default: real UTC ISO-8601), injectable so the
    canonical record stays reproducible under test.

        gate = ConsentGate(config)                 # enforcement (CrystalBridge)
        chain = new_chain()
        gate = recording_gate(gate, chain)         # + witnessing (RDP)
        result = gate.check("hub-a", "recall", {"query": "x"})
        verify(chain)                              # (True, -1)
    """

    def __init__(self, gate: Any, chain: list[dict[str, Any]], *, clock: Any = _utc_now_iso):
        self._gate = gate
        self._chain = chain
        self._clock = clock

    def check(self, guest: str, tool: str, arguments: dict[str, Any] | None = None, **kw: Any) -> Any:
        result = self._gate.check(guest, tool, arguments, **kw)   # decide first
        record_gate_decision(                                     # then witness
            self._chain,
            guest=guest,
            tool=tool,
            decision=result.decision,
            allowed=result.allowed,
            reason=result.reason,
            arguments=arguments,
            ts=self._clock(),
        )
        return result


# A minimal GateResult-shaped stand-in (.allowed/.reason/.decision) for the
# fail-closed refusal witnessing_gate returns when it cannot record — so callers
# read it exactly like a real gate result, without RDP importing GateResult.
_WitnessRefusal = namedtuple("_WitnessRefusal", ["allowed", "reason", "decision"])


class witnessing_gate:
    """Mandatory-witness wrapper: *no allow stands unless it was recorded.*

    This is the stronger, deliberately-coupled sibling of ``recording_gate``, the
    "mandatory witness" policy described in docs/architecture/crystal-core/RDP-INTEGRATION.md. Where
    ``recording_gate`` records best-effort *after* the gate and never affects the
    verdict, this one makes the record **load-bearing**:

      1. the wrapped gate decides (enforcement, unchanged);
      2. the decision is appended to the chain;
      3. if that append raises, the verdict is **downgraded to a refusal** — the
         action must not proceed on a decision we could not witness. Fail closed.

    An allow that *was* recorded is returned untouched; a refusal is returned as
    is (and still recorded when possible). Use this only when you want "no action
    without a durable record" and accept that the ledger is now in the critical
    path — the opposite trade-off from the default.
    """

    def __init__(self, gate: Any, chain: list[dict[str, Any]], *, clock: Any = _utc_now_iso):
        self._gate = gate
        self._chain = chain
        self._clock = clock

    def check(self, guest: str, tool: str, arguments: dict[str, Any] | None = None, **kw: Any) -> Any:
        result = self._gate.check(guest, tool, arguments, **kw)   # decide first
        try:
            record_gate_decision(
                self._chain,
                guest=guest,
                tool=tool,
                decision=result.decision,
                allowed=result.allowed,
                reason=result.reason,
                arguments=arguments,
                ts=self._clock(),
            )
        except Exception as exc:  # could not witness → cannot allow
            return _WitnessRefusal(
                allowed=False,
                reason=f"refused: decision could not be witnessed ({exc})",
                decision="refuse",
            )
        return result


def consent_receipt_event(receipt: Any, *, ts: Any = None) -> dict[str, Any]:
    """Build a canonical event from a Consent Transport ``ConsentReceipt`` (does not append).

    Duck-typed on purpose — this reads ``peer_fingerprint``, ``granted``, ``ts``
    and ``signature`` off the receipt and does **not** import Consent Transport, keeping the
    zero-coupling rule of this module. The signature is a string and rides
    canonicalization untouched, so the chain proves the exact grant→revoke
    sequence a peer's consent went through.

    By default the event's timestamp is the receipt's own ``ts``; pass ``ts`` to
    override (e.g. for a deterministic test) — as everywhere in RDP, timestamps
    are caller-supplied data, never generated here.
    """
    return {
        "kind": RECEIPT_KIND,
        "peer_fingerprint": receipt.peer_fingerprint,
        "granted": bool(receipt.granted),
        "decision": "grant" if receipt.granted else "revoke",
        "signature": getattr(receipt, "signature", "") or "",
        "ts": receipt.ts if ts is None else ts,
    }


def record_consent_receipt(chain: list[dict[str, Any]], receipt: Any, *, ts: Any = None) -> dict[str, Any]:
    """Append a Consent Transport consent grant/revoke to *chain* and return the event.

    Call it whenever a ``ConsentReceipt`` is issued (grant *or* revoke); the chain
    then holds a tamper-evident, ordered proof of the consent history. Takes the
    same duck-typed receipt as ``consent_receipt_event``.
    """
    return append(chain, consent_receipt_event(receipt, ts=ts))


def matrix_result_event(
    *,
    question: str,
    responses: list[dict[str, Any]],
    compare: dict[str, Any],
    ts: Any,
) -> dict[str, Any]:
    """Build the canonical event for a Starline Weaver matrix run (does not
    append). *responses* and *compare* are plain dicts — the shape
    ``StarlineWeaver.run_matrix()``'s transcript entries and ``cross_compare()``
    already produce, filtered to the reply cycle by the caller. No import of
    ``bridge`` here; the caller does the extracting, this module only records.

    Unlike gate arguments, response content is stored in full, not fingerprinted
    — the whole point of witnessing a matrix run is being able to read back what
    each agent actually said. There is nothing here to treat as a secret.
    """
    return {
        "kind": MATRIX_EVENT_KIND,
        "question": question,
        "responses": responses,
        "compare": compare,
        "ts": ts,
    }


def record_matrix_result(
    chain: list[dict[str, Any]],
    *,
    question: str,
    responses: list[dict[str, Any]],
    compare: dict[str, Any],
    ts: Any = None,
) -> dict[str, Any]:
    """Append a Starline Weaver matrix result to *chain* and return the event.

    Call it *after* ``run_matrix()`` has already produced its transcript and
    ``cross_compare()`` its summary — same one-way rule as the gate adapters:
    the Weaver runs the matrix, RDP only remembers it. Nothing here judges the
    responses or the comparison; that reading was already made (or deliberately
    not made) before this is called.
    """
    return append(chain, matrix_result_event(
        question=question, responses=responses, compare=compare,
        ts=_utc_now_iso() if ts is None else ts,
    ))

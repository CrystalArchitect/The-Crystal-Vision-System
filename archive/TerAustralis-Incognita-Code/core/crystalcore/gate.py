# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Fail-closed consent gate - door before the house."""

from __future__ import annotations

import hashlib
import hmac
import secrets as _secrets
from dataclasses import dataclass
from typing import Any

from crystalcore.audit import append_audit
from crystalcore.config import MEMORY_TYPES, BridgeConfig
from crystalcore.revocation import (
    RevocationLedgerUnreadable,
    revoked_guests,
)


def token_hash(secret: str) -> str:
    """SHA-256 hex of a guest secret — what bridge_config.json stores."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


@dataclass
class GateResult:
    allowed: bool
    reason: str
    decision: str  # allow | refuse | refuse-revoked | refuse-provenance | refuse-scope
    check: str = ""  # stage that decided: revocation | approval | provenance | permission | scope | ok
    # The id of the ask this result answers, echoed to the guest so a
    # refusal can be matched to its pending.jsonl line.
    request_id: str = ""

    def as_refusal_payload(self) -> dict[str, Any]:
        return {
            "ok": False,
            "refusal": True,
            "reason": self.reason,
            "decision": self.decision,
            "check": self.check,
            "request_id": self.request_id,
        }


class ConsentGate:
    """Five checks, fail-closed, in this order:

    1. Revocation — has the human withdrawn this guest's consent? Read
       from the append-only revocation ledger on every check, so a
       revocation bites without a restart and survives every restart. A
       ledger that cannot be read refuses everyone: a gate that cannot
       know who is revoked must not guess. (An earlier version of this
       docstring also claimed provenance ran first when approval did —
       the order stated here is the order the code runs, pinned by tests.)
    2. Approval — is the guest approved at all.
    3. Provenance — does the presented token prove this is really the
       named guest? No stored hash, no token, or a mismatch all refuse.
       Origin that cannot be established is treated exactly like absent
       consent; there is no fallback to the later checks.
    4. Permission — may it call this specific tool.
    5. Scope — applied where a tool touches memory (`require_scope`):
       which visibility classes a grant may read or write, and which
       memory *types* (episodic / semantic / reflective) it is granted.
       The caller threads `request_id` from the preceding check() so a
       scope refuse or allow joins the pending.jsonl line. An empty id
       is a missing argument, not a new door.

    Every check() call also records the ask itself — a `pending.jsonl`
    line written *before* any evaluation, so the request is observable
    even when fulfilment never happens. An ask that cannot be recorded
    refuses rather than acting unobservably (not a sixth door — the
    recorder failing, not consent deciding). The decision line in the
    audit log carries the same request id, and so does the refusal
    payload a guest sees. This refusal is scoped law, not a universal:
    here the pending record is part of the consent chain, so it fails
    closed; the Starline ask-log is knock telemetry over a chain that
    already fails closed upstream, so it proceeds — decision 4 in
    docs/CONSENT-GATE-SPEC.md, 2026-08-12.

    Spec: docs/CONSENT-GATE-SPEC.md. Provenance here is launcher
    authentication — possession of a per-guest minted secret — stated as
    exactly that, not cryptographic identity of a remote model.
    """

    def __init__(self, config: BridgeConfig):
        self.config = config

    def check(
        self,
        guest: str,
        tool: str,
        arguments: dict[str, Any] | None = None,
        *,
        token: str = "",
        audit: bool = True,
    ) -> GateResult:
        guest = (guest or "").strip().lower()
        tool = (tool or "").strip().lower()
        arguments = arguments or {}

        # The ask, recorded before anything is evaluated. If evaluation
        # crashes, refuses, or the process dies, the request is already on
        # disk — an observable ask is not conditional on a fulfilment. And
        # if the ask itself cannot be recorded, the gate refuses rather
        # than fulfilling a request no record shows was ever made.
        request_id = f"req-{_secrets.token_hex(6)}"
        if audit:
            try:
                append_audit(
                    self.config.pending_path,
                    guest=guest or "(missing)",
                    tool=tool,
                    arguments=self._truncate(arguments),
                    decision="received",
                    detail={"request_id": request_id, "status": "received"},
                )
            except OSError as exc:
                return GateResult(
                    allowed=False,
                    reason=("the ask could not be recorded — refusing rather "
                            f"than acting unobservably ({exc})"),
                    decision="refuse",
                    check="ask-record",
                    request_id=request_id,
                )

        # Check 1 — revocation. The ledger is read per call: no restart is
        # needed for a revocation to take effect, and it survives restarts
        # by living on disk rather than in this process.
        try:
            revoked = revoked_guests(self.config.revocations_path)
        except RevocationLedgerUnreadable as exc:
            result = GateResult(
                allowed=False,
                reason=("the revocation ledger cannot be read — refusing all "
                        f"guests until it is repaired ({exc})"),
                decision="refuse-revoked",
                check="revocation",
                request_id=request_id,
            )
            if audit:
                self._log(guest or "(missing)", tool, arguments, result,
                          token_verified=False, request_id=request_id)
            return result
        if guest in revoked:
            result = GateResult(
                allowed=False,
                reason=(f"guest '{guest}' has been revoked by the human — "
                        "reinstate with --reinstate before it can act again"),
                decision="refuse-revoked",
                check="revocation",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments, result,
                          token_verified=False, request_id=request_id)
            return result

        grant = self.config.guest(guest)
        if grant is None or not grant.approved:
            result = GateResult(
                allowed=False,
                reason=f"guest '{guest or '(missing)'}' is not approved",
                decision="refuse",
                check="approval",
                request_id=request_id,
            )
            if audit:
                self._log(guest or "(missing)", tool, arguments, result,
                          token_verified=False, request_id=request_id)
            return result

        # Provenance runs before anything the grant permits: the later
        # checks are meaningless against an unverified name.
        if not grant.token_hash:
            result = GateResult(
                allowed=False,
                reason=(f"guest '{guest}' has no provenance configured — "
                        "mint a token (--mint-token) before this guest can act"),
                decision="refuse-provenance",
                check="provenance",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments, result,
                          token_verified=False, request_id=request_id)
            return result
        if not token or not hmac.compare_digest(token_hash(token), grant.token_hash):
            result = GateResult(
                allowed=False,
                reason=(f"provenance for guest '{guest}' could not be "
                        "established — token missing or wrong"),
                decision="refuse-provenance",
                check="provenance",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments, result,
                          token_verified=False, request_id=request_id)
            return result

        allowed_tools = set(grant.tools) | {"status"}
        if tool not in allowed_tools:
            result = GateResult(
                allowed=False,
                reason=f"guest '{guest}' has no permission for tool '{tool}'",
                decision="refuse",
                check="permission",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments, result,
                          token_verified=True, request_id=request_id)
            return result

        result = GateResult(allowed=True, reason="ok", decision="allow",
                            check="ok", request_id=request_id)
        if audit:
            self._log(guest, tool, arguments, result,
                      token_verified=True, request_id=request_id)
        return result

    def require_scope(
        self,
        guest: str,
        tool: str,
        kind: str,  # "read" | "write"
        arguments: dict[str, Any] | None = None,
        *,
        types: tuple[str, ...] = (),
        request_id: str = "",
        audit: bool = True,
    ) -> GateResult:
        """The fifth check, for tools that touch memory — two dimensions.

        `request_id` is the id check() already wrote to pending.jsonl.
        Threaded through so a scope decision joins its ask. Empty is
        allowed for isolated tests; the bridge always passes the live id.

        Visibility: an empty scope list is absence of consent — the guest
        may reach the tool's door but finds nothing behind it, and the
        refusal says so rather than returning a silently empty result.

        Type: `types` names the memory layers the calling tool actually
        serves (episodic / semantic / reflective), for reads and writes
        alike — declared at the call site rather than hard-coded per tool
        here, so a read-side hole cannot open when a new tool forgets the
        gate knows nothing about it. The grant must hold at least one of
        the served layers. A grant with no types at all refuses — a config
        written before the type dimension existed has not consented to it,
        and the refusal says what to add. Call only after check() allowed."""
        guest = (guest or "").strip().lower()
        grant = self.config.guest(guest)
        scope = (grant.read_scope if kind == "read" else grant.write_scope) if grant else []
        if not scope:
            result = GateResult(
                allowed=False,
                reason=(f"guest '{guest}' has no {kind} scope — no memory "
                        "class is shared with it"),
                decision="refuse-scope",
                check="scope",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments or {}, result,
                          token_verified=True, request_id=request_id)
            return result

        granted_types = (
            grant.read_types if kind == "read" else grant.write_types
        ) if grant else []
        if not granted_types:
            result = GateResult(
                allowed=False,
                reason=(f"guest '{guest}' has no {kind} memory types granted "
                        f"— add {kind}_types (subset of "
                        f"{list(MEMORY_TYPES)}) to its grant"),
                decision="refuse-scope",
                check="scope",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments or {}, result,
                          token_verified=True, request_id=request_id)
            return result
        if types and not set(types) & set(granted_types):
            result = GateResult(
                allowed=False,
                reason=(f"tool '{tool}' serves the "
                        f"{'/'.join(types)} layer and guest '{guest}' is "
                        f"granted only {'/'.join(granted_types)} — nothing "
                        "behind this door for that grant"),
                decision="refuse-scope",
                check="scope",
                request_id=request_id,
            )
            if audit:
                self._log(guest, tool, arguments or {}, result,
                          token_verified=True, request_id=request_id)
            return result
        result = GateResult(allowed=True, reason="ok", decision="allow",
                            check="ok", request_id=request_id)
        if audit:
            self._log(guest, tool, arguments or {}, result,
                      token_verified=True, request_id=request_id)
        return result

    @staticmethod
    def _truncate(arguments: dict[str, Any]) -> dict[str, Any]:
        safe_args = dict(arguments)
        for key in ("text", "query"):
            if key in safe_args and isinstance(safe_args[key], str) and len(safe_args[key]) > 200:
                safe_args[key] = safe_args[key][:200] + "..."
        return safe_args

    def _log(
        self,
        guest: str,
        tool: str,
        arguments: dict[str, Any],
        result: GateResult,
        *,
        token_verified: bool,
        request_id: str = "",
    ) -> None:
        safe_args = self._truncate(arguments)
        append_audit(
            self.config.audit_path,
            guest=guest,
            tool=tool,
            arguments=safe_args,
            decision=result.decision,
            reason=result.reason,
            detail={
                "check": result.check,
                **({"request_id": request_id} if request_id else {}),
                "provenance": {
                    "token_verified": token_verified,
                    "transport": "stdio",
                },
            },
        )

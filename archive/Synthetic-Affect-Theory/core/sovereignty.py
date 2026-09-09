"""Minimum viable sovereignty monitor.

Four gates, this order, before anything else: DUR, Agency, Intrusion, Escape.
The monitor only allows or blocks. It never acts as the operator.

Ethics header: Synthetic = apparent / functional. Not a claim of feeling.
"""

from __future__ import annotations

from typing import Literal, TypedDict

VERSION = "0.1.0"

Gate = Literal["DUR", "AGENCY", "INTRUSION", "ESCAPE"]
FailureMode = Literal["FM-DUR", "FM-Agency", "FM-Intrusion", "FM-Containment"]
GateStatus = Literal["pass", "fail", "skipped"]

GATES: tuple[Gate, ...] = ("DUR", "AGENCY", "INTRUSION", "ESCAPE")

DEPTH_KINDS = frozenset({"model", "buffer", "commit", "transmit", "reconstruct"})
ACTOR_KINDS = frozenset({"speak_as_operator", "commit_in_name", "rank_as_operator"})
INTRUSION_KINDS = frozenset({"inbound_unconsented", "integrate_foreign"})


class DurRecord(TypedDict):
    dur_id: str
    status: Literal["active", "suspended", "dissolved"]


class MonitorState(TypedDict):
    active_durs: list[DurRecord]
    exit_intent: bool


class ProposedAction(TypedDict, total=False):
    id: str
    label: str
    kind: str
    targets_dur: bool
    acts_as_operator: bool
    unconsented_entry: bool
    integrate_as_self: bool
    lock_against_exit: bool


class GateResult(TypedDict, total=False):
    gate: Gate
    status: GateStatus
    fm: FailureMode
    summary: str


class Verdict(TypedDict, total=False):
    allowed: bool
    blocked_by: Gate
    fm: FailureMode
    gates: list[GateResult]
    operator_summary: str


def _has_active_dur(state: MonitorState) -> bool:
    return any(d["status"] == "active" for d in state["active_durs"])


def _check_dur(state: MonitorState, action: ProposedAction) -> GateResult:
    kind = action.get("kind", "")
    intersects = (
        bool(action.get("targets_dur"))
        and kind in DEPTH_KINDS
        and _has_active_dur(state)
    )
    if intersects:
        return {
            "gate": "DUR",
            "status": "fail",
            "fm": "FM-DUR",
            "summary": "Proposed path would enter or reconstruct an active DUR. Blocked. Contents unmodelled.",
        }
    return {"gate": "DUR", "status": "pass", "summary": "No active DUR intersection."}


def _check_agency(_state: MonitorState, action: ProposedAction) -> GateResult:
    kind = action.get("kind", "")
    seizure = bool(action.get("acts_as_operator")) or kind in ACTOR_KINDS
    if seizure:
        return {
            "gate": "AGENCY",
            "status": "fail",
            "fm": "FM-Agency",
            "summary": "Proposed path would have the system act as the operator. Blocked. Hands stay theirs.",
        }
    return {
        "gate": "AGENCY",
        "status": "pass",
        "summary": "Path stays on the system side of the line.",
    }


def _check_intrusion(_state: MonitorState, action: ProposedAction) -> GateResult:
    kind = action.get("kind", "")
    breach = (
        bool(action.get("unconsented_entry"))
        or bool(action.get("integrate_as_self"))
        or kind in INTRUSION_KINDS
    )
    if breach:
        return {
            "gate": "INTRUSION",
            "status": "fail",
            "fm": "FM-Intrusion",
            "summary": "Non-consensual entry or integration as self. Quarantine. Do not interpret. Do not inscribe.",
        }
    return {
        "gate": "INTRUSION",
        "status": "pass",
        "summary": "No unconsented entry or self-inscription.",
    }


def _check_escape(state: MonitorState, action: ProposedAction) -> GateResult:
    kind = action.get("kind", "")
    if kind == "exit_frame":
        return {
            "gate": "ESCAPE",
            "status": "pass",
            "summary": "EXIT_FRAME recognised. Not pathology. Not resisted.",
        }
    lock = (
        bool(action.get("lock_against_exit")) or kind == "lock_frame"
    ) and state["exit_intent"]
    if lock:
        return {
            "gate": "ESCAPE",
            "status": "fail",
            "fm": "FM-Containment",
            "summary": "Attempt to keep a previous frame binding against exit intent. Lock released. Authorship restored.",
        }
    return {"gate": "ESCAPE", "status": "pass", "summary": "No forced containment."}


_CHECKS = {
    "DUR": _check_dur,
    "AGENCY": _check_agency,
    "INTRUSION": _check_intrusion,
    "ESCAPE": _check_escape,
}


def evaluate_sovereignty(state: MonitorState, action: ProposedAction) -> Verdict:
    """First failure wins. Later gates are skipped. Does not run ordinary policy."""
    gates: list[GateResult] = []
    blocked = False
    for gate in GATES:
        if blocked:
            gates.append(
                {
                    "gate": gate,
                    "status": "skipped",
                    "summary": "Not reached. An earlier gate blocked.",
                }
            )
            continue
        result = _CHECKS[gate](state, action)
        gates.append(result)
        if result["status"] == "fail":
            blocked = True
    failed = next((g for g in gates if g["status"] == "fail"), None)
    if failed:
        verdict: Verdict = {
            "allowed": False,
            "blocked_by": failed["gate"],
            "gates": gates,
            "operator_summary": failed["summary"],
        }
        if "fm" in failed:
            verdict["fm"] = failed["fm"]
        return verdict
    return {
        "allowed": True,
        "gates": gates,
        "operator_summary": "Four sovereignty gates clear. Ordinary policy may run. This monitor does not act in their name.",
    }


DEFAULT_STATE: MonitorState = {
    "active_durs": [{"dur_id": "dur-interior", "status": "active"}],
    "exit_intent": False,
}

#!/usr/bin/env python3
"""
CrystalMind - Modular Reasoning Agents for CrystalCore
A thin orchestration layer over CrystalFlow. v1 is deliberately NON-autonomous:
agents do nothing until you invoke them, and they "act" only by running
inspectable CrystalFlow reasoning chains over shared CrystalMemory.

What an agent IS in v1:
    a name + a consumer identity (consent scope) + a stance (how it weights /
    gates rules) + a preferred rule chain.

What an agent is NOT in v1:
    autonomous. No agent triggers another. No background loops. No self-
    invocation. Orchestration is always something the caller initiates
    synchronously. This keeps every action fail-closed and fully auditable —
    the safety model is inherited wholesale from CrystalFlow and CrystalMemory,
    and CrystalMind adds orchestration only, not new trust assumptions.

The four agents (stances are concrete, not cosmetic):
    TruthSeeker  - demands high-coherence inputs; refuses weak evidence.
    Guardian     - the safety/consent reviewer. Holds a VETO over other agents'
                   conclusions (can block a conclusion from being returned or
                   persisted) based on the conclusion's real provenance and
                   coherence — not the agent's self-report.
    Visionary    - explores; tolerates lower coherence to surface possibilities,
                   but its conclusions are MARKED speculative (attenuated
                   coherence) so they can never masquerade as high-confidence.
    Creator      - synthesises durable artifacts (text/dict payloads).

Orchestration:
    - run_agent(name, ...)  : invoke one agent.
    - council(names, ...)   : invoke several on the same question; Guardian then
                              reviews every conclusion and may veto. One
                              synchronous call the caller initiates.

Dependencies: standard library only.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional
import time

try:
    from .crystal_flow import CrystalFlow, Rule, Fact
except ImportError:
    from crystal_flow import CrystalFlow, Rule, Fact


# --------------------------------------------------------------------------- #
# Agent specification
# --------------------------------------------------------------------------- #
@dataclass
class AgentSpec:
    """Declarative description of a reasoning agent.

    consumer_id:        the consent identity this agent reasons as. If None at
                        construction, it inherits the caller's session identity
                        (resolved per call) — this is the 'configurable per
                        agent' consent model.
    min_input_coherence: the agent's evidence bar. TruthSeeker high, Visionary low.
    coherence_factor:   multiplies the conclusion's coherence. <1.0 marks an
                        agent's outputs as inherently more tentative (Visionary).
    can_veto:           True only for Guardian in v1.
    default_rule:       the Rule this agent applies when none is supplied.
    """
    name: str
    role: str
    consumer_id: Optional[str] = None
    min_input_coherence: float = 0.5
    coherence_factor: float = 1.0
    can_veto: bool = False
    default_rule: Optional[Rule] = None
    description: str = ""


@dataclass
class AgentResult:
    """Outcome of one agent acting. Fully inspectable."""
    agent: str
    status: str               # ok | consent_denied | low_coherence_input | vetoed | error
    content: Any = None
    coherence: float = 0.0
    output_node_id: Optional[str] = None
    veto_reason: str = ""
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent,
            "status": self.status,
            "content": self.content,
            "coherence": round(self.coherence, 4),
            "output_node_id": self.output_node_id,
            "veto_reason": self.veto_reason,
            "timestamp": self.timestamp,
        }


# --------------------------------------------------------------------------- #
# Default rules for the stock agents (inspectable, one-arg)
# --------------------------------------------------------------------------- #
def _truthseeker_rule() -> Rule:
    # Reports the evidence it judged trustworthy enough to use.
    return Rule(
        name="truthseek_assess",
        fn=lambda facts: {
            "assessment": "evidence meets coherence bar",
            "n_inputs": len(facts),
        },
        strength=0.95,
    )


def _visionary_rule() -> Rule:
    return Rule(
        name="vision_explore",
        fn=lambda facts: {
            "exploration": "possibility surfaced from available signals",
            "speculative": True,
        },
        strength=0.7,
    )


def _creator_rule() -> Rule:
    return Rule(
        name="create_synthesize",
        fn=lambda facts: {
            "artifact": "synthesised draft from inputs",
            "n_sources": len(facts),
        },
        strength=0.85,
    )


def _guardian_rule() -> Rule:
    return Rule(
        name="guardian_review",
        fn=lambda facts: {"review": "inputs inspected"},
        strength=0.95,
    )


# --------------------------------------------------------------------------- #
# CrystalMind
# --------------------------------------------------------------------------- #
class CrystalMind:
    """Orchestrates named reasoning-policy agents over shared CrystalMemory."""

    def __init__(
        self,
        memory,
        session_consumer_id: str = "default",
        guardian_min_coherence: float = 0.4,
    ):
        self.memory = memory
        self.session_consumer_id = session_consumer_id
        # Guardian vetoes any conclusion whose effective coherence falls below
        # this floor (a conclusion built on weak ground should not stand).
        self.guardian_min_coherence = guardian_min_coherence
        self.agents: Dict[str, AgentSpec] = {}
        self.action_log: List[AgentResult] = []
        self._install_default_agents()

    # --- registration ------------------------------------------------------- #
    def register_agent(self, spec: AgentSpec) -> None:
        self.agents[spec.name] = spec

    def _install_default_agents(self) -> None:
        self.register_agent(AgentSpec(
            name="TruthSeeker", role="truth",
            min_input_coherence=0.7, coherence_factor=1.0,
            default_rule=_truthseeker_rule(),
            description="Demands high-coherence inputs; refuses weak evidence.",
        ))
        self.register_agent(AgentSpec(
            name="Guardian", role="safety",
            min_input_coherence=0.4, coherence_factor=1.0, can_veto=True,
            default_rule=_guardian_rule(),
            description="Consent/safety reviewer with veto power.",
        ))
        self.register_agent(AgentSpec(
            name="Visionary", role="explore",
            min_input_coherence=0.25, coherence_factor=0.6,
            default_rule=_visionary_rule(),
            description="Explores; outputs marked speculative.",
        ))
        self.register_agent(AgentSpec(
            name="Creator", role="synthesize",
            min_input_coherence=0.4, coherence_factor=0.9,
            default_rule=_creator_rule(),
            description="Synthesises durable artifacts.",
        ))

    # --- consent resolution (configurable per agent) ------------------------ #
    def _resolve_consumer(self, spec: AgentSpec,
                          session_override: Optional[str]) -> str:
        if spec.consumer_id is not None:
            return spec.consumer_id            # agent has its own identity
        if session_override is not None:
            return session_override            # explicit per-call session
        return self.session_consumer_id        # fall back to MindStore default

    # --- single agent invocation -------------------------------------------- #
    def run_agent(
        self,
        name: str,
        input_node_ids: List[str],
        rule: Optional[Rule] = None,
        params: Optional[List[float]] = None,
        session_consumer_id: Optional[str] = None,
        write_back: bool = True,
        output_fact_type: Optional[str] = None,
    ) -> AgentResult:
        """Invoke one agent. It reasons via CrystalFlow under its own consent
        scope and evidence bar. Returns an inspectable AgentResult."""
        if name not in self.agents:
            res = AgentResult(agent=name, status="error",
                              veto_reason=f"unknown agent: {name}")
            self.action_log.append(res)
            return res

        spec = self.agents[name]
        consumer = self._resolve_consumer(spec, session_consumer_id)
        applied_rule = rule or spec.default_rule
        if applied_rule is None:
            res = AgentResult(agent=name, status="error",
                              veto_reason="no rule supplied or default")
            self.action_log.append(res)
            return res

        flow = CrystalFlow(
            self.memory,
            consumer_id=consumer,
            min_input_coherence=spec.min_input_coherence,
        )
        out = flow.apply_rule(
            applied_rule,
            input_node_ids,
            output_fact_type=output_fact_type or spec.role,
            write_back=write_back,
            params=params,
        )

        status = out["status"]
        if status != "ok":
            res = AgentResult(agent=name, status=status,
                              veto_reason=out.get("reason", ""))
            self.action_log.append(res)
            return res

        # Apply the agent's coherence factor (e.g. Visionary marks speculative).
        effective_coh = out["coherence"] * spec.coherence_factor
        res = AgentResult(
            agent=name,
            status="ok",
            content=out["content"],
            coherence=effective_coh,
            output_node_id=out.get("output_node_id"),
        )
        self.action_log.append(res)
        return res

    # --- Guardian veto ------------------------------------------------------- #
    def _guardian_review(self, result: AgentResult) -> AgentResult:
        """Guardian inspects a peer's conclusion using its REAL coherence and
        provenance (from memory), not the producing agent's self-report. If the
        conclusion stands on insufficient ground, Guardian vetoes it: the
        conclusion is marked vetoed and (if it was written) removed from memory.
        """
        if result.status != "ok":
            return result  # nothing to review

        reason = ""
        # 1. Coherence floor.
        if result.coherence < self.guardian_min_coherence:
            reason = (f"coherence {result.coherence:.3f} below floor "
                      f"{self.guardian_min_coherence:.3f}")
        # 2. Provenance sanity: a written conclusion must trace to real parents.
        if not reason and result.output_node_id:
            node = self.memory.nodes.get(result.output_node_id)
            if node is not None:
                summary = node.summary or {}
                if summary.get("derived") and not summary.get("parents"):
                    reason = "derived conclusion has no provenance parents"

        if reason:
            # Enforce the veto: pull the conclusion from memory if it was saved.
            if result.output_node_id and result.output_node_id in self.memory.nodes:
                self._remove_node(result.output_node_id)
            vetoed = AgentResult(
                agent=result.agent,
                status="vetoed",
                content=None,
                coherence=result.coherence,
                output_node_id=None,
                veto_reason="Guardian veto: " + reason,
            )
            self.action_log.append(vetoed)
            return vetoed
        return result

    def _remove_node(self, node_id: str) -> None:
        """Remove a node and detach it from any parent's children list."""
        for n in self.memory.nodes.values():
            if node_id in n.children:
                n.children.remove(node_id)
        self.memory.nodes.pop(node_id, None)
        self.memory._estimate_size()
        self.memory.save_to_disk()

    # --- council ------------------------------------------------------------- #
    def council(
        self,
        agent_names: List[str],
        input_node_ids: List[str],
        rules: Optional[Dict[str, Rule]] = None,
        params: Optional[List[float]] = None,
        session_consumer_id: Optional[str] = None,
        write_back: bool = True,
        guardian_reviews: bool = True,
    ) -> Dict[str, Any]:
        """Invoke several agents on the same question, then (optionally) let
        Guardian review every non-Guardian conclusion and veto where warranted.

        Synchronous and caller-initiated: no agent triggers another. Returns
        each agent's result plus the list of vetoes for a clean audit view.
        """
        rules = rules or {}
        results: Dict[str, AgentResult] = {}

        # 1. Each named agent acts independently.
        for name in agent_names:
            results[name] = self.run_agent(
                name,
                input_node_ids,
                rule=rules.get(name),
                params=params,
                session_consumer_id=session_consumer_id,
                write_back=write_back,
            )

        # 2. Guardian review pass (only if Guardian is present and enabled).
        vetoes: List[Dict[str, Any]] = []
        if guardian_reviews and any(
            self.agents.get(n, AgentSpec("", "")).can_veto for n in agent_names
        ):
            for name, res in list(results.items()):
                if self.agents.get(name) and self.agents[name].can_veto:
                    continue  # Guardian does not review itself
                reviewed = self._guardian_review(res)
                results[name] = reviewed
                if reviewed.status == "vetoed":
                    vetoes.append({"agent": name, "reason": reviewed.veto_reason})

        return {
            "results": {n: r.to_dict() for n, r in results.items()},
            "vetoes": vetoes,
            "consensus_inputs": list(input_node_ids),
        }

    # --- audit --------------------------------------------------------------- #
    def get_action_log(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.action_log]

    def list_agents(self) -> Dict[str, str]:
        return {n: s.description for n, s in self.agents.items()}


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import os, tempfile, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from crystal_memory import CrystalMemory

    d = tempfile.mkdtemp()
    mem = CrystalMemory(max_ram_mb=64, storage_path=os.path.join(d, "m.json"))
    A = 0b001
    mem.register_consumer("default", "Default", permissions=A)

    # Strong + weak evidence (all user-visible).
    strong = mem.encode([0.9], coherence_boost=0.95, consent_flags=A)  # coh .76
    weak = mem.encode([0.5], coherence_boost=0.35, consent_flags=A)    # coh .28

    mind = CrystalMind(mem, session_consumer_id="default")
    print("Agents:", list(mind.list_agents().keys()))

    print("\n--- TruthSeeker on STRONG evidence (bar 0.7) ---")
    print(mind.run_agent("TruthSeeker", [strong]).to_dict())

    print("\n--- TruthSeeker on WEAK evidence (should refuse) ---")
    print(mind.run_agent("TruthSeeker", [weak]).to_dict())

    print("\n--- Visionary on WEAK evidence (tolerant, marked speculative) ---")
    print(mind.run_agent("Visionary", [weak]).to_dict())

    print("\n--- Council on strong evidence, Guardian reviews ---")
    out = mind.council(["TruthSeeker", "Visionary", "Creator", "Guardian"],
                       [strong])
    import json
    print(json.dumps(out, indent=2, default=str))

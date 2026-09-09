#!/usr/bin/env python3
"""
CrystalFlow - Computation & Reasoning Engine for CrystalCore
Operates directly on CrystalMemory.

Two clean, separable engines that share CrystalMemory's consent and coherence:

  1. Autograd core (micrograd-style scalar reverse-mode autodiff)
     - Pure Python, no NumPy required.
     - Every Value is inspectable; every gradient step is traceable.
     - Intended for small optimization / fitness scoring on edge hardware,
       NOT for large neural nets.

  2. Symbolic reasoning engine (inspectable first-principles chains)
     - Each step reads PERMITTED nodes from CrystalMemory.
     - Applies an explicit, named, auditable rule.
     - Writes a derived conclusion back to memory with provenance links.
     - Coherence propagation is conservative:
           output_coherence = min(input effective_coherences) * rule_strength
     - Consent is FAIL-CLOSED: if the active consumer lacks permission for ANY
       required input, the whole step refuses. A confident conclusion must never
       be built on an input the reasoner could not actually see.

Sovereignty / edge rationale:
  - No black-box outputs: every conclusion carries its inputs, rule, and the
    coherence that produced it.
  - Graceful degradation: under memory pressure the engine drops to pure
    symbolic mode (no gradient tape) so reasoning stays available.
  - Consumer-aware sessions support the family "power of three" model.

Dependencies: standard library only.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import math
import time


# --------------------------------------------------------------------------- #
# 1. Autograd core (micrograd-style)
# --------------------------------------------------------------------------- #
class Value:
    """A single scalar value in a reverse-mode autodiff graph.

    Deliberately minimal and fully inspectable: `.data` is the number,
    `.grad` is the accumulated gradient, `._prev` is the set of parents, and
    `.op` names the operation that produced this node. Call `.backward()` on
    the output to populate gradients throughout the graph.
    """

    __slots__ = ("data", "grad", "_backward", "_prev", "op", "label")

    def __init__(self, data: float, _children: Tuple["Value", ...] = (),
                 op: str = "", label: str = ""):
        self.data = float(data)
        self.grad = 0.0
        self._backward: Callable[[], None] = lambda: None
        self._prev: Set["Value"] = set(_children)
        self.op = op
        self.label = label

    def __repr__(self) -> str:
        return f"Value(data={self.data:.6g}, grad={self.grad:.6g}, op='{self.op}')"

    # --- core ops ------------------------------------------------------------ #
    def __add__(self, other: Any) -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other: Any) -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, exponent: float) -> "Value":
        assert isinstance(exponent, (int, float)), "only numeric powers supported"
        out = Value(self.data ** exponent, (self,), f"**{exponent}")

        def _backward():
            self.grad += (exponent * self.data ** (exponent - 1)) * out.grad
        out._backward = _backward
        return out

    def relu(self) -> "Value":
        out = Value(0.0 if self.data < 0 else self.data, (self,), "relu")

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out

    def tanh(self) -> "Value":
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - t * t) * out.grad
        out._backward = _backward
        return out

    # --- conveniences -------------------------------------------------------- #
    def __neg__(self) -> "Value":
        return self * -1

    def __sub__(self, other: Any) -> "Value":
        return self + (-other if isinstance(other, Value) else Value(-other))

    def __radd__(self, other: Any) -> "Value":
        return self + other

    def __rmul__(self, other: Any) -> "Value":
        return self * other

    def __truediv__(self, other: Any) -> "Value":
        other = other if isinstance(other, Value) else Value(other)
        return self * other ** -1

    # --- backprop ------------------------------------------------------------ #
    def backward(self) -> None:
        """Topologically sort the graph and run reverse-mode autodiff."""
        topo: List[Value] = []
        visited: Set[Value] = set()

        def build(v: "Value"):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                topo.append(v)

        build(self)
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()


def sgd_step(params: List[Value], lr: float = 0.01) -> None:
    """One vanilla gradient-descent step. Inspectable, no momentum/state."""
    for p in params:
        p.data -= lr * p.grad


def zero_grad(params: List[Value]) -> None:
    for p in params:
        p.grad = 0.0


# --------------------------------------------------------------------------- #
# 2. Symbolic reasoning engine
# --------------------------------------------------------------------------- #
@dataclass
class Fact:
    """A typed, inspectable unit of knowledge pulled from or written to memory.

    fact_type examples: "policy_claim", "family_decision", "creative_fragment".
    `node_id` links back to the CrystalMemory node (None for transient facts).
    `coherence` is the EFFECTIVE coherence at read time (decay already applied
    by CrystalMemory.retrieve).
    """
    fact_type: str
    content: Any
    coherence: float = 1.0
    node_id: Optional[str] = None
    consent_flags: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fact_type": self.fact_type,
            "content": self.content,
            "coherence": self.coherence,
            "node_id": self.node_id,
            "consent_flags": self.consent_flags,
        }


@dataclass
class Rule:
    """An explicit, named transformation over input facts.

    `fn` receives the list of input Facts and returns the derived content
    (any serializable value). It MAY optionally accept a second argument — a
    numeric parameter vector (List[float]) — letting a rule's behaviour be
    tuned by an evolved genome. The signature is detected automatically, so
    one-argument rules (`fn(facts)`) and two-argument rules
    (`fn(facts, params)`) are both supported and backward compatible.

    `strength` in [0, 1] expresses how much the rule itself preserves
    confidence — it multiplies the propagated coherence. A weak heuristic
    should declare a low strength; an identity restatement ~1.0.

    `uses_params` is cached at construction so we don't re-introspect per call.
    """
    name: str
    fn: Callable[..., Any]
    strength: float = 1.0
    description: str = ""
    uses_params: bool = field(init=False, default=False)

    def __post_init__(self):
        try:
            import inspect
            n = len(inspect.signature(self.fn).parameters)
            self.uses_params = n >= 2
        except (ValueError, TypeError):
            self.uses_params = False

    def invoke(self, facts: "List[Fact]", params: "Optional[List[float]]" = None) -> Any:
        """Call the rule, passing params only if the rule declared it wants them."""
        if self.uses_params:
            return self.fn(facts, params if params is not None else [])
        return self.fn(facts)


class ConsentViolation(Exception):
    """Raised (and caught) when a reasoning step touches a forbidden input."""


@dataclass
class StepRecord:
    """Audit record for a single reasoning step."""
    rule: str
    input_node_ids: List[str]
    input_coherences: List[float]
    output_coherence: float
    output_node_id: Optional[str]
    consumer_id: str
    status: str            # "ok" | "consent_denied" | "degraded_symbolic"
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule": self.rule,
            "input_node_ids": self.input_node_ids,
            "input_coherences": [round(c, 4) for c in self.input_coherences],
            "output_coherence": round(self.output_coherence, 4),
            "output_node_id": self.output_node_id,
            "consumer_id": self.consumer_id,
            "status": self.status,
            "timestamp": self.timestamp,
        }


class CrystalFlow:
    """
    Reasoning engine over CrystalMemory.

    Reads are consent- and coherence-aware (delegated to CrystalMemory).
    Conclusions are written back with provenance. Every step is logged.
    """

    def __init__(
        self,
        memory,
        consumer_id: str = "default",
        min_input_coherence: float = 0.5,
        apply_temporal_decay: Optional[bool] = None,
        low_memory_symbolic_only: bool = False,
    ):
        self.memory = memory
        self.consumer_id = consumer_id
        self.min_input_coherence = min_input_coherence
        self.apply_temporal_decay = apply_temporal_decay
        # When True, the autograd tape is disabled (pure symbolic mode).
        self.low_memory_symbolic_only = low_memory_symbolic_only
        self.derivation_log: List[StepRecord] = []

    # --- memory reads (consent + coherence first-class) ---------------------- #
    def read_fact(self, node_id: str, fact_type: str = "fact") -> Fact:
        """Read a node as a Fact. Raises ConsentViolation if not permitted.

        Coherence here is the EFFECTIVE coherence (decay applied by memory),
        so downstream propagation uses real, current confidence.
        """
        result = self.memory.retrieve(
            node_id,
            consumer_id=self.consumer_id,
            min_coherence=0.0,  # we want the value + its coherence, then judge
            apply_temporal_decay=self.apply_temporal_decay,
        )
        if result is None:
            raise ConsentViolation(f"node {node_id} not found")
        if result.get("status") == "consent_denied":
            raise ConsentViolation(
                f"consumer '{self.consumer_id}' denied access to node {node_id}"
            )

        coherence = result.get(
            "effective_coherence",
            result.get("metadata", {}).get("coherence_score", 0.0),
        )
        # Prefer durable payload (policy text, decision, genome) over the
        # numeric tensor view when the node carries one.
        payload = result.get("payload")
        content = payload if payload is not None else result.get("content")
        consent_flags = result.get("metadata", {}).get("consent_flags", 1)
        return Fact(
            fact_type=fact_type,
            content=content,
            coherence=coherence,
            node_id=node_id,
            consent_flags=consent_flags,
        )

    # --- coherence propagation ---------------------------------------------- #
    @staticmethod
    def propagate_coherence(input_coherences: List[float], rule_strength: float) -> float:
        """Conservative rule: weakest input caps confidence, then the rule
        attenuates it. Empty inputs -> 0 (a conclusion from nothing is not
        confident)."""
        if not input_coherences:
            return 0.0
        return min(input_coherences) * max(0.0, min(1.0, rule_strength))

    # --- the core reasoning step -------------------------------------------- #
    def apply_rule(
        self,
        rule: Rule,
        input_node_ids: List[str],
        output_fact_type: str = "derived",
        write_back: bool = True,
        output_consent_flags: Optional[int] = None,
        params: Optional[List[float]] = None,
    ) -> Dict[str, Any]:
        """Apply a rule to inputs read from memory and (optionally) write the
        conclusion back with provenance.

        `params` (optional) is a numeric vector passed to rules that declared a
        two-argument signature — the bridge that lets an evolved genome's
        numeric vector tune symbolic rule behaviour.

        FAIL-CLOSED on consent: if ANY input is forbidden, the step does not
        run, nothing is written, and a 'consent_denied' record is logged.
        """
        # 1. Read all inputs first — any violation aborts the whole step.
        facts: List[Fact] = []
        try:
            for nid in input_node_ids:
                facts.append(self.read_fact(nid))
        except ConsentViolation as e:
            record = StepRecord(
                rule=rule.name,
                input_node_ids=list(input_node_ids),
                input_coherences=[],
                output_coherence=0.0,
                output_node_id=None,
                consumer_id=self.consumer_id,
                status="consent_denied",
            )
            self.derivation_log.append(record)
            return {"status": "consent_denied", "reason": str(e),
                    "record": record.to_dict()}

        # 2. Enforce the minimum-coherence gate on inputs.
        for f in facts:
            if f.coherence < self.min_input_coherence:
                record = StepRecord(
                    rule=rule.name,
                    input_node_ids=list(input_node_ids),
                    input_coherences=[f.coherence for f in facts],
                    output_coherence=0.0,
                    output_node_id=None,
                    consumer_id=self.consumer_id,
                    status="low_coherence_input",
                )
                self.derivation_log.append(record)
                return {"status": "low_coherence_input",
                        "record": record.to_dict()}

        # 3. Apply the rule (passing params only if the rule wants them).
        derived_content = rule.invoke(facts, params)

        # 4. Propagate coherence conservatively.
        out_coherence = self.propagate_coherence(
            [f.coherence for f in facts], rule.strength
        )

        # 5. Consent for the output: intersection (AND) of input flags by default
        #    so a conclusion is never MORE widely visible than its inputs.
        if output_consent_flags is None:
            out_flags = facts[0].consent_flags
            for f in facts[1:]:
                out_flags &= f.consent_flags
        else:
            out_flags = output_consent_flags

        # 6. Write back with provenance (unless transient or symbolic-only).
        out_node_id = None
        status = "ok"
        if write_back:
            # Numeric conclusions go in the tensor; non-numeric (text, dict,
            # decisions, genomes) go in the durable payload and survive intact.
            if isinstance(derived_content, (list, tuple)):
                tensor_data = derived_content
                payload = None
            else:
                tensor_data = [0.0]            # lightweight numeric placeholder
                payload = derived_content      # the real, durable conclusion
            out_node_id = self.memory.encode_derived(
                data=tensor_data,
                parent_ids=[f.node_id for f in facts if f.node_id],
                coherence=out_coherence,
                consent_flags=out_flags,
                rule=rule.name,
                payload=payload,
            )
            if getattr(self.memory, "last_status", "") == "degraded_symbolic":
                status = "degraded_symbolic"

        record = StepRecord(
            rule=rule.name,
            input_node_ids=list(input_node_ids),
            input_coherences=[f.coherence for f in facts],
            output_coherence=out_coherence,
            output_node_id=out_node_id,
            consumer_id=self.consumer_id,
            status=status,
        )
        self.derivation_log.append(record)

        return {
            "status": status,
            "content": derived_content,
            "coherence": out_coherence,
            "output_node_id": out_node_id,
            "output_consent_flags": out_flags,
            "record": record.to_dict(),
        }

    # --- chains -------------------------------------------------------------- #
    def reason_chain(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run a sequence of rule applications. Each step dict:
            {"rule": Rule, "inputs": [node_id, ...], "fact_type": str}
        The output node of one step can be referenced by later steps, enabling
        first-principles derivation chains. Stops early on consent denial.
        """
        results = []
        for step in steps:
            res = self.apply_rule(
                rule=step["rule"],
                input_node_ids=step["inputs"],
                output_fact_type=step.get("fact_type", "derived"),
            )
            results.append(res)
            if res["status"] == "consent_denied":
                break  # fail-closed: do not continue a chain past a denial
        return results

    # --- autograd bridge ----------------------------------------------------- #
    def values_from_node(self, node_id: str) -> List[Value]:
        """Extract a node's stored values as autograd Values (consent-checked).

        In low-memory symbolic-only mode this returns an empty list so callers
        degrade to non-gradient reasoning rather than building a tape.
        """
        if self.low_memory_symbolic_only:
            return []
        fact = self.read_fact(node_id)  # raises if forbidden
        content = fact.content
        raw: List[float] = []
        if isinstance(content, dict) and "values_sample" in content:
            raw = [float(v) for v in content["values_sample"]]
        elif isinstance(content, (list, tuple)):
            raw = [float(v) for v in content]
        return [Value(v, label=f"{node_id}[{i}]") for i, v in enumerate(raw)]

    # --- audit --------------------------------------------------------------- #
    def get_derivation_log(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.derivation_log]


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import os, tempfile, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from crystal_memory import CrystalMemory

    d = tempfile.mkdtemp()
    mem = CrystalMemory(max_ram_mb=64, storage_path=os.path.join(d, "m.json"))
    mem.register_consumer("alice", "Alice", permissions=0b01)
    mem.register_consumer("bob", "Bob", permissions=0b10)

    # Two policy-claim nodes Alice can see.
    a = mem.encode([0.8, 0.6, 0.9], coherence_boost=0.95, consent_flags=0b01)
    b = mem.encode([0.7, 0.5, 0.8], coherence_boost=0.90, consent_flags=0b01)
    # One node only Bob can see.
    secret = mem.encode([0.1, 0.1], coherence_boost=0.99, consent_flags=0b10)

    flow = CrystalFlow(mem, consumer_id="alice", min_input_coherence=0.4)

    # Rule: average the first sampled value of each input (toy first-principle).
    avg_rule = Rule(
        name="average_first_values",
        fn=lambda facts: [
            sum(f.content["values_sample"][0] for f in facts) / len(facts)
        ],
        strength=0.9,
        description="Mean of leading sampled values; mild confidence loss.",
    )

    print("--- Alice reasons over permitted nodes ---")
    res = flow.apply_rule(avg_rule, [a, b], output_fact_type="policy_claim")
    print("status:", res["status"], "coherence:", round(res["coherence"], 4))

    print("\n--- Alice tries to use Bob's private node (fail-closed) ---")
    res2 = flow.apply_rule(avg_rule, [a, secret])
    print("status:", res2["status"])

    print("\n--- Autograd sanity (z = x*y + x^2) ---")
    x = Value(2.0, label="x")
    y = Value(3.0, label="y")
    z = x * y + x ** 2          # dz/dx = y + 2x = 7 ; dz/dy = x = 2
    z.backward()
    print(f"z={z.data:.4f}, dz/dx={x.grad:.4f} (expect 7), "
          f"dz/dy={y.grad:.4f} (expect 2)")

    print("\n--- Derivation log ---")
    for r in flow.get_derivation_log():
        print(r)

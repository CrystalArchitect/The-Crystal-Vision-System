#!/usr/bin/env python3
"""
CrystalEvolve - Population-Based Training for CrystalCore
Evolves hybrid genomes (numeric parameters + symbolic rule chains) using
CrystalFlow for fitness evaluation and CrystalMemory for durable, provenance-
linked storage of survivors.

Design commitments (locked with the user):

  1. CLOSED RULE REGISTRY. Symbolic mutation may only recombine pre-registered,
     inspectable rules referenced by name. It cannot synthesize new rule logic.
     This keeps every evolved genome fully auditable and prevents an unattended
     edge device from ever generating opaque or unsafe behaviour.

  2. INVALID GENOMES GET FITNESS 0 AND ARE LOGGED (not silently repaired).
     A malformed symbolic mutation is *visible* in the run log and dies off
     naturally. This preserves honest provenance and keeps the run
     deterministic. A `repair_hook` seam exists for a future, evidence-driven
     repair strategy — but v1 does not hide failures.

  3. GATED FITNESS. Symbolic validity is a hard pass/fail gate:
       - invalid genome            -> fitness 0.0
       - valid genome              -> fitness = numeric_score * symbolic_coherence
     Symbolic quality still influences ranking (via propagated coherence) but
     cannot paper over an invalid structure, and there are no magic weights.

  4. DETERMINISTIC. Given a seed, a run is fully reproducible offline — a
     requirement for auditability on field hardware.

Edge discipline:
  - Pure Python, standard library only.
  - Survivors are written back with HIGH family_priority so CrystalMemory's
    pruning (score = coherence * family_priority * temporal_weight) does not
    evict them under pressure. This is essential: without it, the best results
    of a run could be pruned exactly when memory is tight.
  - Population size and generations are bounded; no unbounded growth.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
import random
import time

# CrystalFlow provides the autograd Value type and consent-aware reasoning.
try:
    from .crystal_flow import Value, Rule, CrystalFlow
except ImportError:  # direct script / flat import
    from crystal_flow import Value, Rule, CrystalFlow


# --------------------------------------------------------------------------- #
# Rule registry (closed, inspectable)
# --------------------------------------------------------------------------- #
class RuleRegistry:
    """A closed set of named, pre-vetted rules.

    Symbolic genomes reference rules ONLY by these names. Mutation can add,
    remove, or swap names drawn from this registry — never invent new logic.
    Every rule here is human-inspected once, then safe to recombine freely.
    """

    def __init__(self):
        self._rules: Dict[str, Rule] = {}

    def register(self, rule: Rule) -> None:
        self._rules[rule.name] = rule

    def get(self, name: str) -> Optional[Rule]:
        return self._rules.get(name)

    def has(self, name: str) -> bool:
        return name in self._rules

    def names(self) -> List[str]:
        return list(self._rules.keys())

    def __len__(self) -> int:
        return len(self._rules)


# --------------------------------------------------------------------------- #
# Genome
# --------------------------------------------------------------------------- #
@dataclass
class Genome:
    """A hybrid genome: numeric parameters + an ordered symbolic rule chain.

    params:     numeric vector optimised by perturbation / gradients.
    rule_chain: ordered list of rule NAMES (keys into a RuleRegistry).
    The genome is a plain, serializable dict — it round-trips through
    CrystalMemory's durable `payload` field intact.
    """
    params: List[float] = field(default_factory=list)
    rule_chain: List[str] = field(default_factory=list)
    genome_id: str = ""
    parent_ids: List[str] = field(default_factory=list)
    generation: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "genome",
            "params": list(self.params),
            "rule_chain": list(self.rule_chain),
            "genome_id": self.genome_id,
            "parent_ids": list(self.parent_ids),
            "generation": self.generation,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Genome":
        return cls(
            params=list(d.get("params", [])),
            rule_chain=list(d.get("rule_chain", [])),
            genome_id=d.get("genome_id", ""),
            parent_ids=list(d.get("parent_ids", [])),
            generation=d.get("generation", 0),
        )


@dataclass
class FitnessResult:
    """Outcome of evaluating one genome. Fully inspectable."""
    genome_id: str
    valid: bool
    numeric_score: float
    symbolic_coherence: float
    fitness: float
    reason: str = ""          # why invalid, if applicable

    def to_dict(self) -> Dict[str, Any]:
        return {
            "genome_id": self.genome_id,
            "valid": self.valid,
            "numeric_score": round(self.numeric_score, 6),
            "symbolic_coherence": round(self.symbolic_coherence, 6),
            "fitness": round(self.fitness, 6),
            "reason": self.reason,
        }


# --------------------------------------------------------------------------- #
# Evolution engine
# --------------------------------------------------------------------------- #
class CrystalEvolve:
    """Population-based trainer over hybrid genomes.

    numeric_scorer: Callable[[List[Value]], Value]
        Builds a differentiable score from the genome's params (as autograd
        Values). Higher is better. Evolve treats it as a black box but can
        optionally take a gradient step (Lamarckian refinement) before scoring.
    """

    def __init__(
        self,
        memory,
        registry: RuleRegistry,
        numeric_scorer: Callable[[List[Value]], Value],
        consumer_id: str = "default",
        seed: int = 0,
        population_size: int = 12,
        param_dim: int = 4,
        max_chain_len: int = 4,
        mutation_rate: float = 0.3,
        param_sigma: float = 0.2,
        survivor_priority: float = 10.0,
        max_eval_steps: int = 64,
        lamarckian: bool = True,
        repair_hook: Optional[Callable[["Genome", "RuleRegistry"], "Genome"]] = None,
    ):
        self.memory = memory
        self.registry = registry
        self.numeric_scorer = numeric_scorer
        self.consumer_id = consumer_id
        self.rng = random.Random(seed)
        self.population_size = population_size
        self.param_dim = param_dim
        self.max_chain_len = max_chain_len
        self.mutation_rate = mutation_rate
        self.param_sigma = param_sigma
        # Survivors get HIGH family_priority so pruning won't evict them.
        self.survivor_priority = survivor_priority
        self.max_eval_steps = max_eval_steps
        # Inheritance mode: True = Lamarckian (write back learned params),
        # False = Baldwinian (select for learning capacity, keep base params).
        self.lamarckian = lamarckian
        self.repair_hook = repair_hook  # reserved; unused in v1 by design

        self.population: List[Genome] = []
        self.eval_log: List[FitnessResult] = []
        self.generation = 0
        self._counter = 0

    # --- genome identity ---------------------------------------------------- #
    def _new_id(self) -> str:
        self._counter += 1
        return f"g{self.generation}_{self._counter}"

    # --- initialisation ----------------------------------------------------- #
    def seed_population(self) -> None:
        names = self.registry.names()
        self.population = []
        for _ in range(self.population_size):
            params = [self.rng.gauss(0.0, 1.0) for _ in range(self.param_dim)]
            chain_len = self.rng.randint(1, max(1, self.max_chain_len))
            chain = [self.rng.choice(names) for _ in range(chain_len)] if names else []
            self.population.append(
                Genome(params=params, rule_chain=chain,
                       genome_id=self._new_id(), generation=self.generation)
            )

    # --- validation (the symbolic safety gate) ------------------------------ #
    def validate(self, genome: Genome) -> Tuple[bool, str]:
        """A genome is valid iff:
          - it has at least one rule,
          - every rule name exists in the closed registry,
          - the chain length is within bounds (terminates / bounded compute).
        Returns (is_valid, reason)."""
        if not genome.rule_chain:
            return False, "empty_rule_chain"
        if len(genome.rule_chain) > self.max_chain_len:
            return False, "chain_too_long"
        for name in genome.rule_chain:
            if not self.registry.has(name):
                return False, f"unknown_rule:{name}"
        return True, "ok"

    # --- symbolic coherence over the chain ---------------------------------- #
    def _chain_coherence(self, genome: Genome) -> float:
        """Conservative product of the rule strengths along the chain, matching
        CrystalFlow's 'a chain is only as strong as its composition' stance.
        Empty/invalid chains are handled by validate() before this is called."""
        coh = 1.0
        for name in genome.rule_chain:
            rule = self.registry.get(name)
            coh *= max(0.0, min(1.0, rule.strength)) if rule else 0.0
        return coh

    # --- fitness (gated) ---------------------------------------------------- #
    def evaluate(self, genome: Genome, refine_steps: int = 0,
                 lr: float = 0.05, lamarckian: Optional[bool] = None) -> FitnessResult:
        """Gated fitness:
            invalid -> 0.0 (logged)
            valid   -> squash(numeric_score) * symbolic_coherence

        Optional gradient refinement: take `refine_steps` gradient-ascent steps
        on the numeric params before scoring.

        Inheritance mode (`lamarckian`, defaults to the engine's setting):
          - Lamarckian (True):  refined params are written back into the genome
            — learned traits are inherited. Strong exploitation; can collapse
            diversity toward a shared local optimum.
          - Baldwinian (False): refinement improves the *score* the genome is
            judged by, but the genome keeps its ORIGINAL params. The capacity to
            learn is selected for, without freezing the learned values. Better
            exploration / diversity retention.
        """
        if lamarckian is None:
            lamarckian = self.lamarckian

        valid, reason = self.validate(genome)
        if not valid:
            res = FitnessResult(genome.genome_id, False, 0.0, 0.0, 0.0, reason)
            self.eval_log.append(res)
            return res

        # Build autograd params from the genome's current values.
        values = [Value(p, label=f"p{i}") for i, p in enumerate(genome.params)]

        # Optional gradient refinement (bounded, deterministic).
        for _ in range(refine_steps):
            for v in values:
                v.grad = 0.0
            score = self.numeric_scorer(values)
            score.backward()
            for v in values:
                v.data += lr * v.grad      # ascent: maximise score

        refined_params = [v.data for v in values]
        if lamarckian:
            # Inherit the learned values.
            genome.params = refined_params
            scoring_params = refined_params
        else:
            # Baldwinian: judge by the refined score, keep original params.
            scoring_params = refined_params  # score reflects learning capacity
            # genome.params left unchanged

        # Final numeric score (no grad needed).
        numeric_score = float(self.numeric_scorer(
            [Value(p) for p in scoring_params]
        ).data)

        # Gating multiplies by symbolic coherence in [0,1]. For that to be
        # well-behaved, the numeric score must also be non-negative — otherwise
        # higher coherence would *raise* a negative score (rewarding LESS
        # coherent chains). We squash the raw score into (0,1] with a monotone
        # map so ordering is preserved and gating always behaves correctly.
        squashed = self._squash(numeric_score)
        symbolic_coh = self._chain_coherence(genome)
        fitness = squashed * symbolic_coh

        res = FitnessResult(
            genome.genome_id, True, numeric_score, symbolic_coh, fitness, "ok"
        )
        self.eval_log.append(res)
        return res

    @staticmethod
    def _squash(x: float) -> float:
        """Monotone map from any real score to (0, 1], preserving order.

        Uses a logistic on the raw score. This keeps multiplicative gating
        meaningful for objectives that produce negative values (e.g. -loss):
        a better raw score always yields a higher squashed score, and
        multiplying by coherence in [0,1] then always penalises weaker chains.
        """
        # Guard against overflow for very negative x.
        if x < -60:
            return 1e-26
        import math
        return 1.0 / (1.0 + math.exp(-x))

    # --- mutation (numeric + symbolic) -------------------------------------- #
    def mutate(self, parent: Genome) -> Genome:
        """Produce a child by perturbing params (numeric) and/or editing the
        rule chain using only registry names (symbolic)."""
        names = self.registry.names()

        # --- numeric mutation: Gaussian perturbation ---
        child_params = [
            p + (self.rng.gauss(0.0, self.param_sigma)
                 if self.rng.random() < self.mutation_rate else 0.0)
            for p in parent.params
        ]

        # --- symbolic mutation: add / remove / swap a rule (registry-only) ---
        child_chain = list(parent.rule_chain)
        if names and self.rng.random() < self.mutation_rate:
            op = self.rng.choice(["add", "remove", "swap"])
            if op == "add" and len(child_chain) < self.max_chain_len:
                pos = self.rng.randint(0, len(child_chain))
                child_chain.insert(pos, self.rng.choice(names))
            elif op == "remove" and len(child_chain) > 1:
                del child_chain[self.rng.randrange(len(child_chain))]
            elif op == "swap" and child_chain:
                child_chain[self.rng.randrange(len(child_chain))] = \
                    self.rng.choice(names)

        child = Genome(
            params=child_params,
            rule_chain=child_chain,
            genome_id=self._new_id(),
            parent_ids=[parent.genome_id],
            generation=self.generation,
        )
        # Reserved repair seam (disabled in v1 by design).
        if self.repair_hook is not None:
            child = self.repair_hook(child, self.registry)
        return child

    # --- one generation ----------------------------------------------------- #
    def step_generation(self, refine_steps: int = 0) -> Dict[str, Any]:
        """Evaluate the population, select survivors (top half by fitness),
        and breed the next generation by mutation. Returns a summary."""
        results = [(g, self.evaluate(g, refine_steps=refine_steps))
                   for g in self.population]
        scored = [(g, r.fitness) for g, r in results]
        scored.sort(key=lambda gs: gs[1], reverse=True)

        n_survivors = max(1, len(scored) // 2)
        survivors = [g for g, _ in scored[:n_survivors]]

        self.generation += 1
        children: List[Genome] = []
        while len(survivors) + len(children) < self.population_size:
            parent = self.rng.choice(survivors)
            children.append(self.mutate(parent))
        # Keep survivors (elitism) + new children.
        for g in survivors + children:
            g.generation = self.generation
        self.population = survivors + children

        best_g, best_fit = scored[0]
        return {
            "generation": self.generation,
            "best_genome_id": best_g.genome_id,
            "best_fitness": round(best_fit, 6),
            "n_survivors": n_survivors,
            # Count STRUCTURAL validity, not fitness sign — a valid genome may
            # legitimately have negative fitness (e.g. a -loss objective).
            "n_valid": sum(1 for _, r in results if r.valid),
            "population_size": len(self.population),
        }

    def run(self, generations: int, refine_steps: int = 0) -> List[Dict[str, Any]]:
        if not self.population:
            self.seed_population()
        history = []
        for _ in range(generations):
            history.append(self.step_generation(refine_steps=refine_steps))
        return history

    # --- persist survivors with strong provenance --------------------------- #
    def persist_best(self, top_k: int = 1,
                     consent_flags: int = 1) -> List[str]:
        """Write the top-k current genomes back to CrystalMemory as derived
        nodes with HIGH family_priority and provenance to their parents.

        Returns the new node IDs. Genomes live in the durable `payload`."""
        scored = [(g, self.evaluate(g).fitness) for g in self.population]
        scored.sort(key=lambda gs: gs[1], reverse=True)
        node_ids = []
        for g, fit in scored[:top_k]:
            valid, _ = self.validate(g)
            if not valid:
                continue
            nid = self.memory.encode_derived(
                data=g.params if g.params else [0.0],
                parent_ids=g.parent_ids,
                coherence=self._chain_coherence(g),
                consent_flags=consent_flags,
                family_priority=self.survivor_priority,  # protect from pruning
                rule="evolve:" + ">".join(g.rule_chain),
                payload=g.to_dict(),                      # durable genome
            )
            node_ids.append(nid)
        return node_ids

    def get_eval_log(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.eval_log]


# --------------------------------------------------------------------------- #
# Demo
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import os, tempfile, sys
    sys.path.insert(0, os.path.dirname(__file__))
    from crystal_memory import CrystalMemory

    d = tempfile.mkdtemp()
    mem = CrystalMemory(max_ram_mb=64, storage_path=os.path.join(d, "m.json"))

    # A tiny closed registry of inspectable rules.
    reg = RuleRegistry()
    reg.register(Rule(name="normalize", fn=lambda f: f, strength=0.95))
    reg.register(Rule(name="weight", fn=lambda f: f, strength=0.9))
    reg.register(Rule(name="aggregate", fn=lambda f: f, strength=0.85))

    # Numeric objective: maximise -sum((p - target)^2), target = [1, -1, 0.5, 2].
    target = [1.0, -1.0, 0.5, 2.0]

    def scorer(values):
        loss = Value(0.0)
        for v, t in zip(values, target):
            loss = loss + (v - t) ** 2
        return -loss  # higher (less negative) is better

    evo = CrystalEvolve(
        mem, reg, scorer, seed=42,
        population_size=12, param_dim=4, max_chain_len=4,
    )

    print("--- Evolving (with gradient refinement) ---")
    history = evo.run(generations=8, refine_steps=5)
    for h in history:
        print(h)

    print("\n--- Persisting best survivor (high priority) ---")
    ids = evo.persist_best(top_k=1, consent_flags=0b01)
    print("survivor node:", ids)
    if ids:
        got = mem.retrieve(ids[0], min_coherence=0.0)
        print("durable genome payload:", got["payload"]["rule_chain"],
              "params~", [round(p, 3) for p in got["payload"]["params"]])

    print("\n--- Invalid-genome handling (fitness 0, logged) ---")
    bad = Genome(params=[0.0] * 4, rule_chain=["nonexistent_rule"],
                 genome_id="bad")
    res = evo.evaluate(bad)
    print(res.to_dict())

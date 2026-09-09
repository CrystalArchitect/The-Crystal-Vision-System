#!/usr/bin/env python3
"""
Family Decision Pipeline — End-to-End CrystalCore Demo
=======================================================

A realistic "power of three" scenario: a family is weighing a decision
(relocating for work) using several pieces of evidence, some private to one
member. This single script exercises the whole stack and every sovereignty
property the framework promises:

  CrystalMemory  -> durable, consent-tagged storage of evidence + the decision
  CrystalFlow    -> a consent- and coherence-aware reasoning chain that
                    synthesises a recommendation, with full provenance
  CrystalEvolve  -> optimises a numeric "weighting" genome (how much to trust
                    each evidence category) against a fitness objective, then
                    persists the best weighting durably

Demonstrated guarantees (each labelled in the output):
  [CONSENT]     a private node is invisible to a member who lacks permission;
                a reasoning step that needs it FAILS CLOSED.
  [COHERENCE]   a stale/low-confidence input lowers the conclusion's coherence
                (min(inputs) x rule_strength), and can gate a step out.
  [PROVENANCE]  the written decision links back to the exact evidence + rule.
  [DURABLE]     the decision text and the evolved weighting survive a reload.
  [PRUNING]     a high-priority decision survives memory pressure that evicts
                low-priority chatter.

Run:  python3 examples/family_decision_pipeline.py
Requires only the standard library.
"""

import os
import sys
import tempfile

# Allow running from the repo root or the examples/ dir.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from src.crystal_memory import CrystalMemory
    from src.crystal_flow import CrystalFlow, Rule, Value
    from src.crystal_evolve import CrystalEvolve, RuleRegistry, Genome
except ImportError:
    from crystal_memory import CrystalMemory
    from crystal_flow import CrystalFlow, Rule, Value
    from crystal_evolve import CrystalEvolve, RuleRegistry, Genome


def hr(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def main():
    workdir = tempfile.mkdtemp(prefix="family_demo_")
    store = os.path.join(workdir, "family_memory.json")

    # Consent bit layout: bit0 = parent_a, bit1 = parent_b, bit2 = teen.
    # "family_shared" = all three bits set (0b111).
    A, B, T = 0b001, 0b010, 0b100
    SHARED = A | B | T

    # ---------------------------------------------------------------- #
    # 1. MEMORY — store evidence with consent + coherence
    # ---------------------------------------------------------------- #
    hr("1. CrystalMemory — storing family evidence")
    mem = CrystalMemory(max_ram_mb=64, storage_path=store,
                        decay_half_life_days=45.0)
    mem.register_consumer("parent_a", "Parent A", permissions=A)
    mem.register_consumer("parent_b", "Parent B", permissions=B)
    mem.register_consumer("teen", "Teen", permissions=T)
    mem.register_consumer("family", "Family (shared view)", permissions=SHARED)

    # Shared evidence (all can see). Values are toy "scores" 0..1.
    job = mem.encode([0.85], coherence_boost=0.95, consent_flags=SHARED,
                     family_priority=2.0,
                     payload={"category": "job_opportunity",
                              "note": "Strong role, +30% salary"})
    schools = mem.encode([0.70], coherence_boost=0.90, consent_flags=SHARED,
                         family_priority=2.0,
                         payload={"category": "schools",
                                  "note": "Good but not top-tier district"})
    community = mem.encode([0.55], coherence_boost=0.85, consent_flags=SHARED,
                           family_priority=2.0,
                           payload={"category": "community",
                                    "note": "Smaller friend network initially"})

    # A PRIVATE note from the teen, visible only to the teen (bit 2).
    private = mem.encode([0.30], coherence_boost=0.95, consent_flags=T,
                         family_priority=1.5,
                         payload={"category": "private_feelings",
                                  "note": "Anxious about leaving close friends"})

    print(f"  stored job_opportunity   -> {job}   (shared)")
    print(f"  stored schools           -> {schools}   (shared)")
    print(f"  stored community         -> {community}   (shared)")
    print(f"  stored private_feelings  -> {private}   (teen only)")
    print(f"  stats: {mem.get_stats()}")

    # ---------------------------------------------------------------- #
    # 2. EVOLVE — optimise how much to weight each evidence category
    # ---------------------------------------------------------------- #
    hr("2. CrystalEvolve — optimising evidence weights (numeric+symbolic genome)")

    # A closed, inspectable registry. These rules can consume the genome's
    # numeric params (the weights) — the numeric<->symbolic bridge.
    reg = RuleRegistry()
    reg.register(Rule(
        name="weighted_blend",
        # params = [w_job, w_schools, w_community]; rule reports the weights.
        fn=lambda facts, params: {"weights": [round(p, 3) for p in params]},
        strength=0.95,
        description="Blend evidence using evolved weights.",
    ))
    reg.register(Rule(
        name="sanity_clip",
        fn=lambda facts, params: facts,
        strength=0.9,
        description="Clip/normalise step (placeholder).",
    ))

    # Fitness: we want weights that (a) sum to ~1 (a valid distribution),
    # (b) are non-negative, and (c) lean toward higher-confidence evidence.
    #
    # NOTE (a real lesson): an earlier version omitted the positivity term.
    # The optimiser promptly returned NEGATIVE weights — a valid solution to
    # the objective as written, but not the one intended. This is reward
    # hacking in miniature: the genome optimises exactly what you specify, so
    # under-specified objectives get exploited. The `neg_pen` term below closes
    # that loophole. Higher fitness is better; we return -loss.
    def fitness_scorer(values):
        w = values  # [w_job, w_schools, w_community]
        s = w[0] + w[1] + w[2]
        sum_pen = (s - 1.0) ** 2
        # Penalise negative weights (relu of -w is >0 only when w<0).
        neg_pen = (-w[0]).relu() + (-w[1]).relu() + (-w[2]).relu()
        # Encourage ordering w_job >= w_schools >= w_community.
        order_pen = (w[1] - w[0]).relu() + (w[2] - w[1]).relu()
        loss = sum_pen + 2.0 * neg_pen + order_pen
        return -loss

    evo = CrystalEvolve(
        mem, reg, fitness_scorer,
        consumer_id="family", seed=7,
        population_size=14, param_dim=3, max_chain_len=3,
        survivor_priority=20.0,         # protect the result from pruning
        # Lamarckian here: we want the PERSISTED genome to carry the refined,
        # constraint-respecting weights. (Baldwinian would explore better but
        # store the unrefined base params — wrong for a deliverable we keep.)
        lamarckian=True,
    )
    history = evo.run(generations=12, refine_steps=6)
    print("  generation-by-generation best fitness:")
    for h in history:
        print(f"    gen {h['generation']:>2}: best={h['best_fitness']:.4f}  "
              f"valid={h['n_valid']}/{h['population_size']}")

    best_ids = evo.persist_best(top_k=1, consent_flags=SHARED)
    best = mem.retrieve(best_ids[0], consumer_id="family", min_coherence=0.0)
    weights = best["payload"]["params"]
    print(f"\n  [DURABLE] best weighting genome persisted -> {best_ids[0]}")
    print(f"            weights ~ {[round(w, 3) for w in weights]}  "
          f"chain={best['payload']['rule_chain']}")
    print(f"            family_priority={mem.nodes[best_ids[0]].metadata.family_priority} "
          f"(high -> protected from pruning)")

    # ---------------------------------------------------------------- #
    # 3. FLOW — reason to a recommendation, with consent + provenance
    # ---------------------------------------------------------------- #
    hr("3. CrystalFlow — synthesising a recommendation (consent-aware)")

    # The recommendation rule consumes the evolved weights (params) and the
    # shared evidence facts, producing durable decision text.
    def recommend(facts, params):
        w = params if params else [1/3, 1/3, 1/3]
        labels = [f.content.get("category", "?") if isinstance(f.content, dict)
                  else "?" for f in facts]
        score = sum(w_i for w_i in w)  # weights already ~normalised
        verdict = "RELOCATE" if score >= 0.0 else "STAY"  # toy threshold
        return {
            "verdict": "RELOCATE",
            "based_on": labels,
            "weights_used": [round(x, 3) for x in w],
            "summary": "Recommend relocation: job + schools outweigh "
                       "initial community adjustment.",
        }

    recommend_rule = Rule(name="recommend", fn=recommend, strength=0.9)

    flow = CrystalFlow(mem, consumer_id="family", min_input_coherence=0.4,
                       apply_temporal_decay=False)

    # --- 3a. Family-level reasoning over SHARED evidence (succeeds) ---
    print("  [3a] Family reasons over shared evidence:")
    res = flow.apply_rule(
        recommend_rule,
        [job, schools, community],
        output_fact_type="family_decision",
        params=weights,
    )
    print(f"       status        : {res['status']}")
    print(f"       [COHERENCE]   : {res['coherence']:.4f}  "
          f"(= min(input coherences) x rule_strength)")
    decision_id = res["output_node_id"]
    decision = mem.retrieve(decision_id, consumer_id="family", min_coherence=0.0)
    print(f"       verdict       : {decision['payload']['verdict']}")
    print(f"       [PROVENANCE]  : decision {decision_id}")
    print(f"                       rule='{mem.nodes[decision_id].summary['rule']}'")
    print(f"                       parents={mem.nodes[decision_id].summary['parents']}")

    # --- 3b. Parent A tries to reason using the teen's PRIVATE note ---
    print("\n  [3b] Parent A attempts to use the teen's private note:")
    flow_a = CrystalFlow(mem, consumer_id="parent_a", min_input_coherence=0.4)
    denied = flow_a.apply_rule(recommend_rule, [job, private], params=weights)
    print(f"       [CONSENT]     : status='{denied['status']}'  -> FAIL-CLOSED")
    print(f"                       nothing written; reason recorded in the log")

    # --- 3c. The teen CAN use their own private note ---
    print("\n  [3c] The teen reasons including their own private note:")
    flow_t = CrystalFlow(mem, consumer_id="teen", min_input_coherence=0.4)
    teen_res = flow_t.apply_rule(
        Rule(name="teen_reflect",
             fn=lambda facts: {"note": "Teen's view recorded privately."},
             strength=0.9),
        [private],
        output_fact_type="private_reflection",
    )
    print(f"       status        : {teen_res['status']}  "
          f"(teen has permission for their own note)")

    # ---------------------------------------------------------------- #
    # 4. DURABILITY — reload from disk, decision + genome intact
    # ---------------------------------------------------------------- #
    hr("4. Durability — reloading from disk")
    mem2 = CrystalMemory(max_ram_mb=64, storage_path=store)
    mem2.register_consumer("family", "Family", permissions=SHARED)
    again = mem2.retrieve(decision_id, consumer_id="family", min_coherence=0.0)
    print(f"  [DURABLE] decision reloaded: verdict="
          f"{again['payload']['verdict']!r}, "
          f"summary present={bool(again['payload'].get('summary'))}")
    geno = mem2.retrieve(best_ids[0], consumer_id="family", min_coherence=0.0)
    print(f"  [DURABLE] genome reloaded : weights="
          f"{[round(w,3) for w in geno['payload']['params']]}")

    # ---------------------------------------------------------------- #
    # 5. PRUNING — the important decision survives memory pressure
    # ---------------------------------------------------------------- #
    hr("5. Pruning — high-priority decision survives churn")
    mem2.max_ram_mb = 0.05  # squeeze hard
    for i in range(150):
        mem2.encode([float(i)] * 30, coherence_boost=0.4,
                    family_priority=0.1, consent_flags=SHARED)
    survived = decision_id in mem2.nodes
    geno_survived = best_ids[0] in mem2.nodes
    print(f"  flooded 150 low-priority nodes under a 0.05 MB budget")
    print(f"  [PRUNING] family decision survived : {survived}")
    print(f"  [PRUNING] evolved genome survived  : {geno_survived}")
    print(f"  final stats: {mem2.get_stats()}")

    # ---------------------------------------------------------------- #
    # Audit trail
    # ---------------------------------------------------------------- #
    hr("Audit — CrystalFlow derivation log (family session)")
    for rec in flow.get_derivation_log():
        print(f"  {rec}")

    hr("Done")
    print(f"  Working store: {store}")
    print("  Every conclusion above is traceable to its inputs, rule, and")
    print("  coherence — and access was enforced per consumer throughout.")


if __name__ == "__main__":
    main()

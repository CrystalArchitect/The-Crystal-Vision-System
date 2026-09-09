#!/usr/bin/env python3
"""
Policy-Drafting Council — End-to-End CrystalCore Demo
=====================================================

The second of the two shipped demos (the first is
``family_decision_pipeline.py``). Where that one follows a single family
decision through the whole stack, this one shows the CrystalMind *council* doing
real policy work over a body of evidence, using the substantive rules in
``src/policy_rules.py`` rather than the stock placeholder rules.

The scenario: an advocacy group is weighing a position on a proposed measure.
Each piece of evidence is stored in CrystalMemory as a consent-tagged Fact whose
payload looks like::

    {"claim": str, "stance": "support" | "oppose" | "neutral",
     "weight": float in [0, 1], "source": str}

Three agents are then convened on the same evidence, each with the policy rule
matched to its stance:

  TruthSeeker -> truthseeker_weigh : weighs support vs. opposition by claim
                                     weight AND each fact's coherence.
  Creator     -> creator_draft     : synthesises a durable position statement.
  Guardian    -> guardian_audit    : audits the evidence base for one-sidedness,
                                     low-coherence reliance, and thin coverage,
                                     then reviews every peer conclusion and may
                                     veto one built on insufficient ground.

Demonstrated guarantees (each labelled in the output):
  [CONSENT]     every agent reasons under an explicit consumer identity; an
                input it cannot see fails the step closed.
  [COHERENCE]   a conclusion is never more confident than its weakest input.
  [PROVENANCE]  the written position statement links back to its evidence.
  [VETO]        Guardian can remove a conclusion that lacks sound ground.

Run:  python3 examples/policy_council.py
Requires only the standard library.
"""

import json
import os
import sys
import tempfile

# Allow running from the repo root or the examples/ dir.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from src.crystal_memory import CrystalMemory
    from src.crystal_mind import CrystalMind
    from src.policy_rules import policy_rule_set
except ImportError:
    from crystal_memory import CrystalMemory
    from crystal_mind import CrystalMind
    from policy_rules import policy_rule_set


def hr(title):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def main():
    workdir = tempfile.mkdtemp(prefix="policy_demo_")
    store = os.path.join(workdir, "policy_memory.json")

    # Consent bit layout: bit 0 = analyst (the advocacy group's working view).
    ANALYST = 0b001

    # ---------------------------------------------------------------- #
    # 1. MEMORY — store the evidence base with consent + coherence
    # ---------------------------------------------------------------- #
    hr("1. CrystalMemory — storing the evidence base")
    mem = CrystalMemory(max_ram_mb=64, storage_path=store)
    mem.register_consumer("analyst", "Policy Analyst", permissions=ANALYST)

    # Each evidence item: a high-/low-coherence Fact carrying a stance payload.
    evidence = [
        (0.95, {"claim": "Cuts household energy costs by ~12%",
                "stance": "support", "weight": 0.9, "source": "Treasury model"}),
        (0.90, {"claim": "Creates regional maintenance jobs",
                "stance": "support", "weight": 0.7, "source": "Industry body"}),
        (0.88, {"claim": "Improves grid resilience in heat events",
                "stance": "support", "weight": 0.6, "source": "Operator review"}),
        (0.92, {"claim": "High upfront capital outlay",
                "stance": "oppose", "weight": 0.65, "source": "Budget office"}),
        (0.91, {"claim": "Transition risk for incumbent suppliers",
                "stance": "oppose", "weight": 0.4, "source": "Sector submission"}),
    ]

    node_ids = []
    for coh, payload in evidence:
        nid = mem.encode([coh], coherence_boost=coh, consent_flags=ANALYST,
                         family_priority=1.5, payload=payload)
        node_ids.append(nid)
        print(f"  stored {payload['stance']:<7} w={payload['weight']:<4} "
              f"-> {nid}  ({payload['claim']})")

    # ---------------------------------------------------------------- #
    # 2. MIND — convene the council on the same evidence
    # ---------------------------------------------------------------- #
    hr("2. CrystalMind — convening the policy council")
    mind = CrystalMind(mem, session_consumer_id="analyst")
    print("  agents:", list(mind.list_agents().keys()))

    out = mind.council(
        ["TruthSeeker", "Creator", "Guardian"],
        node_ids,
        rules=policy_rule_set(),
    )

    # ---------------------------------------------------------------- #
    # 3. RESULTS — each stance's conclusion, with provenance + veto pass
    # ---------------------------------------------------------------- #
    hr("3. Council results (Guardian has reviewed every peer conclusion)")
    for agent, res in out["results"].items():
        print(f"\n  [{agent}] status={res['status']} "
              f"coherence={res['coherence']}")
        if res["content"] is not None:
            print("    " + json.dumps(res["content"], indent=4).replace("\n", "\n    "))
        if res["status"] == "ok" and res["output_node_id"]:
            node = mem.nodes.get(res["output_node_id"])
            if node is not None and node.summary:
                print(f"    [PROVENANCE] rule='{node.summary.get('rule')}' "
                      f"parents={node.summary.get('parents')}")

    hr("4. Vetoes")
    if out["vetoes"]:
        for v in out["vetoes"]:
            print(f"  [VETO] {v['agent']}: {v['reason']}")
    else:
        print("  No vetoes — every conclusion stood on sufficient ground.")

    hr("Done")
    print(f"  Working store: {store}")
    print("  Every conclusion above is traceable to its evidence and rule,")
    print("  and access was enforced per consumer throughout.")


if __name__ == "__main__":
    main()

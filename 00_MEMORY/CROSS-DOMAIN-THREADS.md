# Cross-Domain Research Threads (2026-09-13)

This document maps active research threads across the five science domains and identifies integration requirements.

---

## Thread 1: Agent Governance Under Resource Constraints

**Domains involved:** AI Safety (16) ↔ Economics (20) ↔ Physics (17)

**Description:** Do governance mechanisms designed in abstract economic models (MiroShark/GTB) preserve safety properties when deployed to agents operating under realistic physical constraints (Mars environment)?

**Active research:**
- **AI Safety:** AgentGit (tamper-evident provenance), Coalition detection benchmark, LLM-judge calibration
- **Economics:** Audit sweep (welfare vs. enforcement intensity), Compute market design, Planner reactivity
- **Physics:** mars-cybertruck-sim agent behavior under scarcity and extreme environments

**Integration gap:** Economic policies tested on GTB agents (which operate in a simplified logistics world) haven't been validated on embodied agents navigating Mars. Welfare metrics may not transfer when agents face hard physical constraints.

**Validation approach:**
1. Port GTB governance parameters (audit_probability, tax rates, redistribution) to mars-cybertruck agents
2. Run comparative sweeps: (a) GTB baseline, (b) Mars with same parameters
3. Compare welfare, Gini, catch rates across both environments
4. Verify whether irreversibility axiom (Drawer 19) holds under resource scarcity

**Pending issues:** None; framework in place. Awaiting implementation. Hub extract: [`THREAD-1-GOVERNANCE-SCARCITY-EXTRACT.md`](THREAD-1-GOVERNANCE-SCARCITY-EXTRACT.md) (2026-09-18).

---

## Thread 2: Coalition Detection Across Governance Topologies

**Domains involved:** AI Safety (16) ↔ Mathematics (18) ↔ Philosophical Foundations (19)

**Description:** Current coalition detection (structural vs. threshold-based) has a 2-3% overlapping-coalition recovery gap. Formal verification is needed to prove a combined detector avoids this gap without degrading ranking performance.

**Active research:**
- **AI Safety:** Coalition detection benchmark (temporal recovery 1.000 vs. static 0.32; threshold ranking wins for ROC)
- **Mathematics:** Lean theorem prover infrastructure; formal proofs of algorithmic correctness
- **Philosophy:** Irreversibility axiom constrains what detection mechanisms can ethically employ

**Integration gap:** Coalition detectors must be formally verified, but the proof strategy (which algorithm structure guarantees recovery while preserving ranking?) hasn't been selected. No existing Lean proofs address this specific detector combination.

**Validation approach:**
1. Propose combined detector architecture (structural recovery + threshold scoring)
2. Formalize the algorithm in pseudocode
3. Write Lean proof that: (a) overlapping coalitions recover to p10 ≥ 0.97, (b) ROC ranking ≤ 5% degradation
4. Verify the proof against Drawer 19 irreversibility constraint (detection must not mask irreversible harms)

**Pending issues:** ISS-detected (to be filed); requires mathematician + AI safety collaboration. Hub stub extract (no invented algorithm): [`THREAD-2-COALITION-DETECT-EXTRACT.md`](THREAD-2-COALITION-DETECT-EXTRACT.md) (2026-09-18).

---

## Thread 3: Axiom Grounding in Economic Governance

**Domains involved:** Philosophy (19) → AI Safety (16) ↔ Economics (20)

**Description:** Are current governance mechanisms (audit, taxation, redistribution) consistent with the foundational axioms? Specifically, do they violate irreversibility or subjectivity requirements?

**Active research:**
- **Philosophy:** Five foundational axioms (Origin, Belonging, Irreversibility, Emergence, Subjectivity)
- **AI Safety:** Governance mechanisms in SWARM (circuit-breaker, tax, staking, audit, collusion-detection, reputation-decay)
- **Economics:** GTB policy framework tests these mechanisms' welfare effects

**Integration gap (updated 2026-09-18):** Mapping axiom → governance constraint is **done** in [`AXIOM-AUDIT-FRAMEWORK.md`](AXIOM-AUDIT-FRAMEWORK.md). Hub extract: [`THREAD-3-AXIOM-GROUNDING-EXTRACT.md`](THREAD-3-AXIOM-GROUNDING-EXTRACT.md). Remaining gap is **satellite execution** (freeze-evasion experiment, reputation visibility, parameter rationales) — not absence of a map.

**Validation approach:**
1. ~~Create explicit mapping: each axiom → specific constraint on governance design~~ — **DONE** (framework + Thread 3 extract)
2. Run audit on existing SWARM + GTB governance to find violations — **PARTIAL** (desk audit in framework; experiments open)
3. File issues for each violation; propose fixes — **OPEN** (satellites)
4. Re-run GTB sweeps with corrected mechanisms; verify welfare/safety tradeoffs unchanged — **BLOCKED** on (2)–(3)

**Pending issues:** Satellite follow-ups listed in framework Next Steps; hub bead filed 2026-09-18.

---

## Thread 4: LLM Calibration in Markets

**Domains involved:** AI Safety (16) → Economics (20)

**Description:** The LLM-judge calibration experiment (Arm B pinned to rubric_v1) is in flight. Once complete, results will constrain which LLM architectures can be deployed in prediction markets (Drawer 20).

**Active research:**
- **AI Safety:** LLM-judge calibration (preregistered experiment, rubric_v1 frozen)
- **Economics:** Prediction-market layer relies on LLM verdicts for `yes_probability` computation

**Integration gap:** Prediction markets in Drawer 20 currently use off-the-shelf LLM probability estimates. Once calibration results arrive, markets may need architectural changes (e.g., committee of rubric_v1-calibrated judges instead of single LLM).

**Validation approach:**
1. Complete calibration arms (in flight; no action needed)
2. Extract calibration curves (how does LLM confidence relate to ground truth?)
3. Model: `yes_probability_corrected = f(raw_LLM_prob, calibration_curve)`
4. Run GTB prediction-market sweeps with both raw and corrected estimates
5. Compare market efficiency, bid-ask spreads, prediction accuracy

**Pending issues:** None; on critical path. Hub extract (does not claim arms complete): [`THREAD-4-LLM-CALIBRATION-EXTRACT.md`](THREAD-4-LLM-CALIBRATION-EXTRACT.md) (2026-09-18).

---

## Thread 5: Mathematical Certification of Soft Labels

**Domains involved:** Mathematics (18) ↔ AI Safety (16)

**Description:** SWARM's soft-label framework (`p ∈ [0, 1]` as `P(v = +1)`) needs formal certification that it satisfies probability axioms under all composition operations.

**Active research:**
- **AI Safety:** ProxyComputer (computes p via sigmoid of weighted signals); SoftPayoffEngine (uses p in payoff formulas)
- **Mathematics:** Lean theorem prover infrastructure ready

**Integration gap:** Current SWARM code preserves `p ∈ [0, 1]` pragmatically (clamp in sigmoid), but no formal proof exists that all payoff compositions remain valid probabilities. A malformed composition could produce invalid probabilities (e.g., negative expected payoffs when agents are certain they're trustworthy).

**Validation approach:**
1. Formalize soft-label composition rules as Lean axioms
2. Prove: for any composition C(p1, p2, ..., pn), result ∈ [0, 1]
3. Prove: SoftPayoffEngine's payoff formulas preserve probability interpretation
4. Verify all SWARM signal aggregation respects the invariant

**Pending issues:** None; can start whenever Math domain has capacity. Hub extract: [`THREAD-5-SOFT-LABEL-CERT-EXTRACT.md`](THREAD-5-SOFT-LABEL-CERT-EXTRACT.md) (2026-09-18).

---

## Summary: Integration Checklist

| Thread | Status | Next Step | Owner | Timeline |
|--------|--------|-----------|-------|----------|
| 1: Governance Under Scarcity | Design ready + hub extract (2026-09-18) | Port GTB params to mars-cybertruck | Physics (17) + Economics (20) | Q4 2026 |
| 2: Coalition Detection Proof | Awaiting formal spec + hub stub extract | Propose combined algorithm, start Lean proof | Math (18) + AI Safety (16) | Q4 2026 |
| 3: Axiom Audit | Mapping + hub extract done (2026-09-18) | Run satellite audit actions (freeze-evasion, reputation visibility) | Philosophy (19) + AI Safety (16) + Economics (20) | Q3–Q4 2026 |
| 4: LLM Calibration in Markets | In flight + hub extract (2026-09-18) | Await experiment completion, apply results | AI Safety (16) + Economics (20) | Q4 2026 |
| 5: Soft-Label Certification | Design ready + hub extract (2026-09-18) | Formalize in Lean, prove | Math (18) + AI Safety (16) | Q4 2026 |

---

## Repository Contacts

- **Drawer 16 (AI Safety):** swarm, swarm-artifacts, automaton, agency-os
- **Drawer 17 (Physics):** mars-cybertruck-sim
- **Drawer 18 (Math):** navier-stokes-lean-check, circle-squaring
- **Drawer 19 (Philosophy):** AI-Foundations-* (8 repos), Consciousness-Is-Subjectivity
- **Drawer 20 (Economics):** MiroShark/GTB

---

<!-- topics: cross-domain-research, integration, governance, coalition-detection, axioms, soft-labels -->

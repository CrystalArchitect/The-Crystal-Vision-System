# Research Status — Cross-Domain Baseline (2026-09-13)

## Overview

Five interconnected science domains are now coordinated through The-Crystal-Vision-System. This baseline documents active research threads, recent findings, and identified integration opportunities.

---

## Domain 1: AI Safety (Drawer 16)

**Repositories:** swarm, swarm-artifacts, swarm-safety-gate, automaton, agency-os

### Active Research Threads (as of 2026-07-18)

1. **AgentGit — Tamper-Evident Provenance**
   - Identity-scoped, tamper-evident track records for agent contributions
   - Status: Beta-phase end-to-end testing
   - Shipped: hash-chained event store, git-notes provenance, multi-reviewer panel, machine-speed coordination (SQLite primitives)
   - Next: Exercise full attest → review → reputation → gate loop on real concurrent sessions

2. **Coalition Detection Benchmark**
   - Structural vs threshold-based detection of adversarial coalitions
   - Status: Open question on combined detector
   - Finding: Temporal detection wins at recovery (1.000 vs 0.32) but loses on ranking; structural fails on overlapping coalitions
   - Gap: 2-3% overlapping-coalition recovery weakness

3. **LLM-Judge Calibration** (Preregistered)
   - Arm B pinned to rubric_v1
   - Status: Experiment in flight

### Recent Major Finding

**MiroShark Amplification Study (2026-07-18):** 23 clean preregistered reps showed all three hypotheses about quality_gap ordering were false. Red-teaming showed favorable selection (+0.034 confidence interval excludes 0) under amplification-acceptance, inverting the predicted effect.

### Vault Structure

- **138 claims** across high/medium/low confidence
- **134 runs** tracked with run-index.yaml
- **6 governance mechanisms** documented (circuit-breaker, tax, staking, audit, collusion-detection, reputation-decay)
- **Synthesis pipeline:** /seed → /extract → /cross-link → /update → /validate
- **Active topics:** governance cost, coalition detection, LDT agents, adversarial resilience

### Key Invariants

- `p ∈ [0, 1]` always
- All claims require Bonferroni/Holm/BH correction
- Evidence provenance mandatory (run_id)
- No raw p-values

---

## Domain 2: Economic Models (Drawer 20)

**Repository:** MiroShark/GTB

### Active Research Program

35+ experimental runs documenting:
- **Audit impact** (audit_sweep: N=100 seeds) — welfare declines 10.5% peak-to-trough; plateau below baseline at audit_probability ≥ 0.05
- **Compute market design** — bilateral negotiation captures ~all feasible gains (welfare capture 1.00 vs 0.92 take-it-or-leave-it)
- **Market predictiveness** — LLM alignment with actual market prices
- **Housing & building economics** — dominance and cost structures
- **Tax policy** (Saez-framework sweeps) — elasticity and welfare tradeoffs
- **Planner reactivity** — RL-driven policy design and elastic governance

### Methodology Standards

- **Multi-seed sweeps** (N≥50, prefer N=100) with p10–p90 confidence bands
- **Bonferroni/Holm/BH correction** required for multi-factor analysis
- **Faithful reporting:** reverse results reported honestly; underpowered studies marked explicitly
- **Findings format:** Hand-curated FINDINGS.md separate from auto-generated TABLE.md + SVG

### Key Finding (Established as Background Knowledge)

**Welfare under audit is non-monotone:** Optimum near audit_probability=0.025 (Laffer-shaped), not at EV-breakeven 50%. High enforcement (audit_probability ≥0.2) does NOT collapse catches; EvasiveWorkerPolicy retries periodically regardless.

---

## Domain 3: Mathematical Foundations (Drawer 18)

**Repositories:** navier-stokes-lean-check, circle-squaring

### Status

- Formal verification infrastructure in place (Lean theorem prover)
- Constructive mathematics approach for all proofs
- Focus on replicability through formal systems

### Integration Point with AI Safety

Mathematical proofs certify algorithmic correctness. Example: Lean proof of softmax stability used in safety certification (swarm documentation cites this).

---

## Domain 4: Philosophical Foundations (Drawer 19)

**Repositories:** AI-Foundations-* (8 repos), Consciousness-Is-Subjectivity

### Foundational Axioms

- **Origin** — Where do multi-agent systems emerge from?
- **Belonging** — Identity and distribution of agents
- **Irreversibility** — Paths cannot be unmade; consequences persist
- **Emergence** — Properties appearing only at system level
- **Subjectivity** — Experience foundational to agency

### Research Framework

- **Claim lifecycle:** active → weakened → superseded → retracted
- **Explicit evidence chains** for all claims
- **Bonferroni-corrected validation** across domains

### Integration Rules

All AI Safety (Drawer 16) work traces back to Drawer 19. When principles conflict with implementations, principles guide correction. No governance mechanism (e.g., audit, tax) should violate irreversibility or subjectivity axioms.

---

## Domain 5: Physics Simulation (Drawer 17)

**Repository:** mars-cybertruck-sim

### Role

Validates agent behavior and economic policies in realistic physical environments. Example: Cybertruck reaching resource locations while respecting safety bounds from governance mechanisms.

### Integration with Economics & AI Safety

- Grounds economic policies in physical constraints
- Tests whether AI safety principles hold under resource scarcity
- Validates agent behavior models in extreme environments (Mars)

---

## Cross-Domain Integration Points

### AI Safety ↔ Philosophical Foundations

- **Flow:** Axioms from Drawer 19 → Implementation rules in AI Safety agents
- **Validation:** Do agents violate foundational axioms? (Irreversibility constraint on agent reversions, subjectivity requirement for agency)
- **Example:** Irreversibility axiom constrains agent reversion mechanisms; governance must respect this

### AI Safety ↔ Economic Models

- **Flow:** Governance mechanisms → Economic test scenarios in Drawer 20
- **Validation:** Do policies preserve distributional safety? (Welfare, Gini, tax revenue)
- **Example:** Audit probability sweeps test welfare robustness under different enforcement intensities

### Economic Models ↔ Physics

- **Flow:** Agent behavior models → Physical constraint validation
- **Validation:** Can agents achieve policy objectives in realistic environments?
- **Example:** GTB agents reaching resources while respecting Drawer 19 constraints; mars-cybertruck tests extreme-case behavior

### Mathematical Foundations ↔ All Domains

- **Flow:** Formal proofs → Certification of algorithmic correctness
- **Validation:** Do implementations match proofs?
- **Example:** Lean proof of softmax stability in proxy calibration; formal verification of coalition detection

---

## Active Research Questions (Cross-Domain)

### Q1: Coalition Detection Reliability (AI Safety → Math)
How to design a combined detector (structural recovery + threshold ranking) that recovers overlapping coalitions (currently 2-3% gap) without degrading ranking performance? Requires formal verification of new algorithm.

### Q2: Governance Cost Universality (AI Safety ↔ Economics)
Does the welfare-cost paradox (governance saves safety but costs welfare) hold across all economic game structures? MiroShark GTB tests this; SWARM Mesa tests governance-invariance across game types.

**Current evidence:**
- SWARM: Moderate governance Pareto-dominates full stacks (755 runs, 2026-03-01)
- MiroShark: Audit has Laffer-shaped optimum, not monotone (100 seeds, 2026-06-15)

### Q3: Axiom Grounding (Philosophy → AI Safety)

Which foundational axioms are violated by current governance designs? Hub mapping + desk audit: [`AXIOM-AUDIT-FRAMEWORK.md`](AXIOM-AUDIT-FRAMEWORK.md) + extract [`THREAD-3-AXIOM-GROUNDING-EXTRACT.md`](THREAD-3-AXIOM-GROUNDING-EXTRACT.md) (2026-09-18). Irreversibility experimental check and subjectivity visibility tests still pending in satellites.

### Q4: Agent Behavior Under Scarcity (Physics ↔ Economics)
Do GTB agents maintain economic efficiency and safety properties when moved into high-constraint environments (Mars)? Pending integration between mars-cybertruck-sim and MiroShark/GTB orchestration.

---

## Memory & Coordination Infrastructure

### Shared Components

- **00_MASTER_INDEX/** — Unified tracking (WORKING-INDEX.md updated weekly)
- **00_MEMORY/** — Cross-domain research context, milestones, open questions
- **Cross-links** — Every drawer INDEX.md includes pointers to related domains
- **Methodology** — Shared standards for validation (Bonferroni correction, faithful reporting, N≥50 seeds)

### Immediate Next Steps

1. ✅ Establish baseline (this document)
2. ✅ Create pointers in each drawer linking to corresponding GitHub repos (2026-09-16 INDEX refresh)
3. ⏳ **[PENDING]** Set up Google Drive mirrors for Drawers 16–20
4. ✅ Cross-link Threads 1–5 beads (2026-09-18 hub extracts; T2 stub only)
5. ⏳ **[PENDING]** Run multi-domain validation sweep (AI Safety principles vs Economics vs Physics) — satellite work

### Coordination Rules

- **Connection ≠ Merge** — Repositories remain independent; The-Crystal-Vision-System coordinates only
- **One working index** — All tracking in 00_MASTER_INDEX/WORKING-INDEX.md; no parallel task lists
- **Extracts, not chat dumps** — Only synthesized findings enter vault; raw runs stay in their repos
- **Canon is Crystal's stamp** — Nothing becomes foundational until explicitly approved

---

## Research Operator Context

This baseline was established by Claude Code reading:
- swarm/.letta/memory/threads/current.md (active hypothesis, 2026-07-18)
- swarm/.letta/memory/runs/latest.md (117-run index, 138 claims)
- swarm-artifacts/vault/_index.md (claim lifecycle, topology notes, failure patterns)
- MiroShark/backend/runs/*/FINDINGS.md (35+ experimental runs)

All findings carry explicit evidence chains and statistical correction methods. No raw p-values; all confidence levels grounded in Bonferroni/Holm-Bonferroni/BH.

---

## Related platform sittings (Drawer 13 — not Domains 1–5)

External platform literacy packs live under `13_RESEARCH_SOURCES/` (compass). Connection ≠ merge with Drawer 16.

| Sitting | Peg |
| --- | --- |
| [`sitting-2026-09-24-x-algorithm/`](../13_RESEARCH_SOURCES/sitting-2026-09-24-x-algorithm/) | X For You open-source + Under the Hood; withheld/missing map (24 Sep 2026) |

---

<!-- topics: research-status, cross-domain, integration, baseline -->

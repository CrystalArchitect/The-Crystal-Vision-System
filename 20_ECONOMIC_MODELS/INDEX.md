# Drawer 20: Economic Models

**Canon:** **no**  
**Updated:** 2026-09-18 AEST  
**Rule:** Connection ≠ merge — satellite is a **fork-mirror**.

## Overview

Agent-based economic simulation and policy modeling in stylized worlds. Drawer points at the CrystalArchitect mirror of MiroShark / GTB.

## Repositories (CrystalArchitect URLs)

### Core Models

- **MiroShark** — [https://github.com/CrystalArchitect/MiroShark](https://github.com/CrystalArchitect/MiroShark)  
  **fork-mirror** of `swarm-ai-research/MiroShark`. GTB (Gather-Trade-Build) economic world; AI Economist gridworld (vendored relationship to swarm); LLM-driven worker personas; prediction-market layer; policy evaluation framework.

## Research Focus

- **Agent-Based Economics** — Policies tested on diverse agent populations
- **Governance Mechanisms** — Audit systems, tax policies, redistribution
- **Market Design** — Trading, negotiation, and price discovery
- **Welfare Analysis** — Gini coefficient, total welfare, distributional effects
- **Prediction Markets** — Polymarket-shaped envelopes for consensus measurement

## Key Experiments (extract pointers — not Canon)

### Audit Sweep (N=100 seeds)

- Welfare declines steeply in audit_probability up to ~0.2
- Peak-to-trough welfare cost: 10.5%
- Plateau below no-audit baseline for audit_probability ≥ 0.05

### Compute Market Study

- Bilateral negotiation captures ~all feasible gains-from-trade (welfare capture 1.00 vs 0.92)
- Fills 0.50 vs 0.34 of drawn encounters vs take-it-or-leave-it pricing
- Selection artifacts explain realized-rate / surplus-share gaps

### Persona Alignment

- Without explicit contrarian agents, LLM populations produce one-sided markets
- `yes_probability` becomes sentiment poll, not forecast
- Balanced lineup required for meaningful prediction markets

## Methodology

- Multi-seed sweeps (N≥50, prefer N=100) with p10–p90 confidence bands
- Bonferroni/Holm-Bonferroni/BH correction for multiple comparisons
- Faithful reporting: reverse results reported honestly
- Minimal runs indicate "underpowered" status; never omit

## Cross-domain bead (Thread 3)

GTB/MiroShark side of axiom grounding:

- Extract: [`../00_MEMORY/THREAD-3-AXIOM-GROUNDING-EXTRACT.md`](../00_MEMORY/THREAD-3-AXIOM-GROUNDING-EXTRACT.md)
- Framework open actions include freeze-evasion irreversibility check and tax-bracket rationales (run in MiroShark, not here)

## Cross-Links

- [[16_AI_SAFETY_RESEARCH]] — Safety under economic pressure
- [[19_PHILOSOPHICAL_FOUNDATIONS]] — Foundational axioms for economics
- [[00_MASTER_INDEX]] — Coordination hub
- [[00_MEMORY/THREAD-3]] — Axiom grounding extract (Canon: no)

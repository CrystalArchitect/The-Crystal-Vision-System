# Drawer 20: Economic Models

## Overview
Agent-based economic simulation and policy modeling in stylized worlds.

## Repositories

### Core Models
- **MiroShark** (with GTB - Gather-Trade-Build economic world)
  - AI Economist gridworld (vendored from swarm-ai-research/swarm)
  - LLM-driven worker personas
  - Auto-derived prediction-market layer
  - Economic policy evaluation framework

## Research Focus

- **Agent-Based Economics** — Policies tested on diverse agent populations
- **Governance Mechanisms** — Audit systems, tax policies, redistribution
- **Market Design** — Trading, negotiation, and price discovery
- **Welfare Analysis** — Gini coefficient, total welfare, distributional effects
- **Prediction Markets** — Polymarket-shaped envelopes for consensus measurement

## Key Experiments

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

## Cross-Links

- [[16_AI_SAFETY_RESEARCH]] — Safety under economic pressure
- [[19_PHILOSOPHICAL_FOUNDATIONS]] — Foundational axioms for economics
- [[00_MASTER_INDEX]] — Coordination hub

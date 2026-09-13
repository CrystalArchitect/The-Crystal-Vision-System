# Drawer 16: AI Safety Research

## Overview
Distributed AI safety research examining emergent failures in multi-agent systems.

## Repositories

### Core Framework
- **swarm** (`github.com/swarm-ai-research/swarm`)
  - Multi-agent simulation with soft labels and probabilistic metrics
  - SoftPayoffEngine, SoftMetrics, ProxyComputer
  - Research memory system with vault, claims, experiments

### Safety Infrastructure
- **swarm-artifacts** (`github.com/swarm-ai-research/swarm-artifacts`)
  - Artifact store and knowledge vault
  - Run database, claims lifecycle, experiment notes
  - Ars Contexta methodology for research management

- **swarm-safety-gate** 
  - Safety evaluation framework for agent populations

### Agent Systems
- **automaton** — autonomous agent framework
- **agency-os** — distributed agent operating system

## Research Methodology

- **Soft Labels**: Probabilistic `p = P(v = +1)` instead of binary good/bad
- **Metrics**: Toxicity, quality gap, adverse selection, conditional loss
- **Scenarios**: Baseline, economic models, governance mechanisms
- **Validation**: Multi-seed sweeps (N≥50), Bonferroni correction, effect sizes

## Key Findings

- Welfare declines steeply in audit_probability up to ~0.2, plateaus below baseline
- Tax revenue is Laffer-shaped, peaking near audit_probability=0.025
- Bilateral negotiation captures ~all feasible gains-from-trade vs posted-price mechanisms
- Persona-aligned LLM populations produce one-sided markets without explicit contrarian agents

## Active Research Threads

- Collusion detection and prevention
- Governance mechanism design
- Market efficiency under soft-label evaluation
- Agent learning and strategy evolution

## Cross-Links

- [[19_PHILOSOPHICAL_FOUNDATIONS]] — AI foundation principles
- [[20_ECONOMIC_MODELS]] — GTB world model
- [[00_MASTER_INDEX]] — Coordination hub

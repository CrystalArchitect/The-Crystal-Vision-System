# Drawer 16: AI Safety Research

**Canon:** **no**  
**Updated:** 2026-09-18 AEST  
**Rule:** Connection ≠ merge — satellites are **fork-mirrors** unless noted.

## Overview

Distributed AI safety research examining emergent failures in multi-agent systems. This drawer **points at** CrystalArchitect mirrors; it does not host living upstream trees.

## Repositories (CrystalArchitect URLs)

### Core Framework

- **swarm** — [https://github.com/CrystalArchitect/swarm](https://github.com/CrystalArchitect/swarm)  
  **fork-mirror** of `swarm-ai-research/swarm`. Multi-agent simulation with soft labels and probabilistic metrics (SoftPayoffEngine, SoftMetrics, ProxyComputer); research memory vault / claims / experiments.

### Safety Infrastructure

- **swarm-artifacts** — [https://github.com/CrystalArchitect/swarm-artifacts](https://github.com/CrystalArchitect/swarm-artifacts)  
  **fork-mirror** of `swarm-ai-research/swarm-artifacts`. Artifact store and knowledge vault; run DB; Ars Contexta methodology.

- **swarm-safety-gate** — [https://github.com/CrystalArchitect/swarm-safety-gate](https://github.com/CrystalArchitect/swarm-safety-gate)  
  **fork-mirror** of `swarm-ai-research/swarm-safety-gate`. Safety evaluation framework for agent populations.

- **swarmgym** — [https://github.com/CrystalArchitect/swarmgym](https://github.com/CrystalArchitect/swarmgym)  
  **fork-mirror** of `swarm-ai-research/swarmgym`.

### Agent Systems

- **automaton** — [https://github.com/CrystalArchitect/automaton](https://github.com/CrystalArchitect/automaton)  
  **fork-mirror** of `Conway-Research/automaton`. Autonomous agent framework.

- **agency-os** — [https://github.com/CrystalArchitect/agency-os](https://github.com/CrystalArchitect/agency-os)  
  **fork-mirror** of `swarm-ai-research/agency-os`. Distributed agent operating system.

### Related runtimes (same science neighborhood)

- **aeon** — [https://github.com/CrystalArchitect/aeon](https://github.com/CrystalArchitect/aeon) — **fork-mirror** of `swarm-ai-research/aeon`
- **aeon-atlas** — [https://github.com/CrystalArchitect/aeon-atlas](https://github.com/CrystalArchitect/aeon-atlas) — **fork-mirror** of `swarm-ai-research/aeon-atlas`

## Research Methodology

- **Soft Labels**: Probabilistic `p = P(v = +1)` instead of binary good/bad
- **Metrics**: Toxicity, quality gap, adverse selection, conditional loss
- **Scenarios**: Baseline, economic models, governance mechanisms
- **Validation**: Multi-seed sweeps (N≥50), Bonferroni correction, effect sizes

## Key Findings (extract pointers — not Canon)

- Welfare declines steeply in audit_probability up to ~0.2, plateaus below baseline
- Tax revenue is Laffer-shaped, peaking near audit_probability=0.025
- Bilateral negotiation captures ~all feasible gains-from-trade vs posted-price mechanisms
- Persona-aligned LLM populations produce one-sided markets without explicit contrarian agents

## Active Research Threads

- Collusion detection and prevention
- Governance mechanism design
- Market efficiency under soft-label evaluation
- Agent learning and strategy evolution
- **Thread 1** — [`../00_MEMORY/THREAD-1-GOVERNANCE-SCARCITY-EXTRACT.md`](../00_MEMORY/THREAD-1-GOVERNANCE-SCARCITY-EXTRACT.md)
- **Thread 2** (stub) — [`../00_MEMORY/THREAD-2-COALITION-DETECT-EXTRACT.md`](../00_MEMORY/THREAD-2-COALITION-DETECT-EXTRACT.md)
- **Thread 3** — [`../00_MEMORY/THREAD-3-AXIOM-GROUNDING-EXTRACT.md`](../00_MEMORY/THREAD-3-AXIOM-GROUNDING-EXTRACT.md); audit: [`../00_MEMORY/AXIOM-AUDIT-FRAMEWORK.md`](../00_MEMORY/AXIOM-AUDIT-FRAMEWORK.md)
- **Thread 4** — [`../00_MEMORY/THREAD-4-LLM-CALIBRATION-EXTRACT.md`](../00_MEMORY/THREAD-4-LLM-CALIBRATION-EXTRACT.md)
- **Thread 5** — [`../00_MEMORY/THREAD-5-SOFT-LABEL-CERT-EXTRACT.md`](../00_MEMORY/THREAD-5-SOFT-LABEL-CERT-EXTRACT.md)

## Cross-Links

- [[19_PHILOSOPHICAL_FOUNDATIONS]] — AI foundation principles
- [[20_ECONOMIC_MODELS]] — GTB world model
- [[17_PHYSICS_SIMULATION]] — Embodied scarcity tests (Thread 1)
- [[18_MATHEMATICAL_FOUNDATIONS]] — Soft-label / coalition proofs (Threads 2, 5)
- [[00_MASTER_INDEX]] — Coordination hub
- [[00_MEMORY]] — Thread beads 1–5 (Canon: no)

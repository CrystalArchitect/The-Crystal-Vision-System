# 05 — Technical Brief

**CrystalCore as Multiplanetary Intelligence Layer**  
**TerAustralis Incognita**

---

## Design Premise

Multiplanetary operations impose constraints that Earth-centric intelligence architectures handle poorly:

- High and variable latency
- Intermittent or contested connectivity
- Long periods of isolation
- Need for local decision-making that remains coherent with human intent and continuity

CrystalCore is designed from first principles for this regime.

---

## Core Properties

These are the architecture's design targets. Current build status against each is tracked plainly in [Document 13 — What Is Built](13-WHAT-IS-BUILT.md); nothing below should be read as flight-proven.

**Local-first**  
Primary intelligence and memory reside on the local substrate. Continuous external dependency is not required for core function.

**Consent-native**  
Significant actions and modifications to continuity-critical memory require valid, current consent tokens. The consent gate is fail-closed and revocable at runtime — implemented, tested, and re-verified at repository head (Document 13).

**Auditable**  
Decision paths and memory operations remain inspectable by the authorised human operator. The message bus rejects any claim that does not declare its evidence layer; gate decisions are logged today.

**Fail-safe isolation** — *design target, not yet demonstrated*  
When external links degrade or are compromised, the system is designed to default to local isolation rather than fail-open behaviour. This is architecture, not a tested behaviour: no isolation-under-sustained-link-loss test exists yet.

**Continuity-preserving** — *design target*  
Continuity of decision-making, memory, and agency is treated as a hard constraint the architecture is built around. Full end-to-end continuity guarantees remain in progress.

**Distance-as-normal**  
High latency is assumed as the operating condition, not treated as an error state.

Document 12 states the honest summary plainly: CrystalCore is *"operating at prototype scale, honestly labelled."*

---

## Orchestration Architecture: Behavior Trees over Finite State Machines

For the control and orchestration of agent behaviours and synthetic decision processes, CrystalCore prefers **Behavior Tree (BT)** architecture over legacy Finite State Machine (FSM) frameworks.

**Rationale:**

- BTs provide superior modularity. New corrective, ethical, or safety subroutines can be inserted hierarchically without requiring a full logic rewire.
- FSMs become brittle as state and transition complexity grows. Adding a single pre-condition or corrective check often forces tangled new transitions across the graph.
- In high-latency and isolation conditions, the ability to dynamically insert checks (for example: consent validation, grasp/validity equivalents, continuity integrity tests) without destabilising the whole system is an operational requirement, not a convenience.

**Design implication for CrystalCore:**  
Orchestration layers should be structured so that consent gates, continuity checks, and fail-safe isolations can be added or refined as modular subtrees. This keeps the architecture adaptable under unexpected conditions while preserving the hard constraints defined in the First Principles.

---

## Comparison: Two Families, One Gap

The existing landscape splits into two families. Neither occupies the position this architecture targets.

### Family 1 — Contemporary agent frameworks

LangGraph, CrewAI, Microsoft Agent Framework (formerly AutoGen), SuperAGI and their peers solve orchestration: graph-structured or role-structured coordination of multiple agents, model-agnostic at the interface.

Their shared assumptions are the problem here, not their quality:

- Reachable model endpoints are assumed. Model-agnostic is not the same as link-agnostic.
- Managed cloud deployment is the default path, with self-hosting a secondary option.
- Behaviour under sustained link loss is degradation, not designed isolation.

Framework churn is itself a continuity risk worth naming: AutoGen has moved into maintenance and merged into Microsoft Agent Framework 1.0 ([GA April 2026](https://www.langchain.com/resources/ai-agent-frameworks)), and SuperAGI — 17.6k stars, MIT licensed — last saw a commit to `main` in [January 2025](https://github.com/TransformerOptimus/SuperAGI/commits/main). Architectures intended to carry continuity across decades cannot rest on a layer with that half-life.

### Family 2 — Flight software and spacecraft autonomy

This family already operates under the conditions in question, and does so successfully.

- **F Prime** (JPL, 2013; open-sourced 2017) decomposes flight software into discrete components with well-defined interfaces, over a C++ framework supplying message queues and threading. It flew on Ingenuity. ([JPL](https://www.jpl.nasa.gov/news/meet-the-open-source-software-powering-nasas-ingenuity-mars-helicopter/))
- **cFS** (NASA Goddard) layers a Platform Support Package, an OS Abstraction Layer, and Core Flight Executive services; flown on Lunar Reconnaissance Orbiter and GPM. The cFS 2.0 roadmap adds plug-and-play capability for in-space robotics, distributed computing, spacecraft autonomy and onboard machine learning. ([coreflightsystem.net](https://www.coreflightsystem.net/))
- **MEXEC** (JPL) integrates planning and execution in a models-based scheduler and executive, with tighter planner/executive coupling than procedural alternatives. ([JPL AI Group](https://ai.jpl.nasa.gov/public/documents/papers/IntEx-2020-MEXEC.pdf))
- **CASPER** flew on EO-1, performing onboard detection of thermal anomalies and autonomously replanning follow-up observations.

What this family does not attempt: general adaptive reasoning, and the preservation of a human operator's memory, agency, and continuity as a protected property. These systems are deterministic and mission-specific by design. That is a strength for their purpose, not a deficiency — but it leaves the intelligence layer unfilled.

### Family 3 — Local-first open-source stacks

The closest existing work to this architecture, and the most direct challenge to any novelty claim it makes. Ettore Di Giacinto's projects, all Go, all open source, all actively maintained:

- **LocalAI** (~48k stars) — an open-source inference engine running LLM, vision, voice, image and video models on commodity hardware, no GPU required
- **LocalAGI** (~1.9k) — a self-hostable agent platform, positioned as a privacy-preserving alternative to hosted response APIs
- **LocalRecall** (~934) — a memory and knowledge-base layer for agents
- **edgevpn** (~2k) — decentralised peer-to-peer networking with no central servers and token-gated shared tunnels
- **kairos** (~1.8k) — an immutable Linux distribution for edge deployment

Taken together these already supply local inference without external dependency, persistent agent memory, token-gated peer transport, and an immutable edge substrate. That is most of the physical stack this brief describes.

**The honest position:** this is candidate substrate, not competition. Building a parallel implementation of what LocalAI already does well would be reinvention of precisely the kind rejected above. The layer that remains genuinely unfilled is narrower than "a local-first intelligence system," and is better stated narrowly:

- **Consent as an enforced runtime primitive** — not a privacy posture or a deployment choice, but a gate that significant actions and continuity-critical memory writes must pass, with revocation that takes effect at runtime.
- **Continuity as a hard architectural constraint** — memory, agency and decision coherence as protected properties with explicit guarantees, rather than features that happen to persist.
- **Fail-safe semantics defined as isolation** — a specified and tested behaviour on link loss, not an emergent consequence of running locally.

Local-first is a precondition for these. The projects above supply it. It is not by itself the contribution.

### The gap

| | Local-first / fail-safe | Adaptive reasoning | Consent &amp; continuity as hard constraints |
|---|---|---|---|
| Agent frameworks | No | Yes | No |
| Flight software / autonomy | Yes | Limited by design | Not their purpose |
| Local-first open-source stacks | Local-first yes; isolation semantics unspecified | Yes | Partial — privacy posture, not enforced primitive |
| CrystalCore | Yes | Yes | Yes |

The operating condition is not hypothetical: Mars round-trip light time runs roughly 8 to 48 minutes depending on orbital geometry, and a Uranus mission faces about 5.5 hours two-way. Under those constraints an architecture that treats link loss as an error state is mismatched to the domain.

### Stated honestly

F Prime and cFS are flight-proven. CrystalCore is not. The claim here is architectural fit, not flight heritage, and the distinction matters.

The corollary is that where these families already solve a problem well, the correct move is adoption rather than reinvention. F Prime's component decomposition and MEXEC's planner/executive coupling are considerably closer to the Behavior Tree orchestration described above than anything in the contemporary LLM agent stack — and are the more useful prior art for this work.

The same applies to Family 3 more sharply still. The realistic path is CrystalCore's consent, continuity and isolation semantics implemented **on** a local-first substrate that already exists and is maintained, rather than a parallel stack built to reach the same starting line.

---

## Role in the Larger Architecture

CrystalCore is the intelligence counterpart to geographic and industrial redundancy.  
Where the southern node supplies physical recovery, feedstock, and energy capacity, CrystalCore supplies the decision and continuity layer that remains functional when links are thin or broken.

The preference for Behavior Tree-style orchestration directly supports the requirement that ethical and continuity constraints remain enforceable and extensible without system-wide fragility.

---

**All rights reserved.**  
TerAustralis Incognita — ABN 70 741 068 059

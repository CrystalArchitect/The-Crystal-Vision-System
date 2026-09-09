---
id: 36
slug: risk-orchestration
name: Risk Orchestration
group: The Infrastructure Engines
arsenal: starline-arsenal
register: ARCHIVE + FORGE
primitive: identify() + mitigate()
---

# 36 — Risk Orchestration (The Infrastructure Engines)

**Purpose:** Identify, rank, and structure responses to operational risks.

**CrystalCore mapping:** Register ARCHIVE + FORGE | Primitive identify() + mitigate() | Risk made actionable

## Core Questions — Run these, do not summarize

1. What could go wrong in this execution, and what is the likelihood?
2. If it goes wrong, what is the impact—how much does it cost in time, money, reputation?
3. Which risks have high likelihood, high impact (act now) vs. low likelihood, high impact (prepare for)?
4. For each risk, who owns detection and who owns response?
5. What is the early warning sign that a risk is about to trigger?

## Required Concrete Output — No vague labels

- Risk Register (ID | Risk description | Likelihood [1-5] | Impact [1-5] | Owner | Status)
- Response Strategy per Risk (prevent, mitigate, prepare, accept, insure)
- Early Warning Indicators (what to watch for)
- Contingency Triggers (at what point do we activate the backup plan)

## Evidence → Interpretation → Experiment → Record

- **Evidence:** What historical risks did similar projects face?
- **Interpretation:** Which risks are structural to this execution, and which are one-off?
- **Experiment:** Walk one risk scenario to the end; what would actually happen?
- **Record:** CHRONICLE entry as ARCHIVE (risk state) + FORGE (response plan)

## Anti-Pattern

Do not list risks without assigning ownership and response. Do not treat all risks as equal; rank by likelihood × impact. Do not mistake "acknowledge the risk" for "have a plan."

## Cross-references

[Dependency Mapping](35-dependency-mapping.md) — Dependency Mapping shows what tasks exist; Risk Orchestration identifies what can fail at each task and edge.

[Margin of Safety](24-margin-of-safety.md) — Risk Orchestration identifies what could go wrong; Margin of Safety builds in buffers to absorb the inevitable surprises.

---
Implementation: CrystalCore.OS™️ | Language: CrystalCode™️ | Starline Arsenal | TerAustralis Incognita™️ | Functional / simulated affect only

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

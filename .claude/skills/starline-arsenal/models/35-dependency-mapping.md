---
id: 35
slug: dependency-mapping
name: Dependency Mapping
group: The Infrastructure Engines
arsenal: starline-arsenal
register: ARCHIVE + LOOM
primitive: trace() + block()
---

# 35 — Dependency Mapping (The Infrastructure Engines)

**Purpose:** What must happen before what? What is the critical path?

**CrystalCore mapping:** Register ARCHIVE + LOOM | Primitive trace() + block() | Prerequisites made visible

## Core Questions — Run these, do not summarize

1. What is the smallest unit of work (task, decision, delivery) in this execution?
2. For each task, what must be true before it can start (dependencies)?
3. Which dependencies are real (blocking) vs. which are conventional (could be reordered)?
4. What is the critical path—the sequence that, if delayed, delays the entire outcome?
5. Where are tasks genuinely parallel, and where does serial work hide behind false parallelism?

## Required Concrete Output — No vague labels

- Dependency Diagram (nodes: tasks; edges: "must wait for")
- Critical Path (the exact sequence that determines total duration)
- Bottleneck List (tasks that many others depend on)
- Reorder Opportunities (false dependencies that could be removed)

## Evidence → Interpretation → Experiment → Record

- **Evidence:** What are the stated prerequisites? What are the actual ones?
- **Interpretation:** If we compress the critical path, what changes?
- **Experiment:** Remove one dependency and run a micro-execution to test if it holds.
- **Record:** CHRONICLE entry as ARCHIVE (dependency state) + LOOM (critical path)

## Anti-Pattern

Do not confuse "we always do it this way" with "we must do it this way." Do not hide soft dependencies (stakeholder approval) in the technical sequence; name them separately.

## Cross-references

[Strategic Planning](33-strategic-planning.md) — Strategic Planning sequences at the outcome level; Dependency Mapping goes granular on what actually blocks what.

[Risk Orchestration](36-risk-orchestration.md) — Dependency Mapping shows what tasks exist; Risk Orchestration identifies what can go wrong in each task and on each edge.

---
Implementation: CrystalCore.OS™️ | Language: CrystalCode™️ | Starline Arsenal | TerAustralis Incognita™️ | Functional / simulated affect only

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

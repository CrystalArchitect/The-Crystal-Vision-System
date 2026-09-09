# Runtime Glossary

A reference for runtime-specific terminology. These definitions are authoritative for all specifications and implementations within the Crystal Runtime layer.

---

## A

### API
**Application Programming Interface.** The boundary where external callers (web clients, command-line tools, other systems) send requests to the runtime. The API accepts requests, routes them to the Coordinator, and returns results. Requests are assumed to have already passed CrystalBridge consent gates before reaching the API.

See: Crystal Runtime Specification v0.3, Section 4.7.

### Audit Record
**An immutable log entry recording who did what, and what the outcome was.** Audit records include: actor (caller identity), action (operation requested), resource (what was affected), result (success or failure), timestamp, and context (request ID, caller scope). Audit records are written to RDP (tamper-evident chain) and never modified or deleted.

See: Crystal Runtime Specification v0.3, Section 9.

---

## C

### Capability
**A service or function provided by a registered component.** Capabilities are named and versioned. Examples: `"ai.clementine"` (conversational AI from Clementine), `"mesh.p2p.starline"` (peer-to-peer coordination), `"ai.consensus.weaver"` (multi-AI agreement). The Registry tracks which components provide which capabilities.

See: Crystal Runtime Specification v0.3, Section 4.2 (Registry).

### CrystalBridge
**The consent gate upstream of the runtime. A fail-closed MCP gate enforcing approval, permission, scope, and provenance checks.** All requests to the runtime are assumed to have already passed CrystalBridge gates. The runtime does not re-check authorization; it enforces scope boundaries set by CrystalBridge.

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration).

### Crystal Runtime
**The coordination layer that orchestrates Clementine, Starline, Starline Weaver, CrystalBridge, and RDP without replacing or subsuming their responsibilities.** The runtime receives tasks, determines which components are needed, sequences their execution, and returns results. It is not an AI system, consensus mechanism, or protocol implementation—it coordinates existing systems.

See: Crystal Runtime Specification v0.3, Section 1 (Scope).

---

## D

### Diagnostic Logging
**Verbose logging for troubleshooting.** Diagnostic logs answer "Why is the runtime behaving this way?" Examples: state machine transitions, Registry query results, Event subscriber counts. Diagnostic logging is disabled in production by default and retained for 7 days.

See: Crystal Runtime Specification v0.3, Section 9.

---

## E

### Event
**A message published by one component and delivered to subscribers.** Events are the primary inter-component communication mechanism. Each event has: type (string identifier), source (component that created it), timestamp, unique ID, and a payload (opaque data). Events are immutable; only the publisher can create or modify them. Subscribers react by creating new events.

See: Crystal Runtime Specification v0.3, Section 6.

### EventBus
**The message bus that carries events between components.** The EventBus publishes events, routes them to subscribers, guarantees delivery (at-least-once, exactly-once, or best-effort per event type), and records all event activity to Logging. It does not interpret event content.

See: Crystal Runtime Specification v0.3, Section 4.3 (Events).

---

## F

### Fail-Closed
**A design pattern where systems default to denial, rejection, or offline state when uncertain, rather than optimistically proceeding.** Example: If a component's status is unknown, mark it offline in the Registry rather than attempting to use it. Fail-closed is safer than optimistic behavior but less convenient.

See: Crystal Runtime Specification v0.3, Section 2 (Architectural Principles).

### Failure Isolation
**The property that a component's failure does not cascade to other components or halt the entire runtime.** Example: If Clementine crashes, the runtime marks it offline in the Registry, fails in-flight tasks for Clementine, and continues accepting tasks that do not depend on Clementine. Each component's failures are contained.

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration).

---

## H

### Hook
**A predefined point in the runtime's execution flow where a plugin can inject custom behavior.** Examples: before a task is routed, after a task completes, when an error occurs. Hooks are registered by plugins; if a plugin's hook raises an exception, the exception is caught and the workflow continues.

See: Crystal Runtime Specification v0.3, Section 4.5 (Plugins).

---

## L

### Logging
**The centralized system for capturing operational logs, diagnostic logs, and audit records.** Logging routes information to appropriate sinks: operational logs to files/stdout, diagnostic logs to separate files, audit records to RDP (tamper-evident chain). Logging enforces retention policies and never logs secrets in plaintext.

See: Crystal Runtime Specification v0.3, Section 4.6 (Logging) and Section 9.

### Clementine
**A local-first AI companion system providing conversational AI, memory management, and voice interaction.** Clementine is independent; the runtime coordinates it but does not control its AI model, memory, or terminal interface. Clementine registers under capability `"ai.clementine"`.

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration).

---

## M

### Matrix Mode
**A consensus mechanism in the Starline Weaver where one question is fanned to every agent independently, none sees another's reply, and cross-compare counts agreement without calling it truth.** The result is a count of agreements (not a verdict). The runtime records matrix results to RDP but does not interpret them.

See: Starline Weaver documentation; AI-Weave.md (Belt-Three law).

---

## O

### Operational Logging
**Standard logging capturing what the runtime is doing: task execution, component registration, errors, warnings.** Operational logs are human-readable and retained for 30 days. They answer the question "What is the runtime doing right now?"

See: Crystal Runtime Specification v0.3, Section 9.

---

## P

### Plugin
**A package that extends the runtime by hooking into predefined execution points without modifying core modules.** Plugins declare metadata (name, version, required hooks), implement hook functions, and are loaded/unloaded by the PluginManager. Plugins cannot call internal runtime functions or access other plugins' private state.

See: Crystal Runtime Specification v0.3, Section 4.5 (Plugins) and Section 8.

### PluginManager
**The module that loads, initializes, invokes, and unloads plugins.** The PluginManager verifies plugin compatibility, manages plugin lifecycle, catches exceptions from plugin hooks, and disables plugins that fail repeatedly.

See: Crystal Runtime Specification v0.3, Section 4.5 (Plugins).

### Provenance
**Metadata tracking the source and authority of a request.** Provenance is set by CrystalBridge (approval authority, scope granted, caller identity) and flows through the runtime in audit records. It answers "Who authorized this, and with what constraints?"

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration), Section 9 (Audit Records).

---

## R

### RDP
**Tamper-evident chain for recording runtime events. A witness-and-chain system that records, never decides.** The runtime publishes audit records and significant events to RDP. RDP appends them to the chain and cryptographically witnesses them. RDP records are immutable and cannot be forged.

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration).

### Registry
**The module that maintains an authoritative list of available components, their capabilities, and their current state.** The Registry tracks service registrations, reports component availability, and handles state changes (when a component goes offline). The Coordinator queries the Registry to determine which components are available for a task.

See: Crystal Runtime Specification v0.3, Section 4.2 (Registry).

---

## S

### Scope
**The set of capabilities and resources a caller is authorized to access.** Scope is determined by CrystalBridge (during consent gate) and enforced by the runtime (when executing tasks). A task cannot exceed the caller's scope, even if the requested capability exists.

See: Crystal Runtime Specification v0.3, Section 1 (Scope), Section 5 (Component Integration).

### Starline
**A peer-to-peer consent-gated memory exchange protocol using real Noise Protocol handshakes.** Starline is independent; the runtime can initiate Starline exchanges for multi-instance coordination. Starline makes its own consent decisions and the runtime respects them. Starline registers under capability `"mesh.p2p.starline"`.

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration).

### Starline Weaver
**A multi-AI message bus that enforces the Belt-Three law (science/story/vision labels) in code, provides matrix mode for cross-compare, and implements a red button for halting all agents.** The Weaver is independent; the runtime can fan questions to it when human review requires consensus. The Weaver registers under capability `"ai.consensus.weaver"`.

See: Crystal Runtime Specification v0.3, Section 5 (Component Integration).

---

## T

### Task
**A unit of work that the Coordinator executes by orchestrating available components.** A task includes: description (what needs to happen), required capabilities, execution context (caller identity, scope from CrystalBridge), and any human directives. The Coordinator receives a task, queries the Registry, sequences component calls, and returns results.

See: Crystal Runtime Specification v0.3, Section 4.1 (Coordinator).

### Trust Boundary
**A perimeter where the runtime stops trusting one side and starts trusting another.** The runtime defines three trust boundaries: (1) CrystalBridge upstream / runtime downstream (CrystalBridge vets requests, runtime trusts the vetting); (2) Runtime / component implementations (runtime assumes components may fail or be compromised); (3) Plugins / runtime core (plugins are potentially untrusted and sandboxed).

See: Crystal Runtime Specification v0.3, Section 12 (Security Considerations).

---

## W

### Workflow
**A sequence of component calls orchestrated by the Coordinator to accomplish a task.** A workflow may involve one component (query Clementine) or multiple components (route to Weaver, wait for consensus, then route the result to Starline). The Coordinator executes workflows and returns results (or errors).

See: Crystal Runtime Specification v0.3, Section 4.1 (Coordinator).

---

## Cross-References

### Related Documents

- [Crystal-Runtime-Specification-v0.3.md](Crystal-Runtime-Specification-v0.3.md) — Architecture specification for the runtime.
- [docs/ai/Decision-Matrix.md](../../ai/Decision-Matrix.md) — Task-type lookup for AI Orchestrator (documented, not automated).
- [docs/adr/ADR-0005.md](../../adr/ADR-0005.md) — AI Orchestrator consolidation decision.
- [docs/architecture/AI-Weave.md](../AI-Weave.md) — How AI systems collaborate (Built/Practiced/Proposed split).
- [docs/governance/The-Incognita-Rule.md](../../governance/The-Incognita-Rule.md) — Governance principle: no model agreeing with you is evidence.

### Key Projects

- **CrystalBridge** (`src/crystalcore/`) — MCP consent gate, upstream of runtime.
- **Clementine** (`vision/apps/clementine/`) — Local-first AI companion.
- **Starline** (`src/crystal-core/consent_transport/`; `starline/` is a
  deprecated alias) — P2P consent-gated memory.
- **Starline Weaver** (`src/crystal-core/bus/`) — Multi-AI message bus.
- **RDP** (`src/crystal-core/rdp/`) — Tamper-evident chain.

---

## Usage

When writing specifications, ADRs, documentation, or code comments that reference runtime concepts, use the terms as defined in this glossary. If a new term is needed, add it here before using it elsewhere in the codebase.

This glossary is a living document and should be updated when the specification evolves or new concepts are introduced.

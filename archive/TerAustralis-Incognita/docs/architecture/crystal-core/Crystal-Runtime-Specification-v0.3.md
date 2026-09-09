# Crystal Runtime Specification v0.3

**Status:** Draft  
**Purpose:** Architecture Specification (Not an Implementation)  
**Date:** 2026-07-23

---

## 1. Scope

### What the Runtime Is

The Crystal Runtime is a coordination layer that orchestrates the interaction between independent systems already built and working: Clementine, Starline, Starline Weaver, CrystalBridge, and RDP.

The runtime does not provide AI capabilities, consensus mechanisms, or protocol implementations. It coordinates existing capabilities, maintains component lifecycle, routes requests to appropriate systems, and provides a unified external interface.

### What It Is Not

- **Not a replacement for Clementine, Starline, Starline Weaver, CrystalBridge, or RDP.** Each retains its responsibility and operates independently.
- **Not an AI orchestrator in the algorithmic sense.** The AI Orchestrator is a documented decision process in `docs/ai/Decision-Matrix.md`, not a runtime dispatcher. Any future automation of that process requires its own specification and ADR.
- **Not a message bus.** The Starline Weaver provides that. The runtime uses it where needed but does not replace or duplicate it.
- **Not a storage system.** Each component manages its own state; the runtime coordinates access, not ownership.
- **Not a security boundary.** CrystalBridge enforces security; the runtime assumes authorization decisions are already made.

### Relationship to CrystalCore OS

CrystalCore OS is the platform — the repository structure, governance model, documentation standards, and development discipline defined in `docs/adr/ADR-0001.md`.

The Crystal Runtime is a *component* within that platform. It is not another "CrystalCore-*" name; that naming is locked per `docs/adr/ADR-0004.md`. The runtime has one name, one responsibility set, and one interface contract.

### Relationship to Clementine

**Clementine** is an independent local-first AI companion that provides conversational AI, memory management, and voice interaction.

- **Remains independent:** Clementine's AI model, memory system, and terminal interface are unchanged.
- **Runtime interaction:** Clementine registers with the runtime's Registry. The runtime can route requests to Clementine through standard interfaces.
- **What the runtime does not do:** The runtime does not choose what Clementine says, modify its memory, or override its decisions.
- **Data exchanged:** Task requests (text, voice, context) and responses (text, structured data).
- **Failure isolation:** If Clementine is unavailable, the runtime marks it as offline in the Registry and fails requests appropriately without cascading.

### Relationship to Starline

**Starline** is a peer-to-peer consent-gated memory exchange protocol using real Noise Protocol handshakes.

- **Remains independent:** Starline's protocol, handshake, and memory model are unchanged.
- **Runtime interaction:** The runtime can initiate Starline exchanges for multi-instance coordination when needed.
- **What the runtime does not do:** The runtime does not decide which peers are trusted or override Starline's consent gates.
- **Data exchanged:** Peer discovery, handshake initiation, encrypted memory payloads.
- **Failure isolation:** Network failures or peer unavailability do not block other runtime operations.

### Relationship to Starline Weaver

**Starline Weaver** is a multi-AI message bus enforcing the Belt-Three law (science/story/vision labels) in code, with matrix mode for cross-compare and a red button for halting all agents.

- **Remains independent:** The Weaver's belt-three enforcement, matrix cross-compare logic, and agent halting mechanism are unchanged.
- **Runtime interaction:** The runtime can fan questions to the Weaver when human review requires consensus or multiple perspectives.
- **What the runtime does not do:** The runtime does not label messages; the Weaver enforces that. The runtime does not interpret matrix cross-compare results; it records and returns them.
- **Data exchanged:** Labeled task questions and agent responses.
- **Failure isolation:** If the Weaver is unavailable, the runtime fails requests that depend on it and succeeds those that don't.

### Relationship to CrystalBridge

**CrystalBridge** is the MCP consent gate, enforcing approval, permission, scope, and provenance checks for guest AIs with append-only audit logging. It is fail-closed by design.

- **Remains independent:** CrystalBridge's consent checks, audit trail, and fail-closed defaults are unchanged.
- **Runtime interaction:** The runtime assumes all inbound requests have already passed CrystalBridge consent gates. The runtime does not duplicate those checks.
- **What the runtime does not do:** The runtime does not decide whether to approve a guest AI or what scope it receives. CrystalBridge decides.
- **Data exchanged:** Provenance metadata, scope constraints, audit log references.
- **Failure isolation:** If CrystalBridge denies a request, it fails before reaching the runtime. If CrystalBridge is unavailable, the runtime remains online but no guest requests are accepted.

### Relationship to RDP

**RDP** is a tamper-evident chain that records and witnesses system activity. It never decides; it only records.

- **Remains independent:** RDP's chain logic, witness model, and append-only semantics are unchanged.
- **Runtime interaction:** The runtime logs significant events to RDP (component lifecycle, task completion, error conditions) via standard RDP adapters.
- **What the runtime does not do:** The runtime does not interpret RDP records or use them to make decisions. It delegates that to audit processes.
- **Data exchanged:** Event records, timestamps, component state transitions.
- **Failure isolation:** If RDP is unavailable, the runtime continues operating but audit records are lost until recovery.

**Explicit contract:** The Crystal Runtime coordinates these existing systems. It does not replace, subsume, or duplicate their responsibilities.

---

## 2. Architectural Principles

The runtime is designed to preserve the discipline and clarity established in earlier project phases.

### Single Responsibility per Module

Each runtime module has one job:
- Coordinator executes workflows.
- Registry knows what is available.
- Events defines how components communicate.
- Configuration manages settings.
- Plugins provides extension mechanisms.
- Logging captures observability.
- API exposes external entry points.

No module should blur these boundaries or take on responsibilities better delegated elsewhere.

### Loose Coupling

Components should not have hard dependencies on each other's implementation details. They should depend on published interfaces, not internal state.

Example: The Coordinator requests a capability from the Registry and receives an interface contract, not a direct reference to a component.

### Explicit Interfaces

All module contracts should be documented before implementation. If the interface is not documented, the module is not ready to build.

Interfaces include:
- Method signatures and parameter types.
- Expected inputs and outputs.
- Failure modes and error codes.
- Lifecycle methods (initialization, shutdown).

### Fail-Closed Defaults Where Appropriate

Following CrystalBridge's example, systems should default to denial, rejection, or offline state when uncertain. Graceful degradation is preferred over silent failure.

Example: If a component's status is unknown, mark it offline in the Registry rather than optimistically trying to use it.

### Human Governance Remains Outside Runtime Execution

Decisions about which AI should handle a task, what data is sensitive, or whether an action is permitted remain human decisions. The runtime coordinates execution, not governance.

The AI Orchestrator (`docs/ai/Decision-Matrix.md`) documents which humans should make which decisions. The runtime enforces their decisions; it does not replace them.

### Runtime Does Not Confer Authority

The runtime's decision to route a request to a component does not grant that component authority it does not already have. CrystalBridge's consent gates remain the source of truth for what a guest AI is permitted to do.

---

## 3. Runtime Topology

```
                 Crystal Runtime
                        │
        ┌───────────────┬───────────────┐
        │               │               │
    Coordinator      Registry          Events
        │               │               │
        ├──────────────┬┼┬──────────────┤
        │              │││              │
     Clementine      Starline Weaver   CrystalBridge
        │              │││              │
        └──────────────┴┼┴──────────────┘
                        │
                        RDP
                    (Logging)
```

**Conceptual flow:**

1. **Request arrives** at the runtime's API boundary (CrystalBridge consent gate already passed).
2. **Coordinator** receives the request and determines which components are needed.
3. **Registry** provides current availability and capabilities of each component.
4. **Events** carry task data to target components (Clementine, Weaver, Starline).
5. **Components execute** independently using their existing logic.
6. **Results return** through Events to the Coordinator.
7. **Logging** records the transaction to RDP and operational logs.
8. **Response** is returned to the caller.

No component directly manipulates another's internal state. All interaction is through published interfaces.

---

## 4. Runtime Modules

### 4.1 Coordinator

**Purpose**

Execute workflows by orchestrating the available components in the runtime.

**Responsibilities**

- Receive a task request.
- Query the Registry for available capabilities.
- Determine which components must participate.
- Sequence component calls.
- Aggregate results.
- Handle partial failures and timeouts.
- Return final output to the caller.

**Public Interface**

```
Coordinator.execute_workflow(
  task: Task,
  context: ExecutionContext
) -> WorkflowResult
```

`task` includes: description, required capabilities, human directives.  
`context` includes: request ID, caller identity, scope from CrystalBridge.

`WorkflowResult` includes: status, outputs, error details if failed, audit trail reference.

**Inputs**

- Task description (what needs to happen).
- Execution context (who is asking, with what authority).
- Available capabilities from the Registry.
- Status of registered components.

**Outputs**

- Structured result or error response.
- Event stream to Logging.
- Status update to Registry if a component changed state.

**Dependencies**

- Registry (to query capabilities).
- Events (to communicate with components).
- Logging (to record execution).

**Constraints**

- Does not make authorization decisions (CrystalBridge decided before the runtime saw the request).
- Does not retry indefinitely; has a configurable timeout per task.
- Does not modify component configuration.
- Does not substitute its judgment for explicit human directives in the task.

**Failure Behavior**

- If a required component is unavailable, fail the task immediately (fail-closed).
- If a component returns an error, propagate it and attempt rollback if applicable.
- If timeout occurs, halt the workflow and return partial results with error context.
- Log all failures to RDP and operational logs.

**Future Extension Points**

- Pluggable workflow engines (different orchestration strategies per task type).
- Distributed coordination if multi-instance Clementine is built.
- Advanced scheduling (priority queues, resource constraints).

---

### 4.2 Registry

**Purpose**

Maintain an authoritative list of available components, their capabilities, and their current state.

**Responsibilities**

- Track registered services and their capabilities.
- Report component availability (online/offline/degraded).
- Provide capability lookups (what can handle this task type?).
- Detect and handle component state changes.
- Persist or replay registry state on restart.

**Public Interface**

```
Registry.register(
  service_id: str,
  capabilities: Capability[],
  metadata: ServiceMetadata
) -> RegistrationToken

Registry.query_capability(
  capability_name: str
) -> ServiceReference[]

Registry.get_status(
  service_id: str
) -> ComponentStatus

Registry.unregister(
  service_id: str
) -> bool
```

**Inputs**

- Component registration (identity, capabilities, metadata).
- Heartbeat/liveness signals from components.
- Configuration changes that affect available capabilities.

**Outputs**

- Capability lookups for the Coordinator.
- Status updates to Logging.
- Events when component state changes.

**Dependencies**

- Configuration (for initial registry snapshot).
- Events (to notify of status changes).
- Logging (to record registrations/deregistrations).

**Constraints**

- Does not start or stop components; only tracks them.
- Does not interpret capabilities; services declare what they provide.
- Does not enforce ordering; if a service declares capability X, the Registry trusts it.

**Failure Behavior**

- If a component fails to heartbeat, mark it offline after a configurable grace period.
- If duplicate registrations occur, reject the second or use the most recent (policy TBD).
- If the Registry is queried for a nonexistent capability, return an empty list (not an error).

**Future Extension Points**

- Dynamic discovery (mDNS, gossip, or other peer discovery mechanisms).
- Capability versioning (service provides v1.0 and v2.0 of a capability).
- Performance metrics (registry tracks response times, error rates).

---

### 4.3 Events

**Purpose**

Define the async messaging model by which components communicate through the runtime.

**Responsibilities**

- Publish events from one component to another.
- Subscribe to event types.
- Guarantee event ordering and delivery semantics (at-least-once, exactly-once, best-effort).
- Route events to the correct subscribers.
- Provide observability into event flow.

**Public Interface**

```
EventBus.publish(
  event: Event,
  source: str
) -> EventID

EventBus.subscribe(
  event_type: str,
  handler: Callable
) -> SubscriptionHandle

EventBus.unsubscribe(
  subscription: SubscriptionHandle
) -> bool
```

**Inputs**

- Events from the Coordinator or from components.
- Subscriptions for event types.
- Configuration of routing and delivery guarantees.

**Outputs**

- Delivered events to subscribers.
- Audit trail of all events to Logging.
- Status updates if delivery fails.

**Dependencies**

- Configuration (routing rules, delivery semantics).
- Logging (record all event activity).

**Constraints**

- Does not interpret event content; events are opaque payloads.
- Does not guarantee ordering across unrelated event types.
- Does not buffer events indefinitely; has a configurable retention policy.
- Does not make decisions based on event content (that is the subscriber's job).

**Failure Behavior**

- If a subscriber fails to handle an event, the event remains in the queue and is retried (configurable).
- If the event bus is overwhelmed, new events are rejected with a backpressure error.
- If message delivery fails, log the failure and mark the event as undelivered.

**Future Extension Points**

- Multiple delivery semantics (at-least-once, exactly-once, best-effort per event type).
- Event filtering and transformation (middleware).
- Dead-letter queues for permanently failed events.

---

### 4.4 Configuration

**Purpose**

Load, validate, and provide runtime configuration to all modules.

**Responsibilities**

- Load configuration from sources (file, environment, runtime API).
- Validate configuration against a schema.
- Provide configuration to modules on demand.
- Detect configuration changes and notify affected modules.
- Handle secrets safely (never log, encrypt at rest).

**Public Interface**

```
Config.load(
  sources: ConfigSource[]
) -> Configuration

Config.validate(
  config: Configuration,
  schema: Schema
) -> ValidationResult

Config.get(
  key: str
) -> Any

Config.override(
  key: str,
  value: Any
) -> bool
```

**Inputs**

- Configuration files (YAML, TOML, JSON).
- Environment variables.
- Runtime overrides (for development/debugging).

**Outputs**

- Validated configuration to all modules.
- Events when configuration changes.
- Validation errors that block startup.

**Dependencies**

- Logging (record configuration load and validation).
- Events (notify of configuration changes).

**Constraints**

- Does not apply configuration; modules read it and apply changes.
- Does not restart components on configuration change (that decision is per-module).
- Does not store secrets in memory longer than necessary.
- Does not log sensitive values.

**Failure Behavior**

- If configuration is invalid, fail startup and report errors clearly.
- If a required configuration key is missing, fail startup (fail-closed).
- If a runtime override conflicts with a file-based setting, runtime override wins (intended for dev/debug).

**Future Extension Points**

- Hot reload (apply config changes without restart).
- Configuration versioning (rollback support).
- Multi-environment configurations (dev/staging/prod).

---

### 4.5 Plugins

**Purpose**

Provide a standard mechanism for extending runtime behavior without modifying core modules.

**Responsibilities**

- Define the plugin lifecycle (load, initialize, execute, shutdown).
- Enforce plugin isolation (plugins cannot call internal runtime functions).
- Validate plugin compatibility before loading.
- Provide plugin hooks (early in request, late in response, on error).
- Track plugin execution and failures.

**Public Interface**

```
PluginManager.load(
  plugin_path: str,
  metadata: PluginMetadata
) -> PluginHandle

PluginManager.unload(
  plugin_id: str
) -> bool

PluginManager.invoke_hook(
  hook_name: str,
  event: Event
) -> HookResult
```

**Inputs**

- Plugin source code or package.
- Plugin metadata (name, version, required hooks, dependencies).
- Hook invocation events.

**Outputs**

- Loaded plugin status.
- Hook execution results (modify event or pass through).
- Failure logs if a plugin crashes.

**Dependencies**

- Configuration (where to find plugins, which to load).
- Logging (record plugin lifecycle and failures).

**Constraints**

- Plugins cannot modify runtime core state directly.
- Plugins cannot access other plugins' private state.
- Plugins cannot override core decisions (e.g., cannot unilaterally approve a denied request).
- Plugins run in sandboxes if available (language-dependent).

**Failure Behavior**

- If a plugin fails to load (syntax error, missing dependency), log the error and skip it.
- If a plugin's hook raises an exception, catch it, log it, and continue (do not halt the workflow).
- If a plugin modifies an event in an invalid way, reject the modification and log a warning.

**Future Extension Points**

- Plugin versioning and compatibility checking.
- Plugin marketplaces (curated plugin repositories).
- Plugin resource limits (CPU, memory per plugin).

---

### 4.6 Logging

**Purpose**

Provide centralized telemetry, audit logging, and operational diagnostics.

**Responsibilities**

- Capture operational logs (what the runtime is doing).
- Capture diagnostic logs (details for troubleshooting).
- Capture audit records (who did what, for compliance).
- Route logs to appropriate sinks (files, RDP, external systems).
- Enforce retention policies.

**Public Interface**

```
Logger.operational(
  level: str,
  message: str,
  context: Dict
) -> None

Logger.diagnostic(
  level: str,
  message: str,
  context: Dict
) -> None

Logger.audit(
  event_type: str,
  actor: str,
  action: str,
  resource: str,
  result: str,
  context: Dict
) -> AuditRecord
```

**Inputs**

- Log messages from all runtime modules.
- Events from the event bus.
- Component status changes.
- Configuration changes.

**Outputs**

- Operational logs (stdout, log files).
- Diagnostic logs (detailed, usually disabled in production).
- Audit records (to RDP and audit store).
- Alerts if error rates exceed thresholds.

**Dependencies**

- Configuration (log levels, sinks, retention).
- RDP (append audit records).

**Constraints**

- Does not log secrets or sensitive data.
- Does not block the runtime if logging fails (log failures are not workflow failures).
- Diagnostic logs are verbose and should be disabled in production.
- Audit records are immutable once written.

**Failure Behavior**

- If RDP is unavailable, continue logging to local files.
- If a log sink is full, implement backpressure (drop oldest records or fail new ones, configurable).
- If a log file cannot be written, log the error (to stderr) and continue.

**Future Extension Points**

- Structured logging (JSON output for machine parsing).
- Metrics collection (latency, throughput, error rates).
- Integration with external logging services (Elasticsearch, Datadog, etc.).

---

### 4.7 API

**Purpose**

Expose the runtime to external callers (human interfaces, other systems).

**Responsibilities**

- Accept inbound requests.
- Assume CrystalBridge consent gates have already been passed.
- Route requests to the Coordinator.
- Format and return results.
- Handle authentication/identification of the caller (not authorization; CrystalBridge handles that).

**Public Interface**

```
API.handle_request(
  http_method: str,
  path: str,
  body: Any,
  caller_identity: str
) -> APIResponse

API.health_check() -> HealthStatus
```

**Inputs**

- HTTP requests from web clients or integrations.
- Caller identity (already authenticated by CrystalBridge or upstream).
- Task data in request body.

**Outputs**

- Structured API responses (JSON or other formats).
- Status codes (200, 400, 500, etc.).
- Workflow results or error details.

**Dependencies**

- Coordinator (to execute tasks).
- Logging (to record API calls).
- Configuration (API endpoints, rate limits).

**Constraints**

- Does not re-implement CrystalBridge consent checks (assumes they already passed).
- Does not interpret task data; passes it as-is to the Coordinator.
- Does not make authentication decisions (that is upstream).

**Failure Behavior**

- If Coordinator rejects a task (required capability unavailable), return 503 (Service Unavailable).
- If a task times out, return 408 (Request Timeout).
- If request body is malformed, return 400 (Bad Request).
- If an internal error occurs, return 500 (Internal Server Error) with minimal detail (full details to logs).

**Future Extension Points**

- Multiple API formats (REST, GraphQL, gRPC).
- API versioning (v1, v2, etc.).
- Rate limiting and throttling per caller.
- Webhook callbacks for long-running tasks.

---

## 5. Component Integration

### Clementine Integration

**Clementine remains an independent system.** The runtime does not control its AI model, memory, or terminal interface.

**Runtime interaction:**
- Clementine registers itself with the Registry under capability `"ai.clementine"`.
- When a task requires conversational AI, the Coordinator routes it to Clementine via Events.
- Clementine processes the request using its own logic and returns a response.
- The response flows back through Events to the Coordinator.

**What remains independent:**
- Clementine's choice of which model to use.
- Clementine's memory management and recall strategy.
- Clementine's voice interface and terminal UI.
- Clementine's internal error handling.

**Data exchanged:**
- Request: task description, context (user message, prior conversation).
- Response: AI-generated text or structured data.

**Failure isolation:**
- If Clementine crashes, the Registry marks it offline.
- In-flight requests to Clementine timeout and are failed back to the caller.
- The runtime continues operating; other workflows proceed.
- Clementine restarts independently (not controlled by the runtime).

### Starline Integration

**Starline remains an independent P2P protocol.** The runtime does not decide trust relationships or override consent gates.

**Runtime interaction:**
- Starline registers under capability `"mesh.p2p.starline"`.
- When a task requires multi-instance coordination, the Coordinator requests a Starline exchange via Events.
- Starline initiates peer discovery and Noise handshakes.
- Memory payloads are encrypted and exchanged.
- Results return to the Coordinator.

**What remains independent:**
- Peer discovery mechanism.
- Noise Protocol handshake and key derivation.
- Consent gate enforcement (Starline decides what it shares).
- Memory encryption and storage.

**Data exchanged:**
- Request: peer identifier, message/memory to exchange.
- Response: acknowledged receipt or consent denial.

**Failure isolation:**
- If a peer is unreachable, Starline returns a timeout error (not a runtime failure).
- If a peer denies consent, Starline returns a denial (not a runtime failure).
- If Starline itself crashes, mark it offline and fail tasks requiring it.

### Starline Weaver Integration

**Starline Weaver remains an independent message bus.** The runtime does not label messages or interpret cross-compare results; the Weaver enforces the belt-three law.

**Runtime interaction:**
- Weaver registers under capability `"ai.consensus.weaver"`.
- When a task requires multiple AI perspectives, the Coordinator fans the question to the Weaver via Events.
- Weaver enforces belt-three labels (science/story/vision) on each response.
- In matrix mode, Weaver cross-compares responses and returns agreement counts.
- Results flow back to the Coordinator.

**What remains independent:**
- Belt-three label enforcement (Weaver rejects unlabeled messages).
- Red button halting mechanism (Weaver implements it, runtime observes).
- Cross-compare logic (Weaver decides what "agreement" means).
- Agent participant list (Weaver decides who is invited).

**Data exchanged:**
- Request: question, task context, which agents to consult.
- Response: agent answers (each with belt-three label), cross-compare results if matrix mode.

**Failure isolation:**
- If Weaver is unavailable, fail tasks requiring consensus.
- If the red button is pressed, Weaver halts all agents; the runtime observes the halt state and stops sending new tasks.
- If an agent within the Weaver crashes, Weaver handles it; runtime sees it as a failed participant in the cross-compare.

### CrystalBridge Integration

**CrystalBridge is the consent gate upstream of the runtime.** The runtime assumes all inbound requests have already passed approval, permission, scope, and provenance checks.

**Runtime interaction:**
- CrystalBridge is upstream, not downstream. Requests reach the runtime only after CrystalBridge approves them.
- The runtime does not call CrystalBridge for permission checks; it trusts the CrystalBridge decision.
- The runtime logs request provenance (from CrystalBridge metadata) for audit purposes.
- If a task is out of scope (determined by CrystalBridge), the runtime respects that scope boundary.

**What remains independent:**
- Approval/denial decisions (CrystalBridge makes them).
- Permission scope enforcement (CrystalBridge decided how much authority this caller has).
- Provenance tracking (CrystalBridge is the source of truth).
- Audit trail append (CrystalBridge owns it, runtime contributes to it).

**Data exchanged:**
- CrystalBridge metadata: caller identity, approved capabilities, scope constraints.
- Runtime logs: task executed, results returned.

**Failure isolation:**
- If CrystalBridge is unavailable (no new requests can be approved), the runtime remains online but all inbound requests fail.
- If CrystalBridge rejects a request before it reaches the runtime, the runtime never sees it.
- CrystalBridge and runtime failures are independent; one going down does not cascade to the other.

### RDP Integration

**RDP is a tamper-evident chain that records, never decides.** The runtime logs significant events; RDP witnesses them.

**Runtime interaction:**
- Runtime publishes events to RDP: task execution start, task completion, error conditions, component state changes.
- RDP appends these events to the chain with timestamps and cryptographic witnesses.
- Runtime may query RDP for audit records but does not use them to make decisions.

**What remains independent:**
- Chain validation (RDP verifies the chain, runtime does not).
- Witness selection (RDP chooses witnesses, runtime does not).
- Immutability (RDP ensures append-only, runtime trusts it).

**Data exchanged:**
- Request: event record (timestamp, actor, action, result, context).
- Response: witnessed record with chain reference.

**Failure isolation:**
- If RDP is unavailable, audit records are queued locally and sent when RDP recovers.
- If RDP rejects a record (invalid format, etc.), log the rejection and retry with a corrected format.
- If RDP is permanently down, operational logs continue but audit chain is interrupted until recovery.

---

## 6. Event Model

Events are the primary mechanism by which components communicate through the runtime.

### Event Lifecycle

1. **Created:** A component (Coordinator, Registry, a task handler) creates an event.
2. **Labeled:** Event includes: type (string), source (component ID), timestamp, unique ID.
3. **Published:** Component calls `EventBus.publish(event)`.
4. **Routed:** EventBus finds all subscribers for that event type.
5. **Delivered:** Event is sent to each subscriber.
6. **Handled:** Subscriber processes the event (may create new events).
7. **Logged:** EventBus records the event delivery status to Logging.
8. **Retained:** Event remains in audit trail for configurable duration.

### Event Ownership

The component that creates an event owns it. Only the owner can modify or cancel it. Subscribers may create *new* events in response but do not modify the original.

### Event Propagation

Events propagate only to direct subscribers. There is no transitive fan-out (event A triggers event B triggers event C without explicit subscription to C).

Subscribers are registered by event type, not by component. Multiple components can subscribe to the same event type; they all receive it.

### Error Events

Errors are represented as events with type `"error.*"` (e.g., `"error.component_unavailable"`). These propagate to subscribers just like normal events.

A component that encounters an error creates an error event and publishes it. Other components can subscribe to error events and react.

### Cancellation

A task (or workflow) can issue a cancellation request. This is an event with type `"request.cancel"`. Components that are executing work for that task should stop and clean up.

Cancellation is a request, not a guarantee. Components that are in the middle of an operation may not be able to stop immediately.

### Observability

All events are recorded for observability. The Logging module captures:
- Event type and ID.
- Source and destination (which component published, which subscribed).
- Timestamp and latency (when published, when delivered).
- Result (success, failure, timeout).

This enables post-mortem analysis of event flow and latency bottlenecks.

---

## 7. Configuration Model

### Configuration Sources

The runtime loads configuration from multiple sources, in priority order:

1. **Runtime overrides** (highest priority — for development/debugging).
2. **Environment variables** (for containerized deployments).
3. **Configuration files** (YAML, TOML, JSON in a standard location).
4. **Defaults** (lowest priority — baked into code).

### Validation

Configuration is validated against a schema before being used. The schema specifies:
- Required vs. optional fields.
- Data types (string, integer, boolean, list, object).
- Allowable values (enums).
- Constraints (min/max values, string patterns).

If validation fails, startup fails with a clear error message listing what is invalid.

### Overrides

Runtime overrides are provided via CLI flags or environment variables and take precedence over file-based configuration. This is intended for:
- Development (testing different configs without changing files).
- Emergency patching (changing behavior without redeploying code).

Examples:
- `CRYSTAL_RUNTIME_LOG_LEVEL=debug` (override log level).
- `--coordinator-timeout 30` (override coordinator timeout).

### Secrets Handling

Secrets (API keys, passwords, encryption keys) are handled specially:
- Never logged in plaintext.
- Read from environment variables or secret management systems (e.g., HashiCorp Vault).
- Encrypted at rest if stored in files.
- Cleared from memory after use (when possible).

### Runtime Reload Policy

Configuration changes take effect according to a per-setting policy:
- **Immediate:** Log level, debug flags (no restart needed).
- **Next cycle:** Registry configuration, plugin list (restart runtime).
- **Manual restart:** Core module configuration (Coordinator, API) (requires full restart).

Configuration changes are logged to the audit trail. If a config change breaks the runtime, revert and restart.

---

## 8. Plugin Contract

Plugins extend the runtime by hooking into predefined points in the execution flow.

### Registration

A plugin is a package that provides:
- Plugin metadata (name, version, description, author).
- One or more hook implementations.
- An optional initialization function.

Plugins are loaded by the PluginManager at startup or at runtime.

### Discovery

Plugins are discovered from:
- A configured plugins directory.
- A plugins manifest file (list of plugins to load).
- Dynamic loading (a component requests a specific plugin).

### Version Compatibility

Each plugin declares:
- Minimum runtime version it requires.
- Maximum runtime version it is tested against.
- Required plugin dependencies (if any).

The PluginManager verifies compatibility before loading. Incompatible plugins are rejected.

### Lifecycle

1. **Load:** PluginManager loads the plugin code.
2. **Initialize:** PluginManager calls the plugin's `init()` function. Plugin sets up state, registers hooks.
3. **Execute:** Plugin's hooks are invoked at predefined points.
4. **Shutdown:** PluginManager calls the plugin's `shutdown()` function. Plugin cleans up resources.

### Isolation

Plugins cannot:
- Call internal runtime functions directly (only via published plugin API).
- Access other plugins' private state.
- Modify shared data structures without explicit synchronization.
- Spawn threads or processes without permission.

### Failure Handling

If a plugin's hook raises an exception:
1. Catch the exception.
2. Log the error.
3. Continue the workflow (the plugin's output is discarded).
4. If the same plugin fails multiple times in a row, disable it and log a warning.

A failing plugin does not halt the runtime.

---

## 9. Logging & Audit

### Operational Logging

Operational logs answer: "What is the runtime doing right now?"

Examples:
- `[INFO] Coordinator starting task ID 12345`.
- `[INFO] Component Clementine registered, available.`.
- `[WARN] Timeout waiting for Weaver response, failing task.`.

Retention: 30 days (configurable).  
Destination: Log files, stdout/stderr.

### Diagnostic Logging

Diagnostic logs answer: "Why is the runtime behaving this way?"

Examples:
- `[DEBUG] Registry query for 'ai.clementine' returned 1 match.`.
- `[DEBUG] Event published to 3 subscribers, delivered to 2, 1 timeout.`.
- `[TRACE] Coordinator.execute() entering state machine: AWAITING_REGISTRY.`.

Retention: 7 days (configurable).  
Destination: Separate log file (disabled in production by default).

### Audit Records

Audit records answer: "Who did what, and what was the outcome?"

Each audit record includes:
- Actor (which human or system made the request).
- Action (what was requested: execute_workflow, register_component, etc.).
- Resource (what was affected: task ID, component name, etc.).
- Result (success, failure, reason).
- Timestamp and context (request ID, caller IP, scope from CrystalBridge).

Retention: Permanent (audit records are never deleted, per regulatory requirements).  
Destination: RDP (tamper-evident chain).

Audit records are immutable once written. They can be queried but not modified.

---

## 10. Error Model

The runtime categorizes errors to guide appropriate handling.

### Recoverable Errors

The operation failed, but retrying may succeed.

Examples:
- A component was temporarily unavailable (just registered).
- Network timeout (brief network hiccup).
- A component returned an error that is not definitive.

**Runtime behavior:** Retry with exponential backoff. After N retries, fail the task.

### Retryable Errors

The operation failed in a way that suggests retrying is likely to succeed.

Examples:
- CrystalBridge is temporarily offline (will recover).
- Event queue is full (will drain).

**Runtime behavior:** Retry immediately or with minimal backoff. Fail the task if retries exhaust.

### Fatal Errors

The operation failed in a way that will not succeed on retry.

Examples:
- A required component was not found (not registered).
- Task exceeds allowed scope from CrystalBridge.
- A component rejected the task permanently (e.g., Clementine's refusal).

**Runtime behavior:** Fail the task immediately. Do not retry.

### Configuration Errors

Configuration is invalid or inconsistent.

Examples:
- Required configuration key is missing.
- Configuration value is outside allowed range.
- A referenced component does not exist.

**Runtime behavior:** Log the error clearly. Fail startup (fail-closed). Do not attempt to correct the error silently.

### External Dependency Errors

An external system that the runtime depends on failed.

Examples:
- CrystalBridge is down.
- RDP is unavailable.
- A registered component is unavailable.

**Runtime behavior:** Degraded mode. Operations that depend on the failed system are failed; operations that do not are allowed to proceed.

### Security Errors

A request or action violated security policy.

Examples:
- A task attempts to exceed the caller's scope.
- A plugin attempts to access unauthorized data.
- A caller is not authenticated.

**Runtime behavior:** Deny the operation. Log the security event to audit trail. Do not retry.

---

## 11. Testing Strategy

Testing verifies that the runtime correctly orchestrates components and handles failure cases.

### Unit Testing

**Scope:** Individual modules (Coordinator, Registry, Events, etc.) in isolation.

**Emphasis:**
- Module interface contracts (method signatures, inputs, outputs).
- Happy path (normal operation).
- Error cases (invalid inputs, failure conditions).
- State transitions (initialization, shutdown, state changes).

**Example:**
- Test that `Registry.register()` adds a new service and makes it queryable.
- Test that `Registry.query_capability()` returns services in the correct order.
- Test that `Registry.get_status()` reflects the last heartbeat.

### Integration Testing

**Scope:** Multiple modules working together (Coordinator with Registry, Events with Logging, etc.).

**Emphasis:**
- Cross-module communication (data flows correctly between modules).
- Failure propagation (if one module fails, others respond appropriately).
- State consistency (all modules see consistent state after an operation).

**Example:**
- Test that when Coordinator calls Registry, it gets current capability status.
- Test that when a component fails to heartbeat, Registry marks it offline and Coordinator fails new tasks for it.

### Contract Testing

**Scope:** Runtime interfaces with external components (Clementine, Starline, Weaver, CrystalBridge, RDP).

**Emphasis:**
- Request/response format (do we send valid requests, do we parse responses correctly?).
- Error handling (do we handle component errors gracefully?).
- Timeout behavior (do we wait appropriately and timeout correctly?).

**Example:**
- Mock Clementine returning a response, verify the Coordinator correctly parses it.
- Mock Clementine timing out, verify the Coordinator fails the task appropriately.
- Mock CrystalBridge rejecting a request, verify the Coordinator fails the task.

### Replay Testing

**Scope:** Testing against recorded event sequences.

**Emphasis:**
- Deterministic behavior (given the same sequence of events, the runtime produces the same results).
- Failure scenario coverage (recorded sequences of edge cases and failures).

**Example:**
- Record a sequence of events: Coordinator receives task, Registry returns capabilities, Coordinator routes to Clementine, Clementine times out, Coordinator fails the task.
- Replay that sequence and verify the same outcome.

### End-to-End Testing

**Scope:** Full workflow from request to response.

**Emphasis:**
- Real component interaction (use real or well-simulated components).
- Latency and timing (workflows complete in reasonable time).
- Audit trail correctness (all events are logged correctly).

**Example:**
- Send a real task to the runtime, get back a result, verify that RDP contains the audit trail.
- Simulate a component failure mid-workflow, verify that the workflow fails gracefully and audit trail reflects it.

---

## 12. Security Considerations

### Trust Boundaries

**Boundary 1:** Between CrystalBridge and the runtime.
- Everything upstream of CrystalBridge is untrusted (users, external systems).
- CrystalBridge vets requests and only allows approved ones to reach the runtime.
- The runtime trusts CrystalBridge's decisions and does not re-check approval.

**Boundary 2:** Between the runtime and components.
- The runtime does not trust component implementations.
- The runtime assumes components may fail, behave incorrectly, or be compromised.
- The runtime monitors component behavior and can isolate a misbehaving component.

**Boundary 3:** Between plugins and the runtime.
- Plugins are loaded from potentially untrusted sources.
- Plugins run in a sandbox if available and have limited access to runtime state.
- A malicious plugin can be disabled or removed.

### Authentication

The runtime does not authenticate users; CrystalBridge does. The runtime assumes incoming requests are already authenticated and identified.

### Authorization

Authorization decisions (what is the caller permitted to do) are made by CrystalBridge before the request reaches the runtime. The runtime enforces scope boundaries but does not make new authorization decisions.

### Secret Handling

Secrets (API keys, encryption keys, passwords) are:
- Never logged or displayed in error messages.
- Stored encrypted if persisted to disk.
- Read from secure sources (environment variables, secret management systems).
- Cleared from memory after use (when possible).

### Failure Defaults

When uncertain, the runtime defaults to denial (fail-closed).

Examples:
- If a component's authorization is unclear, mark it as unauthorized.
- If a configuration value is missing, fail startup rather than guess.
- If a request seems suspicious, log it and deny it.

---

## 13. Extension Points

The runtime is designed to be extended without modifying core modules. Extension points are:

### New AI Providers

**Extension point:** New component type can implement the `"ai.*"` capability.

Example: A new AI system registers under `"ai.custom_provider"` and the Coordinator can route tasks to it.

No runtime code change needed.

### Additional Transports

**Extension point:** Registry and Events can work with different underlying transports (local, network-based, message queues).

Example: Use RabbitMQ for events instead of the built-in in-process bus.

No runtime code change needed (if the interfaces are preserved).

### Alternative Storage Backends

**Extension point:** Registry can persist state to different backends (file, database, distributed cache).

Example: Store Registry state in Redis for multi-instance runtimes.

No runtime code change needed (if the interface is preserved).

### New Runtime Services

**Extension point:** New modules can be added to the runtime (e.g., a caching layer, rate limiter, load balancer).

Example: Add a Caching module that sits between Coordinator and components.

Requires coordination via Configuration and Events; no runtime core change needed.

### Plugin System

**Extension point:** Plugins hook into the runtime at predefined points.

Examples:
- A plugin that enforces rate limiting.
- A plugin that adds tracing/observability.
- A plugin that implements a new scheduling strategy.

No runtime code change needed.

---

## 14. Out of Scope

Explicitly stating what the specification does not define prevents scope creep and clarifies boundaries.

### AI Autonomy

This specification does not define how to make AI autonomous or how to reduce human oversight. The AI Orchestrator remains a documented decision process (humans make the calls), not a runtime dispatcher.

If future work automates parts of the AI Orchestrator, that requires its own specification and ADR.

### Automatic Task Delegation

The runtime does not automatically choose which AI should handle a task based on learned preferences or heuristics. That choice is human-guided (via Decision-Matrix.md) and explicit.

### New Governance Rules

This specification does not create new governance rules or decision-making processes. Governance is defined in `docs/governance/` and `docs/ai/`; the runtime implements those decisions, not the reverse.

### New Protocol Behavior

This specification does not modify Starline, Starline Weaver, CrystalBridge, or RDP. Those components retain their behavior and responsibilities. The runtime coordinates them but does not change how they work.

### Replacement of Existing Systems

The runtime does not replace Clementine, Starline, CrystalBridge, or RDP. It coordinates them. If future versions of those systems are needed, they are built independently; the runtime adapts by updating how it invokes them.

### Repository Organization

This specification does not redefine repository structure. That was addressed in v1.0 via ADR-0001. The runtime is code organized within the existing structure, not a reason to reorganize again.

---

## 15. Implementation Readiness Checklist

No code should be written until the checklist is complete for a module. This ensures interfaces are defined before implementation begins.

| Module | Interface Defined | Dependencies Identified | Testing Plan Complete | Ready for Implementation | Status |
|--------|---|---|---|---|---|
| Coordinator | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |
| Registry | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |
| Events | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |
| Configuration | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |
| Plugins | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |
| Logging | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |
| API | [ ] | [ ] | [ ] | [ ] | Deferred until specification review |

**Process:**
1. Review this specification with project stakeholders.
2. Resolve open questions and clarifications.
3. For each module, confirm:
   - Interface is documented and unambiguous.
   - Dependencies (what it needs from other modules) are identified.
   - Testing strategy covers happy path, error cases, and edge cases.
4. Mark the module "Ready for Implementation" once all three are confirmed.
5. Implementation proceeds module by module.

---

## Next Steps

This specification is a draft. The path forward:

1. **Stakeholder review.** Gather feedback from anyone who will implement or maintain the runtime.
2. **Refinement.** Address ambiguities and resolve open questions.
3. **Detailed interface definitions.** For each module, produce formal interface specifications (method signatures, data types, error codes).
4. **Implementation readiness.** Complete the checklist above for all modules.
5. **Implementation.** Build the runtime according to the specification.

Until the specification is accepted and the readiness checklist is complete, no runtime code is written.

---

## References

- [ADR-0001: Adopt the CrystalCore OS v1.0 repository architecture](../../adr/ADR-0001.md)
- [ADR-0004: Lock the CrysCore naming taxonomy](../../adr/ADR-0004.md)
- [ADR-0005: AI Orchestrator — consolidate the naming](../../adr/ADR-0005.md)
- [Decision-Matrix.md](../../ai/Decision-Matrix.md)
- [The-Incognita-Rule.md](../../governance/The-Incognita-Rule.md)
- [Roadmap.md](../../governance/Roadmap.md)

## Architectural Inspiration

This specification draws on proven patterns from production systems:

- **MemClaw** (Apache 2.0, eToro) — Multi-agent governed memory systems, visibility scopes, trust tiers, outcome-based reinforcement, and hybrid search patterns informed the Registry and Events model. See [ATTRIBUTIONS.md](../../ATTRIBUTIONS.md).

---

**License:** This specification is part of CrystalCore OS and is licensed under CC BY-NC-ND 4.0 (see `LICENSE`). Non-commercial use only; no derivative redistribution; attribution to the original authors and third-party sources listed above required.

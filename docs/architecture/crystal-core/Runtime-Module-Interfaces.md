# Crystal Runtime v0.3: Module Interface Specifications

**Status:** Draft - Implementation Contract  
**Purpose:** Formal interface definitions for each runtime module before implementation  
**Date:** 2026-07-23

This document defines the public interfaces, contracts, and behavior specifications for all seven Crystal Runtime modules. These are implementation-binding contracts — code must conform to these signatures and behaviors.

---

## 1. Coordinator Module

**File:** `src/runtime/coordinator/coordinator.py`  
**Responsibility:** Execute workflows by orchestrating available components in the runtime.

### Core Class: `Coordinator`

```python
class Coordinator:
    """Orchestrates workflow execution across runtime components."""
    
    def __init__(self, registry: Registry, events: EventBus, logging: Logger, config: Config) -> None:
        """
        Initialize the Coordinator.
        
        Args:
            registry: Registry instance for capability queries
            events: EventBus instance for component communication
            logging: Logger instance for audit/operational logging
            config: Config instance with coordinator settings
            
        Raises:
            ValueError: If required configuration is missing
        """
        
    def execute_workflow(
        self,
        task: Task,
        context: ExecutionContext
    ) -> WorkflowResult:
        """
        Execute a workflow for the given task.
        
        Args:
            task: Task object with description, required capabilities, directives
            context: ExecutionContext with request ID, caller identity, scope
            
        Returns:
            WorkflowResult: status, outputs, error details, audit trail reference
            
        Raises:
            TaskExecutionError: If workflow fails (see error categories below)
            TimeoutError: If workflow exceeds configured timeout
            
        Behavior:
            1. Validate task against execution context scope
            2. Query Registry for required capabilities
            3. Determine component sequence
            4. Execute components via EventBus
            5. Handle partial failures and timeouts
            6. Return aggregated result
            7. Log to RDP via Logging
        """
```

### Data Structures

```python
class Task:
    """A unit of work to be executed by the Coordinator."""
    task_id: str              # Unique task identifier
    description: str          # Human-readable task description
    capabilities_required: list[str]  # ["capability.name", ...]
    directives: dict[str, Any]        # Human guidance (e.g., {"retry": False})
    metadata: dict[str, Any]          # Additional context (e.g., priority)

class ExecutionContext:
    """Context for task execution (from CrystalBridge)."""
    request_id: str           # Unique request identifier
    caller_identity: str      # Who made the request
    approved_scope: list[str] # Capabilities caller is authorized for
    approval_level: str       # "read" | "write" | "admin"
    provenance: str           # How/why this request was approved

class WorkflowResult:
    """Result of workflow execution."""
    task_id: str              # Echo of input task_id
    status: str               # "success" | "partial_failure" | "fatal_error" | "timeout"
    outputs: dict[str, Any]   # Structured outputs from components
    error_details: Optional[ErrorDetails]  # If status != success
    components_executed: list[str]         # Which components ran
    components_failed: list[str]           # Which components failed
    start_time: float         # Unix timestamp
    end_time: float           # Unix timestamp
    duration_ms: float        # Execution time in milliseconds
    audit_trail_ref: str      # Reference to RDP audit record
```

### Error Handling

```python
class TaskExecutionError(Exception):
    """Base class for task execution errors."""
    error_code: str           # Specific error category
    message: str              # Human-readable description
    retryable: bool           # Whether retry might succeed
    component: Optional[str]   # Which component failed

class ScopeViolationError(TaskExecutionError):
    """Task exceeds caller's authorized scope."""
    error_code = "scope_violation"

class CapabilityNotFoundError(TaskExecutionError):
    """Required capability is not registered."""
    error_code = "capability_not_found"
    retryable = True          # Might register soon

class ComponentTimeoutError(TaskExecutionError):
    """Component exceeded timeout."""
    error_code = "component_timeout"

class ComponentFailureError(TaskExecutionError):
    """Component returned non-retriable error."""
    error_code = "component_failure"
```

### Configuration

```python
# In config.py or config.yaml:
coordinator:
  default_timeout_seconds: 30    # Per-task timeout
  retry_count: 3                 # Max retries for retriable errors
  retry_backoff_ms: [100, 500, 2000]  # Exponential backoff per retry
  max_concurrent_tasks: 100      # Concurrency limit
  log_level: "info"              # "debug" | "info" | "warn" | "error"
```

---

## 2. Registry Module

**File:** `src/runtime/registry/registry.py`  
**Responsibility:** Maintain authoritative list of available components and their capabilities.

### Core Class: `Registry`

```python
class Registry:
    """Manages component registration, discovery, and status tracking."""
    
    def __init__(self, config: Config, events: EventBus, logging: Logger) -> None:
        """
        Initialize the Registry.
        
        Args:
            config: Config instance with registry settings
            events: EventBus for broadcasting status changes
            logging: Logger for audit logging
        """
    
    def register(
        self,
        service_id: str,
        capabilities: list[Capability],
        metadata: ServiceMetadata
    ) -> RegistrationToken:
        """
        Register a new service and its capabilities.
        
        Args:
            service_id: Unique identifier for the service (e.g., "clementine", "starline.weaver")
            capabilities: List of Capability objects this service provides
            metadata: ServiceMetadata with version, health_check_url, etc.
            
        Returns:
            RegistrationToken: Token for later unregistration
            
        Raises:
            ValueError: If service_id is invalid or already registered
            
        Behavior:
            1. Validate service_id and capabilities
            2. Store registration with timestamp
            3. Publish "registry.service_registered" event
            4. Log to audit trail
        """
    
    def unregister(self, service_id: str) -> bool:
        """
        Unregister a service.
        
        Args:
            service_id: Service to remove
            
        Returns:
            True if service was registered and removed, False if not found
            
        Behavior:
            1. Remove service from registry
            2. Mark all capabilities as unavailable
            3. Publish "registry.service_unregistered" event
            4. Log to audit trail
        """
    
    def query_capability(self, capability_name: str) -> list[ServiceReference]:
        """
        Find all services providing a capability.
        
        Args:
            capability_name: Capability to search for (e.g., "ai.clementine")
            
        Returns:
            List of ServiceReference objects (sorted by status, then registration time)
            
        Raises:
            None (returns empty list if no matches)
            
        Behavior:
            1. Search registry for capability match
            2. Filter out offline services
            3. Return online services first, then degraded
        """
    
    def get_status(self, service_id: str) -> ComponentStatus:
        """
        Get current status of a service.
        
        Args:
            service_id: Service to check
            
        Returns:
            ComponentStatus: "online" | "degraded" | "offline"
            
        Raises:
            KeyError: If service is not registered
        """
    
    def heartbeat(self, service_id: str) -> bool:
        """
        Record a heartbeat from a service (liveness signal).
        
        Args:
            service_id: Service sending heartbeat
            
        Returns:
            True if heartbeat was recorded, False if service not found
            
        Behavior:
            1. Update last_heartbeat timestamp
            2. If service was offline, mark as online and publish event
            3. Log to audit trail if status changed
        """
    
    def mark_degraded(self, service_id: str, reason: str) -> bool:
        """
        Mark a service as degraded (partial failure).
        
        Args:
            service_id: Service to mark
            reason: Human-readable reason (e.g., "high latency")
            
        Returns:
            True if marked, False if service not found
        """
```

### Data Structures

```python
class Capability:
    """A capability provided by a service."""
    name: str                 # e.g., "ai.clementine", "mesh.p2p.starline"
    version: str              # Semantic version (e.g., "1.0.0")
    description: str          # Human-readable description
    input_schema: dict        # JSON Schema for inputs
    output_schema: dict       # JSON Schema for outputs

class ServiceMetadata:
    """Metadata about a registered service."""
    service_id: str
    version: str              # Service version
    health_check_url: Optional[str]  # URL to check liveness
    health_check_interval_seconds: int
    tags: list[str]           # Arbitrary tags for filtering

class ServiceReference:
    """Reference to a registered service."""
    service_id: str
    capabilities: list[str]
    status: str               # "online" | "degraded" | "offline"
    last_heartbeat: float     # Unix timestamp
    registered_at: float      # Unix timestamp

class ComponentStatus:
    """Detailed status of a component."""
    service_id: str
    status: str               # "online" | "degraded" | "offline"
    reason: Optional[str]     # Why degraded/offline, if applicable
    last_heartbeat: float
    capabilities_online: list[str]
    capabilities_degraded: list[str]
```

### Configuration

```python
registry:
  heartbeat_timeout_seconds: 30   # Mark offline if no heartbeat in this time
  status_check_interval_seconds: 5  # How often to check timeouts
  max_services: 1000              # Hard limit on registered services
  log_level: "info"
```

---

## 3. Events Module (EventBus)

**File:** `src/runtime/events/eventbus.py`  
**Responsibility:** Publish events and route to subscribers; handle delivery guarantees.

### Core Class: `EventBus`

```python
class EventBus:
    """Asynchronous message bus for component communication."""
    
    def __init__(self, config: Config, logging: Logger) -> None:
        """
        Initialize the EventBus.
        
        Args:
            config: Config instance with event bus settings
            logging: Logger for event audit
        """
    
    def publish(
        self,
        event_type: str,
        event_data: dict,
        source: str,
        metadata: Optional[dict] = None
    ) -> str:
        """
        Publish an event.
        
        Args:
            event_type: Event type (e.g., "task.started", "component.failed")
            event_data: Opaque event payload (dict)
            source: Component publishing the event
            metadata: Optional metadata (timestamp overrides, priority, etc.)
            
        Returns:
            event_id: Unique event identifier
            
        Raises:
            EventPublishError: If event queue is full or event is invalid
            
        Behavior:
            1. Validate event_type and event_data
            2. Assign unique event_id
            3. Record publish timestamp
            4. Add to event queue
            5. Notify all subscribers for event_type
            6. Log to audit trail
        """
    
    def subscribe(
        self,
        event_type: str,
        handler: Callable[[Event], None],
        options: Optional[SubscriptionOptions] = None
    ) -> str:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type: Event type to subscribe to (wildcard "task.*" allowed)
            handler: Callable to invoke when event is published
            options: SubscriptionOptions (delivery guarantee, timeout, etc.)
            
        Returns:
            subscription_id: Token for later unsubscribe
            
        Raises:
            ValueError: If event_type is invalid
            
        Behavior:
            1. Register subscriber for event_type
            2. Deliver any buffered events matching subscription
            3. Return subscription_id
        """
    
    def unsubscribe(self, subscription_id: str) -> bool:
        """
        Unsubscribe from events.
        
        Args:
            subscription_id: Token from subscribe()
            
        Returns:
            True if subscription existed, False otherwise
        """
    
    def get_pending_events(self, event_type: str) -> list[Event]:
        """
        Get events matching a type that have been published but not yet delivered.
        (For recovery/replay scenarios)
        
        Args:
            event_type: Event type filter
            
        Returns:
            List of Event objects
        """
```

### Data Structures

```python
class Event:
    """An event in the runtime."""
    event_id: str             # Unique identifier
    event_type: str           # Type of event
    source: str               # Component that published
    event_data: dict          # Opaque payload
    timestamp: float          # Unix timestamp (when published)
    delivery_status: str      # "pending" | "delivered" | "failed" | "undelivered"
    metadata: dict            # Additional context

class SubscriptionOptions:
    """Options for event subscription."""
    delivery_guarantee: str   # "at-least-once" | "exactly-once" | "best-effort"
    timeout_seconds: int      # How long handler can run
    buffer_size: int          # How many events to buffer if handler is slow
    filter_predicate: Optional[Callable[[Event], bool]]  # Optional filter
```

### Configuration

```python
events:
  delivery_guarantee: "at-least-once"  # Default for new subscriptions
  max_queue_size: 10000              # Drop events if queue full
  event_retention_seconds: 3600      # Keep events for replay
  subscription_timeout_seconds: 30   # Max time per handler call
  log_level: "info"
```

---

## 4. Configuration Module

**File:** `src/runtime/config/config.py`  
**Responsibility:** Load, validate, and provide configuration to all modules.

### Core Class: `Config`

```python
class Config:
    """Centralized configuration manager."""
    
    @staticmethod
    def load(sources: list[ConfigSource]) -> 'Config':
        """
        Load configuration from multiple sources.
        
        Args:
            sources: List of ConfigSource objects (file, env, runtime overrides)
            
        Returns:
            Config instance
            
        Raises:
            ConfigValidationError: If configuration is invalid
            
        Behavior:
            1. Load each source in priority order (later sources override earlier)
            2. Validate against schema
            3. Substitute environment variables
            4. Return validated Config
        """
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Dot-separated key (e.g., "coordinator.timeout_seconds")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
            
        Raises:
            KeyError: If key not found and no default provided
        """
    
    def get_section(self, section: str) -> dict:
        """
        Get an entire configuration section.
        
        Args:
            section: Section name (e.g., "coordinator", "registry")
            
        Returns:
            Dictionary of all config in that section
        """
    
    def validate(self, schema: dict) -> ValidationResult:
        """
        Validate current configuration against a schema.
        
        Args:
            schema: JSON Schema
            
        Returns:
            ValidationResult with any errors/warnings
        """
    
    def override(self, key: str, value: Any) -> None:
        """
        Runtime override of a configuration value.
        (For development/debugging)
        
        Args:
            key: Dot-separated key
            value: New value
            
        Raises:
            ValueError: If override violates constraints
        """
```

### Data Structures

```python
class ConfigSource:
    """A source of configuration data."""
    source_type: str  # "file" | "environment" | "runtime"
    location: str     # File path, env var name, or description
    priority: int     # Lower number = higher priority

class ValidationResult:
    """Result of configuration validation."""
    is_valid: bool
    errors: list[str]
    warnings: list[str]
```

### Configuration Schema

```yaml
# Crystal Runtime configuration structure
coordinator:
  default_timeout_seconds: 30
  retry_count: 3
  log_level: debug|info|warn|error

registry:
  heartbeat_timeout_seconds: 30
  status_check_interval_seconds: 5
  log_level: debug|info|warn|error

events:
  delivery_guarantee: at-least-once|exactly-once|best-effort
  max_queue_size: 10000
  event_retention_seconds: 3600
  log_level: debug|info|warn|error

plugins:
  enabled: true
  directory: ./plugins
  auto_load: true
  log_level: debug|info|warn|error

logging:
  operational_level: info|debug|warn|error
  diagnostic_level: debug|trace
  audit_enabled: true
  retention_days: 30
  sinks:
    - type: file
      path: ./logs/runtime.log
    - type: stdout
      level: warn

api:
  host: 0.0.0.0
  port: 8000
  rate_limit_per_minute: 1000
  log_level: info|debug
```

---

## 5. Plugins Module (PluginManager)

**File:** `src/runtime/plugins/plugin_manager.py`  
**Responsibility:** Load, validate, and manage plugin lifecycle.

### Core Class: `PluginManager`

```python
class PluginManager:
    """Manages plugin loading, initialization, and execution."""
    
    def __init__(self, config: Config, logging: Logger) -> None:
        """
        Initialize the PluginManager.
        
        Args:
            config: Config instance
            logging: Logger instance
        """
    
    def load(
        self,
        plugin_path: str,
        metadata: PluginMetadata
    ) -> str:
        """
        Load a plugin from disk or package.
        
        Args:
            plugin_path: File path or module name
            metadata: PluginMetadata with version, hooks, etc.
            
        Returns:
            plugin_id: Unique identifier for loaded plugin
            
        Raises:
            PluginLoadError: If plugin cannot be loaded or is incompatible
            
        Behavior:
            1. Validate plugin_path exists
            2. Check runtime version compatibility
            3. Verify plugin dependencies are available
            4. Load plugin code
            5. Call plugin's init() function
            6. Register hooks
            7. Log plugin load
        """
    
    def unload(self, plugin_id: str) -> bool:
        """
        Unload a plugin.
        
        Args:
            plugin_id: Plugin to unload
            
        Returns:
            True if unloaded, False if not found
            
        Behavior:
            1. Call plugin's shutdown() function
            2. Unregister hooks
            3. Unload plugin code from memory
            4. Log plugin unload
        """
    
    def invoke_hook(
        self,
        hook_name: str,
        event: Event
    ) -> HookResult:
        """
        Invoke all plugins' implementations of a hook.
        
        Args:
            hook_name: Hook name (e.g., "before_task_execution")
            event: Event to pass to hook handlers
            
        Returns:
            HookResult aggregating results from all plugins
            
        Behavior:
            1. Find all plugins with this hook
            2. Call each plugin's hook function in order
            3. Catch exceptions from individual plugins
            4. Log failures but continue
            5. Aggregate results
            6. Return combined result
        """
    
    def list_plugins(self) -> list[PluginInfo]:
        """
        Get information about all loaded plugins.
        
        Returns:
            List of PluginInfo objects
        """
```

### Data Structures

```python
class PluginMetadata:
    """Metadata about a plugin."""
    name: str
    version: str              # Semantic version
    description: str
    author: str
    required_hooks: list[str] # Hooks this plugin implements
    dependencies: list[str]   # Other plugins this depends on
    min_runtime_version: str  # Minimum supported runtime version
    max_runtime_version: Optional[str]  # Maximum supported (None = any)

class HookResult:
    """Result of hook invocation."""
    hook_name: str
    succeeded: int            # Number of plugins that succeeded
    failed: int               # Number of plugins that failed
    results: list[dict]       # Individual results from each plugin
    errors: dict[str, str]    # Errors keyed by plugin_id

class PluginInfo:
    """Information about a loaded plugin."""
    plugin_id: str
    name: str
    version: str
    status: str               # "loaded" | "failed" | "disabled"
    hooks_registered: list[str]
    load_time: float          # Unix timestamp
```

### Error Handling

```python
class PluginLoadError(Exception):
    """Plugin cannot be loaded."""
    error_code: str           # "not_found" | "incompatible" | "syntax_error" | "init_failed"
    plugin_name: str
    reason: str
```

---

## 6. Logging Module

**File:** `src/runtime/logging/logger.py`  
**Responsibility:** Capture and route operational, diagnostic, and audit logs.

### Core Class: `Logger`

```python
class Logger:
    """Centralized logging system."""
    
    def __init__(self, config: Config) -> None:
        """
        Initialize the Logger.
        
        Args:
            config: Config instance with logging settings
        """
    
    def operational(
        self,
        level: str,
        message: str,
        context: dict
    ) -> None:
        """
        Log an operational message (what the runtime is doing).
        
        Args:
            level: "debug" | "info" | "warn" | "error"
            message: Log message
            context: Contextual data (request_id, component, etc.)
            
        Behavior:
            1. Format message with context
            2. Write to operational log sink(s)
            3. If level >= configured, also write to stdout
        """
    
    def diagnostic(
        self,
        level: str,
        message: str,
        context: dict
    ) -> None:
        """
        Log a diagnostic message (for troubleshooting).
        
        Args:
            level: "debug" | "trace"
            message: Diagnostic message
            context: Contextual data
            
        Behavior:
            1. Check if diagnostic logging is enabled
            2. Format and write to diagnostic log (if enabled)
            3. Never write to stdout (debug data only)
        """
    
    def audit(
        self,
        event_type: str,
        actor: str,
        action: str,
        resource: str,
        result: str,
        context: dict
    ) -> AuditRecord:
        """
        Log an audit record (compliance/security).
        
        Args:
            event_type: Type of event (e.g., "task_executed", "plugin_loaded")
            actor: Who performed the action (caller identity)
            action: What action was taken
            resource: What resource was affected
            result: Outcome ("success", "failure", error code, etc.)
            context: Additional context (request_id, timestamps, etc.)
            
        Returns:
            AuditRecord: Immutable record that was logged
            
        Behavior:
            1. Create AuditRecord with timestamp
            2. Write to RDP (tamper-evident chain)
            3. Also write to audit log file
            4. Log failures but never fail the operation
        """
```

### Data Structures

```python
class AuditRecord:
    """An immutable audit log entry."""
    audit_id: str             # Unique identifier
    timestamp: float          # Unix timestamp
    event_type: str
    actor: str
    action: str
    resource: str
    result: str               # "success" | "failure" | error_code
    context: dict
    rdp_reference: str        # Reference to RDP chain entry
```

### Configuration

```yaml
logging:
  operational:
    level: info               # Min level to log
    destinations:
      - type: file
        path: ./logs/runtime.log
        rotation: daily       # Size-based or time-based rotation
      - type: stdout
        level: warn           # Only log warn/error to console
  
  diagnostic:
    level: debug              # Min level (only if enabled)
    enabled: false            # Usually off in production
    destinations:
      - type: file
        path: ./logs/debug.log
  
  audit:
    enabled: true
    retention_days: 365
    destinations:
      - type: rdp             # Tamper-evident chain (primary)
      - type: file
        path: ./logs/audit.log  # Backup file copy
```

---

## 7. API Module

**File:** `src/runtime/api/api.py`  
**Responsibility:** Accept inbound requests and route to Coordinator.

### Core Class: `RuntimeAPI`

```python
class RuntimeAPI:
    """HTTP/REST interface to the runtime."""
    
    def __init__(
        self,
        coordinator: Coordinator,
        logging: Logger,
        config: Config
    ) -> None:
        """
        Initialize the API.
        
        Args:
            coordinator: Coordinator instance
            logging: Logger instance
            config: Config instance
        """
    
    def handle_request(
        self,
        http_method: str,
        path: str,
        body: Optional[dict],
        caller_identity: str,
        headers: dict
    ) -> APIResponse:
        """
        Handle an inbound HTTP request.
        
        Args:
            http_method: "GET" | "POST" | "PUT" | "DELETE"
            path: Request path (e.g., "/task/execute")
            body: Request body (parsed JSON)
            caller_identity: Caller identity (from auth, CrystalBridge)
            headers: HTTP headers
            
        Returns:
            APIResponse with status, headers, body
            
        Raises:
            None (all errors are caught and returned as APIResponse)
            
        Behavior:
            1. Validate request format
            2. Log request (operational)
            3. Determine request type (task execution, health, etc.)
            4. Route to appropriate handler
            5. Return APIResponse
        """
    
    def health_check(self) -> HealthStatus:
        """
        Get runtime health status.
        
        Returns:
            HealthStatus: Overall status and component statuses
            
        Behavior:
            1. Query Registry for component statuses
            2. Check event queue depth
            3. Check recent error rates
            4. Determine overall health (online | degraded | offline)
        """
```

### Data Structures

```python
class APIResponse:
    """Response to an API request."""
    status_code: int          # HTTP status
    headers: dict             # Response headers
    body: dict                # JSON response body
    
    # Common status codes:
    # 200: Success
    # 400: Bad request (malformed body, missing fields)
    # 403: Forbidden (scope violation)
    # 408: Request timeout
    # 503: Service unavailable (required component offline)
    # 500: Internal error

class HealthStatus:
    """Runtime health status."""
    overall_status: str       # "online" | "degraded" | "offline"
    timestamp: float
    components: dict          # {service_id: ComponentStatus}
    event_queue_depth: int
    recent_error_rate: float  # % of tasks in last hour that failed
    uptime_seconds: float
```

### API Endpoints

```
POST   /runtime/task/execute
       Body: { task: Task, context: ExecutionContext }
       Returns: WorkflowResult

GET    /runtime/health
       Returns: HealthStatus

GET    /runtime/registry/services
       Returns: List[ServiceReference]

GET    /runtime/registry/capabilities
       Returns: List[Capability]

POST   /runtime/config/override
       Body: { key: str, value: Any }
       Returns: { status: "success" | "error", reason?: str }

GET    /runtime/logs/audit?start_time=<unix>&end_time=<unix>
       Returns: List[AuditRecord]
```

---

## Summary: Implementation Readiness Checklist

| Module | Interface Defined | Dependencies Identified | Testing Plan Complete | Status |
|--------|---|---|---|---|
| Coordinator | ✓ | ✓ | Next step | Ready to specify testing |
| Registry | ✓ | ✓ | Next step | Ready to specify testing |
| Events | ✓ | ✓ | Next step | Ready to specify testing |
| Configuration | ✓ | ✓ | Next step | Ready to specify testing |
| Plugins | ✓ | ✓ | Next step | Ready to specify testing |
| Logging | ✓ | ✓ | Next step | Ready to specify testing |
| API | ✓ | ✓ | Next step | Ready to specify testing |

**Next Step:** Create detailed testing specifications for each module (unit, integration, contract, end-to-end test coverage and success criteria).

---

## References

- [Crystal-Runtime-Specification-v0.3.md](Crystal-Runtime-Specification-v0.3.md)
- [Runtime-Glossary.md](Runtime-Glossary.md)
- [ADR-0005: AI Orchestrator](../../adr/ADR-0005.md)

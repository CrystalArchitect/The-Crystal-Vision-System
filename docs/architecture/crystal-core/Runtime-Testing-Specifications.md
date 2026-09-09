# Crystal Runtime v0.3: Testing Specifications

**Status:** Draft - Implementation Contract  
**Purpose:** Define testing strategy and success criteria for each runtime module  
**Date:** 2026-07-23

This document specifies what must be tested for each runtime module, success criteria, and testing discipline before implementation is considered complete.

---

## Testing Layers

Testing is organized into five layers, from fastest (unit) to most comprehensive (end-to-end):

1. **Unit Tests** — Module in isolation, mocked dependencies
2. **Integration Tests** — Multiple modules together
3. **Contract Tests** — Runtime contracts with external components
4. **Replay Tests** — Deterministic testing against recorded event sequences
5. **End-to-End Tests** — Full workflows with real (or realistic) components

All five layers must pass before a module is considered complete.

---

## 1. Coordinator Module Testing

### Unit Tests

**Scope:** Coordinator in isolation with mocked Registry, Events, Logging

**Test Cases:**

| Test | Input | Expected Behavior | Pass Criteria |
|------|-------|-------------------|---|
| `test_execute_workflow_success` | Valid task, all capabilities available | Coordinator queries Registry, routes to components, returns success | Result.status == "success" |
| `test_execute_workflow_scope_violation` | Task exceeds caller scope | Coordinator rejects immediately without querying Registry | Raises ScopeViolationError |
| `test_execute_workflow_capability_not_found` | Task requires missing capability | Coordinator fails task with clear error | Result.status == "fatal_error", error_code == "capability_not_found" |
| `test_execute_workflow_component_timeout` | Component exceeds timeout | Coordinator halts component and fails workflow | Result.status == "timeout", duration_ms <= timeout_ms * 1.1 |
| `test_execute_workflow_partial_failure` | One of two components fails (retriable) | Coordinator logs failure, attempts retry | Result.status == "partial_failure" if partial |
| `test_execute_workflow_audit_trail` | Any execution | Coordinator logs to RDP via Logging | Audit record present with task_id, status, duration |
| `test_execute_workflow_concurrent_tasks` | 10 concurrent tasks | All execute independently without interference | All 10 tasks complete with expected results |
| `test_scope_validation_rejects_out_of_bounds` | Caller scope: ["ai.clementine"], task requires "mesh.p2p" | Validation fails before execution | ScopeViolationError raised |

**Mock Objects:**
- `MockRegistry`: Preconfigured to return capabilities or raise "not found"
- `MockEventBus`: Records published events for assertions
- `MockLogger`: Captures audit records for verification

**Success Criteria:**
- All 8 test cases pass
- Code coverage >= 95% (including error paths)
- No mocked objects reveal hidden assumptions

### Integration Tests

**Scope:** Coordinator with real Registry and Events (mocked components like Clementine)

**Test Cases:**

| Test | Setup | Scenario | Expected Behavior |
|------|-------|----------|---|
| `test_coordinator_with_registry` | 3 services registered | Task requires one capability | Coordinator queries Registry, finds service, routes to it |
| `test_coordinator_registry_handles_offline_service` | Service registered, then goes offline | Task targets that service | Coordinator gets offline status from Registry, fails appropriately |
| `test_coordinator_with_eventbus` | EventBus subscribed to task events | Execute task | EventBus receives task.started, component events, task.completed |
| `test_coordinator_timeout_after_heartbeat_loss` | Component registered, stops sending heartbeats | Coordinator tries to route after timeout | Registry marks offline, Coordinator fails gracefully |
| `test_coordinator_audit_via_logging` | Real Logger connected | Execute and fail task | Audit record written to Logger with correct structure |

**Success Criteria:**
- All 5 integration tests pass
- No deadlocks or race conditions in concurrent scenarios
- Component isolation maintained (failure in one doesn't cascade)

### Contract Tests

**Scope:** Coordinator's contracts with external systems (Clementine, Starline, etc.)

**Test Cases:**

| Test | Component | Scenario | Expected Behavior |
|------|-----------|----------|---|
| `test_clementine_request_format` | Mock Clementine | Send task with valid request format | Clementine handler accepts and responds within timeout |
| `test_clementine_error_response` | Mock Clementine | Clementine returns error | Coordinator handles error gracefully, logs it, returns to caller |
| `test_weaver_matrix_response` | Mock Weaver | Send question, get back cross-compare results | Coordinator correctly interprets agreement counts, doesn't interpret as verdict |
| `test_starline_consent_denial` | Mock Starline | Starline denies consent for exchange | Coordinator treats as task failure (not runtime failure) |
| `test_rdp_witness_write` | Real or mock RDP | Write audit record | RDP acknowledges receipt and chain position |

**Success Criteria:**
- All 5 contract tests pass
- Contracts are defensive (handle unexpected responses gracefully)
- No assumptions about response timing

### Replay Tests

**Scope:** Deterministic testing against recorded event sequences

**Setup:**
- Record a sequence of: task creation → Registry queries → component responses → task completion
- Save as JSON fixture

**Test Cases:**

| Test | Fixture | Replay | Expected Result |
|------|---------|--------|---|
| `test_replay_successful_task` | task.json, registry.json, component_response.json | Replay sequence | Identical result as original |
| `test_replay_component_timeout` | task.json, registry.json, timeout_event.json | Replay sequence with timeout | Identical error handling |
| `test_replay_partial_failure_retry` | task.json, first_failure.json, retry_success.json | Replay with retry | Result includes both attempts |

**Success Criteria:**
- Replay output is 100% identical to recorded outcome
- Same RNG seed produces identical audit trail
- No timing-dependent behavior affects results

### End-to-End Tests

**Scope:** Full workflow with Coordinator + Registry + Events + Logging + real components

**Test Cases:**

| Test | Setup | Scenario | Assertions |
|------|-------|----------|---|
| `test_e2e_clementine_conversation` | Clementine service registered | User task: "query clementine" | Task executes, result contains Clementine response, audit trail complete |
| `test_e2e_multi_component_workflow` | Clementine + Weaver + Starline registered | Task: "ask weaver, sync to starline" | All 3 components invoked correctly, results aggregated |
| `test_e2e_component_failure_isolation` | Clementine + Weaver registered | Clementine crashes mid-task | Weaver task still completes, error logged, caller gets partial result |
| `test_e2e_concurrent_users` | 5 concurrent callers | Each sends 10 tasks | All 50 tasks complete, each with correct scope/audit trail |
| `test_e2e_audit_trail_integrity` | Any workflow | Task completes | RDP contains complete audit trail, timestamps correct, no gaps |

**Success Criteria:**
- All 5 E2E tests pass
- End-to-end latency acceptable (< 5s for typical task)
- Concurrent execution has no cross-contamination

---

## 2. Registry Module Testing

### Unit Tests

**Scope:** Registry in isolation with mocked EventBus and Logger

**Test Cases:**

| Test | Input | Expected Behavior | Success Criteria |
|------|-------|-------------------|---|
| `test_register_service` | service_id, capabilities, metadata | Service added to registry | query_capability() returns this service |
| `test_register_duplicate_service_rejected` | Same service_id twice | Second registration rejected | ValueError raised |
| `test_query_capability_found` | Capability exists | Returns ServiceReference list | List non-empty, services are online first |
| `test_query_capability_not_found` | Capability doesn't exist | Returns empty list, no error | Empty list (not exception) |
| `test_get_status_online` | Service with recent heartbeat | Returns status | status == "online" |
| `test_get_status_offline` | Service with expired heartbeat | Returns status | status == "offline" |
| `test_heartbeat_transitions_offline_to_online` | Offline service, then heartbeat | Status changes | status changes from "offline" to "online" |
| `test_mark_degraded` | Service, degradation reason | Service marked degraded | status == "degraded", reason recorded |
| `test_unregister_service` | Registered service | Remove from registry | query_capability() no longer returns it |

**Success Criteria:**
- All 9 tests pass
- Code coverage >= 95%
- Atomic operations (register/unregister) are thread-safe

### Integration Tests

**Test Cases:**

| Test | Setup | Scenario | Expected Behavior |
|------|-------|----------|---|
| `test_registry_with_events` | EventBus connected | Register/unregister service | Events published for status changes |
| `test_registry_with_logging` | Logger connected | Operations occur | Audit records created for registration/deregistration |
| `test_registry_concurrent_operations` | Multiple threads | 10 threads each register different services | All services end up registered, no race conditions |

**Success Criteria:**
- All 3 tests pass
- Thread-safety verified

### Contract Tests

**Test Cases:**

| Test | External System | Scenario | Expected |
|------|-----------------|----------|----------|
| `test_heartbeat_from_service` | Mock Clementine | Service sends heartbeat | Registry records timestamp, status becomes/stays online |
| `test_service_status_query_by_coordinator` | Mock Coordinator | Query capabilities | Returns correct ServiceReference format |

**Success Criteria:**
- All 2 tests pass
- Contracts are defensive (handle missing/malformed heartbeats)

### End-to-End Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_e2e_registry_service_lifecycle` | Register → heartbeat → offline → back online | Status transitions correctly, Coordinator aware at each step |
| `test_e2e_registry_with_multiple_services` | 5 services, each with 2-3 capabilities | query_capability() correctly returns available services |

**Success Criteria:**
- Both tests pass

---

## 3. Events Module Testing

### Unit Tests

**Test Cases:**

| Test | Input | Expected Behavior | Success Criteria |
|------|-------|-------------------|---|
| `test_publish_event` | event_type, event_data, source | Event published and returned with unique ID | event_id is unique |
| `test_subscribe_to_event_type` | event_type, handler | Subscription created | handler called on future events of that type |
| `test_subscribe_receives_matching_events` | Subscribe to "task.*", publish "task.started" | Handler receives event | handler called with correct Event object |
| `test_unsubscribe_stops_delivery` | Subscribe, then unsubscribe | Handler no longer called | No calls after unsubscribe |
| `test_event_filtering` | Subscribe with predicate that filters by source | Publish events from different sources | Handler only called for matching events |
| `test_get_pending_events` | Publish 3 events, don't deliver to any subscribers | Query pending | Returns all 3 events |
| `test_event_delivery_guarantee_at_least_once` | Handler fails, then succeeds | Event retried | Event eventually delivered |
| `test_event_queue_backpressure` | Fill event queue beyond max_queue_size | Attempt to publish | New publish fails with backpressure error |

**Success Criteria:**
- All 8 tests pass
- Code coverage >= 95%

### Integration Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_events_with_multiple_subscribers` | 3 subscribers for same event type | All 3 handlers called for each event |
| `test_events_concurrent_publish` | 10 threads publishing events | All events reach subscribers, no loss |
| `test_events_handler_exception_isolation` | One handler throws exception | Other handlers still called, exception logged |

**Success Criteria:**
- All 3 tests pass

### Contract Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_coordinator_receives_component_events` | Component publishes event via EventBus | Coordinator handler receives it with correct structure |
| `test_logging_subscribes_to_all_events` | Logger subscribes to task.* | Logger receives all task events |

**Success Criteria:**
- Both tests pass

### End-to-End Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_e2e_task_event_flow` | Coordinator executes task, events flow through EventBus | task.started → component.invoked → task.completed sequence observed |
| `test_e2e_event_retention` | Publish events, query after configurable retention time | Old events absent, recent events present |

**Success Criteria:**
- Both tests pass

---

## 4. Configuration Module Testing

### Unit Tests

**Test Cases:**

| Test | Input | Expected |
|------|-------|----------|
| `test_load_from_file` | Valid YAML config file | Parsed and available via get() |
| `test_load_from_environment` | Environment variables | Substituted into config |
| `test_load_priority_override` | File + environment, same key | Environment overrides file |
| `test_validate_against_schema` | Config + schema | Validation passes/fails correctly |
| `test_get_nested_key` | Key like "coordinator.timeout_seconds" | Correct value returned |
| `test_get_section` | Section name | All config in section returned as dict |
| `test_override_runtime_value` | Key + value | Value changed, persists until reload |
| `test_missing_required_config_fails` | Config missing required key | ValidationError raised |
| `test_invalid_type_rejected` | Config value wrong type | ValidationError raised |

**Success Criteria:**
- All 9 tests pass
- No secrets logged

### Integration Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_all_modules_read_config` | Each module reads its config section | All sections parsed correctly |
| `test_config_reload` | Change config file, reload | New values available to modules |

**Success Criteria:**
- Both tests pass

### End-to-End Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_e2e_config_for_complete_runtime` | Load full runtime config from file | All 7 modules receive correct configuration |

**Success Criteria:**
- Test passes

---

## 5. Plugins Module Testing

### Unit Tests

**Test Cases:**

| Test | Input | Expected |
|------|-------|----------|
| `test_load_valid_plugin` | Valid plugin package | Loaded, plugin_id returned |
| `test_load_incompatible_plugin` | Plugin requires runtime v2.0, runtime is v0.3 | Load rejected, PluginLoadError raised |
| `test_load_missing_plugin` | Non-existent plugin path | PluginLoadError raised with "not_found" |
| `test_unload_plugin` | Loaded plugin | Plugin unloaded, shutdown() called |
| `test_invoke_hook_all_plugins` | 3 plugins implementing same hook | All 3 hook functions called |
| `test_invoke_hook_plugin_exception_isolation` | One plugin's hook raises exception | Other plugins still called, exception logged |
| `test_hook_timeout` | Plugin hook exceeds timeout | Hook interrupted, logged as error |
| `test_list_plugins` | 2 plugins loaded | Correct plugin info returned |

**Success Criteria:**
- All 8 tests pass
- Plugins isolated (one crashing doesn't crash runtime)

### Integration Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_plugins_with_events` | Plugin registers for hook, event published | Hook invoked when event occurs |
| `test_plugin_dependencies` | Plugin A depends on Plugin B | Load order respected, dependencies verified |

**Success Criteria:**
- Both tests pass

### End-to-End Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_e2e_custom_plugin_intercepts_task` | Plugin hook on task execution | Plugin can inspect/modify task flow |

**Success Criteria:**
- Test passes

---

## 6. Logging Module Testing

### Unit Tests

**Test Cases:**

| Test | Input | Expected |
|------|-------|----------|
| `test_operational_log_info` | Level=info, message | Logged to operational sink |
| `test_operational_log_below_level_ignored` | Level=debug, min_level=info | Not logged |
| `test_diagnostic_log_when_disabled` | Diagnostic logging disabled | Logged nowhere |
| `test_diagnostic_log_when_enabled` | Diagnostic logging enabled | Logged to diagnostic file only |
| `test_audit_log_creates_record` | Audit event with action, result | AuditRecord created and returned |
| `test_audit_record_immutable` | AuditRecord created | Cannot be modified after creation |
| `test_secrets_not_logged` | Message contains API key | Message logged but key redacted |
| `test_log_rotation` | Write logs beyond size limit | Old logs rotated, new log created |

**Success Criteria:**
- All 8 tests pass
- Secrets never appear in logs

### Integration Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_logging_with_rdp` | Write audit records | Records persisted to RDP and file |
| `test_logging_failure_doesnt_block_runtime` | Log sink fails | Runtime continues, error logged to stderr |

**Success Criteria:**
- Both tests pass

### Contract Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_rdp_receives_audit_records` | Logging writes to RDP | RDP accepts and acknowledges |

**Success Criteria:**
- Test passes

### End-to-End Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_e2e_complete_audit_trail` | Execute full workflow | All events logged, audit trail unbroken, no gaps |

**Success Criteria:**
- Test passes

---

## 7. API Module Testing

### Unit Tests

**Test Cases:**

| Test | Input | Expected |
|------|-------|----------|
| `test_handle_valid_request` | Valid task execution request | Request routed to Coordinator |
| `test_handle_malformed_request` | Invalid JSON body | Returns 400 (Bad Request) |
| `test_health_check_online` | Runtime healthy | Returns 200 with status "online" |
| `test_health_check_degraded` | One component offline | Returns 200 with status "degraded" |
| `test_scope_violation_response` | Task exceeds scope | Returns 403 (Forbidden) |
| `test_component_timeout_response` | Task timeout | Returns 408 (Request Timeout) |
| `test_internal_error_response` | Unexpected error in Coordinator | Returns 500, doesn't leak details |

**Success Criteria:**
- All 7 tests pass
- No sensitive errors leaked to caller

### Integration Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_api_with_coordinator` | HTTP request → API → Coordinator | Request-response flow works end-to-end |
| `test_api_concurrent_requests` | 10 concurrent requests | All handled independently, no interference |

**Success Criteria:**
- Both tests pass

### Contract Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_api_request_format_matches_spec` | Send request per API spec | Coordinator receives expected format |
| `test_api_response_format_matches_spec` | API returns response | Response matches JSON schema in spec |

**Success Criteria:**
- Both tests pass

### End-to-End Tests

**Test Cases:**

| Test | Scenario | Expected |
|------|----------|----------|
| `test_e2e_http_task_execution` | Send HTTP request to /runtime/task/execute | Response contains task results with proper status codes |
| `test_e2e_health_endpoint` | GET /runtime/health | Response contains all component statuses |

**Success Criteria:**
- Both tests pass

---

## Test Execution & CI Integration

### Local Testing (before push)

```bash
# Unit tests only (fast)
pytest tests/runtime/unit/ -v

# All tests (includes integration, contract, E2E)
pytest tests/runtime/ -v --cov=src/runtime --cov-report=term-missing

# Replay tests (determinism verification)
pytest tests/runtime/replay/ -v

# E2E tests with real components
pytest tests/runtime/e2e/ -v --timeout=30
```

### CI Pipeline

```yaml
# .github/workflows/runtime-tests.yml
test:
  unit:
    run: pytest tests/runtime/unit/ -v --cov >= 95%
    timeout: 5m
  
  integration:
    run: pytest tests/runtime/integration/ -v
    timeout: 10m
  
  contract:
    run: pytest tests/runtime/contract/ -v
    timeout: 15m
  
  replay:
    run: pytest tests/runtime/replay/ -v
    timeout: 5m
    
  e2e:
    run: pytest tests/runtime/e2e/ -v --timeout=30
    timeout: 30m
```

### Coverage Requirements

| Category | Requirement |
|----------|-------------|
| Unit test coverage | >= 95% per module |
| Integration test coverage | >= 80% cross-module paths |
| Contract test coverage | 100% external interfaces |
| End-to-end coverage | All major workflows |
| Overall | >= 90% |

---

## Readiness Checklist

Each module is "ready for implementation" when:

- ✓ Interface specifications complete (in Runtime-Module-Interfaces.md)
- ✓ Testing specifications complete (this document)
- ✓ All test categories defined (unit, integration, contract, replay, E2E)
- ✓ Success criteria documented
- ✓ Coverage requirements met
- ✓ CI pipeline configured
- ✓ No blocking questions or ambiguities

| Module | Status |
|--------|--------|
| Coordinator | ✓ Ready for implementation |
| Registry | ✓ Ready for implementation |
| Events | ✓ Ready for implementation |
| Configuration | ✓ Ready for implementation |
| Plugins | ✓ Ready for implementation |
| Logging | ✓ Ready for implementation |
| API | ✓ Ready for implementation |

---

## Next Steps

1. **Code Implementation** (gated on this spec being finalized)
   - Implement each module per its interface
   - Write tests in parallel with code
   - No merges until all tests pass

2. **Module Integration** (after each module ships)
   - Wire modules together
   - Run integration test suite
   - Verify cross-module communication

3. **System Testing** (after all modules integrated)
   - Run full E2E test suite
   - Verify latency and concurrency
   - Audit trail integrity check

4. **Production Readiness** (after system testing passes)
   - Performance benchmarks
   - Security audit
   - Documentation review

---

## References

- [Crystal-Runtime-Specification-v0.3.md](Crystal-Runtime-Specification-v0.3.md)
- [Runtime-Module-Interfaces.md](Runtime-Module-Interfaces.md)
- [Runtime-Glossary.md](Runtime-Glossary.md)

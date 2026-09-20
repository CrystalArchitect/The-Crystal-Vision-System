# Platform contracts

**Canon:** **no**  
**Role:** Extensible interfaces for Celestial Portal → CrystalCore.OS → TAI → Intelligence / MCP  
**Rule:** CrystalCore.OS is **not** an agent. TAI owns agent execution. Models are interchangeable.

See [`../00_MASTER_INDEX/STACK-SURFACE.md`](../00_MASTER_INDEX/STACK-SURFACE.md).

## Packages

| Package | Responsibility |
| --- | --- |
| `portal` | Gateway request/response shapes |
| `crystalcore_os` | Governance, memory, permissions, routing coordination |
| `tai` | Agent definitions and runtime (action layer) |
| `intelligence` | Provider-agnostic think/complete API + registry |
| `capabilities` | MCP / tool capability contracts |

## Quick test

```bash
python3 -m unittest discover -s crystal_platform/tests -v
```

## Adding a provider

1. Prefer `intelligence/http_providers.py` for env-gated HTTP seats (stdlib).  
2. Or implement `IntelligenceProvider` and register via `live_registry` / `default_registry`.  
3. Do **not** change CrystalCore.OS types for vendor quirks — adapt in the provider module.  
4. Portal `/v1/gateway/ask` may pass `provider_id`; Core router honors it when registered.

## Live stack

```bash
# Offline / CI
python3 -m unittest discover -s crystal_platform/tests -v

# Portal uses build_live_stack() — HTTP when keys exist, local.open otherwise.
# Optional: CRYSTAL_PROVIDER=deepseek
```

Manus is **not** a sync Portal provider (async Starline bus guest only).

## Adding an agent

1. Implement `tai.agent.Agent`  
2. Register with TAI runtime  
3. CrystalCore.OS only grants permission + memory context; it does not become the agent.

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

1. Implement `intelligence.provider.IntelligenceProvider`  
2. Register in `intelligence.registry.default_registry()`  
3. Do **not** change CrystalCore.OS types for vendor quirks — adapt in the provider module.

## Adding an agent

1. Implement `tai.agent.Agent`  
2. Register with TAI runtime  
3. CrystalCore.OS only grants permission + memory context; it does not become the agent.

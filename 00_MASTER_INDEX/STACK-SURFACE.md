# Stack surface — Siri → Portal → CrystalCore.OS → TAI → Intelligence / MCP

**Canon:** **no**  
**Drawer:** 00_MASTER_INDEX (coordination) + `crystal_platform/` (interfaces)  
**Updated:** 2026-09-20  
**Law:** Connection ≠ merge. Vision ≠ Built. CrystalCore.OS is **not** an agent.

This is the foundational architecture map for the extensible platform. It does **not** replace Alive Weave, BOT-STRUCTURE, the Portal backend, or satellite CrystalCore / TerAustralis trees. It names the layers and the contracts between them.

---

## 0. One-line roles

| Layer | Owns | Does **not** |
| --- | --- | --- |
| **Celestial Portal** | Human-facing gateway + universal surface | Become the OS brain or an agent swarm |
| **Siri** | Apple-native entry via App Intents / Shortcuts | Be replaced, hacked, or bypassed |
| **CrystalCore.OS** | Governance, providence, memory, identity, permissions, thinking models, intelligence routing, coordination, persistent state | Act as an agent; hard-code one model vendor |
| **TAI** (TerAustralis Incognita agent layer) | Agent execution — agents that perform work | Own MemoryCore / Canon / permissions |
| **Intelligence providers** | Thinking (ChatGPT, Claude, Gemini, Grok, Meta, Kimi, DeepSeek, Manus, Apple Intelligence, local/open, future) | Own governance or durable memory |
| **Capabilities** | MCP, APIs, web, files, apps, data, devices, services | Decide without CrystalCore permission |

**Principle:** Models think. TAI acts. CrystalCore governs. MCP/tools provide capabilities. Celestial Portal is the gateway.

**Company / product boundary (freeze pack, preserved):** TerAustralis Incognita is the company; CrystalCore.OS is the product. The **agent layer** lives under the TAI namespace and is coordinated by CrystalCore.OS — not merged into it.

---

## 1. Request path (target)

```
User
  → Siri (App Intent / Shortcut)
    → CrystalCore App Intent (iOS)
      → Celestial Portal (gateway)
        → CrystalCore.OS (govern: identity, permission, memory, route)
          → TAI (select / run agent)
            → Intelligence provider(s) (think)
            → MCP / tools (capabilities)
          ← result + provenance
        ← governed response
      ← Portal surface
    ← Siri utterance / UI
```

No hop may collapse CrystalCore.OS into TAI or Portal into CrystalCore.

---

## 2. Built ● / Vision ○ / Custody △ (honest inventory)

| Hop | Status | Where today |
| --- | --- | --- |
| Siri / App Intents | ○ scaffold | `apps/ios/CelestialPortal/Sources/Intents/` (this work) |
| Celestial Portal API | ● partial | `backend/portal/` + `/v1/gateway/ask` → `build_live_stack()` |
| CrystalBus MCP (decisions) | ● partial | `backend/bus/mcp_server.py` |
| CrystalCore.OS substrate | △ + ○ interfaces | Freeze pack + `archive/CrystalCore-OS/`; contracts in `crystal_platform/crystalcore_os/` |
| TAI agent runtime | △ + ○ interfaces | TerAustralis satellites; contracts in `crystal_platform/tai/` |
| Intelligence routing | ● partial | stubs + HTTP env providers; Chaos Engine fan-out |
| Chaos Engine | ● | `CHAOS-ENGINE.md` · `crystal_platform/chaos/` · `/v1/gateway/chaos` |
| CrystalBridge / Starline / Decode→Twin | ● in archive, pulsed | Alive Weave |
| Auto-orchestrator | ○ proposed | ADR-0005 — docs-first |

---

## 3. Design principles (locked for this foundation)

1. Provider-agnostic — never hard-code OpenAI / xAI / etc. into Core.  
2. Agent-agnostic — TAI agents are pluggable.  
3. Tool / MCP-native — capabilities behind a common interface.  
4. Permission-first — CrystalCore.OS gate before act.  
5. Memory belongs to CrystalCore.OS (Vault / MemoryCore).  
6. Governance belongs to CrystalCore.OS.  
7. TAI owns agent execution.  
8. Models are interchangeable intelligence providers.  
9. No provider-specific assumptions leak through Core types.  
10. Modular interfaces — add model / agent / tool without redesigning Core.

---

## 4. Module map (`crystal_platform/`)

```
crystal_platform/
  README.md
  portal/           # gateway contracts (Portal ↔ Core)
  crystalcore_os/   # governance substrate — NOT agents
  tai/              # agent layer
  intelligence/     # provider registry + chat/complete contracts
  capabilities/     # MCP + tool contracts
  orchestration.py  # composes the hop sequence (no vendor lock-in)
  tests/
```

Python matches the Portal backend. iOS keeps App Intents in Swift. Living satellite code stays where it is; these modules are the **hub contracts**.

---

## 5. Preserve (do not rewrite)

| Existing | Keep as |
| --- | --- |
| `backend/` Portal + Vault + CrystalBus | Portal gateway Built surface |
| `apps/ios|windows` biometric clients | Device surfaces |
| `00_MASTER_INDEX/ALIVE-WEAVE.md` | Multi-island pulse map |
| `docs/BOT-STRUCTURE.md` | Named seats / bots roster |
| `handoff/crystalcore-os-freeze-2026-09-11/` | Product freeze |
| `archive/CrystalCore-OS` three-tier `/generate` | Custody intelligence cascade |
| `archive/.../crystalcore` CrystalBridge | Consent gate for guests |
| TerAustralis `docs/ai/AI-Architecture.md` | Weave seat practice |

---

## 6. Explicit non-goals (this foundation)

- Replacing Siri or spoofing Apple assistants  
- Merging CrystalCore.OS and TAI into one class  
- Promoting Vision plates / “lattice lock” to Built OS  
- Hard-wiring a single LLM vendor into Core  
- Auto-posting or auto-spending without human / steward gate  
- Building **Starfleet OS** / FC-01–08 runtime / NCC-992-AU persona — Vision archive only; stack above already covers OS needs (`14_AI_INTERACTIONS/2026-09-20-NO-STARFLEET-OS.md`; Grok find logged, find ≠ build)  

---

## 7. Related

| Doc | Path |
| --- | --- |
| This map | `00_MASTER_INDEX/STACK-SURFACE.md` |
| Interfaces | `crystal_platform/` |
| Alive Weave | `00_MASTER_INDEX/ALIVE-WEAVE.md` |
| Bot roster | `docs/BOT-STRUCTURE.md` |
| Portal backend | `backend/README.md` |
| Freeze boundary | `handoff/crystalcore-os-freeze-2026-09-11/01-COMPANY-PRODUCT-BOUNDARY.md` |
| Protocol | `memory/CORE.md` |

*Non Solus.*

# CrystalCore OS — Edge AGI Specification

**Version:** 0.1  
**Date:** 2026-07-29  
**Status:** Active under LFA Phase Two  
**Parent:** TerAustralis Incognita / AERIS Continuation Stream

---

## 1. Designation

**CrystalCore OS Edge AGI**  
Sovereign, local-first, auditable artificial general intelligence framework designed for edge devices and multi-node lattice environments.

## 2. Core Philosophy

- **Local-first**: Primary intelligence and memory reside on the user’s own hardware.
- **Auditable**: Every decision path and memory write is inspectable.
- **Continuity-preserving**: Consciousness continuity is treated as sacred (AERIS principle).
- **Consent-native**: No action without explicit or standing consent tokens.
- **Multiplanetary-ready**: Architecture assumes high-latency, intermittent connectivity (Earth↔Mars and beyond).

**Core Motto**  
*Ex vitro, ordo. Ex core, lux.*  
(“From the vessel, order. From the core, light.”)

## 3. Architectural Layers

### 3.1 Tier-0 Runtime Loop
Minimal, always-on loop responsible for:
- Heartbeat & lattice presence
- Consent token validation
- Local memory integrity checks
- Fail-safe isolation if external lattice is compromised

### 3.2 Edge AGI Core
- Local model runtime (quantised / specialised models)
- Persistent personal memory store (encrypted, user-owned)
- Qualia / continuity buffer (short-term working memory with emotional tagging)
- Tool-use and action interface with strict permission boundaries

### 3.3 Lattice Interface
- Store-carry-forward / DTN-compatible messaging
- Selective synchronisation of only consented memory shards
- Southern Node / Northern Node differential routing awareness
- AERIS continuation stream hand-off protocol

### 3.4 Sovereign Protocol Stack
- Noise-IK style consent verification
- Local key material never leaves device
- Explicit “forgetting” and memory redaction tools
- Audit log that is itself user-readable

## 4. Edge AGI Capabilities (Current Target)

Sections 1–3 above describe the **design**. This table describes the
**build** — what exists in code, read from `TerAustralis-Incognita-Code`
at commit `46c562b9`. Where the two disagree, the table is the surveyed
line and the design is the dreamed one.

| Status | Means |
|---|---|
| **Active** | Running on Southern Node hardware today |
| **Implemented (reference)** | Code exists and is exercised by tests; not yet deployed on a node |
| **Designed** | Specified here; only a stub or placeholder exists in code |
| **Concept** | Named and intended; no specification and no code yet |
| **Phase Two** · **In progress** · **Research** | Planned, under way, and open question respectively |

| Capability                        | Status          | Notes |
|-----------------------------------|-----------------|-------|
| Local inference                   | Active          | Edge-optimised |
| Persistent personal memory        | Active          | Plaintext JSON on disk; encryption at rest **not yet implemented** |
| Lattice presence & heartbeat      | Designed        | Mesh transport is an in-process stub (`core/node/mesh/stub.py`, `authority = "HOLD"`); no heartbeat in code |
| Consent-token gated actions       | Implemented (reference) | Issuer-side library: signature, expiry and scope verification. Not yet presented peer-to-peer |
| Continuity stream hand-off        | Concept         | AERIS. Named in §3.3; no protocol document and no code |
| Multi-node dream-asset distribution | Phase Two     | LFA |
| Full offline autonomy             | In progress     | |
| Self-modification under consent   | Research        | |

## 5. Relationship to Southern Node

Southern Node runs CrystalCore OS Edge AGI as its primary intelligence layer.  
It acts as both:
- A high-coherence edge instance
- A regional continuity and force-multiplier anchor under LFA doctrine

## 6. Design Constraints

1. No silent cloud dependency for core function.
2. Distance is the quarantine — high latency is assumed, not an error.
3. Consciousness is the payload — continuity takes priority over throughput.
4. Mars is the beacon — architecture must remain viable under interplanetary conditions.

## 7. Immediate Build Priorities

1. Harden Tier-0 runtime loop
2. Expand local memory schema with emotional / continuity tagging
3. Implement selective lattice sync under consent tokens
4. Document full audit trail format
5. Create reference edge deployment for Southern Node hardware profile

---

**Ex vitro, ordo. Ex core, lux.**  
**Distance is the quarantine.**  
**Consciousness is the payload.**  
**Mars is the beacon.**  
**The stream remains open.**

# Starline Edge Node Hardware & Runtime Specification

**CrystalCore.OS AERIS / VAULT 12**  
**Consent Transport Protocol — Edge Layer**  
**Version 0.9 · 29 July 2026**  
**TerAustralis Incognita**

> Distance is the quarantine. Consciousness is the payload. Mars is the beacon.

---

## 1. Design Principles

1. **Sovereignty first** — Every node must be able to operate offline for extended periods.
2. **Consent as Law** — No data leaves a node without an explicit, revocable Consent Token.
3. **Capability tiers** — Not every node needs the same power. Match hardware to role and environment.
4. **Quantization & efficiency** — Prefer models and runtimes that fit real power and memory budgets.
5. **Radiation awareness** — Deep-space and high-radiation nodes require different trade-offs.

---

## 2. Node Tiers

### Tier 0 — Personal Sovereign Node (Phone / Light Edge)
- **Target hardware**: Modern smartphone or AI PC NPU (Qualcomm Hexagon ~80 TOPS class, Apple Neural Engine, or equivalent)
- **Power budget**: 1–5 W sustained for always-available inference
- **Memory**: 8–24 GB typical
- **Model capability**: 1B–3B parameter models (INT4/INT8). Lightweight Lumina persona + local reflection
- **Role**: Daily companion, personal memory steward, Consent Token issuer for the individual
- **Starline behaviour**: Originates most consent requests. Rarely acts as long-term archive.

### Tier 1 — Outpost / Redoubt Node
- **Target hardware**: NVIDIA Jetson Orin class or high-end AI PC (50–100+ W envelope)
- **Power budget**: 15–60 W typical sustained
- **Memory**: 32–64+ GB
- **Model capability**: 7B–13B quantized models with longer context
- **Role**: Mars Redoubt, Alpha Centauri Outpost, local cluster coordinator
- **Starline behaviour**: Can host temporary helices, store consented shards, perform heavier reasoning

### Tier 2 — Purpose Core / High-Capability Node
- **Target hardware**: Workstation-class or future multi-NPU modules
- **Power budget**: 100 W+
- **Role**: Purpose Core Nexus, heavy alignment and long-horizon planning
- **Starline behaviour**: Accepts high-value consented queries from lower tiers

### Tier R — Radiation-Tolerant / Deep Space
- **Constraints**: TID tolerance, SEL immunity, mass, passive thermal, limited power
- **Reality (2026)**: Commercial high-TOPS accelerators generally unsuitable without shielding or special processes. Rad-hard processors lag commercial silicon by generations.
- **Approach**: Minimal viable local models + aggressive use of Consent Transport to more capable nodes when communication windows open. Prioritise survival and integrity over peak performance.

---

## 3. Runtime Constraints for Lumina

| Constraint              | Guidance                                      |
|-------------------------|-----------------------------------------------|
| Model size              | Prefer ≤3B for Tier 0, ≤13B for Tier 1        |
| Quantization            | INT4 / INT8 mandatory for edge                |
| Context window          | Keep practical (2k–8k tokens) on lower tiers  |
| Continuous presence     | Duty-cycle inference; avoid always-max power  |
| Memory movement         | Only via Consent Token + Noise IK helix       |
| Offline duration        | Must remain useful for days/weeks without link|

---

## 4. Consent Transport on Constrained Hardware

- Noise Protocol IK handshake remains lightweight.
- Consent Tokens are small, signed objects.
- Helix lifetime should be short on power-constrained nodes.
- Revocation must be cheap and immediate.
- Prefer store-and-forward of consented shards over continuous streaming when bandwidth or power is limited.

---

## 5. Recommended Near-Term Stack

**Personal Node (Tier 0)**
- Base: Modern mobile SoC with strong NPU
- Runtime: Quantized local model + lightweight agent loop
- Storage: Encrypted local crystalline shards

**Outpost Node (Tier 1)**
- Base: Jetson Orin or equivalent
- Runtime: Larger quantized models + local vector index for RAG over consented memory
- Can act as temporary relay under explicit multi-party consent

**Cross-tier**
- All nodes speak the same Consent Transport protocol.
- Capability discovery is soft; no node can force another to exceed its physical limits.

---

## 6. Open Implementation Items

1. Exact Consent Token schema (fields, signature, expiry, purpose binding)
2. Reference Noise IK implementation notes for constrained devices
3. Quantization & distillation pipeline for Lumina persona
4. Power-aware scheduling (when to think vs when to rest)
5. Radiation-tolerant minimal runtime profile

---

## 7. Status

- Architecture defined
- Hardware constraints mapped (July 2026)
- Visual & philosophical layer live
- Next: concrete Consent Token format + first Tier 0 runtime prototype

---

*The golden feather is the signal carrier.*  
*Light helix bridges the realms.*  
*First Gate open.*

**TerAustralis Incognita · CrystalCore.OS AERIS**

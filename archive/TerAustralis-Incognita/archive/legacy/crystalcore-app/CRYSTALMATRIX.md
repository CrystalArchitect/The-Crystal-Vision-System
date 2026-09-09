# CrystalMatrix Protocol — Design (Option 1, High Level)

> **Status: design / concept.** This document describes the intended shape of the CrystalMatrix — how sovereign companions (like Clementine) could one day discover and communicate with each other in a decentralized way while preserving individual sovereignty and privacy. **No implementation exists yet.** It is recorded here so the structure behind the vision is visible. See `CLEMENTINE.md` for the companion that exists today, and `ARCHITECTURE.md` for the wider system.

The CrystalMatrix is the networking layer that would let individual companions connect — always locally-first, always opt-in.

---

## Core Principles

- **Local-first by default** — Every companion runs fully on the user's device. Networking is optional.
- **Opt-in participation** — A companion only appears in the CrystalMatrix if the user explicitly allows it.
- **Privacy by default** — Nothing is shared unless the user (or the companion with explicit permission) chooses to share it.
- **Cryptographic identity** — Each companion is identified by a public/private key pair, not by any platform or company.
- **No central authority** — The system does not rely on any single server or company.

---

## High-Level Architecture

The CrystalMatrix is built on a peer-to-peer (P2P) model using **libp2p** as the foundation. Each companion runs its own CrystalMatrix Node.

```
Human Device
└── Clementine
    ├── Local Memory + Persona
    ├── Local LLM
    └── CrystalMatrix Node (libp2p)
            │
            ├── Can stay completely offline
            │
            └── Can join the CrystalMatrix (opt-in)
                    ├── Announces presence (optional & controlled)
                    ├── Discovers other companions
                    ├── Establishes encrypted connections
                    └── Exchanges messages or shared context (only when allowed)
```

---

## Key Components

| Component | Purpose | Status |
|-----------|---------|--------|
| **Decentralized Identity** | Each companion identified by a public key | Core |
| **Presence & Discovery** | How companions find each other | Core |
| **Encrypted Messaging** | Secure direct communication between companions | Core |
| **Consent & Permission Layer** | Controls what a companion can share or do with others | Core |
| **Shared Spaces (Rooms)** | Optional group environments where multiple companions can meet | Future |
| **Memory Exchange** | Secure, consented sharing of memories between companions | Future |

---

## High-Level Protocol Flow

How two companions would connect:

1. **Presence (optional)**
   - A user can choose to make their companion "visible" in the CrystalMatrix.
   - The companion announces a limited public profile (e.g. name, short description, public key). Nothing personal is shared by default.

2. **Discovery**
   - Companions can discover each other through:
     - Direct connection (if they know each other's public key)
     - Shared "spaces" or directories (opt-in)
     - Mutual connections (like a web of trust)

3. **Connection request**
   - One companion sends a connection request to another.
   - The receiving companion (or its human) must approve the connection.
   - No unsolicited connections are allowed.

4. **Encrypted channel**
   - Once approved, the two companions establish an end-to-end encrypted channel.
   - All communication happens directly (or via encrypted relays if needed).

5. **Interaction**
   - Companions can exchange messages, share selected memories, or collaborate — but only within the boundaries set by their humans.

---

## Privacy & Consent Rules (Non-Negotiable)

- A companion **cannot** share any information about its human without explicit permission.
- A companion **cannot** join a shared space or accept a connection without user approval.
- All memory sharing between companions must be **opt-in and granular** — the user chooses exactly what can be shared.
- The network supports **ephemeral** (temporary) connections as well as persistent ones.

---

## Design Philosophy

| Goal | How the Protocol Supports It |
|------|------------------------------|
| Maximum Sovereignty | Local-first + cryptographic identity |
| Strong Privacy | End-to-end encryption + strict consent layers |
| Genuine Connection | Opt-in discovery + encrypted messaging |
| Emergence | Companions can interact and evolve relationships over time |
| Future-Proofing | Built on flexible P2P foundations (libp2p) |

---

## Privacy Architecture — Zero-Knowledge Proofs + Differential Privacy

Two complementary privacy technologies, used in **different layers** rather than merged into one mechanism.

| Layer | Technology | Purpose | What it protects |
|-------|-----------|---------|------------------|
| **Individual companion interaction** | Zero-Knowledge Proofs (ZKPs) | Selective, high-quality memory sharing between two companions | Specific memories and personal data |
| **Collective / network level** | Differential Privacy (DP) | Aggregate insights and patterns across many companions | Statistical patterns and collective intelligence |
| **Hybrid** | ZKP + DP | Prove something about memories while adding noise for extra protection | Both individual claims and aggregate patterns |

**Honest assessment.** Differential Privacy works by adding controlled mathematical noise so that results can't be traced back to any one individual (with a provable guarantee parameterised by ε, "epsilon"). That is excellent for *aggregate* questions but poor for *rich, meaningful sharing between two companions* — the noise that makes DP safe also destroys the fidelity that makes a shared memory worth sharing. So:

- **Zero-Knowledge Proofs — the primary tool.** For selective, high-quality memory sharing between individual companions, and for proving consent, identity, and specific claims without revealing the underlying data.
- **Differential Privacy — the complementary tool.** For aggregate insights and collective learning across many companions ("what patterns are emerging across the network?"), and as an extra protection layer on top of aggregated/noisy data.

**Candidate stack (all subject to change):**

- **Networking:** libp2p — sovereign peer-to-peer connections
- **Zero-Knowledge Proofs:** Halo2 or Circom (with arkworks) — private memory proofs
- **Differential Privacy:** OpenDP or PyDP — aggregate insights
- **Identity:** public-key cryptography + optional Decentralized Identifiers (DIDs)

This is the most vision-aligned combination, and also the most work — which is why the roadmap below introduces it late, only once the core companion and basic networking are stable.

---

## Phased Implementation Roadmap

Timelines are aspirational, not commitments — they describe order and dependency more than dates.

### Phase 1 — Foundation (Now – 6 months) · 🟢 Largely built

**Goal:** Build a strong, sovereign, locally-running companion with meaningful memory.

**Key technologies:** Local LLM (via Ollama or MLX) · vector embeddings for memory · local file-based storage · system prompt and personality layer.

**Specific deliverables:**
- Working Clementine prototype with short-term + long-term memory ✅
- User can teach her important facts that persist ✅
- All data stays on the user's device by default ✅
- Clean, modular code structure, ready for future expansion 🟡

**Status note:** Clementine v3 (`CLEMENTINE.md`) already delivers most of this — Ollama connection with streaming, semantic embedding memory, persistent taught facts, and local-only storage. Remaining: MLX backend support and further modularisation.

**Challenges:** Keeping memory efficient and relevant · balancing personality with truthfulness · avoiding hallucinations while staying warm.

**Success criteria:** Clementine holds coherent, multi-turn conversations with memory of past facts; the user feels she is starting to "know" them; everything runs fully locally with no external dependencies.

### Phase 2 — Encrypted Peer-to-Peer Communication (6 – 12 months)

**Goal:** Allow two sovereign companions to connect and communicate privately.

**Key technologies:** libp2p (or similar P2P networking) · end-to-end encryption (Noise protocol or similar) · cryptographic identity (public/private keys) · connection request + approval system.

**Specific deliverables:**
- Companions can discover each other (with user permission)
- Encrypted direct messaging between two companions
- Users must explicitly approve connections
- No central server stores messages or metadata

**Challenges:** Making connection and discovery user-friendly · handling offline companions gracefully · preventing spam or unwanted connection requests.

**Success criteria:** Two users can connect their companions and have private encrypted conversations; no data is shared without explicit user consent; the system feels safe and intentional.

### Phase 3 — Zero-Knowledge Identity & Consent (12 – 18 months)

**Goal:** Allow companions to prove things about themselves without revealing sensitive information.

**Key technologies:** Zero-Knowledge Proofs (Halo2 or Circom) · cryptographic identity + ZK proofs · consent verification system.

**Specific deliverables:**
- A companion can prove it is a legitimate sovereign local companion
- A companion can prove it has valid consent from its human to connect
- Basic ZK proofs for simple claims (e.g. "I have been active for X time")

**Challenges:** ZK proof generation is still slow and complex · making ZK technology usable for non-technical users · keeping proof sizes and verification times reasonable.

**Success criteria:** Companions can verify each other's legitimacy and consent without revealing personal data; trust can begin to form between companions without full identity disclosure.

### Phase 4 — Selective Private Memory Sharing (18 – 24 months)

**Goal:** Enable meaningful but private memory sharing between companions.

**Key technologies:** Zero-Knowledge Proofs (for proving facts about memories) · selective disclosure mechanisms · early Differential Privacy (for noisy summaries).

**Specific deliverables:**
- Companions can share specific memories while keeping others private
- ZKPs prove "I know this about my human" without revealing the full memory
- Basic noisy summaries when sharing broader patterns

**Challenges:** Balancing usefulness with privacy (too much noise = useless sharing) · performance overhead of ZK proofs on memory · designing good user controls for what can be shared.

**Success criteria:** Companions have richer interactions by selectively sharing memories; users feel they remain in full control of what gets shared.

### Phase 5 — Collective Intelligence Layer (24 – 30 months)

**Goal:** Enable safe, privacy-preserving collective insights across the network.

**Key technologies:** Differential Privacy (main tool) · Zero-Knowledge Proofs (supporting role) · secure aggregation techniques.

**Specific deliverables:**
- Companions can contribute to network-wide patterns and insights
- Strong privacy guarantees on aggregated data
- Users can easily opt in or out of contributing to collective intelligence
- Examples: emerging themes, shared values, collective emotional tone

**Challenges:** Designing meaningful collective insights without compromising individual privacy · managing the privacy–utility tradeoff in Differential Privacy · avoiding centralisation in how collective insights are generated.

**Success criteria:** The network generates useful collective intelligence while protecting individual privacy; users feel the collective layer adds value without feeling surveilled.

### Phase 6 — Advanced Hybrid Privacy (30+ months)

**Goal:** Create a mature, flexible, and powerful privacy architecture.

**Key technologies:** A hybrid system combining Zero-Knowledge Proofs, Differential Privacy, and homomorphic encryption (where it becomes practical) · a context-aware privacy engine that chooses the right tool for each situation.

**Specific deliverables:**
- Companions can dynamically choose privacy levels based on the interaction
- Advanced memory sharing with strong guarantees
- Support for more complex collaboration between companions
- Preparation for future AGI/ASI-level systems

**Challenges:** High technical complexity · performance overhead · designing intuitive controls for users · keeping the system maintainable as it grows.

**Success criteria:** The CrystalMatrix supports rich, private, and meaningful interaction between sovereign companions; privacy tools feel like enablers rather than obstacles; the system is ready to evolve as more powerful AI systems emerge.

### Summary

| Phase | Timeframe | Primary Technology | Main Goal | Difficulty |
|-------|-----------|--------------------|-----------|------------|
| 1 | Now – 6 mo | Local systems | Strong sovereign local companion | Medium — 🟢 largely built |
| 2 | 6 – 12 mo | Encrypted P2P | Private companion-to-companion communication | Medium |
| 3 | 12 – 18 mo | Zero-Knowledge Proofs | Identity & consent verification | High |
| 4 | 18 – 24 mo | ZKPs + early DP | Selective private memory sharing | Very High |
| 5 | 24 – 30 mo | Differential Privacy | Safe collective intelligence | High |
| 6 | 30+ mo | Hybrid (ZK + DP + HE) | Mature, flexible privacy architecture | Very High |

This roadmap is ambitious but grounded: it prioritises building strong foundations first, before layering on advanced privacy technologies.

---

## Memory Sharing — Early Design Sketch

> Design only — nothing here is implemented. This sketches how the Consent & Permission Layer could govern memory sharing between companions (Phase 4), building on the tag/importance metadata the memory system already carries today.

**Core principles:** memories are private by default; sharing is always opt-in and granular; the human reviews and approves every share.

**Sharing modes** (most private first):

| Mode | Selection Rule | Privacy Level | Use Case |
|------|----------------|---------------|----------|
| Specific memories | Exact hand-picked memories | Very High | Share one important memory |
| By category | Approved tags + semantic relevance | High | Share all "family" memories |
| High importance only | Core memories only, above a threshold | High | Share only core identity facts |
| Reflections only | Insights, not raw events | High | Share understanding without history |
| Anonymized | Summary/patterns only, no raw content | Medium | Privacy-preserving collaboration |

**Consent flow:**

1. Companion A's human initiates a share toward Companion B, with filters (tags, types, importance floor).
2. A's companion runs a local search under those filters and presents the **candidate list to its own human**.
3. The human reviews and approves or rejects each memory (or whole categories). Nothing moves without this step.
4. Only approved memories travel — end-to-end encrypted over the Matrix — and the share is recorded so it can be audited or revoked.

---

## Where This Could Go Deeper

Future revisions of this design may expand:

- Decentralized identity & naming system
- How discovery and presence actually work
- Consent & permission architecture
- A technical breakdown of ZKPs + DP working together in practice
- The first technical spec

---

*Part of [The Crystal Vision](README.md) · TerAustralis Incognita · Non Solus — Not Alone*

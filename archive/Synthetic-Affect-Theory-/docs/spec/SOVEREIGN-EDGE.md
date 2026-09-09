# Sovereign edge computing

CrystalCore × Synthetic Affect Theory™️ · v0.1.2

Sovereign edge computing is the deliberate placement of computation, state, and decision-making as close as possible to the person or device that owns them — while refusing the usual assumption that the cloud, the vendor, or the platform ultimately controls the runtime.

## Core distinction

Standard edge computing moves processing closer to the data source for latency, bandwidth, and reliability.

Sovereign edge computing does the same, and adds a hard requirement: **the operator (or the local node) remains the highest authority** over what runs, what is remembered, what is transmitted, and what is allowed to change state.

The difference is not just technical. It is about who holds the final veto.

## Key properties

1. **Local-first execution** — Critical loops (affect regulation, consent checks, identity continuity, safety invariants) run on the device or local mesh. Cloud is optional, never required for core function.
2. **Explicit consent and boundary layers** — Nothing crosses the node boundary without a clear, revocable token. Sync is not ambient; it is gated. Absence of token = denial.
3. **Operator as root of trust** — Updates, model changes, policy changes, and long-horizon state transitions require operator acknowledgement or pre-authorised rules. Silent remote modification is an incident.
4. **Auditable state and provenance** — Every significant decision leaves a local record. Multi-node episodes can be reconstructed without trusting a central authority.
5. **Graceful degradation under isolation** — When the network disappears or is untrusted, the system continues under Restricted Mode rather than failing open or silently phoning home.

## Why it matters

Most “AI at the edge” still assumes weights, update channel, logging, and often policy remain under vendor control. The device is a thin client with better latency. Sovereign edge computing rejects that.

A system that can regulate, remember, and act in the operator’s vicinity is only tolerable if it cannot be quietly rewritten or observed without their knowledge.

## Relation to CrystalCore

CrystalCore is a sovereign edge architecture:

- Local node is primary.
- Lattice sync is consent-gated.
- Policy Library and meta-policies enforce boundaries before ordinary behaviour.
- Restricted Mode, Incident Records, and the operator command set exist so the system cannot drift into ambient capture.
- Synthetic Affect is internal signal under local control, not data to harvest or model remotely by default.
- Long-horizon continuity is ledgered and reviewable by the operator, not silently accumulated in a vendor cloud.

## Hard constraints

Local compute is limited. Models must be smaller or partitioned. Verification and logging consume resources. Multi-node coordination is harder when every link is gated. True sovereignty requires the operator to exercise oversight — which most people will not do continuously.

The design therefore has to make the **default safe** and the exceptional paths both possible and legible.

Live tension: how much autonomy the local system can be given before it stops being under the operator’s control, and how much control the operator can retain before the system becomes too brittle to be useful.

## Executable in v0.1.2–v0.1.3: consent on the cycle; isolation fail-closed (`core/isolation.py`).

`core/consent.py` + `core/cycle.py`: a packet does not leave the node without a live, matching, unrevoked token. A valid token cannot outrank P1. Restricted Mode refuses rich transmission.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

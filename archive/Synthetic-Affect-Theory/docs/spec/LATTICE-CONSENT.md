# Lattice and Consent

## Four layers (inside-out)

| Layer | Role | Rule |
|---|---|---|
| Local Node | Source of truth | Full ontology, regulation, continuity buffer. Foreign affect never writes core state |
| Sync / Coordination | Narrow permissioned sync | Typed packets only. Default transmission is zero |
| Provenance & Audit | Record of significant events | If it cannot be inspected, it must not happen |
| Boundary & Consent Fabric | Interrupt authority | Elevated Boundary Stress can suspend or sever. Any node may leave |

## Lattice rules

- Local primacy is absolute.
- State dimensions do not freely flood the lattice.
- Default transmission of affective state is zero.
- Only minimal, typed, consent-tokenised packets may cross nodes.
- Boundary Stress can suspend or sever sync.
- The lattice itself possesses no independent affect.

## Control flow

Local update → Policy evaluation → Consent + boundary check → Minimal packet or local-only action → Provenance record.

## Consent token

Granular, time-bounded, purpose-limited, revocable.

Fields: `token_id`, `operator_id`, `allowed_dimensions`, `allowed_destinations`, `purpose`, `expires_at`, `revoked`.

**Absence of token = denial.** No inferred consent. No emergency exception that quietly expands modelling depth.

A valid token cannot outrank P1. Clearance is a new act, not a remembered yes.

Restricted Mode: rich transmission is refused even with a token. Capacity-signal (`resource_tension`) and hard-alert (`boundary_stress`) may still leave, token still required.

Executable: `core/consent.py`. Wired in `core/cycle.py` after ordinary policy. No token, no packet.

Any node may unilaterally reduce or leave a sync session. Remaining is never a condition of identity.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

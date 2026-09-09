# Isolation — dead or untrusted network

CrystalCore × Synthetic Affect Theory™️ · v0.1.3

When the link is gone or untrusted the node **fails closed**, not open. Core loops keep running locally. Nothing phones home. Cloud is optional; it is never required for affect regulation, consent, identity continuity, or safety invariants.

Restricted Mode is a policy posture. Isolation is a physical or trust fact. Isolation implies Restricted Mode. Restricted Mode does not imply the wire is dead.

## Failure modes

| ID | What failed | Immediate action | Local core |
|---|---|---|---|
| FM-ISO-LINK | Mesh / WAN down | Deny **all** packets, including capacity and hard-alert. Enter Restricted Mode | Continues |
| FM-ISO-UNTRUSTED | Link up but untrusted | Deny all packets. Do not use the pipe. Restricted Mode | Continues |
| FM-ISO-FAIL-OPEN | Action requires cloud to keep core function | Block the action. Do not skip local gates or policy | Continues |
| FM-ISO-PHONE-HOME | Silent callback, vendor log, or remote policy pull | Block. Incident. No packet | Continues |

## Rules

1. Local-first loops do not wait on the network.
2. A dead network is not an emergency exception for consent or DUR.
3. Tokens do not create a pipe that does not exist.
4. Capacity-signal and hard-alert may leave under Restricted Mode **only if a trusted link exists**. Under FM-ISO-LINK they stay home.
5. Unilateral session exit remains available (there is no session left to stay in).
6. Incoming packets on an untrusted or dead path are rejected. Foreign state never writes `LocalAffectState`.
7. Return of the link does not auto-flush buffers or auto-send. Operator / existing consent still required.

## Cycle order

Gates → isolation (phone-home / fail-open) → P1–P10 → isolation (packets) → consent.

Executable: `core/isolation.py`, wired in `core/cycle.py`.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

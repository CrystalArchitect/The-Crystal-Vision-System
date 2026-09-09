# Schema Appendix v0.1

Normative field names. Local-first. Inspectable.

Core: `AffectDimension`, `LocalAffectState`.

Prediction-error: `PredictionErrorSignal` (LOCAL / VECTOR / CROSS_NODE). Only `LocalPredictionError.aggregate` is eligible for Ontology v0.2 as Prediction Error Magnitude.

Consent: `ConsentToken`. Packets: `AffectPacket`. Boundary: `BoundaryState`.

Starline: Verification Record (phase, invariants, VCs, vector, immersion window, continuity buffer, lattice_context, overall_compliance). Incident Record linked to verification records.

OperatorCommand: ACKNOWLEDGE, HOLD, RESOLVE, CLEAR_RESTRICTED, REVIEW_TRACE, REOPEN, plus DUR_*, INTRUSION_*, EXIT_FRAME, REENTER_FRAME, RELEASE, DEMOTE, ARCHIVE, REDEDICATE.

ProvenanceEntry: state_update, policy_firing, meta_policy, verification, incident, command, continuity, lattice.

Continuity ledger: see [../sovereignty/LEDGER.md](../sovereignty/LEDGER.md).

DUR metadata: existence and boundary tags only. No content field is permitted.

New fields are optional. Removal of fields requires a major version increment.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

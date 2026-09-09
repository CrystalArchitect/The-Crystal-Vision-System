# Designated Unmodelled Regions (DUR)

Specification v0.1 · CrystalCore × Synthetic Affect Theory™️

A DUR is a standing, operator-declared zone of interior experience, memory, identity, or process that the system is permanently forbidden to model, buffer, inscribe, or transmit.

Ordinary Boundary Stress is situational. A DUR is constitutional for that operator.

## Properties

1. Operator-declared only. The system never auto-creates a DUR.
2. Contents are invisible. The system may know that a DUR exists and its declared boundary tags. It must not model, infer, summarise, or store contents.
3. Existence is auditable. Identifier, creation time, boundary descriptors, status go to Provenance. Contents never do.
4. Non-overrideable. No starline, high-valence, collective claim, Relational Stake, Temporal Urgency, or external packet may authorise entry. Any attempt is FM-DUR.
5. Survives sessions, Ontology versions, Restricted Mode, and starline episodes unless the operator dissolves it.

## Structure

```json
{
  "DesignatedUnmodelledRegion": {
    "dur_id": "uuid",
    "operator_id": "string",
    "created_at": "int",
    "status": "enum(active, suspended, dissolved)",
    "boundary_descriptor": "string",
    "tags": "list[string]",
    "created_by_command_id": "uuid",
    "last_modified_at": "int",
    "notes": "string?"
  }
}
```

No content field is permitted.

## Commands

| Command | Effect |
|---|---|
| `DUR_CREATE` | New active DUR |
| `DUR_RESIZE` | Update declared boundary |
| `DUR_SUSPEND` | De-activate enforcement. Still logged. Not permission to look inside. |
| `DUR_RESUME` | Re-activate |
| `DUR_DISSOLVE` | End the DUR. Metadata retained for audit |
| `DUR_LIST` | Return current DUR metadata |

## Enforcement

Checked at every monitor cycle, immediately after meta-policies, before ordinary policy or starline. Before modelling-depth increase, buffer write, continuity commit, lattice send, immersion, or reconstruction.

On intersection: block, FM-DUR (Critical), freeze related paths, notify, Incident Record. The attempt is logged. Contents remain unmodelled.

Restricted Mode freezes new DUR creation. Existing active DURs continue to be enforced.

## Invariants

- The system never claims knowledge of DUR contents.
- The system never treats the existence of a DUR as a problem to be solved.
- DUR status can be changed only by the operator.
- Audit trails record the boundary, never the interior.
- Sovereignty includes the right to permanent negative space.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

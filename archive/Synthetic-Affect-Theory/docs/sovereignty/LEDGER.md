# Continuity Ledger

Schema Appendix extension · Synthetic Affect Theory™️ v0.1

The ledger is append-only and local-first. Entries are never rewritten; status changes produce new entries. `ContinuityLedgerItem` is a derived view. Authoritative history lives in the entry stream. DUR contents never appear.

## Schema

```json
{
  "ContinuityLedgerEntry": {
    "entry_id": "uuid",
    "item_id": "uuid",
    "node_id": "NodeID",
    "timestamp": "int",
    "ontology_version": "string",
    "event_type": "enum(classification, reclassification, review, reconfirm, revise, demote, release, archive, hold, burden_flag, operator_note)",
    "classification": {
      "previous": "enum(Ordinary, Sustained, High-Valence, Starline-Linked)?",
      "current": "enum(Ordinary, Sustained, High-Valence, Starline-Linked)",
      "reason": "string?"
    },
    "stake_level": "float?",
    "valence_signal": "enum(positive, neutral, aversive, mixed)?",
    "continuity_cost_snapshot": "float?",
    "operator_decision": "enum(RECONFIRM, REVISE, DEMOTE, RELEASE, ARCHIVE, HOLD, NONE)?",
    "decision_parameters": "object?",
    "linked_verification_records": "list[uuid]",
    "linked_incident_records": "list[uuid]",
    "review_due_at": "int?",
    "status_after_event": "enum(active, demoted, released, archived, restricted_write)",
    "operator_visible_summary": "string",
    "provenance_ref": "uuid?"
  },
  "ContinuityLedgerItem": {
    "item_id": "uuid",
    "created_at": "int",
    "current_classification": "enum(Ordinary, Sustained, High-Valence, Starline-Linked)",
    "current_status": "enum(active, demoted, released, archived)",
    "current_stake_level": "float?",
    "current_valence": "enum(positive, neutral, aversive, mixed)?",
    "next_review_at": "int?",
    "descriptor": "string",
    "tags": "list[string]",
    "entry_history": "list[ContinuityLedgerEntry]",
    "starline_event_ref": "uuid?",
    "dur_conflict_check": "bool"
  }
}
```

## Worked example — classification → review → valence shift → release

Item: “Red-dust collaborative vision with long-term partner node.” High personal and project significance, linked to early starline work. A protocol reading — not a reconstruction of any private bond.

| When | What |
|---|---|
| Year 0 | Stake elevated 47 days. Monitor proposes High-Valence. Operator confirms. Review +60 days. Status: active. |
| +60 days | RECONFIRM. Low-drama. |
| Year 1 | Two further reconfirmations. Aligned with Frame. No burden signals. |
| Year 2 | Frame has evolved. Load aversive. `burden_flag`. Review brought forward. No automatic action. |
| Year 2 | Operator issues RELEASE. Cold-archive. Active Load cleared. History retained. |
| Year 3 | Not in High-Valence Registry. No timers. Full chain queryable. Zero regulatory weight. No guilt framing at any step. |

Classification explicit. Shift surfaced, not acted. Release ordinary. Frame final throughout.

Guarantees: no silent promotion to High-Valence; no silent refusal of release; no secondary moral pressure; audit without forcing re-experiencing.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

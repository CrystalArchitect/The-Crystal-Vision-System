# Version/Migration Key — Convergence Lens Archive Durability

**Status**: LOCKED  
**Version**: 0.1.0  
**Date**: 2026-07-27

## Purpose

Establish the versioning contract for Convergence Lens, the immutability guarantee for Chronicle archive entries, and the backwards-compatibility boundary. Ensures that once a claim is recorded, its meaning cannot be rewritten; and that old claims remain readable as new code evolves.

---

## Archive Immutability Contract

### Guarantee

**Chronicle entries are append-only and never deleted.**

Once a claim is admitted to CHRONICLE:
- Its content cannot be modified
- Its timestamp cannot be changed
- Its provenance record cannot be altered
- It cannot be erased from the archive

New claims may be marked "superseded" (a new claim with a different assessment), but the original remains.

### Implementation

- Chronicle storage is write-once
- Deletes are rejected at the API layer (fail-closed)
- Archive backups are immutable snapshots
- Retention: permanent (never purged)

### Exception: Only Governance Can Authorize Breaking Changes

If a future CONSTITUTION amendment requires reinterpreting existing claims (extremely rare):
1. Governance council votes to amend the Constitution
2. Amendment is recorded as a new CHRONICLE entry
3. Amendment applies only to new claims going forward
4. Old claims retain their original interpretation under the old rules
5. Dual-interpretation tooling is provided (read claims under old or new rules)

This ensures that even constitutional change does not rewrite history.

---

## Schema Versioning Strategy

### Current Schema

**Ingress Claim Format**: `obs-claim/1.0`
```json
{
  "statement": "string (1-500 chars)",
  "source": {
    "origin": "clementine|api|human|archive",
    "identifier": "string",
    "timestamp": "ISO8601 UTC"
  },
  "evidence_tier": "simulation|historical|live",
  "quality_gate": "high|medium|low"
}
```

**Chronicle Entry Format**: `chronicle-entry/1.0`
```python
{
  "timestamp": "ISO8601 UTC",
  "claim": "string",
  "statement_type": "observation|evidence|interpretation|vision",
  "status": "measurement|hypothesis|proposed|unknown",
  "confidence": "high|medium|low|unknown",
  "evidence_state": "none|developing|established",
  "latencies": dict,  # gap inventory
  "uncertainties": list,
  "future_review": bool,
  "review_trigger": str | null
}
```

### Forward Compatibility

New claims may use `schema_version` (e.g., `obs-claim/2.0`) if future evolution becomes necessary.

**Rule**: A reader supporting `obs-claim/1.0` is never required to understand `obs-claim/2.0`, but:
1. Unknown schema versions are rejected at ingress (fail-closed)
2. A migration pathway must exist before new versions are deployed
3. Governance must approve all new schema versions

### Backwards Compatibility

Code released in v0.1.0 must read claims from `obs-claim/1.0` forever.

If a breaking change (e.g., new required field) becomes necessary:
1. A shim layer is written to translate old claims to new schema without changing their meaning
2. The translation is recorded in a new CHRONICLE entry (transparent audit)
3. All old claims are re-admitted under the new schema with a link to the translation record
4. No data loss; no rewriting of originals

---

## Release Tagging Convention

### Code Versioning

Semantic versioning for the implementation:
- `v0.1.0`: Initial Convergence Lens release (observation-only surfaces, five governance keys)
- `v0.2.0`: Example — Clementine integration (new features, no breaking changes to existing APIs)
- `v1.0.0`: Only when Constitution and Archive contracts are frozen (all layers mature)

All releases are tagged in git as `v{major}.{minor}.{patch}`.

### Chronicle Dating

Chronicle entries are dated by their admission timestamp, not by code version:
- `2026-07-27T09:45:33Z`: A claim about the state of the world on this date
- Not versioned; immutable by definition
- Readable by any version of code that can parse its schema

### Release Notes

Every release includes:
1. Code changes (git diff summary)
2. Schema changes (if any)
3. Backwards compatibility statement
4. Archive compatibility statement (which old claims are readable)

---

## Durability & Replication

### Storage Requirements

Chronicle archive must be:
- **Replicated**: Minimum 3 zones (geographic or logical separation)
- **Immutable**: Write-once, no deletion
- **Audited**: Every read logged with identity + timestamp
- **Backed up**: Daily snapshots, 7-year retention (or governance decision)

Failure Boundary Key gates all write operations; if replication fails, the system halts rather than losing data.

### Geographic Durability (Optional; Sovereignty Requirement)

If data residency is a constraint (AU-based operations):
- Primary: Australia (zone A)
- Secondary: Australia (zone B)
- Tertiary: Optional (Australia or neutral jurisdiction)

This is a governance choice, not a technical requirement. Default is cloud-native distribution.

---

## Migration Procedures

### Scenario A: New Field Added to Chronicle Entry (Non-breaking)

1. Deploy code that reads the new field if present, ignores if absent
2. New claims include the new field
3. Old claims remain unchanged (no modification)
4. No migration; both old and new coexist

### Scenario B: Required Field Becomes Part of the Spec (Breaking)

1. Write migration code to derive the field for old claims
2. Create a new CHRONICLE entry: `migration_v1_to_v2_complete`
3. Re-admit all old claims with the new field populated
4. New code requires the field; old claims all have it now
5. No data loss; audit trail is clear

### Scenario C: Constitution Amendment Changes Interpretation Rules (Rare)

1. Governance votes and records amendment in CHRONICLE
2. Amendment specifies the new rule and effective date
3. Claims before the effective date are read under old rules
4. Claims after use new rules
5. Dual-interpretation reader is provided (user can choose which lens)

---

## Success Criteria

Version/Migration Key is locked when:
- ✓ Archive immutability contract is documented and enforced
- ✓ Schema versioning strategy is clear and forward-compatible
- ✓ Backwards compatibility is guaranteed (old claims always readable)
- ✓ Release tagging convention is established (semver for code, dates for claims)
- ✓ Migration procedures are documented for all scenarios
- ✓ Durability and replication requirements are specified
- ✓ No claim is ever silently lost or rewritten; all changes are audited

---

## Governance Implications

This key represents a permanent commitment:

1. **Immutability is not optional**: Once locked, this contract cannot be softened. No future version can delete old claims.

2. **Breaking changes require consensus**: Any schema change that would invalidate old claims requires full governance review.

3. **Audit trails are sacred**: Every read, write, and migration is logged. The chronicle is the permanent record.

4. **Code evolves; data persists**: New versions of Convergence Lens must remain compatible with v0.1.0 claims forever (or provide a shim).

This is the spine of the archive's integrity: the code can be rewritten, but the record cannot.

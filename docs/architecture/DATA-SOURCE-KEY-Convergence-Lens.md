# Data Source Key — Convergence Lens Ingress Contract

**Status**: LOCKED  
**Version**: 0.1.0  
**Date**: 2026-07-27

## Purpose

Define what claims Convergence Lens accepts from external sources (Clementine, APIs, humans), how they are validated before ingestion, and how provenance is preserved. Prevents invalid or unclaimed observations from entering MIRROR/CHRONICLE registers.

---

## Input Contracts

### Claim Structure (Required)

```json
{
  "statement": "string (1-500 chars)",
  "source": {
    "origin": "clementine|api|human|archive",
    "identifier": "string (source-specific ID)",
    "timestamp": "ISO8601 UTC"
  },
  "evidence_tier": "simulation|historical|live",
  "quality_gate": "high|medium|low"
}
```

### Validation Gate (Must Pass All)

1. **Statement non-empty**: `len(statement) > 0` and `len(statement) <= 500`
2. **Source traceable**: `origin` in `{clementine, api, human, archive}`; `identifier` unique within that origin
3. **Timestamp valid**: ISO8601 UTC, not more than 24 hours in future
4. **Evidence tier specified**: one of `{simulation, historical, live}`
5. **Quality gate present**: one of `{high, medium, low}`

### Rejection Rules

Claim is **REJECTED** if:
- Statement is empty, exceeds 500 chars, or contains only whitespace
- Source is missing or `origin` not in allowed set
- Timestamp is invalid, unparseable, or >24h in future
- Evidence tier is missing or unknown
- Quality gate is missing or unknown
- Duplicate `identifier` from same source within last 24h (prevents replay)

---

## Evidence Tier Semantics

| Tier | Definition | Stored as | Review Cadence | Expires |
|------|-----------|-----------|---|---|
| **simulation** | Hypothetical scenario, not measured | `evidence_state: none` | ad-hoc (governance only) | never |
| **historical** | Measured in past (>30d ago), context matters | `evidence_state: developing` | yearly | never |
| **live** | Measured recently (<30d), actionable signal | `evidence_state: established` | weekly | 90d (archive then) |

---

## Quality Gate Mapping

- **high**: Source has >90% accuracy history; claim cites specific evidence or measurement; used in governance decisions
- **medium**: Source has 70-90% accuracy history; claim is reasonable inference; used for planning
- **low**: Source is new (<10 claims) OR claim is speculative; marked clearly as uncertain; used only for exploration

Quality is assigned by ingestion point, not automatically derived.

---

## Provenance Requirements

Every admitted claim must retain:

```python
{
  "source_origin": str,        # "clementine", "api", "human", "archive"
  "source_id": str,             # Unique within origin
  "submitted_at": ISO8601,      # When ingested
  "evidence_tier": str,         # simulation | historical | live
  "quality_gate": str,          # high | medium | low
  "submitter_role": str,        # "contributor" | "governance" | "system"
  "can_modify": bool,           # True only if submitter role ≥ contributor
}
```

**Invariant**: Once in Chronicle, provenance cannot change. Claims can be marked superseded (new claim added), but originals remain immutable.

---

## Source Reliability Tracking

Each source tracks:
- **Total claims submitted**: N
- **Claims admitted**: N_admitted (passed validation gate)
- **Admission rate**: N_admitted / N
- **High-quality rate**: (claims marked "high") / N_admitted
- **Contradiction count**: Claims that contradict prior admitted claims from same source

Sources with admission rate <30% are flagged as "unreliable". Governance views this flag but does not auto-reject; human decision required.

---

## Clementine-Specific Rules

Clementine claims must:
1. Include exact `evidence_tier` (simulation/historical/live) — no auto-detection
2. Include measurement timestamp or explicit "no direct measurement"
3. If `live`, must be measurable/falsifiable within 90 days
4. If `simulation`, must state the scenario clearly in statement

Clementine claims admitted at quality_gate ≥ "medium" proceed to MIRROR decomposition; lower-quality claims are queued for governance review before ingestion.

---

## Ingress Sequence

```
External Claim → Validation Gate → Quality Assignment → Provenance Record → MIRROR Decomposition → CHRONICLE Entry
                  (reject if fails)                      (becomes immutable)    (extract type/gaps)  (timestamped)
```

If validation gate fails: claim is logged (with reason) in source's rejection_log but NOT admitted.

If quality gate is below "medium" and source is Clementine: governance must approve before MIRROR decomposition.

---

## Safety Invariants

1. **No claim loses provenance** — If a claim is in CHRONICLE, its source is in the record forever
2. **No source can edit history** — Admitted claims cannot be deleted or modified; only superseded
3. **No tier downgrade** — A claim cannot move from "live" to "historical" or "simulation"
4. **No quality inflation** — Quality gate cannot increase after ingestion
5. **Contradiction is preservable** — Incompatible claims from different sources can coexist if both passed validation

---

## Success Criteria

Data Source Key is locked when:
- ✓ Clementine can submit claims and have them validated correctly
- ✓ Rejected claims are logged with reason but not admitted
- ✓ Provenance is attached to every admitted claim
- ✓ Simulation vs live claims are distinguished in Chronicle storage
- ✓ Governance can audit source reliability and override quality gate if needed

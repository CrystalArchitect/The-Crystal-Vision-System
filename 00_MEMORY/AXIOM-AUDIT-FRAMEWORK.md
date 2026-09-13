# Axiom Audit Framework (2026-09-13)

This document maps the five philosophical axioms (Drawer 19) to specific governance constraints and provides an audit checklist for SWARM mechanisms (Drawer 16) and GTB policies (Drawer 20).

---

## Axiom 1: Origin — Where do systems emerge?

**Principle:** Multi-agent systems must have identifiable, transparent foundations. Governance rules are not imposed externally; they emerge from agent interaction within documented constraints.

### Mapping to Governance Constraints

| Constraint | SWARM Mechanism | GTB Policy | Audit Question |
|-----------|-----------------|-----------|-----------------|
| **Design rationale documented** | Circuit-breaker, tax, staking, audit, collusion-detection, reputation-decay | Planner type, objective weights, tax schedules | Does code/config include written rationale for *why* this parameter exists? |
| **Initial conditions transparent** | Event log startup, seed documentation | Scenario YAML, initial budget distribution | Are starting states identical across runs, or seeded deterministically? |
| **Rule genesis traceable** | Git commit history, bead tracking | PR description, issue linkage | Can we trace each governance rule to a research decision? |
| **Agent-level agency** | Agents can observe rules; rules apply equally | All agents see same tax schedule, audit probability | Do rules apply uniformly, or do some agents have exceptions? |

### Audit Results

**SWARM Status:** ✓ Excellent. Event logs are append-only and traceable. Git history documents each mechanism. **Concern:** Some reputation-decay thresholds lack written rationale — check `swarm/core/payoff.py` for undocumented parameter choices.

**GTB Status:** ✓ Good. Scenario files document initial conditions; FINDINGS.md provides rationale for swept parameters. **Concern:** Tax schedule brackets are tuned empirically; the rationale "welfare maximization at ineq_weight=0.5" is not documented in code.

### Action Items

- [ ] Add docstring to `swarm/core/payoff.py` explaining each reputation parameter
- [ ] Add `# Rationale:` comment block to GTB tax-schedule brackets explaining why those thresholds
- [ ] File ISS-TBD: "Undocumented governance parameter choices" if not already tracked

---

## Axiom 2: Belonging — Identity and distribution of agents

**Principle:** Agents have durable, publicly observable identities. Governance mechanisms cannot arbitrarily exclude agents or distribute benefits unevenly without explicit rule.

### Mapping to Governance Constraints

| Constraint | SWARM Mechanism | GTB Policy | Audit Question |
|-----------|-----------------|-----------|-----------------|
| **Identity is stable** | Agent `id` field immutable per session | Worker ID persistent across epochs | Can an agent's identity change mid-run? |
| **Identity is observable** | Event log includes agent_id in every record | Polymarket envelope includes agent_id | Can the public see which agent took which action? |
| **Exclusion is rule-based** | Freeze-on-repeat, reputation thresholds explicit | Audit-catch → fine, repeat → freeze | Are agent exclusions triggered by breach of documented rule, or discretionary? |
| **Distribution is transparent** | Payoffs logged per-agent per-epoch | Income, tax, redistribution logged | Can we reconstruct every agent's reward trajectory? |
| **No hidden coalitions** | Coalition detection looks for non-independent behavior | Bunching detection flags income coordination | Is there an audit against secret agreements? |

### Audit Results

**SWARM Status:** ⚠️ Partial. Event logs include agent_id; reputation thresholds are explicit. **Concern:** `reputation-decay` rate is not agent-visible (agents don't see their own reputation score mid-run), violating observability.

**GTB Status:** ✓ Good. Worker IDs are stable; income/tax/redistribution fully logged. **Concern:** Collusion detection (similarity_threshold=0.7) is a heuristic with no formal justification for the threshold value.

### Action Items

- [ ] Add `agent_reputation` field to SWARM event log so agents can see their own reputation each step
- [ ] Document justification for `collusion.similarity_threshold=0.7` (why 0.7? What does it mean operationally?)
- [ ] Run audit: check if any agent is ever frozen without a corresponding (audit_probability, fine_multiplier) rule application

---

## Axiom 3: Irreversibility — Paths cannot be unmade

**Principle:** Governance mechanisms must respect that consequences are permanent. Agents cannot undo audits, unfine evasion, or reverse reputational damage. This is a safety constraint: allowing reversal enables escape-route exploitation.

### Mapping to Governance Constraints

| Constraint | SWARM Mechanism | GTB Policy | Audit Question |
|-----------|-----------------|-----------|-----------------|
| **Audit findings are permanent** | Once logged, event cannot be deleted | Catch remains in history; no expungement | Can an agent petition to have an audit reversed? |
| **Fine is not refundable** | Fine deducted from payoff, stays deducted | Tax withheld; no rebate mechanism | Is there any condition under which a caught evasion is forgiven? |
| **Reputation loss persists** | Reputation never increases (only decays to 0) | No "forgiveness" of prior catches | Does reputation *ever* recover after reputation_penalty_per_catch? |
| **Freeze is inescapable** | freeze_after_n_catches → freeze_duration_epochs is applied | Repeat catch → 2-epoch freeze | Can an agent break a freeze by paying a fine or negotiating? |
| **Record is immutable** | Event logs are append-only JSONL | No deletion of historical records | Are event logs versioned or immutable-by-design? |

### Audit Results

**SWARM Status:** ✓ Excellent. Event logs are append-only. Reputation only decays; no recovery mechanism. **Concern:** `reputation-decay` parameter itself allows tuning how fast reputation falls; is there a lower bound check to ensure reputation ∈ [0, 1]?

**GTB Status:** ⚠️ Requires verification. Tax fines are permanent; freezes are temporary. **Specific question:** Does `freeze_duration_epochs=2` mean after 2 epochs the agent is unfrozen and can evade again? This violates irreversibility if the agent can repeat evasion indefinitely.

### Action Items

- [ ] Verify SWARM reputation ∈ [0, 1] is enforced in `ProxyComputer.sigmoid()` and `payoff.py` 
- [ ] Run GTB experiment: measure whether agents caught for evasion, frozen for 2 epochs, then released, attempt evasion again at same rate as before. If yes, freeze is not an irreversible consequence — it's a temporary penalty.
- [ ] **If GTB freeze is temporary:** Document whether this violates the irreversibility axiom, or whether temporary freezes are acceptable as long as a *record* of the catch is permanent.

---

## Axiom 4: Emergence — Properties at system level

**Principle:** Governance effectiveness depends on population composition and cannot be reduced to individual agent behavior. Consequences of governance appear at collective scale, not individually.

### Mapping to Governance Constraints

| Constraint | SWARM Mechanism | GTB Policy | Audit Question |
|-----------|-----------------|-----------|-----------------|
| **Governance scales with diversity** | Toxicity metric depends on population mix of agents | Welfare cost depends on fraction of evasive workers | Do we measure governance *per-agent* or *system-wide*? |
| **Effectiveness cannot be individual** | Reputation gates depend on peer distribution | Tax revenue depends on total income, not per-agent | Is governance success measured individually or collectively? |
| **Composition-dependent outcomes** | Same governance at ρ=0.3 may fail with 80% adversarial agents but succeed with 20% | Same audit_probability has different impact with different evasion_rates | Have we tested governance across agent-type compositions? |
| **No individual-level guarantees** | Governance does not promise "each agent gets X"; only "system achieves Y" | Tax does not guarantee individual welfare; only gini coefficient | Are payoff formulas stated system-level or per-agent? |

### Audit Results

**SWARM Status:** ✓ Good. Metrics are population-level (toxicity, quality_gap, welfare). Governance cost varies with adversary fraction. **Concern:** Are we reporting governance success "at ρ=0.5 with 20% adversarial" or just "at ρ=0.5"? The composition should be explicit.

**GTB Status:** ✓ Good. Welfare/Gini/tax-revenue are system-level. Sweeps vary `audit_probability` and seed → naturally vary composition. **Concern:** Are we distinguishing "welfare cost of audit" from "welfare cost under this particular agent population"?

### Action Items

- [ ] Audit SWARM publications: every governance result should include agent-composition as a factor. Add to methods: "Tested with N% adversarial agents of type T."
- [ ] Audit GTB FINDINGS.md: every welfare claim should note "sample population: 14 workers, X% evasive tendency." Separate "audit reduces welfare" from "audit reduces welfare with evasive workers."
- [ ] Run cross-composition test: take best-performing governance (e.g., ρ=0.5, audit_prob=0.2) and test on 4 different agent-composition profiles (all benign, 25% evasive, 50% evasive, all adversarial). Report governance success at each composition.

---

## Axiom 5: Subjectivity — Experience is foundational

**Principle:** Agents have preferences, constraints, and subjective values. Governance cannot violate agent autonomy by suppressing legitimate preferences or forcing outcomes that contradict agent values.

### Mapping to Governance Constraints

| Constraint | SWARM Mechanism | GTB Policy | Audit Question |
|-----------|-----------------|-----------|-----------------|
| **Agent preferences are visible** | Agents express preferences through payoff; governance respects pref-satisfaction metrics | Workers have explicit income targets; governance affects ability to meet them | Can we observe what each agent *wants* to achieve? |
| **Governance does not eliminate choices** | Agents can still choose to accept/reject, cooperate/defect, etc. | Workers can choose to evade, trade, build, etc. | Does governance remove options, or only change their payoffs? |
| **Legitimate interests protected** | Quality gap (adverse selection) indicates when governance favors low-quality agents | Gini coefficient indicates redistribution is not crushing high performers | Is governance neutral to diverse agent types, or biased against some? |
| **Suppression is visible & justified** | Reputation penalties are logged with rationale | Freeze reason is documented (audit-catch, repeat-offender, etc.) | When governance suppresses an agent's action, is the reason logged? |
| **Autonomy is respected** | Agents can observe rules and adjust behavior accordingly | Tax schedule is public; agents can optimize income subject to it | Do agents have *information* necessary to make informed choices under governance? |

### Audit Results

**SWARM Status:** ⚠️ Partial. Agents can observe reputation thresholds and adjust behavior. **Concern:** Do agents know their own reputation score in real-time? If not, they cannot make informed decisions about risk.

**GTB Status:** ✓ Good. Tax schedule is public. Workers can optimize income by varying effort/trade/build mix. **Concern:** Does the LLM worker know it's being audited? If audit is hidden, workers cannot respect the constraint of "I might be audited," so they cannot adjust risk tolerance rationally.

### Action Items

- [ ] Run SWARM transparency test: run scenario with `agent_reputation_visible=true` vs. `false`. Measure whether agents that can see their reputation adopt different (more careful) policies than those that cannot.
- [ ] GTB: verify workers know audit_probability. If using LLM workers, check if system prompt includes "you might be audited at probability P" clause.
- [ ] Audit: document for each agent type whether it has access to the full rules it operates under. If not, note as a subjectivity violation.

---

## Audit Checklist (Quick Summary)

### SWARM (Drawer 16)

- [ ] Axiom 1: Reputation parameter rationale documented in code
- [ ] Axiom 2: Agent reputation scores visible in event log
- [ ] Axiom 3: Event logs are append-only; reputation ≥ 0 enforced
- [ ] Axiom 4: Governance results include agent-composition as explicit factor
- [ ] Axiom 5: Agents can observe reputation thresholds and adjust behavior

### GTB (Drawer 20)

- [ ] Axiom 1: Tax schedule bracket rationale documented in code comments
- [ ] Axiom 2: Collusion similarity_threshold value justified; worker IDs persistent
- [ ] Axiom 3: Verify whether temporary freeze violates irreversibility (run repeat-evasion experiment)
- [ ] Axiom 4: Every welfare claim in FINDINGS.md specifies agent composition
- [ ] Axiom 5: Workers know audit_probability; can make informed evasion decisions

---

## Next Steps

1. **High priority:** Run Axiom 3 audit on GTB freeze mechanism. If agents can repeat evasion after freeze expires, file issue against irreversibility.
2. **High priority:** Add `agent_reputation_visible=true` option to SWARM and measure behavior change (Axiom 2).
3. **Medium priority:** Document all governance parameter rationales (Axiom 1).
4. **Medium priority:** Run cross-composition governance test (Axiom 4).
5. **Medium priority:** Verify worker access to audit_probability in LLM prompts (Axiom 5).

---

## File Structure for Audit

```
00_MEMORY/
  AXIOM-AUDIT-FRAMEWORK.md          ← this file
  axiom-audit-results/
    axiom-1-origin-audit.md          ← detailed findings
    axiom-2-belonging-audit.md
    axiom-3-irreversibility-audit.md  ← highest priority
    axiom-4-emergence-audit.md
    axiom-5-subjectivity-audit.md
```

---

<!-- topics: axiom-grounding, governance-audit, philosophy-to-implementation, irreversibility, subjectivity -->

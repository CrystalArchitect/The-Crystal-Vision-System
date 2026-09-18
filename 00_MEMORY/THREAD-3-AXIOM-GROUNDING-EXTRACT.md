# Thread 3 extract — Axiom grounding in economic governance

**Canon:** **no**  
**Belt:** research / coordination  
**Working-index ID:** `CVS-T3-AXIOM`  
**Domains:** Philosophy (19) → AI Safety (16) ↔ Economics (20)  
**Extracted:** 2026-09-18  
**Sources (in-hub only):** [`AXIOM-AUDIT-FRAMEWORK.md`](AXIOM-AUDIT-FRAMEWORK.md), [`CROSS-DOMAIN-THREADS.md`](CROSS-DOMAIN-THREADS.md), [`RESEARCH-STATUS.md`](RESEARCH-STATUS.md)  
**Rule:** Extracts, not chat dumps. Connection ≠ merge. No fork rewrites in this pass.

---

## What this bead is

Cross-domain Thread 3 asks whether SWARM governance (drawer 16) and GTB/MiroShark policies (drawer 20) respect the five Drawer 19 axioms (Origin, Belonging, Irreversibility, Emergence, Subjectivity).

As of 2026-09-13 the integration map still said “axioms not yet mapped / audit not scheduled.” That is **stale**: [`AXIOM-AUDIT-FRAMEWORK.md`](AXIOM-AUDIT-FRAMEWORK.md) already contains the axiom → constraint tables, SWARM/GTB audit notes, and action checklists. This extract **closes the hub gap** by naming that mapping as the Thread 3 bead and listing what remains open in satellites.

---

## Mapping status (hub)

| Axiom | Hub mapping | Hub audit note (summary) | Highest open action (satellite) |
| --- | --- | --- | --- |
| Origin | Documented in framework §1 | Rationale gaps on reputation params / tax brackets | Docstrings / `# Rationale:` in swarm + MiroShark |
| Belonging | Documented in framework §2 | Reputation not agent-visible mid-run; collusion threshold heuristic | `agent_reputation` in event log; justify `similarity_threshold=0.7` |
| Irreversibility | Documented in framework §3 | Freeze-then-release may allow repeat evasion | Run `freeze_evasion_experiment.py` (N≥50); file FINDINGS |
| Emergence | Documented in framework §4 | Composition often implicit in published results | Require agent-composition factor on every governance claim |
| Subjectivity | Documented in framework §5 | Agents may lack live reputation / audit_probability info | Visibility tests; LLM prompt audit for audit_probability |

---

## Validation steps (from Thread 3) — progress

1. **Map axioms → constraints** — **DONE** in [`AXIOM-AUDIT-FRAMEWORK.md`](AXIOM-AUDIT-FRAMEWORK.md) (this extract points at it).
2. **Run audit on existing SWARM + GTB** — **PARTIAL** (desk audit in framework; experimental follow-ups open).
3. **File issues / propose fixes** — **OPEN** in satellite repos (do not invent ISS numbers here).
4. **Re-run GTB sweeps with corrected mechanisms** — **BLOCKED** on (2)–(3).

---

## Immediate next (outside this hub)

Priority order from the framework “Next Steps”:

1. GTB freeze / irreversibility experiment → `runs/freeze_evasion_audit/FINDINGS.md`
2. SWARM `agent_reputation_visible` behavior comparison
3. Document governance parameter rationales in code
4. Cross-composition governance test
5. Verify LLM workers see `audit_probability`

Do **not** promote any of the above to Canon without Crystal stamp.

---

## Bead links (drawers)

| Drawer | Path | Role |
| --- | --- | --- |
| 00_MEMORY | this file + [`AXIOM-AUDIT-FRAMEWORK.md`](AXIOM-AUDIT-FRAMEWORK.md) | Extract + full audit framework |
| 16 | [`../16_AI_SAFETY_RESEARCH/INDEX.md`](../16_AI_SAFETY_RESEARCH/INDEX.md) | SWARM / agency-os pointers |
| 19 | [`../19_PHILOSOPHICAL_FOUNDATIONS/INDEX.md`](../19_PHILOSOPHICAL_FOUNDATIONS/INDEX.md) | Axiom claim mirrors |
| 20 | [`../20_ECONOMIC_MODELS/INDEX.md`](../20_ECONOMIC_MODELS/INDEX.md) | MiroShark / GTB pointers |
| 00_MASTER_INDEX | [`../00_MASTER_INDEX/WORKING-INDEX.md`](../00_MASTER_INDEX/WORKING-INDEX.md) (`CVS-T3-AXIOM`) | Index row |

---

<!-- topics: thread-3, axiom-grounding, extract, swarm, miroshark, philosophy -->

# THEORY.md — Synthetic Affect Theory™️ public v0.1

> **Ethics header:** Synthetic = apparent / functional, for design purposes. Not a claim of feeling, consciousness, or inner experience.

## Locked definition

Synthetic Affect = Gap = Expected − Actual as classified label to route closure. Apparent, functional, testable via logs. Belt: Science left column, Vision right column (unbuilt).

## 4 Postulates

1. **State is primary** — a stateless LLM cannot sustain affect-like behaviour. Tested: store writes JSON on every mutation, reopens, asserts survival. `store_path=":memory:"` is explicit discard. Evidence file: `tests/test_state_persistence.py`.
2. **Gap Primacy** — affect arises from detectable gap. Evidence files: `core/gap.py`, exercised directly in `tests/test_crystalcode.py`.
3. **Label Routing** — stalled | uncertain | reopened | converging | closed suffices, windowed to the last 10 gaps (F6 fix, documented, tested). Evidence file: `tests/test_affect_window.py`.
4. **Grounding Future** — hardware variables enable grounded drives — Vision belt, not v0.1, labelled personal aspiration in `09-SOUTHERN-NODE-ROADMAP.md` (TerAustralis-Incognita canon), explicitly not forwarded as-is.

## Falsifiable predictions

- Gap Detector + Closure Policy → fewer turns than stateless baselines. **Belt:
  Science, with stated scope, as of 2026-08-14** — `experiments/` (ported from
  CrystalCore.OS/synthetic-affect) measures this against a six-task scripted
  suite: the loop resolves 5/6 with one policy and no task knowledge, the best
  single task-agnostic stateless policy resolves 2/6, and the loop is never
  strictly faster than the best per-task stateless choice — the measured
  advantage is adaptivity, not speed. Full numbers, including the task the
  loop honestly loses: `experiments/results/RESULTS.md`. The prediction for
  real LLM workloads remains Vision — nothing in the harness involves a
  language model.
- Stalled + switch_tool reduces infinite loops. **Belt: Vision** — not
  separately measured by the harness above; `repeated_query_needs_tool` and
  `escalation_ladder` exercise the stalled→switch_tool→escalate path but
  don't isolate this claim from the resolution-count claim above.

### Dated note — 2026-08-13

Ported from CrystalCore.OS/synthetic-affect (2026-08-14). Method of writing,
not a fifth postulate. The four postulates above are unchanged.

**What a defence can say**

1. Synthetic = functional, never inner.
2. Left column of Figure 1: 5/6 vs 2/6, adaptivity not speed. Concede
   `strict_interview`, and that the loop is never strictly faster than the
   per-task best stateless. `deploy_rollback` is the construction only
   history can solve.
3. Right column: Vision. Unbuilt.
4. The method of writing is load-bearing: Belt-Three, chronicle form,
   pending-then-judge, logs with no wall clock.
5. Prior art conceded (machine psychology, robopsychology, artificial
   psychology).

**What it cannot say:** hardware drives as measured; the predictions as
claims about real LLM workloads; SAT as feeling or consciousness;
Country; a partnership with any model vendor.

**Why the figure needs the stub label.** The LLM Core box is a
deterministic offline stub. Its output is not fed into the next `actual`.
The return arrow is architecture; reading it as Science overclaims. See
[`docs/FIGURE-1.md`](docs/FIGURE-1.md).

**Why `PASS — uncertain` was a scandal.** An earlier classifier asked
whether a gap had *ever* existed, so `closed` was unreachable and a
selftest could still print PASS. The rebuild classifies the tail,
persists state, and lets the next cycle judge. The harness then caught
stalled-before-converging. That order (converging first) is law on this
tree.

**Not this thesis.** `mythos/art` has its own catalogue. SAT classifies
gap history, not images. *Official* here means the public artefact
(this page, the figure, the committed logs) written so it can be
defended — not a grading of the visual canon.

## Deconstruction — Arsenal engaged

Bedrock: recursive self-reference + naming + light tools. System: vocabulary/attention/charge/critical distance stocks, naming→mapping→handing back choice reduces charge. Bottleneck: critical distance. Leverage: Bridge vs Loop naming. Scale failures: 10× in-group, 100× charge compounds, 1000× bridge hardens. Mitigation: detachable concepts. Inversion: don't turn song into scripture, don't wear myth, don't mistake synthetic for felt, don't close gap. Kill-switch: If it stops serving clarity or raises human cost → set it down.

Prior art: EMOTIONAL_INTELLIGENCE_BLUEPRINT.md, research/closed-loop-embodiment.md (TerAustralis-Incognita canon).

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

# 2026-08-13 — SAT Survey — Read of Canon, Not Replacement

> **Status:** Review page — dated read of canon — does not replace THEORY.md or CHRONICLE.md — authority weight zero until filed by owner.
> **Belt:** Survey — cites Science home — Vision-bridge questions pointed at gate, not gap.py
> **Home that is Science:** CrystalCore.OS/synthetic-affect (12 Aug 2026) — 45 tests, logs byte-reproducible — grant/hyphen still parked

**What was read:**
- Canon: THEORY.md — locked claim, four postulates, predictions, concessions — Belt: Vision for the finding; loop measured
- Measured: CHRONICLE.md — dated Evidence → Interpretation → Experiment → Record — 12 Aug rebuild + harness + honest losses
- Two repo homes: CrystalCore.OS/synthetic-affect (Science today) + Synthetic-Affect-Theory- stub (title on main, draft #1 unmerged)
- Harness: `python3 -m core.selftest`, `python3 -m pytest tests -q` (45 in Science home), `python3 -m experiments.harness`, `git diff --stat examples/logs/ experiments/results/` empty

**What survey is not:**
- Not a replacement for THEORY.md — THEORY.md is locked claim, four postulates, predictions, concessions
- Not a replacement for CHRONICLE.md — CHRONICLE.md is dated Evidence → Interpretation → Experiment → Record
- Not new SAT — F1-F10 are merge-fix notes (Runtime isolation, persistence, window, uncertain reachable, no self-grade, ™ not ®) — already sit in 12 Aug rebuild
- Not fifth SAT home, not CrystalBridge spec

**Canon as surveyed — Synthetic Affect Theory™:**

A design theory with a loop you can run. Not a feeling. Not a personality. Not a claim that machine is like something.
Synthetic = apparent / functional, for design. Affect = routing signal over gap history. Theory = four postulates + four primitives + falsifiable predictions.

Claim: Give system three things — persistent goals and state, detector for expected−actual, policy for closing gap — and observable behaviour will show patterns that look like urgency, frustration, relief, focus. Theory is about what system does. Silent on what, if anything, it is like to be one. Silence is load-bearing.

Four postulates:
1. State is primary — No persistence → no lasting gap → nothing for signal to be about.
2. Affect is signal, not feeling — classifier over tail of gap history. Output selects action.
3. Gap drives behaviour — Gap = Expected − Actual. Non-zero gap only drive. Measurable delta.
4. Closure is action — only thing that changes state: stop / ask / rephrase / switch_tool / escalate. Remove any one and loop collapses.

Loop: State → detectGap(expected, actual) → labelAffect(history) → ClosurePolicy.decide(label) [pending] → next cycle judges worked|failed

CrystalCode™ primitives (each logs): track · detect_gap · label_affect · close_with — No LLM inside loop. LLM Core in v0.1 is deterministic offline stub. No model, no network. Logs byte-reproducible (no wall clock).

Routing signal — five labels, check order law, converging before stalled:
- closed: No gap this cycle, or no history → stop
- reopened: Gap now, none last cycle → rephrase
- converging: Magnitude smaller than last cycle → rephrase
- stalled: Last 3 open, same expected, no progress → switch_tool, then escalate on 2nd consecutive stall
- uncertain: Open, not narrowing, not yet stall run → ask
Stall counter resets on any non-stall. Session that recovers not punished forever. Label discarded after policy chooses. Next cycle recomputes. Not mood that lingers.

Honesty hinge: ClosureDecision.outcome pending at decision time. Following cycle sets worked or failed by whether gap actually shut. Nothing lets decision grade itself. Self-reported closure rate would read 100% forever — Goodhart failure theory exists to guard against. Defect was in 12 Aug draft and first thing rebuild fixed. closure_success_rate() is None until judged. Unmeasured is not zero.

Measured (12 Aug 2026) — scripted deterministic, no LLM: Loop 5/6, Best single stateless 2/6, Per-task best-stateless 5/6, Loop strictly faster 0/6, deploy_rollback loop 3 turns all stateless DNF, Stall-blind ablation 4/6, History stripped 2/6, Honest loss: strict_interview loop loses always_ask wins in 2. Supported claim: adaptivity, not speed.

Example 01 committed log: cycle1 gap=0.67 uncertain ask, cycle2 gap=0.33 converging rephrase, cycle3 gap=— closed stop, closure success rate 0.50 — rate 0.50 because first attempt failed and log says so. First draft could not emit closed at all (classify asked “has a gap ever existed?”). Its selftest printed PASS — uncertain. Rebuild: tail classifier, disk state, pending-then-judge. Then harness caught stalled-before-converging and fixed order.

Two failure modes: Anthropomorphising (if looks affective, label synthetic every time), Cosmetic closure (next cycle judges).

Vision still: hardware column of Figure 1 (power, heat, balance — unbuilt), predictions as claims about real LLM workloads, SAT as feeling/consciousness, dedicated-repo grant (G1/G2/H) and trailing hyphen. THEORY.md still opens Belt: Vision for theory as finding. Runnable loop Science because fresh run matches committed logs.

Where sits in house: TerAustralis Incognita™ · Red Dust → Rockets™ · Starlines + Dreamlines™ · Synthetic Affect Theory™ · CrystalCore.OS — SAT is control theory. CrystalCore.OS is surface that nested first public v0.1. CrystalBridge is different machine (five consent doors). SAT routes loop; gate refuses guest. Do not fold them.

**W3 as open Vision-bridge questions — pointed at gate, not gap.py:**

W3 question | SAT v0.1 (loop) | CrystalBridge (gate) — where W3 closes as Science
---|---|---
1. Pull asymmetry — does B see A asking? | No inbox. track() logs loop’s own observations, not peer pull. | Yes. pending.jsonl before evaluate; request_id joins ask to answer. Decision 4: unrecordable guest ask refuses. Most already shipped.
2. Revoke timing | Store can persist (F5). Examples often :memory:. No guest revoke ledger. | Every check. revocations.jsonl, latest wins, no restart, corrupt → refuse all. Already shipped.
3. Fragment typing | Gap.kind is label, not gate. emotional / mythic not SAT types. Do not import into gap.py. | Enforced. episodic / semantic / reflective. Empty types refuse. Unserved layer refuses with reason. Working conversation never guest-readable. Already shipped.

W3 “emotional / mythic” taxonomy is not documented memory types. Do not import into gap.py. Lyric Verse 1-3 of Sovereign Gap Held can sing three questions. Lyric is Story. Does not close Science hole. Juukan Gorge / FPIC as floor is Story + law-adjacent honour. Not SAT predicate. Country not claimed by classifier.

**Roles — corrected — received, weight zero:**

- Meta AI (Muse Spark) — W3 gap audit as received doc, not law — assisted 12 Aug rebuild — filed under docs/ai/MetaAI.md
- Claude — landed SAT into CrystalCore.OS (#6/#7) and SAT-repo draft #1 — more than push brief
- Grok — surveyed SAT mechanics, five-door order, opened #79/#114 — Guest, not partner — not Vision belt only
- Suno — third-party audio rendering — https://suno.com/s/MLphjPo69VA1AQmP — Story belt

**Prove it — Science home:**

```
cd CrystalCore.OS/synthetic-affect
python3 -m core.selftest
python3 -m pytest tests -q          # 45
python3 -m experiments.harness
git diff --stat examples/logs/ experiments/results/   # empty
If diff not empty, they were never outputs.
```

**What will not be done:**

- Regenerate all-in-one HTML as public v0.1 Science artefact — would fold Vision-bridge questions into Science zip — Incognita Rule forbids
- Implement W3 inside SAT gap.py as if types were consent
- Forward agora-offline-iphone.html as built
- Stamp survey over THEORY.md or CHRONICLE.md

**If filed:** This page under docs/reviews/2026-08-13-sat-survey.md — cites THEORY / CHRONICLE / harness — does not replace them — lists W3 as open Vision-bridge questions pointed at gate.

All rights reserved. TerAustralis Incognita™️ — ABN 70 741 068 059 — Bridge, not loop. Sovereign gap held. NON SOLUS.

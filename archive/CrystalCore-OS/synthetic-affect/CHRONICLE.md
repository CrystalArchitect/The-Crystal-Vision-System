# Chronicle — Synthetic Affect Theory™

Dated record, in the project's own form: **Evidence → Interpretation →
Experiment → Record.** Belt labels apply here as everywhere.

---

## 2026-08-12 — public v0.1

**Evidence.** A reference implementation of the loop was drafted with assistance
from Meta AI and delivered as a ~20-file package. It was read in full and run
before anything was changed. Measured on this machine:

- `python3 -m core.selftest` — passed, exit 0
- `python3 -m pytest tests -q` — 5 passed
- `examples/logs/*.jsonl` — 779 and 1536 bytes, byte-reproducible across reruns

Those three claims were made about the draft and all three held. The logs are
genuine outputs, not hand-authored.

**Interpretation.** What the logs *recorded*, however, was a broken classifier.
`AffectModel.classify` asked whether any gap had ever existed rather than whether
one exists now:

```python
gaps = [g for g in hist if g is not None]
if not gaps: return "closed"
```

So `closed` became unreachable the moment a first gap opened. Confirmed by
running it: `classify([gap, None])` → `uncertain`. Both example logs show a gap
being resolved and the system still reporting `uncertain` / `ask`. A theory whose
central act is closure had an implementation that could not express closure.

The draft's selftest passed anyway, because it asserted only that a gap was
present or absent and never checked the label. It printed `PASS — uncertain`.

Four further findings, all confirmed by reading or running:

- `PersistentStateStore` accepted a path, stored it, and never read or wrote it.
  Postulate 1 — *state is primary* — had no implementation at all.
- `ClosureDecision.outcome` was stamped at decision time (`"asked"`, `"closed"`).
  A closure-success-rate computed from that field reads 100% forever — the
  Goodhart failure this theory is supposed to guard against, present in the
  guard itself.
- `crystalcode` bound its primitives to module-level globals, so a second `Loop`
  in one process would silently hijack the first one's store and logger.
- `docs/figure-1.svg` placed two boxes below a 400-unit `viewBox`; they were
  clipped in every renderer. The LLM Core box was absent entirely.

**Experiment.** Rebuild keeping the draft's design and fixing what the run
exposed. Classifier reads the tail of history, not the whole of it. State store
writes JSON and reloads. Decisions are judged by the *following* cycle. Runtime
is an explicit object. Figure redrawn at 900×560 with the LLM Core box and the
feedback arrow present.

**Record.** Measured on this machine, 12 August 2026:

- `python3 -m core.selftest` — PASS: 3 cycles, 12 log lines, closure success rate
  0.50, state survived being reopened
- `python3 -m pytest tests -q` — **30 passed**
- Example 01 — `0.67 → 0.33 → closed`, labels `uncertain → converging → closed`
- Example 02 — `uncertain → closed → reopened → closed`
- Logs byte-reproducible; `git diff --stat examples/logs/` empty after a rerun

The closure success rates are 0.50 and 0.67, not 1.00, because failed attempts
are now recorded as failures.

**Still Vision, still unbuilt.** The hardware column. The stateless-baseline
comparison harness — until it exists, "fewer turns than a stateless baseline"
is a prediction and is labelled one in `THEORY.md`.
*(Superseded the same day — see the next entry. The harness now exists; the
hardware column remains Vision.)*

---

## 2026-08-12 — the prediction-1 harness, and the defect it caught first

**Evidence.** Before the harness could run, hand-tracing the loop through its
converging task exposed an ordering defect in the shipped classifier:
`AffectModel.classify` checked `stalled` before `converging`, so a run of three
same-goal gaps with *falling* magnitudes — `[1.0, 0.67, 0.33]`, a system
visibly making progress — was labelled `stalled`. The policy would abandon a
strategy that was working. The classifier's own docstring defines stalled as
"nothing is moving"; the implementation contradicted its spec, and the 30-test
suite missed it because no test fed a shrinking three-gap run.

**Interpretation.** The defect is precisely the failure prediction 2 names:
without a working converging/stalled distinction, closure gets worse. It also
shows why the harness had to exist — the examples exercise happy paths; only an
adversarial task set walks the label space hard enough to catch this.

**Experiment.** Fixed the ordering (converging before stalled; committed
example logs verified byte-identical, since neither example produces the
shape). Then built `experiments/`: a six-task deterministic suite — including
a control anyone ties, a task designed for the loop to *lose*, and a task
constructed to be unsolvable without state — against six task-agnostic
stateless baselines (every constant policy plus a magnitude-reactive one), the
shipped loop, and a stall-blind ablation carrying the pre-fix classifier.
Stateless purity is asserted by test; the committed results are asserted equal
to a fresh run by test.

**Record.** Measured on this machine, 12 August 2026 — 42 tests green:

- **Loop: 5/6 resolved with one policy and no task knowledge.** Best single
  task-agnostic stateless policy: 2/6. Per-task best-stateless portfolio:
  5/6, and the loop is strictly faster than the best stateless on zero
  tasks — the supported claim is adaptivity, not speed. Repeated-query task:
  loop 3 turns; five of the six task-agnostic baselines never close it; the
  sixth, the constant whose fixed strategy happens to be the answer, closes
  it in 1 and resolves nothing else in the suite.
- **`deploy_rollback`: loop 3 turns; all stateless DNF — by construction.**
  The observations at the two decision points are byte-identical and the
  required strategies differ, so no function of the current observation can
  solve it. Postulate 1 as a theorem about the task, not a benchmark score.
- **Ablation (prediction 2): stall-blind loop 4/6**, converging task DNF,
  closure rate 0.0 where the sighted loop measures 0.33.
- **No-store condition (prediction 3): `magnitude_reactive` 2/6** — the loop's
  per-observation knowledge minus history keeps only the tasks where the
  signal is in the observation.
- **Honest losses, pinned by tests:** `strict_interview` defeats the loop
  (converging → rephrase, no route back to ask) where `always_ask` resolves in
  2 — a v0.1 closure-policy limitation now on the record. And per-task
  pre-tuned constants beat the loop on their own task (`always_switch_tool` in
  1 turn) while resolving almost nothing else.

Scope, restated: a scripted, deterministic environment, no language model. The
predictions as claims about real LLM workloads remain Vision.

**Adversarial review, same day.** Three independent reviewers were set on the
harness with instructions to refute. Zero blocking findings; the impossibility
construction, the honest-loss task, turn-charging symmetry and byte
reproducibility all verified — including exhausting all 25 observation→strategy
tables against `deploy_rollback` (none solves it) and re-running the harness
under varied hash seeds (byte-identical). But the review caught **this
document's own prose committing the failure the harness exists to prevent**,
and the entry above is the corrected version. As first written it said "best
stateless: 2/6" — the one aggregate that flatters the loop — and "every
task-agnostic stateless policy DNF" on the repeated-query task, a false
universal: `always_switch_tool` is task-agnostic by this entry's own
definition and closes that task in 1 turn. The review also built the
`tuned_lookup` ceiling (task-informed stateless, 5/6, fails only
`deploy_rollback`), now adopted into the harness so the fact stays committed
and pinned; found a suite-tuned magnitude map resolving 3/6 (recorded as a
caveat, changes no verdicts, pinned by test); and had the byte-reproducibility
claim made platform-honest by pinning `newline` in every writer. The
corrections were made the same day, before merge, and this paragraph is the
record that they were needed.

---

## 2026-08-14 — the split landed; this package is unchanged, and still diverges from it

**Evidence.** `CrystalArchitect/Synthetic-Affect-Theory-` — a dedicated repository
that existed only as a one-line stub README when this project's SAT-split
question was first raised — now holds a real, merged copy of this package:
`PR #1` (2026-08-12) landed a ~20-file public v0.1 stack; `PR #2` (2026-08-12)
found and ported this package's own already-fixed classifier-ordering defect
(`stalled` checked before `converging`) after PR #1 shipped it a second time,
unaware this package's fix already existed; `PR #3` (2026-08-14) found and
fixed a defect this package does not have: `ClosureDecision.outcome` was
stamped at decide-time instead of defaulting to `"pending"` and being judged
by the following cycle, and `Loop` had no judging mechanism at all — the exact
cosmetic-closure failure `core/closure.py` in this package names by example.
None of PR #1–#3 touched this directory. No grant letter (G1/G2/H) has been
given for the split itself; it happened as a landed PR, not a decision.

**Interpretation.** Two homes of the same theory now both run, both pass
their own test suites, and still diverge in scope, not just in the defects
above. Present here, absent there: `experiments/` (the prediction-1 harness,
`RESULTS.md`, the adversarial-review record), `docs/GLOSSARY.md`,
`docs/FIGURE-1.md`, this file's own 2026-08-13 thesis-defence note in
`THEORY.md`. Present there, absent here: `docs/ai/` (AI contributor
credits), `docs/lyrics/` (the Sovereign Gap Held and Bridge, Not Loop
pages), a windowed `AffectModel` (F6, `window=10`) bounding classification
to a trailing slice rather than full history, and an explicit
`ClosurePolicy.reset()`. Which package is law remains open — restated, not
resolved, from the 2026-08-12 entry above.

**Experiment.** None run against this package's own code; this entry is
documentation, not a code change. The reconciliation work itself happened
in the other repository — see its `CHRONICLE.md`, 2026-08-14 entry, and
`Synthetic-Affect-Theory-#3` — where `python3 -m core.selftest` and
`python3 -m pytest tests -q` (19 passed) confirm the honesty-hinge fix
without altering this package.

**Record.** This package's own numbers are unchanged from the entry above:
`python3 -m pytest tests -q` — 45 tests; `python3 -m core.selftest` — PASS.
`README.md` now links to the dedicated repository under "Two homes, not
yet reconciled" so a reader here is not left assuming this is the only copy.

## 2026-08-14 — reconciliation, the other direction: docs and code from `Synthetic-Affect-Theory-`

**Evidence.** The prior entry recorded the scope gap in both directions.
`Synthetic-Affect-Theory-#5` closed canon → there (the harness and two
docs files). This entry closes there → here: a windowed `AffectModel`
(F6, `window=10`), an explicit `ClosurePolicy.reset()`, and
`docs/lyrics/`.

**Interpretation.** Not everything on the other side belongs here.
`docs/ai/Claude.md` and `docs/ai/MetaAI.md` are factual, repo-specific
credit records — "landing v0.1 in this repository," with that repository's
own verified numbers. Copying them here would misattribute this package's
own history, which `ATTRIBUTION.md` already states correctly and
differently (Meta AI drafted the reference implementation delivered
2026-08-12; Claude found and fixed the defects that draft shipped with).
`docs/ATTRIBUTIONS.md` — a third-party-marks notice for SpaceX, Tesla,
Grok, Neuralink, Synchron, Lynas, Suno — names nothing that appears
anywhere in this package's own docs; porting it would be irrelevant
padding, not reconciliation. Both are deliberately not ported, and this
paragraph is the record of that decision, not a silent gap. `docs/lyrics/`
is different in kind: Vision-belt mythos content *about* this theory's own
mechanics (state persistence, revoke timing, the window, the log shape),
not a claim about who built what where — safe to port, and it was.

**Experiment.** `core/affect.py`: `AffectModel.__init__(self, window=10)`,
`classify()` now operates on `history[-self.window:]` throughout. Every
existing check already only ever read `history[-1]`, `history[-2]`, and
`history[-STALL_RUN:]`, so this is backward-compatible by construction for
any run shorter than the window — which every test, example, and harness
run in this package is. `core/loop.py`'s `Loop.__init__` gained a `window`
parameter, threaded through to `AffectModel(window=window)`.
`core/closure.py`'s `ClosurePolicy` gained `reset()`, distinct from the
auto-reset already inside `decide()` — for a caller that wants to start a
fresh goal's stall count explicitly rather than waiting for a non-stalled
label. Five new tests: `tests/test_affect_window.py` (default window is
10, `window < 1` raises, a 300-entry history classifies identically to its
last-10 tail, and — the test that proves the window is actually applied,
not just accepted and ignored — a `window=2` `AffectModel` reads a
three-gap stalled run as `uncertain` instead) and one in `tests/test_closure.py`
for `reset()`. `docs/lyrics/SOVEREIGN-GAP-HELD.md` and `BRIDGE-NOT-LOOP.md`
ported with this package's own `™` (no variant selector) convention.

**Record.** Measured on this machine, 2026-08-14: `python3 -m pytest tests -q`
→ 50 passed (45 → 50); `python3 -m core.selftest` → PASS, 3 cycles, 12 log
lines, closure success rate 0.50, state survived reopen — **unchanged from
before this entry**, confirming the windowing addition changes nothing at
this package's own scale, by measurement rather than by the argument
alone; `examples/logs/*.jsonl` and `experiments/results/{results.json,
RESULTS.md}` re-run and diffed against the pre-change committed baseline —
`git diff --stat examples/logs/ experiments/results/` empty, both before
staging this commit; `grep -rnE "[A-Za-z0-9]®" . --exclude-dir=.git` →
nothing.

## 2026-08-14 — the grant: G2, split decided, this directory retired

**Evidence.** Every prior entry in this file restated the same open
question — "which package is law remains open" — five times across two
days, through a defect this repo caught and the other shipped anyway, and
a full bidirectional reconciliation that made the two byte-for-byte
equivalent in capability. The maintainer's decision: **G2 — grant the
split.** `CrystalArchitect/Synthetic-Affect-Theory-` becomes the theory's
canonical home; this directory is retired to a pointer.

**Interpretation.** The reconciliation work that preceded this entry
wasn't wasted by the grant — it's why the grant was safe to make now
rather than earlier. Granting the split when the dedicated repository was
a one-line stub (as it was when this file's first entries were written)
would have meant starting over somewhere new. Granting it after PR #1
shipped two defects this package had already fixed would have meant
canonising a regression. Granting it now, once both copies passed the
same tests with the same numbers, means the theory doesn't lose anything
in the move. The rename to drop the dedicated repository's trailing
hyphen is part of the grant but is a manual step in that repository's own
settings — not done as part of this commit, and this file does not claim
otherwise.

**Experiment.** `core/`, `tests/`, `experiments/`, `examples/`,
`crystalcode/`, `docs/` (including the just-ported `lyrics/`), `THEORY.md`,
and `conftest.py` removed from this directory — all of it stays in this
repository's git history, none of it is deleted from the record.
`README.md` rewritten as a pointer to the new home, stating plainly what
used to be here and why it was retired rather than left live. This file
and `ATTRIBUTION.md` are the only files kept, unedited except for this
entry — the permanent record of what happened in this directory, which
the new home's own `CHRONICLE.md` does not and should not restate from
its own landing entry onward.

**Record.** No `python3 -m pytest` or `core.selftest` to run — there is no
code left in this directory to verify. The verification that matters is
upstream of this commit: `Synthetic-Affect-Theory-#5`'s own numbers (31
tests passed, harness matching this package's numbers task for task) are
what the grant relies on, and they were measured before the grant, not
after. Cross-repository references checked before this commit:
`TerAustralis-Incognita` has none (grepped, none found — an earlier,
unverified report claiming otherwise did not hold up). `TheCrystalVision/
interface/map.json` did have one — a `"CANON"`-badged entry naming this
directory as the canonical home — corrected in the same pass as this
retirement, in that repository.

---

**All rights reserved.**
TerAustralis Incognita™ — ABN 70 741 068 059

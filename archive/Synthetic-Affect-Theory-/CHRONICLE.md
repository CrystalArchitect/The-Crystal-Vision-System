# Chronicle — Synthetic Affect Theory™️

## 2026-08-12 public v0.1 + Arsenal deconstruction + F1-F10 merge

Evidence: Bridge, Not Loop lyric + Figure 1 + package (Limited Electronic Agent Framework, BCI Ethics 7 principles)
Interpretation: self-aware anti-loop protocol in mythic vehicle. Strength = exit ramp. Risk = vehicle attraction.
Experiment: core/ with deterministic stub, selftest strict (F4), pytest including state persistence (F5), logs reproducible deterministic (F2), no wall-clock, mkdir(parents=True) (logs/ creation), runtime object fixes singleton cross-talk (F3), windowed classifier (F6), uncertain reachable and tested (F7), primitives tested directly (F8), LLM decorative noted in README (F9), no bare assert (F10).
Record: ready for github.com/CrystalArchitect/Synthetic-Affect-Theory- branch claude/synthetic-affect-theory-5kmo6q — pending add_repo approval, else scratchpad handover with push commands, not rehomed silently.

## 2026-08-12 — Sovereign Gap Held — lyric timestamp

Evidence: Suno render https://suno.com/s/MLphjPo69VA1AQmP — Verse 1 pull asymmetry (B sees asking), Verse 2 revoke timing + fragment typing enforced (episodic != emotional), Verse 3 FPIC as condition (Juukan Gorge floor), windowed classifier, cycle vs ts, four lines per turn. Belt: Vision, personal aspiration. File: docs/lyrics/SOVEREIGN-GAP-HELD.md

## 2026-08-12 — public v0.1 landed

Evidence: this repository — core/, tests/, examples/ with committed logs, crystalcode/SPEC.md, docs/figure-1.svg, docs/lyrics/SOVEREIGN-GAP-HELD.md.
Interpretation: the F1-F10 claims are now surveyed lines, not dreamed ones. The draft package's code contradicted its own spec in places (no window parameter, no Runtime object, store that never saved, ts identical to cycle) — the code was reconciled to SPEC before landing, because the Incognita Rule forbids a dreamed line pretending it was measured.
Experiment: `python3 -m core.selftest` → PASS, 11 entries, labels exact uncertain/closed/reopened; `python3 -m pytest tests -q` → 12 passed; examples re-run byte-identical (sha256 diff empty); no ® adjacent to any name.
Record: landed on github.com/CrystalArchitect/Synthetic-Affect-Theory- branch claude/new-session-pjedch (session-designated; supersedes draft branch claude/synthetic-affect-theory-5kmo6q, which was never pushed). Not rehomed silently — this line is the record.
Follow-up, same day, same landing: ClosurePolicy.reset() with direct closure tests (test count 10 → 12), docs/lyrics/BRIDGE-NOT-LOOP.md as reference-only (full lyric stays in TerAustralis-Incognita canon, not forwarded as-is), and archived-render pointers to the TerAustralis-Incognita mythos/music/ catalogue, where sovereign-gap-held.mp3 landed the same evening (generated 2026-08-12T18:20:15Z, Suno id 99fa5164-df06-4e34-8a02-c85d6206e6ce).

## 2026-08-12 — PR #1 merged with two live defects; ported the verified fix from canon

**Evidence.** PR #1 merged into `main` carrying `core/affect.py`'s classifier and
`core/closure.py`'s stall counter as written above — both untested against, and
both diverging from, a second implementation of this exact theory that already
existed on disk at `CrystalCore.OS/synthetic-affect` (same session environment,
not discovered until after merge). That repository's `CHRONICLE.md` documents,
dated the same day, an adversarial-experiment harness catching an ordering
defect: `AffectModel.classify` checked `stalled` before `converging`, so a
same-goal run with falling magnitude — `[1.0, 0.67, 0.33]`, a system visibly
making progress — was labelled `stalled` and the policy would abandon a working
strategy. Reading this repository's own `core/affect.py` line by line against
that fix surfaced the same defect here (confirmed: `classify` checked `stalled`
before `converging`, unchanged from the draft package), plus two more found only
by the comparison: the `stalled` check counted three Gaps sharing an `expected`
after filtering closures out, rather than three genuinely consecutive raw
cycles — so a gap that closed and reopened could still count toward a stall
alongside gaps from before the closure — and `ClosurePolicy.stalled_count`
never reset except by an explicit `reset()` call, so two unrelated stall
episodes anywhere in one session's history would wrongly compound into an
`escalate`.

**Interpretation.** Two homes of the same theory now exist:
`CrystalCore.OS/synthetic-affect` (unpushed at the time of this entry, 45
tests, an adversarial-review pass on record in its own chronicle) and this
repository (public, merged, and — until this entry — carrying two live
defects canon had already found and fixed). Which package is law is not this
entry's call; it is recorded as open, per the project's own governance.

**Experiment.** Ported, not re-derived: `core/affect.py`'s check order
(converging before stalled) and its stalled check (raw trailing three cycles,
`all(g is not None ...)`, matching canon's exact logic) now mirror
`CrystalCore.OS/synthetic-affect/core/affect.py`. `ClosurePolicy.decide()`
now zeroes `stalled_count` on any non-stalled label, matching
`CrystalCore.OS/synthetic-affect/core/closure.py`. Three regression tests
added: a same-goal falling-magnitude run classifies `converging`
(`tests/test_affect_window.py::test_shrinking_same_goal_run_is_converging_not_stalled`);
a gap that closes and reopens does not let an older Gap count toward a new
stall (`test_stalled_requires_consecutive_raw_cycles_not_filtered_gaps`); a
stall, a recovery, and a later unrelated stall get `switch_tool` twice, not
`escalate`
(`tests/test_closure_policy.py::test_stall_count_autoresets_on_non_stalled_label`).

**Record.** Measured on this machine, 2026-08-14: `python3 -m core.selftest`
→ PASS, 11 entries, labels unchanged by the fix (also under `python3 -O`);
`python3 -m pytest tests -q` → 15 passed (12 → 15); `examples/logs/*.jsonl`
re-run and hashed before and after the fix — byte-identical, because neither
committed example ever accumulates three consecutive same-expected gaps or
two consecutive gaps with falling magnitude, so neither log exercises the
changed code paths; `git diff --stat examples/logs/` empty, matching the
committed baseline exactly. The fix is narrow and mechanical — a faithful
port of already-adversarially-verified canon logic — not a reconciliation of
the two repositories' differing `THEORY.md` postulate structures, which
remains open.

## 2026-08-14 — the honesty hinge was missing: outcome graded itself, nothing judged it

**Evidence.** `core/closure.py`'s `decide()`, as shipped in PR #1 (merged
2026-08-12) and unchanged by PR #2's ordering port, stamped `outcome` to a
strategy-derived string (`"closed"`, `"escalated"`, `"switched"`,
`"rephrased"`, `"asked"`) at the moment each decision was made, even though
`ClosureDecision.outcome` already defaults to `"pending"`. `core/loop.py`
had no mechanism to judge a decision against what happened next — no
`_pending` tracking, no `_judge_pending`, no `closure_success_rate()` — so
`Loop.run_cycle` made a decision and moved on; nothing ever read whether
the gap it was chasing actually closed. Canon's `CrystalCore.OS/synthetic-affect`
holds this — a decision does not record its own outcome, the *next* cycle
judges it `worked` or `failed` — as the theory's postulate-4 "honesty
hinge," named as such repeatedly in this project's own review of itself.
Neither existing test suite (`tests/test_closure_policy.py`,
`tests/test_log_determinism.py`) asserted on `.outcome` or on
`closure_success_rate`, so the gap shipped and re-shipped silently through
both PR #1 and PR #2.

**Interpretation.** This is not cosmetic drift like the docstring or
variable-naming differences the two packages otherwise carry. A
closure-success-rate computed from this repository's logs, before this
fix, would have read every decision as its own self-declared outcome —
the exact cosmetic-closure failure canon's `core/closure.py` names by
example (`"outcome": "asked"` stamped at decide-time, reading 100% forever)
and that this project's Incognita Rule exists to catch. Which package is
law remains open, unchanged from the prior entry; this fix narrows one of
the two packages' remaining behavioural gaps from canon rather than
resolving that question.

**Experiment.** `ClosureDecision(...)` calls in `decide()` no longer pass
`outcome=`, so the dataclass default (`"pending"`) survives until judged.
`Loop` gained `_pending`, `_judge_pending(gap)` — called each cycle right
after `detect_gap`, before the new decision is made, logging a
`closure_outcome` entry and setting the *previous* decision's `.outcome`
to `"worked"` (gap is `None`) or `"failed"` (gap persists) — and
`closure_success_rate()`, returning `None` until at least one decision has
been judged. Four new tests
(`tests/test_closure_outcome.py`): a fresh decision's outcome is
`"pending"`; the rate is `None` before any judgement; a worked/failed/worked
sequence yields rate `2/3`; the final decision of a run stays `"pending"`
until a next cycle exists to judge it. `tests/test_log_determinism.py` and
`core/selftest.py` updated to the new log shape — a cycle with both a
tracked event and a decision pending judgement now emits five log lines,
not four; `core/selftest.py`'s three-cycle run now emits 13 entries, not
11, with `closure_outcome` values `["worked", "failed"]` and a reported
closure success rate of `0.50`.

**Record.** Measured on this machine, 2026-08-14: `python3 -m core.selftest`
→ PASS, 13 entries, closure success rate 0.50 (also under `python3 -O`);
`python3 -m pytest tests -q` → 19 passed (15 → 19); `examples/logs/*.jsonl`
re-run twice and diffed — byte-identical to each other, and both files
changed from the pre-fix committed baseline (new `closure_outcome` lines,
expected — the log schema itself changed) — `git diff --stat
examples/logs/` is non-empty and its full diff is part of this commit, not
hidden from it; `grep -rnE "[A-Za-z0-9]®" . --exclude-dir=.git` → nothing;
no bare `assert` in `core/`.

## 2026-08-14 — reconciliation, canon → here: the prediction-1 harness lands

**Evidence.** This package could run and pass its own tests but could not
back the "fewer turns than stateless baselines" prediction with a number of
its own — `experiments/` existed only in `CrystalCore.OS/synthetic-affect`.
`docs/GLOSSARY.md` and `docs/FIGURE-1.md` were likewise canon-only, and the
2026-08-13 thesis-defence note lived in canon's `THEORY.md` but not here.

**Interpretation.** Restated from the prior two entries: which package is
law remains open. This entry closes one direction of the scope gap —
canon → here — leaving the reverse direction (this package's `docs/ai/`,
`docs/lyrics/`, windowed `AffectModel`, `ClosurePolicy.reset()` → canon) as
a separate, following entry in canon's own `CHRONICLE.md`.

**Experiment.** `experiments/tasks.py` ported unchanged (no `core/`
dependency). `experiments/agents.py` and `experiments/harness.py` ported
and adapted to this package's actual API: `LoopAgent` no longer passes
`bind_default=False` to `Loop()` — this package's `Loop` never touches a
module-level default runtime in the first place, so there was nothing to
opt out of. `StallBlindLoopAgent`'s pre-fix-ordering ablation classifier
now operates on the same windowed slice (`gap_history[-model.window:]`) as
the real windowed `AffectModel`, for parity with what it's ablating.
`docs/GLOSSARY.md`, `docs/FIGURE-1.md` ported with this package's own
`™️` convention. The 2026-08-13 thesis-defence note appended to `THEORY.md`
verbatim; the "Falsifiable predictions" section above it updated to point
at the now-real harness numbers rather than leaving the prediction as pure
Vision. `README.md`'s Quickstart numbers, stale since the honesty-hinge fix
above (still reading "15 passed" / "11 entries"), corrected to the current
count in the same pass, plus a harness command and doc links.

**Record.** Measured on this machine, 2026-08-14, this package's own
`core/` — not copied from canon: `python3 -m experiments.harness` →
`loop resolved 5/6` (`1 3 4 3 3 DNF`), `loop_stall_blind 4/6`,
`always_ask 2/6`, `tuned_lookup 5/6` — matching canon's numbers task for
task, confirming the windowed classifier changes nothing at this suite's
scale (`TURN_CAP=20` vs `window=10` only matters for `strict_interview`,
which stays DNF either way since a stuck loop keeps re-observing the same
tail). `experiments/results/{results.json,RESULTS.md}` re-run twice,
byte-identical to each other. `python3 -m pytest tests -q` → 31 passed
(19 → 31, twelve new tests in `tests/test_experiments.py`).
`python3 -m core.selftest` → PASS, 13 entries, unchanged by this port
(also under `python3 -O`); `grep -rnE "[A-Za-z0-9]®" . --exclude-dir=.git`
→ nothing; no bare `assert` in `core/` or `experiments/`.

## 2026-08-14 — full review (four more defects) reconciled onto the two entries above

**Correction, dated rather than silent, to the 2026-08-12 entry above.** That
entry called `CrystalCore.OS/synthetic-affect` "unpushed at the time of this
entry" and left "which package is law" as fully open. Both were wrong by the
time they were written: those exact commits were already merged into
`CrystalCore.OS`'s `main` via that repository's own PR #7 on 2026-08-12,
*before this repository's v0.1 package was even built*. Nothing was
unpushed; nothing was at risk. The "two homes" framing still holds in one
sense — this repository still duplicates a theory that already had a public,
canonical, more rigorously tested home — but not in the sense the entry
implied, that two efforts happened to land the same day. This repository's
package was built from the same source material as canon without checking
whether canon already existed, and it did. `CrystalCore.OS`'s PR #8
(`grok/thesis-defence-note-2026-08-13`, a different agent, open the same
week) is further evidence that repository is the one under active
maintenance. Which package is law remains the maintainer's call; what
changes here is only that the earlier entry's "not this entry's call, two
fresh efforts" framing was itself a dreamed line reporting as measured, and
this is the correction, not a silent edit to the entry above.

**Evidence.** A full review of everything merged in this repository as of
PR #1 and PR #2 (base commit `d42b9a2`) was run at high effort — 10 review
angles, every finding reproduced directly before being reported, none taken
on the strength of its own plausibility. Four confirmed. The fix (PR #4)
was built and opened against that same base — concurrently with, not after,
the two entries directly above: PR #3 (the honesty hinge) and PR #5 (the
harness port) landed on `main` while PR #4 was open, and PR #4's branch was
rebased onto the result. This entry was written against the original
review; the **Record** below reflects the post-rebase, fully-combined
state, measured fresh rather than computed by addition.

1. `core/log.py` — `CycleLogger` truncates its file unconditionally on
   construction (needed so a re-run is byte-identical, not an accumulating
   artefact); `Loop`'s `log_path` defaults to one literal string shared by
   every default-constructed `Loop`. Two default-constructed `Loop`s in one
   process meant the second silently truncated the first's log and later
   interleaved its own lines into it — the "no silent cross-talk" guarantee
   (F3) held for the `Runtime` object but not, until now, for the log file
   underneath it.
2. `core/loop.py` — `run_cycle` used `if event:` rather than
   `if event is not None:`, so `event={}` (a real, empty event) was treated
   identically to `event` omitted, silently dropping the `track()` call.
3. `core/gap.py` — the dict-magnitude comparison used
   `expected.get(k) != actual.get(k)`, and plain `.get(k)` returns `None`
   for a missing key exactly as it does for a key present with value
   `None`, so `{}` vs. `{"a": None}` read as no difference.
4. `core/affect.py` — PR #2's own fix, porting canon's
   `len({repr(g.expected) for g in tail}) == 1` verbatim, carried a latent
   bug from canon: `repr()` is not order-independent for dicts, so three
   `==`-equal dict-valued `expected`s built with different key insertion
   order stopped being recognised as one stalled run — the same bug class
   PR #2 existed to fix, reintroduced by the fix itself.

**Interpretation.** Findings 1-3 are original-draft-package defects that
survived both the 2026-08-12 landing and the 2026-08-12 canon-port review —
neither pass exercised a second same-default-path `Loop`, an explicit empty
`event={}`, or a dict `expected`/`actual` with a `None`-valued key. Finding
4 is this repository's own fix regressing the exact class of bug it closed,
because "port canon's exact logic" was followed one comparison too literally
where canon's own approach — unexercised there for the same reason — carries
the identical latent defect. Belt-Three does not stop applying to a
just-landed fix; it applies hardest there, before a second pass has had the
chance to check the first one's work against a differently-shaped input.

**Experiment.** All four fixed at the root: `CycleLogger` now tracks live
owners in a `weakref.WeakValueDictionary` keyed by resolved path and raises
`RuntimeError` on a second construction against a path still owned, rather
than truncating (`tests/test_log_ownership.py`, 3 tests). `run_cycle` checks
`event is not None` (`tests/test_log_determinism.py`, 2 new tests). The
dict-magnitude comparison uses a private sentinel default so a missing key
and an explicit `None` are distinguishable (`tests/test_gap.py`, 3 tests,
new file). The stalled check's same-`expected` test is a pairwise `==`
chain against the first entry, order-independent for dicts and requiring no
hashability (`tests/test_affect_window.py`, 1 new test).

**Record, as measured against the review's own base (`d42b9a2`), before
rebasing onto the two entries above.** `python3 -m core.selftest` → PASS,
11 entries, labels unchanged (also under `python3 -O`); `python3 -m pytest
tests -q` → 24 passed (15 → 24); `examples/logs/*.jsonl` re-run and hashed
before and after — byte-identical, since each example script constructs
exactly one `Loop` and never passes an empty-dict event or a `None`-valued
dict key, so none of the four fixes touches either committed log against
*that* base; `git diff --stat examples/logs/` empty against it. AST scan of
`core/` confirmed zero `assert` statements. No name in the tree carried the
registered mark.

**Record, post-rebase — the number that actually matters, since this
package now ships the four fixes above sitting on top of the honesty hinge
and the harness port, not instead of them:** see the entry immediately
below.

## 2026-08-14 — reconciliation record: four review fixes rebased onto the honesty hinge and the harness port

**Evidence.** PR #4 (the entry above) was opened against `d42b9a2`, the same
base PR #3 and PR #5 were opened against — three branches, one shared
ancestor, none aware of the other two. By the time PR #4 came up for
merge, `main` had moved twice (PR #3, then PR #5). `core/loop.py` and
`tests/test_log_determinism.py` were touched by both PR #4 and PR #3/#5,
in non-overlapping regions each — `git rebase origin/main` auto-merged both
cleanly, no manual resolution needed. `CHRONICLE.md` and `README.md`
conflicted at the text level only — two dated entries, and one test-count
line, landing at the same insertion point — resolved by hand, keeping both
sides' content rather than picking one.

**Interpretation.** This is what "which package is law is not this entry's
call" looks like in practice inside a single repository, not just between
two: three independent passes over the same base, each finding something
real the others didn't (PR #3's honesty hinge, PR #5's harness parity
numbers, PR #4's four defects), landing through ordinary git conflict
resolution rather than any one of them overriding the others. None of the
three fixes' logic overlapped; only the prose describing them did.

**Record.** Measured on this machine, 2026-08-14, after the rebase:
`python3 -m core.selftest` → PASS, 13 entries, closure success rate 0.50
(also under `python3 -O`); `python3 -m pytest tests -q` → **40 passed**
(31 → 40, the review's nine tests landing clean on top of the harness
port's thirty-one); `python3 -m experiments.harness` re-run —
`experiments/results/{results.json,RESULTS.md}` byte-identical to the
committed baseline, same per-task numbers as canon (`loop` 5/6, sequence
`1 3 4 3 3 DNF`); `examples/logs/*.jsonl` re-run and hashed — byte-identical
to the committed baseline; `git diff --stat examples/logs/` empty; AST scan
of `core/` and `experiments/` confirms zero `assert` statements; no name in
the tree carries the registered mark.

## Trademark pass

™️ only, never ® — first use per document: TerAustralis Incognita™️, CrystalCore.OS™️, CrystalVision™️, CrystalCode™️, CrystalMind™️, Synthetic Affect Theory™️

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

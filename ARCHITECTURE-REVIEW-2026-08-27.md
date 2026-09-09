# Architecture Review — 2026-08-27

*Independent review, requested by the maintainer. No prior review artifact
existed at this or a similar path — this is original analysis. Every finding
below was checked against the actual code and test suite on this branch
(`git log` tip `cdd9db9`), not against what the docs claim.*

---

## Summary

This is not the theory-only repository the review brief assumed it might be.
`Synthetic Affect Theory` is a "constitutional layer" — a veto grammar wrapped
around a model turn — with real, tested Python under `core/` implementing
most of what its own spec describes, and a repo-wide practice of explicitly
labelling what is executable versus merely specified. That practice is
genuinely good discipline, and it is also currently wrong in one place: the
spec's own "executable vs specified" table undersells its own code, listing
the P1–P10 Policy Library as "not yet a runtime" when it is fully implemented
and covered by 12 passing tests. Outside that, the repo is clean — no
locked-name violations, no Indigenous-knowledge-boundary issues, and only one
residual gendered pronoun survived the repo's own recent targeted sweep to
remove them.

---

## Strengths

- **"What is executable vs specified" is a real, rare practice, not just a
  slogan.** `docs/spec/README.md` states plainly which parts of the spec have
  a runtime and which don't, dated and versioned. This is close to exactly
  the Belt-Three discipline the wider ecosystem asks for, applied here
  independently.
- **The four-gate sovereignty MVP does what it says.** `core/sovereignty.py`
  implements DUR → Agency → Intrusion → Escape as claimed; `core/stochastic.py`
  correctly blocks remote sampling of operator/relational state without a
  consent token. The full suite — 130 tests across `core/` — passes cleanly
  (`python3 -m pytest tests/`: 130 passed).
- **The Indigenous Data Sovereignty boundary holds.** No occurrence of
  "Songline" anywhere in the repo, in code or docs (checked by full-tree
  grep). "Starline" is used extensively as this repo's own long-arc
  coherence-pattern concept — a real, distinct coinage in the same spirit as
  the wider ecosystem's usage, not a collision with it. `docs/spec/REGIMES.md`'s
  "song-mapping stress tests" use only mainstream pop-song titles as metaphor
  labels ("titles only, not lyrics," as the doc itself states) — no
  Indigenous cultural material appears anywhere in the set.
- **No LLM carries a "Crystal" name.** Checked `core/`, `docs/spec/`, and
  `docs/sovereignty/` directly — "CrystalCore" and "CrystalCode™️" are this
  project's own declared trademarks (consistent with the wider ecosystem's
  locked names), never applied to a vendor model.
- **The repo's own targeted pronoun fix mostly worked.** The tip commit,
  `cdd9db9` ("Operator language: they/them, not she/her"), correctly changed
  the operator's pronoun language across the fixture/gate summary surface it
  targeted — a full-tree grep after that commit finds only one surviving
  instance (see Findings), not a wholesale miss.

---

## Findings

### MEDIUM — The spec's own "executable vs specified" table understates its own code

**Evidence.** `docs/spec/README.md` states:

> **Specified, not yet a runtime:** ontology sampling, **P1–P10**, starline
> techniques, Addendum A monitors, ledger cadence, transformation exemption
> checks.

But `core/policies.py`'s own module docstring says otherwise: *"Ordinary
Policy Library P1–P10. **v0.1.1 executable sketch.**"* Every one of P1, P2,
P3, P4, P5, P6, P8, P9, P10 is implemented as a real function
(`_p1`–`_p10` in `core/policies.py`), and `tests/test_ontology_policies.py`
exercises nine of them directly by name (`test_p1_fires_on_elevated_boundary`,
`test_p10_when_steady`, `test_p8_on_low_clarity`, `test_p9_surfaces_does_not_pick`,
`test_p6_distance_not_attunement`, `test_gates_block_before_policy`,
`test_ordinary_cycle_runs_p10`, plus the ontology-validation tests). All 12
tests in that file pass.

This is the reverse of the usual Belt-Three failure mode (Vision presented as
Science) — here, real Science-belt work is mislabelled as unbuilt Vision. It's
lower severity than overclaiming, since nobody reading this table would be
misled into trusting something that doesn't exist, but the table is a direct,
checkable claim about the code, and it's currently false for P1–P10.

I did *not* extend this finding to "ontology sampling" — the base ontology
dimension types and validation (`core/ontology.py`) are also implemented and
tested (`test_eleven_core_dimensions`, `test_values_clamp`,
`test_no_hidden_keys`), but "sampling" may refer to a narrower,
not-yet-built instrumentation feature distinct from dimension validation, and
I don't have enough context to be certain either way — flagged as an open
question below rather than asserted.

**Recommendation.** Update the table to move "P1–P10" from "Specified, not
yet a runtime" to "Executable now," alongside the four-gate MVP. Left as a
documented finding rather than fixed directly, since the maintainer may want
to word the distinction more precisely than a one-line table edit would
(e.g. "executable sketch" vs. "production-hardened" is a real distinction
this repo cares about elsewhere, per the policies.py docstring itself).

### FIXED — One residual gendered pronoun survived the repo's own pronoun sweep

**Evidence.** `docs/sovereignty/ADDENDUM-B.md:17` (Burden Release Note):
*"The system may surface the cost. It may never insist **she** keep wearing
it."* — referring to the operator. This is the sole instance of "she,"
"her," "he," or "his" found anywhere in the repo (full-tree, case-insensitive,
whole-word grep across every `.md` and `.py` file) after the tip commit's
explicit "Operator language: they/them, not she/her" fix — a residual miss
from that same pass, not a new issue.

**Fixed in this PR.** Changed to "It may never insist **they** keep wearing
it," consistent with the rest of the document and the repo's own stated
convention.

---

## Open questions for the maintainer

1. **Does "ontology sampling" in the executable-vs-specified table refer to
   something beyond the dimension validation already implemented and tested
   in `core/ontology.py`?** If it's the same thing, that line should move to
   "executable" alongside P1–P10. If it refers to a genuinely separate,
   unbuilt sampling/instrumentation feature, the table is already correct on
   that point and no change is needed.
2. **Is a "v0.1.1 executable sketch" (per `policies.py`'s own docstring)
   meant to count as "executable" in the table's binary sense**, or is there
   an intended maturity gap between "sketch" and "runtime" that the table is
   trying to preserve? This affects how Finding 1 above should actually be
   worded, not just whether it's raised.

---

**Rights.** All rights reserved. TerAustralis Incognita™️ — ABN 70 741 068 059

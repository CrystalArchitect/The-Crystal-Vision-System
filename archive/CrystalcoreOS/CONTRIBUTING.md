# Contributing to CrystalCore.OS

Thank you for wanting to build sovereign, auditable, local-first intelligence.
Contributions of all sizes are welcome — code, tests, documentation, and
thoughtful issue reports all count.

## How to contribute

1. **Fork** this repository to your own account
2. **Branch** from `main` with a descriptive name (`fix-memory-pruning`,
   `docs-sensor-examples`)
3. **Make your change**, following the non-negotiables below
4. **Run the tests** — everything must pass:
   ```bash
   python3 run_tests.py                    # core suites
   python3 run_tests.py tests/test_mesh.py tests/test_swarm.py
   ```
5. **Open a pull request** against `main`, describing what changed and why

All changes land through pull requests reviewed and merged by the maintainer.
Nobody — including collaborators — pushes directly to `main`.

## The non-negotiables

These properties define the project. PRs that break them will not be merged,
however good the idea:

- **Standard library only.** No required external dependencies, ever. The
  framework must run on a bare Python 3 install on a Raspberry Pi.
- **Consent fails closed.** A forbidden input refuses, logs, and writes
  nothing. Never "fail open for convenience."
- **Coherence is honest.** A conclusion is never more confident than its
  weakest input. No mechanism may inflate coherence without cause — see the
  swarm's reinforcement layer for the pattern (persistence-gated, capped,
  diminishing returns).
- **Provenance everywhere.** Derived items link back to their inputs and the
  rule that produced them.
- **Closed registries.** Evolutionary mutation recombines named, pre-vetted
  rules/behaviours — it never invents new logic at runtime.
- **Tests required.** New behaviour ships with tests that run under the
  stdlib runner (`run_tests.py`); plain `test_*` functions, no pytest
  dependency.
- **Determinism where it counts.** Seeded runs must reproduce.

## Style

- Match the surrounding code: clear docstrings explaining *why*, dataclasses
  for records, type hints throughout.
- Keep modules independently useful and importable.
- No network code in core paths. External communication belongs behind the
  lattice/sensor boundaries with injected transports.

## Cultural respect

This project draws inspiration from Australian Indigenous concepts (Songlines,
Dreamtime references) within its naming and vision. Contributors must treat
this material with care:

- Indigenous knowledge in the planned Wisdom Layer is **strictly
  consent-pending until custodian partnership exists** — do not add cultural
  content, stories, or knowledge beyond the existing naming without explicit
  maintainer approval.
- If you believe existing material oversteps, please open an issue — that
  feedback is welcome and taken seriously.

## Security

- Never commit secrets, credentials, API keys, server addresses, or personal
  information — yours or anyone else's.
- Report suspected vulnerabilities privately to the maintainer rather than in
  a public issue.

## Licensing of contributions

By contributing, you agree your contribution is licensed under the project's
**AGPL-3.0** license.

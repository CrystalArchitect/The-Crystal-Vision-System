# H2 experiments

Methodology is locked at V0.1. This directory runs the execution sequence
from `docs/H2/GOVERNANCE.md`. It must not modify production CrystalCore.

## 1. Reference-fidelity test (32k / 64k) — recorded

```
python3 experiments/run_reference_fidelity.py --selftest
python3 experiments/run_reference_fidelity.py
```

## 2. Development sweep — not a configuration freeze

```
python3 experiments/run_dev_sweep.py --selftest
python3 experiments/run_dev_sweep.py
```

Independent systems: `reference`, `candidate_a`, `candidate_b`.
Development partition only. Final seed family is refused.
Receiver fidelity is the ranking axis. Bandwidth is recorded, not gated.

## 3. Validation — not a configuration freeze

```
python3 experiments/run_validation.py --selftest
python3 experiments/run_validation.py
```

Validation seed family only (`VAL_CORPUS_SEED`). Refuses `development`
(already used in steps 1–2) and `final`. Configs under test are taken
from each candidate's own published sweep ranking plus the Step-1
development default. See `benchmarks/validation_configs.py`.

## 4. Configuration freeze — recorded (not a 1M decision)

One config per candidate, selected from the validation record by the
rule in `docs/H2/FROZEN-CONFIGS-V0.1.md`. Machine copy:
`benchmarks/frozen_configs.py`. Record: `results/config-freeze-v0.1/`.

## 5. Immutable final test (32k → 1M)

```
python3 experiments/run_final_test.py --selftest
python3 experiments/run_final_test.py
```

Final seed family is unsealed **only** by this runner. Frozen configs only
(`benchmarks/frozen_configs.py`) + dense reference. Dual-gate evaluated at
1M tokens. Development and validation seeds are not reused.

Record: `results/final-test-v0.1/`. Dual-gate at 1M: **fail** for both
frozen configs (quality LCB ≥ 0.90; analytical BW/ref ≰ 0.40). Not a
language-model result. Not a CrystalCore product claim.


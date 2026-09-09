# H2 Governance

## Rules

* H1 remains frozen and untouched.
* H2 methodology is fully locked.
* No performance claims until the immutable final test is complete.
* Candidate independence rule is binding.
* Development may explore parameters but may not change the frozen benchmark, metrics, gates, or final-test corpus.
* Any substantive change to the locked protocol creates H2 V0.2.

## Recorded (V0.1, not a protocol change)

1. Reference-fidelity test (32k/64k) — recorded
2. Development sweep — recorded (not a freeze)
3. Validation — recorded (not a freeze)
4. Configuration freeze — recorded 2026-08-23; [`FROZEN-CONFIGS-V0.1.md`](FROZEN-CONFIGS-V0.1.md)
5. Immutable final test (32k → 1M) — recorded 2026-08-23; [`../../results/final-test-v0.1/`](../../results/final-test-v0.1/)
6. Decision against dual gates — **fail** for both frozen configs (quality LCB pass, bandwidth fail; simultaneous gate not met). See the final-test SCOPE.

No performance claims beyond this locked record. The fail is on the synthetic
associative-memory encoder under the V0.1 analytical bandwidth model. It is
not a language-model result and not a CrystalCore product claim.


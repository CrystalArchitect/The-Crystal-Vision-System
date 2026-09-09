# H2 reference-fidelity measurements (32k / 64k)

**Status:** Development partition · methodology locked · no performance claims

See [SCOPE.md](SCOPE.md). Measurements only. The 1M dual gate is not
evaluated. Candidate configs are development defaults, not frozen.
CrystalCore advantage remains unproven.

| System | Gold acc | LCB(acc) | vs ref (ratio LCB) | BW bytes | BW / ref | Agree with ref |
|---|---|---|---|---|---|---|
| reference | 1.0000 | 0.9981 | — | 228366848000 | 1.00 | — |
| candidate_a | 0.9970 | 0.9935 | 0.9970 (LCB 0.9945) | 164734936952 | 0.7214 | 0.9970 |
| candidate_b | 0.9930 | 0.9883 | 0.9930 (LCB 0.9890) | 160796560832 | 0.7041 | 0.9930 |

n = 1000 items per length, lengths = 32768 and 65536 (2000 paired items).
Bandwidth model: analytical fp32 element counts (index / routing / kv / attention / output).

These ratios are **not** a pass or fail of the 1M dual gate.

H1 remains frozen. Production `core/` was not modified.

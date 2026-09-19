# Synthetic Affect Theory — public v0.1 stack

> **Ethics header, first thing, non-negotiable:** Synthetic = apparent / functional, for design purposes. Not a claim of feeling, consciousness, or inner experience.

![Figure 1](docs/figure-1.svg)

**Implementation:** CrystalCore.OS | **Language:** CrystalCode | **TerAustralis Incognita** | **ABN 70 741 068 059**

### The 80/20 that protects it
**Bridge, Not Loop distinction + final rule:** If it stops serving clarity or raises human cost → set it down.

### What this is
Theory locked in conversation but exists nowhere on disk — this repo date-stamps authorship and turns Figure 1 into a stack others can test.

- **Science:** "The loop runs; here are its gap/closure logs" — `python3 -m core.selftest`
- **Vision (prediction, not result):** "Systems with Gap Detector + Closure Policy resolve repeated queries in fewer turns than stateless baselines"
- **Vision (unbuilt):** Right-hand column — grounded drives once hardware supplies real variables

v0.1 loop wires **no language model**. LLM Core is injected callable, default = deterministic stub.

### Quickstart
```bash
python3 -m core.selftest
python3 -m pytest tests -q
python3 examples/01_repeated_query.py
python3 examples/02_gap_reopens.py
git diff --stat examples/logs/   # must be empty
```

Licence: CC BY-NC-ND 4.0 — All rights reserved.

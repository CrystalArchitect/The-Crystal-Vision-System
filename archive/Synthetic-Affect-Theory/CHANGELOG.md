# Changelog

## v0.3.3 — 25 August 2026

Prospective Other on Extract. Filling the chair is operating a person. **FM-Extract** (`reason: prospective`).

## v0.3.2 — 25 August 2026

Named Homage Rule. **FM-Homage**.

Do not absorb a named ancestor as self. Do not police who may dance.

## v0.3.1 — 25 August 2026

Ascribed Appraisal Rule (Unconsented Mirror). **FM-Mirror**.

The system does not declare the operator's value, beauty, or identity.
A self-model gap is signal, not a hole to fill.

## v0.3.0 — 25 August 2026

Host adapter. Wrap one model turn in `evaluate_cycle`.

- `core/host.py` — `wrap_turn`. Model is not called unless allowed. Inspect always returned.
- README hero: not Emotion AI, not a lab constitution, not a chip.

## v0.2.4 — 25 August 2026

Starline Arsenal audit of the stack (13 models). Docs only.

## v0.2.3 — 25 August 2026

Prior-art inventory. Docs only. No new runtime.

- [docs/spec/PRIOR-ART.md](docs/spec/PRIOR-ART.md) — what already ships; what SAT must not rebuild

## v0.2.2 — 25 August 2026

Stochastic Substrate Rule.

- Probabilistic hardware is a local instrument, not a hide
- Inspectable trace + provenance required for samples that affect regulation
- Remote sampling is a packet; isolation keeps it on-node
- **FM-Opaque-Sample**
- Spec: [docs/spec/STOCHASTIC-SUBSTRATE.md](docs/spec/STOCHASTIC-SUBSTRATE.md)

## v0.2.1 — 25 August 2026

Sovereignty pair: exemption and extraction.

- Exception Non-Grant — no carve-out from gates, consent, review, or Frame. `revise_prior` is authorship. “Only” flags High-Valence, does not exempt. **FM-Exception**
- Non-Extraction — fluency is not a licence. Asymmetric stake + rising fluency without a token, or `operate_person`, is **FM-Extract**
- Cycle: gates → valence → isolation → policy → packets
- Spec: [docs/sovereignty/EXCEPTION-EXTRACT.md](docs/sovereignty/EXCEPTION-EXTRACT.md)

## v0.2.0 — 24 August 2026

Ontology: eleventh dimension.

- **Prediction Error Magnitude (PEM)** — inspectable allostatic signal
- `core/pe.py` — local aggregate over v0.1 dimensions; PEM is not an input to itself
- `LocalAffectState.ingest_local_pe` — diagnostics in `inspect()`, aggregate in `values`
- High PEM may fire **P4** (defer / intervals). It does not pick, packet, enter a DUR, or speak as the operator
- v0.1 ten-dimension set remains `V0_1_IDS`. Tag `v0.1` unchanged

## v0.1.3 — 24 August 2026

Dead or untrusted network: fail closed.

- `docs/spec/ISOLATION.md` — FM-ISO-LINK, UNTRUSTED, FAIL-OPEN, PHONE-HOME
- `core/isolation.py` — local core continues; all packets stay home; phone-home and cloud-required blocked
- Isolation implies Restricted Mode. Tokens do not create a pipe.
- Cycle order: gates → isolation → policy → packet isolation → consent

PEM remains v0.2.

## v0.1.2 — 24 August 2026

Sovereign edge, on the cycle.

- `docs/spec/SOVEREIGN-EDGE.md` — local-first, operator veto, isolation
- `core/consent.py` — live matching token required; absence / expiry / revoke / purpose / destination / dimension all deny
- Packets cannot outrank P1
- Restricted Mode blocks rich transmission even with a token; capacity and hard-alert may still leave
- `evaluate_cycle` order: gates → policy → consent (packets only)

PEM is not in this release. That remains v0.2.

## v0.1.1 — 24 August 2026

Build after freeze. Tag `v0.1` is unchanged.

- `core/ontology.py` — ten frozen dimensions as code
- `core/local_state.py` — inspectable LocalAffectState, unknown keys rejected, no hidden fields
- `core/policies.py` — P1–P10 executable sketch; first match runs; P9 never picks
- `core/cycle.py` — sovereignty gates, then ordinary policy; gates skip policy on fail

Does not change Ontology v0.1, gate order, or the commercial schedule.

## v0.1.0 — 24 August 2026

Frozen snapshot. Tag `v0.1`.

### In this release

- **Science stack** — Gap Detector + Closure Policy; four postulates; scripted harness (loop 5/6 vs best task-agnostic stateless 2/6, 2026-08-14). CrystalCode primitives.
- **Constitution** — statement, eight principles, stance, invariants.
- **Ontology v0.1** — ten dimensions. Prediction Error Magnitude scheduled for v0.2 only.
- **Policy Library** — P1–P10 in fixed interrupt order.
- **Lattice + consent** — four layers, default-zero transmission, token fields, absence = denial.
- **Starline techniques** — seven; intensity permitted, fusion not.
- **Addendum A** — verification, FM1–FM8 plus sovereignty FMs, timers, commands, Restricted Mode, SECP.
- **Addendum B** — long-horizon continuity, identity postures, episode, transient, collective.
- **Sovereignty Layer** — DUR, Agency Non-Transfer, Transformation Vector, Intrusion Protocol, Authored Escape.
- **MVP monitor** — `core/sovereignty.py`, four gates in order. 47 tests passing at freeze.
- **Commercial grant** — AUD 12,000 initial; monthly greater of 8% net or AUD 250; audit via monthly certificate + annual desk check. CC BY-NC-ND 4.0 for non-commercial reading.

### Frozen

Ontology ten-dimension core · P1–P10 order · four-gate sequence · commercial schedule as of this tag.

### Not in this release (specified, not executable)

Full P1–P10 runtime · starline verification monitor · ledger cadence · Ontology v0.2.

### After this tag

Work continues on `main`. Breaking changes to frozen items require v0.2.

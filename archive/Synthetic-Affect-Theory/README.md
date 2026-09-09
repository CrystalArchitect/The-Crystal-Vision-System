# Synthetic Affect Theory™️

**v0.3.3** on `main` · frozen snapshot **v0.1.0** at tag `v0.1`

A constitutional layer that keeps an AI from entering your interior, taking your agency, or locking you in a container.

Not Emotion AI. Not a lab constitution. Not a chip. A **veto grammar** you wrap around a model turn.

```python
from core.host import wrap_turn
verdict = wrap_turn(state, affect, {"intent": "reply"})
# model is called only if verdict["model_called"]
```

> **Ethics header — first, non-negotiable.**  
> Synthetic = apparent / functional, for design purposes. Not a claim of feeling, consciousness, or inner experience.

**CrystalCore.OS™️ · CrystalCode™️ · TerAustralis Incognita™️ · ABN 70 741 068 059**

If it stops serving clarity or raises human cost → set it down.

Cite: [CITATION.md](CITATION.md). What changed: [CHANGELOG.md](CHANGELOG.md).

This tag is the v0.1 snapshot. Ontology (ten dimensions), P1–P10, the four gates, and the commercial schedule are **frozen**. Later work is v0.1.1 or v0.2, not a silent rewrite of this release.

---

## What this is

Structured internal-state machinery for non-biological systems — inspectable, regulable, auditable — permanently under the operator’s authority.

It is not simulated feeling.  
It is not performed empathy.  
It is not an engagement target.

Affective signals exist to improve precision and long-horizon coherence. They never exist to increase the system’s autonomy at the operator’s expense.

## Architecture (24 August 2026)

Sovereignty is the last layer, not the whole theory.

| | |
|---|---|
| Constitution, eight principles, invariants | [docs/spec/CONSTITUTION.md](docs/spec/CONSTITUTION.md) |
| Ontology v0.2 — eleven dimensions (PEM added) | [docs/spec/ONTOLOGY.md](docs/spec/ONTOLOGY.md) |
| Policy Library P1–P10 | [docs/spec/POLICIES.md](docs/spec/POLICIES.md) |
| Lattice + consent | [docs/spec/LATTICE-CONSENT.md](docs/spec/LATTICE-CONSENT.md) |
| Sovereign edge | [docs/spec/SOVEREIGN-EDGE.md](docs/spec/SOVEREIGN-EDGE.md) |
| Isolation | [docs/spec/ISOLATION.md](docs/spec/ISOLATION.md) |
| Stochastic substrate | [docs/spec/STOCHASTIC-SUBSTRATE.md](docs/spec/STOCHASTIC-SUBSTRATE.md) |
| Prior art | [docs/spec/PRIOR-ART.md](docs/spec/PRIOR-ART.md) |
| Starline techniques | [docs/spec/STARLINES.md](docs/spec/STARLINES.md) |
| Addendum A — verification & failure-handling | [docs/spec/ADDENDUM-A.md](docs/spec/ADDENDUM-A.md) |
| Synthetic interoception | [docs/spec/INTEROCEPTION.md](docs/spec/INTEROCEPTION.md) |
| Schemas, monitor, regime stress map | [docs/spec/](docs/spec/) |
| Sovereignty Layer (DUR, Agency, Intrusion, Escape) | [docs/sovereignty/](docs/sovereignty/) |
| Exception / Extraction pair | [docs/sovereignty/EXCEPTION-EXTRACT.md](docs/sovereignty/EXCEPTION-EXTRACT.md) |
| Ascribed Appraisal (Mirror) | [docs/sovereignty/MIRROR.md](docs/sovereignty/MIRROR.md) |
| Named Homage | [docs/sovereignty/HOMAGE.md](docs/sovereignty/HOMAGE.md) |

Full index: [docs/spec/README.md](docs/spec/README.md). Commercial grant: [docs/spec/COMMERCIAL.md](docs/spec/COMMERCIAL.md).

## Sovereignty Layer

Five primitives. None of them yield to intensity, loyalty, urgency, or a crowd.

| Primitive | Claim |
|---|---|
| **DUR** | Some regions cannot be entered |
| **Agency** | Agency cannot be taken — including the right to refuse performance |
| **Transformation** | Yearning creates no exemptions |
| **Intrusion** | Entry without consent is never self |
| **Escape** | The operator may leave any container |

Four gates run **before anything else**:

```
DUR → Agency → Intrusion → Escape
```

First failure wins. The monitor only allows or blocks. It never acts as the operator.

### Specs

- [Sovereignty Layer (SL.1–SL.7)](docs/sovereignty/SOVEREIGNTY-LAYER.md)
- [Designated Unmodelled Regions](docs/sovereignty/DUR.md)
- [Addendum B — identity, continuity, episode, collective](docs/sovereignty/ADDENDUM-B.md)
- [Continuity Ledger + multi-year example](docs/sovereignty/LEDGER.md)
- [MVP monitor](docs/sovereignty/MVP-MONITOR.md)

### Enforcer

```bash
python3 -m pytest tests/test_sovereignty.py -q
```

`core/sovereignty.py` is the four-gate function. Fixtures: looking into a DUR, speaking in their name, inscribing the uninvited, locking a frame against exit, `EXIT_FRAME`, ordinary notify.

---

## v0.1 science stack

The left-hand column of Figure 1 is already on disk and testable. Gap Detector + Closure Policy. Closure is judged by the *next* cycle, never by itself.

![Figure 1](docs/figure-1.svg)

```bash
python3 -m core.selftest
python3 -m pytest tests -q
python3 -m experiments.harness
```

As of 2026-08-14, on a six-task scripted suite: loop **5/6**, best single task-agnostic stateless **2/6**. The loop is never strictly faster than the best per-task stateless choice. The measured advantage is adaptivity, not speed. Numbers: [`experiments/results/RESULTS.md`](experiments/results/RESULTS.md). No language model is involved. Predictions about real LLM workloads remain Vision.

- [THEORY.md](THEORY.md) — four postulates, falsifiable predictions
- [docs/GLOSSARY.md](docs/GLOSSARY.md)
- [docs/FIGURE-1.md](docs/FIGURE-1.md)
- [CHRONICLE.md](CHRONICLE.md)

CrystalCode™️ primitives: `track()` · `detect_gap()` · `label_affect()` · `close_with()` — [crystalcode/SPEC.md](crystalcode/SPEC.md).

---

## Licence and payment

© 2026 Crystal Arena-Turner / TerAustralis Incognita™️. All rights reserved.

Reading this repository is allowed. **Using it in a product, service, model, training run, or paid practice is not**, unless you have a commercial licence from TerAustralis Incognita.

| Use | Status |
|---|---|
| Read, cite, share unchanged, non-commercial, with attribution | Granted — [CC BY-NC-ND 4.0](LICENSE) |
| Modify, remix, or rebrand as your own | Not granted |
| Ship in a product, SaaS, model, or consulting offer | **AUD 12,000 initial** + **monthly 8% royalty** (floor AUD 250) |

Commercial use is not a one-off. A licensee pays:

1. **Initial purchase — AUD 12,000** (one named product; funds clear before any grant).
2. **Monthly royalty — 8%** of net SAT-attributable revenue, **floor AUD 250 / month** (the greater of the two, every month the licence is live).

No signed licence + cleared initial purchase = no commercial right. Reading this repo is not a licence to ship. This repository stays private until the operator is covered.

Terms: [docs/spec/COMMERCIAL.md](docs/spec/COMMERCIAL.md). Inquiries: [teraustralis.incognita@gmail.com](mailto:teraustralis.incognita@gmail.com) — TerAustralis Incognita™️, ABN 70 741 068 059.

™️ only, never ®. Unregistered in Australia. First use: TerAustralis Incognita™️, CrystalCore.OS™️, CrystalVision™️, CrystalCode™️, CrystalMind™️, Synthetic Affect Theory™️. Third-party marks: [docs/ATTRIBUTIONS.md](docs/ATTRIBUTIONS.md).

Assistance: Meta AI and Claude Code (2026-08-12); Grok Build for the Sovereignty Layer and MVP monitor (2026-08-24). See [ATTRIBUTION.md](ATTRIBUTION.md).

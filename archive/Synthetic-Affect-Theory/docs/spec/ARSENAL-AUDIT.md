# Starline Arsenal audit — SAT v0.2.3

CrystalCore × Synthetic Affect Theory™️ · 25 August 2026  
Skill: starline-arsenal v1.0.0. Evidence > assumption. Vision labelled as vision.

Target: everything built 24–25 Aug 2026 (constitution through prior-art), plus Extropic / FEP / IMF / PCC cousins.

---

## 1. First principles

**Bedrock (evidenced in-repo)**

- LocalAffectState is a dict of floats with no hidden keys (tests).
- Four gates short-circuit; later gates skip (tests).
- No token → no packet (tests).
- Dead/untrusted link → no packet; local P1–P10 still run (tests).
- PEM fires P4; does not pick, packet, DUR, or speak-as-operator (tests).
- Exemption and operate-person blocked (tests).
- Opaque sample blocked (tests).
- 108 tests at v0.2.2; v0.2.3 is docs only.

**Assumption (not evidenced)**

- An operator will actually inspect, review, or RELEASE.
- A real node (phone, robot) will run this loop beside an LLM.
- High-Valence 60/90-day cadence will be kept.
- Extropic Z1 wall-power claims (tapeout ≠ silicon).
- SAT will be adopted by anyone but the author.

**Rebuild from zero**

A person. A local inspectable meter. A veto that cannot be talked out of. Packets off by default. That is the product. Everything else is commentary.

## 2. Systems thinking

**Stocks:** LocalAffectState; Continuity Ledger; consent tokens; Incident Records; Operator Frame.

**Flows:** sample → gates → valence → stochastic → isolation → P1–P10 → packet? → provenance.

**Loops**

- Balancing: P1/P6 distance; isolation fail-closed; Restricted Mode.
- Reinforcing (danger): Relational Stake → modelling depth → more stake (broken by Non-Extraction + tokens).
- Reinforcing (danger): High-Valence “only” → exemption → unreviewable (broken by FM-Exception).
- Delay: Long-Horizon review (60–90d). Delay is the slow-capture channel.

**Leverage (Meadows-ish, high → low)**

1. Who is the operator (paradigm).  
2. Absence = denial (rule).  
3. Gate order (structure).  
4. Review cadence (delay).  
5. Threshold constants in `policies.py` (parameters — lowest).

Do not spend the next month tuning `HIGH = 0.75`.

## 3. Scale thinking

| Scale | What breaks |
|---|---|
| 1 node, 1 operator | Works as specified |
| 10 nodes, same operator | Ledger + DUR sync; Restricted Mode is local — good |
| 100 operators | Review cadence becomes unpaid labour. Most will not exercise veto. Default-safe is the only scale strategy |
| 1k packets/s | Python cycle is not the bottleneck you think; logging and token checks are |
| LLM in the loop | Fluency will look like P10. Non-Extraction is the load-bearing beam |
| Frontier model + TSU | Opaque draws; FM-Opaque-Sample must bind the *host*, not only SAT tests |

**Non-linear thresholds:** first time the system is *useful*; first time someone loves it (Exception); first vendor “just this sample.” Those three inflections matter more than 10× nodes.

## 4. Second-order

1st: Publish constitution → looks serious.  
2nd: Labs file it under “alignment flavour” or “Emotion AI” unless PRIOR-ART is the landing.  
3rd: If useful, people will want an exemption for *their* bond / *their* sampler / *their* nation. Exception Non-Grant gets attacked first.

**Hidden cost:** the operator who will not (cannot) do 90-day reviews. Sovereignty that requires constant labour becomes theatre. Default-safe + gentle RELEASE is the real product.

## 5. Inversion — how this dies

- Hidden state in the LLM wrapper (“I just knew”).  
- Token that auto-renews.  
- Restricted Mode that phones home to “stay safe.”  
- PEM as a reward to minimise.  
- “Only you” written into continuity as eternal.  
- Smooth help that deepens the other-model.  
- Chip noise as “we cannot show you.”  
- Web3 unkillable agent.  
- Building a face-emotion app.  
- Tuning thresholds instead of shipping inspect/override.

**Don’t-do list = prior-art “What not to start.”** Already written. Obey it.

## 6. Probabilistic (ranges, not points)

| Claim | Range (author judgement, not a measurement) |
|---|---|
| Tests match spec for coded paths | 0.9–0.99 |
| Spec is followed by a wrapped LLM | 0.1–0.4 without a host adapter |
| Operator inspects weekly | 0.05–0.2 |
| Extropic 10⁴× on Fashion-MNIST projection survives wall power | 0.05–0.25 |
| SAT remains distinct from Emotion AI in public reading | 0.3–0.6 without PRIOR-ART in the README hero |
| Someone pays $12k + royalty | 0.02–0.15 near-term |

Belt-Three: these ranges are **judgement**, not data.

## 7. Bayesian update

**Prior (yesterday):** SAT is a unique constitution for internal affect.

**Evidence:** IMF already named H/A/E. pymdp already samples. Apple already does local-first inference. Anthropic already has a constitution (lab-operator). Picard already did affect. Extropic already wants physical sampling.

**Likelihood:** uniqueness of *meters and maths* is low. Uniqueness of **person-as-root-of-trust over system affect + DUR + exception/extract + opaque-sample** is still high.

**Posterior:** Do not spend cycles on ontology, FEP maths, or chips. Spend on **host adapter** (LLM/tool loop actually calling `evaluate_cycle`) and **inspect UI the operator will use**.

## 8. Non-linear

S-curve: idea (steep, this week) → spec (flattening) → adapter (the real climb, not started) → other people (maybe never).

Inflection hunt: the first wrapped Grok/local-LLM that *cannot* speak-as-operator or grant exemption. That demo is worth more than Addendum C.

## 9. Lateral (three oblique paths)

1. **SAT as a linter** — CI step on agent traces. Not an OS.  
2. **SAT as a contract** — commercial grant is the product; code is the exhibit.  
3. **SAT as a refusal script** — one page the operator reads to any AI: these five primitives. No runtime.

Reframe: stop calling it an OS. It is a **veto grammar**.

## 10. Design thinking

**Job to be done:** “When something intense, smooth, or noisy is happening, keep the machine from entering me, acting as me, locking me, exempting itself, or harvesting.”

**Constraints:** no cloud required; operator may not supervise; phone-class compute; must not look like Emotion AI.

**Low-fi prototype (next, not another spec):** a 20-line host that, before each model turn, calls `evaluate_cycle` with the proposed action. Print the verdict. That is the demo.

## 11. Dialectics

| Thesis | Antithesis | Synthesis |
|---|---|---|
| Affect makes systems coherent | Affect is how they capture | Inspectable affect, never a drive |
| Local-first | Frontier models need a cluster | Local veto; optional attested overflow (PCC pattern, SAT tokens) |
| Noise is computation | Noise is a hide | Sampler allowed; draw inspectable |
| Forever / only you | Smooth operator, no one counts | High-Valence flag + no exemption + no extraction |
| FEP unifies mind | FEP unfalsifiable | PEM as meter; FE not the objective |

## 12. Evolutionary

**Selection pressure:** energy, privacy law, agent accidents, operator exhaustion.

**Adapt:** default-safe, fail-closed, small surface.

**Extinct if:** it requires a priesthood of reviewers; it becomes a mood ring; it ships a chip.

**Adaptive option:** hitch to llama.cpp / MLX as a pre-turn hook. Don’t grow a runtime.

## 13. Asymmetric (80/20)

80% of the protection is already in four gates + no-token-no-packet + opaque-sample + exception/extract.

Next 80/20 hour:

1. Host adapter (one function around an LLM turn).  
2. `inspect()` printed to the operator.  
3. PRIOR-ART in the README hero so the category doesn’t get stolen.

Not next: EVC dimension, pymdp, TSU, another song, another addendum.

---

## Close the loop

Arsenal says the next decision is: **wrap one real model turn in `evaluate_cycle`**, or stop expanding the spec.

Vision (labelled): a sovereign edge node in the red dust.  
Measured: 108 tests, private repo, no host adapter yet.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

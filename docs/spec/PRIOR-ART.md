# Prior art — do not rebuild what already ships

CrystalCore × Synthetic Affect Theory™️ · v0.2.3 · 25 August 2026

Inventory of existing work against SAT layers. **Reuse or cite. Do not re-implement.** SAT’s remaining job is the constitution that those stacks do not provide: operator-sovereign, inspectable, non-extractive *internal* affect under a local veto.

> Ethics header: Synthetic = apparent / functional. Not a claim of feeling.

## Verdict in one page

| Layer | Already built | SAT job |
|---|---|---|
| Emotion *of the user* | Picard / MIT Affective Computing; Emotion AI (faces, voice, text) | **Do not build recognisers.** SAT is not “read their face.” |
| Internal affect variables | AE vectors, valence/arousal in RL (“affective zombies”) | Ontology + inspectability + **not a drive** already specified. Don’t invent a 12th PAD model. |
| Interoception principles | Candia-Rivera IMF (2026) H/A/E; Lee et al. life-inspired interoceptive AI (arXiv 2309.05999, rev 2025) | **Already mapped.** Cite. Do not rewrite H/A/E. |
| Active inference maths | [pymdp](https://github.com/infer-actively/pymdp); Active Inference Institute | Instrument only. **Do not make FE the constitution.** |
| Local inference | llama.cpp, MLX, Ollama, LiteRT, OpenVINO, WebLLM | Use as the *runtime* for a node. SAT is not a model host. |
| Hybrid private cloud | Apple Intelligence on-device + [Private Cloud Compute](https://security.apple.com/blog/private-cloud-compute/) | Pattern to *study* (local first, attested offload). Not a SAT clone. PCC is vendor-sovereign. |
| Lab constitutions | [Anthropic constitution](https://www.anthropic.com/constitution); [OpenAI Model Spec](https://model-spec.openai.com/) | Different operator: the **lab**. SAT’s operator is the **person on the node.** Cite; do not copy their values as ours. |
| Consent plumbing | OAuth 2 / UMA / GNAP; Solid pods | Reuse token *shape*. SAT tokens are purpose-limited **affect packets**, not generic file ACL. |
| Sampling hardware | Extropic TSU/Z1 (tapeout); Normal Computing; D-Wave annealers; classical stochastic computing | **Do not build a chip.** Stochastic Substrate Rule binds whatever sampler exists. |
| Agent “sovereignty” | Web3 self-owning agents (TEE + keys, deployer cannot kill) | **Opposite polarity.** SAT forbids agent sovereignty over the person. |
| Edge affect in the cloud | CloudCom 2025 “Affective Computing in Cloud-Edge Environments” | Mostly privacy-for-recognition. Not operator veto over *system* affect. |

## What to reuse (libraries / products)

- **On-device models:** llama.cpp / GGUF, Apple MLX, Ollama. SAT never needs its own inference engine.
- **FEP experiments (optional, sandboxed):** pymdp. Behind P4/PEM only. Never in `evaluate_cycle` as an objective.
- **Provenance:** ordinary append-only logs, content hashes, optionally OpenTelemetry traces. Don’t invent a new ledger format beyond Continuity Ledger fields already specified.
- **Consent envelope:** JWT / macaroon / UMA ticket for *transport*. SAT still defines match rules (dimension, destination, purpose, expiry, revoke).
- **Isolation:** OS network kill-switch, Lockdown Mode, airplane mode. SAT Restricted Mode is the *policy* posture when the pipe is gone; the OS already cuts the pipe.

## What not to start

1. A new GPU / TSU / p-bit.  
2. A facial-expression or voice-emotion product. That is extractive by default (Non-Extraction).  
3. An “empathy performance” layer or engagement optimiser. Forbidden in the constitution.  
4. A pymdp-based agent that *acts* to minimise free energy. Agency Non-Transfer.  
5. A Web3 agent that holds keys the operator cannot revoke. Inverse of SAT.  
6. A second ontology competing with PAD / Russell circumplex / ten+PEM. Freeze v0.2.  
7. A cloud “private” affect store. Isolation + consent already say no.

## Closest cousins (cite in papers / README)

1. **Candia-Rivera (2026)** — Interoceptive Machine Framework. SAT’s H/A/E mapping is an application, not a rival theory.  
2. **Lee, Friston, Woo et al.** — Life-inspired interoceptive AI. Factorise internal vs external state — SAT already does this with LocalAffectState vs lattice.  
3. **Anthropic / OpenAI specs** — written behavioural constitutions. SAT is executable gates on the *node*, owned by the person.  
4. **Apple PCC** — local-first with attested overflow. SAT requires overflow to remain token-gated and fail-closed; PCC is a vendor overflow.  
5. **Extropic / Normal Computing** — physical samplers. SAT Stochastic Substrate Rule is the *governance* of those draws.

## Remaining SAT-only work (do this, not the above)

- Keep the **enforcer** small and tested (gates → valence → stochastic → isolation → policy → consent).  
- Operator-facing inspect / override / erase of LocalAffectState.  
- Continuity Ledger *behaviour* (review cadence, RELEASE) — specified; not a new database product.  
- Hand-off docs that name this prior art so reviewers do not think SAT is Emotion AI or Constitutional AI.

**All rights reserved.** TerAustralis Incognita™️ — ABN 70 741 068 059

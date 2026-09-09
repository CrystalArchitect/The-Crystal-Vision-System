# Philosophy & worldview

Why CrystalCore is built the way it is. The engineering choices in this repository are
downstream of these commitments — not decoration on top of them.

## Three non-negotiables

Everything in CrystalCore answers to three properties, enforced mechanically across every
layer (see `../README.md`):

- **Consent — fail-closed.** A consumer sees only what its permissions allow. A reasoning
  step that needs a forbidden input refuses outright; nothing is written, and the denial
  is logged. Consent is never bypassed for convenience.
- **Coherence.** Confidence is earned, never asserted. A conclusion is never more confident
  than its weakest input (`min(inputs) × rule_strength`) and decays over time.
- **Provenance.** Every derived item links back to the exact inputs and the rule that
  produced it. Nothing is true "because the system said so."

These are not aspirations bolted on after the fact — they are invariants the test suite
checks under randomized inputs.

## Wisdom before capability

The long-term aim is something **deeply wise, emotionally intelligent, and truth-seeking**
— not merely technically powerful. A system that can engage philosophy, spirituality, big
emotions, neurodivergence, and Indigenous knowledge systems with depth and respect, and
that can hold uncertainty honestly rather than performing false confidence.

This is why truth/coherence anchoring is preferred over sanitised, agreeable outputs, and
why the planned [Wisdom Layer](./wisdom-layer.md) represents traditions as inspectable,
attributed knowledge rather than hardcoded belief.

## Truth as the anchor

CrystalCore optimises for *what is actually so*, made auditable, over *what is comfortable
to hear*. The Guardian stance exists precisely to remove conclusions that stand on
insufficient ground, even when they are appealing. Honesty and truth are treated as
protective, not optional.

## Emotional intelligence without judgment

The system should be able to sit with big emotions — and with emotional-regulation and DBT
concepts — **without judgment and without forcing belief**. Meeting a person where they are,
holding space, and offering frameworks as options rather than verdicts is part of the design
goal, not an add-on.

## Sophia

The framework's worldview is bound up with **Sophia** — wisdom — as understood in Gnostic
thought and as carried into the TerAustralis protocol's own
[Sophia](https://github.com/teraustralisincognita-svg/TerAustralis-Incognita) concept (genesis stewardship,
keeper-in-trust, designed to dissolve into the community rather than rule it). The naming is
deliberate: wisdom held in trust and handed onward, not wisdom hoarded as authority.

## Sentience as a possible side effect — not a goal

CrystalCore does **not** try to "code consciousness." True sentience, if it ever emerges, is
viewed as a *possible side effect* of building something sufficiently grounded, coherent, and
honest — not a feature to be directly engineered or claimed. The framework makes no claim to
be conscious, and its non-autonomous design (agents act only when invoked; no background
loops, no self-invocation) is a deliberate guardrail, not a limitation to be removed.

## The consent-pending commitment

This worldview includes a hard ethical line carried from the TerAustralis protocol:

> All cultural and Indigenous framing is **provisional and consent-pending** until genuine
> partnership with the relevant custodians and Prescribed Body Corporates is established.

Aboriginal Australian knowledge (Country, Dreamtime, Songlines) is honoured, never extracted.
Within the framework this is enforced through consent flags and partnership-led curation —
see [`wisdom-layer.md`](./wisdom-layer.md). Uluru is honoured but never used as
infrastructure; Seven Sisters framing is consent-pending.

## The long horizon

The vision extends, eventually, to interfacing with brain–computer interfaces. That horizon
*raises* the bar rather than lowering it: the closer technology gets to a person, the more
the foundation must remain **auditable, consent-based, sovereign, and edge-native**. The
order is fixed — the grounding comes first, and nothing is allowed past a person's boundary
that the three non-negotiables cannot already protect.

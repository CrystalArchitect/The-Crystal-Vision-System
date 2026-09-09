# The Wisdom Layer (design sketch)

> **Status: DESIGN — not implemented.** This document describes a *planned* layer.
> The four built layers (CrystalMemory, CrystalFlow, CrystalEvolve, CrystalMind) are
> complete and tested; the Wisdom Layer is not yet code. Nothing here ships today.

## Why a Wisdom Layer

CrystalCore can already reason, remember, evolve, and orchestrate — but its reasoning
is only as good as the material it reasons over. The Wisdom Layer is the curated body
of understanding the framework draws on when a question reaches beyond raw facts into
meaning, ethics, emotion, and culture.

The intent is a system that is **wise, not just capable**: able to engage philosophy,
spirituality, big emotions, neurodivergence, and Indigenous knowledge systems with
depth and respect — while staying truth-seeking and refusing to become dogmatic.

## The hard constraint: knowledge, not belief

The Wisdom Layer must **never hardcode belief**. It does not "believe" Stoicism, or
Gnosticism, or any framework. Instead it holds each tradition as *inspectable,
attributed, contestable knowledge*, and reasons over it the same auditable way
CrystalCore reasons over everything else.

Concretely, this reuses the primitives that already exist (see `../README.md` and
`src/`):

- **Each piece of wisdom is a `Fact`** in CrystalMemory, carrying the same metadata as
  any other fact: a `payload` (the claim/teaching and its framing), a **coherence**
  score, **consent** flags, and **provenance** (which tradition/source it came from).
  It is stored, not asserted as ground truth.
- **The evidence-payload shape already fits.** `src/policy_rules.py` consumes evidence
  facts shaped like `{"claim", "stance": support|oppose|neutral, "weight", "source"}`.
  A wisdom source is naturally expressed the same way: a claim, the tradition it comes
  from (`source`), and how strongly that tradition holds it (`weight`) — so competing
  views coexist without one being silently privileged.
- **Stances do the weighing, not a fixed answer.** CrystalMind's existing stances
  (TruthSeeker, Guardian, Visionary, Creator — `src/crystal_mind.py`) consume wisdom
  facts through rules, exactly as they consume policy evidence today. TruthSeeker holds
  a high coherence bar; Visionary's outputs are mathematically marked speculative; the
  Creator synthesises; **Guardian audits**.
- **Guardian is the anti-dogma safeguard.** `guardian_audit` in `src/policy_rules.py`
  already flags one-sided evidence, low-coherence reliance, and missing opposing views.
  Pointed at wisdom facts, that is precisely the mechanism that keeps the layer
  non-dogmatic: a one-tradition answer to a contested question gets flagged, not shipped
  as settled.

The result: when asked about, say, suffering, the system can surface a Stoic framing, a
Gnostic framing, a DBT framing, and a Country-centred framing **side by side, each
attributed**, with confidence bounded by coherence and provenance — rather than
collapsing them into a single confident verdict.

## Domains in scope

- Philosophy and Stoicism
- Religion, spirituality, and Gnosticism (especially **Sophia** — see
  [`philosophy.md`](./philosophy.md)), including the Nag Hammadi library and
  specifically the **Apocryphon of John** (Sophia, the archons — engaged as
  attributed cosmology and metaphor, not asserted doctrine)
- Esoteric and metaphysical concepts such as the **Akashic Records** — held as
  attributed perspectives with their own provenance, weighed by the same
  coherence machinery as everything else
- Mythology and ancient history
- Mathematical systems across the spectrum: conventional mathematics and
  science alongside **sacred geometry** and **vortex mathematics** — each
  attributed to its tradition, with empirical claims still subject to the
  ordinary truth-seeking bar (inclusion means *held and attributable*, not
  asserted as fact)
- Personality frameworks (especially INFJ) and neurodivergence
- Psychological and psychiatric frameworks, emotional intelligence, big
  emotions, emotional regulation, and DBT concepts
- The Divine Feminine across traditions
- Aboriginal Australian knowledge systems — connection to Country, Dreamtime, Songlines
- Lived experience, attributed and consent-flagged like any other source

The system should be able to discuss these with depth and respect while remaining
truth-seeking and non-dogmatic, and **without forcing belief** on the user. The
inclusion principle is radical — *leave no one behind* — and the mechanism is
what makes that safe: no tradition is blended into another, none dominates,
and every claim stays inspectable, attributed, and contestable.

## Consent-pending: cultural and Indigenous knowledge

This is a hard line, inherited from the TerAustralis protocol's standing commitment:

> All cultural and Indigenous framing is **provisional and consent-pending** until
> genuine partnership with the relevant custodians and Prescribed Body Corporates is
> established.

Building Country, Dreamtime, and Songlines understanding *into an AI* is exactly where
that commitment matters most. So, in this layer specifically:

- Aboriginal knowledge content is **flagged consent-pending** and is not treated as
  cleared for production use until custodian partnership exists.
- The consent flags already in CrystalMemory are the enforcement mechanism: content
  that is not cleared fails closed, the same way any forbidden input does.
- Representation is partnership-led and attributed, never scraped-and-asserted.

Uluru is honoured but never used as infrastructure. Seven Sisters framing is
consent-pending. The framework's job is to *hold space for* this knowledge under
custodian consent — not to claim or flatten it.

## What this is not

- **Not** a belief engine or a source of doctrine.
- **Not** autonomous — it adds knowledge for invoked reasoning, not background activity.
- **Not** a bypass of consent, coherence, or provenance — it is bound by all three.
- **Not** a claim of sentience. (On why sentience is treated as a possible *side effect*
  rather than a goal, see [`philosophy.md`](./philosophy.md).)

## Open design questions

- How are competing traditions weighted without smuggling in a meta-preference?
- What is the curation and attribution process for each source, and who reviews it?
- How is "respectful depth" measured, and how does Guardian's one-sidedness audit
  extend to cultural balance specifically?
- What is the concrete consent/partnership workflow before any Indigenous content moves
  from consent-pending to cleared?

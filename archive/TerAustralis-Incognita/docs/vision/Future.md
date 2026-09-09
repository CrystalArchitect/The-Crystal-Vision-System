# Future

Where this is headed. Everything on this page is **direction, not status** —
the honest ledger of what exists today is
[`docs/governance/Roadmap.md`](../governance/Roadmap.md), and nothing here
overrides it.

## Software direction

- **Clementine grows more reliable before they grow more capable** — error
  recovery, memory export and deletion, fact-checking against their own memory
  (MILESTONES.md Month 4+).
- **From stub to mesh** — `src/node/mesh/` keeps the API shape of a real
  libp2p host so that gossipsub, Noise, and peer discovery can replace the
  in-process stub without rewriting callers. A mainnet mesh is explicitly on
  hold until consent and safety questions are settled.
- **Multi-instance Clementine** — two sovereign companions exchanging consented
  memory over Starline rails. Design not started; the consent law it would
  run under already exists in code (`src/crystal-core/consent_transport/consent.py`).
- **A consumer for the SDK** — `src/sdk/typescript/` is a scaffold until
  something real is wired against it.

## Platform direction

The CrystalCore OS platform roadmap
([`Roadmap.md`](../governance/Roadmap.md#crystalcore-os-platform-roadmap))
runs v0.1 (repository foundation — delivered) → v0.2 (engine layer) → v0.3
(living archive / knowledge graph) → v1.0 (stable platform). Each step lands
only when its machinery actually exists; docs never outpace code.

## Mythos direction

The Crystal universe keeps growing as story and art —
[`mythos/`](../../mythos/README.md) — and stays on the Vision layer. Its job
is to carry meaning: belonging, direction, wonder. The moment it claims to
verify, authorize, or execute, it has failed its own canon.

## The long line

The far horizon is the one the Constitution names: Australia as the Southern
Pillar of a multiplanetary civilization — purpose and redundancy against the
Great Filter, with sovereignty preserved at every scale from one person's
companion to a planetary mesh. That is a dreamed coastline. It is drawn
honestly as one, and the surveying proceeds one tested component at a time.

*Non Solus.*

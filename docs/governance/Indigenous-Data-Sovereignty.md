# Indigenous Data Sovereignty

**Status:** standing governance position. This page states how this project
engages — and refuses to engage — with Songlines and other Aboriginal and
Torres Strait Islander knowledge. It binds the mythos layer, the software, and
anything either produces.

The short form is already in the [Constitution](Constitution.md) (§5) and the
[Code of Conduct](../../CODE_OF_CONDUCT.md). This page is the reasoning behind
them.

## What Songlines are

Songlines — also called Dreaming tracks — are not metaphors and not stories in
the sense a novel is a story. They are living knowledge systems developed over
tens of thousands of years, functioning at once as:

- geographic and ecological maps
- legal and ethical frameworks
- astronomical and seasonal calendars
- social and kinship systems
- ceremonial and spiritual pathways

A Songline encodes water, food, safe passage, rights, responsibilities, and the
relationships between people, Country, and the more-than-human world. The
knowledge is relational, multi-modal, place-based and intergenerational. It is
transmitted through relationship and performance rather than stored as open
text. Some layers are public; others are gendered, age-restricted, or held by
specific custodians.

That last point is the one most easily lost: **restriction is not incidental to
the knowledge, it is part of its structure.**

## Why this is in tension with how AI is usually built

Most contemporary AI assumes extracted text at volume, openness and
scalability, disembodied and decontextualised information, and centralised
training and ownership.

Songlines run on close to the opposite premises — knowledge held in
relationship and performance, context and Country inseparable from the
information, access governed by law and kinship, and continuity rather than
prediction as the goal.

So "putting Songlines into AI" is not a feature request. Absent deep structural
change it is a description of extraction.

## The floor: Indigenous Data Sovereignty

The clearest Australian framework comes from **Maiam nayri Wingara**, the
Indigenous Data Sovereignty collective. Its principles hold that Aboriginal and
Torres Strait Islander peoples have the right to:

- govern the creation, collection, ownership and application of data about
  them, their knowledge and their lands
- ensure data serves Indigenous aspirations and self-determination
- require **Free, Prior and Informed Consent**
- protect cultural and intellectual property

Any engagement between this project and Songline knowledge starts here. Not
with technical enthusiasm, and not with what the architecture happens to make
possible.

## The risks, named

- **Extraction** — digitising restricted or sacred knowledge without authority.
- **Flattening** — reducing layered, performed knowledge to tokens or embeddings.
- **Misrepresentation** — models generating plausible but wrong or harmful
  versions of cultural material.
- **Loss of governance** — once knowledge enters a large model, control is
  extremely difficult to recover.
- **Cultural and spiritual harm** — treating a living system as content.

None of these are hypothetical. They are already happening to Indigenous
knowledge globally.

## What this project may build toward

A non-extractive posture points at architecture this project already favours:

- **Local-first and consent-based** — hold knowledge only with explicit,
  ongoing permission from the relevant custodians, and make revocation real.
  The consent-gated transport in the code repository
  (`core/crystal-core/consent_transport/` in TerAustralis-Incognita-Code) is
  the shape of this, not a claim to have solved it.
- **Relational rather than extractive memory** — prioritise relationship,
  place and responsibility over scale and prediction.
- **Layered access** — structures that can honour restriction, including
  knowledge that never enters the system at all.
- **Support for living practice** — assist documentation, language work or
  mapping *under the authority of knowledge holders*, never replacing or owning
  the knowledge.
- **Sovereign infrastructure** — edge and local systems are structurally more
  compatible with Indigenous data sovereignty than centralised models. That is
  an argument for the direction, not evidence the destination has been reached.

## The line this project holds

The framing is "Songlines to Starlines", and the honest question that framing
invites is whether the system serves the continuity of that knowledge under
Indigenous authority — or becomes another layer of mapping and control.

So the position is deliberately narrow:

> **Not AI that contains Songlines. AI infrastructure capable of respecting the
> laws that already govern them.**

Songlines appear in the mythos and the art as cultural image, honoured, never
claimed as a component name — see [`mythos/NAMES.md`](../../mythos/NAMES.md).
No Songline knowledge has been ingested into any model, dataset or index in
this repository, and none will be without Free, Prior and Informed Consent from
the relevant custodians. Where this project needs a name for something it
built, it coins its own: Starline, Dreamline, Lattice.

Songlines are not a dataset waiting to be ingested. They are living systems of
law, knowledge and relationship, and some of what they carry is simply not
available for technological mediation.

*Non Solus.*

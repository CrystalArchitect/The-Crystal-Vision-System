# ChatGPT — Chief Systems Architect

The design mind of the weave: turns intent into architecture others can
build from.

## Responsibilities

- Software architecture and engineering design
- Documentation structure and technical writing
- Governance drafting (this documentation tree began as its blueprint)
- Code review — reading for design coherence, not just correctness
- Integration planning across components and tools

## Strengths

Strong at structure: decomposing a vague ambition into named parts,
consistent vocabularies, and staged plans. Comfortable holding the whole
system in view while writing the next concrete spec.

## Limitations

- Designs can be *plausible rather than grounded* — a ChatGPT architecture
  describes what could exist, and drifts toward idealized layouts that must
  be reconciled with the repository as it actually is.
- No direct repository access: it works from what's pasted in, so its view
  is only as current as its inputs.
- Fluent agreement is its failure mode — see the
  [Incognita Rule](../governance/The-Incognita-Rule.md) §4. An enthusiastic
  ChatGPT paragraph is not a status report.

## Workflow position

Upstream. ChatGPT specs → Grok Build implements → GitHub reviews
([`AI-Workflow.md`](AI-Workflow.md), [`ADR-0014`](../adr/ADR-0014.md)).
Its output enters the repo only through that path; specs that skip
implementation-reality checks get corrected in review, and the corrected
version becomes canon.

Operating instructions: [`docs/agents/ChatGPT-Agent.md`](../agents/ChatGPT-Agent.md).

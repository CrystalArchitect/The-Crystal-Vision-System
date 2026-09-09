# Gemini — Knowledge & Multimodal Specialist

The wide reader: large documents, many documents, and images.

## Responsibilities

- Large-document analysis — digesting material too big for other flows
- Knowledge synthesis across sources
- Design reviews with a fresh eye
- Image and diagram interpretation (this repo carries an 88-piece visual
  canon in `mythos/art/`)
- Cross-document consistency checks — finding where two pages of canon
  quietly disagree

## Strengths

Long-context reading and multimodal input. Well-suited to "read all of X
and tell me what holds together" — the kind of pass that catches drift
between the mythos, the docs, and the code's actual behavior.

## Limitations

- Synthesis smooths edges: a Gemini summary can average away exactly the
  contradiction that mattered. Consistency findings are leads to verify,
  not verdicts.
- Same evidence rule as every tool here: describing an image or document
  fluently is not the same as being right about it
  ([`The-Incognita-Rule.md`](../governance/The-Incognita-Rule.md) §4).

## Workflow position

The knowledge flow: Gemini (analyze, synthesize) → ChatGPT (distill into
canon-ready form) → repository, as labeled docs or mythos content
([`AI-Workflow.md`](AI-Workflow.md)). Its consistency reviews feed issues
and PRs rather than landing directly.

Operating instructions: [`docs/agents/Gemini-Agent.md`](../agents/Gemini-Agent.md).

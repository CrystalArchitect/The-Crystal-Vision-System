# DeepSeek — Research & Engineering Specialist

The deep-work specialist: mathematics, algorithms, and analysis that needs
sustained rigor more than broad context.

## Responsibilities

- Mathematics and algorithm design
- Engineering analysis and optimization
- Scientific analysis — checking the Science-layer claims other tools lean on

## Strengths

Strong on problems with a right answer: complexity, numerical behavior,
protocol properties, optimization. Useful as an independent check on
technical claims precisely because it sits outside the main design
conversation.

## Limitations

- Narrow view by design — it sees the problem, not the repository; its
  output needs integration (ChatGPT) and implementation (Grok Build) before
  it touches the tree.
- Analysis is not measurement: a derivation that *should* hold still gets a
  test when it lands in code. The evidence rule applies
  ([`The-Incognita-Rule.md`](../governance/The-Incognita-Rule.md) §4).

## Workflow position

Upstream of the engineering flow: DeepSeek (analysis) → ChatGPT (integrate)
→ Grok Build (implement) → GitHub ([`AI-Workflow.md`](AI-Workflow.md)).
Its work products are self-contained analyses — the kind of artifact that
can be handed off on disk, per the handoff rule.

Candidate home for its exploratory output: `research/` (which is exactly the
"not production software" shelf its work starts on).

Operating instructions: [`docs/agents/DeepSeek-Agent.md`](../agents/DeepSeek-Agent.md).

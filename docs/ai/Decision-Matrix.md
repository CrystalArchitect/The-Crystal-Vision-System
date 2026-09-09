# AI decision matrix

Which AI to reach for, for a given kind of task. This is the first,
documentation-only increment of the **AI Orchestrator** concept
([`AI-Architecture.md`](AI-Architecture.md)): a human reads this table,
picks the recommended tool, and decides — no runtime, no automation, no new
failure mode. If it proves useful in practice, a coded version can route to
the same table later; until then, the table *is* the orchestrator.

Midstream seat as of 2026-08-20: Grok Build, not Claude
([`ADR-0014`](../adr/ADR-0014.md)).

## How to read this

- **Recommended AI** — who's best positioned by role and strength (see each
  tool's page in this folder). Not a rule: judgment beats the table when
  they disagree.
- **Human review** — **Required** means a human should read the output
  closely before it goes further, regardless of how confident the AI
  sounds (the [Incognita Rule](../governance/The-Incognita-Rule.md) §4: a
  model agreeing with you is not evidence). **Recommended** means the
  normal PR review already covers it — no extra scrutiny implied beyond
  that. Every row still goes through the ordinary review process
  ([`Review-Process.md`](../governance/Review-Process.md)); this column is
  about *how carefully*, not *whether*.
- **Multi-step tasks** — some rows are really a handoff, not one tool. The
  full sequences (who feeds whom) are in
  [`AI-Workflow.md`](AI-Workflow.md); this table names the tool that leads.

## The matrix

| Task | Recommended AI | Human review | Notes |
|---|---|---|---|
| Repository structure / multi-file refactor | Grok Build | Required | Verify against the real tree, not a remembered one — [`Grok.md`](Grok.md) §2 |
| New software architecture / system design | ChatGPT | Required | Specs can be plausible but ungrounded — check against repo reality before implementing |
| Documentation structure or drafting | ChatGPT → Grok Build | Required | ChatGPT drafts structure, Grok Build places and cross-links it across the tree |
| Mathematical modeling / algorithm design | DeepSeek | Required | Analysis, not measurement — gets a test when it lands in code |
| Large-document or corpus synthesis | Gemini | Recommended | Synthesis can smooth over a contradiction that mattered — treat findings as leads |
| Image / diagram interpretation | Gemini | Recommended | States what's depicted, kept separate from what it means |
| Cross-document consistency check | Gemini | Recommended | Findings are "X says A, Y says B," not verdicts, unless code settles it |
| Creative brainstorming / alternative framings | Grok | Recommended | Diverges on purpose — filtering is the next step, not this one |
| Mythos or art generation | Grok | Recommended | Cultural-respect boundaries apply in full — [`Grok-Agent.md`](../agents/Grok-Agent.md) §A |
| Bug fix / small, scoped code change | Grok Build | Recommended | Still a PR, still CI, still reviewed — just not extra scrutiny beyond that |
| Naming or responsibility decisions | ChatGPT → Grok Build | Required | Gets an ADR, not just a decision — [`Decision-Records.md`](../governance/Decision-Records.md) |
| New GitHub repository | ChatGPT → maintainer | Required | Default is **no**. Lands in an existing living repo unless a new ADR names why it cannot ([`ADR-0015`](../adr/ADR-0015.md)). Grok Build does not create repositories |

GitHub isn't a row here — it's not a competing option, it's where every row
ends up ([`GitHub.md`](GitHub.md)).

Claude is not a row here. The historical profile is [`Claude.md`](Claude.md).

## Using this before it's code

Point a task at this file the same way you'd point it at a person: read the
row, take the recommendation as a starting position, and let the human at
the end of the flow make the actual call — the same veto that governs
everything else in this project
([`AI-Governance.md`](../governance/AI-Governance.md)).

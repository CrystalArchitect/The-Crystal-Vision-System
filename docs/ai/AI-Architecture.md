# AI architecture — the whole picture

The pages in this folder each describe one tool. This page is the
assembly instructions: how the roles relate, what connects them today, and
what's proposed but not yet real. Read this first if you're new; read the
individual profiles for depth.

The midstream seat moved on 2026-08-20: see [`ADR-0014`](../adr/ADR-0014.md).

## The roles at a glance

| Tool | Role | One line |
|---|---|---|
| [ChatGPT](ChatGPT.md) | Chief Systems Architect | Turns intent into specs others can build from |
| [Grok Build](Grok.md) | Repository Engineer | Implements specs across the real tree, through PRs |
| [DeepSeek](DeepSeek.md) | Research & Engineering Specialist | Mathematics, algorithms, analysis with rigor |
| [Gemini](Gemini.md) | Knowledge & Multimodal Specialist | Reads wide — large documents, images, consistency |
| [Grok](Grok.md) | Creative Exploration | Diverges first; ideas and art, filtered later |
| [GitHub](GitHub.md) | Development Platform | Not an AI — where every flow ends and becomes canon |
| [Claude](Claude.md) | Repository Engineer (historical) | Held the midstream seat until 2026-08-20; retained as record |

Grok and Grok Build are two seats in one family, not one job. Mixing them
is how a session invents instead of implementing.

## How they connect today

Every arrow below is a **working agreement**, not enforced software — the
full flows (which tool feeds which, and in what order per kind of task) are
in [`AI-Workflow.md`](AI-Workflow.md). In outline:

```
   DeepSeek ─┐
             ▼
   Gemini ─▶ ChatGPT ─▶ Grok Build ─▶ GitHub ─▶ (merged: canon)
             ▲
   Grok ─────┘
```

ChatGPT is the hub every design-shaped flow passes through before Grok
Build touches the tree; GitHub is the hub every flow passes through before
anything counts. Nothing left of GitHub is canon on its own — see
[`AI-Workflow.md`](AI-Workflow.md#what-the-flows-mean-in-practice).

## What's actually enforced vs. practiced vs. proposed

Three different strengths of rule apply to "AI architecture" here, and
conflating them is the most common way a repo like this drifts into
overclaiming ([`The-Incognita-Rule.md`](../governance/The-Incognita-Rule.md)):

- **Enforced in code** — the Starline Weaver refuses unlabeled messages; the
  CrystalBridge gate fails closed. Detail:
  [`docs/architecture/AI-Weave.md`](../architecture/AI-Weave.md).
- **Practiced by convention** — the roles and flows on this page and in
  `AI-Workflow.md`. Nothing stops a contributor from skipping them; review
  is the only enforcement, per
  [`AI-Governance.md`](../governance/AI-Governance.md).
- **Proposed, not built** — see below.

## The AI Orchestrator concept

Raised in review (ChatGPT, 2026-07-23): rather than each tool being reached
independently, an **orchestrator** could sit in front of the roles and route
a task to whichever tool fits it. An earlier sketch of the same idea (an "AI
Router" module inside a proposed CrystalCore Engine) named the identical
responsibility twice — **consolidated to one name, AI Orchestrator**, per
[`ADR-0005`](../adr/ADR-0005.md).

The concept has two parts, one built and one deliberately not:

**Built today, docs-only:** [`Decision-Matrix.md`](Decision-Matrix.md) — a
table a human reads to get a recommendation. That table *is* the
orchestrator's first increment, not a placeholder for it: no runtime, no
automation, no new failure mode, and per ChatGPT's own framing, that's a
feature, not a gap to fill quickly.

**Not built, and not yet specified:** anything that runs this automatically.
The internal shape, if it's ever built, is:

```
Task
  │
  ▼
Capability Assessment   (what does this task actually need?)
  │
  ▼
Recommended AI          (today: a lookup in Decision-Matrix.md)
  │
  ▼
Human Review            (the veto stays here — always)
```

— which is *how* a request gets routed once it reaches the orchestrator,
distinct from the diagram above showing *what* it routes between.
This would be a real addition to the Lattice's designed-but-unbuilt
machinery ([`docs/architecture/Lattice.md`](../architecture/Lattice.md))
rather than a restatement of it: the Lattice's Weave Map registers nodes,
but doesn't route work between them. Automating the middle step is a future
decision, not a current one — it needs its own spec and its own ADR before
any code, the same sequence that produced the v1.0 architecture itself
([`docs/adr/ADR-0001.md`](../adr/ADR-0001.md)).

Until then, routing "which AI for this task" stays a human judgment call,
made by reading [`Decision-Matrix.md`](Decision-Matrix.md) and the full
flows in [`AI-Workflow.md`](AI-Workflow.md).

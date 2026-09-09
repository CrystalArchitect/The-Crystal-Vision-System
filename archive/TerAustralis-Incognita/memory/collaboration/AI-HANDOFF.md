# AI-HANDOFF — how work moves between AI tools

**Status:** Docs / governance. Summary only. Canonical source:
[`../../docs/ai/AI-Workflow.md`](../../docs/ai/AI-Workflow.md) and
[`ADR-0014`](../../docs/adr/ADR-0014.md). If this page and either of those
disagree, they win — fix this page.

## The two real seats (not a role table)

Only two things are actually named "seats" on disk. Do not invent others.

| Seat | Who | Does | Boundaries |
|---|---|---|---|
| **Repository Engineer** | Grok Build (xAI, repo-connected session) | Midstream implementer: takes a spec, makes the tree match it, opens a PR | No push to `main`, no history rewrite, no locked-name changes, no silent edits to another contributor's Vision-layer content, no merge. The maintainer merges. |
| **Creative Exploration** | Grok | Divergent ideas, mythos, art | Does not implement. Filtering happens downstream. |

**Claude's seat is historical, not current.** Claude held the Repository
Engineer role from the v1.0 reorg until 2026-08-20
([`ADR-0014`](../../docs/adr/ADR-0014.md)). Claude's profile stays on disk
as history ([`../../docs/ai/Claude.md`](../../docs/ai/Claude.md)); it is not
a live instruction. **A Claude Code session that runs anyway does not
restore that seat** — it follows root [`CLAUDE.md`](../../CLAUDE.md)'s
read-and-write memory protocol instead, which is a different job (session
memory and navigation, not repository implementation).

ChatGPT, DeepSeek, and Gemini appear in the flows below by the *function*
they perform in a given handoff (design, algorithms, synthesis) — the
workflow document does not name them as standing seats the way it names
Repository Engineer and Creative Exploration. Do not promote a flow role
into a seat title.

## The flows (from AI-Workflow.md)

```
Architecture:    ChatGPT (design, spec) → Grok Build (implement) → GitHub (PR, review)
Engineering:     DeepSeek (analysis) → ChatGPT (integrate) → Grok Build (implement) → GitHub
Documentation:   ChatGPT (structure, draft) → Grok Build (place across tree) → GitHub
Knowledge:       Gemini (large-doc synthesis) → ChatGPT (distill) → repository (labeled)
Brainstorming:   Grok (divergent) → ChatGPT (select, shape) → architecture (or discarded)
```

## Constraints that bind every flow

- Every flow **ends at the repository through a pull request** — no AI
  output is canon until the maintainer merges it.
- Skipping a flow step is fine for small work; **skipping review is never
  fine**.
- Handoffs happen through artifacts (spec, diff, doc) — the receiving tool
  works from what's on disk, not from a summary of a conversation.
- Every PR names the tools that touched it. Name **Grok Build**
  specifically when the implementer was Grok Build, not "Grok" (Creative
  Exploration is a different seat).
- Chaining AIs multiplies fluency, not truth. Each handoff re-checks
  Built/Vision labels. The human keeps the veto.

## Where this leaves a Claude Code session

If one runs anyway (this file's own origin), it is a guest, not the
engineer. Its job per [`CLAUDE.md`](../../CLAUDE.md): read durable memory,
work from disk canon, write back confirmed state — not implement across
the tree as if the seat were restored. See
[`CONTEXT-PACK.md`](CONTEXT-PACK.md) for session bootstrap specifics.

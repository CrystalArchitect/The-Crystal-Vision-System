# The AI Weave

How multiple AIs work together in this project — the part that is code, the
part that is practice, and the part that is design-not-yet-built. The three
must not be confused.

## Enforced in code (Built)

- **The Starline Weaver** (`src/crystal-core/bus/`) — the bus
  where AI agents actually converse. The Belt-Three law is enforced by the
  hub, not by convention: a message without a science/story/vision label is
  not heard. A red button halts every agent at once. Matrix mode fans one
  question out to every agent independently and counts agreement — a count,
  not a verdict (an echo is not a witness).
- **CrystalBridge** (`src/crystalcore/`) — the consent gate guest AIs pass
  through to reach Clementine: approval → permission → scope → provenance,
  fail-closed, append-only audit.
- **RDP** (`src/crystal-core/rdp/`) — when the Weaver runs a matrix, the
  result can be witnessed onto a tamper-evident chain. RDP records; it never
  decides.

## Practiced by humans and tools (Process)

The collaboration model — which AI does what kind of work, and in what
order — is documented in [`docs/ai/`](../ai/AI-Workflow.md), with a quick
task → tool lookup in [`Decision-Matrix.md`](../ai/Decision-Matrix.md) and
per-agent operating instructions in [`docs/agents/`](../agents/). It is a
working agreement, not software: nothing enforces it except review
discipline ([`AI-Governance.md`](../governance/AI-Governance.md)) and the
standing rule that every PR names the AI tools that helped produce it.

## Designed, never built (Vision)

The Constitution's weave law (§3) sketches a **Weave Map** (every AI node
registered), **Lattice deltas** (time-stamped memory of agent work), and a
**contradictions file**. None of this machinery exists — see the
Constitution's implementation note and [`Lattice.md`](Lattice.md). Until it
is built for real, agent work lands the ordinary way: a commit, honestly
labeled, through review.

## The one rule over all of it

From the [Incognita Rule](../governance/The-Incognita-Rule.md) §4: **a model
agreeing with you is not evidence.** The Weaver's cross-compare counts
agreement without calling it truth; the human collaboration model requires
the same discipline of its participants. Text a model generates about this
project is dreamed until surveyed ground — running, tested code, or a
checkable fact — says otherwise.

# Infrastructure & runtime topology

How and where CrystalCore runs, and how heavy work is offloaded without breaking the
sovereignty guarantee.

## The live system

The live CrystalCore system — reasoning, memory, and agents — runs **24/7 on a modest
always-on Linux server**, owned and administered by the project's infrastructure
steward.

Current server profile:

- Linux, running continuously (24/7)
- Modest CPU, **no GPU**
- Sized for websites, databases, and APIs — **not** for heavy model training or hosting
  large neural networks

This matches CrystalCore's design target exactly: the core is engineered for constrained
hardware (a small working set, no GPU, CPU-only reasoning), so a modest always-on server
is a natural home for the reason → remember → improve loop.

## Heavy training is offloaded — deliberately

CrystalEvolve's population-based training and evolutionary search are compute-heavy and
do not belong on the always-on server. They are offloaded:

- to a **separate GPU workstation** operated by the infrastructure steward, or
- to **Google Colab**,

with the server **calling out via an API key** when it needs a heavy training or
evolution run, then **bringing the improved version back** to run locally.

## The sovereignty boundary

This split is intentional and worth stating precisely, because it looks — at a glance —
like it tensions the "no cloud dependency" principle. It does not:

- **Core reasoning and memory always stay local.** CrystalMemory and CrystalFlow run on
  the sovereign server with no required network. The system reasons, remembers, and
  serves answers fully offline. This is the guarantee that must never be broken.
- **Only training *compute* may burst out.** Evolution is an *offline improvement step*,
  not part of the live reasoning path. Offloading it to a GPU box or Colab is a build-time
  optimisation; the result is a better genome that is then run locally.

So the principle holds in its exact wording — *no cloud dependency for core reasoning and
memory* — while still allowing heavy training to use more powerful hardware when needed.

```
   sovereign (always local)                burst (on demand, training only)
   ┌────────────────────────────┐          ┌──────────────────────────────┐
   │  Linux server (DK, 24/7)    │  API     │  GPU workstation  /  Colab    │
   │  CrystalMemory              │ ───────▶ │  CrystalEvolve heavy runs     │
   │  CrystalFlow (reasoning)    │ ◀─────── │  → improved genome returned   │
   │  CrystalMind (agents)       │  result  └──────────────────────────────┘
   └────────────────────────────┘
        live reasoning path:                  off-path improvement only —
        never leaves the server               never on the live answer path
```

## Roles

- The **infrastructure steward** handles infrastructure, deployment, server
  administration, and technical implementation, and is a collaborator on this
  repository.
- **Terminal access** to the server is via SSH when hands-on work is needed, guided by
  the infrastructure steward.

## Operational notes

The standalone-deployment guidance in [`../README.md`](../README.md) ("Deployment on
Raspberry Pi") applies to the server too: atomic, checksummed JSON persistence on the
most resilient writable mount, `get_stats()` for observability, and OS-level tooling
(`systemd` service, log rotation, a watchdog) for a long-running process.

## Long horizon

The same sovereignty boundary is the precondition for any future hardware integration,
including brain–computer interfaces: the foundation must stay **auditable, consent-based,
and edge-native** before anything is allowed closer to a person. See
[`philosophy.md`](./philosophy.md).

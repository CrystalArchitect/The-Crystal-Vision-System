# CrystalCore — the taxonomy

"CrystalCore" is the project's oldest and most overloaded name. This page is
the canonical taxonomy: the tree every use of the name should fit into, and
the rule for anything that doesn't yet exist. The naming decision itself is
recorded in [`ADR-0004`](../adr/ADR-0004.md).

## The tree

```
CrystalCore
│
├── CrystalCore Framework        the sovereign-companion engine (Clementine runs on it)
│
├── CrystalCore Protocol         the multi-agent protocol pack (Weaver, pipeline,
│                                Starline, RDP)
│
├── CrystalBridge                the integration layer (fail-closed guest-AI gate)
│
└── CrystalCore OS                the repository and governance platform itself
    │                             — AND, confusingly, also the mythos terminal
    └── (see "the one collision   (see the note below — this is the taxonomy's
         this taxonomy didn't      one unresolved case, kept honest rather
         resolve" below)           than papered over)
```

Three branches are running, tested code. The fourth — CrystalCore OS — is
not software at all; it's how the repository is organized and governed
(the tree you're reading right now is part of it).

## The map

| Canonical name | What it is | Layer | Where |
|---|---|---|---|
| **CrystalCore Framework** | The sovereign-companion engine Clementine runs on: brain, layered memory, profiles | Built | `core/crystalcore/mind/` |
| **CrystalCore Protocol** | Starline Weaver, Decode→Ingest→Twin pipeline, Starline, RDP record kernel | Built | `src/crystal-core/` |
| **CrystalBridge** | The MCP consent gate — a Python package that happens to also be named `crystalcore` | Built | `src/crystalcore/` |
| **CrystalCore OS** (platform) | This repository's organizational architecture — layout, docs tree, governance, AI collaboration model | Process | [`docs/architecture/SystemMap.md`](../architecture/SystemMap.md), [`ADR-0001`](../adr/ADR-0001.md) |
| **CrystalCore.OS** (mythos terminal) | The mythos as a terminal you can fly — a playable story, not an operating system | Vision | `src/crystalcore-os/crystalcore_os.py`, [`mythos/CRYSTALCORE-OS.md`](../../mythos/CRYSTALCORE-OS.md) |

Per the [Incognita Rule](../governance/The-Incognita-Rule.md), the mythos
terminal may *point at* the real components and say "that one is real"; it
never borrows their authority. And the platform, despite the "OS" in its
name, runs nothing — it organizes.

## The one collision this taxonomy didn't resolve

The platform (row 4) and the mythos terminal (row 5) are two genuinely
different things that ended up with almost the same name — exactly the
ambiguity this page exists to prevent, except this instance predates the
page. It's left as-is rather than silently merged or quietly renamed,
because:

- both names were already in use in shipped docs and code before this
  taxonomy existed (`mythos/CRYSTALCORE-OS.md` and this document's own
  ADR-0001 title both predate this page);
- the punctuation difference (`CrystalCore.OS` for the terminal,
  `CrystalCore OS` for the platform) is real but too subtle to lean on;
- renaming either one is a bigger, separate decision — not a side effect
  of writing a taxonomy page.

If one of them gets renamed later, it happens deliberately, with its own
ADR, the way the rule below asks of anything new.

## The rule for anything not yet on this tree

**A new runtime component does not become a fifth "CrystalCore."** It gets a
name that describes what it does. `ADR-0004` doesn't mandate a specific
name, but offers the shape: *Crystal Runtime*, *Crystal Nexus*, *Crystal
Coordinator*, *Crystal Kernel* — the exact word matters less than not
repeating this page's oldest mistake. The AI Orchestrator concept
([`docs/ai/AI-Architecture.md`](../ai/AI-Architecture.md)) follows this rule
already: it's named for its role, not folded into "CrystalCore" anything.

## Relationships between the built components

Covered in depth in [`docs/architecture/CrystalCore.md`](../architecture/CrystalCore.md)
("why three, not one"): the Framework, Protocol, and Bridge answer different
trust questions — one human trusted completely, many mutually-untrusting
agents, and outsiders let in through a gate that fails shut — and merging
them would blur exactly the boundaries the project exists to keep sharp.

The name itself is inspired by the ordered structures of crystallography:
building with clarity, stability, and user-defined structure.

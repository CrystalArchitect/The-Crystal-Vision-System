# Plain English Explainer

**Status:** Draft for [90-Day Public Roadmap deliverable #5](../../../memory/projects/90-Day-Roadmap/PLAN.md) (First-Principles Systems Thinking). Target: ~300 words, zero myth overlay, readable by an engineer with no context on this project's mythos.

**Source:** [`docs/architecture/crystal-core/ARCHITECTURE.md`](../../../docs/architecture/crystal-core/ARCHITECTURE.md) — this explainer translates that real, labeled Built/Vision architecture into plain terms. It adds no new claims and doesn't use this project's mythic names for the same system ("Sovereign Lattice," etc.) — those are a separate, explicitly-labeled Story/Vision-layer document (`mythos/content/THE-SOVEREIGN-KEY.md`), not this one.

---

## What this project is actually building

A personal AI companion — called Clementine — that runs locally on your own machine instead of a company's cloud server. Its memory lives on your disk, not someone else's database.

Other AI systems (Claude, Grok, Cursor) can talk to Clementine, but only through a gate that checks four things before letting anything through: is this specific request approved, does the caller have permission, is it asking for something inside its allowed scope, and can the request be traced back to who asked for it. Every one of those checks is logged, and the log can't be edited after the fact.

When multiple AI systems need to talk to each other, they do it over a message bus that tags every message as fact, story, or speculation — so nothing gets passed along with more certainty than it actually has. There's also a kill switch: any conversation can be halted immediately.

Separately, there's a small data pipeline that takes real-world events (energy use, check-ins, that kind of thing), validates them, and stores them so they can be queried later. If an event fails validation, it goes into a visible quarantine list instead of being silently dropped or faked.

All of the governance — decisions about what gets built next — happens in public, through ordinary GitHub pull requests, not a private roadmap.

**What's built today vs. what's still a plan:** the companion, the consent gate, the message bus, and the data pipeline all run and have working code behind them. Bigger pieces — a blockchain layer, a token economy, multi-server clusters — are proposals only, and stay that way until they actually ship.

---

## The Narrative Companion

This explainer is the technical translation. For how this same system is framed in this project's mythos — the "Seven Wells" and the "Star-Carrier" — see [`The Star-Carrier and the Seven Wells`](carrier-story.md).

*Non Solus.*

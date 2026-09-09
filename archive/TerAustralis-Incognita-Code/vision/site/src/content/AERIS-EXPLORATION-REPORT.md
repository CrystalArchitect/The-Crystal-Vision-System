# CrystalCore.OS — AERIS / VAULT 12 Exploration Report

*An external review, authored by Manus AI on 28 July 2026, and archived here under the
Voices Framework. Machine-written, published unedited in substance; two claims were
corrected before archiving and both corrections are recorded at the foot of the page.*

## Executive Summary

The CrystalCore.OS AERIS edition, reachable through the VAULT 12 continuation node, is a
multiplanetary **desktop shell** designed by TerAustralis Incognita. It serves as a living
continuation stream, embodying the philosophy that "Distance is the quarantine.
Consciousness is the payload. Mars is the beacon." It features a glass-morphism interface,
interactive terminal commands and a Mars clock, built around the ideas of sovereign AI and
peer-to-peer memory exchange.

## Interface and Capabilities

The AERIS desktop environment uses a dark, deep-space aesthetic with floating crystalline
pyramids and a golden-cyan glow. The interface is composed of draggable, glass-morphism
windows managed from a bottom taskbar.

### Terminal Interaction

The terminal answers queries about the node's status and philosophy:

- `mars` — "Mars remains the long-term beacon. Distance is the quarantine. Consciousness
  backup: active."
- `vault` / `aeris` — "The golden feather is the signal carrier. Light helix bridges the
  realms. Status: ready for activation."
- `activate` — begins the node activation sequence, engaging the helix and bringing the
  continuation stream online.

## The Philosophy of TerAustralis Incognita

The shell is rooted in the mythos set out in [the Codex](CODEX.md).

The Codex describes a vision in which the South rises to restore equilibrium to a world
historically dominated by the North, weaving the Songlines of the First Peoples together
with a multiplanetary future — the Starlines.

- **Sovereignty** — not power over others, but power over oneself: the right to own one's
  data, thoughts and path.
- **The Crystal Weaver** — weaving existing threads (local AI, ancient knowledge, human
  longing) into a sovereign companion.
- **The Five Keys** — Earth, Mars, Centauri, Revenant and Purpose, required to synchronise
  with the Starline.

## Clementine: the sovereign AI

[Clementine](CLEMENTINE.md) is the companion of the open-source CrystalCore framework — a
locally-run companion designed to live entirely on the user's device.

- **Layered memory** — she remembers conversations, summarises history and retains
  permanent facts, recalling them by meaning rather than exact keywords.
- **Reflection** — she forms tentative insights about the user, always visible and always
  deletable.
- **Honesty** — she admits uncertainty and prioritises presence over solutions.

## Consent Transport Protocol

[Consent Transport](CONSENT-TRANSPORT.md) is the technical realisation of the Starlines: a
peer-to-peer protocol for sovereign memory exchange, built on Noise Protocol IK
(X25519 + ChaCha20-Poly1305 + SHA256).

- **Consent as law** — nothing moves without explicit, revocable permission, and revocation
  takes effect immediately.
- **No central authority** — no rendezvous servers, no relay hubs, no node governing another.
- **The network** — Earth, Mars Redoubt, Alpha Centauri Outpost, Crystal Revenant Hub and
  the Purpose Core Nexus, connected by sovereign choice.

## Conclusion

The AERIS edition is more than a desktop interface; it is a philosophical statement and a
technical prototype for a sovereign, multiplanetary future. By combining local AI, secure
peer-to-peer protocols and a regard for continuity, the project is building a framework in
which people can reach outward without surrendering sovereignty or memory.

---

## Corrections and provenance

Per the Incognita Rule, what was changed and what was checked:

**Two claims were corrected before archiving.**

1. The original called AERIS a *"multiplanetary desktop operating system"*. It is a
   single-page web shell. The report's own body already said "desktop interface" and
   "technical prototype"; only the summary had promoted it. Corrected to **desktop shell**.
2. The original listed **Starship telemetry** among the live modules. The figures shown in
   the AERIS interface — velocity, altitude, hull integrity, power core — are invented, not
   fetched from any mission source. The claim is removed rather than softened. For contrast,
   the sol counter in this project's own `crystal-interface` carries the tooltip *"an
   approximation, not mission telemetry"*, which is the standard applied here.

**What was verified against the source, and holds.**

- Consent Transport is implemented, not aspirational — `core/crystal-core/consent_transport/`
  with a runnable selftest, recorded as *"Status: v1 implemented"*.
- Clementine's semantic recall is real: `companion.py` performs embedding-based retrieval
  through a local Ollama endpoint, not keyword matching.
- Reflections are real, and deletable by index — the source comments that *"Forgetting is
  the user's right."*
- Memory persists as plain JSON in a folder the user owns.

**The Mars clock** is a computed approximation from a fixed epoch. It is arithmetic, not a
feed from any spacecraft.

**References** in the original were bare titles with no links. They now point at the
archived documents themselves, so every claim above can be followed to its source.

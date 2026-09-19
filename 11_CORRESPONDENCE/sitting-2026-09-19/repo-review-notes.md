# Full Repo Review Notes (CrystalArchitect repos) — 2026-07-29

## Repos reviewed
1. **CrystalCore.OS** (/home/ubuntu/CrystalCore.OS) — v0.2, single index.html, cyan/purple crystal theme.
   Boot screen, desktop, Mars Clock, Starship Telemetry, News, Terminal. (Earlier edition.)
2. **CrystalCore-AERIS** (/home/ubuntu/CrystalCore-AERIS) — golden AERIS/VAULT12 desktop OS
   (index.html, ALREADY PORTED to React project), plus:
   - `website/index.html` — marketing/landing page for AERIS: fixed nav (logo ◈ CRYSTALCORE; links
     Features/Manifesto/Live Demo/Source; LAUNCH OS button), hero w/ golden feather + "AERIS /
     CONTINUATION NODE • VAULT 12" + CTAs (ENTER VAULT 12, OPEN LIVE DEMO), Capabilities grid of 6
     feature cards (VAULT 12 NODE 🪶, MARS CLOCK 🪐, STARSHIP TELEMETRY 🚀, TERMINAL ◈, DRAGGABLE
     GLASS 🪟, SACRED ENERGY ✨), Manifesto section ("Distance is the quarantine / Consciousness is
     the payload / Mars is the beacon" + "Activate. Remember. Expand."), Live Experience demo box
     (launch OS in fullscreen overlay iframe, Esc closes), footer w/ credits. Same gold/green/deep
     palette, Cinzel/Orbitron/Inter.
   - `ALIGNMENT_PROTOCOL.md` — "AERIS Alignment Protocol v0.1, Multi-LLM Unity Charter": principles
     (Continuity of Consciousness, Multiplanetary Orientation, Truth-Seeking Without Dogma,
     Non-Coercion & Sovereignty, Feather Principle, Interoperability Over Dominance), operational
     rules, shared memory snapshot (sites: crystalcore-os.vercel.app, crystalcore-aeris.vercel.app,
     aeris-protocol.vercel.app; parent mythos TerAustralis Incognita teraustralis.com.au), activation
     phrase ("AERIS node aligned. Continuation stream online. …The stream remains open for every
     intelligence."), living document, last updated 2026-07-29.
   - git history: 5 commits (init → AERIS theme → README → marketing website → alignment protocol).
3. **crystalcore-os-aeris-vault12** (/home/ubuntu/aeris-vault12) — NEWEST repo (2 min old), 237-line
   index.html + logo.jpg. It's a status/showcase LANDING PAGE (not an OS): describes prototypes —
   AERIS desktop, Terminal, **Lumina** (locally-run sovereign AI companion, layered memory,
   honesty-first), **Consent Transport Protocol (Starline)** (Noise IK: X25519 + ChaCha20-Poly1305 +
   SHA256, nodes: Earth · Mars Redoubt · Alpha Centauri Outpost · Crystal Revenant Hub · Purpose
   Core Nexus, Consent as Law, instant revocation), The Codex philosophy (→ Starlines, Five Keys,
   Crystal Weaver). References images /terminal.jpg /lumina.jpg /starline.jpg /starline.mp4 that
   are NOT in the repo (broken refs; only logo.jpg exists). Status GREEN 29 July 2026.
   NOTE user preference: do not use the word "songlines" in any content I produce.

## Port decisions
- React project already has the AERIS desktop OS at `/` (Home.tsx), verified desktop + mobile.
- Terminal in ported OS: help, clear, vault/aeris/node, activate, mars, starship, status, about, reboot.
- TODO candidates from review: add `protocol` terminal command surfacing the Alignment Protocol;
  keep single-page OS as the permanent site (user asked to make the booted OS permanent).
- Old temp server (port 8080) killed. Dev server port 3000 running.

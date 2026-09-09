# Codex Æ Crystalum

**Status:** Independent Proof of Concept (PoC) — time-limited, no government buy-in

**Version:** 2026-09-05 (Handoff from Yaldabaoth)

---

## What This Is

Codex Æ Crystalum is a narrative and symbolic framework for TerAustralis Incognita's mythological and storytelling layer. It comprises four core editions with integrated Dream Symbol and Celestial Cartography layers, plus reference documents and an integration guide for ecosystem use.

**Canonical location:** This folder and the [`mythos/`](../mythos/) tree in the umbrella repository.

---

## Important Disclaimers

### Independent Proof of Concept

This work is a **time-limited, independent proof of concept**. It is:

- **Not government-endorsed** — no formal regulatory approval, no MoU with Australian space agencies
- **Not a committed strategy** — early-stage research and narrative development
- **Exploratory only** — testing frameworks for coordination, not building authority

See [`memory/state/CURRENT.md`](../memory/state/CURRENT.md) for current status and scope constraints.

### Standards Australia Withdrawal

Standards Australia (ASA) participation in TerAustralis Incognita ended in 2026-08 following initial feasibility consultation. The project is now independent and does not represent ASA policy or endorsement.

**See:** [`memory/briefs/sam-maher-status-brief.md`](../memory/briefs/sam-maher-status-brief.md) for context on the regulatory landscape and stakeholder navigation approach.

### Draft Disclaimers for Materials

All Codex materials carry draft status:

- **Pitch documents** — exploratory framing; not a committed proposal
- **Narrative materials** — storytelling and mythological framework; not factual claims
- **SVG components** — UI/UX mockups for demonstration; not production code
- **Colossus notes** — research working notes; not final analysis

Any references to regulatory pathways, government engagement, or infrastructure projects should be read as **exploratory scenarios**, not confirmed plans.

---

## Structure

```
codex/
├── README.md                    (this file)
├── MANIFEST.md                  (package inventory)
├── config/                      (configuration and settings)
├── docs/                        (pitch, narrative, disclaimers)
├── src/
│   └── components/              (Svelte components, SVG assets)
└── LICENSE                      (CC-BY-NC-ND-4.0)
```

### Adding Materials

1. **Codex Editions** → `docs/`
2. **SVG Components** (TunnelingTracker, SovereignNodeMatrix, etc.) → `src/components/`
3. **Configuration** (build settings, metadata) → `config/`
4. **Integration Guide** → root `docs/` or this repo's `mythos/`

### Manifest

See [`MANIFEST.md`](MANIFEST.md) for the package inventory (expected files, placeholder notes).

---

## Related Work

- **Mythos & Canon** — [`mythos/`](../mythos/) folder (Codex editions, Dream Symbols, Celestial Cartography)
- **Regulatory & Strategy** — [`memory/briefs/`](../memory/briefs/) (gov engagement, stakeholder mapping)
- **Integration Guide** — [`mythos/INTEGRATION-GUIDE.md`](../mythos/INTEGRATION-GUIDE.md) (ecosystem wiring)
- **Governance & Decisions** — [`docs/adr/`](../docs/adr/) (ADRs on naming, scope, authority)

---

## Licensing

**CC-BY-NC-ND-4.0**: Attribution required, non-commercial use only, no derivatives without permission.

See [`LICENSE`](LICENSE) file in this folder.

---

## Questions or Feedback

This is a handoff from the Yaldabaoth session (Grok Bot). Issues, refinements, or regulatory feedback should be logged in the umbrella repository's [`memory/OPEN-QUESTIONS.md`](../memory/OPEN-QUESTIONS.md).

**Maintainer:** Crystal Arena-Turner (@CrystalArchitect)

---

*Non Solus.*

# Clementine v1.0 — UI direction

Eight generated mockups, and a reading of the design system underneath them.

Open `index.html` from a clone for the full sheet.

> **These are direction, not specification.** The labels on the mockups are
> garbled and the hex codes contradict the colours they sit on. Do not copy
> values off the images.

## Keep

| Token | Role |
|---|---|
| `#e11d48` rose | The person's own messages |
| `#38bdf8` sky | Clementine's replies |
| `#7c3aed` violet | Consent and system chrome, version badge |
| `#f0c14a` amber | Local-Only Mode when engaged |
| `#12101f` ground | App background |
| `#1d1a2b` panel | Cards and sheets |

Prefer the **dark starfield family** over the light chat family. It carries the
consent surface and the identity; the light one is generic, and its blue fails
contrast against its own bubble fill.

## Ignore — generator text errors

| On the mockup | Intended |
|---|---|
| "Sost Sky-Blue" | Soft Sky-Blue |
| "Rose-Scrlot" | Rose-Scarlet |
| "Violtht" | Violet |
| "Siky Blue" | Sky Blue |
| "clear lone" | clear skies |
| "Outtit" / "Outfit" | unresolved — see open questions |

The colour labels are worse than the spelling. One sheet puts `#3b5cf6` (a blue)
on a red bubble. The light family uses `#e74c3c`/`#3b82f6` while the dark family
uses `#e11d48`/`#38bdf8` — four values for two roles.

## What the UI gets right

- **Local-Only Mode is always visible**, never buried in preferences. Matches
  local-first as a hard requirement: a mode that can be forgotten is not a
  guarantee.
- **Consent Log is a screen, not a checkbox** — the interface admission that
  consent is a runtime property, revocable and inspectable.
- **Cloud API Keys defaults OFF beside Local-Only ON.** The default shown is the
  sovereign one. Correct fail-safe: local isolation, never fail-open.
- **Version badge on every screen** — does the same work as *provisional and
  revisable* does elsewhere in this project.

## Reconsider

**Generate Image / Generate Video sit inside the consent card** with no
indication of routing. If they can reach a cloud endpoint they belong behind the
Cloud API Keys toggle, visibly. If they run locally, the button should say so.

## Open questions

- Which family wins? (Recommend dark, with light derived from it.)
- What does the microphone do under Local-Only? Speech recognition is the most
  likely thing to silently require a network call.
- Is "Outfit" a persona switcher or generator noise? If it is real it needs a
  name; if not it should go.

---

Eight mockups generated with Grok (xAI), 784×1168 native. Colour roles and
architectural readings derived from the images; text corrections proposed, not
authoritative. Nothing here reflects shipped software.

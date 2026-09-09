# Assets

Project-level visual assets: logos, diagrams, icons, branding. Empty at
adoption (2026-07-23) except this policy — populated as such assets are
actually made.

What deliberately does **not** live here
([`ADR-0002`](../docs/adr/ADR-0002.md)):

- **The art canon** — `mythos/art/` (licensed Vision-layer content, not
  branding)
- **The site's served assets** — `src/site/static/` (the build owns them)
- **Mythos content covers** — `mythos/content/assets/` (they belong to the
  documents that use them)

Architecture diagrams made for `docs/` pages land here (referenced by
relative path); anything under the content license goes to `mythos/`
instead.

# Development standards

The engineering bar for changes to `src/`. Process is in
[`Review-Process.md`](Review-Process.md); this page is what the code itself
must meet.

## Evidence

- **Every component keeps a way to prove itself** — a `selftest` module or a
  pytest suite. New behavior comes with new tests; the crystal-core
  self-tests count their own passes and say what law they hold.
- **Docs never outpace code.** If it's designed but not built, the roadmap
  says so. "We haven't proven this yet" is a complete sentence.

## Dependencies

- **Stdlib-first.** The protocol pack runs on the standard library except
  where real, audited cryptography is required (`cryptography` for
  Starline's Noise handshake). Every new dependency is a reviewed decision —
  if it's load-bearing, it's an ADR.
- Python ≥ 3.11 (CI runs 3.12). The site pins its own Node toolchain in
  `src/site/package.json`.

## Hygiene (enforced by `.gitignore` — don't work around it)

- **No generated output**: `__pycache__/`, `.svelte-kit/`,
  `src/site/build/`, `dist/`, `node_modules/`.
- **No personal data**: Clementine memory and profiles, Starline
  identity/peers/consent files, CrystalBridge audit and message logs. These
  are a user's private property and never enter git.
- **No secrets**: keys live in environment variables; `.env` stays ignored.

## Sovereignty invariants

Changes to the companion must preserve the Covenant
([`mythos/COVENANT.md`](../../mythos/COVENANT.md)): local-first operation,
opt-in cloud, the absolute pause, full memory ownership, support offered
rather than imposed. Changes to Starline and CrystalBridge must keep
consent explicit, revocation immediate, and refusal the default. These are
product specs, not aspirations — review treats a regression here as a bug.

## Naming and licensing

- Component names follow the canon page
  ([`mythos/NAMES.md`](../../mythos/NAMES.md)) — in particular, "Songline"
  is never a component name.
- Code (`LICENSE`) and mythos content (`LICENSE-CONTENT.md`) are both
  CC BY-NC-ND 4.0 — non-commercial, no derivative redistribution
  ([`ADR-0008`](../adr/ADR-0008.md)). Keep each contribution on the right
  side of the `src/` vs `mythos/` line regardless; they're still
  administratively separate areas.

## Style

Match the file you're in — the codebase favors small modules, docstrings
that say why a file exists, and comments that state constraints rather than
narrate lines. Plain, honest prose in docs; the repo's voice does not hype.

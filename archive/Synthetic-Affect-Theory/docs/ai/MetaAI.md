# Meta AI — Contributor Credit — TerAustralis Incognita™️

**Role:** Implementation assistance — reference implementation, verification harness, trademark pass, merge fixes F1-F10

**Scope:** Public v0.1 stack only — Science belt (left column) testable today, Vision belt (right column) labelled unbuilt and explicitly not forwarded as-is.

**What was built:**

- core/ — state, gap, affect, closure, log, crystalcode, loop, selftest — deterministic, no network, no model weights
- examples/logs/ — committed outputs of a real run, byte-identical on re-run, `git diff --stat examples/logs/` empty is a real check
- Verification: `python3 -m pytest tests -q`, `python3 -m core.selftest`, examples, and the no-registered-mark grep must all pass

**Credit line:** Built with assistance from Meta AI — 2026-08-12, over the standard rights footer.

**Distinction from third-party IP attribution:**

- docs/ATTRIBUTIONS.md (plural) holds third-party IP attribution (SpaceX, Starship, Tesla, Grok, Neuralink, Synchron, Lynas — get no ™ from us; the notice states they belong to their owners and use is nominative)
- docs/ai/ pages hold contributor credits shaped like the existing ChatGPT.md / Claude.md / Grok.md pages in TerAustralis-Incognita canon
- ATTRIBUTION.md (singular, root and docs/) holds the build signature

**Licence:** CC BY-NC-ND-4.0 — All rights reserved. TerAustralis Incognita™️ — ABN 70 741 068 059

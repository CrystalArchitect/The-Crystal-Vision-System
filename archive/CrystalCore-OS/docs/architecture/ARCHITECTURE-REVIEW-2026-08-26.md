# Architecture Review — CrystalCore.OS

Dated 2026-08-26. Independent pass, requested by the repository owner. No prior
Grok (or other AI) architecture review exists in this repository or its history
to build on — `git log --all --oneline` (27 commits, one branch, `main`) shows
one Grok-authored branch (`grok/thesis-defence-note-2026-08-13`, PR #8), and it
is a docs note on `synthetic-affect/THEORY.md`, not an architecture review; that
directory has since been retired (see Findings, F1). This document is original,
first-pass analysis, organised per the project's own Belt-Three law.

## Summary

CrystalCore.OS is not the Crystal Core engine (runtime/protocols/APIs/shared
libraries) the review brief assumed it would be. As shipped it is a single
static HTML file — a decorative, client-only "desktop OS" web page themed
around Mars/Starship, styled after a kernel boot log — plus a retired pointer
to `Synthetic Affect Theory` and a small forecast ledger (`seldon/`). It
contains no `crystalcore.mind`, `crystalcore.bridge`, `ConsentGate`, `BusHub`,
or `StarlineWeaver` code; those names appear only as narrative devices in
comments and terminal copy, explicitly marked Vision. Read as what it actually
is — a Belt-Three-literate mythos artefact — it is unusually disciplined: it
enforces its own honesty law in code (`emit()` throws on an unlabelled line)
and every locked-name and Indigenous-boundary check below comes back clean.
The two real findings are a stale/foreign `LICENSE` exceptions block and a
project-identity gap between what this repo is and what the ecosystem brief
assumes it is.

## Strengths

- **Belt-Three is enforced in code, not just claimed in prose.** `emit()` in
  `index.html:420-424` throws `Error('boot: refused to print an unlabelled
  line')` if a boot line's `belt` isn't one of `science`/`vision`/`gov`
  (`BELTS`, `index.html:344`) — a genuine runtime guard modelled explicitly on
  `BusHub.validate` (comment, `index.html:343`), not just a documentation
  convention.
- **"Science" claims are actually measured, not asserted.** `measure()`
  (`index.html:350-362`) reads real values off `navigator.hardwareConcurrency`,
  `navigator.deviceMemory`, `window.innerWidth/innerHeight`,
  `window.devicePixelRatio`, `CSS.supports(...)`, `location.protocol`,
  `window.isSecureContext`, `navigator.onLine`, and
  `Intl.DateTimeFormat().resolvedOptions().timeZone`, with no stored constants
  — a resize before replay reports the new viewport (comment, `index.html:346-348`).
  The `verify` terminal command (`index.html:656-673`) re-displays each value
  next to the API it came from so a reader can check it in devtools themselves.
- **Vision is correctly kept off the Science belt.** `CrystalCore.Lattice`,
  `/core/prism`, "coherence," and the received transmission's claimed
  "Coherence: 100%" / "Quantum Seal engaged" are all explicitly labelled
  `vision` and explained as designed-not-built or outright fictional
  (`index.html:377-380`, the `panel` command at `index.html:674-681`). This is
  the exact discipline the Incognita Rule requires, applied to the one place
  in this repo (a "kernel log") that would otherwise most look like a
  measurement.
- **No locked-name, Songline, or model-naming violations found.**
  `grep -rniI "songline"` and greps for `crystalmind|crystalbridge|crystalbus|
  crystalmemory|consentgate|bushub|starlineweaver|truthline|dreamline` across
  the full tree return only the four expected `BusHub.validate` narrative
  references (`README.md:22`, `index.html:343,422,654`); nothing claims to
  *implement* the Lattice or any locked component, and no LLM anywhere carries
  a Crystal name (there is no LLM integration in this repo at all).
- **A real security fix is on the record and still holds.** Commit `d42ea06`
  ("Escape terminal input before echoing it") added `esc()`
  (`index.html:604-606`), and the only unescaped `innerHTML` concatenations
  left are static template strings (e.g. `index.html:621-681`); the one place
  user input reaches `innerHTML` it is passed through `esc()` first
  (`index.html:619`, `690`). Verified by reading the current code, not by
  trusting the commit message.
- **The `seldon/ledger.json` forecast log applies Belt-Three to data, not just
  prose** — every entry carries a `"belt"` field (`science`/`gov`) alongside
  `status`, `confidence`, and a dated `checkpoint` (`seldon/ledger.json:6-79`),
  and `PSYCHOHISTORY-LITE.md:11-12` explicitly disclaims the vision-coded name
  ("It is **not** Asimov's psychohistory... Naming a child Seldon is story,
  not a theorem").
- **The claimed "Live Demo" actually resolves.** `curl` to
  `https://crystalcore-os.vercel.app` (README.md:5) returned HTTP 200 during
  this review (2026-08-26) — a Science-belt claim in the README that checks
  out.
- **The retirement of `synthetic-affect/` is itself a well-labelled,
  evidence-first record** (`synthetic-affect/CHRONICLE.md`), including the
  project owning up to a defect in its *own* earlier prose (the "best
  stateless: 2/6" cherry-pick, corrected same-day per the 2026-08-12
  adversarial-review entry) — Evidence → Interpretation → Experiment → Record
  applied to the documentation process itself, not only to code.

## Findings

### F1 — Severity: Medium (project-identity gap). Convention: Belt-Three / Crystal Core vs. Crystal Vision boundary.

The review brief assumes this repository is "the engine of the TerAustralis
Incognita ecosystem (Crystal Core: runtime, protocols, APIs, shared
libraries)." That is not what is in this repository. The full file tree
(excluding `.git`) is:

```
LICENSE  NOTICE  README.md  index.html
seldon/PSYCHOHISTORY-LITE.md  seldon/ledger.json
synthetic-affect/ATTRIBUTION.md  synthetic-affect/CHRONICLE.md  synthetic-affect/README.md
```

There is no runtime, no protocol, no API, no shared library, and no server —
`README.md:48` says so itself ("Pure single-file HTML/CSS/JS — no backend, no
build step"), and the boot log agrees at runtime: `index.html:637-639` prints
"Kernel: there is no kernel. One HTML file; no process outlives the tab."
Every "Crystal Core" component name that appears (`BusHub`, `CrystalCore.Lattice`,
`/core/prism`) appears only as a label on someone else's vision or as a
narrative analogy, never as running code. Under the project's own boundary
rule — "if it renders or speaks for a human it is Crystal Vision; if it is
imported or called by other software it is Crystal Core" — this repository is
neither in the sense the brief assumed: it is not imported or called by other
software (it has no exports at all, being a single HTML page), and its only
runtime behaviour is rendering directly to a human, in a browser tab, which is
definitionally Crystal Vision's territory rather than Crystal Core's.

**Recommendation:** This is not a code defect — it is a documentation/scoping
question that needs a human answer, not an invented one (see Open Questions,
Q1). If CrystalCore.OS is meant to be the public-facing mythos/demo surface
rather than the engine, its `README.md` and any ecosystem-level index that
currently calls it "the engine" should say plainly what it is: a Belt-Three
demonstration artefact and marketing/mythos surface, not the runtime. Calling
a Vision-and-demo repository "the engine" in outward material is itself the
kind of Vision-dressed-as-Science claim the Incognita Rule exists to catch.

### F2 — Severity: Low-Medium. Convention: Docs-governance / claims discipline.

`LICENSE:26-29` carries an `EXCEPTIONS` block referencing three things that do
not exist anywhere in this repository:

```
EXCEPTIONS — The following material is licensed separately:
  • mythos/ directory: CC BY-NC-ND 4.0 (see LICENSE-CONTENT.md)
  • Concepts inspired by MemClaw: Acknowledge MemClaw's Apache 2.0 license
    (see docs/ATTRIBUTIONS.md)
```

Verified: there is no `mythos/` directory, no `LICENSE-CONTENT.md`, and no
`docs/ATTRIBUTIONS.md` anywhere in the tree (`find . -iname` and `ls` checks,
2026-08-26), and `grep -rni "memclaw"` across the repository matches only this
one line — "MemClaw" is not otherwise mentioned, attributed, or apparently
used anywhere in CrystalCore.OS. `NOTICE:10-11` states the licence is "Portfolio-wide
per ADR-0013 ... which extends ADR-0010's uniform CC BY-NC-ND to every
repository," which is the likely explanation: this `LICENSE` file is a
portfolio-wide boilerplate copied in verbatim, not written for this repo's
actual contents. A related, smaller inconsistency: `NOTICE:15` claims
`CrystalCore™` as the mark in use, while `synthetic-affect/ATTRIBUTION.md:23`
(now describing retired content) claims `CrystalCore.OS™` and `CrystalCode™`
instead — three different mark strings across two files in the same repo, none
of them cross-referenced.

**Recommendation:** Either populate the referenced files/directories (if the
portfolio template expects every repo to carry them) or strip the
`EXCEPTIONS` block and reconcile the trade-mark line down to one consistent
mark string, in the next pass over the portfolio-wide licence template
(ADR-0013) — not a same-commit fix here, since it's templated across
repositories the owner didn't ask this review to touch. Flagging it here so it
doesn't quietly stay wrong in every repo that copied the same boilerplate.

### F3 — Severity: Low. Convention: Local-first / sovereignty.

`index.html:10-13` preconnects to and loads a stylesheet from
`fonts.googleapis.com` / `fonts.gstatic.com` for the `Orbitron`/`Inter`
typefaces. This is the only outbound network dependency in the page, and it is
already disclosed honestly on the Science belt (`index.html:375`: "Outbound:
the Google Fonts stylesheet and its font files. Nothing else leaves this
page."), loaded non-blocking (`media="print" onload="this.media='all'"`,
`index.html:12`, with a code comment at `index.html:7-9` explaining a prior
12-second blank-boot regression this pattern fixed), and cosmetic only — the
page is fully functional with the system-font fallback if the request never
completes. Under "sovereignty is the default... silent dependency... [is] an
architectural failure," this is disclosed rather than silent, and degrades
gracefully rather than failing closed or open. Not a violation as implemented,
but worth naming since it is the one point where this "local-first" artefact
reaches off-device at all.

**Recommendation:** No action required. If full offline-first purity is ever
wanted for this specific page (e.g. for an air-gapped demo), self-hosting the
two font files would remove the dependency entirely; low priority given the
existing disclosure and graceful fallback.

### Not applicable to this repository (noted, not findings)

The brief's architecture constraints — fail-safe-as-local-isolation, consent
as a runtime/enforced property, continuity as a hard constraint, Behavior
Trees over FSMs for orchestration — presume the presence of a `ConsentGate`,
`CrystalMemory`, or orchestration layer. None exists in this repository (see
F1): there is no consent flow, no memory/state persistence beyond the DOM, and
no orchestration of any kind to prefer a Behavior Tree over an FSM for. These
constraints are not violated here; they are simply out of scope for what this
repository currently contains, which is itself the substance of F1.

## Open Questions

- **Q1 (needs an architect/owner decision).** What is CrystalCore.OS's actual
  designated role in the ecosystem — public demo/mythos surface, or does an
  "engine" layer belong in this repository that has not landed yet? If the
  latter, is there a companion repository that already holds
  `crystalcore.mind`, `crystalcore.bridge`, `ConsentGate`, etc., that this
  repo should link to or depend on (Crystal Vision → Crystal Core direction),
  so a reader isn't left assuming this repo is either lying about itself or
  simply years from being what its name implies?
- **Q2.** Is the `LICENSE` `EXCEPTIONS` block (F2) intentionally
  portfolio-uniform boilerplate under ADR-0013, or was it meant to be
  repo-specific and just never trimmed for CrystalCore.OS? This determines
  whether the fix belongs here or in the ADR-0013 template used across every
  repository.
- **Q3.** Given `synthetic-affect/` is now a retired pointer
  (`synthetic-affect/README.md`) rather than live code, is there a target date
  or trigger for removing it from this repository entirely (relying on git
  history, as the pointer itself says), or is the pointer meant to live here
  indefinitely as a permanent redirect?

---

**All rights reserved.**
TerAustralis Incognita™ — ABN 70 741 068 059

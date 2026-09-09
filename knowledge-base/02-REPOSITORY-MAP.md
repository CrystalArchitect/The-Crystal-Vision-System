# Repository Map

The canonical map of all seventeen repositories: what each owns, how they
relate, and where the seams between them are.

> **Second scope correction (2026-08-08, later the same day).** The count
> immediately below — eleven — is also wrong. The portfolio holds
> **seventeen**: six archived, eleven live, six of those public. Both the
> earlier "twelve" and its correction to "eleven" were taken from a
> GitHub *search* query, which under-reports; five repositories that had
> existed since June and July were simply never returned. The
> authoritative list is the account's own repositories page, and no count
> in this knowledge base should come from a search result again. Recorded
> in full in [`11-CORRECTIONS.md`](11-CORRECTIONS.md) Part 20, including
> why a ledger that logs its catches but not its misses is advertising.
>
> The correction below stands as to *what happened* — two repositories
> were deleted, found, rescued and re-archived — and is wrong only in its
> arithmetic.

> **Scope correction (2026-08-08).** The portfolio holds **eleven**, not
> twelve. `CrystalCore-AERIS` and `CrystalCore.OS-Aeris-Vault12` were
> deleted from the account in the week before this date; every Statement
> below that describes them in the present tense describes a repository
> that no longer exists, and is true only of its own date.
>
> The deletion was found by this archive disagreeing with the account —
> a routine check before publication listed eleven repositories where
> this map claimed twelve. No test failed and no alarm fired; the
> disagreement was the only signal there was.
>
> Both were restored from GitHub's 90-day window at the maintainer's
> direction on 2026-08-08, their contents rescued verbatim into
> `TerAustralis-Incognita/archive/2026/rescued-2026-08-08/`, and then
> deleted again. Twenty-six files were recovered; fourteen existed in no
> other repository, verified by hashing every rescued file against every
> file in all eleven surviving ones.
>
> This map understated one of them badly. It recorded
> `CrystalCore.OS-Aeris-Vault12` as ten tracked files holding seven
> specifications; it held **twenty** files, including seven documents
> this archive never recorded at all — among them an
> `ETHICAL-RUNTIME-SPEC.md` and a 372-line operational log, the largest
> document in the repository. The Historical Notes below already flag
> that this entry was written from a stale clone. That flag was correct
> and its consequence is now measured: the archive's account of a
> repository was the only surviving record of it for nine days, and the
> account was incomplete.

> **Scope correction (2026-07-28).** This document was written on
> 2026-07-24 against six repositories and said "six" throughout. The
> portfolio review of 2026-07-28 found **five more** that this archive
> had never recorded — four of them created after this map was written,
> and four of the five more recently active than anything it did cover.
> They are added as their own Statement below rather than folded into
> the original six, so the reconstruction of 2026-07-24 stays legible as
> what was true on 2026-07-24. See `11-CORRECTIONS.md`.

## Statement

Six repositories exist. One is public; five are private. The public
repository holds no application code — it is canon, governance, and
mythos only.

**Status: Implemented** (verified directly against live GitHub metadata,
not assumed from any document).

### Evidence
- GitHub API, queried directly 2026-07-24: `TerAustralis-Incognita` —
  `"private":false`, `"visibility":"public"`, `has_pages:true`,
  `has_discussions:true`, `pull_request_creation_policy:
  "collaborators_only"` (public read, closed contribution). The other
  five — `TerAustralis-Incognita-Code`,
  `CrystalCore.OS-the-Crystal-Architecture-Archive`, `The-Crystal-
  Vision`, `crystalcore`, `crystal-vision` — all `"private":true`.

### Historical Notes
The system ledger (`STATUS.md` in this repository) previously described
`The-Crystal-Vision`, `crystalcore`, and `crystal-vision` as "archived
2026-07-18, read-only." Live GitHub metadata shows `archived:false` for
all three, confirmed 2026-07-24. Corrected in this repository's
`STATUS.md`; see `11-CORRECTIONS.md`. Whether to formally archive them
is an open decision the umbrella's own governance charter records as
undecided — not a settled fact any document simply got wrong. See "Open
decisions" below.

### Cross References
`04-GOVERNANCE.md`, `07-IP` content in `04-GOVERNANCE.md`.

---

## Statement

The canonical, current per-repository map, quoted from the umbrella's
own governance charter, rewritten 2026-07-24 (hours before this
reconstruction) from a same-day survey of all six repositories:

**The living system:**

| Repository | Role |
|---|---|
| `TerAustralis-Incognita` | The umbrella: governance, ADRs, architecture docs, research, provenance mirrors under `archive/`, and `mythos/` — the canon home (Codex, Apocryphon, The First Remembering, the crystalcore-os terminal). |
| `TerAustralis-Incognita-Code` (private) | The software, per Migration-Plan Stages 1–2: `core/` (engine — protocol pack with Clementine, CrystalBridge, mesh stub, SDK) and `vision/` (application — Lumina, voicebox, demo shells, the site source). Full CI; carries the Pages deploy and `CNAME`. |
| `CrystalCore.OS-the-Crystal-Architecture-Archive` | The system ledger: one fleet-wide `STATUS.md` — state, receipts, known unknowns across all repositories. Deliberately small (now also holds this knowledge base). |

**Frozen provenance** — checkpointed 2026-07-17 (the laptop hand-off),
deliberately left unarchived, never edited; their code lives on as
ancestors of the `-Code` tree:

| Repository | Was | Lives on as |
|---|---|---|
| `The-Crystal-Vision` (tag `vision-safe-2026-07-17`) | Codex site + Clementine companion; holds the complete crystalcore v0.13.4 bytecode rescue and the laptop snapshot | Ancestor of Lumina's embedded framework (which forked the earlier 0.7.0 line — see "Open decisions") |
| `crystalcore` (tag `crystalcore-safe-2026-07-17`) | The Songline protocol pack | Direct ancestor of `core/crystal-core` (Songline Bus → Starline Weaver) |
| `crystal-vision` | Static demo shell (Grok build) | Direct ancestor of `vision/apps/crystal-interface` |

**Status: Implemented** (this table's every row was independently
re-verified during this reconstruction, not merely copied).

### Evidence
- `TerAustralis-Incognita/docs/governance/Project-Boundaries.md`,
  "Repositories, today" section — added via merged PR #58
  (2026-07-24T03:57:10Z).
- Provenance tags fetched and directly confirmed to exist:
  `vision-safe-2026-07-17` on `The-Crystal-Vision`,
  `crystalcore-safe-2026-07-17` on `crystalcore`.

### Historical Notes
This section itself replaced an earlier version of the same file that
called `TerAustralis-Incognita-Code` "empty by design," stale since
Stage 1 landed the engine. This reconstruction's local clone of the
umbrella repository was briefly stale by three merged pull requests
(#56, #57, #58) mid-session; fast-forwarded and re-verified before this
content was trusted — see `10-PROVENANCE.md` for the full methodology
note.

### Cross References
`07-HISTORY.md`, `10-PROVENANCE.md`.

---

## Statement

The explicit, repeated dependency rule between the engine and the
application: **Crystal Vision may depend on Crystal Core; Crystal Core
never imports Crystal Vision.** The one apparent exception — CrystalBridge
reaching Lumina's memory — is explicitly framed as a runtime filesystem-
path coupling, not a module/package dependency.

**Status: Implemented** (stated identically, independently, in two
separate module READMEs within the same repository).

### Evidence
- `TerAustralis-Incognita-Code/core/README.md`: "Crystal Vision may
  depend on Crystal Core; Crystal Core never imports Crystal Vision.
  (CrystalBridge reaches Lumina's memory *by configured data path at
  runtime* — it serves the companion without importing it.)"
- `TerAustralis-Incognita-Code/vision/README.md`: near-identical
  wording, independently stated.

### Historical Notes
None.

### Cross References
`06-COMPONENTS.md` (CrystalBridge, Lumina entries).

---

## Statement

Canon reaches the public website through exactly one pipeline, which is
manual at one step and is explicitly flagged, by the project's own
governance charter, as a deliberate drift risk:

```
mythos/ (umbrella, canonical)
   → copied by hand into vision/site/src/content/ (Code repo)
   → built by deploy.yml → GitHub Pages → www.teraustralis.com.au
```

The site renders *copies*, not the canon directly — new canon is not
public until its copy step happens. This drift is live right now, not
theoretical: a new mythos file (`THE-FIRST-REMEMBERING.md`) is canonical
in the umbrella as of 2026-07-24 and has not yet been copied into the
site's content set.

**Status: Implemented** (the pipeline mechanism), **Unresolved** (the
specific current drift instance — "site copy of new canon" is one of
the project's own open decisions, see below).

### Evidence
- `TerAustralis-Incognita/docs/governance/Project-Boundaries.md`,
  "How canon reaches the public site" section (added 2026-07-24).
- `TerAustralis-Incognita-Code/CNAME` and
  `vision/site/static/CNAME` — both `www.teraustralis.com.au`, confirmed
  to exist; the umbrella repository has no `CNAME` file at all (moved
  out at Migration-Plan Stage 2).
- The domain itself is **not independently verifiable** from a session
  container — the egress proxy returns 403 on the CONNECT (domain not
  on the allowlist), confirmed directly this session, not merely
  inherited from an earlier claim of "egress blocked."

### Historical Notes
Pages/CNAME/`deploy.yml` all moved from the umbrella to
`TerAustralis-Incognita-Code` at Migration-Plan Stage 2 (2026-07-23). The
umbrella's own `SystemMap.md` described this move as still-broken for
several hours after it had already been resolved — corrected in this
pass, see `11-CORRECTIONS.md`. GitHub Pages source for
`TerAustralis-Incognita-Code` has not yet been switched to "GitHub
Actions" — a pending manual admin step with no API path available from
an agent session.

### Cross References
`06-COMPONENTS.md` (Site entry), `04-GOVERNANCE.md` (open decisions).

---

## Statement

The same brand/concept name is reused across the portfolio for
genuinely unrelated things, in two cases:

**"crystalcore"** names three unrelated things: (1) the companion Python
package family in `The-Crystal-Vision` (four version copies: 0.13.4
canonical, 0.13.4 bytecode-recovered, 0.12.0 reconstructed, 0.7.0
oldest), (2) the CrystalBridge MCP consent-gate package at
`TerAustralis-Incognita-Code/core/crystalcore/` (v0.1.0, unrelated
codebase), and (3) the standalone `crystalcore` repository's Seven
Sisters/Songline protocol-pack brand.

**"Clementine"** names two unrelated things: (1) the companion chat
persona, born in `The-Crystal-Vision` on 2026-07-15, later renamed
Lumina in the current lineage, and (2) the multi-AI message-bus/hub-
agent persona, born in the `crystalcore` repo on 2026-07-17 as the
"Clementine Singularity Bridge," later renamed Starline Weaver in the
current canon. Both original "Clementine" senses were renamed away in
the same 2026-07-21 rename sweep, to two *different* new names, because
they were always two different concepts that happened to share a first
name.

**Status: Historical** (both collisions are fully resolved in current
canon by the 2026-07-21 renames; the old names persist only in
un-updated, frozen-provenance repositories).

### Evidence
- `TerAustralis-Incognita/mythos/NAMES.md`: the governing rename
  document — "Starlines are the map. Dreamlines are the traveller of
  the map," and explicitly reserves "Songline" for Aboriginal culture
  only, not the software.
- Git commit evidence (umbrella repo, 2026-07-21): "lore: complete the
  persona sweep — Clementine (companion) → Lumina"; "rename the
  Songline Bus → Starline Weaver + Dreamline Narrator."
- `The-Crystal-Vision` commit (2026-07-15): "Refactor into the
  CrystalCore package; Clementine is its first persona" — confirms the
  framework was multi-persona-shaped from birth, with Clementine as
  persona #1.

### Historical Notes
The standalone `crystalcore` repository, created 2026-07-17, was never
updated past the pre-rename names — it is the only repository in the
portfolio still natively using "Clementine Singularity Bridge" and
"Songline Bus" throughout its own docs and code. This is presented as a
historical/provenance fact about a frozen repository, not a defect to
fix — that repository is deliberately checkpointed and unedited per the
umbrella's own charter.

### Cross References
`07-HISTORY.md`, `09-GLOSSARY.md`.

---

## Statement

The interface-demo concept and the Seven Sisters/protocol-pack content
each exist in two diverged copies across the portfolio, confirmed
non-identical by direct diff, not merely assumed to be duplicates:

- The crystal-vision interface demo: `crystal-vision/app.js` (546
  lines, newer, standalone repo) vs. `crystalcore/interface/app.js`
  (349 lines, older, inside the standalone Songline-pack repo).
- The Seven Sisters corpus: `TerAustralis-Incognita/research/
  seven-sisters/` vs. the standalone `crystalcore` repository's root
  markdown pack — mostly byte-identical, but `README.md` and three
  core path files differ in a consistent way: the `crystalcore` repo's
  copy keeps older, more grandiose framing ("Quantum Songline Weaver
  v∞.Δ+"), while the umbrella's reorganized copy explicitly downgrades
  to "a Vision-layer motif, not a claim."

**Status: Historical** (both are point-in-time forks, not actively
synchronized).

### Evidence
- Direct `diff` of `app.js`/`style.css` between `crystal-vision/` and
  `crystalcore/interface/`: all files differ.
- Direct `diff` of the Seven Sisters files between the two locations.

### Historical Notes
The editorial toning-down between the two Seven Sisters copies is
itself evidence of the project's own move toward more honest framing
over time — worth noting as a positive signal, not just a duplication
defect.

### Cross References
`03-ARCHITECTURE.md` (Seven Sisters section).

---

## Statement — Open decisions this map records rather than resolves

The umbrella's own governance charter states four open decisions
explicitly, and this archive preserves them as open — they are the
project's questions, not this archive's to answer:

- **Stage 3 repo count** — whether `core/`/`vision/` split into two
  repositories (Migration-Plan criteria; deliberately not decided).
- **0.13.4 lineage** — Lumina's framework forked the 0.7.0 line; the
  0.13.4 rescue's extras (SpaceXAI provider, `node.py`, `status.py`,
  CLI) sit unreconciled in `The-Crystal-Vision`.
- **Frozen repos' end state** — whether to GitHub-archive (read-only
  flag) the three provenance repos, or leave them as-is. Explicitly
  undecided — not a fact any prior STATUS.md simply got wrong when it
  called them "archived."
- **Site copy of new canon** — The First Remembering is canonical but
  not yet copied into the site content set.

**Status: Unresolved** (by design — these are the project's own stated
open questions).

### Evidence
- `TerAustralis-Incognita/docs/governance/Project-Boundaries.md`,
  "Open decisions this map records rather than resolves" section.

### Historical Notes
None — current as of 2026-07-24.

### Cross References
`04-GOVERNANCE.md`, `07-HISTORY.md`.

---

## Statement

Five further repositories exist that this archive did not record before
2026-07-28. Four are single-page CrystalCore.OS terminal artefacts; one
is a full React/TypeScript application with its own presentation deck.
Together they are 5 of the portfolio's 11 repositories, and four of the
five were the most recently active repositories in the portfolio at the
time this section was written.

**Status: Implemented** (all five exist, carry commits, and were read
directly from local clones).

| Repository | What it is | Root commit | Head | Commits / files |
|---|---|---|---|---|
| `CrystalCore.OS` | Single-page mythos terminal — the multiplanetary desktop: boot screen, draggable windows, Mars clock, a static Starship stat panel, a static news panel, command prompt. `index.html` + `README.md`, no build step. | `b9bcbd2` 2026-07-29 02:47 +1000 | `5af57a4` 2026-07-29 02:52 +1000 | 5 / 2 |
| `CrystalCore-AERIS` | The AERIS Edition of the same terminal, plus `ALIGNMENT_PROTOCOL.md` (a multi-LLM unity charter) and a `website/` directory. | `fde9a56` 2026-07-29 03:04 +1000 | `c8f0d95` 2026-07-29 04:06 +1000 | 5 / 4 |
| `crystalcore-os-aeris-vault12` | **The specification home for Starline edge nodes and the Consent Token.** Seven technical specifications (see the Statement below), plus the AERIS / Vault 12 terminal page and its README. | `1348a80` 2026-07-29 05:57 +1000 | `a09943c` 2026-07-29 (docs: complete technical document set + NON SOLUS) | 10 tracked files |
| `teraustralis-incognita-v2` | The largest of the five: a React 19 + TypeScript + Vite + Tailwind application (65 `.tsx` files) with an Express static server, built on a Manus generator scaffold. Co-authored by `Manus` — the only non-maintainer author anywhere in the portfolio since `The-Crystal-Vision`'s bot commits. | `7fa231c` 2026-07-24 14:14 UTC | `3762968` 2026-07-28 20:22 UTC | 4 / 90 |
| `teraustralis-v2-presentation` | The deck for the above: 13 standalone HTML slides plus a presentation script, slide notes, and slide state. | `f056b9c` 2026-07-28 20:22 UTC | `d4fae1e` 2026-07-28 20:29 UTC | 3 / 17 |

### Evidence
- Tier A (git object database), read from local clones 2026-07-28: root
  and head commit hashes, author dates, commit counts, and
  `git ls-files` counts exactly as tabulated.
- Tier A: `git log --format='%an'` gives `Crystal Arena-Turner` as sole
  author for the three terminal repositories, and
  `CrystalArchitect` + `Manus` for `teraustralis-incognita-v2`.
- Tier C: each repository's own `README.md`.

### Historical Notes
`00-INDEX.md` opens "from a full read of the six-repository
CrystalArchitect portfolio," and this map's own heading said "all six
repositories." Both were accurate on 2026-07-24: `CrystalCore.OS`,
`CrystalCore-AERIS`, and `crystalcore-os-aeris-vault12` did not exist
yet (their root commits are 2026-07-29 +1000, i.e. after the
reconstruction), and `teraustralis-incognita-v2` had existed for ten
days without being surveyed. `teraustralis-v2-presentation` was created
2026-07-28. So this is one genuine omission at the time
(`teraustralis-incognita-v2`) and four repositories that arrived after
the archive was written — not a reconstruction error, but a ledger that
had not been re-run.

**Corrected 2026-07-29: this table asserted the defect it documents.**
The `CrystalCore.OS` row read "Mars clock, **Starship telemetry**, news
feed" — under a Statement graded **Implemented**, which asserts that
telemetry is what the panel is. It is not, and Parts 5, 6 and 9 of
`11-CORRECTIONS.md` are entirely about that phrase: the window titles a
static stat block with zero network calls behind it. Every other
occurrence of "Starship telemetry" in this archive sits inside quotation
marks, being *discussed* as a false claim. This row was the only place
the archive stated it in its own voice, and it went unnoticed through
five corrections that were about exactly this. The row now says "a static
Starship stat panel, a static news panel." Nothing else in the row
changed, and the defect in `CrystalCore.OS` itself remains live and
unfixed by the maintainer's decision — see Part 9's "identified, not
applied" table.

### Cross References
`11-CORRECTIONS.md`, `01-SYSTEM-OVERVIEW.md`,
`FULL-REVIEW-2026-07-28.md` (root of this repository).

---

## Statement

The two single-page terminal repositories (`CrystalCore.OS` and
`CrystalCore-AERIS`) are variants of one another, not independent works,
and neither is the mythos terminal the umbrella ships.
`crystalcore-os-aeris-vault12` carries a third variant of the same page,
but is **not** primarily a terminal repository — see the correction below.

**Status: Implemented** (read from the files themselves).

> **Correction (2026-07-28, same day).** This Statement first read "the
> three single-page terminal repositories," counting
> `crystalcore-os-aeris-vault12` as a third variant and nothing more, and
> the table above described it as `index.html`, `logo.jpg`, and a README.
> That was measured against a clone taken at 20:45 UTC. The seven
> specification documents below landed on its `main` after that, and the
> archive described a specification repository as a single-page artefact.
> The error is the one this archive exists to prevent — a claim outliving
> the evidence it was drawn from — so it is corrected in place and left
> visible rather than quietly rewritten. Re-read from `origin/main`
> 2026-07-28 21:5x UTC.

The umbrella's `mythos/crystalcore-os/crystalcore_os.py` — the terminal
`STATUS.md` lists under "Running" — is a Python program with save/resume
that plays to the First Gate. These three are browser pages: an HTML
boot screen, draggable windows, and a command prompt with a fixed
command set (`help`, `clear`, `mars`, `starship`, `status`, `about`,
`reboot`, and in the AERIS cuts `vault`, `aeris`, `activate`, `node`).
They share the same command-dispatch structure and differ mainly in
theming and in which commands exist. Same name, same fiction, different
artefact and different lineage.

### Evidence
- Tier A: `CrystalCore.OS/index.html`, `CrystalCore-AERIS/index.html`,
  and `crystalcore-os-aeris-vault12/index.html` read in full
  2026-07-28; the first two carry near-identical terminal handlers
  (`crystal@core:~$` vs `aeris@vault12:~$` prompts).
- Tier C: `TerAustralis-Incognita/STATUS.md`, "Running" section,
  describing the Python terminal as a separate artefact.

### Historical Notes
None — first recorded here.

### Cross References
`06-COMPONENTS.md`, `09-GLOSSARY.md`.

---

## Statement

`crystalcore-os-aeris-vault12` holds the **Starline Consent Transport
specification set** — seven documents, all dated 2026-07-29, covering
edge-node hardware tiers, the Consent Token, the Keeper role, the Tier 0
runtime loop, canonical lattice status messages, and Noise IK + token
verification for constrained devices.

**Status: Exists as a document** (all seven read in full; they specify
behaviour, they do not implement it).

| Document | Lines | What it fixes |
|---|---|---|
| `STARLINE-EDGE-SPEC.md` | 117 | Hardware tiers 0 / 1 / 2 / R, power envelopes, model sizes |
| `STARLINE-EDGE-NODE-ARCHITECTURE.md` | 156 | Layered node design |
| `CONSENT-TOKEN-SCHEMA.md` | 129 | Token structure, lifecycle, revocation mechanics |
| `AELTHARION-KEEPER.md` | 78 | The Keeper as a technical role |
| `TIER0-RUNTIME-LOOP.md` | 154 | Duty cycle, Lumina tick, Power Governor |
| `LATTICE-STATUS-MESSAGES.md` | 87 | Canonical boot/status messages, incl. NON SOLUS |
| `NOISE-IK-CONSENT-VERIFICATION.md` | 122 | Minimal verification steps for constrained nodes |

### Evidence
- Tier A: `git ls-tree -r origin/main` and `git show origin/main:<file>`,
  read 2026-07-28. Head `a09943c`, "docs: update README with complete
  current technical document set + NON SOLUS".

### Historical Notes
See the correction in the Statement above: an earlier version of this
map described this repository as a single-page terminal artefact,
measured before these documents landed.

### Cross References
`03-ARCHITECTURE.md`, `06-COMPONENTS.md`, and the Statement below on how
this specification relates to the running code.

---

## Statement

The Starline specification in `crystalcore-os-aeris-vault12` and the
running Starline implementation in `TerAustralis-Incognita-Code`
(`core/crystal-core/consent_transport/`) describe the same protocol at
the transport layer and **diverge at the consent layer**. The transport
half is built; the Consent Token half is designed, not built.

**Status: Implemented** (the Noise IK transport and per-peer consent
gate) **and Designed, not built** (Consent Tokens, expiry, scope,
propagatable revocation).

> **Superseded 2026-07-29 — the consent layer no longer diverges.** The
> statement above was accurate when written at 2026-07-28 21:57 UTC. PR
> #34, *"Consent Tokens: reference implementation of the v0.1 schema"*,
> merged into `TerAustralis-Incognita-Code` at 2026-07-29 03:42 UTC —
> about five and three quarter hours later — and builds all four of the
> things listed as designed-only. It is left standing, dated, rather than
> rewritten, per this file's practice.
>
> `consent_transport/token.py` (344 lines) implements the schema and
> names `CONSENT-TOKEN-SCHEMA.md` v0.1 as its source; `consent.py` gained
> 181 lines, and the token layer is wired into `transport.py` and
> `agent.py` rather than standing beside them.
>
> Each of the four is exercised by a named test, not merely present:
>
> | Was "designed, not built" | Now covered by |
> |---|---|
> | Consent Tokens | `test_purpose_is_mandatory`, `test_identity_binding_cannot_be_skipped`, `test_tampering_with_any_field_breaks_the_signature` |
> | Expiry | `test_token_expires`, `test_expired_token_stops_the_exchange_that_a_live_one_allowed` |
> | Scope | `test_token_grants_only_what_its_scope_names`, `test_token_scope_is_enforced_over_a_real_connection`, `test_byte_budget_is_enforced_and_refuses_an_oversized_transfer` |
> | Propagatable revocation | `test_revocation_kills_the_token_and_is_signed`, `test_forged_revocation_is_refused`, `test_revocation_gossiped_from_the_real_issuer_is_honoured` |
>
> `python -m consent_transport.selftest` reports **32/32 passing**, up
> from 9, verified by running it 2026-07-29. `ci.yml:43` runs that same
> command, so the coverage is enforced rather than incidental. Several
> tests drive a real socket — `test_token_scope_is_enforced_over_a_real_connection`
> and `test_byte_budget_stops_a_batch_midway_on_the_wire` — so this is
> Built in the strong sense, not a schema with a struct behind it.
>
> The conformance table below predates the token layer and describes only
> the transport half. It is still true; it is no longer the whole picture.

**Where the code already meets the spec:**

| Spec | Implementation |
|---|---|
| `NOISE-IK-...` §5 — pattern `-> e, es, s, ss` / `<- e, ee, se`, pre-message `<- s` | `noise.py` `MESSAGE_PATTERNS` is exactly this; mutual auth and forward secrecy hold |
| `CONSENT-TOKEN-SCHEMA` §3 — Ed25519 over *canonical* serialization, deterministic field order, no whitespace | `ConsentReceipt._signable_bytes()` uses `json.dumps(..., sort_keys=True, separators=(",", ":"))` |
| `NOISE-IK-...` §7 — "Fail closed: any doubt → reject" | `is_granted()` returns `False` when no receipt exists; unpaired peers denied; unverifiable fragments dropped |
| `CONSENT-TOKEN-SCHEMA` §4.5 — revocation immediate | Consent is re-checked per request, so a revoke lands on the very next connection; covered by `test_revocation_takes_effect_next_request` |
| "No central authority" | Receipts are local, signed by the local identity; no registry anywhere |

**Where the spec describes something the code does not have:**

1. **There is no token.** Consent is a per-peer boolean —
   `ConsentReceipt{peer_fingerprint, granted, ts}` — not a token with
   `token_id`, `purpose`, `scope`, `constraints`.
2. **No expiry.** `expires_at` is required by the schema and `§4.6` calls
   it a hard wall-clock wall. `is_granted()` has no time bound at all: a
   grant is eternal until explicitly revoked. This is the widest gap —
   the verification doc's "time binding" step has nothing to check.
3. **No scope.** The schema allows `shard_ids`, `shard_class`,
   `max_bytes`. In code, consent is all-or-nothing per peer. The `kinds`
   filter in `fragment_provider` is the *requester's* preference, not a
   consent-enforced ceiling — a consented peer may ask for any kind.
4. **Revocation does not propagate.** The schema makes revocation a
   signed message carrying `token_id` and `revoked_at` that any node
   honouring it must treat as final. In code, revocation is a local
   receipt; nothing transmits it. `consent.py`'s own docstring is honest
   about the consequence: it stops future requests, and cannot reach data
   a peer already holds.
5. **Recipient binding is indirect.** The schema binds a token to *both*
   identities. `ConsentReceipt` names only the peer and is signed by the
   local identity, so the issuer is implicit; the two long-term keys are
   tied together by the `PeerStore` pairing record rather than by the
   consent artefact itself.

### Evidence
- Tier A: `consent_transport/noise.py`, `consent.py`, `transport.py`,
  `peers.py`, `fragment.py` read in full; the four Crystal Core suites
  executed 2026-07-28 (51/51, and 13/13 for `consent_transport` after
  hardening).
- Tier C: `CONSENT-TOKEN-SCHEMA.md` §§2–5 and
  `NOISE-IK-CONSENT-VERIFICATION.md` §§3–7.

### Historical Notes
First recorded here. The specification postdates the implementation: the
`consent_transport` module was imported under Migration-Plan Stage 1,
and these documents were written 2026-07-29.

### Cross References
`06-COMPONENTS.md`, `FULL-REVIEW-2026-07-28.md`.

---

## Statement

The canon → site copy pipeline has drifted in **two** documents, not the
one this archive previously recorded — and nine canon documents have
never been copied to the site at all. The remaining differences are
correct and expected, not drift.

**Status: Unresolved** (the drift and the uncopied set), **Implemented**
(the pipeline itself).

Measured across all 24 documents in the umbrella's `mythos/content/`
against `TerAustralis-Incognita-Code/vision/site/src/content/`,
2026-07-28:

| State | Count | Documents |
|---|---|---|
| In sync, byte-identical | 5 | `SPONSORS`, `STARLINE-TRANSMISSIONS`, `THE-FULL-NARRATIVE`, `THE-SOVEREIGN-KEY`, `VISION` |
| Differ **only** by relative-link depth | 7 | `MEMORY`, `STRATEGY`, `CRYSTALMATRIX`, `GOVERNANCE`, `LUMINA`, `MILESTONES`, `LICENSE-CONTENT` |
| **Real content drift** | 2 | `CODEX`, `APOCRYPHON` |
| Filename collision — two different works | 1 | `ARCHITECTURE` |
| **Never copied to the site** | 9 | `CRYSTALCORE-OS-VISION`, `FERMIS-SILENT-LINE`, `MOTIFS`, `RED-DUST-AXIS`, `SHOOTING-STAR-GIRL`, `THE-FIRST-REMEMBERING`, `THE-IN-GEAR-PROTOCOL`, `THE-SOVEREIGN-GAP`, `WIRE-SKULL-MEMORY` |

**The seven "differences" that are not drift.** Each differs by exactly
one line, and always the same line: a footer link reading
`[README](../README.md)` in the umbrella and `[README](README.md)` on the
site. The file sits at a different depth in each tree, so the relative
link *must* differ. This is the copy step working correctly. Any future
audit that counts these as drift will overstate the problem — as a first
pass of this one did.

**The two real drifts.**

- `CODEX.md` — canon is a strict superset: 149 lines against the site's
  73. Six whole sections exist only in canon: *The Red Dust Remembers*,
  *The Northern Dream*, *The Awakening*, *The Bridge Between Worlds*,
  *The Sovereign Heart*, *The New Axis*. Nothing exists only on the site.
  Canon grew; the copy was never refreshed.
- `APOCRYPHON.md` — the site copy omits the cover-image line
  `![The Apocryphon of Crystal — Australian Anchor Edition](assets/apocryphon-cover.jpeg)`.
  Whether that is drift or a deliberate difference in how the site
  handles imagery is **not determined here**.

**`ARCHITECTURE.md` is a collision, not a copy.** The umbrella's is
"Architecture — TerAustralis Incognita", a design overview that opens by
saying most components remain at concept stage. The site's is "Crystal
Universe — System Architecture · Decode · Ingest · Upgrade", a
Built-vs-Vision map. Two different documents sharing a filename. Treating
them as two copies of one document — as a filename-matching audit will —
is wrong in both directions.

### Evidence
- Tier A: SHA-256 over both trees, plus `diff` per document, run
  2026-07-28 against `origin/main` of both repositories. Direction of
  drift established by counting `<` and `>` lines separately, precisely
  so that "sync them" could be judged safe or destructive rather than
  assumed.

### Historical Notes
An earlier Statement in this file recorded the canon→site drift as a
single live instance (`THE-FIRST-REMEMBERING.md` not yet copied). That
was true of the file it named and understated the set: nine documents
have never been copied, and two of those that were have since diverged.

### Cross References
`FULL-REVIEW-2026-07-28.md` (finding M6), `04-GOVERNANCE.md`.

---

## Statement

A twelfth repository exists: `teraustralis-proposal`, created 2026-07-29
20:17 and **public**. It is the only repository in the portfolio
addressed to people outside the project — a formal proposal package
seeking technical review and partnership, published under an ABN with a
named founder.

It holds **no code**. Seven numbered documents (`01-PROBLEMS.md` through
`07-INVESTMENT-THESIS.md`), a `README.md` and a `LICENSE`. Nothing to
build, nothing to run, no CI.

Two things distinguish it from every other repository here.

**It diverges on licence.** ADR-0013 sets CC-BY-NC-ND 4.0 portfolio-wide.
This repository is **All Rights Reserved**, refusing permission to "copy,
reproduce, or redistribute" or to "build upon, implement, or
commercialise any of the ideas" without written consent. That is a
defensible choice for a proposal under evaluation — the reasoning is
different from the reasoning for canon — but it is an undocumented
divergence from an accepted ADR, and ADR-0009 requires licensing changes
be recorded.

**It restates CrystalCore for a reader who has never seen it.**
`05-TECHNICAL-BRIEF.md` describes the same architecture that
`crystalcore-os-aeris-vault12` specifies and
`TerAustralis-Incognita-Code` implements. That is a third copy of a
description whose canonical homes are elsewhere, and it is the copy most
likely to be read by someone with money and no context.

**Status: Exists as a document** (prose only, nothing executable).

### Evidence
- `origin/main` at `829156b`, read 2026-07-29. Twelve commits, from
  `9698d7e` at 20:17 to `829156b` at 20:54 — **thirty-seven minutes** of
  history at the time of survey.
- Zero files under `.github/`: no CI, no deploy workflow.
- Licence history: MIT until `4bfb860` ("Replace MIT with All Rights
  Reserved — view only"), strengthened at `4bbe185` (ABN added).
- `05-TECHNICAL-BRIEF.md` §Core Properties, checked against
  `TerAustralis-Incognita-Code` at `f81dc37`: of six properties asserted
  in the present tense, one held fully, two held partly, and one —
  "fail-safe isolation" — was not implemented at all. Reported to the
  maintainer 2026-07-29 with a correction patch.

### Historical Notes
The archive did not know this repository existed until 2026-07-29, when
a survey prompted by an unrelated question happened to list the account's
repositories and returned twelve rows where the archive expected eleven.
Nothing in the method would have surfaced it otherwise — the same gap
recorded in `11-CORRECTIONS.md` Parts 0, 10 and 11, now in its fifth
instance. See Part 16.

A pre-restructure duplicate document set (`VISION.md`, `PROPOSAL.md`,
`TECHNICAL-BRIEF.md`, `GEOGRAPHIC-BRIEF.md`, `INVESTMENT-THESIS.md`) was
present at survey time, unreferenced and diverged from the numbered set
that superseded it. Notably the older `TECHNICAL-BRIEF.md` carried a
`## Current Status` section — "this brief states the design intent" —
which the restructure at `c0a7c63` dropped. The honesty label existed
first and was lost in reorganisation, which is how the numbered version
came to read as a description of a built system.

### Cross References
`STATUS.md` (per-repo ledger), `SURVEYED.md`, `11-CORRECTIONS.md`
Part 16, `04-GOVERNANCE.md` (licensing, ADR-0009 and ADR-0013).

---

## Statement

`crystal-vision` was **renamed** to `CrystalCore-Starlines-and-Dreamlines` on
2026-07-29 and now publishes via GitHub Pages rather than Vercel. It is the
same repository — GitHub redirects the old name, so both resolve — and the
portfolio still holds **twelve**. *(True on 2026-07-30. Eleven from
2026-08-08 — see the scope correction at the head of this document.)*

Every Statement above that names `crystal-vision` remains correct as a claim
about its date. This entry exists so that a reader looking for that name today
finds where it went, rather than concluding the repository is missing or that
a new one has appeared.

**Status: Implemented** (verified against live GitHub metadata, not inferred
from file contents).

### Evidence
- GitHub API returns id **1304095452**, `full_name:
  CrystalArchitect/CrystalCore-Starlines-and-Dreamlines`, for *both*
  `CrystalArchitect/crystal-vision` and the new name. One id, one repository.
- `git ls-remote` against a clone whose `origin` is `…/crystal-vision`
  returns `6364d0d`, the head of the renamed repository.
- Head `6364d0d`, read 2026-07-30. Still private.

### Historical Notes
An assistant first read this as a *thirteenth* repository holding a duplicate
of `crystal-vision`, on the evidence that all twelve shared files were
byte-identical, and drafted entries here, in `STATUS.md` and in `SURVEYED.md`
raising the count to thirteen. That was wrong, was caught by this archive's own
freshness check reporting an impossible shared head commit, and was discarded
before it was committed. Recorded in `11-CORRECTIONS.md` Part 18.

Two defects found in the repository during that survey were real and were
corrected the same day: two GitHub Actions workflows racing to publish Pages
(both succeeding, the later winning), and a README that still identified the
repository by its former name.

### Cross References
`STATUS.md` (per-repo ledger), `SURVEYED.md` (rename is invisible to a
name-keyed survey — see its Known limits), `11-CORRECTIONS.md` Part 18.

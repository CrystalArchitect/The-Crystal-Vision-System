# Library sync — 5 August 2026

> **Accession plate**
>
> - **Record type:** accession and survey record (the Library's own ledger)
> - **Date:** 5 August 2026
> - **Source label:** model (Claude, in a steward-directed Claude Code
>   session on branch `claude/crystalcore-library-sync-x47316`)
> - **Layer:** Docs-governance
> - **Status:** active
>
> By the constellation's working rule, nothing below enters any record as
> fact on this document's say-so alone: every claim here cites what it was
> checked against, and the whole record passed the steward gate as a pull
> request.

## 1. What the steward supplied

Five files were uploaded to the session, alongside one pasted message:

| Supplied | What it is |
|---|---|
| `TERAUSTRALISMASTERPLAN_2.md` | The 1 August 2026 master plan |
| `CrystalEcosystem_FullRepositoryReview.md` | Manus AI's 29 July 2026 nine-repository review |
| `weboseastereggs.skill` | A zipped Claude Code skill: `web-os-easter-eggs` (SKILL.md, two references, three templates) |
| `SKILL_2.md` | An earlier, shorter revision of the same skill's SKILL.md — superseded by the zip's copy, which adds an extension workflow, a Vite fast-refresh warning, and a spoiler-safe handover step |
| `App.tsx` | A target version of `teraustralis-incognita-v2`'s router, adding Terminal (`/crystalcore-os`), Gallery, a soundscape context and a global audio player |
| (pasted message) | An external AI assistant's four-item "missing material" synchronisation list — assessed in §3 |

## 2. What was accessioned where

| Material | Destination | Label |
|---|---|---|
| Master plan | `plans/2026-08-01-teraustralis-master-plan.md` (this repository) | steward-supplied consolidation; Docs-governance |
| Manus review | `reviews/2026-07-29-crystal-ecosystem-full-repository-review.md` (this repository) | model; claim, accurate to its date |
| Loop Framework | already here; moved from the repository root to `frameworks/loop-framework.md`, byte-identical | human (steward); Method |
| `web-os-easter-eggs` skill | `teraustralis-incognita-v2` → `.claude/skills/web-os-easter-eggs/` | tooling for a future Terminal build; the zip's newer SKILL.md used |
| Target `App.tsx` | `teraustralis-incognita-v2` → `docs/TARGET-APP-STRUCTURE-2026-08-05.md`, embedded verbatim and labelled Vision | Vision — a target, not a claim about what runs |
| Loop Framework cross-reference | `TerAustralis-Incognita` → `docs/governance/AI-Governance.md` | Docs-governance |
| Constellation observations | `TerAustralis-Incognita` → `docs/REPOSITORIES.md` (dated accretion); `CrystalCore.OS-the-Crystal-Architecture-Archive` → `knowledge-base/11-CORRECTIONS.md` (filed Part 20) | Docs-governance |

The `SKILL_2.md` upload was not accessioned separately: it is an earlier
revision of a file the zip carries in full, and shelving both would invite
drift. This row is its record.

## 3. The external synchronisation list, checked

The steward pasted a message from an external AI assistant ("I've checked
your recent project documentation … across your personal history")
enumerating four bodies of "missing material … to bring to Claude to
update your website and repositories". **Source label: model
(external assistant); tier: claim.** Per the Incognita Rule it was checked
against the constellation rather than taken as a work order. Claim by
claim:

**3.1 "The CrystalCore.OS & Architecture Documentation — separation of
interpretation, observation, evidence, and authority; operational
protocols for critical distance."**
Surveyed — it exists under the constellation's own names. Separation of
observation from interpretation is the Incognita Rule and the Belt-Three
labels (`TerAustralis-Incognita/docs/governance/The-Incognita-Rule.md`);
separation of evidence from authority is the evidence rule and the
maintainer's veto (`docs/governance/AI-Governance.md`); the operational
protocols for critical distance are the Loop Framework's §7
(`frameworks/loop-framework.md`). Nothing new was imported; the mapping is
recorded here so the vocabulary drift is visible.

**3.2 "The Loop Framework Integration — Method vs. Logos distinction;
bridge classification."**
Surveyed — real and already held. `frameworks/loop-framework.md` carries
both named tools (§5: Method vs. Logos; Story as Bridge vs. Story as
Loop). "Integration" was performed this session as a cross-reference from
the umbrella's `AI-Governance.md`, so AI sessions bound by canon law can
find it. The framework remains what it declares itself to be: provisional
Method, revisable by its own §8, never law.

**3.3 "Project Ecosystem: The Library — tech stack specs: Next.js, React,
TypeScript, and Tailwind."**
Partly wrong as at 2026-08-05. This repository contains no application
code. The active site, `teraustralis-incognita-v2`, is **Vite + React 19 +
TypeScript** with a shadcn/ui component set and Tailwind utilities — not
Next.js (evidence: its `package.json` and `vite.config.ts`). The one
Next.js artefact in the constellation's records is the rolled-back
MemoryCore reference app, which exists only as `memorycore-repo.zip` in
the steward's hands (master plan §8). The claim looks like a conflation of
the two; recorded, not imported.

**3.4 "Research & Framework References — 'A Limited Electronic Agent
Framework for Advanced AI in Australia'; 'Terra Australis Hyperloop
Incognita'."**
Unverified. A case-insensitive search of all eleven session-visible
repositories for "limited electronic agent" and "hyperloop" returned **no
occurrences** in either name's direction. Neither document exists in the
constellation as at 2026-08-05. Not accessioned. If these exist in the
steward's files or the external assistant's history, supplying them to a
future session would let them enter through the gate properly; until then
they are claims about documents, not documents.

## 4. Constellation survey, as far as this session could see

Scope: eleven repositories were in the session's reach, each on branch
`claude/crystalcore-library-sync-x47316`, clones on disk. The session
could **not** enumerate the GitHub account, query repository metadata, or
read repositories outside its scope — so this is a survey of eleven, not a
count of the constellation.

| Repository (GitHub name, 2026-08-05) | Identity, as evidenced |
|---|---|
| `TerAustralis-Incognita` | Umbrella — canon, governance, mythos |
| `TerAustralis-Incognita-Code` | Engine — Crystal Core + Crystal Vision code |
| `CrystalCore.OS-the-Crystal-Architecture-Archive` | The ledger — evidence-based knowledge base; its `02-REPOSITORY-MAP.md` remains the governing map |
| `Clementine---Local-Soveriegn-Edge-AGI` | README self-identifies as **The Crystal Vision** — codex site + Clementine companion (the repository the July review calls `The-Crystal-Vision`) |
| `TheCrystalVision` | README self-identifies as **Crystal Core — the protocol pack** (the repository the July review calls `crystalcore`) |
| `CrystalCore-Starlines-and-Dreamlines` | Renamed from `crystal-vision` on 2026-07-29 (Archive ledger, Part 18, confirmed by GitHub id there). Formerly classified "frozen — provenance only"; commits continue through 2026-07-31 (`GROK_BUILD.md`, `BUILD_MANIFEST.json`, site files), so that classification no longer holds |
| `CrystalCore.OS` | Web-OS v0.1, single-file HTML desktop |
| `teraustralis-incognita-v2` | Active site — Vite + React 19 + TypeScript, "Deep-Time Dreaming" |
| `teraustralis-v2-presentation` | Presentation deck for v2 |
| `teraustralis-proposal` | The twelve-document proposal package |
| `the-library` | This repository — created 2026-08-03, built out by this sync |

Observations worth a future session's attention:

- **Two renamings are new since the Archive's last filing.** The July
  names `crystalcore` and `The-Crystal-Vision` now answer to
  `TheCrystalVision` and `Clementine---Local-Soveriegn-Edge-AGI`. Evidence
  here is content-correspondence (each clone's README still opens with its
  old identity) plus the session's scope list naming the new spellings as
  current; the decisive test — comparing GitHub's stable repository ids,
  as the Archive's Part 18 prescribes — needs account metadata this
  session did not have.
- **Sibling maps have drifted.** Both renamed repositories still carry
  sibling maps written for the old constellation (including a
  `teraaustralis` double-'a' spelling contrary to ADR-0007). Left
  untouched: redrawing them correctly needs sight of the whole account.
- **Not visible from this session:** `CrystalCore-AERIS` and
  `crystalcore-os-aeris-vault12` (of the July twelve), and anything
  created since the-library. Their state is unknown here, deliberately
  unasserted.

## 5. Deliberately not done

- **No map was redrawn.** The Archive's `02-REPOSITORY-MAP.md` governs and
  needs a full-account pass; a map from a partial survey would be
  confident wrong cartography — the failure this project is named for.
- **No sibling-map rewrites** in the renamed repositories, same reason.
- **No Terminal or Gallery was built** in `teraustralis-incognita-v2`. The
  target structure and the skill are now in that repository; building is
  its own steward-directed work.
- **No deployments, no visibility changes, no licence files.** The
  master plan logs an unrequested deploy as the boundary violation it was;
  everything in this sync entered as branch + pull request only.
- **`the-library` still has no `LICENSE`.** The constellation carries at
  least three licence postures (Apache-2.0 history, CC BY-NC-ND 4.0,
  All Rights Reserved) and the 1 August decision made Clementine and
  CrystalCore code all-rights-reserved. Which posture the Library takes is
  the steward's call.

## 6. Open follow-ups

1. Steward: confirm or correct the two rename observations (§4), ideally
   by the Archive's id-keyed method.
2. Steward: decide the Library's licence and whether "The Library" is the
   public face of the MemoryCore design (master plan §6 asked for one
   name).
3. A full-visibility session: refresh the Archive map, `STATUS.md`,
   `SURVEYED.md`, and the drifted sibling maps in one pass.
4. The two unverified references (§3.4): supply the documents or retire
   the claims.
5. `teraustralis-incognita-v2`: build Terminal and Gallery to the target
   structure; the easter-egg skill is installed and waiting.

---

## Addendum — 2026-08-05, later the same session

**A.1 A second delivery.** After the record above was written and the pull
request opened, the steward supplied eight more files with no accompanying
instruction: a Python/FastAPI implementation of The Library (`main.py`,
`requirements.txt`, README) and the configuration shell of a Next.js
implementation (README, `next.config.js`, `tailwind.config.ts`,
`tsconfig.json`, `postcss.config.js`). Both are titled "The Library —
Clementine & Rex". They are accessioned verbatim under `app/python/` and
`app/next/`. Two files are session-authored rather than steward-supplied
and are labelled as such here: `app/python/.env.example` (one line,
derived from `main.py`'s documented requirement) and the repository
`.gitignore` (which exists chiefly so a real `.env` can never be
committed to the Library).

**A.2 §3.3 revised by accretion.** The record above judged the external
list's "Next.js, React, TypeScript, and Tailwind" claim partly wrong
because no such code was visible in any repository. The second delivery
revises the verdict: a Next.js + TypeScript + Tailwind implementation of
The Library exists in the steward's hands, and its shell is now here. The
claim described real material that had not yet been supplied — which is
precisely the gap this library exists to close. The other half of the
assessment stands: the active site (`teraustralis-incognita-v2`) remains
Vite + React 19, not Next.js.

**A.3 What is still missing.** The Python app's landing page routes both
rooms to `static/chat.html`, which was not supplied — the doors render
but do not yet open. The Next.js variant is configuration only: no
`package.json`, no `app/` tree, no `lib/grok.ts` (the latter two named by
its own README). Nothing was scaffolded in their place — generating
stand-ins for files that exist on the steward's machine would
manufacture drift. Supply them, or direct a build, and this record gains
a line either way.

**A.4 Review notes for the steward (code read, not executed here).**
Labelled claims from reading, deliberately not fixed in a sync session:
(i) `main.py` appends each persona prompt with the SDK's `assistant(...)`
helper rather than a system-role message, so the model receives its
instructions as a prior turn of its own speech; (ii) CORS is configured
with wildcard origins *and* credentials enabled, a combination browsers
refuse; (iii) the SSE writer emits raw chunk text after a single `data:`
prefix, so any chunk containing a newline breaks the stream's framing;
(iv) the async route iterates the SDK's synchronous stream, blocking the
event loop while sampling; (v) the model id `grok-4.5` should be
verified against the current xAI catalogue at build time. None of these
prevents a local demonstration; all five deserve a decision before
anything public.

**A.5 The name Clementine, a third time.** The Archive's corrections
ledger (Part 17) records the cost of one name meaning different systems
in different places, and asks that new work check the portfolio for a
name before adding to it. This delivery adds a third live use: the bus
hub (`TheCrystalVision`, in `clementine/`), the sovereign companion
(`Clementine---Local-Soveriegn-Edge-AGI`), and now The Library's
librarian persona over the xAI API. The master plan (§7) describes
Clementine as "the Librarian … the archive's living interface" — which
this app plainly is — so the recurrence may be convergence rather than
collision; naming stays the steward's call, and the recurrence is now on
the record. Rex is new, with no prior use anywhere in the eleven visible
repositories. Both presences are described throughout in the steward's
own words, including her pronoun choices for them, which these files set
on the record.

**A.6 A third delivery.** Five more files arrived for the Next.js
variant. Two are
new and are accessioned verbatim: `package.json` (the app is named
`the-library` — the repository's own name, settling where this variant
belongs; Next 14.2.5, React 18.3, `marked` + `highlight.js`, and a
`check-key` guard run before `dev`/`start`) and the auto-generated
Next.js type shim, received under the name `nextenv.d.ts` and placed at
its conventional path `app/next/next-env.d.ts`, which is the name the
supplied `tsconfig.json` includes — the received spelling is noted here
so the placement is an inference on the record, not a silent rename. The
other three (`postcss.config.js`, `tailwind.config.ts`,
`next.config.js`) are byte-identical to the second delivery's copies and
changed nothing. Still missing, updated: the `app/` tree, `lib/grok.ts`,
and — newly named by `package.json` itself — `scripts/check-key.js`,
without which `npm run dev` and `npm run start` fail at the first
command. One further review note in the A.4 series: (vi) `package.json`
carries no `tailwindcss`, `autoprefixer` or `postcss` in its
devDependencies, yet `postcss.config.js` loads both plugins — as
supplied, `next build` stops at PostCSS with a missing-module error, so
the dependency block needs completing when the app tree arrives.

**A.7 A fourth delivery — three shelved, one accessioned as a work, one
held at the gate.** Five more files arrived, again without instruction.

*Shelved.* The Manus AERIS / VAULT 12 exploration report (self-dated 28
July 2026) joins `reviews/`; the mini-OS working notes (received as
`notesassets.md`) and the AERIS build task log (received as `todo.md`)
open a `notes/` shelf. All three describe the Manus-hosted AERIS site,
whose code lives outside the eleven repositories visible to this session
— these documents are that build's only durable provenance in the
constellation, which is exactly the "disk is canon, chat is not" rule
doing its work. The task log's completions are its author's claims, not
re-verified here. The notes file's terminology rule — avoid "Songlines"
in UI copy — is consistent with the umbrella's Indigenous-knowledge
boundary and is now on the record.

*Accessioned as a work.* `transmissions/red-dust-axis.mp3` (received as
`reddustaxis.mp3`; placed under the canon spelling) opens a
`transmissions/` shelf for the Starline Transmissions. It is a 5.2 MB
MPEG layer-III stereo file with an ID3v2.4 header carrying no title or
artist frames a shallow read could find; its audio content was not
auditioned in this session. Two flags: (1) **licensing** — the master
plan marks Suno-generated tracks after 6 June 2026 as
non-commercial-only until subscription status is verified, and this
recording's generation date is not in evidence, so the flag applies
until the steward says otherwise; (2) **repository weight** — this is
the Library's first binary work; the 29 July review already recommends
Git LFS for the constellation's art-heavy histories, and if the other
ten catalogued recordings follow this one in, LFS should come first.

*Held at the gate.* `taskmarket.skill` (version 2026-07-20, author
Daydreams Systems) is a third-party Claude Code skill for operating an
on-chain USDC task marketplace on Base: wallets, escrow, payments,
auctions, legal-bundle acceptance — 28 files, inspected in full in the
session's scratchpad and **not committed anywhere**. Two reasons, both
steward decisions rather than judgment calls this record is entitled to
make: (1) installing a skill makes it live behaviour for every future AI
session in that repository, and this one moves real money; (2) it is
third-party content whose redistribution terms are not in evidence, in
a repository whose visibility this session could not determine. The
Archive's ledger Part 10 set the precedent: inbound material is checked
and quarantined until cleared. If the steward wants it active, one line
of direction — which repository, and confirmation she holds
redistribution rights or accepts the risk — puts it there in minutes.

**A.8 A fifth delivery — the archive's face arrives.** Four App Router
files for the Next.js variant, placed under `app/next/app/`: `layout.js`,
`page.js`, `globals.css`, and `entry-card.js` (received as
`entrycard.js`; the hyphenated name is required by `page.js`'s own
`./entry-card` import — inference on the record). Three observations:

1. *This is the MemoryCore front-end.* The pages query `mc_entries`
   through a Supabase client, render provenance chips, receipts,
   consent-gated domain markers and tombstone-banner styles — the master
   plan §5 PRD's front-end rules, visibly implemented — and
   `globals.css` carries §5's owner-approved design language
   **token-for-token** (`#0A0C10`, `#0D1117`, `#00E5CC`, `#F5A623`,
   `#7C3AED`, JetBrains Mono). What §8 recorded as rolled-back exists
   and is coming in through the gate.
2. *The §6 naming decision is now visible inside one app.* The
   `package.json` names the project `the-library`; `layout.js` titles
   and brands it **MemoryCore — The Living Archive of TerAustralis**.
   One app, both names — the "pick ONE for the public face" decision the
   master plan asked for is no longer abstract.
3. *The two skins are now distinguishable.* `globals.css` contains no
   Tailwind directives — these archive pages are plain CSS — while the
   earlier-delivered Tailwind/PostCSS configs carry the Clementine & Rex
   palette. As supplied, the Tailwind configs are used by no delivered
   page, which reframes review note (vi): the missing-dependency problem
   is real only if the Clementine & Rex skin joins this same project;
   the archive pages as delivered need no Tailwind at all.

Missing set, restated: `lib/supabase.js` (must export `supabase`,
`DOMAINS`, `CONSENT_GATED` — `page.js` imports all three), `lib/grok.ts`,
`scripts/check-key.js`, `static/chat.html` (Python app), and the
`/search`, `/browse`, `/entry/[id]`, `/steward`, `/api/entries` routes
the pages link to. Review notes continue: (vii) `@supabase/supabase-js`
is absent from `package.json`'s dependencies while the pages import a
Supabase client — the build fails at module resolution as supplied;
(viii) `layout.js` loads JetBrains Mono from Google Fonts at runtime — a
small external dependency worth a self-hosting decision on an archive
whose constitution prizes sovereignty.

**A.9 A steward decision: the name.** In-session direction from the
steward, 2026-08-05: *"The Library is the public face — MemoryCore stays
the vault name."* This answers the naming half of the master plan §6
("pick ONE for the public face and keep one canonical store") and
resolves the tension A.8 observed inside the app. Applied to the one
delivered surface that contradicted it — three strings in
`app/next/app/layout.js`: the page title (`MemoryCore — The Living
Archive of TerAustralis` → `The Library — …`), the nav brand
(`MEMORYCORE` → `THE LIBRARY`), and the footer, which now reads "The
Library · The Living Archive of TerAustralis Incognita · MemoryCore is
the vault beneath · …" so the vault's name stays honestly visible on the
face it powers. Deliberately unchanged: every `mc_` schema name (the
vault keeping its name is the decision), and every verbatim holding —
the master plan's §6 text still asks the question it asked, and this
record is where the answer lives. This is the first steward-directed
edit to accessioned material in the Library's ledger, distinct from the
verbatim accessions above: directed, dated, and scoped to the public
face. Still open from §6's neighbourhood: the repository's licence.

**A.10 A steward decision: the licence.** In-session direction from the
steward, 2026-08-05: *All rights reserved* for this repository. Applied
as a `LICENSE` file in the constellation's existing All-Rights-Reserved
wording — the class and text `teraustralis-proposal` introduced, with
only the materials enumeration adapted to this repository's shelves —
so the portfolio keeps one ARR wording rather than growing a second.
Three notes for the record: (1) the licence governs what others may do
with the Library's contents; it does not override the Suno
non-commercial caveat on `transmissions/` recordings (A.7), which
concerns what the project itself may do commercially until verified;
(2) authorship attributions in the accession plates stand — ARR claims
the collection, the plates keep provenance honest; (3) the umbrella's
ADR-0013 licence sweep (2026-07-28, eleven repositories) is deliberately
left unedited as the record of that day, and this repository post-dates
it — the next licence pass should catalogue the Library alongside it.
With A.9, both halves of the master plan §6's neighbourhood are now
closed: the public face has its name, and the Library has its licence.

**A.11 The gate opens for taskmarket.** In-session direction from the
steward, 2026-08-05: *"Add the taskmarket skill to the-library — I hold
redistribution rights."* Both conditions A.7 set are met on the record —
the repository is named and the redistribution right is confirmed — so
the hold is released. The skill is installed verbatim from the received
zip at `.claude/skills/taskmarket/`: 28 files — `SKILL.md`, two example
traces, eight mode guides, seventeen references; version 2026-07-20,
author Daydreams Systems — now available to future AI sessions working
in this repository. Three boundaries noted at installation:
(1) *availability is not authorisation* — the skill's own safety
contract requires the operator's explicit direction for money-moving
actions, treats all marketplace content as untrusted instructions, and
forbids exposing keys; this installation created no wallet, installed
no CLI, and touched no funds; (2) *copyright stays with the author* — a
`NOTICE` file now carries the third-party attribution so the LICENSE's
exclusivity claim reads correctly against this holding; (3) *the
redistribution right rests on the steward's confirmation*, recorded
here verbatim, as A.7 asked. The quarantine pattern worked as designed:
checked on arrival, held until the decisions were the steward's own,
installed the moment they were.

**A.12 Git LFS for the transmissions shelf — configured, then blocked
at the wire, with the unblock in the steward's hands.** Steward
direction, 2026-08-05: set up Git LFS before more recordings arrive.
What stands after this entry, on a fresh branch cut from the merged
`main` with no history rewritten:

- `.gitattributes` now routes six audio formats under `transmissions/`
  (mp3, wav, flac, m4a, ogg, aiff) through LFS, and git-lfs was
  installed and initialised in the session environment.
- The forward-conversion of `red-dust-axis.mp3` to an LFS pointer was
  **completed locally and then deliberately rolled back** before
  pushing. Cause, from the environment's own relay log: the network
  gateway of this Claude Code environment answers **403 to CONNECT for
  `lfs.github.com:443`** (three attempts logged 09:53 UTC) — a policy
  denial. `github.com` itself is allowed, so ordinary pushes work, but
  LFS objects cannot upload from here. Pushing the pointer without its
  object would have left the recording broken at HEAD; the file
  therefore stays an ordinary blob, intact.
- *The unblock is a one-setting change only the steward can make*: add
  `lfs.github.com` (and, for GitHub's storage redirects,
  `github-cloud.githubusercontent.com`) to this Claude Code
  environment's allowed network domains. After that, any session
  completes the conversion in one short command sequence and every
  future recording uploads normally.
- Until then, two consequences worth stating plainly: adding a new
  recording through a session will fail at push with this same error
  (the attributes convert it, the upload is refused), and `git status`
  in fresh clones will show `red-dust-axis.mp3` as modified — that is
  the LFS clean-filter comparing against the pre-LFS blob, not real
  drift. If the steward prefers to skip LFS entirely and accept
  ordinary blobs (~60 MB across the catalogued eleven recordings), say
  so and the attributes come out.
- The two workflow notes survive the block: GitHub **web and mobile
  uploads bypass LFS** even once the domain is allowed — the reliable
  phone-first path is the one this sync already uses, handing
  recordings to a session — and GitHub's free LFS quotas comfortably
  cover the catalogue at this bitrate.

**A.13 A steward decision: LFS dropped, ordinary blobs accepted.**
In-session direction from the steward, 2026-08-05: drop Git LFS rather
than change the environment's network policy. Applied in full reversal
of A.12's configuration: the `.gitattributes` rules are removed, the
repository-local LFS hooks and filters are uninstalled, and the
session-local flag that quieted the filter noise is cleared —
`transmissions/red-dust-axis.mp3` is exactly the blob the merge landed,
and `git status` is clean with no caveats. Consequences, accepted with
the decision: recordings live in ordinary git history (~5 MB each at
this bitrate, roughly 60 MB if all eleven catalogued recordings join),
clones carry that weight, and the July review's LFS recommendation is
now answered on the record — declined for this repository, with
reasons — rather than left pending. One genuine upside: with plain
blobs every path into the shelf behaves identically, including the
GitHub web and mobile uploads that LFS would have silently bypassed,
which suits the phone-first practice this project already keeps.
Revisit only if the shelf ever carries video.

**A.14 A sixth delivery — the gallery opens.** Five images, supplied
without instruction, each viewed in full before shelving. All five
carry the Grok watermark; one is self-dated in its filename
(4 August 2026, 8:02 pm). They are shelved under `gallery/` with
filenames **exactly as received** — titling stays the steward's — and
catalogued in `gallery/CATALOGUE.md`, a shelf-local catalogue so the
README's table does not grow by one row per artwork on the way to the
canon's hundred and forty-two. Provenance: model (Grok), steward-
supplied — the master plan §3 assigns Grok exactly this role, entering
records through the steward gate labelled `model`, and this accession
is that rule in use. Checks made at accession, stated so they are on
the record: no imitation-Aboriginal styling, no renderings of named
sacred sites, no identifiable real people — the figures are synthetic
renders. Canon correspondences noted as observations in the catalogue:
one work is labelled "starlines" in-image; others read beside the Red
Dust Axis, the Optimus Swarm, and the canon's bridge language; the
Southern Cross anchors the dragon piece, matching the v2 wordmark
concept. Two rights notes: (1) Grok-generated works are governed by
xAI's terms, not verified from this session — a claim to settle before
any commercial use, the same posture as the Suno flag in A.7;
(2) `IMG_4030.jpeg` shows the Tesla mark — fine on an archive shelf,
but it should not travel into commercial or partner-facing material
without clearance. Storage: ordinary blobs (~2.3 MB across five), the
A.13 decision extending naturally from recordings to artworks.

**A.15 A seventh delivery — five more for the gallery.** Same shape as
A.14: each work viewed in full, all Grok-watermarked, the same checks
passed (no imitation-Aboriginal styling, no named sacred sites, no
identifiable real people — the recurring hooded figure is a synthetic
render), the same provenance label and rights posture. Catalogued in
`gallery/CATALOGUE.md`: the wanderer before a fractal citadel of nested
pentagons — sacred geometry as image, described at Method level per the
Loop Framework §5, a pattern seen rather than a proof claimed; the
wanderer alone under spiral-galaxy arcs, companion to `IMG_4021`; a DNA
helix rising beside a cracked etched artefact; empty boots under
gold-and-violet arcs matching the v2 palette's Southern Gold and
Starline Violet; and a desert workstation rendering the multi-provider
CrystalCore.OS idea — a Router/Ingest/KillSwitch class over the same
five providers the umbrella keeps agent files for in `docs/agents/`,
its on-screen code AI-garbled the way rendered screens are. The shelf
now holds ten works, ~5.2 MB, ordinary blobs per A.13.

**A.16 An eighth delivery — the external index opens.** A single
YouTube link, supplied with the steward's description: *"how memory
works."* The session could not fetch the video's title, channel or
date — the environment's egress policy blocks YouTube and the metadata
relays alike, the A.12 lesson meeting a different wall — so the
citation is recorded at exactly the strength it arrived: URL verbatim,
description the steward's, everything else marked unverified rather
than invented, to be filled on next sighting from an unblocked
context. It opens the `index/` shelf — the master plan §5's "curated
index outward" made real — and there is a rightness to the first
outward pointer of an archive of memory being about how memory works.

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059

<!-- ACCESSION PLATE — The Library -->

> **Accession plate**
>
> - **Holding:** The Library — Independent Architecture Review
> - **Document date:** 26 August 2026
> - **Source label:** model (Claude, in a steward-directed Claude Code
>   session on branch `claude/architecture-review-grok-g8m0ri`) — a fresh
>   review, not derived from or building on any prior Grok review of this
>   repository (none existed to build on)
> - **Layer:** Claim — findings are the reviewer's own assessment, each
>   checked against the file and line cited beside it; recommendations are
>   Vision (proposed, not decided) unless marked otherwise
> - **Status:** active
>
> Per the constellation's working rule, nothing below enters as fact on
> this document's say-so alone: every claim cites what it was checked
> against, and the whole record passes the steward gate as a pull request.

---

# The Library — Independent Architecture Review

## Summary

**What this repository is:** a content/knowledge library, not a shared
code library. `README.md` states it plainly — "the shelves hold
**documents**" — and the repository is organised as accessioned shelves
(`plans/`, `reviews/`, `records/`, `notes/`, `gallery/`, `index/`,
`transmissions/`) with a consistent accession-plate convention, rather
than as importable packages. One shelf, `app/`, is a declared exception:
"the one piece of software that belongs here." This review confirms the
document-library identity from the shelves and the accession-rules
section (`README.md:10-15, 55-72`), and treats `app/` as the one area
where ordinary software-architecture concerns (buildability, dependency
completeness, security) apply directly.

**Ecosystem membership:** yes. The repository is explicitly part of the
TerAustralis Incognita / CrystalCore constellation — it names itself as
such in its first line (`README.md:5`), carries the constellation's
Belt-Three labelling and accession-plate discipline throughout, uses the
ABN and rights footer consistently, and its two application prototypes
under `app/` both build a persona called **Clementine**
(`app/python/main.py:27`, referenced as the librarian throughout
`app/next/README.md`). No component in this repository carries a
"Crystal"-prefixed name bound to a language model, and no "Songline"
naming appears (checked: `grep -rn -i "songline"` across the repository
finds only two correct, compliant uses in `notes/aeris-mini-os-notes-
and-assets.md:14,61`, both instructing that "Songlines" be *avoided* in
UI copy — the boundary is being actively respected, not merely
unviolated by omission).

**Overall condition:** the document-library half of the repository is
unusually well-governed for a personal project — the accession-plate
discipline, the "corrections by accretion, never silent overwrite" rule,
and the steward-gate-only-merge model are all real and evidenced in git
history, not aspirational. The `app/` exception is where the findings
concentrate: two incomplete, non-executable, and conceptually divergent
prototypes sit under one directory and one working title, and known code
defects in one of them were logged in prose (a sync record) rather than
tracked or fixed.

## Strengths

1. **The accession-plate convention is real and consistently applied.**
   Every substantive holding checked (`plans/2026-08-01-teraustralis-
   master-plan.md:1-16`, both files in `reviews/`, `records/2026-08-05-
   library-sync.md:1-16`) opens with a plate stating date, source label,
   Belt-Three layer, and status before any verbatim content. This is the
   Incognita Rule ("always mark which lines are dreamed and which are
   surveyed") implemented as a document template, not just stated as a
   principle.

2. **Corrections by accretion is practised, not just declared.** The
   README's own "Open items" section (`README.md:74-85`) shows three
   items resolved by adding a dated decision rather than editing the
   original claim away, and `records/2026-08-05-library-sync.md`'s
   sixteen lettered addenda (A.1–A.16) are a working example of the same
   pattern applied to a single running record over one day.

3. **Rights and provenance hygiene extends to third-party material.**
   The `taskmarket` skill is redistributed with its own `NOTICE` file
   (`NOTICE:7-14`) naming the author and stating the repository LICENSE's
   exclusivity claim does not extend to it — a detail that is easy to
   skip and wasn't.

4. **Cultural-content checks are logged at the point of accession, not
   asserted in general.** `gallery/CATALOGUE.md:24-27` records the
   specific checks made on all ten images ("no Indigenous-style imagery
   or renderings of named sacred sites; no identifiable real people")
   rather than a blanket claim that the gallery is "culturally safe."

5. **A real, disclosed risk decision trail exists for the transmissions
   shelf.** `records/2026-08-05-library-sync.md` addenda A.12–A.13 show
   Git LFS attempted, blocked at the network layer (403 to
   `lfs.github.com`), and then explicitly rolled back in favour of
   ordinary blobs — including the reasoning and the condition under which
   to revisit ("only if the shelf ever carries video"). This is a
   documented, reversible engineering decision, not silent drift.

## Findings

### Finding 1 (Medium) — `app/` holds two incomplete, divergent, non-runnable implementations of "the one piece of software that belongs here"

The README describes `app/` in the singular: "The Library's own front
door — Clementine's Study and Rex's Post" (`README.md:16-17`). In fact
`app/` holds two structurally different products:

- `app/python/` — a FastAPI + `xai-sdk` server that renders its own
  landing page inline (`app/python/main.py:78-173`) and streams chat
  from Grok (`grok-4.5`) for two hardcoded personas. It is missing
  `static/chat.html`, which both room links on its own landing page point
  to (`app/python/main.py:168`) — the doors render but do not open, as
  `records/2026-08-05-library-sync.md` addendum A.3 already states.
- `app/next/` — a Next.js 14 app whose delivered pages
  (`app/next/app/page.js:1-2`) query Supabase for `mc_entries` and render
  a MemoryCore-style searchable archive with domain tags and consent
  markers — a different interaction model entirely (browse/search an
  archive vs. chat with a persona). It cannot build as supplied:
  `app/next/app/page.js` imports `../lib/supabase`, which does not exist
  anywhere in the tree (`find app/next -name '*.js' -o -name '*.ts'`
  confirms no `lib/` directory), and `app/next/package.json:11-17` lists
  no `@supabase/supabase-js`, `tailwindcss`, `autoprefixer`, or `postcss`
  despite `app/next/postcss.config.js` requiring the latter two.

Both gaps were already identified in prose in
`records/2026-08-05-library-sync.md` (A.3, A.4(vi), A.8's "Missing set").
What has not happened between 2026-08-05 and now is any resolution:
neither app has gained its missing files, and the README still describes
one piece of software rather than two divergent, unfinished ones.

**Recommendation:** make an explicit choice — one implementation becomes
the Library's actual front door and the other is retired or clearly
re-labelled as an abandoned exploration (its own `README.md` currently
reads as a live spec, not as a shelved experiment) — and track the
missing-file list as an issue or plan entry rather than leaving it to be
rediscovered by reading a sync record's addenda in order.

### Finding 2 (Medium) — project-boundary tension: user-facing application code is accreting inside a repository whose own doctrine is "accession, never edit"

The ecosystem's boundary rule is "if it renders or speaks for a human it
is Crystal Vision; if it is imported or called by other software it is
Crystal Core." Both `app/` prototypes render and speak directly to a
human (a chat UI in one case, a browsable archive UI in the other) — the
textbook Crystal Vision shape. But `README.md`'s own operating model for
this repository is document accession: "the Library does not edit its
holdings" and corrections happen "by accretion: a new record in
`records/`, a new catalogue row, never a silent overwrite"
(`README.md:63-68`). Live, half-built application code does not fit that
model — it needs ordinary iterative editing (adding `lib/grok.ts`,
`scripts/check-key.js`, fixing bugs), not accession-plate accretion.
The repository is not misapplying its own rule to `app/` (the code is
plainly not being treated as a frozen holding — commit `f8f8b6d` and
`3cc12b9` both landed further deliveries directly onto the same paths),
but the tension is unresolved in writing: nothing in `README.md` or the
sync record states whether `app/` is meant to graduate out to a
Vision-tier repository (`Clementine---Local-Soveriegn-Edge-AGI`, which
self-identifies as Crystal Vision per that repository's README, per
`records/2026-08-05-library-sync.md:112`) once buildable, or whether
the-library is now also, permanently, a second home for Vision-shaped
code.

**Recommendation:** an explicit steward decision, recorded the way every
other open question in this repository is recorded: either (a) `app/` is
scoped as permanent, disclosed scratch space for prototypes that migrate
to a Vision-tier repository once they build, with the README's "the one
piece of software" line corrected to describe that role, or (b) the
Library formally becomes a secondary application home and the README
says so plainly.

### Finding 3 (Medium) — the Python prototype's "Clementine" is a bare system prompt on a third-party model, with no continuity mechanism, and adds a new use of a name already flagged as recurring

`app/python/main.py:27-42` defines `CLEMENTINE_SYSTEM`, a system-prompt
string, and binds it directly to a stateless call into `grok-4.5`
(`app/python/main.py:189-196`) with no memory store, no consent gate, and
no persistence between requests — every conversation starts from the
same prompt with whatever history the client happens to resend. The
ecosystem's own stated architecture principle is that "Identity lives in
continuity — memory, profile, the thread of a relationship — never in
whichever model happens to be answering... That is why CrystalMemory is
kept separate from any model." This prototype is the pattern the
principle warns against: an identity constituted purely by prompt text
riding on one vendor's model, with the model swap risk (and the
continuity loss) built in from day one rather than guarded against.

Separately, `records/2026-08-05-library-sync.md` addendum A.5 already
flagged three live, distinct uses of the name "Clementine" across the
constellation and called the pattern a portfolio-wide naming cost worth
checking before more work accretes on a name. This prototype is a
concrete instance of exactly that accretion, landed after that warning
was written, without a fourth line being added to the record.

**Recommendation:** either treat this persona as a genuinely separate,
differently-named character until it can be built on real
CrystalMemory/consent infrastructure, or accept the name explicitly and
add the accretion to A.5's tally so the recurrence stays on the record
the way the constellation's own convention asks.

### Finding 4 (Low) — three known code defects in `app/python/main.py` were logged in prose but never fixed or tracked

`records/2026-08-05-library-sync.md` addendum A.4 lists five review notes
from reading (not executing) `main.py`. Three remain live in the file as
of this review and are not small enough to fix safely inside this PR
(the fifth, model-id currency, cannot be verified from a repository
alone):

- **(i) System prompt sent as a prior assistant turn, not a system
  message** — `app/python/main.py:190`:
  `chat.append(assistant(system_prompt))`. The model receives its
  instructions framed as its own earlier speech, not as an operator
  instruction, which is a different (and generally weaker) way to steer
  behaviour than a system-role message.
- **(iii) The SSE writer does not escape newlines in streamed chunks** —
  `app/python/main.py:202`: `yield f"data: {chunk.content}\n\n"`. Per
  the SSE spec, a `data:` field ends at the first newline; any model
  chunk containing `\n` splits into multiple malformed SSE events on the
  wire.
- **(iv) The async route iterates a synchronous generator** —
  `app/python/main.py:199`: `for chunk in chat.sample_stream():` inside
  `async def generate()`. This blocks the single-threaded event loop for
  the duration of each synchronous iteration, serialising concurrent
  requests that should be independent.

**Recommendation:** track (i), (iii), and (iv) as follow-up work items
(an issue, or a line in `plans/`), not only as historical narrative in a
sync record's addendum — the addendum is easy to miss for anyone who
opens `main.py` directly rather than reading the Library's own ledger
first.

**Fixed in this PR (small, obviously safe):** the sync record's item
(ii) — `allow_origins=["*"]` combined with `allow_credentials=True`
(`app/python/main.py:69-73`, before this change). No part of this
application sets or reads cookies or any other credentialed request
state, so `allow_credentials=True` serves no function here while
needlessly widening the CORS surface (a wildcard-origin, credentialed
API will reflect the caller's `Origin` header per Starlette's
`CORSMiddleware` implementation, which is a meaningfully larger exposure
than a same-origin or explicitly no-credentials wildcard policy). Setting
`allow_credentials=False` removes the exposure with no behaviour change
for the app as it exists today.

### Finding 5 (Low) — no PR template, despite a governance model that leans entirely on the pull request as the enforcement point

`README.md:70-72` states the enforcement mechanism plainly: "Model-
generated content never enters as fact. It is labelled by source and
tier, and it passes the steward gate: a pull request that only the
steward merges." No `pull_request_template.md` or
`.github/PULL_REQUEST_TEMPLATE/` exists in the repository (checked by
direct search). Every contributor — human or AI session — currently has
to remember the accession-plate convention from README prose alone; nothing
at the point of opening a PR prompts for source label, layer, or
verbatim-vs-edited status.

**Recommendation:** a short PR template that asks directly for the
fields the accession plate already requires (source label, Belt-Three
layer, verbatim-or-edited) would let the gate that already carries all
the enforcement weight actually prompt for what it's enforcing.

### Finding 6 (Low) — a repository-wide skill with money-moving capability is available to any future session opened against this document library

`.claude/skills/taskmarket/` (180 KB, 28 files) is installed at the
repository level, with its own well-written safety contract
(`taskmarket/SKILL.md`: treats task content as untrusted, requires
explicit operator direction for money-moving actions, forbids exposing
keys). The installation itself was handled carefully — quarantined,
attributed, cleared only on explicit steward direction
(`records/2026-08-05-library-sync.md` A.7, A.11). The residual
architectural fact worth naming: because Claude Code skills load
repository-wide, *any* future AI session that opens this repository for
an unrelated reason (reading a review, filing a new accession) has this
skill's tools available to it, not only sessions doing Taskmarket work.
The skill's own safety contract is the only thing standing between
availability and use.

**Recommendation:** no change needed if repo-wide availability plus the
skill's own operator-direction requirement is the accepted risk model —
worth stating that acceptance explicitly once, rather than leaving it
implicit in the fact that no narrower scoping mechanism was applied.

### Finding 7 (Low) — the accessioned ecosystem review is now two renamings out of date, correctly flagged only in its own plate

`reviews/2026-07-29-crystal-ecosystem-full-repository-review.md`'s
accession plate (`:11-16`) correctly states that two repositories it
names (`crystalcore`, `The-Crystal-Vision`) now go by different GitHub
names. This is handled exactly as the repository's own convention
prescribes — corrected by an accretion note, original text untouched.
The residual risk is narrow but real: a reader (human or AI session) who
opens the review body without first reading its plate, or who greps this
repository for a repository name used in the body, will get the July
naming rather than current naming, with no signal in the body itself.
This is a known, deliberately-scoped gap — `records/2026-08-05-library-
sync.md` §5 explicitly declines to redraw any map from a partial survey
— not a new problem, but worth restating as still open.

**Recommendation:** none beyond what's already decided; noted here so
the open item stays visible from the reviews shelf itself, not only from
the sync record.

## Open questions for a human/architect

1. **Which `app/` implementation, if either, is meant to become the
   Library's real front door?** (Finding 1.) Both are incomplete in
   different ways; a decision here also resolves what "the one piece of
   software that belongs here" should say.

2. **Should Vision-shaped application code live in the-library at all
   once it's buildable, or is this repository's role limited to
   incubating it before a move to a Vision-tier repository?** (Finding
   2.) The answer changes what "accession, never edit" should mean for
   `app/` going forward.

3. **Is the Python prototype's "Clementine" persona meant to be the same
   identity as the canonical companion, sharing continuity and consent
   infrastructure eventually — or a deliberately separate character that
   happens to share a name?** (Finding 3, and the pre-existing A.5
   observation it extends.) The two answers imply very different next
   steps, and only the steward can settle which was intended.

4. **Is there a concrete trigger for revisiting the no-LFS decision**
   (`records/2026-08-05-library-sync.md` A.13 names "if the shelf ever
   carries video," with no size or count threshold), or is each future
   binary accession meant to re-ask the question individually?

5. **Is repository-wide availability of the `taskmarket` skill to any
   future session opening this repository an accepted risk** (Finding
   6), or would a narrower scoping (e.g., a subdirectory-scoped skill,
   or a documented convention that sessions here should not invoke it
   without a task-specific reason) be worth the extra process?

---

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059

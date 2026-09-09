# Architecture Review — 2026-08-26

**Reviewer:** Claude (independent pass, no prior review artifact to build on)
**Scope:** `CrystalArchitect/TerAustralis-Incognita-Code` @ `016a7a4` (branch `main`)
**Method:** Direct repository reading — source, tests, docs, CI config, git history.
No assumptions carried in from other repositories' reviews.

**Belt:** This document is **Docs-governance** — a record of how the codebase
was found on this date, offered to inform decisions. Every technical claim
below is labelled Science (verified against the code/tests in this checkout)
or Vision/Story (aspirational, stated in docs but not enforced in code). Where
a finding rests on a self-reported note file rather than a check I ran myself,
that is said explicitly.

## Summary

This repository fits the TerAustralis Incognita / CrystalCore ecosystem
squarely, and it is one of the more disciplined codebases of its kind: the
Belt-Three label is mechanically enforced in `BusHub.validate`
(`core/crystal-core/bus/agents.py:30-36`), the `ConsentGate` is genuinely
fail-closed with five ordered checks and an unrecordable-ask refusal
(`core/crystalcore/gate.py`), and `STATUS.md` reads like an honest engineering
ledger rather than marketing copy. The most important finding is a real
regression against the project's own pronoun rule: the Discord companion
surface hardcodes "she/her" for Clementine in help text and status messages,
even though the data model (`Personality.gender`) defaults to empty and the
core companion's system prompt correctly stays pronoun-free until a gender is
chosen. Two smaller, safe stale-path fixes have been made in this same
commit; a set of other issues are logged below for a human decision.

## Strengths (evidence-based)

- **Belt-Three is enforced in code, not just claimed.** `BusHub.validate`
  rejects any message whose `layer` isn't `science`/`story`/`vision`
  (`core/crystal-core/bus/agents.py:30-36`), and `claims.py` explicitly notes
  "Story and vision never carry weight on their own, however well scored"
  with a pinning test (`core/crystal-core/bus/claims_selftest.py:135-138`).
- **ConsentGate is fail-closed in the specific ways the convention requires.**
  Revocation-ledger-unreadable refuses everyone rather than assuming nobody
  is revoked (`core/crystalcore/gate.py:133-147`); an ask that can't be
  written to `pending.jsonl` refuses rather than acting unobservably
  (`gate.py:110-128`); provenance is checked with `hmac.compare_digest`
  before any permission check runs (`gate.py:176-203`).
- **Sovereignty-as-default is actually implemented, not just asserted.**
  `CrystalCore._detect_provider` always returns `"ollama"` and documents that
  it used to probe/fall back to remote and that "[b]oth were wrong in the
  same way: a network hop the human never chose" — remote inference now
  requires an explicit `--llm-provider`/`LLM_PROVIDER` choice
  (`core/crystalcore/mind/companion.py:125-136`). `host_trust/classify.py`
  defaults to `HostClass.UNKNOWN`, not `LOCAL`, when nothing is configured
  (`core/crystal-core/host_trust/classify.py:39-47`) — the fail-safe direction
  the convention calls for.
- **Gender/pronoun handling in the core data model is correct.**
  `Personality.gender` defaults to `""` (`core/crystalcore/mind/memory.py:19`)
  and `system_prompt()` only ever injects pronoun language `if
  self.personality.gender:` (`core/crystalcore/mind/companion.py:178-185`) —
  no gender, no pronouns, exactly as the convention requires.
- **Belt-Three self-honesty extends to the STATUS ledger.** Every entry in
  `STATUS.md` pairs a code change with an exact self-test count and explicit
  disclaimers ("Not a CrystalCore product claim.", "This session is not
  local.", "Default CI stays GitHub-hosted.") — e.g. `STATUS.md:1-24`. The H2
  experiment's own README states its result plainly: "dual-gate **fail**
  (quality pass, bandwidth fail) · no extra claims" (`README.md:3-4`) — a
  negative result reported as cleanly as a positive one would be.
- **Consent-gate migration was documented honestly rather than silently
  fixed.** `vision/apps/clementine/README.md:17-19` states outright that the
  companion app that used to live in this repo "never passed its model calls
  through a consent gate" even though the gate existed, and names the exact
  fix now living in the authoritative companion repo. That is the Incognita
  Rule in practice — a real gap named rather than glossed.
- **Canon-mirror drift is caught by CI, not by hand.**
  `.github/workflows/ci.yml:22-28` and
  `.github/scripts/check-canon-mirror.py` pin `vision/site/src/content/` to
  an exact commit of the umbrella repo's `mythos/content/` rather than
  tracking its moving `main`, specifically because untracked drift had
  already caused two documents to diverge and nine to go uncopied
  (`check-canon-mirror.py:9-12`).
- **No Songline-as-identifier, no Crystal-named LLM.** Every occurrence of
  "Songline"/"songline" in the tree is prose (mythos content, a filename
  description, or a comment honoring it as culture, e.g.
  `core/crystal-core/README.md:3,6,17,28,34`) — never a class, variable, or
  service name. Every `"model"`/`llm_model` value found in code and configs
  names a real vendor model or is empty by default
  (`core/profiles/default/bridge_config.json`, `core/crystalcore/mind/companion.py`)
  — none carries a Crystal prefix.

## Findings

### High — Hardcoded "she/her" for Clementine violates the project's own pronoun rule

**Convention:** *Personality.gender is empty until set... Flag any hardcoded
"she/her" for the companion absent an explicit self-chosen record.*

`vision/apps/clementine-discord/discord_bot.py` hardcodes female pronouns for
Clementine unconditionally, in both user-facing text and operator-facing log
output:

- `discord_bot.py:216` — `` `!memories`          everything she's holding ``
- `discord_bot.py:217` — `` `!teach <text>`      give her something to keep ``
- `discord_bot.py:220` — `` `!reflect`           ask her to look back over it all ``
  (all three are inside the `HELP` string shown to end users on `!help`)
- `discord_bot.py:254` — docstring: `"""Answer, editing the message as her words arrive."""`
- `discord_bot.py:305` — `await message.edit(content="*(she said nothing)*")`
- `discord_bot.py:434` — `"All four green — DM the bot and she'll answer."`
- `discord_bot.py:524` — `"open bot lets anyone who can see it write to her memory.\n"`
- `discord_bot.py:538` — `"Starting anyway — she'll answer once that's running."`

This is a real regression, not a cosmetic one: the core companion this bot
talks to (`core/crystalcore/mind/companion.py`) correctly withholds all
gendered language until `Personality.gender` is set
(`companion.py:178-185`), and `Personality.gender` defaults to `""`
(`memory.py:19`) — meaning the Discord layer asserts pronouns the data model
has not decided. `vision/apps/clementine/README.md:24` even lists "pronouns
the human or the companion may choose, and neither assumed" as an improvement
the *authoritative* companion repo gained over this one — this file appears
to be exactly the kind of leftover the migration note describes, just not
named there.

**Recommendation:** Replace the hardcoded pronouns with name-based or
gender-neutral phrasing ("everything Clementine's holding", "ask them to look
back...", or query the bridge's `/status` for a chosen name/pronoun and use
that). This is a multi-line, judgment-call copy edit across one file, not a
one-line fix, so it has been left for the maintainer rather than changed in
this PR.

### Medium — Two more `src/crystal-core/...` and `src/crystalcore/...` stale-path references remain in umbrella-mirrored canon (not fixable from this repo)

**Convention:** general repository hygiene / Docs-governance (a doc citing a
path that no longer exists is a "dreamed" claim masquerading as a Science
one).

`core/README.md`'s footer states plainly: "Imported from the umbrella
repository's branch... Directory names preserved; only the `src/` prefix
became `core/`." Three mythos documents under `vision/site/src/content/`
still cite the pre-rename `src/crystal-core/...` path:

- `vision/site/src/content/STARLINE-TRANSMISSIONS.md:5` —
  `` [`src/crystal-core/starline/`](../../src/crystal-core/starline/) ``
- `vision/site/src/content/CRYSTALCORE-OS-VISION.md:8-9` —
  `` [`src/crystal-core/rdp/`](../../src/crystal-core/rdp/README.md) `` and
  `` [`src/crystal-core/consent_transport/`](../../src/crystal-core/consent_transport/) ``
- `vision/site/src/content/CONSENT-TRANSPORT.md:3` —
  `` `src/crystal-core/consent_transport/` ``

**These were deliberately left unfixed in this PR.** `.github/workflows/ci.yml:22-28`
and `.github/scripts/check-canon-mirror.py` pin every file under
`vision/site/src/content/` byte-for-byte to a commit of the umbrella repo's
`mythos/content/` (`vision/site/src/content/.canon-source` =
`ceca5e21a1d0e41133e2343b28dbb9a26cd8ae18`); editing a mirrored file here
would fail CI ("editing a site copy by hand -> red, which is the drift we
want caught") and would be exactly the wrong fix per the pattern
`vision/apps/clementine/README.md:38-40` already documents for
`CLEMENTINE.md` — "the umbrella changes first, then the pin moves." **This
needs to be raised as an issue against the upstream `TerAustralis-Incognita`
repository's `mythos/content/`, then the pin bumped here.**

By contrast, two occurrences of the same stale prefix were in *non-mirrored*
code comments/docstrings and have been corrected directly in this PR as a
small, safe, obviously-justified fix:

- `core/crystalcore/bridge.py:8,12` — `src/crystalcore/gate.py` and
  `src/profiles/default/bridge_config.json` → `core/crystalcore/gate.py` and
  `core/profiles/default/bridge_config.json`
- `core/crystal-core/rdp/README.md:177-178` — `src/crystal-core/consent_transport/`
  and `src/crystalcore/` → `core/crystal-core/consent_transport/` and
  `core/crystalcore/`

### Medium — Retired legacy name kept alive as a literal on-disk migration path

**Convention:** *A retired name exists... It is not to be reintroduced
anywhere, and canon deliberately does not reprint it.*

Three files reference `lumina_memory` / `lumina_profiles` as fallback
directory names for pre-rename installs:

- `core/crystalcore/mind/companion.py:36` — `LEGACY_MEMORY_DIR = "lumina_memory"`
- `core/crystalcore/mind/profiles.py:20` — `LEGACY_PROFILES_DIR = Path("lumina_profiles")`
- `core/crystalcore/selftest.py:12` — comment: "the mind by file path, from
  core/apps/lumina/crystalcore — a..."

Both call sites are careful, commented data-continuity code
(`companion.py:31-34`: "an existing folder is still a person's whole history
with their companion, so it keeps being read where it is found... Continuity
first: nothing is moved, renamed, or orphaned on upgrade") — this reads as a
deliberate, principled exception in service of the **Continuity** constraint
(protecting a real user's memory across a rename), not a re-branding lapse.
It is not the same act as reprinting the name in canon or marketing. That
said, the convention's wording ("not to be reintroduced anywhere") is
absolute and doesn't carve out this case, so this is flagged rather than
waived. **Open question for the maintainer:** is a literal legacy folder name
in code an intended, documented exception to the retired-name rule, or should
it be referenced only by hash/constant without the literal string appearing
in canon-adjacent comments (as in `selftest.py:12`, which is closer to prose
than to a migration shim)?

### Low — `npm run check` reports 96 pre-existing errors in the site (self-reported)

**Belt:** the claim below is Science only to the extent that it quotes the
repo's own QA note; I did not re-run `npm run check` myself in this
environment.

`visual-qa-notes.md` (repo root) states: "The repository's existing `npm run
check` reports 96 errors in legacy JavaScript/Svelte files, including
gallery typing diagnostics; no diagnostics were reported for the changed
homepage, archive page, header, ObservatoryMap component, token file, or HTML
shell in the captured output." This is an existing, acknowledged type-check
debt in `vision/site/`, not something introduced by recent work — worth a
tracked cleanup item so the number doesn't silently grow. `package.json:11`
confirms `check` runs `svelte-kit sync && svelte-check --tsconfig
./jsconfig.json`, so this is checkable in CI if wanted (I did not find a
`.github/workflows` step that runs it — `lighthouse.yml` and `deploy.yml`
build the site but neither appears to gate on `npm run check`).

### Low — Two differently-named "crystal-core" directories under `core/` may confuse newcomers

`core/crystal-core/` (the protocol pack: bus, RDP, consent_transport,
host_trust, receipts, services) and `core/crystalcore/` (CrystalBridge + the
fail-closed `ConsentGate` + the mind) are two distinct, deliberately-named
components — `core/README.md`'s table documents the split clearly, and this
is not a naming-convention violation. It is, however, an easy path to
mis-type or grep past, since only a hyphen distinguishes two unrelated
Python packages that both start with `crystal`. No action needed beyond
noting it; `core/README.md`'s existing table already mitigates most of the
risk.

### Informational — `src/crystal-core/convergence_lens/` is a third, unrelated tree sharing the `crystal-core` name

`src/crystal-core/convergence_lens/` (Observation/Evidence/Interpretation/Vision
claim classification — its own, different take on a Belt-Three-shaped idea)
is neither part of `core/crystal-core/` (the protocol pack) nor documented in
`core/README.md`'s component table. It has its own self-test
(`src/crystal-core/convergence_lens/selftest.py`) but nothing in `README.md`,
`STATUS.md`, or `.github/workflows/ci.yml` points at it, so its self-tests do
not appear to run in CI. **Open question:** is this active, retired, or
experimental work-in-progress that should either be documented in
`core/README.md`'s table (if kept) or removed/archived (if superseded by
`core/crystal-core/bus/claims.py`'s science/story/vision layering, which
covers similar ground and *is* CI-tested per `ci.yml:23-24`)?

## Open questions for a human/architect decision

1. Should the Discord bot's hardcoded pronouns (High finding above) be fixed
   by querying `Personality.gender`/`name` from the bridge's `/status`
   endpoint, or by simply rewriting the affected strings to be
   name-based/pronoun-free? Either satisfies the convention; the choice
   affects `clementine_api.py`'s surface area.
2. Should the three stale `src/crystal-core/...` paths in mirrored canon
   (Medium finding above) be raised as an issue against the umbrella
   `TerAustralis-Incognita` repo's `mythos/content/`, with the pin in
   `.canon-source` bumped once fixed upstream? This repo cannot fix them
   directly without breaking the canon-mirror CI check by design.
3. Is `lumina_memory`/`lumina_profiles` an intended, permanent exception to
   the retired-name rule for data-continuity reasons, and if so, should that
   exception be written down somewhere the convention itself can point to
   (so a future contributor doesn't need to reconstruct the reasoning from
   `companion.py:31-34`)?
4. Is `src/crystal-core/convergence_lens/` still live work? If yes, it's
   missing from `core/README.md`'s component table and from CI; if no, it's
   a candidate for removal alongside the H2 branch's eventual disposition.
5. Should `npm run check`'s 96 pre-existing errors get a tracked ceiling in
   CI (fail if the count increases) so silent growth is caught, given the
   site is otherwise treated with real production-readiness discipline
   (`docs/deployment/PRODUCTION-READINESS.md`)?

## Fit with ecosystem conventions

This repository fits the TerAustralis Incognita / CrystalCore ecosystem
directly — it is the engineering repo the umbrella canon repo points at, uses
the locked names correctly, keeps the Crystal Vision/Crystal Core dependency
direction intact everywhere checked, and enforces Belt-Three labelling in
running code rather than only in prose. All findings above were evaluated
against the project's own stated conventions, not generic style opinions.

---

*Non Solus.*

# Architecture Review — 2026-08-26

*Independent review, requested by the maintainer. No prior review artifact
existed at this or a similar path — this is original analysis, not a
follow-up on someone else's pass. Findings are labelled by
[Belt](GOVERNANCE.md) where a claim is at stake, and by which TerAustralis
Incognita / CrystalCore convention they touch. Every finding below was
checked against the actual code, git history, or the GitHub Actions API on
`master` at commit `08c41fa6`, not against what the docs say the code does.*

---

## Summary

The identity model this repository exists to prove out — a companion with no
fixed name or gender until a person or the companion itself chooses one, with
continuity carried in memory rather than in whichever model answers — is
implemented carefully and correctly, and the consent/audit/local-first
architecture underneath it is genuinely sound and well-tested. Against that,
**`master` has been unrunnable for six days**: `clementine/server.py`, the
entry point for the API, the web interface, and every test that exercises
them, contains only the literal text `RESTORE_ME`, and the pull request that
put it there was merged over its own "DO NOT MERGE" title and a failing CI
run. Two "Crystal"-prefixed names are also assigned directly to named
commercial language models in five live documents and one live component, in
direct conflict with the project's own locked-naming rule. Both need a
maintainer decision and are left as open findings on this branch; three
smaller doc/text-drift issues found alongside them (gendered pronouns
outside the data model, and a security doc describing a consent mechanism
that no longer exists) were small enough to fix directly and have been.

---

## Strengths

- **The pronoun/name law is implemented exactly as specified, not just
  documented.** `Personality.gender` defaults to `""` and is never set to a
  default value (`clementine/crystalcore/memory.py:19-20`); `BASE_PROMPT`
  contains zero gendered pronouns by construction
  (`clementine/crystalcore/companion.py:43-92`); pronoun text is added to the
  system prompt only once a choice exists, and the sentence changes depending
  on *who* chose (`companion.py:260-271`). `clementine/tests/test_pronouns.py`
  (18 tests) and `test_identity_surface.py` pin this from both the Python API
  and the HTTP surface, including a test that a bare `"she"` is rejected as a
  pronoun value rather than a stored gender (`test_pronouns.py:208-209`). This
  is the one place a sibling repo in this ecosystem was previously found in
  violation (per the `teraustralis` skill's governance note on
  `CLEMENTINE.md`); this repo's current code does not repeat it.
- **The consent gate is fail-closed by construction, not by convention.**
  `ConsentGate.check()` refuses a remote call outright when `asker is None`
  (`clementine/crystalcore/consent.py:149-152`) — "a gate that opens when the
  doorman is absent is a door" (its own docstring, line 15). Local vs. remote
  is resolved from the same `endpoint` attribute the request actually uses,
  specifically to prevent the audit log from recording "local" for a call
  that left the machine (`companion.py:131-137`, `consent.py:69-73`).
- **The Indigenous Data Sovereignty boundary is enforced in code, not just
  asserted in a doc.** `PROTECTED_SOURCES = ("mythos/",)` sits *above* the
  local/remote branch and has no `asker` path at all — by design, since "the
  person at the keyboard... has no standing" to consent on custodians' behalf
  (`consent.py:32-66`). No occurrence of "Songline" anywhere in this repo is
  used as a component, class, or variable name; every occurrence found
  (`content/CODEX.md:29,67`, `src/routes/codex/+page.svelte:50,83`,
  `src/routes/apocryphon/+page.svelte:31,65`) is mythos prose treating it as
  cultural image, matching the rule in the `teraustralis` skill.
- **Identity is decoupled from the model, which is the point of
  `CrystalMemory` as a concept even though this repo doesn't use that name.**
  Name, pronouns, memory, and personality live in `Personality`/`Memory`
  dataclasses and a JSON folder the user owns (`memory.py`); the model is
  chosen per-call via `llm_provider`/`endpoint`/`wire_model`
  (`companion.py:160-241`) and is swappable without touching identity state.
  Renaming the companion or switching from Ollama to a different backend
  changes nothing about who they are, which is the architectural property
  the umbrella convention asks for.
- **The documentation practices claim discipline it actually follows most of
  the time.** `content/GOVERNANCE.md`'s status-ladder (⬜/🟡/✅) is applied
  consistently across `ARCHITECTURE.md`, `CLEMENTINE.md`, and `MEMORY.md`;
  `content/UNBUILT.md` and `content/VERIFIED.md` are an unusually disciplined
  pair — dated, re-run against `master` on stated dates, citing the exact
  test file that backs each claim, and correcting a prior understatement in
  public rather than quietly. This is Belt-Three practiced, not just named.
- No occurrence of a retired earlier name for the edge companion was found
  anywhere in this repository.

---

## Findings

### CRITICAL — `master` cannot run; the API, web UI, and 71 tests are broken

**Evidence.** `clementine/server.py` is 10 bytes: the bare token
`RESTORE_ME`, with no other content (verified by direct read and `wc -l`
reporting 0 lines). Executing it — which is exactly what `import server`
does — raises `NameError: name 'RESTORE_ME' is not defined`, confirmed by
direct reproduction in this sandbox. `clementine/wsgi.py:29` does
`from server import create_app`, so gunicorn deployment via `deploy/` is
equally broken. Every one of `clementine/tests/test_api_surface.py`,
`test_export_import.py`, `test_server_csrf.py`, `test_audit_visibility.py`,
`test_audit_witness.py`, `test_companions.py`, `test_export_bundle.py`,
`test_identity_surface.py`, `test_import_safety.py`, `test_memory_handles.py`,
and `test_recall_honesty.py` imports `from server import create_app`. Running
`pytest tests/ -q --continue-on-collection-errors` in this sandbox against
the current tree produces **49 failed, 121 passed, 22 errors** out of 192
collected tests.

This is not a stale-doc problem; the docs are largely right and the code has
regressed under them. `content/CLEMENTINE.md:42` still reads "✅ Working
(rebuilt)" for the Web Interface, and `content/VERIFIED.md` claims **229
tests** re-run against `master` on 11 August 2026 — both true when written,
both false today.

**How it happened, evidenced via git and the GitHub Actions API, not
inferred:**
- `a474702` ("feat: POST /api/transcribe (local Whisper via faster-whisper)",
  2026-08-20) replaced all 703 lines of `server.py` with the single word
  `PLACEHOLDER` (`git show a474702` — 1 insertion, 703 deletions).
- `5c47eb9` ("fix: restore server.py (remove PLACEHOLDER)", same day) changed
  `PLACEHOLDER` to `RESTORE_ME` — a one-word rename, not a restoration.
- Both commits are the only two on PR **#89**, titled *"WIP: local Whisper —
  DO NOT MERGE (server.py broken mid-push)"*. Its own description: "Restoring
  it is the next step... Grok is restoring `server.py` next. Leave this draft
  closed until green."
- CI on the PR head (`5c47eb9`) reports `conclusion: "failure"` (run
  `32325326049`). CI on `master` immediately after the merge also reports
  `conclusion: "failure"` (run `32335441403`, triggered by push, commit
  message "Merge pull request #89...").
- The PR **was merged anyway** (`merged: true`, `merged_by: CrystalArchitect`,
  `merged_at: 2026-08-20T05:23:53Z`) onto `master`, where it has sat for six
  days as of this review.

**Belt / convention.** `content/GOVERNANCE.md:19-22` states "every change...
passes the offline test suite before merging" and "the human steward
merges... nothing enters `master` without a human decision." Both halves of
that sentence were technically true and the outcome was still a broken
`master` — the human decision that was made overrode a mechanism whose entire
purpose was to catch exactly this. This is a Docs-governance breach with a
Science-belt consequence: the code's actual current behavior no longer
matches what several Science-belt documents assert about it.

**Recommendation.** Restore `clementine/server.py` from
`git show a474702^:clementine/server.py` (the last known-good, 703-line
version) as an explicit, reviewed change — not folded quietly into another
feature commit — and re-land the `/api/transcribe` wiring described in PR
#89's checklist on top of that restored base, since `crystalcore/whisper_stt.py`
and the `faster-whisper` dependency already exist and appear otherwise
unused. Re-run the full suite and confirm the "229 tests" (or current)
figure in `VERIFIED.md` before merging. Separately: consider making the `CI`
job's `unit-tests` and `python-tests` a required status check on `master` in
repository settings, since GOVERNANCE.md's rule currently relies entirely on
a human choosing not to override it.

*This fix was intentionally **not** made in this review's commit — restoring
700+ lines and re-integrating a half-landed feature is exactly the kind of
change this review is scoped to flag, not to perform.*

---

### HIGH — Two commercial language models carry locked "Crystal" names

**Rule.** *"No language model carries a Crystal name. The Crystal prefix
marks what this project owns and governs. Models are swappable faculties or
gated guests, and are called exactly that."*

**Evidence.** `content/ARCHITECTURE.md:23` lists, under "Voices Framework
(Active)": `**CrystalDreamer** — Vision and mythic development (Grok)`. The
same pairing, plus `CrystalScribe` for DeepSeek, recurs verbatim across five
more live (non-archive) files:

| File | Line |
|---|---|
| `content/CODEX.md` | 5 |
| `content/APOCRYPHON.md` | 5 |
| `src/routes/apocryphon/+page.svelte` | 17 |
| `src/routes/codex/+page.svelte` | 17 |
| `src/lib/components/Footer.svelte` | 20-21 |

`Footer.svelte` is a shared component (`showVoices` block), so this
attribution is live on every page of the SvelteKit app that renders it, not
buried in one archived document.

**Why it matters beyond the letter of the rule.** The Voices Framework is
explicitly Vision/Story — a working-method narrative, not a running system —
so this isn't a Belt-Three mislabelling in the usual sense. But the naming
rule is unconditional: it doesn't carve out an exception for mythic or
process labels, and the practical concern it guards against (a reader
assuming "Crystal" identifies something this project built and controls) is
just as live in an attribution line as in a technical spec.

**Recommendation.** Replace `CrystalDreamer`/`CrystalScribe` with names that
don't carry the prefix (e.g. keep the plain vendor names, "Grok" and
"DeepSeek", and drop the parenthetical relabelling entirely, or rename the
*roles* to something un-prefixed like "the Dreamer voice" if the role names
need to stay). Apply the same change everywhere in the table above and in
`archive/` is optional (archive is explicitly excluded from CI and treated as
superseded), but the six live occurrences should not ship with the prefix
attached to a named vendor model. This is a wording decision the maintainer
should make once, then apply consistently — not attempted as a drive-by edit
here.

---

### FIXED — Gendered pronouns for the companion were baked into prose the code's own data model says should stay open

**Evidence.** The runtime data model is correct (see Strengths). Outside it,
"she"/"her" is used to refer to the companion, unconditionally, in:

- `clementine/webapp/public/manifest.webmanifest:4` — `"A sovereign
  companion. She runs on hardware you own."` (this is the PWA install-prompt
  description a person actually sees before ever setting a gender)
- `clementine/deploy/clementine.service:7,19,21,38,56`
- `clementine/deploy/Caddyfile:18-20,32`
- `clementine/deploy/bootstrap.sh:18,37,63,65,84,86,115,166,167,181`
- `clementine/webapp/public/sw.js:1,6-7,13,15,80-81`
- `clementine/webapp/public/icon.svg:2`
- `.claude/skills/clementine/evals/evals.json:8,20,22` and
  `evals/RESULTS-2026-08-09.md` (eval named `honesty-about-where-she-runs`)

**Belt / convention.** None of this touches `BASE_PROMPT` or the
`Personality` model, so the companion a person actually talks to is not
mis-gendered by the running system. But the project's own rule — "until then,
they/them... deciding for them would be the one thing this rule exists
against" — reads as a statement about the project's voice generally, not
only about the one string sent to the model. A person reading the deploy
docs or the PWA install prompt before ever meeting Clementine encounters a
settled "she" the data model deliberately hasn't settled.

**Recommendation.** Reword the operational/comment prose to "they/them" or
neutral phrasing ("runs on hardware you own" needs no pronoun at all, as the
manifest fix in this PR shows). Lower priority than the two findings above
because none of it reaches the model or a stored profile — this is a
documentation-consistency issue, not a data-model bug.

**Fixed in this PR.** All instances listed above across
`manifest.webmanifest`, `clementine.service`, `Caddyfile`, `bootstrap.sh`,
`sw.js`, and `icon.svg` were reworded to they/them or pronoun-free phrasing
("she lives" → "they live", "her memory" → "their memory", the manifest
description dropped the pronoun entirely rather than defaulting it). The
`.claude/skills/clementine/evals/` fixtures were left untouched — they're
recorded eval inputs/outputs from a past run, not live prose, and editing a
dated eval record after the fact would misrepresent what was actually run;
that's a call for the maintainer if they want to re-run and re-date it.

---

### FIXED — `SECURITY.md` described a consent mechanism that doesn't exist in the code

**Evidence.** `SECURITY.md:19-20`: *"Cloud is opt-in only: the xAI provider
requires an explicit `/optin` and can be revoked with `/optout`; opt-in state
is recorded locally."* No `/optin`, `/optout`, or equivalent command exists
anywhere in `clementine/` (checked by grep across the tree). The actual
mechanism for reaching a non-local provider is the generic `ConsentGate` —
a per-call terminal prompt (`consent.py:177-190`) or, for the server,
pre-authorization via the `CLEM_REMOTE_OK` environment variable
(`wsgi.py:20-23,31-34`), with no persisted "opt-in state" and no
provider-specific command pair. `XAI_API_KEY` does exist, but only as the
third of three fallback environment variables for an API key
(`companion.py:156-158`), not tied to any `/optin` flow.

**Belt / convention.** This is a Science-belt claim in a security-relevant
document that does not match the code it describes — the exact drift
`GOVERNANCE.md` says must be corrected downward on discovery. It's a
lower-severity finding than the two above because the actual behavior
(fail-closed, gate-everything) is at least as strict as what's described, not
looser — nobody is exposed by the doc being wrong. But a security policy
that describes a mechanism which isn't there will mislead exactly the
audience (security researchers, cautious adopters) it exists to reassure.

**Fixed in this PR.** `SECURITY.md`'s bullet now describes the actual
mechanism (`ConsentGate`'s fail-closed refusal, pre-authorization via
`CLEM_REMOTE_OK=1`) rather than the `/optin`/`/optout` command pair, which
appears to describe an earlier or never-shipped design.

---

### LOW / NOTE — The one provider name with a hardcoded default is a partial exception to "never guess a vendor's address"

**Evidence.** `_default_endpoint()` and `_default_model()`
(`companion.py:201-241`) refuse to guess an endpoint or model for every
remote provider *except* `"grok"`, which defaults to `DO_INFERENCE_URL`
(`https://inference.do-ai.run/v1/chat/completions`, `companion.py:37`) and
`os.getenv("DO_INFERENCE_MODEL", "gpt-5-5")`. The code's own docstring
explains this is a backward-compatibility carve-out ("kept so setups that
already used the 'grok' alias keep working," line 35), not an oversight, and
it is still fully consent-gated like every other remote call — so this is
not a sovereignty violation in practice, only a narrower exception to the
stated principle than the principle's own wording ("every other remote
provider must be told where it lives") suggests exists.

**Recommendation.** No code change needed. Worth a one-line note in
`companion.py`'s module docstring or `SOVEREIGNTY.md` acknowledging the one
named exception, so a future reader doesn't have to find it by reading
`_default_endpoint()` line by line.

---

### LOW / NOTE — House style and boilerplate

- Australian/British spelling is followed consistently in original prose
  (`organise`, `authorise`, `recognise` throughout `content/` and
  `crystalcore/`). The one American-spelling instance found is GitHub's own
  default template boilerplate, `.github/ISSUE_TEMPLATE/bug_report.md:14,20`
  ("Steps to reproduce the **behavior**"/"Expected **behavior**") — not worth
  fixing, per the review brief's own instruction not to treat this as a big
  deal.

---

## Open questions for the maintainer / architect

1. **Branch protection.** Is `CI` currently a *required* status check on
   `master`? The PR #89 sequence shows a human can merge over a failing run
   today; if that's intentional (the steward's prerogative per
   `GOVERNANCE.md`), that's a valid governance choice, but it means the
   safety of `master` rests entirely on that judgment call being exercised
   correctly every time, which this instance shows doesn't always happen.
2. **Reconciling the restore.** Should `server.py` be restored verbatim from
   `a474702^` and the transcribe feature re-added on top afterward, or should
   the maintainer take the opportunity to review whether the pre-regression
   `server.py` is still the right shape given everything else that landed in
   PR #88 (`feat/pages-companion-face`) around it? This review does not have
   enough context on the intended `/api/transcribe` design to make that call.
3. **The mythos line "the Songlines are becoming Starlines"**
   (`content/CODEX.md:67`, `src/routes/codex/+page.svelte:83`). No component
   is named "Songline" — the hard rule is not broken — but the narrative
   frames the project's own coinage ("Starline") as a successor to or
   evolution of Songlines specifically, rather than as a separate, clearly
   distinct coinage running alongside them. The project's own boundary
   document warns that "stripping a name while keeping the structure is not
   a fix — it removes the acknowledgment, not the appropriation." Whether
   this specific line crosses that line is a cultural-sensitivity judgment
   this review isn't positioned to make; it's flagged for the steward (and
   ideally, per the project's own FPIC principle, for consultation with
   people who have standing to judge it) rather than resolved here.
4. **`CrystalBridge` naming.** The umbrella ecosystem's own convention table
   maps `CrystalBridge` to `crystalcore.bridge` + `ConsentGate`. This repo
   implements the same consent-gate concept as a *standalone*
   `clementine/crystalcore/consent.py`, with no reference to "CrystalBridge"
   anywhere in the tree, and no shared code with whatever `crystalcore.bridge`
   is in the umbrella/engine repo. Is that intentional (this app is meant to
   stand alone, pre-`CrystalBus`, and will adopt the shared name once it
   integrates with the wider mesh), or is it drift worth aligning now?

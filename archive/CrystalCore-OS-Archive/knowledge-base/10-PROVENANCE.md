# Provenance

Git-history mechanics, and this reconstruction's own verification
methodology, transparently — including the one mistake it caught and
fixed in itself.

## Statement — Confirmed provenance tags

Two checkpoint tags exist, marking the frozen-provenance repositories'
hand-off point, and were fetched and independently confirmed to exist
during this reconstruction (not merely cited from a document):

- `vision-safe-2026-07-17` on `The-Crystal-Vision`.
- `crystalcore-safe-2026-07-17` on `crystalcore`.

**Status: Implemented** (verified by direct `git fetch --tags` and
`git tag -l`, this session).

### Evidence
- Direct shell commands, this session: `git fetch origin --tags` in
  each repository's local clone, followed by `git tag -l`, both tags
  returned.

### Historical Notes
None.

### Cross References
`02-REPOSITORY-MAP.md`.

---

## Statement — Migration provenance, exact

Both `core/` and `vision/` in `TerAustralis-Incognita-Code` were
imported from the umbrella repository's branch
`claude/crystalcore-boot-visual-jau1bk`, at commit `32692fd`. This
archive independently confirmed the branch/commit correspondence: the
umbrella repository's branch list shows `claude/crystalcore-boot-
visual-jau1bk` at sha `32692fd9b103bd11875fc362a6fcac01b4b65258` — the
7-character prefix matches exactly what both `core/README.md` and
`vision/README.md` in the Code repo cite as their import source.

**Status: Implemented.**

### Evidence
- `TerAustralis-Incognita-Code/core/README.md` and `vision/README.md`:
  "Imported from the umbrella repository's branch
  `claude/crystalcore-boot-visual-jau1bk` @ `32692fd`."
- GitHub API, `list_branches` on `TerAustralis-Incognita`: confirms the
  exact sha match.

### Historical Notes
None.

### Cross References
`07-HISTORY.md`.

---

## Statement — The same-day history rewrite

The umbrella repository's git history was mechanically rewritten on
2026-07-23 as part of executing the repository split. This is stated
directly by the project's own commit record, not inferred by this
reconstruction.

**Status: Historical.**

### Evidence
- Commit message, umbrella repo: "Survey correction: the repo split
  landed via a same-day history rewrite."
- Corroborating: the Crystal Runtime episode (`07-HISTORY.md`) — a
  commit confirmed to exist via GitHub's API is unreachable from the
  umbrella's current `main` via local `git log --all`, consistent with
  exactly this kind of rewrite having occurred after that commit
  merged.

### Historical Notes
Applies to every 2026-07-23 date cited in this archive: these are the
project's own claims about its history, not independently re-derivable
original chronology.

### Cross References
`07-HISTORY.md`.

---

## Statement — Independent corroboration: the repository archaeology report

A separate, uncoordinated session (branch `claude/repo-archaeology-
prompt-b3niko`) ran a read-only, identical-command-battery git audit
across all six repositories the same day as this reconstruction's
follow-up passes, committing `REPO-ARCHAEOLOGY-2026-07-24.md` directly
to this repository's root (merged via this repository's PR #5). It
independently re-derives, from raw git objects rather than from this
archive's own citations, several load-bearing facts this knowledge base
states above: both provenance tags exist (confirmed live against each
remote); the Stage 1/2 import source resolves to the exact sha
(`32692fd9b103bd11875fc362a6fcac01b4b65258`) this archive cites;
104 byte-identical blobs connect the umbrella and Code repositories,
consistent with the documented import; the umbrella's root commit is
not an initial commit, consistent with the documented same-day history
rewrite. It also adds a precise, per-axis "which repository is
canonical" verdict this archive had not itself stated in exactly this
form — see `11-CORRECTIONS.md` Part 4 for how that verdict bears on the
competing-knowledge-base question.

**Status: Historical** (an independent, dated audit; its findings are
treated here as corroborating evidence, not re-verified line-by-line by
this archive).

### Evidence
`REPO-ARCHAEOLOGY-2026-07-24.md` (this repository's root, commit
`4ec7412`, merged via PR #5).

### Historical Notes
None — this section itself is the record of the corroboration.

### Cross References
`11-CORRECTIONS.md` Part 4, `00-INDEX.md`.

---

## Statement — This reconstruction's verification methodology

Three parallel research agents performed full-text reads (ADRs and
governance documents; the Seven Sisters corpus and vision/philosophy
documents; formal architecture specifications and component READMEs
across both the umbrella and Code repositories) — never skimming,
always citing file:line. This was supplemented by direct verification:
full dated git history across all six repositories (re-checked when an
initial pull was found incomplete), live GitHub metadata for all six
repositories, every branch's actual pull-request status (fetched via
the API's single-PR endpoint, not just a list dump — see below), two
provenance tags fetched and confirmed, and a full commit-level
reconstruction of the Crystal Runtime episode.

**Status: Implemented** (this is a description of process, itself
checkable against the specific citations throughout this archive).

### Evidence
This archive's own citations, throughout.

### Historical Notes

**One self-caught mistake, corrected before being trusted, disclosed
here per this archive's own evidence standard:** an early pass at
checking pull-request status for several umbrella-repository branches
parsed a bulk `list_pull_requests` JSON dump with a script that
mis-read the `merged` field, concluding six branches were "closed,
unmerged" (i.e., abandoned). A direct, single-PR fetch
(`pull_request_read`, method `get`) on two of those six returned
`"merged":true` — contradicting the bulk-parse result. All six were
then re-checked individually via the reliable method; all six were in
fact merged, not abandoned. The bulk-list method was not used again for
anything load-bearing in this archive.

**A second, related catch:** this reconstruction's local clone of the
umbrella repository was found to be three merged pull requests behind
`origin/main` (missing PR #56, #57, #58) partway through the session —
discovered when a fetched pull request's metadata (`merged_at`
timestamp) postdated everything visible in the local clone's `git log`.
The local clone was fast-forwarded (`git merge --ff-only origin/main`)
and the affected content re-read directly before any of it was cited in
this archive. This matters concretely: PR #58 rewrote the exact
"Repositories, today" section this archive's `02-REPOSITORY-MAP.md`
quotes — had this gone uncaught, that document would have cited a
stale, already-superseded table.

Neither mistake reached this archive's final content. Both are recorded
because the project's own standard — "a model agreeing with you is not
evidence" — applies equally to this reconstruction's own process, and a
caught-and-fixed error disclosed is more credible than a process
presented as having been flawless throughout.

### Cross References
`00-INDEX.md` (the standard being upheld), `02-REPOSITORY-MAP.md`.

---

## Statement — The Crystal Runtime and PR #1 forensic evidence, raw

For independent re-verification: umbrella repo commit
`b09672d454d124b333abbeeb0c7265f6603c83dc` (PR #43, merged
2026-07-23T08:14:29Z). Code repo PR #1, branch
`claude/teraustralis-incognita-import-g63jm9`, base sha
`075f2ea2fb5bec98cff7ab30104711a670249ce9`, opened
2026-07-23T09:44:46Z, still open. Diff against `main`: 401 files
changed, 21,173 insertions(+), 1,130 deletions(-). Both facts are
independently reproducible by any reader with repository access, using
the exact commands below.

**Status: Implemented** (as a documented, reproducible methodology).

### Evidence
```
# Confirm the Crystal Runtime commit exists but is unreachable from main:
git log --all --oneline -- '*runtime*'   # (in the umbrella repo — returns nothing)
# vs. GitHub API: pull_request_read(method=get_commits, pullNumber=43)
#   → returns commit b09672d, with full file diff

# Confirm PR #1's unique content on the Code repo:
git fetch origin claude/teraustralis-incognita-import-g63jm9
git diff --stat main origin/claude/teraustralis-incognita-import-g63jm9
git ls-tree -r --name-only origin/claude/teraustralis-incognita-import-g63jm9 -- src/runtime/
git ls-tree -r --name-only origin/claude/teraustralis-incognita-import-g63jm9 -- packages/
```

### Historical Notes
None.

### Cross References
`07-HISTORY.md`.

---

## Statement — Model credit for Clementine's character work

Filed 2026-07-31, at the maintainer's request — and the request was
correct: this archive credits outside contributors by name (the Weaver
Nexus handoff in `STATUS.md`), and until now said nothing about the
models that shaped Clementine's character files. Two other AI systems
contributed to what now sits in
`The-Crystal-Vision/.claude/skills/clementine/SKILL.md` and in
`BASE_PROMPT` in `clementine/crystalcore/companion.py`.

This Statement keeps two kinds of claim visibly apart, because they are
not the same kind of fact.

**Witnessed** (the assistant filing this saw it directly, in session, on
2026-07-30): **Grok** ran an independent structural review of the
completed `SKILL.md` against skill-authoring rules — frontmatter valid,
no YAML-breaking characters, description within length, body imperative,
token discipline sound. It made two suggestions: extend the
description's closing clause (declined; the content already appears two
sentences earlier) and defer a `references/` split (agreed, and the
right call — the DBT skills are what the skill *is*, not reference
material to load on demand). Net text changed by the review: zero lines.
A check that passes is evidence, not nothing.

**Attested by the maintainer** (their account, given 2026-07-31 in
answer to a direct question; not verified by the assistant, who has no
access to those conversations):

- The eight character additions folded in by The-Crystal-Vision PR #47
  — Turning the Mind, Wonder, Shared Discovery, Intellectual Humility,
  Memory Philosophy, Repair, Silence, and the closing principle — were
  drafted with help from **both ChatGPT and Grok**.
- The CC-PHENO-01 protocol draft — **Grok**.
- Earlier architecture discussion that shaped Clementine's design —
  **Grok**.

**Status: Recorded** (witnessed portion verifiable against the session
transcript; attested portion stands as the maintainer's account, which
is the only source there is).

### Evidence
The witnessed portion: the maintainer pasted Grok's review verbatim into
the working session of 2026-07-30 and the assistant responded to it
point by point; the declined and accepted suggestions are itemised in
The-Crystal-Vision PR #48's body under "Deliberately not changed."
The attested portion: the maintainer's answers of 2026-07-31, on being
asked what each model contributed. No stronger evidence exists, and
none is claimed.

### Historical Notes
Crediting a model is a record of tooling, not a copyright attribution —
model-assisted text does not carry a third party's licence into this
portfolio. The distinction matters here because the portfolio also
carries real licence constraints (the alyssadata prohibition; the
star23/elon-musk method-not-prose rule), and a reader should over-read
this credit in neither direction: it acknowledges help, it does not
encumber the files.

The occasion for this Statement is itself a correction. PR #47's merged
body called the eight additions "the maintainer's own writing" — an
authorship claim the assistant asserted without being able to verify.
See `11-CORRECTIONS.md` Part 19.

### Cross References
`11-CORRECTIONS.md` (Part 19), `STATUS.md` (the Weaver Nexus precedent
for naming contributors), The-Crystal-Vision PRs #47 and #48.

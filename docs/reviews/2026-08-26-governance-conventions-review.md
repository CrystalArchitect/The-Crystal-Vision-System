# TerAustralis Incognita — Governance & Conventions Review

**A fresh, independent pass checking whether this repository — the umbrella that defines the project's own rules — actually follows them.**

- **Surveyed:** 2026-08-26
- **Scope:** `CrystalArchitect/TerAustralis-Incognita` only (the umbrella/canon repo). This does not re-check the code repositories, the dbt warehouse, or the live site — see [`2026-07-23-architecture-survey.md`](2026-07-23-architecture-survey.md) in this same directory for that broader, earlier cross-repo pass. Several numbers in that survey are now stale (it counted "ten ADRs"; sixteen exist today, ADR-0011–ADR-0016 having landed since), which is itself a small illustration of the drift this repo's own honesty discipline exists to catch.
- **Method:** Direct reads of the governance, ADR, mythos, and research trees; full `git log --all` (659 commits, not a shallow clone) searched for naming history; every claim below is a file path and quote, not an impression.

**Finding labels used throughout** (matching this repo's own Belt-Three vocabulary):
- ✅ **Sound** — the rule is actually followed, verified by direct read
- ⚠️ **Drift** — two of the project's own documents disagree, or a document disagrees with its own directory
- 🔴 **Violation** — a stated rule is contradicted in a live, canonical document
- 🔧 **Fixed in this PR** — small, mechanical, already corrected
- ❓ **Open question** — needs a human decision; not answered here

---

## Summary

This repo's honesty discipline is real where it matters most: the three locked names are genuinely locked and unredefined, the Indigenous Data Sovereignty boundary is substantive rather than aspirational, and the retired edge-companion name has in fact been kept out of every live document — a rare thing for a fast-moving, AI-co-authored project to actually pull off. Set against that, the "Belt-Three" law is inconsistently defined between its own two canonical sources, and roughly 3,500 lines of genuine importable ML training code sit inside the umbrella repo's mythos folder under a description that fits only a fraction of what's actually there. "Songline" had also leaked into live documents as a component name, most seriously as an *active proposal* for a future component in `docs/OPEN-DECISIONS.md` — that one is struck in this PR, at the repo owner's direction, since a live naming proposal is exactly the case the rule exists to stop before anything ships; the four historical-record mentions of the retired `SonglineBus` repository name are a genuinely different case and are left open. Small textual defects (a corrupted word from an old find-replace, and an American spelling in the project's own style-setting document) are also fixed directly in this PR; everything else is documented with evidence for a human to weigh.

---

## Strengths

- ✅ **Locked names hold.** [`docs/governance/Constitution.md`](../governance/Constitution.md) §1 locks *TerAustralis Incognita*, *CrystalVision*, and *CrystalCore.Lattice* in a table with "Do not rename casually." A repo-wide search found no live document redefining any of the three; where the Constitution's own machinery (Lattice-delta, Weave-Map) hasn't been built, the document says so itself in a dated implementation note rather than letting the name imply more than exists.
- ✅ **The retired edge-companion name is actually retired.** [`mythos/NAMES.md`](../../mythos/NAMES.md) documents the discipline in detail — the name is deliberately not reprinted even in the page that explains the policy — and a search of the full history (`git log --all`, 659 commits, not a shallow clone) and the current tree found no live reintroduction. The one place the name persists is exactly where the project's own [Repository Principles](../governance/Repository-Principles.md) rule 3 ("preserve history — archive, don't delete") says it should: frozen material under `archive/`. `mythos/CREDITS.md` briefly reprinted it and was corrected within a day (per the dated 2026-08-09 amendment note at the bottom of `NAMES.md`) — a real mistake, caught and logged rather than quietly fixed.
- ✅ **Indigenous Data Sovereignty is substantive, not decorative.** [`docs/governance/Indigenous-Data-Sovereignty.md`](../governance/Indigenous-Data-Sovereignty.md) (119 lines) names concrete risks (extraction, flattening, misrepresentation, loss of governance), cites a real external framework (Maiam nayri Wingara), and states FPIC as a binding condition on ingestion ("No Songline knowledge has been ingested into any model, dataset or index in this repository, and none will be without Free, Prior and Informed Consent"), not just a value statement.
- ✅ **`docs/adr-0015-stop-growing-constellation` is merged, not open.** Confirmed via `git merge-base --is-ancestor`: it landed as PR #118 (commit `889f204`) and its content is already in `main` as `ADR-0015`. The remote branch ref is a stale, unpruned pointer to an already-merged branch — worth deleting as GitHub housekeeping, but not a governance issue and not acted on here per the brief.
- ✅ **Claims discipline, done right, exists in this repo.** [`docs/vision/Positioning.md`](../vision/Positioning.md) is a genuinely good model of the rule in §9 of the conventions: it dates its external reach estimate ("late July 2026"), calls it "third-party estimates from a single outside reading... reported here as claims, not measurements," and concedes the account's reach is small rather than inflating it. This is exactly the discipline the rest of this review is checking for elsewhere.
- ✅ ADR-0013 and ADR-0015 (both flagged in the review brief as load-bearing for a sibling review) were read in full. Nothing found here contradicts either, and neither was touched.

---

## Findings

### 1. 🔧 Fixed (partially) — "Songline" was used as a component name in live governance documents, including one actively proposing it as a future name

The rule, stated in this project's own words: *"'Songline' is never a component name... Where Songlines appear in mythos or art they are honoured as cultural image, never claimed"* ([`Indigenous-Data-Sovereignty.md`](../governance/Indigenous-Data-Sovereignty.md), restated in [`mythos/NAMES.md`](../../mythos/NAMES.md)). Two distinct cases existed, in live (non-archived) documents:

- **🔧 Fixed in this PR, at the repo owner's direction — a live, open governance document proposed it as a candidate name.** [`docs/OPEN-DECISIONS.md`](../OPEN-DECISIONS.md), under "Naming Disambiguation: Starline" (status: Vision 🔮, "last verified 2026-07-23", i.e. an open, unresolved question), previously read:
  > `- **Meaning A:** "Consent Transport" or "SonglineTransport" (already has clear module names)`
  > `- **Meaning C:** "Songline Network" (fictional, distinct from protocol names)`

  This was not a historical record — it was a currently-open recommendation list that a future PR could have acted on literally as written, which would have minted exactly the kind of component name the project's own Indigenous Data Sovereignty page forbids. Both candidates are now struck, replaced with an explicit `[name TBD — must not reference Songline, see Indigenous-Data-Sovereignty.md]` placeholder for each meaning, and a dated note in the document explains why. The actual replacement name is left open for the maintainer — nothing here invents a final answer, it only removes the disallowed ones.

- **Left open, as scoped — historical record.** A real pre-reorg repository was named `SonglineBus`, and four live documents repeat that name as the label for it: [`docs/TIMELINE.md:51`](../TIMELINE.md), [`docs/governance/Project-Boundaries.md:117`](../governance/Project-Boundaries.md), [`docs/REPOSITORIES.md:244,252`](../REPOSITORIES.md), [`docs/ARCHITECTURE.md:180`](../ARCHITECTURE.md) — e.g. *"The Songline protocol pack (SonglineBus, original architecture before Starline Weaver)"*. Unlike the OPEN-DECISIONS case, this is stated as fact about what a retired repository was actually called, not a proposal for something not yet built, and Repository Principle 3 says history should be preserved, not deleted — so this one is genuinely harder to resolve cleanly, and stays an open question below rather than edited.

**❓ Open question (unchanged):** Does the "Songline is never a component name" rule apply retroactively to *historical* facts about an already-renamed, already-retired repository (`SonglineBus`, tag `crystalcore-safe-2026-07-17`), or only to live/future naming? The current four documents describing that lineage read as factual record, not endorsement — but they do put "Songline" in a name-shaped position on the page. The maintainer who holds the actual repository history is better placed to decide whether to keep the name as historical record or rephrase around it (e.g. "the original, unnamed bus" or "the pre-Starline bus").

### 2. ⚠️ The "Belt-Three" law is defined two different ways by its own two canonical sources

[`docs/governance/The-Incognita-Rule.md`](../governance/The-Incognita-Rule.md) §1 defines exactly two kinds of line — Surveyed and Dreamed — and maps them to belts as *"Surveyed → Belt-Three: Science. Dreamed → Belt-Three: Story and Vision"* (Story and Vision as **one** combined belt). [`CONTRIBUTING.md`](../../CONTRIBUTING.md) §"The Belt-Three law (labels)" instead gives a table with **four** separate rows — Science, Story, Vision, and Docs/governance/process — and even documents its own drift in a footnote: *"Added the fourth row 2026-07-24: `.github/PULL_REQUEST_TEMPLATE.md` already carried it as a real, distinct checkbox — this table just hadn't caught up."* The PR template ([`.github/PULL_REQUEST_TEMPLATE.md`](../../.github/PULL_REQUEST_TEMPLATE.md)) matches CONTRIBUTING.md's four-row version, so two of the three canonical sources agree with each other but not with the one that explains the reasoning behind the law (`The-Incognita-Rule.md`), and none of the three currently explains why a "Belt-**Three**" law now runs on four rows split across two files that disagree about whether Story and Vision are one belt or two.

**Recommendation:** Either (a) rename the law to reflect four labels and reconcile `The-Incognita-Rule.md` to match, or (b) collapse `CONTRIBUTING.md`'s table and the PR template back to three rows (Science / Story+Vision / Docs-governance) to match the rule's own explanation. Not fixed here — this is the project's foundational honesty mechanism, and the brief reserves substantive governance edits for the maintainer.

### 3. 🔴 Real, importable ML infrastructure code lives in the umbrella repo, mislabeled by the one document that addresses it

[`docs/governance/Project-Boundaries.md`](../governance/Project-Boundaries.md) line 67 places `crystalcore-os` (this repo's copy: [`mythos/crystalcore-os/`](../../mythos/crystalcore-os/)) in the umbrella deliberately, describing it as *"Canon-as-code: a playable story, not infrastructure."* The directory holds nine Python files, ~3,500 lines total. One of them (`crystalcore_os.py`, 1,202 lines) is genuinely the playable mythos terminal the description names. The other eight are not:

- `huggingface_trainer.py` (299 lines) — a real DistilBERT fine-tuning pipeline built on `torch` and HuggingFace `transformers.Trainer`/`TrainingArguments`, with an explicit 28-class GoEmotions label map.
- `cross_attention_fusion.py`, `multimodal_emotion.py`, `uncertainty_quantification.py`, `active_learning.py`, `training_pipeline.py`, `dbt_integration.py`, `emotional_intelligence.py` — real, importable emotion-classification and active-learning infrastructure, wired together through a genuine package `__init__.py` (`mythos/crystalcore-os/__init__.py`) that exports classes like `BayesianUncertaintyQuantifier`, `CrossAttentionFusion`, and `DbtDataExporter`.

None of this is gameplay. It is exactly the kind of code the project's own boundary rule assigns elsewhere: *"if it is imported or called by other software it is Crystal Core"* ([`.claude/skills/teraustralis/SKILL.md`](../../.claude/skills/teraustralis/SKILL.md) §7, echoing `Project-Boundaries.md`'s own framing). `Project-Boundaries.md` does flag this location as "revisitable at Migration-Plan Stage 1" — so the maintainer already knows the placement is provisional — but the description attached to it today ("a playable story, not infrastructure") undersells eight of the nine files at that path.

**Recommendation:** Either move the eight ML-infrastructure modules to a Crystal Core repository (they have no dependency on the mythos terminal — `crystalcore_os.py` only calls three of them, for status-printing, not training), or, if they stay for now, correct `Project-Boundaries.md`'s description of the location to say what's actually there. Not moved in this PR — relocating working code across repositories is a structural change outside "mechanical/textual," and the brief reserves it for a human decision, consistent with `Project-Boundaries.md` already marking this placement as open.

### 4. 🔧 Fixed — a corrupted word from an old find-and-replace, in three places

A careless global rename (most likely a "replace this old edge-companion name with Clementine" pass, per the history documented in `NAMES.md` §"A retired name") appears to have also matched inside the unrelated word *illuminate*, corrupting it to **"ilclementinete"** / **"Ilclementinete"** in three places:

- [`docs/governance/The-Incognita-Rule.md`](../governance/The-Incognita-Rule.md) §2 — *"Story can ilclementinete, preserve meaning..."*
- [`mythos/content/CODEX-OF-THE-ORACLE.md`](../../mythos/content/CODEX-OF-THE-ORACLE.md) lines 314 and 367

All three corrected to "illuminate"/"Illuminate" in this PR. This is exactly the kind of drift the Incognita Rule itself warns about — a mechanical error sitting for weeks inside the document that explains why honesty about mechanism matters, undetected because nobody re-read the prose after the rename script ran.

### 5. 🔧 Fixed — American spelling in the project's own style-setting governance document

The project's writing convention calls for Australian/British spelling (*organise, colour, recognise* — [`.claude/skills/teraustralis/SKILL.md`](../../.claude/skills/teraustralis/SKILL.md) §8). [`docs/governance/Repository-Principles.md`](../governance/Repository-Principles.md) — the document stating the repo's own rules — used the American spelling "**Favor** reproducibility and clear evidence" twice (lines 16 and 51), and [`README.md`](../../README.md) line 166 used "in **favor** of" once. All three corrected to "Favour" in this PR. (Left alone: the much larger and more ambiguous population of `-ize`/`-ization` spellings such as "organize" and "recognize" scattered across dozens of mythos and docs files — `-ize` is legitimate Oxford/British spelling, not an unambiguous Americanism like "favor" or "color," so a mechanical sweep risks "fixing" correct British spelling. That population is real but lower-confidence and is left as a note, not a fix.)

### 6. ❓ Open question — the rights footer convention has no documented scope, and is applied to a minority of documents

The convention (`**All rights reserved.**` / `TerAustralis Incognita — ABN 70 741 068 059`) appears verbatim in [`research/closed-loop-embodiment.md`](../../research/closed-loop-embodiment.md) and throughout the `.claude/skills/` tree, and a related but distinct form ("Stewarded by the CrystalArchitect / ABN 70 741 068 059...") closes [`mythos/README.md`](../../mythos/README.md). It is absent from `Constitution.md`, `Indigenous-Data-Sovereignty.md`, `The-Incognita-Rule.md`, `CONTRIBUTING.md`, `ADR-0013.md`, `ADR-0015.md`, and the root `README.md`. No governance document states which document types are supposed to carry it, so it's unclear whether this is a broad, currently under-applied rule (in which case most of the repo's core canon is missing it) or a narrower convention meant only for certain content classes (mythos/research pages, or externally-shareable material). Not fixed here — stamping a footer onto the Constitution and every ADR on a guess about scope risks being wrong about intent in a way that's harder to undo cleanly than leaving it flagged.

### 7. ❓ Open question — the "numbered documents 01–09 are canonical" rule has no home in this repository

This project's writing conventions state: *"Numbered documents (`01-` … `09-`) are canonical; unnumbered duplicates in the proposal repo are superseded legacy."* A full search of this repository (`docs/`, `mythos/`, `research/`, repo root) found no `01-`…`09-`-prefixed canonical documents at all — the only numbered-prefix files anywhere are the unrelated `.claude/skills/starline-arsenal/models/01-…13-*.md` mental-model files, and this repo's ADRs use `ADR-000N` numbering, not the `01-`/`09-` pattern the rule describes. The rule's own text ("unnumbered duplicates *in the proposal repo*") suggests the 01–09 canonical set may live entirely in the sibling `teraustralis-proposal` repository rather than here — in which case the rule is accurately scoped and this repo simply has nothing to check it against, not a violation. Flagged rather than assumed either way, since confirming it requires reading `teraustralis-proposal`, which is outside this review's repo scope.

---

## Open questions for a human / architect

1. Which of the two Belt-Three definitions (three belts, per `The-Incognita-Rule.md`; four, per `CONTRIBUTING.md` and the PR template) is the one going forward — and should the law's name change if it's four?
2. Should `SonglineBus` (the real, retired pre-reorg repository name) continue to be named in the four historical/genealogy documents that currently print it, or be rephrased around, given the tension between "Songline is never a component name" and "preserve history, archive don't delete"?
3. Is `mythos/crystalcore-os/`'s ML-infrastructure code (everything except the terminal game itself) meant to stay in the umbrella repo, or move to Crystal Core at the next Migration-Plan Stage 1 pass that `Project-Boundaries.md` already anticipates?
4. What is the intended scope of the rights-footer convention — every canonical document, or a specific subset (mythos/research/externally-shared)?
5. Does a `01-`–`09-` canonical numbered-document set exist in `teraustralis-proposal`, confirming that this repo is correctly out of scope for that rule, or has that convention lapsed everywhere?

---

*Methodology note: this review reads only `CrystalArchitect/TerAustralis-Incognita`. It does not re-verify code, tests, or the live site — see the companion [2026-07-23 architecture survey](2026-07-23-architecture-survey.md) for that ground, keeping in mind its ADR count and repository-count figures are from that date and are now superseded by ADR-0015's own 2026-08-20 count.*

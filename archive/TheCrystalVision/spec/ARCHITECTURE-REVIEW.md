# Architecture Review — TheCrystalVision

**Status:** Independent pass · 2026-08-26
**Reviewer:** Claude (fresh review — no prior Grok/AI review artifact existed for this repo to build on)
**Scope:** Whole-repo architecture and convention audit against the project's own rules —
Belt-Three labelling, locked names, Indigenous Data Sovereignty, the Clementine name/pronoun
rule, and the Crystal Vision / Crystal Core project boundary.

This document itself follows the Incognita Rule: every finding below is checked against the
actual file, not against what a doc *says* the file does. File:line citations are to commit
`2ce1e01` on `main`.

---

## Summary

The repo is honest where it counts most — `spec/ARCHITECTURE.md` marks Built vs Vision
throughout, `services/decode.py` actually implements the quarantine-never-silently-dropped
claim its docs make, and `vision-plates/README.md` is a genuinely exemplary application of
the Indigenous Data Sovereignty rule (it proactively withheld real community names and a
sacred site from publication and explains why). Against that, three things need an
architect's decision: the repository's own identity is internally contradictory (it names
itself "Crystal Core" while living at a GitHub URL and role that other files in the same repo
describe as "Crystal Vision"), a technical component is named `SonglineBus` in running code
— a hard violation of the Indigenous knowledge boundary — and one Belt-Three "Science" claim
("impersonation rejected") overstates what the networked code actually enforces. None of
these are hidden; the repo's habit of labelling things means most of them surface themselves
to anyone who reads closely, which is itself a point in its favour.

---

## Strengths

- **Built vs Vision is a real discipline here, not decoration.** `spec/ARCHITECTURE.md`
  marks every row of its system map `●` (built) or `○` (vision) (`spec/ARCHITECTURE.md:31-63`),
  and `spec/BLUEPRINT-v0.3.md:4-6` opens by telling the reader the two documents "must never
  be confused." That is the Incognita Rule applied at the architecture-doc level, correctly.

- **The quarantine claim is Science, not Story.** `README.md:87` and `SECURITY.md:24-25`
  both claim invalid pipeline events are "quarantined with a reason, never silently dropped."
  `services/decode.py:24-89` actually does this — every rejection path returns a specific
  reason string, and `services/decode.py:79-89` collects them into a `quarantined` list rather
  than discarding them. Verified by reading the code, not by trusting the doc.

- **Belt-Three is enforced in code, with a passing self-test.** `ClementineHub.validate()`
  (`clementine/bridge/agents.py:24-31`) rejects any message without a lawful layer, and
  `clementine/bridge/selftest.py` proves it — confirmed by running
  `python3 -m clementine.bridge.selftest` during this review (3/3 passed).

- **No LLM carries a Crystal name.** The three live-model adapters are named `claude`, `gpt`,
  `grok` (`clementine/bridge/adapters.py:77,96,117`) — compliant with the rule that models are
  swappable, named guests, never Crystal-prefixed.

- **`vision-plates/README.md` is the standard the rest of the repo should be held to.** It
  documents, in its own words, that four "Country maps" naming real Aboriginal communities
  and Cave Hill / Walinynga (a Seven Sisters site with living custodians) were **excluded from
  the archive and never committed**, quoting the project's own FPIC standard as the reason
  (`vision-plates/README.md:241-253`). This is a project holding itself to the Indigenous Data
  Sovereignty rule under no external pressure to do so — genuinely strong governance.

- **The Pages publish workflow narrows on purpose.** `.github/workflows/static.yml:35-53`
  allowlists exactly four files instead of publishing the whole (private) repo, with inline
  comments explaining why each href was traced. Good sovereignty-of-publication hygiene.

---

## Findings

### 1. [HIGH] Repo identity contradicts itself — Crystal Vision vs Crystal Core
**Convention:** Project boundary rule / Docs-governance

The GitHub repo is `CrystalArchitect/TheCrystalVision`, but its own top-level docs declare it
to be the *other* project:

- `README.md:1` — `# CrystalCore`
- `README.md:4-7` — *"This is **Crystal Core** — the protocol pack... Siblings: **The-Crystal-Vision** = The Crystal Vision (codex site + Clementine sovereign companion app)"* — naming a **different, similarly-named repo** as the actual Crystal Vision app.
- `NOTICE:1-2` — `Crystal Core / Copyright 2026 Crystal Arena-Turner`
- `index.html:6,84` — page title `CrystalCore — Seven Sisters Songline`
- `spec/ARCHITECTURE.md:13` — points to `the-crystal-vision/crystalcore-app` as where the actual sovereign companion with memory/profiles lives — again, not this repo.

Per the project's own rule, *"if it renders or speaks for a human it is Crystal Vision; if it
is imported or called by other software it is Crystal Core."* This repo contains
`operator-card/` (a React UI rendered for a human operator — see Finding 6),
`interface/index.html` (an interactive demo UI), and `campaigns/`/`asset-packs/` (marketing
creative) — all Vision-shaped content — yet every self-description in the repo insists it is
Core. Meanwhile the GitHub name (`TheCrystalVision`) and the locked concept it evokes point
the other way. A reader cannot tell, from this repo's own files, which project it actually is.

**Recommendation:** This needs an owner decision, not a doc patch: either (a) this repo *is*
Crystal Vision and `README.md`, `NOTICE`, and `index.html`'s self-description are wrong and
should be corrected, or (b) this repo really is a Crystal Core protocol pack that happens to
be hosted under a Vision-shaped name, in which case the GitHub repo name itself is the
misleading artifact and Vision-shaped content (`operator-card/`, `interface/`) should move to
wherever the real Crystal Vision app lives. Either way, the "which repo is this?" section
(`README.md:5-7`) should resolve the question it raises, not restate the confusion.

### 2. [HIGH] `Songline` used as a component/class name in running code
**Convention:** Indigenous Data Sovereignty — hard boundary ("Songline is never a component name")

`clementine/bridge/bus.py:40` — `class SonglineBus:` — is imported and instantiated as a real
Python class:

- `clementine/bridge/run.py:14,43` — `from .bus import SonglineBus` / `bus = SonglineBus(hub, agents)`
- `clementine/bridge/selftest.py:9,13,21,29` — same import, three instantiations
- `clementine/bridge/bus.py:94`, `server.py:104` — markdown transcript headers literally titled `# Songline Bus transcript`

This is squarely the case the rule anticipates: not honouring Songlines as a cultural image in
prose (which the project does carefully — see Strengths), but naming a piece of software
after them. "Starline" and "Dreamline" are the project's own coinages for exactly this
purpose and are unused here.

**Recommendation:** Rename the class and its public vocabulary (e.g. `StarlineBus` or a
non-mythic name like `MessageBus`/`AgentBus`). This is **not** done in this review's commit —
the name appears in filenames (`clementine/SONGLINE-PROTOCOL.md`), CLI help text, README/
SECURITY/ARCHITECTURE prose, and two committed demo transcripts
(`clementine/transcripts/demo-*.md`) treated as a historical record. A rename here is a real
but mechanical refactor that should be its own reviewed PR, with an owner decision on the
replacement name and on whether the committed transcripts get corrected or left as dated
history. Flagging it here rather than silently fixing it is itself following the Incognita
Rule — this finding should not pretend to be smaller than it is.

### 3. [MEDIUM-HIGH] "Impersonation rejected" overstates what the networked bus enforces
**Convention:** Belt-Three labelling (a Science claim must be checkable against the code)

`README.md:66-67` and `SECURITY.md:20-23` both state, as a flat Science claim, that the bus
has "impersonation rejected." Reading the code:

- `clementine/bridge/agents.py:24-31` — `ClementineHub.validate()` only blocks one thing:
  `if msg.sender == self.name: return False, "no agent may speak under the hub's name"`.
  It does not check whether a message's sender is the agent that actually holds the current
  turn.
- In-process (`bus.py:59-67`) this is safe by construction — the bus itself sets
  `sender=agent.name` from the `Agent` object it is iterating, so an agent cannot lie about
  its own name.
- Over the network (`clementine/bridge/server.py`), the sender name is **client-supplied**
  and unauthenticated: `join()` (`server.py:53-60`) accepts any name and treats a second
  `/join` with a name already in use as a `"rejoined": True` no-op rather than a conflict, and
  `speak()` (`server.py:69-76`) only checks whose *turn* it is, not who is entitled to speak
  as that name. Anything that can reach the port and guesses/knows an agent's chosen name can
  speak as that agent.

So "impersonation rejected" is true for the hub's name and true in-process, but not true for
peer-agent identity on the networked bus — the one case an outside reader would most expect
"impersonation rejected" to cover.

**Recommendation:** Either narrow the claim in `README.md`/`SECURITY.md` to "the hub's
identity cannot be impersonated; peer-agent identity on the networked bus is unauthenticated
and not verified" (a Belt-Three relabelling — cheap and honest), or close the gap in code with
a per-agent join secret returned by `/join` and required on `/speak`. This review does not
make that code change — it is a real design decision (does the bus want lightweight auth at
all, given it is explicitly "not a hosted or authenticated service" per
`clementine/SONGLINE-PROTOCOL.md:114-121`?) that belongs to whoever owns that tradeoff.

### 4. [MEDIUM] Hardcoded gendered pronouns for Clementine — fixed in this commit
**Convention:** Clementine's name/pronouns ("empty until set... they/them, not as a verdict")

Three files hardcoded "she"/"her" for Clementine, in prose that never mentions a choice being
made:

- `clementine/CLEMENTINE.md:14,17-18,28,48,50` (six occurrences)
- `clementine/bridge/agents.py:3-4` (docstring)
- `clementine/SONGLINE-PROTOCOL.md:96`

This is the same violation the `teraustralis` skill's own canon notes as already fixed once,
elsewhere, on 2026-07-29 (`mythos/content/CLEMENTINE.md`) — but that fix did not reach this
repo's independent copy of the same document at `clementine/CLEMENTINE.md`, because it's a
different file in a different repo. **Fixed in this commit**: all six occurrences plus the two
code/doc comments now use "they/them," verified against `python3 -m clementine.bridge.selftest`
(3/3 still passing — this was a comment/prose-only change).

Note for the open-questions section: this repo's `ClementineHub` has no `Personality` object,
no `gender` field, and no memory at all — it is a stateless per-process message router, not
the persistent "companion a person actually talks to" the naming table describes. The pronoun
fix is applied because the *name* triggers the rule regardless, but whether this component
should carry the name "Clementine" at all is a separate, larger question (see Open Questions).

### 5. [MEDIUM] `LICENSE` references files that don't exist in this repo
**Convention:** Docs-governance (a legal document with dead internal references)

`LICENSE:26-29` carries an "EXCEPTIONS" clause:
```
• mythos/ directory: CC BY-NC-ND 4.0 (see LICENSE-CONTENT.md)
• Concepts inspired by MemClaw: Acknowledge MemClaw's Apache 2.0 license
  (see docs/ATTRIBUTIONS.md)
```
This repository has no `mythos/` directory, no `LICENSE-CONTENT.md`, no `docs/` directory, and
no `ATTRIBUTIONS.md` anywhere (`find` over the full tree confirms this). The clause reads as
boilerplate carried over from a sibling repo (several TerAustralis repos do have a `mythos/`
directory) without being adapted to what this repo actually contains.

**Recommendation:** Either remove the EXCEPTIONS clause here, or point it at files that
actually exist in this repo. Left as-is, the license's own text asserts the existence of
things a reader can check are absent — a small-scale version of exactly the "dreamed line
presented as surveyed" problem the rest of the repo is careful about elsewhere.

### 6. [MEDIUM] Human-facing UI code lives inside a repo self-identified as "Crystal Core"
**Convention:** Project boundary rule

`operator-card/src/components/gate-console.tsx` is a complete React component with local
state, a five-door consent simulator, revoke/reinstate buttons and an event ledger — i.e.,
something that renders for a human operator. `lattice-map.tsx` and `public-node.tsx` are
similarly UI-rendering components. This sits inside a repository whose `README.md:1`,
`NOTICE:1`, and `index.html:6` all title themselves "Crystal Core" — the half of the boundary
rule that explicitly excludes anything that "renders or speaks for a human."

This is really the same root cause as Finding 1, viewed from the code side rather than the
doc side: **either** the repo's self-description is wrong, **or** `operator-card/` is in the
wrong repo. Recommendation: resolve alongside Finding 1 rather than as a separate move.

### 7. [LOW] Consent-in-UI requirement has no live implementation in this repo
**Convention:** Architecture constraint (consent must be a surfaced runtime property, not just backend)

`operator-card/src/components/gate-console.tsx:183-187` is honestly labelled: *"Preview only
... Not connected to CrystalCore runtime."* That's good practice — it does not pretend to be
live. But it means the actual requirement ("consent is a runtime property... enforced at the
gate," surfaced in UI) has **no live implementation anywhere in this repo** — the real
`ConsentGate` is said to live in a different repo entirely (`README.md:7`,
`TerAustralis-Incognita-Code/core/crystalcore/`). Not a violation (nothing here claims
otherwise), but worth surfacing as an open question below.

### 8. [LOW] Networked bus has no authentication even when explicitly exposed
**Convention:** Architecture constraint (fail-safe = local isolation, never fail-open)

`clementine/bridge/server.py:184` defaults `--host` to `127.0.0.1`, and `SECURITY.md:20-23`
is upfront that exposing it is "an explicit operator choice" with "no accounts, no tokens, and
no transport encryption." This is disclosed, not hidden, so it's a low-severity note rather
than a violation — but it compounds Finding 3: once `--host` is used, there is no mechanism at
all standing between "anyone who can reach the port" and "can speak as any agent name." Worth
a one-line SECURITY.md addition making the impersonation gap (Finding 3) explicit alongside
the existing encryption/auth disclosure, since a reader currently has to reach that conclusion
by reading `server.py` rather than being told.

### 9. [LOW / no action needed] Australian/British spelling
House style ("honour," "labelled," "organise") is used consistently across the docs checked
in this review. No concern — noted per the review brief, not because it needs fixing.

---

## Open questions for a human/architect decision

1. **What is this repository, actually?** (Finding 1/6) Its GitHub identity, its own README's
   self-description, and its actual file contents point three different directions. This
   review cannot resolve it — it can only confirm the contradiction is real and file-backed.

2. **Should `SonglineBus` / "Songline Bus" be renamed project-wide?** (Finding 2) If yes, what
   replacement name, and what happens to the two committed demo transcripts and the
   `SONGLINE-PROTOCOL.md` filename that currently carry the same name as historical record?

3. **Is `clementine/bridge/`'s `ClementineHub` the same "Clementine" the naming table and the
   pronoun rule describe**, or a differently-scoped reuse of the name for an AI-to-AI router
   that has no memory, no profile, and no persistent identity at all? If it's a genuinely
   different thing, does it need its own name rather than borrowing one that's already spoken
   for elsewhere in canon?

4. **Does a live, network-connected Crystal Vision UI for the actual ConsentGate exist
   anywhere today**, beyond this repo's disconnected `operator-card/` preview? If not, that's
   a real gap against the "consent surfaced in UI, not just backend" architecture constraint —
   just not one this repo can be faulted for alone.

---

*Reviewed against `main` @ `2ce1e01`. This document follows Belt-Three: findings above are
Science (grep/read against the actual file), not Story about what the repo intends.*

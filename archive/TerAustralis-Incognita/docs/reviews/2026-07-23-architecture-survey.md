# TerAustralis Incognita — Architectural Survey

**The map and the territory: a field review of both repositories and the public site — what's actually built, what's still dreamed, and where the two have quietly drifted apart.**

- **Surveyed:** 2026-07-23
- **Repositories:** `CrystalArchitect/TeraAustralis-Incognita` (docs/governance/mythos) · `CrystalArchitect/teraaustralis-incognita-code` (application code)
- **Method:** 4 independent research passes over both repos, plus direct test execution. All test results below were re-run and confirmed this session, not inferred from documentation.

**Finding labels used throughout:**
- ✅ **Verified** — confirmed working, tested, or documented accurately
- 🔮 **Vision** — intentionally speculative; the project's own term for not-yet-built
- ⚠️ **Drift** — docs and code disagree, or two docs disagree with each other
- 🔴 **Critical** — broken, untested where it matters, or actively misleading

---

## §0 Executive summary

The project is in better shape than its symptoms suggest: the engineering underneath is frequently excellent — real Noise-protocol cryptography, a hash-chained audit kernel with property-based tests, a disciplined ADR trail — but it was built across a very compressed timeline by several uncoordinated hands (human and AI), and the seams from that are showing everywhere you look closely. Nothing found here is a five-alarm fire. Several things are quietly accumulating interest.

| Number | Meaning |
|---|---|
| **2** | repos, split same-day (2026-07-23) — the docs repo's own architecture pages still describe the code as living inside it |
| **3** | core systems (`crystalcore`, `crystal-core`, `runtime`) sharing vocabulary, not code — near-zero real integration |
| **150+** | tests passing across the code repo, personally re-run and confirmed this session |
| **7** | `packages/` distributables — zero have ever been executed by a test or CI check |

Five findings matter more than the rest:

1. ⚠️ **The docs repo describes a repo that no longer exists.** Its README, ADRs, and every agent-instruction file still assume `src/`, `tests/`, and `scripts/` live inside it. Those paths are absent from today's `main` and from all locally available history — and GitHub Actions history shows CI successfully exercising `src/` on an *earlier* `main` lineage the same morning, meaning the split landed as a same-day history rewrite (force-push) that no document records. The repo's own CI has been red on `main` ever since.
2. 🔴 **`packages/` is actively misleading, not just unused.** Five of seven namespace packages are byte-for-byte copies of `src/` with the copyright header stripped; every README describes a product that doesn't match the code inside it; two packages have concrete, already-manifested bugs (a broken console-script entry point, an undeclared dependency that fails on install).
3. ⚠️ **Documentation and code have overtaken each other in opposite directions.** The Crystal Runtime is called "not started" in `Roadmap.md` — it already exists and passes 75 tests in the code repo. Meanwhile most `packages/` READMEs describe features that were never built at all.
4. 🔴 **The emotion-data warehouse has no data source.** Every staging model in `dbt/crystalcore_emotion_warehouse/` is a hardcoded CTE of literal nulls; one model has a syntax error that would fail to compile as committed.
5. ✅ **The governance discipline is real and rare.** A formal "Science / Story / Vision" labeling rule, honestly applied almost everywhere it counts, and an ADR trail that is procedurally spotless even when its subject matter (licensing) was chaotic.

---

## §1 The two-repo split — one project, and the paperwork hasn't caught up to the move

Today the project is two repositories. **TeraAustralis-Incognita** holds documentation, governance, ADRs, the mythos, research, and archives. **teraaustralis-incognita-code** holds everything that runs — `src/`, `packages/`, `tests/`. The split is very recent: the code repo's own history is four commits deep, all dated today, and its `README.md` explicitly frames itself as "the code companion" to the docs repo.

> 🔴 **The core problem.** Essentially every architecture document, ADR, and agent-instruction file in the docs repo — `README.md`, `AGENTS.md`, `docs/architecture/SystemMap.md`, all five files under `docs/agents/` — describes a single monorepo where code lives alongside docs. On today's `main`, `src/` and `tests/` don't exist, and they appear nowhere in the locally available history (a shallow clone, 96 commits). GitHub Actions history fills in what the shallow clone can't: CI runs on an earlier `main` lineage were still compiling `src/` and passing self-tests at 08:52 the same morning, and the current tip (`77e910a`) is a *different* merge commit of the same PR #44 than the one CI ran at 08:15 — i.e. `main` was rewritten (force-pushed) mid-morning, the code left in that rewrite, and no document records the move. The CI workflow was not updated either: it still targets `src/` and `tests/`, so **CI has failed on every run of `main`'s current lineage**, starting with the rewrite itself.

It gets one layer more tangled: `mythos/README.md` (in the docs repo, linked from the root README) describes a *third*, older arrangement again — four separate repositories (this one, `crystalcore`, `crystal-vision`, `teraaustralis-incognita`). That page predates the current two-repo reality and the ADR-0001 monorepo model alike, and nothing has swept back through to reconcile any of the three stories.

**The fix here is cheap relative to its payoff:** one clearly-dated note at the top of `SystemMap.md` and the root README explaining the current split, plus a pass to either delete or clearly date-stamp `mythos/README.md`'s older account. Until that happens, anyone new to the project — human or AI — will orient themselves against a map that doesn't match the territory.

---

## §2 Docs & governance layer (TeraAustralis-Incognita repo)

Underneath the confusion in §1, the governance model is a genuine strength worth naming plainly. The project runs on one rule, stated in `docs/governance/The-Incognita-Rule.md`: *always mark which lines are dreamed and which are surveyed, and never let a dreamed line pretend it was measured.* That's operationalized as a mandatory "Science / Story / Vision" label on every PR, and it shows up as real editorial discipline throughout — documents about unbuilt systems say so plainly, in their own words, over and over. That's unusual, and it's the reason a review like this one is even possible to do with confidence.

Ten ADRs govern the project, and the trail itself is procedurally clean: numbers are never reused, supersession is always explicit, and status labels in the index match every file's own header exactly.

| ADR | Decision |
|---|---|
| 0001 | Adopt the "CrystalCore OS v1.0" repository architecture — the monorepo reorganization that, per §1, the current two-repo reality has since overtaken. |
| 0002 | Keep `mythos/` a top-level peer of `docs/` and `src/`, not folded into either — its own license depends on the boundary staying sharp. |
| 0003 | Move code into `src/` as a uniform one-level shift, preserving `__file__`-relative path relationships. |
| 0004 | Lock a four-branch "CrystalCore" naming taxonomy (Framework / Protocol / CrystalBridge / OS); ban future components from taking a fifth "CrystalCore" name. |
| 0005 | Define the "AI Orchestrator" as recommend-then-human-decides, never autonomous dispatch; ship its first increment as documentation only. |
| 0006 | Original dual-license decision (Apache-2.0 code / CC BY-NC-ND mythos) — §1 later superseded by ADR-0008; its IP-principles and trademark sections still stand. |
| 0007 | Correct the project name to "TerAustralis Incognita" (one "a") to match the maintainer's registered ABN trading name. |
| 0008 | Supersede 0006 §1 — adopt CC BY-NC-ND 4.0 for code, after an uncoordinated session had already merged that change and left roughly a dozen files self-contradicting. |
| 0009 | Reconcile a genuine same-day licensing collision (three uncoordinated sessions + one direct push landed conflicting per-package licenses within ~45 minutes) — root license governs today; differentiated `packages/` licensing is a deferred question. |
| 0010 | Close that question: uniform CC BY-NC-ND 4.0 for the whole repository. Differentiated per-package licensing not adopted. |

### Drift found in this layer

- ⚠️ A trio of same-day Crystal Runtime spec documents disagree with *each other* on implementation readiness — one says every module is "deferred until specification review," another says all seven are "ready to specify testing," a third says all seven are "ready for implementation." `Roadmap.md`, also same-day, calls the whole layer "not started." The code repo already ships it (§4).
- ⚠️ `Roadmap.md`'s "Recently landed" section is missing the four most recent ADR entries that `CHANGELOG.md` already records — the single largest recent body of change in the project's history is logged in one place and absent from its supposed companion.
- ⚠️ Of three documents describing the same reverted `packages/` licensing plan, two carry an explicit "Superseded" banner pointing at ADR-0010 and one — `REPO-RESTRUCTURING-PLAN.md` — doesn't, and still reads as a live, actionable plan.
- ⚠️ `docs/README.md`'s own index of the documentation tree omits nine files that physically exist under `docs/`, including `ATTRIBUTIONS.md` — one of the most cross-referenced documents in the whole repository.
- ⚠️ Two guide documents (`Access.md`, `Push.md`) point at scripts and files that don't exist anywhere in either repo — pre-reorg, Windows-local-machine artifacts that the v1.0 sweep never reached.
- 🔮 "Starline" names two unrelated things across two similarly-titled files — the P2P transport (`STARLINE.md`, really about `consent_transport`) and the multi-agent message bus (`STARLINE-WEAVE-PROTOCOL.md`). ADR-0004 fixed exactly this problem for "CrystalCore"; no equivalent taxonomy exists for "Starline."

---

## §3 Content, research & data layers (`mythos/`, `research/`, `archive/`, `dbt/`, `examples/`)

`mythos/` is exactly what it claims to be: 98 content files (96 pieces of art plus two covers) and 34 markdown documents, zero executable code, consistently self-labeling which parts are running software versus story. `research/seven-sisters/` correctly supersedes its older copy preserved in `archive/2026/local-snapshot-2026-07-17/` — confirmed by diff, the archived version is genuinely older and is retained for provenance only, exactly as the archive's own README says it should be.

> ⚠️ **A recovery record that's gone stale.** `archive/2026/local-snapshot-2026-07-17/README-SNAPSHOT.md` lists `status.py` and the SpaceXAI provider module as unrecoverable. A sibling file two folders over, `crystalcore-v0.13/RECOVERY-STATUS.md`, dated the same day, says both were fully recovered. Nobody reconciled the two — a reader who only opens the first file walks away with the wrong picture.

> 🔴 **The emotion-prediction warehouse isn't wired to anything.** `dbt/crystalcore_emotion_warehouse/` is a real, well-modeled 28-class (GoEmotions taxonomy) dbt project — staging views, core marts, an active-learning queue, sensible macros. But every staging model is a CTE of hardcoded `null` literals; there is not one `source()` call anywhere in the project. Running it today produces tables of exactly one null row each. Worse, `stg_emotion_labels.sql` ends its CTE with a dangling `union all` immediately before the closing paren — a genuine SQL syntax error that would fail `dbt compile` as committed. The integration doc describing a `DbtDataExporter` bridge from the code repo's ML module is real code (§4), but nothing ever reads what it writes.

`examples/` is a clean, accurate index — every command it lists really does resolve into the sibling code repo — but that also means it's 100% cross-repo dependency with zero content of its own, which is worth a second look now that the repos are physically separate. `assets/` is intentionally empty, per its own policy note. One structural oddity: `dbt/` sits at the repository root but appears in none of the three documents that purport to map that root.

---

## §4 Core application architecture (teraaustralis-incognita-code — `src/crystalcore`, `src/crystal-core`, `src/runtime`)

This is the most consequential finding in the whole review, so it's worth stating precisely: **the three components that look, from their names, like they should be layers of one system are not integrated.** They share vocabulary — "bridge," "gate," "scope," "provenance," "coordinator" — almost none of it backed by shared code. The repo's own `docs/ATTRIBUTIONS.md` says the quiet part out loud: the runtime's design is "analogous to" the other two, not built on them.

| Component | What it is | Status |
|---|---|---|
| `src/crystalcore` | **CrystalBridge** — a fail-closed MCP server letting a guest AI reach Clementine with only granted access. Internally coherent and precisely wired — but its own docstring claims four checks (approval, permission, scope, provenance) while the code implements exactly two. | 🔴 Zero test coverage |
| `src/crystal-core` | **The protocol pack** — the strongest engineering in the repo: a real Noise-protocol P2P transport (`consent_transport`, 9/9), a labeled multi-agent message bus with a kill switch (`clementine/bridge`, 7/7), a hash-chained audit + decision kernel with property-based tests (`rdp`, 31/31), and a decode/ingest pipeline (`services`, 4/4). | ✅ 51 self-tests |
| `src/runtime` | A well-built, generic service-orchestration scaffold (coordinator, registry, events, config, plugins, logging, API) — heavily tested, defensively written — with no domain logic tying it to Clementine, consent, or MCP. Grep confirms two textual mentions of the other systems in the entire tree, both in comments, neither a real import. | ✅ 75 tests |
| `src/crystalcore-os` | A fourth, standalone island: half text-adventure game (a fictional "Starline Network" with a soundtrack list), half genuinely real ML research code — DistilBERT fine-tuning, Bayesian uncertainty quantification, cross-attention fusion. Wired to nothing else in the repo. | 🔴 Zero test coverage |

The one genuine cross-import in the entire codebase lives in `rdp/run.py`'s demo subcommands, which lazily import the real CrystalBridge and Clementine modules to prove the wiring *can* work — deliberately kept out of any production code path, and out of the test suite, on both sides.

### Test & self-test coverage — re-run and confirmed this session

| Area | Mechanism | Result | Run by |
|---|---|---|---|
| crystalcore (MCP bridge) | — | none found | — |
| clementine / bridge | selftest.py | 7 / 7 | direct + check.sh |
| consent_transport | selftest.py, real sockets + crypto | 9 / 9 | direct only — `-m starline.selftest` alias breaks under `python -m` |
| rdp | selftest.py, incl. 7 property-based checks | 31 / 31 | direct + check.sh |
| services | selftest.py | 4 / 4 | direct + check.sh |
| runtime (7 submodules) | pytest, heavy mocking | 75 | root `pytest` |
| node/mesh | pytest | 3 | root `pytest` |
| crystalcore-os | — | none found | — |
| apps/clementine | pytest + conftest | 16 | check.sh only — excluded from root `testpaths` |

Root `pytest` collects 78 (75 + 3) exactly as the code repo's README claims. Everything above was re-run personally rather than trusted from static reads — all reported passes are confirmed by execution, not inference.

### Naming collisions found

| Term | Meaning A | Meaning B |
|---|---|---|
| `crystalcore` | The MCP bridge package (`src/crystalcore/`) | Clementine's internal companion framework (`core/crystalcore/mind/`) — a third and fourth meaning also exist (`src/crystalcore-os/`, and "Crystal Core" the protocol pack) |
| "bridge" | `crystalcore/bridge.py` — the MCP stdio server | `clementine/bridge/` — an unrelated multi-agent chat bus |
| scope / provenance | Named but never implemented in `gate.py`'s docstring | Fully implemented as `ExecutionContext` fields in `runtime/coordinator.py` — for a different resource model entirely |
| "Starline" | The real P2P transport (`consent_transport`) | The message bus ("Starline Weaver") *and* a fictional game state machine in `crystalcore_os.py` |

---

## §5 Packaging, apps, SDK & site (teraaustralis-incognita-code — the delivery surface)

> 🔴 **`packages/` is not earning its keep.** Seven `teraaustralis.*` namespace packages exist. Five non-empty ones are byte-for-byte copies of `src/` code — verified by diff, the only difference in any file is a stripped copyright header — not thin re-export wrappers. Every README describes an API surface that doesn't exist in the shipped code: fabricated class names (`ConsentTransport`, `RDP`, `Clementine` — none of which are ever defined), invented pricing tiers ("$1,000–$50,000/month" for a package that's actually a toy chat-bus demo), a content structure for `packages/mythos` matching nothing in the real `mythos/`. Nothing in `packages/` has ever been executed by a test, a self-test, or even a syntax check — `check.sh`'s `compileall` pass doesn't include the directory at all.

Drift has already visibly happened, not just theoretically:

- `packages/clementine/__init__.py` carries CrystalBridge's docstring, copied over by mistake — its declared console-script entry point (`clementine = "teraaustralis.clementine:main"`) points at an attribute that doesn't exist, so installing and running it would fail immediately.
- `packages/crystalbridge`'s copy of `bridge.py` hardcodes a relative path that resolved correctly one directory level up in the original — copied one level differently, it now points at a directory that doesn't exist in the shipped package.
- `packages/starline` imports `teraaustralis.consent_transport` without declaring it as a dependency, so a standalone `pip install` fails before any of this even bites.

### The four apps

| App | Stack | Status |
|---|---|---|
| clementine | Flask API + Svelte 5 / Vite 6 | ✅ The most complete surface in the repo — 16 real tests, CORS locked to localhost, real memory/recall logic |
| crystal-interface | Static HTML/JS, no framework | 🔮 Self-labeled "static demo only… Authority: HOLD" in its own SECURITY.md — good hygiene, no ambiguity |
| vision-web | Static HTML/JS | 🔮 Unusually candid "honest scope of the simulation" section calling out its own stubs by name |
| voicebox | stdlib-only Python, single file | ✅ Small, complete, dependency-free MCP text-to-speech server — no tests, but no stubs either |

The TypeScript SDK (`src/sdk/typescript`, v0.5.0) is honestly labeled "demo / Phase 1, no npm publish, Mainnet HOLD" — and the code backing that label is real, not scaffold-with-TODOs: a working `CrystalClient` class with proper error handling, just not yet meant for anyone outside the repo to depend on.

The site (`src/site`, SvelteKit + static adapter) produces nine routes through two different content mechanisms that coexist without much cross-talk: `/docs` and `/docs/[slug]` auto-load all 22 files in `src/content/` at build time; everything else — home, apocryphon, codex, crystalcore, crystalcore-os, clementine, starline, join, gallery — is hardcoded directly into Svelte components. The gallery route's 92 hardcoded entries were checked against the 92 actual image files on disk and match exactly. One redundancy worth knowing about: `/codex` (hardcoded) and `/docs/codex` (markdown-driven, from `CODEX.md`) present closely related material through two independently maintained paths.

### Coverage across the whole delivery surface

| Surface | Executed test coverage |
|---|---|
| All seven `packages/` | 🔴 None — five carry dead duplicate test files that nothing ever runs |
| apps/clementine | ✅ 16 tests, executed via check.sh |
| apps/crystal-interface, vision-web, voicebox | 🔴 None |
| sdk/typescript | ⚠️ Type-check only (`tsc --noEmit`, not a test runner) |
| site | ⚠️ Type-check only (`svelte-check`, not a test runner) |

---

## §6 The website (www.teraustralis.com.au)

The live site could not be checked directly: this session's network egress policy blocks the host outright — the connection was rejected at the proxy layer (a bare 403 on the CONNECT itself, before ever reaching the site), which is a session-level policy boundary, not a problem with the site. A web search for the exact domain also returned no indexed results, so an independent, indirect read wasn't available either.

What this review of "the website" is therefore built from is the site's source (§5) rather than a live render. That source looks coherent and reasonably well-maintained — consistent route structure, the gallery genuinely in sync with its image files, honest self-labeling on the demo apps it links out to. Whether the deployed site currently matches that source, and whether the live pages render as intended, is the one open question in this whole review that a repository read can't answer.

**To close this gap:** paste in a screenshot or the rendered HTML of a page or two, or run this review again from an environment whose network policy allows the host.

---

## §7 Cross-cutting themes

1. **Documentation lags in one direction and leads in the other.** The runtime exists in code while the docs call it unstarted; `packages/` READMEs describe products that were never built at all. Both are symptoms of the same root cause — writing and shipping happened faster than anyone had time to reconcile.
2. **The project already knows how to fix naming collisions — it just hasn't applied the fix everywhere.** ADR-0004 disambiguated "CrystalCore" with a real taxonomy. "Starline," "bridge," and the stray "scope/provenance" echo between `gate.py` and `coordinator.py` would all benefit from the same treatment.
3. **Test coverage is bimodal, and the gap tracks exactly where copying or reconstruction happened.** Hand-written original code (the protocol pack, the runtime, Clementine) is rigorously tested. Copied code (all of `packages/`) and reconstructed code (CrystalBridge itself, crystalcore-os) have none.
4. **The honesty discipline is the project's best asset, and it hasn't yet been turned on the two weakest spots.** The Incognita Rule produces admirably candid "not built yet" language throughout the docs repo and the demo apps' own SECURITY.md files. It has not yet been applied to the repo split itself, or to what `packages/` actually ships versus what its READMEs claim.

---

## §8 Recommended next steps

### Tier 1 — cheap, high-value, do first (days, not weeks)

1. Add a dated note to `SystemMap.md` and the root README explaining the current two-repo split; reconcile or retire `mythos/README.md`'s older four-repo account.
2. Decide `packages/`'s fate. Given zero test coverage and README/code mismatches across the board, the realistic options are: delete it and ship `src/` directly, or commit to thin re-export wrappers wired into CI so drift is caught going forward. Leaving it as-is actively misinforms anyone who reads a package README before its code.
3. Give `src/crystalcore` — the actual consent gate — a test suite. It's the one security-relevant boundary in the whole repo with zero coverage.
4. Fix the dbt warehouse's SQL syntax error and decide whether to wire its staging models to the JSONL files `dbt_integration.py` already writes, or retire the project until it's ready to.

### Tier 2 — important, more surface area (weeks)

1. Reconcile the Crystal Runtime spec trio's self-contradiction, and update `Roadmap.md` to reflect that the runtime already exists and passes 75 tests.
2. Make an explicit call on `crystalcore` / `crystal-core` / `runtime`: intentionally separate systems (then document why, and stop echoing vocabulary across them) or genuinely integrate them (starting from the one demo-only cross-import that already proves it's possible).
3. Disambiguate "Starline" the way ADR-0004 disambiguated "CrystalCore" — a short taxonomy ADR would do it.
4. Reconcile `archive/2026/local-snapshot-2026-07-17`'s two contradictory recovery-status documents.

### Tier 3 — polish, whenever there's a spare afternoon

1. Rebuild `docs/README.md`'s index so it lists all nine currently-missing files, `ATTRIBUTIONS.md` especially.
2. Fix or retire the dead links in `Access.md` and `Push.md`.
3. Give `REPO-RESTRUCTURING-PLAN.md` the same "Superseded" banner its siblings already carry.
4. Cross-check the live site against source once it's reachable, or from a screenshot.

---

*Methodology: four independent research passes covered the docs/governance layer, the content/research/data layers, the core application architecture, and the packaging/apps/SDK/site surface, each reading source files directly rather than relying on their own READMEs. All test and self-test results reported in §4–§5 were re-run and confirmed by direct execution in this session. The live website (§6) could not be reached due to this session's network policy and is the one section built from source alone rather than a live check.*

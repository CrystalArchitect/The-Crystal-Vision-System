# Full Review — 2026-07-28

A review of all eleven repositories currently in the CrystalArchitect
portfolio: what runs, what is defective, and what is inconsistent across
repository boundaries. This report records findings, not fixes — no code
in any repository was changed by it.

**Snapshot:** local clones of all eleven repos, surveyed 2026-07-28.
Every claim below was produced by running something (a test suite, a
hash comparison, a link resolver) or by reading the cited file, not by
inference from documentation. Where a claim is a judgement rather than a
measurement, it says so.

## Evidence tiers

Same scheme as [`REPO-ARCHAEOLOGY-2026-07-24.md`](REPO-ARCHAEOLOGY-2026-07-24.md):

- **Tier A — executed.** A test suite, build, or script was run in this
  session and its output observed. Strongest evidence.
- **Tier B — content-addressed.** SHA-256 over file contents, or exact
  path resolution against `git ls-files`. Mechanical, reproducible.
- **Tier C — read.** A file was read and is quoted or cited. A claim
  about what the code *says*, not about what it does at runtime.

---

## Headline

The engineering core is in better shape than the portfolio around it.
Every test the CI claims to run does in fact run and pass (Tier A, 77/77).
The cryptography is a careful, literal implementation of a published
spec, not invented. The GitHub Actions workflows are clean — no
`pull_request_target`, no untrusted interpolation into `run:` blocks,
explicit `permissions:` on every workflow.

The problems are almost entirely at the seams between repositories:
licensing that contradicts itself across repos, 34% of tracked text
files duplicated across repos with no stated source of truth, and a
knowledge base that documents 6 of the 11 repositories — omitting the 5
that have been most active this week.

| Severity | Count | Area |
|---|---|---|
| High | 1 | Licensing conflict on identical file contents |
| Medium | 6 | Pre-auth DoS surface, key-file permissions, CSRF, dev-server exposure, stale knowledge base, cross-repo duplication |
| Low | 7 | Self-XSS, missing SRI, broken doc links, junk dependency, no-LICENSE repos, CI coverage gaps, empty README |

---

## What was verified to work (Tier A)

Every suite the `TerAustralis-Incognita-Code` CI declares was run
locally on Python 3.11.15. All pass:

| Suite | Result |
|---|---|
| `python -m compileall core vision` | clean, exit 0 |
| `clementine.bridge.selftest` (Starline Weaver) | 7/7 |
| `services.selftest` (pipeline) | 4/4 |
| `rdp.selftest` (record kernel) | 31/31 |
| `consent_transport.selftest` (Starline) | 9/9 |
| `crystalcore.selftest` (CrystalBridge gate) | 7/7 |
| `pytest core/tests` (mesh stub) | 3/3 |
| `pytest vision/apps/lumina/tests` | 16/16 |
| **Total** | **77/77** |

This corroborates this repository's own `STATUS.md` claim of "four
suites, 51/51" for Crystal Core — 7 + 4 + 31 + 9 = 51 exactly, and the
count is still accurate four days later. The maturity ladder in
`STATUS.md` is, on the evidence, honest: things filed under "Running"
run.

---

## High

### H1. The same file contents are published under two incompatible licenses

**Tier B.** SHA-256 over all 887 tracked non-binary files across the
eleven repos finds **91 distinct file contents that exist simultaneously
in a CC-BY-NC-ND-4.0 repository and an Apache-2.0 repository.**

The split:

| License | Repositories |
|---|---|
| CC-BY-NC-ND-4.0 | `TerAustralis-Incognita`, `TerAustralis-Incognita-Code` |
| Apache-2.0 | `crystalcore`, `crystal-vision`, `The-Crystal-Vision` |

Conflicting contents include source code, not just prose — e.g.
`clementine.py`, `crystalcore/expose.py`, `crystalcore/memory.py`,
`crystalcore/__main__.py`, and the `VISION.md` / `MEMORY.md` /
`SPONSORS.md` content documents.

Why this matters: someone who finds `clementine.py` in `The-Crystal-Vision`
reads Apache-2.0 and reasonably concludes they may modify and
redistribute it. The identical bytes in `TerAustralis-Incognita` say
NoDerivatives and NonCommercial. Both statements come from the same
copyright holder, so dual-licensing is entirely permissible — but
nothing anywhere states that it is intentional, so which terms actually
govern is undetermined for any downstream reader.

Second, narrower point: **CC-BY-NC-ND-4.0 is applied to 115 source
files** as an SPDX header (Tier B). Creative Commons explicitly
recommends against using CC licenses for software, and NoDerivatives is
structurally at odds with a repository that accepts pull requests — a
patch is a derivative work.

> **Correction (same day).** An earlier version of this paragraph said
> "Apache-2.0 appears in only 6 SPDX headers by comparison." That was
> wrong, and wrong in a way this report's own evidence tiers should have
> caught: the six occurrences are prose *about* SPDX headers, inside
> `CHANGELOG.md`, `ADR-0009.md`, `04-GOVERNANCE.md`, and
> `11-CORRECTIONS.md` — documents discussing a past batch correction —
> not headers on any source file. **Zero source files carry an
> Apache-2.0 SPDX header.** The original census counted textual
> occurrences and reported them as headers.
>
> This does not affect H1's conclusion, which rests on SHA-256 over file
> *contents* and on the root `LICENSE` files, both of which were measured
> correctly. It does mean the Apache-2.0 side of the conflict lived
> entirely in `LICENSE` files, never in per-file headers — which is why
> `04-GOVERNANCE.md`'s standing claim that "96 files carry
> `SPDX-License-Identifier: Apache-2.0`" is also stale; that batch was
> corrected before this review ran, as `11-CORRECTIONS.md` Part 4 records.

This is the one finding worth resolving before anything else, because
every other repository decision (what to merge where, what to open
source, what to sell under `COMMERCIAL_LICENSE.md`) sits downstream of it.

---

## Medium

### M1. Unbounded, untimed frame reads before authentication

`TerAustralis-Incognita-Code/core/crystal-core/consent_transport/transport.py`

**Tier C.** `protocol.py` defines `MAX_FRAME_LEN = 4 MiB` and enforces it
in `recv_frame()`. `transport.py` carries its own copy of the framing
helpers — `_recv_exact` / `_recv_raw` at lines 27–42 — and that copy
**drops the length check**. Those are the helpers used for the two Noise
handshake messages, i.e. the only ones an unauthenticated peer can reach.

Compounding it, `StarlineServer._handle` spawns a thread per connection
and never sets a timeout on the accepted socket, so a peer that opens a
connection and sends four bytes holds a thread indefinitely. There is no
cap on concurrent connections.

The asymmetry looks accidental — the duplicated code lost the check its
sibling has. Mitigating: the server binds `127.0.0.1` by default and the
module documents that exposing it further is an explicit operator choice.
The fix is to apply `MAX_FRAME_LEN` in `transport.py` too (or import the
one implementation), set `conn.settimeout(...)`, and bound the thread count.

### M2. Identity private keys are written world-readable, then chmodded

`TerAustralis-Incognita-Code/core/crystal-core/consent_transport/identity.py`

**Tier C.** `Identity.save()` calls `path.write_text(...)` and only then
`os.chmod(path, S_IRUSR | S_IWUSR)`. The file is created under the
process umask — typically `0644` — and is world-readable for the window
between the two calls. The docstring states the intent exactly ("owner-read-only
where the platform supports it"); the implementation just gets the order
wrong. Creating with `os.open(path, O_WRONLY|O_CREAT|O_TRUNC, 0o600)`
closes it.

Same function, separate issue: the write is not atomic. Given the
module's own stated stakes — "Losing the key file means losing the
identity — there is no recovery, by design" — a crash or full disk
mid-write destroys an unrecoverable identity. Write to a temporary file
in the same directory and `os.replace()`.

### M3. `POST /api/reflect` is reachable cross-origin

`TerAustralis-Incognita-Code/vision/apps/lumina/server.py`

**Tier C.** The Lumina API is correctly bound to `127.0.0.1` with
`debug=False`, and the CORS handler only reflects `http://127.0.0.1:` and
`http://localhost:` origins — that check is sound (the trailing colon
defeats the usual `127.0.0.1.evil.com` bypass).

But CORS governs *reading responses*, not *causing effects*. Every other
mutating endpoint is incidentally protected because it parses a JSON body
and Flask's `get_json(silent=True)` returns `None` for a form
content-type, so a cross-site form POST turns into a 400. `/api/reflect`
reads no body at all:

```python
@app.post("/api/reflect")
def reflect():
    return jsonify({"insights": holder["c"].reflect()})
```

Any page the user visits can therefore submit a bodyless form POST to
`http://127.0.0.1:5000/api/reflect` and trigger `Lumina.reflect()`, which
(per `crystalcore/companion.py:346–393`) calls the local model and
appends up to three new entries to `memory.reflections`, then `save()`s
them to disk. The attacker cannot read the result; they can still make a
sovereignty-focused local companion write to its own memory unbidden. A
CSRF token, or simply requiring `Content-Type: application/json` on
mutating routes, resolves it.

### M4. The v2 dev server binds to all interfaces with a credentialed proxy attached

`teraustralis-incognita-v2/vite.config.ts`, `package.json`

**Tier C.** `"dev": "vite --host"` plus `server.host: true` binds the Vite
dev server to `0.0.0.0`. Two custom plugins are mounted on it:

- `vitePluginStorageProxy` serves `/manus-storage/*` and forwards requests
  to `BUILT_IN_FORGE_API_URL` **with `Authorization: Bearer $BUILT_IN_FORGE_API_KEY`
  attached server-side**. Anyone who can reach the dev port can use it as
  an authenticated proxy to that storage backend, with the key never
  leaving the machine but its authority fully available.
- `vitePluginManusDebugCollector` accepts `POST /__manus__/logs` from
  anyone and appends the JSON body to files under `.manus-logs/`.

Both are dev-only and both come from the Manus scaffold rather than from
this project. Neither is a defect in production builds. On a shared or
untrusted network during development, both are live. Dropping `--host` /
`host: true` (or binding `127.0.0.1`) is the cheap fix.

Related, same repo: this is visibly an ungroomed generator scaffold —
`template.json`, `client/src/components/ManusDialog.tsx`,
`vite-plugin-manus-runtime`, and `client/public/__manus__/debug-collector.js`
are all tracked, and the last of those ships into the production bundle
because Vite copies `public/` verbatim. `VITE_FRONTEND_FORGE_API_KEY` is
compiled into the client bundle by design (any `VITE_`-prefixed variable
is public), and `client/src/components/Map.tsx` hardcodes
`https://forge.butterfly-effect.dev` as its fallback. For a project whose
stated ethos is local-first sovereignty, a hard runtime dependency on a
third-party vendor's API is worth a deliberate decision rather than an
inherited default.

### M5. The knowledge base documents 6 of 11 repositories

`CrystalCore.OS-the-Crystal-Architecture-Archive/knowledge-base/02-REPOSITORY-MAP.md`

**Tier B.** The repository map names six repos: this archive,
`TerAustralis-Incognita`, `TerAustralis-Incognita-Code`,
`The-Crystal-Vision`, `crystal-vision`, `crystalcore`. Five are absent:

- `CrystalCore.OS`
- `CrystalCore-AERIS`
- `crystalcore-os-aeris-vault12`
- `teraustralis-incognita-v2`
- `teraustralis-v2-presentation`

Four of those five received commits on 2026-07-28 or 2026-07-29 — they
are the *most* active repositories in the portfolio right now, and the
knowledge base does not know they exist. `00-INDEX.md` still opens "from
a full read of the six-repository CrystalArchitect portfolio."

This is ordinary staleness in a fast-moving portfolio, not an error in
the archive's method. But an archive whose stated job is to be the
system ledger is currently missing 45% of the system.

### M6. A third of tracked text files exist in more than one repository

**Tier B.** Of 887 tracked non-binary files, **302 files across 104
distinct content groups appear in two or more repositories**, byte-identical.

Some of this is deliberate and documented — `archive/` in the umbrella is
frozen provenance, and `REPO-ARCHAEOLOGY-2026-07-24.md` already
establishes that `-Code` descends from the umbrella's canon branch. But
the live cases are not obviously intentional: `mythos/content/*.md` is
duplicated between `TerAustralis-Incognita` and `TerAustralis-Incognita-Code`,
and the Seven Sisters corpus (`crystalcore-seven-sisters-*.md`,
`crystalcore-TRANSMIT*`, `WATER-BRIEF.md`, `TRANSMIT-LOG.md`) exists in
three repositories at once.

Nothing declares which copy is canonical, so any edit silently forks the
content. This is also the mechanism that produced H1.

---

## Low

### L1. Self-XSS in the terminal emulators

`CrystalCore.OS/index.html:365,395` and `CrystalCore-AERIS/index.html:528,561`

**Tier C.** User input is interpolated into `innerHTML` unescaped:

```js
out.innerHTML += `crystal@core:~$ ${term.value}<br>`;
...
out.innerHTML += `Command not found: ${cmd}<br><br>`;
```

Typing `<img src=x onerror=...>` executes it. I checked for a delivery
vector — neither page reads `location.hash`, `location.search`,
`URLSearchParams`, or `postMessage` — so this is self-XSS only, on static
pages holding no credentials or state. Impact is close to nil; it is
listed because the fix is one line (`textContent`, or escape before
interpolating) and because `innerHTML +=` in a loop also re-parses the
whole output buffer on every command.

### L2. CDN scripts loaded without Subresource Integrity

**Tier B.** 13 files in `teraustralis-v2-presentation/` and 2 prototypes
in `TerAustralis-Incognita/research/prototypes/story-library/` load:

```html
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1"></script>
```

No `integrity`, no `crossorigin`. `chart.js` is at least version-pinned;
`d3.v7.min.js` is a floating major-version URL, so its contents can
change under the page at any time. Adding SRI hashes, or vendoring both,
removes a live third-party dependency from a presentation deck.

### L3. 62 broken internal links in live documentation

**Tier B.** Resolving every relative Markdown link against `git ls-files`:
895 internal links checked, **92 broken**, of which 62 are outside
`archive/` and `local-snapshot-*` (the frozen trees whose dead links
`.github/workflows/markdown-link-check-config.json` correctly declares to
be historical facts).

This is a *known* gap rather than a missed one — that config deliberately
scopes link checking to `^https?://`, documenting a markdown-link-check
bug with parent-relative links. The contribution here is the number, and
one concrete cluster: **16 broken links under `docs/architecture/crystal-core/`**,
most of which are a single mechanical error — one `../` too few.
Hand-verified examples:

| Link as written | Actual location |
|---|---|
| `ADR-0001.md` | `docs/adr/ADR-0001.md` |
| `../governance/The-Incognita-Rule.md` | `docs/governance/The-Incognita-Rule.md` |
| `../ai/Decision-Matrix.md` | `docs/ai/Decision-Matrix.md` |

Overall, 36 of the 62 have a same-named file elsewhere in their own repo
(so are candidates for a path fix); 26 point at trees that genuinely do
not exist here — largely `src/` and `packages/`, both already tracked as
staged debt in `Migration-Plan.md`.

Resolving links against `git ls-files` rather than by HTTP sidesteps the
tool bug entirely and would let internal links be checked in CI.

### L4. Six repositories have no LICENSE file

**Tier B.** `CrystalCore-AERIS`, `CrystalCore.OS`,
`crystalcore-os-aeris-vault12`, `teraustralis-incognita-v2`,
`teraustralis-v2-presentation`, and this archive repository ship no
license of any kind. Default copyright applies — all rights reserved,
nobody may reuse anything.

`teraustralis-incognita-v2` is the sharpest case: `package.json` declares
`"license": "MIT"` while no MIT text exists in the repository. That is an
unbacked license claim, and it belongs to the same family of problems as H1.

### L5. `"add": "^2.0.6"` is a junk dependency

`teraustralis-incognita-v2/package.json` devDependencies. This is the
artifact of running `npm install add` — a real but unrelated package
that does nothing here. Safe to remove.

Adjacent: `pnpm.patchedDependencies` pins a patch to `wouter@3.7.1` while
`dependencies` declares `wouter: ^3.3.5`. It resolves today via the
lockfile, but pnpm errors when a patch's target version stops matching, so
a future `wouter` bump breaks installs rather than degrading.

### L6. CI coverage gaps

**Tier C.**

- `The-Crystal-Vision` contains a SvelteKit application (`package.json`,
  `svelte.config.js`, `src/`, 14 `.svelte` files) and its CI runs only
  `compileall` over `clementine` and `crystalcore-app`. The JavaScript
  application is never installed, built, type-checked, or tested. Its
  `src/` tree is not even syntax-checked.
- `teraustralis-incognita-v2` has `vitest` in devDependencies, a `check`
  script (`tsc --noEmit`), and **no CI workflow at all** — nothing runs
  either one.
- `teraustralis-incognita-v2` has no script that runs `server/index.ts`
  in development; `dev` starts Vite only and `start` requires a build.

For the record, the branch trigger in `The-Crystal-Vision/.github/workflows/ci.yml`
(`master`) is **correct** — that repo's default branch really is `master`.
It is the only one of the eleven not on `main`, which is worth normalizing
but is not currently breaking anything.

### L7. This repository's README is empty

`CrystalCore.OS-the-Crystal-Architecture-Archive/README.md` is 49 bytes:
the repository name as an H1, no trailing newline, no content. For the
repository that hosts the portfolio's knowledge base and system ledger,
the front door should at minimum point at `knowledge-base/00-INDEX.md`
and `STATUS.md`.

---

## What is notably good

Worth recording, because a review that only lists defects misrepresents
the codebase.

- **The crypto is honest.** `consent_transport/noise.py` is a literal
  implementation of Noise_IK_25519_ChaChaPoly_SHA256 checked against the
  published spec: the HKDF is Noise's two-output construction (§4.3), not
  RFC 5869's; `initialize()` pads-or-hashes the protocol name correctly;
  the ChaChaPoly nonce is 4 zero bytes plus a 64-bit little-endian
  counter as specified; `decrypt_with_ad` does not advance the nonce on
  failure. The IK pre-message and both message patterns are correct for
  both roles. No primitive is home-rolled — X25519, Ed25519,
  ChaCha20-Poly1305 and SHA-256 all come from `cryptography` or the stdlib.
  The decision to write a single-pattern implementation *for auditability*
  is stated in the module docstring and is the right call.
- **`requirements-bridge.txt` pins `mcp>=1.2,<2` with a comment
  explaining that the upper bound is load-bearing** — mcp 2.0 removed
  `mcp.server.fastmcp`, an open range broke CI on unrelated commits, and
  migrating is deliberate work. This is exactly the right way to record a
  version constraint.
- **No secrets anywhere.** A sweep for AWS keys, GitHub tokens, OpenAI
  keys, Slack tokens, Google API keys and PEM private-key blocks across
  all eleven repositories found nothing. The only credential-shaped
  tracked files are four `.env.example` templates.
- **The workflows are clean.** No `pull_request_target`, no
  `${{ github.event.* }}` interpolated into `run:` blocks, and an explicit
  `permissions:` block on all five real workflows.
- **`STATUS.md`'s maturity ladder holds up under testing.** The
  Running/Built/Document/Designed/Concept ledger matched what actually
  ran, including the exact test counts. That discipline is the portfolio's
  most valuable asset and it is being maintained accurately.

---

## Disposition

Every finding above was acted on the same day, across ten pull requests.
This section records what happened to each; the findings themselves are
left as written, so the report stays a snapshot of 2026-07-28 rather than
a moving document.

| # | Fixed in | Note |
|---|---|---|
| H1 | `TerAustralis-Incognita` (ADR-0013) + `crystalcore`, `crystal-vision`, `The-Crystal-Vision`, and six licence-less repos | Maintainer chose uniform CC BY-NC-ND 4.0 portfolio-wide. All eleven now carry byte-identical licence text. |
| M1 | `TerAustralis-Incognita-Code` | Handshake frames capped, socket timeout, bounded connections that refuse rather than queue. |
| M2 | `TerAustralis-Incognita-Code` | Key file created `0600`; write made atomic. |
| M3 | `TerAustralis-Incognita-Code` | Mutating routes require `application/json`, stated once in `before_request`. |
| M4 | `teraustralis-incognita-v2` | Dev server defaults to `127.0.0.1`; `DEV_HOST` is the explicit opt-in. |
| M5 | this repository | Knowledge base extended to eleven repositories, by accretion. |
| M6 | **not fixed** | 302 duplicated files remain. Deduplication is its own decision; ADR-0013 records it as open. |
| L1 | `CrystalCore.OS`, `CrystalCore-AERIS` | Input escaped before echo; verified in Chromium before and after. |
| L2 | `teraustralis-v2-presentation`, `TerAustralis-Incognita` | Unused CDN tags removed from the deck; d3 vendored for the prototypes that do use it. |
| L3 | `TerAustralis-Incognita` | 62 → 0. Checker added to CI that resolves against `git ls-files`. |
| L4 | six repositories | Licence added; `teraustralis-incognita-v2`'s unbacked MIT claim corrected. |
| L5 | `teraustralis-incognita-v2` | Junk `add` dependency removed. |
| L6 | `The-Crystal-Vision`, `teraustralis-incognita-v2` | Both JavaScript applications now build and type-check in CI. |
| L7 | this repository | README written. |

One finding was added during the fixing pass and is not in the list
above, because the review missed it: `TerAustralis-Incognita-Code` had
**Apache-2.0 sub-licences nested inside a CC BY-NC-ND repository**
(`core/crystal-core/LICENSE`, `vision/apps/crystal-interface/LICENSE`),
so 36 source files asserted CC BY-NC-ND in their own SPDX headers while
the `LICENSE` beside them asserted Apache-2.0. It is H1 in miniature,
inside one repository, and the original sweep did not catch it because
that sweep compared licences *between* repositories. Fixed under
ADR-0013; recorded here so the miss is on the record too.

## Suggested order of work

1. **H1** — decide the licensing story and make it consistent. Everything
   about what can be shared, merged, or sold depends on it, and M6 keeps
   regenerating the conflict until the duplication is resolved too.
2. **M1, M2, M3** — three small, local, well-understood fixes in code
   that is already tested; each is a few lines plus a regression test.
3. **M4, L5** — groom the v2 scaffold and stop binding the dev server to
   `0.0.0.0`.
4. **M5, L7** — bring the knowledge base up to eleven repositories and
   give this repo a real README.
5. **L3, L6** — check internal links against `git ls-files` in CI, and
   put the JavaScript applications under CI at all.
6. **L1, L2, L4** — one-line hardening and the missing license files.

---

*Non Solus.*

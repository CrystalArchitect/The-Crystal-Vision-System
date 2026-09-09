# Build pipeline

The scripts that generated everything under `vision-plates/`,
`asset-packs/crystalwood/` and `campaigns/used-memory/`.

Committed so a later pass does not have to reinvent them. They were written
against images in a session scratchpad, so **paths need repointing** before
reuse — see *Repointing* below.

## Layout

| File | What it does |
|---|---|
| `plates.py` | Volume I catalogue — sections, per-plate title, origin, marks, reading |
| `build.py` | Renders Volume I. Holds the shared CSS both volumes use |
| `plates2.py` | Volume II catalogue, plus `HELD_OUT` and a `verify()` integrity check |
| `build2.py` | Renders Volume II. Imports `CSS` from `build.py` |
| `plates3.py` | Volume III catalogue, plus `SURVEYED` and a runnable `verify()` |
| `build3.py` | Renders Volume III. Imports `CSS` from `build.py`, `EXTRA_CSS` from `build2.py` |
| `fonts.py` | Writes `fonts.css` / `fonts-linked.css`. **Run first** — the builders open one of them at import time |
| `resize.py` | Cuts the archival and web JPEGs and writes a manifest |
| `build_crystalwood.py` | Asset-pack production sheet |
| `build_used_memory.py` | Fictional film campaign sheet |
| `build_clementine_ui.py` | Clementine UI direction sheet |
| `manifest*.json` | Per-slug native size and web dimensions, written by `resize.py` |

Nothing in this directory is generated-and-committed: `fonts*.css`, the
`archive*/` and `web*/` JPEG trees and the `*-linked.html` output are all build
products and all git-ignored. The committed galleries are the copies under
`../` and `../volume-2/`.

## Two output modes

Every builder reads a `MODE` environment variable:

- `MODE=inline` — one self-contained file, images and fonts as `data:` URIs.
  Used for the shareable artifact; the CSP on that host blocks external
  requests, so nothing may be linked.
- `MODE=linked` — relative paths (`plates/x.jpg`, `fonts/x.woff2`) and a full
  `<!DOCTYPE html>` wrapper. This is what is committed here, so the galleries
  open from a clone with no build step and no network.

```bash
MODE=inline python3 build2.py "11 August 2026"   # -> plate-archive-vol2.html
MODE=linked python3 build2.py "11 August 2026"   # -> index2-linked.html
```

## Reproducing the committed galleries

Verified from a clean clone on 11 August 2026 — both linked builds come out
**byte-identical** to the files committed under `../` and `../volume-2/`:

```bash
pip install Pillow

python3 fonts.py --prefix ../fonts/
MODE=linked python3 build2.py "11 August 2026"
diff index2-linked.html ../volume-2/index.html          # identical

python3 fonts.py --prefix fonts/
ln -s ../plates archive                                 # build.py measures the archival files
MODE=linked python3 build.py "11 August 2026"
diff index-linked.html ../index.html                    # identical
```

Two things to know before repeating this. The `--prefix` is the only per-volume
difference in the font CSS: Volume I sits beside `fonts/`, anything in a
subdirectory reaches `../fonts/`. And `build.py` — unlike `build2.py`, which
takes its dimensions from the manifest — measures the image files themselves, so
its `WEB` directory (`archive` in linked mode) has to point at real JPEGs.

**Pass the date.** Both builders default to `"August 2026"`, which does not match
what is committed; the galleries were assembled with `"11 August 2026"`.

## Steps that were run inline, not saved as scripts

Two of the three are now scripts. The pipeline could not run from a checkout
without them — `build.py` and `build2.py` both open a font CSS file at *import*
time, so a clean clone failed at the import line before doing any work.

**1. Fonts — now `fonts.py`.** Reads the four Latin-subset WOFF2 files already
vendored in `../fonts/` and emits `fonts.css` (base64 data URIs) and
`fonts-linked.css` (relative paths). No network call. The original heredoc
fetched them from Google Fonts with a full Chrome UA (a bare UA returns TTF with
no subset comments), kept only the `latin` blocks and deduped by content hash —
several families are variable fonts served as one file for multiple weights.
That fetch is what produced the vendored files; it only needs repeating if a
family changes.

**2. Resize — now `resize.py`.** For each slug in a catalogue module, writes two
copies: an archival JPEG (long edge capped at 2400 px, quality 88) committed to
the repo, and a web JPEG (long edge 1000 px for Volume II, 1320 px for Volume I,
quality 76) embedded in the inline build. Nothing is upscaled. Records native
size and web dimensions into `manifest*.json` — the builders read `web` for
`width`/`height` attributes and `native` for the plate rail.

```bash
python3 resize.py --catalogue plates3 --src /path/to/uploads \
    --archive archive3 --web web3 --manifest manifest3.json
```

Checked by round-tripping the 66 committed Volume II plates back through it:
all 66 manifest entries come out identical to `manifest2.json`. That check is
also what pinned the rounding — half-edges round **up**, not to even, because a
1792×1008 source at the 1000 px cap lands on exactly 562.5 and every existing
plate at that ratio records 563.

**3. Video — still a heredoc.** `imageio-ffmpeg` supplies an ffmpeg binary via
pip. Volume I's clip went 5.3 MB → 251 KB at `-crf 30 -preset slow`, scaled to
960 wide, plus a poster frame. Only one plate in either volume is a video; this
was not worth scripting until a second one exists.

## Repointing for a new volume

1. Put the source images somewhere and note the path — `resize.py --src` takes
   it as an argument now, so there is no `SRC` constant to edit.
2. Write the catalogue module (copy `plates2.py`); each entry needs `src`,
   `title`, `sub`, `origin`, `marks` and one or more `reading` paragraphs.
3. Run `verify()` **before** building. It fails on missing files, two plates
   sharing a source, plates defined but not listed in a section, and plates
   listed but never defined. All four were real mistakes during Volume II;
   the check is what caught them.
4. `python3 fonts.py --prefix ../fonts/`, then `resize.py`, then build both modes.
5. Check in a headless browser: every image loads, fonts apply, no horizontal
   overflow at 1280 px and 390 px, and both themes resolve.

`build3.py` shows what that looks like in practice. It is `build2.py` with the
three Volume-II-specific hard-codings moved: the `SURVEYED` slugs now live in
`plates3.SURVEYED` instead of being written out twice (in `rail()` and again in
`plate_html()`), the tally counts derive from the catalogue, and there is no
held-out block. `build2.py` was deliberately left alone so Volume II keeps
reproducing byte-identically; a fourth volume should copy `build3.py`, not
`build2.py`.

`plates3.py` is runnable — `python3 plates3.py <src-dir>` prints the `verify()`
result and exits non-zero on any failure, so it can go in front of a build
without a wrapper. It adds a fifth check to Volume II's four: every slug in
`SURVEYED` must actually be a plate, or a silver stamp gets promised to nothing.

### A bug this turned up, and the fix

The `.stamp` text colour was a theme token while its background was hard-coded
`rgba(11,10,18,.72)`. In the **light** theme that put `--silver` (`#3d3a4d`) on
near-black: measured **1.83:1**, failing WCAG at any text size. It went
unnoticed through two volumes because no surveyed plate in them sits on a dark
image; Volume III's `music-theory-tree` does, which is what surfaced it.

Fixed in `build.py`'s shared CSS with a `--stamp-bg` token defined in all three
theme blocks, so every volume inherits it. Measured over a black image:

| | light | dark |
|---|---|---|
| `SURVEYED` | 1.83:1 → **7.94:1** | 12.14:1 (unchanged) |
| `DREAMED` | 3.26:1 → **4.44:1** | 5.20:1 (unchanged) |

Because the CSS is shared, this regenerated all three committed galleries. The
diff against the previous `index.html` and `volume-2/index.html` is only those
four CSS lines — no markup, content or plate changed.

### One non-bug worth not re-investigating

A headless check of Volume I reports a failed request for
`plates/job-accepted.mp4` (`net::ERR_ABORTED`), and forcing a load times out.
The file is fine: it serves HTTP 200 at 1,749,701 bytes with a valid `ftyp`
`isom` box and `avc1`/`avcC`/`mp4a` tracks. The container's Chromium is the
open-source build, which returns `""` from
`canPlayType('video/mp4; codecs="avc1.42E01E"')` — it has no H.264 decoder.
Real browsers play the plate normally.

## Conventions worth preserving

- **Every plate carries a belt.** Volume I is Vision throughout. Volume II adds
  `Science — checkable` with a silver `SURVEYED` stamp for the five plates that
  survive checking; everything else keeps the ochre `DREAMED` stamp.
- **`MARKS` is per-plate, not a footer.** Naming the third-party trademarks on
  the plate itself is the Incognita Rule applied to imagery.
- **Sections carry an optional `flag`** rendering an ochre panel — used where
  material sits in tension with the project's own governance rather than
  smoothing it over.
- **Colour comes from the project's own tokens** in the root `index.html`
  (ink `#0b0a12`, gold `#d4b56a`, violet `#7b6cff`, silver `#c5c9d6`), extended
  with one iron-oxide accent reserved for honesty markers only.
- **Held-out material is listed, never rendered.** `plates2.HELD_OUT` carries
  descriptions only; those files were never copied into the repository.

## Still uncatalogued

Roughly 160 images from later batches were never processed. Notable threads:
the civic noticeboard (the lattice as precinct walks rather than cosmic
architecture), the bleached-coral plate against `WATER-BRIEF.md`, the AERIS
identity work, and the Consent Transport Protocol diagram — whose Noise XX /
X25519 / ChaChaPoly / Ed25519 stack is real, coherent cryptography and the
closest thing in the collection to something buildable.

Still awaiting a decision, and deliberately absent from this repository: seven
Country maps naming real communities and Cave Hill / Walinynga, one personal
photograph, and a batch addressed to a named individual. See the exclusions
section of `../README.md`.

---

**All rights reserved.** TerAustralis Incognita — ABN 70 741 068 059.

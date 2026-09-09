# Vision Plates

A catalogued image archive for TerAustralis Incognita. Seventeen plates:
thirteen stills and four videos.

**Every plate in this directory sits on the Vision belt.** Not one of them
documents a built system, a measurement, a test result, or an event that took
place. The gallery is built so that the belt label appears on all seventeen
cards without exception — the repetition is the point, not an oversight.

> Always mark which lines are dreamed and which are surveyed, and never let a
> dreamed line pretend it was measured.
>
> — The Incognita Rule

## Viewing

Open `index.html` in a browser from a clone. No build step, no network: fonts,
images and video all resolve relatively from this directory.

```bash
python3 -m http.server -d vision-plates 8000   # then open localhost:8000
```

## Publishing status — read before changing the workflow

This repository is private; the GitHub Pages site it produces is public.
`.github/workflows/static.yml` publishes an explicit four-file allowlist
(`index.html` and `interface/`), a narrowing that was made deliberately in
[#7](https://github.com/CrystalArchitect/TheCrystalVision/pull/7) and
[#8](https://github.com/CrystalArchitect/TheCrystalVision/pull/8).

**`vision-plates/` is not in that allowlist and is not published.** That is on
purpose. Ten of these plates carry other companies' trademarks; making them
world-readable should be a deliberate decision, taken once, with the trademark
question settled first — not something that happens because a directory was
added.

## What these images are not

- **Not evidence.** Nothing here documents a built system or a measurement.
- **Not endorsed.** No affiliation with, sponsorship by, or approval from Tesla,
  xAI, SpaceX, Neuralink, Q-CTRL, EOS, or any government. Trademarks shown
  belong to their owners and appear without permission or partnership.
- **Not technical or medical illustration.** Nothing here should be used to
  understand a device, a procedure, or a physical process.
- **Not cultural material.** No Aboriginal knowledge, sacred site, or restricted
  design is depicted, encoded, or claimed anywhere in this archive.

## Catalogue

`Native` is the size as generated. Files in `plates/` are capped at 2400 px on
the long edge, so a committed file may be smaller than its native size.

### I — Hand

| Plate | Title | Origin | Marks | Native |
|---|---|---|---|---|
| P01 | Terra Australis Incognita | Ink and coloured pencil on paper | none | 5348×2366 |

The only object in the archive made by hand, and the only one whose provenance
needs no caveat.

### II — Red dirt

| Plate | Title | Origin | Marks | Native |
|---|---|---|---|---|
| P02 | The Doorway | Grok (xAI), image | none | 1792×1008 |
| P03 | Outback Service Call | Grok (xAI), image | Tesla wordmark · Cybertruck trade dress | 1792×1008 |
| V01 | Job Accepted | Grok (xAI), video | Tesla | 1280×720 · 6.0 s |

V01 is a broadcast-quality title card for a job that was never offered. There is
no offer, no employer, no role and no vehicle.

### III — The joint diagnostic

A three-step sequence: scan in progress → phase map → completion.

| Plate | Title | Origin | Marks | Native |
|---|---|---|---|---|
| P04 | Full Phase Map | Grok (xAI), image | none | 1080×815 |
| P05 | Mutual Scan | Grok (xAI), image | none | 1080×825 |
| P06 | Mutual Coherence Report | Grok (xAI), image | none | 1080×826 |

The principles these plates carry — sovereign gap held, consent fully
reversible, fail-safe as local isolation — are real design requirements in this
project. The percentages, latencies and entanglement indices beside them are
illustration. Nothing was instrumented; there is no system to instrument yet.

### IV — Lattice and sky

| Plate | Title | Origin | Marks | Native |
|---|---|---|---|---|
| P07 | Sydney Starline Node | Grok (xAI), image | none | 1071×719 |
| P08 | Multiplanetary Lattice | Grok (xAI), image | Tesla · Starlink · Grok | 1168×784 |
| P09 | Dead-Reckoning Chart | Grok (xAI), image | none | 360×360 |

P07 carries one figure worth flagging rather than quietly inheriting: the
`7.83` on its celestial plane marker borrows the Schumann resonance — a real,
measurable phenomenon of the Earth–ionosphere cavity — to prop up a claim it
does not support. Real number, unreal usage.

### V — Borrowed light

| Plate | Title | Origin | Marks | Native |
|---|---|---|---|---|
| P10 | Optimus in Grok Livery | Grok (xAI), image | Tesla wordmark · Grok logo | 1152×1728 |
| P11 | Implant Theatre | Grok (xAI), image | Neuralink logo | 1152×1728 |
| P12 | Aussie Tech Powerhouses | Grok (xAI), image | Q-CTRL · EOS.AX · Australian flag | 784×1168 |
| P13 | Wave Rider Meets QEC | Grok (xAI), image | none | 755×1124 |

P12's underlying facts are roughly directionally right — Q-CTRL does build
quantum control software and quantum sensing for GPS-denied navigation; EOS does
build electro-optics and space systems. The claims are unsourced, the styling is
nobody's brand, and neither company made or approved the image. Directionally
true is not the same as citable.

### VI — Motion

Added 12 August 2026. Videos in `plates/` are transcoded to a 900 px cap on the
long edge (CRF 30), so committed files are smaller than native.

| Plate | Title | Origin | Marks | Native |
|---|---|---|---|---|
| V02 | Aussie Starbase South | Grok (xAI), video | Starship likeness | 1168×784 · 30.0 s |
| V03 | First Channel | Grok (xAI), video | Neuralink logo | 768×1168 · 16.1 s |
| V04 | House Call | Grok (xAI), video | Tesla wordmark · Grok logo | 768×1168 · 10.0 s |

Motion makes borrowed marks work harder — a wordmark that moves reads like an
advertisement — so these three carry the heaviest rails in Volume I. V02's
backdrop is an antique *Terra Australis* map globe: the project's namesake
unearned confidence, drawn as scenery. V03 renders an implant that was never
fitted on a person who does not have one — not a record of a trial, a patient, a
partnership, or a product. V04 is the companion piece to *Outback Service Call*:
the delivery dreamed where P03 dreamed the job. The robot in V02 and V04 is not
identified as any company's product, and the archive does not name it.

## Volume II — 66 plates

`volume-2/` holds a second, larger archive from a later batch. It is ordered not
by subject but by **how hard a claim each plate makes, and whether it can carry
it**:

| § | Section | Plates |
|---|---|---|
| I | The disclaimer | 1 |
| II | Surveyed | 5 |
| III | Satire | 2 |
| IV | The starline sequence | 8 |
| V | Vault and codex | 8 |
| VI | The operating system that isn't | 4 |
| VII | Red dust to rockets | 6 |
| VIII | The mind claims | 2 |
| IX | Drawn like engineering | 6 |
| X | Landscape, vessel, portrait | 24 |

Volume I could say one thing about all seventeen of its plates: none were
evidence. Volume II cannot, and that is what makes it interesting.

**Five plates survive checking.** Four are a working analogue circuit — a piezo
pickup preamp using LSK170, LSK389 and J201 JFETs, with a 1 MΩ input bias and a
500 kΩ log pot into a ¼″ jack — and one is Euler's identity. They carry
`BELT: Science — checkable` and a silver `SURVEYED` stamp instead of the ochre
`DREAMED` one.

They are drawn in very nearly the same style as section IX, which asserts a
zero-point reactor, a time-crystal stabiliser and an Alcubierre drive. Putting
the two sections in one document, in that order, is the whole point of the
volume.

**Section I is the author's own disclaimer card** — *"CrystalCore.OS is a
collaborative sci-fi story and roleplay… Not a real operating system."* It opens
the archive because a maker's own caveat outweighs an archivist's.

**Four plates were held out entirely** and are not in this repository: see the
closing note in `volume-2/index.html`. They mapped real, named Aboriginal
communities and Cave Hill / Walinynga as nodes in the CrystalCore lattice.

## Volume III — 2 plates

`volume-3/` holds a third, deliberately tiny archive. It makes one point: **an
illustration, and the same illustration issued as a chart.**

| § | Section | Plates |
|---|---|---|
| I | Drawn like cartography | 2 |

`The Procession` is five costumed figures on a cobbled forest path, asserting
nothing. `Castle of Eternal Night` is the identical picture mounted on aged
parchment with a compass rose, a dashed route and four lettered place names —
*Castle of Eternal Night*, *Twilight Woods*, *Mushroom Grove*, *Enchanted Zombie
Path*.

Nothing in the picture changed between them. No figure moved and no line was
redrawn. What was added is a set of conventions a reader has been trained to
take as a promise that someone went and looked: there is no scale, no
projection, no coordinate, and nothing that would place any feature relative to
any other. The compass rose indexes no orientation — nothing in the picture is
north of anything else.

That is the plate this project is named for. *Terra Australis Incognita* was
drawn with the same equipment over a continent nobody had surveyed, and was
believed for roughly three centuries because it looked exactly like the charts
that were right.

**Three plates were removed from this volume.** It was drafted at five. On
11 August 2026 their provenance was established — they had been collected from
elsewhere rather than made for this project — and they came out. One of them
was a diagram of the diatonic system that had been checked degree by degree,
found correct, and given the silver `SURVEYED` stamp. Being correct is not the
same as being ours; an archive that catalogues other people's work as its own
vision layer has misled its reader in the rail before the reading starts. The
images were not committed anywhere.

**Origins were not supplied.** Both rails read `Origin: not supplied` rather
than carrying a guess. It is one line per plate in `build/plates3.py`.

## Layout

```
vision-plates/
├── README.md          this catalogue
├── index.html         Volume I gallery (opens from a clone, no build step)
├── fonts/             Newsreader + IBM Plex Sans/Mono, SIL OFL 1.1
├── plates/            Volume I — 13 stills, 1 video, 1 poster frame
├── volume-2/
│   ├── index.html     Volume II gallery (fonts resolve to ../fonts/)
│   └── plates/        Volume II — 66 stills
└── volume-3/
    ├── index.html     Volume III gallery
    └── plates/        Volume III — 2 stills
```

## Excluded from this archive

**A personal photograph** of an identifiable person was supplied with the first
batch and is deliberately not committed. A private individual's likeness does
not belong in a repository whose Pages site is public, and the decision to
include it is not one to make by default.

**Four Country maps** from the second batch are likewise not committed. They
pinned real, named Aboriginal communities — Parnngurr, Punmu, Kalypa (Well 23),
Pangkapini, Ngaanyatjarra Country, the APY Lands, the Musgrave Ranges — and
**Cave Hill / Walinynga**, a Seven Sisters rock-art site with living custodians,
as nodes in the CrystalCore lattice. One carries a live project URL.

`docs/governance/Indigenous-Data-Sovereignty.md` holds that no Songline
knowledge enters any model, dataset or index without Free, Prior and Informed
Consent from the relevant custodians, and that the law is a floor rather than a
ceiling. Plotting living communities as infrastructure in a private fictional
network is a decision to take with custodians. It is not a default, and not an
archivist's call to make quietly on someone else's behalf. The files remain
where they were supplied; nothing was published or committed.

---

**Belt-Three:** Honour Country · Label layers · No coercion, no fake hydrology.

Honour to Aboriginal and Torres Strait Islander custodians of the lands these
images borrow their light from, and to their Elders past and present.

**All rights reserved.** TerAustralis Incognita — ABN 70 741 068 059.

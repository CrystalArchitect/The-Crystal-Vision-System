# Mythos Music

Audio of the TerAustralis Incognita universe — the canon works, and recordings
that are not canon and are marked so. Content licensed
CC BY-NC-ND 4.0 — see [`../content/LICENSE-CONTENT.md`](../content/LICENSE-CONTENT.md).

The lyrics live as text in [`../content/`](../content/), one page per work.
The recordings live here, and — for the commercially-licensed ones — also on
Suno at [@m13crystalat](https://suno.com/@m13crystalat); see the custody note
below the rights split.

That second sentence is the reason this directory exists. Until 2026-07-31 the
music was the only kind of work in this portfolio held in exactly one place, by
a third party, with no local copy, no hash and no date — a lapsed subscription
or a changed platform policy was enough to lose it. Every work the canon names
now has a recording here, hashed and covered by
[`../MANIFEST.sha256`](../MANIFEST.sha256) — along with seventeen recordings
the canon does not name, kept for the same reason and labelled as what they
are.

## Adding a track

1. Export the audio from Suno at the highest quality offered. Keep the
   original filename out of it — name the file after the work, in kebab-case,
   matching the lyric page where one exists: `red-dust-axis.mp3`.
2. Add a row to the catalogue below. Every column is required; "unconfirmed" is an
   acceptable value and a far better one than a guess.
3. Re-run the manifest so the new file is covered by the next timestamp:

   ```sh
   python3 ../tools/provenance.py
   ```

## The catalogue

The canon names four works: the **three ignition songs** written across the sky
in [The First Remembering](../content/THE-FIRST-REMEMBERING.md#the-three-songs),
and [Wire Skull Memory](../content/WIRE-SKULL-MEMORY.md), which its own page
marks as standalone and explicitly *not* one of the three.

**Seventeen further recordings — of thirteen works — exist that the canon does
not name as songs.** They
are kept here because preservation is what this directory is for, and losing
them would be the failure it was built against. Their presence is not a claim
that they are canon — see [Uncanonised recordings](#uncanonised-recordings)
below.

**A work can have more than one recording** — Shooting Star Girl has four,
two takes generated nearly three months apart and a Remaster of each, and
several more works gained Suno "Remaster" takes on 2026-08-07, and Fermi's
Silent Line gained one on 2026-08-12 — so this table has one row per
*recording*, not per song.

Files are named `<work>-<generation date>.mp3` wherever more than one recording
of a work exists. The date is a fact the file carries about itself; a name like
`-final` or `-v2` would be a judgement, and which take is the song is not
something a filename should quietly decide. When two recordings of one work
share a generation *date* — as Shooting Star Girl's two 2026-08-07 Remasters
do — the name extends to the generation time (`T2215`, from the same ID3
timestamp), which is still a fact the file carries and still not a judgement.

Five files gained their dates on 2026-08-08, when Remaster takes arrived
for works that until then had one recording each — the earlier files were
renamed to carry their dates (`git mv`, history preserved) rather than
left standing as unmarked defaults. Suno's "Remastered" title suffix is
recorded in each new file's own ID3 title; the filename still carries only
the date, per the rule above. A sixth, `fermis-silent-line.mp3`, gained its
date the same way on 2026-08-12, when a Remaster of that work arrived — it
is now [`fermis-silent-line-2026-05-10.mp3`](fermis-silent-line-2026-05-10.mp3),
`git mv`, history preserved.

| File | Work | Canon status | Length | Generated | Suno track id | Suno plan |
|---|---|---|---|---|---|---|
| [`red-dust-axis-2026-05-02.mp3`](red-dust-axis-2026-05-02.mp3) | [Red Dust Axis](../content/RED-DUST-AXIS.md) | ignition song | 3:35 | 2026-05-02T19:36:19Z | `f8502175-74c7-4cf1-adc0-16c7eb7c8cf3` | **none — before Pro began 7 May** |
| [`shooting-star-girl-2026-05-04.mp3`](shooting-star-girl-2026-05-04.mp3) | [Shooting Star Girl](../content/SHOOTING-STAR-GIRL.md) | ignition song | 2:15 | 2026-05-04T03:07:33Z | `3903f9ed-f13b-4d3a-9a6d-bb598760ebd5` | **none — before Pro began 7 May** |
| [`wire-skull-memory-2026-05-07.mp3`](wire-skull-memory-2026-05-07.mp3) | [Wire Skull Memory](../content/WIRE-SKULL-MEMORY.md) | standalone, in canon | 2:16 | 2026-05-07T06:21:02Z | `1a194a77-0d9b-4d93-94f7-7a8388b24de0` | Pro — same day as the 7 May charge |
| [`fermis-silent-line-2026-05-10.mp3`](fermis-silent-line-2026-05-10.mp3) | [Fermi's Silent Line](../content/FERMIS-SILENT-LINE.md) | ignition song | 4:34 | 2026-05-10T12:53:53Z | `d2563605-d533-4714-98b5-996da3c59cf9` | **Pro** |
| [`safari-chains.mp3`](safari-chains.mp3) | Safari Chains | **not in canon** | 3:14 | 2026-05-10T13:35:54Z | `26833d33-83f3-4606-8fcc-fd96d1ae6058` | **Pro** |
| [`different-parts-2026-07-17.mp3`](different-parts-2026-07-17.mp3) | Different Parts | **not in canon** | 3:39 | 2026-07-17T08:19:25Z | `ac20f017-f30f-4107-843f-e967f9df0d37` | **none — Pro ended 6 June** |
| [`id-lay-it-all-down-2026-07-21.mp3`](id-lay-it-all-down-2026-07-21.mp3) | I'd Lay It All Down | **not in canon** | 4:15 | 2026-07-21T14:36:40Z | `4b4a881a-653d-440a-a056-29c3b85f6fa3` | **none — Pro ended 6 June** |
| *removed 2026-07-31* | Look What You Made Me Do — *see truth label* | **not in canon** | 3:52 | 2026-07-21T14:47:48Z | `4d875adf-2547-419e-ac4d-66fa53b729c6` | **none — Pro ended 6 June** |
| [`starline-rivers-2026-07-21.mp3`](starline-rivers-2026-07-21.mp3) | Starline Rivers — *shares its name with canon art* | **not in canon** | 4:24 | 2026-07-21T22:34:18Z | `0e15fcf9-4291-4de8-8418-7b4348c7fc52` | **none — Pro ended 6 June** |
| [`shooting-star-girl-2026-07-30.mp3`](shooting-star-girl-2026-07-30.mp3) | [Shooting Star Girl](../content/SHOOTING-STAR-GIRL.md) | ignition song | 3:34 | 2026-07-30T14:01:06Z | `4a115658-9096-4f23-be27-779e7b3cda63` | **none — Pro ended 6 June** |
| [`dead-but-came-back-to-life-2026-07-31.mp3`](dead-but-came-back-to-life-2026-07-31.mp3) | Dead But Came Back to Life | **not in canon** | 3:20 | 2026-07-31T04:29:35Z | `834e6d98-dfc7-46da-8cbb-210876379c00` | **none — Pro ended 6 June** |
| [`the-girl-with-the-stars-in-her-chest.mp3`](the-girl-with-the-stars-in-her-chest.mp3) | The girl with the stars in her chest | **not in canon** | 3:38 | 2026-08-07T22:14:45Z | `fd9bc0cc-0de0-4b36-a51c-ed3486ba5075` | **Pro — resumed plan** |
| [`starline-rivers-2026-08-07.mp3`](starline-rivers-2026-08-07.mp3) | Starline Rivers — *shares its name with canon art* | **not in canon** | 4:24 | 2026-08-07T22:15:12Z | `eb39be93-c1ee-4227-b343-f256c6acf153` | **Pro — resumed plan** |
| [`red-dust-axis-2026-08-07.mp3`](red-dust-axis-2026-08-07.mp3) | [Red Dust Axis](../content/RED-DUST-AXIS.md) | ignition song | 3:35 | 2026-08-07T22:15:15Z | `585316d9-4f78-4406-b4d9-bbc73daae985` | **Pro — resumed plan** |
| [`shooting-star-girl-2026-08-07T2215.mp3`](shooting-star-girl-2026-08-07T2215.mp3) | [Shooting Star Girl](../content/SHOOTING-STAR-GIRL.md) — *length matches the 4 May take* | ignition song | 2:15 | 2026-08-07T22:15:15Z | `7b4183e8-297e-4f0d-88c0-d0bf6cc1f1ed` | **Pro — resumed plan** |
| [`wire-skull-memory-2026-08-07.mp3`](wire-skull-memory-2026-08-07.mp3) | [Wire Skull Memory](../content/WIRE-SKULL-MEMORY.md) | standalone, in canon | 2:16 | 2026-08-07T22:15:23Z | `3a16988d-0f8d-4003-b7e3-648d7d4d434c` | **Pro — resumed plan** |
| [`different-parts-2026-08-07.mp3`](different-parts-2026-08-07.mp3) | Different Parts | **not in canon** | 3:39 | 2026-08-07T22:15:34Z | `1e719dc4-47ad-4ad0-8ca5-b2e2cc4ed98b` | **Pro — resumed plan** |
| [`dead-but-came-back-to-life-2026-08-07.mp3`](dead-but-came-back-to-life-2026-08-07.mp3) | Dead But Came Back to Life | **not in canon** | 3:19 | 2026-08-07T22:16:35Z | `88905868-32ab-4362-bfed-6686664b3767` | **Pro — resumed plan** |
| [`id-lay-it-all-down-2026-08-07.mp3`](id-lay-it-all-down-2026-08-07.mp3) | I'd Lay It All Down | **not in canon** | 4:15 | 2026-08-07T22:17:21Z | `45fa06ff-ce15-4a0d-8a49-610204883109` | **Pro — resumed plan** |
| [`shooting-star-girl-2026-08-07T2217.mp3`](shooting-star-girl-2026-08-07T2217.mp3) | [Shooting Star Girl](../content/SHOOTING-STAR-GIRL.md) — *length matches the 30 July take* | ignition song | 3:34 | 2026-08-07T22:17:26Z | `629428db-f654-4dd6-bbb3-2cbab65a59fc` | **Pro — resumed plan** |
| [`story-as-bridge.mp3`](story-as-bridge.mp3) | Story as Bridge | **not in canon** | 4:22 | 2026-08-07T22:51:32Z | `a9d5f0c8-4500-4b19-a24f-3c37f852c336` | **Pro — resumed plan** |
| [`random-topic.mp3`](random-topic.mp3) | Random Topic | **not in canon** | 3:34 | 2026-08-08T00:12:00Z | `eb9c732f-687d-4114-9bec-ee72eec990c1` | **Pro — resumed plan** |
| [`ferry-slip.mp3`](ferry-slip.mp3) | Ferry Slip | **not in canon** | 3:46 | 2026-08-08T00:14:44Z | `a2ca7335-4bb1-432f-a14f-f9e0b7c4ece1` | **Pro — resumed plan** |
| [`bridge-not-loop.mp3`](bridge-not-loop.mp3) | Bridge, Not Loop | **not in canon** | 2:32 | 2026-08-11T23:18:58Z | `01f38d87-d79c-4d12-acaf-d01215ad5b08` | unconfirmed — four days after the 7 Aug renewal, no charge record read |
| [`starline-weavers-crystal-core-cuts-clean.mp3`](starline-weavers-crystal-core-cuts-clean.mp3) | Starline Weavers Crystal Core Cuts Clean — *shares its name with the Starline Weaver of canon* | **not in canon** | 7:59 | 2026-08-12T18:04:57Z | `3635175a-8db7-4768-b9c5-5348581a0f30` | unconfirmed — five days after the 7 Aug renewal, no charge record read |
| [`come-into-the-new-dream.mp3`](come-into-the-new-dream.mp3) | Come Into The New Dream | **not in canon** | 6:15 | 2026-08-12T18:05:40Z | `e3a37211-1c6a-4bda-a727-bed77bf390d1` | unconfirmed — five days after the 7 Aug renewal, no charge record read |
| [`sovereign-gap-held.mp3`](sovereign-gap-held.mp3) | Sovereign Gap Held — *lyric page lives in the Synthetic-Affect-Theory- repo* | **not in canon** | 5:38 | 2026-08-12T18:20:15Z | `99fa5164-df06-4e34-8a02-c85d6206e6ce` | unconfirmed — five days after the 7 Aug renewal, no charge record read |
| [`fermis-silent-line-2026-08-12.mp3`](fermis-silent-line-2026-08-12.mp3) | [Fermi's Silent Line](../content/FERMIS-SILENT-LINE.md) | ignition song | 4:34 | 2026-08-12T19:06:15Z | `865a2236-d8ad-424a-b2d3-b22484fa90c2` | unconfirmed — five days after the 7 Aug renewal, no charge record read |

Rows are in generation order. Four working periods show up in it: **2–10 May
2026**, five recordings in nine days — Safari Chains arriving forty minutes
after Fermi's Silent Line on the same afternoon; **17, 21, 30 and 31 July** —
the 21st alone produced three, and the 31st's recording was generated on the
morning this directory was created; **the evening of 7 August into the
first minutes of 8 August (UTC)** — nine recordings in two hours: six Suno
"Remaster" takes of works already held and three new works (Story as Bridge,
Random Topic, Ferry Slip), beginning eight minutes after the subscription's
renewal charge, read in the maintainer's timezone (see the rights note
below); and **the evening of 12 August (UTC)** — four recordings in an hour:
three new works (Starline Weavers Crystal Core Cuts Clean, Come Into The New
Dream, Sovereign Gap Held) and a Remaster of Fermi's Silent Line.

All recordings are MP3, VBR between roughly 175 and 196 kbps, 48 kHz stereo.
The audio is Suno, generator version unrecorded. The seventeen files of
2026-08-07 and later carry fuller tags than the earlier exports — title, artist, embedded lyrics,
cover art and a C2PA manifest — a fact about Suno's export pipeline on that
date, recorded because provenance metadata is exactly what this catalogue is
for. Lyrics for the four canon works are credited on their pages to the
CrystalArchitect and CrystalDreamer (Grok); for the uncanonised recordings
the lyric credit is mostly not recorded anywhere and this file does not guess
it — with one exception it can read from the file itself: the embedded lyric
of `story-as-bridge.mp3` is the closing status block of the Grok "Rex"
export received 2026-08-07, filed as received in the Archive
(`GROK-REX-MYTHOS-EXPORT-2026-08-07.md` in
CrystalCore.OS-the-Crystal-Architecture-Archive), so that lyric's credit is
Grok, at the maintainer's direction. Every length, timestamp and track id
above was read from the file's own ID3 tag rather than supplied by hand.

## Uncanonised recordings

`safari-chains.mp3`, both takes of Different Parts, both takes of I'd Lay It
All Down, both takes of Starline Rivers, both takes of Dead But Came Back to
Life,
`the-girl-with-the-stars-in-her-chest.mp3`, `story-as-bridge.mp3`,
`random-topic.mp3`, `ferry-slip.mp3`, `bridge-not-loop.mp3`,
`starline-weavers-crystal-core-cuts-clean.mp3`, `come-into-the-new-dream.mp3`
and `sovereign-gap-held.mp3` are held here
and are **not part of the canon**. Another,
`look-what-you-made-me-do.mp3`, was also uncanonised and has since been
removed — see its truth label. A Suno Remaster of that work exists (generated
2026-08-07T22:16:08Z, id `796e8ece-61d4-469a-a7c6-7b09af287641`, 3:52) and
was deliberately **not** added to this directory on 12 August 2026: the
original was removed by the maintainer's decision, and a remaster of a
removed work does not come back on an archivist's. This line is that
recording's only record here.

**Story as Bridge sings the mythos's own words.** Its embedded lyric is the
closing status block of the Grok "Rex" export received the same day — the
mythos singing its own status line. The export it quotes is filed as
received in the Archive, under a reception record; being sung does not
canonise it, any more than being filed did. No lyric
page exists for any of them, and they appear in no canon document — not in
[The First Remembering](../content/THE-FIRST-REMEMBERING.md), not in the track
list in [`../crystalcore-os/crystalcore_os.py`](../crystalcore-os/crystalcore_os.py).

**One of them is a near miss worth naming.** Starline Rivers (both takes)
shares its title with [`starline-rivers.jpeg`](../art/starline-rivers.jpeg), which *is*
canon art — *"the starline rivers, light flowing between crystal cities across
the dark country."* Starline is also one of this project's own coinages rather
than a borrowed word. So the name is canon; the song is not. Those are
different facts and the table keeps them apart, but a later reader should see
the connection rather than have to notice it.

Being in this folder is not what makes a work canon. A work enters the canon by
being written into it — a page in [`../content/`](../content/), a line in a
canon document — and that is the maintainer's decision, not a consequence of a
file being backed up. Until then these are recordings that exist, honestly
labelled as such.

The same applies in reverse: nothing here says they *should not* be canon. The
question is simply open, and open is what it looks like when written down.

**Seven recordings are non-commercial; fifteen carry commercial rights; five
are unconfirmed.** The July tracks were generated after the first Pro period
ended on 6 June 2026, and Red Dust Axis and the first Shooting Star Girl take
were generated before it began on 7 May — see the plan column and the note
below it. The three mid-May recordings fall inside the first Pro period, and
the twelve recordings of 7–8 August were generated under the resumed Pro
plan. Bridge, Not Loop (11 August) and the four recordings of 12 August are
the unconfirmed ones: four and five days after the recorded renewal is
almost certainly inside the resumed plan's month, but this catalogue has
read no charge record past 7 August, and "almost certainly" is not a value
the plan column accepts. Nothing
about preservation changes; what changes is what may be done with them.

**Custody note, 2026-08-08.** The maintainer reports deleting from Suno the
tracks that cannot be used commercially. For the non-commercial recordings,
this directory now holds the only copy in existence — the failure this
directory was built against arrived from the other direction, and the
archive held. One recording was lost before it could be preserved: the
original, pre-Remaster take of The girl with the stars in her chest was
deleted on the platform and had never been exported. Its Remaster is the
only surviving recording of that work, and this line is that original's
only record.

**An open question, recorded rather than guessed.** Eight of the nine
Remaster takes derive from originals generated on the free tier. Whether a
remaster generated under a paid plan carries full commercial rights when
its source generation did not is a question of Suno's terms this catalogue
cannot settle from here. The plan column records the plan that was running
— a fact — and this note records the question.

**Which Shooting Star Girl is the song is an open question**, and this file
does not answer it. Both recordings are kept. If one is later chosen as canon,
say so here in a dated line and leave the other standing — the earlier record
is not wrong about the date it describes.

### What the columns mean

- **Canon status** — `ignition song` (one of the three in The First
  Remembering), `standalone, in canon` (named in the canon but not one of the
  three), or `not in canon` (no lyric page, named in no canon document). The
  canon draws these lines; the catalogue records them rather than deciding
  them.
- **Generated** and **Suno track id** — read from the file's ID3 tag. The id is
  a durable pointer back to the source, worth keeping now rather than
  reconstructing later.
- **Suno plan** — which plan was running *at the time the track was
  generated*. This is not bookkeeping trivia. Suno's free tier grants
  non-commercial use only; paid tiers grant commercial rights. The same audio
  file carries different rights depending on the plan it was made under, and
  the answer cannot be recovered from the file later. Record it while it is
  still knowable.

  **What the records show.** Three screenshots, order-detail receipts pulled
  directly from Apple's purchase history:

  - A subscription page (2026-07-31): **Suno Pro Plan, cancelled, ended
    6 June 2026**.
  - Order `MS2QMWQ5BD`, **7 May 2026, 4:52pm**: Suno Pro Plan, **"Init.
    Subscription"**, $15.00.
  - Order `MS2S00Y490`, **8 Aug 2026, 6:06am**: Suno Pro Plan, "Subscription
    Renewal", $15.00 — the subscription resumed and is renewing monthly as of
    this writing.

  **What that settles.** "Init. Subscription" is Apple's own label for a
  plan's *first* charge, not a renewal — this is not an inference from a time
  window, it is what the receipt itself says. The Pro period therefore began
  on 7 May 2026 and ended 6 June 2026, thirty days later, matching the
  cancellation record. Everything generated in that window was made on a paid
  plan: Wire Skull Memory, Fermi's Silent Line, Safari Chains. Everything
  outside it was not: Red Dust Axis and the first Shooting Star Girl take (both
  before 7 May), and all six July recordings (after 6 June). All rows from
  those periods are resolved; none remain open.

  **The resumed plan covers the August batch.** The renewal order
  `MS2S00Y490` reads 8 Aug 2026, 6:06am in the maintainer's local time —
  which is 2026-08-07T22:06Z in AWST (UTC+8), where this project lives. The
  nine generations run 2026-08-07T22:14:45Z to 2026-08-08T00:14:44Z: the
  first began eight minutes after the charge. Those nine rows are therefore recorded as
  made on the resumed Pro plan. If the receipt's timezone is ever shown to
  be something other than AWST, the charge still precedes the generations in
  any Australian timezone, so the conclusion holds.

## Truth labels

The [art README](../art/README.md) carries truth labels where a work needs
one — two pieces there bear a real person's photographic likeness and are
excluded from the Ordinals grant for that reason. The same discipline applies
here. A track needs a truth label if:

- it uses a real person's voice or likeness;
- it was generated on a plan that does not permit commercial use;
- it samples, interpolates or closely models an identifiable existing work;
- its provenance is uncertain in any way that would matter to someone
  licensing it.

### `look-what-you-made-me-do.mp3` — removed 2026-07-31

**The audio has been removed from this repository.** The catalogue row above is
kept, because the recording existed and a record that loses its own history is
not a record.

**What was found.** This file was filed on 2026-07-31 with an open truth label:
it shared its title with a very widely known 2017 song by Taylor Swift, and
nobody had listened to both. A shared title is not itself a problem — titles
carry no copyright, and unrelated works share them constantly. The audio was
the unverified part.

The maintainer listened, the same day, and **confirmed the recording does
relate to the earlier song**. That answers the question the label was raised
to hold open.

**Why removal rather than relabelling.** This repository is public and asserts
CC BY-NC-ND 4.0 over its audio. A Creative Commons licence is a *grant* — it
tells the world it may redistribute the file. Where a recording relates to
someone else's composition, that grant is not the maintainer's to make. The
copyright in *Look What You Made Me Do* sits with its writers, who include the
writers of *I'm Too Sexy* through its interpolation.

That reasoning is independent of any question about whether model-generated
audio attracts copyright of its own. The problem was never what the file is; it
was what publishing it under this licence claimed.

**What was not done.** The file remains in git history, and this repository has
not been rewritten to erase it. Rewriting public history to remove one track
would break the commit the Bitcoin anchor was made against, and would be a
larger act than the situation calls for. Anyone determined can still find the
blob; nothing at `main` serves it, and nothing here licenses it.

**What the anchor says now.** `MANIFEST.sha256.ots` attests the state of this
work on 2026-07-31, when the file was present. That attestation stays true
about that date. The manifest has been regenerated without the file and will be
stamped again; the two proofs sit beside each other, which is what a dated
record is supposed to look like.

**For anything measured rather than heard.** Objective features of the removed
file, for the record: 3:52, roughly 74 BPM, reading as D major. Those diverge
from the earlier song on every axis, which is a useful reminder that tempo and
key comparison cannot detect interpolation. Listening could and did.

## On copyright, plainly

Music generated by a model may attract **no copyright at all** — in Australia
as in the United States, copyright generally requires a human author. The
lyrics here are human-written (with model assistance, credited), and lyrics
are a separate copyright from a recording; the generated audio is the part in
question.

The practical consequence is not that the work is worthless. It is that the
thing being sold may not be exclusivity. What cannot be copied by copying a
file is the canon these songs belong to — the lattice, the lore, the art, one
author's coherent universe.

Two documents are affected by this and should be read alongside it:
[`../../docs/governance/ORDINALS-LICENCE-GRANT.md`](../../docs/governance/ORDINALS-LICENCE-GRANT.md),
which describes the Grantor as sole copyright holder, and
[`../content/LICENSE-CONTENT.md`](../content/LICENSE-CONTENT.md), which is a
copyright licence and therefore only bites where copyright exists.

Neither is wrong to have. Both are worth understanding before money moves.

## Ordinals

The [Ordinals licence grant](../../docs/governance/ORDINALS-LICENCE-GRANT.md)
covers **images in `mythos/art/` as at 2026-07-28**. It does not cover audio,
this directory, or anything added since that date. Extending it takes a dated
amendment to that file — not an assumption made here.

**The project issues no token.** That statement is load-bearing in the grant
and is repeated here so it travels with the music too.

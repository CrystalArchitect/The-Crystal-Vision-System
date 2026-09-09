# The Ancients Cycle

**Story- and Vision-layer — received mythos, reproduced whole, one bug
fixed.** This is not the project's own canon and not a claim about the
world. It is a functional, playable-in-browser custom card set —
fifteen legendary "Ancient" cards, Magic: The Gathering–style — built as
a single-page React app and delivered to the operator as a
Claude-Artifact-style HTML export (`React_Artifact.html`, the generic
default title that format uses).

The app itself: [`the-ancients-cycle/index.html`](the-ancients-cycle/index.html) —
open it in a browser, no build step required.

## Credit and provenance

Received as a direct upload to a conversation, 2026-09-04. **Authorship
(which model or person built it) was not stated at the point of
upload**, and none is invented here — the Constitution's own rule holds:
crediting a name costs nothing, guessing one wrongly costs someone their
attribution. If the operator confirms who made it, update this line
rather than replace it silently.

## What changed from the received file

One fix only, verified before and after: card **XIV, "In Your Name, the
Oathbearer,"** had its `mana` and `typeLine` object keys written twice
in the same object literal (`mana:"{W}{W}",typeLine:"...",tokenImage:Kv,
mana:"{W}{W}",typeLine:"..."`). Both writes held identical values so it
rendered fine, but it was a landmine — an edit to one copy without the
other would have silently diverged. The duplicate pair was removed;
nothing else in the file was touched. No other cards had this defect.

**Known, not fixed:** the file is ~15MB, almost entirely 16 embedded
base64 WebP card-art images inlined directly in the JS rather than
loaded as separate assets — every viewer downloads the full file before
anything renders. The card-open modal and the individual cards are not
keyboard-operable (`onClick` on a plain `<article>`, no `role="button"`,
no `tabIndex`, no in-app Escape handler). Left as received; flagged here
rather than silently "improved," since fixing either would mean editing
minified/bundled output rather than a real source tree.

## Terminology check against this project's own names

Checked against [`NAMES.md`](NAMES.md) and the locked names in
[`../docs/governance/Constitution.md`](../docs/governance/Constitution.md)
§1. **One real collision, logged rather than silently resolved** (same
discipline `CODEX-OF-THE-ORACLE.md` used for its own Weaver/Chronicle
collision, now also noted in
[`../memory/CANON-MAP.md`](../memory/CANON-MAP.md) "Known overlaps and
gaps"):

- **"Lattice"** is used repeatedly as a card game noun — a permanent
  type ("Artifact — Lattice Wall"), a land subtype ("Legendary Land —
  Mars Lattice"), and a counter ("lattice counter"). The Constitution
  locks **CrystalCore.Lattice** as a specific named component (the
  substrate, designed not built). This set's usage is a different,
  Loom-register sense of the bare word — a game piece, not the
  substrate — and does not touch or redefine the locked name. Read the
  card text as belonging to this document, not to the map.
- **"Crystal"** (a 0/1 colourless token type) and **"Rocket"** (a hasty
  creature token) are weaker echoes — generic nouns, not the compound
  Crystal-prefixed component names (CrystalMind, CrystalBus, etc.).
  "Rocket" in particular sits comfortably alongside this project's own
  mantra, *Red Dust → Rockets* — reinforcing rather than colliding with
  it.
- No Indigenous knowledge, imagery, or restricted term appears anywhere
  in the set.

## What it is, in its own terms

Fifteen legendary cards (numerals I–XV), each with a name, mana cost,
type line, rules text, flavour text, and an in-set "design meaning"
note tying it back to the wider Crystal/Lattice/Rocket/Scry mythos
already living in this repository — e.g. *"I Monad of Red Dust"* as
origin point, *"XIII TerAustralis Itself"* as a Legendary Land, *"VI"*
and *"VII"* built around a running joke (why is VI afraid of VII? — VII
ate IX, mechanically: VII exiles permanents of mana value 6+). The set's
own footer states plainly: *"Not affiliated with Wizards of the Coast.
Custom fan set."*

That self-disclosure is exactly right by this project's own test: it is
Vision by the plain check applied to every claim here — *can this be
executed or checked against the world?* A card game reskin of the
mythos cannot, and does not try to. It sits next to
[`MOTIFS.md`](content/MOTIFS.md) and
[`CODEX-OF-THE-ORACLE.md`](content/CODEX-OF-THE-ORACLE.md) the same way:
drawn with because it's good, not cited as if it does anything.

---

*Non Solus.*

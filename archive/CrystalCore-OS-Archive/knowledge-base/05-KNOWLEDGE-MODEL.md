# Knowledge Model

How the portfolio organizes truth, and how this archive fits into that
model.

## Statement

The portfolio has one primary truth-register: **Belt-Three** (Science /
Story / Vision), applied to every piece of content, everywhere,
including inside single documents that mix registers deliberately (the
Seven Sisters water briefs pair a Science entry with a Vision entry for
the same basin, never merging them). A claim's register is not a
quality judgment — a Vision-layer claim is not "worse" than a
Science-layer one, it is a different *kind* of claim, and the discipline
is entirely about never letting one kind pretend to be the other.

**Status: Implemented** (applied consistently almost everywhere this
reconstruction checked, with one confirmed exception — see below).

### Evidence
- `CONTRIBUTING.md`: "Code claims must be true; mythos must be labeled
  as mythos; no real-world coercion or fake hydrology, ever."
- `docs/governance/The-Incognita-Rule.md`, §1 ("Two kinds of line"):
  Surveyed = Science, Dreamed = Story/Vision.

### Historical Notes
None.

### Cross References
`04-GOVERNANCE.md` (Belt-Three in full).

---

## Statement

The second organizing register is the **Built / Vision split**: whether
a thing is running code a reader can execute, or narrative/art/
speculative framing. This is coarser than Belt-Three (a Vision-layer
document can still be "Built" in the sense of existing and being
complete as a document) but is the one most load-bearing for
architecture questions specifically — it is what separates
`03-ARCHITECTURE.md`'s two halves (the four real components vs. the
Seven Sisters narrative).

**Status: Implemented**, with **one confirmed inconsistency**:
`mythos/crystalcore-os/` is filed, by every document that describes it,
as Vision-layer / "a story, not infrastructure" / "Exists as a
document" — yet 8 of its 10 files (~2,300 of 2,860 lines) are ordinary,
structurally coherent Python implementing a real applied-ML system
(HuggingFace/DistilBERT fine-tuning, cross-attention multimodal fusion,
Bayesian uncertainty quantification), categorically different in kind
from the one file (`crystalcore_os.py`, 563 lines) that actually matches
the "Vision-layer text adventure" description. This reconstruction
preserves the project's own stated classification rather than
overriding it, while flagging the inconsistency plainly, per the
Incognita Rule's own standard.

### Evidence
- `mythos/CRYSTALCORE-OS.md`: "It's Vision-layer: a playable story, not
  one of the project's Built software components."
- `STATUS.md` (umbrella repo): files `mythos/crystalcore-os` under
  "Exists as a document," not "Built."
- Direct line-count and content read of all 10 files in
  `mythos/crystalcore-os/`: confirmed the ~2,300/2,860 split above.

### Historical Notes
None — this is a standing, unresolved classification tension, not
something that changed.

### Cross References
`06-COMPONENTS.md` (full component-level detail).

---

## Statement

A five-tier maturity ladder, used identically across every `STATUS.md`
in the portfolio: **Running** (executes, usable by someone other than
the maintainer), **Built, not currently running** (code exists, no
runtime exercises it), **Exists as a document** (written, no execution
involved), **Designed, not built** (specified, nobody has built it),
**Concept only** (named, not specified). This is the project's own
answer to this archive's "implemented / designed / historical /
unresolved" question — the two vocabularies map directly onto each
other, and this archive's Statement blocks use the four-term version
throughout for consistency with the reconstruction brief that produced
this archive.

**Status: Implemented.**

### Evidence
- `CrystalCore.OS-the-Crystal-Architecture-Archive/STATUS.md`
  (system ledger) and the two per-repo `STATUS.md` files, all using the
  identical five-category structure.

### Historical Notes
None.

### Cross References
`00-INDEX.md` (the four-question test).

---

## Statement

This knowledge base is itself governed by the same evidence discipline
it documents. It does not replace the underlying repositories' own
documentation — it is a secondary, reconstructed layer, and where it
and a primary source disagree, the primary source wins and this archive
has a bug. Every claim in this archive traces to a citation precise
enough to independently re-check (file path, line reference, commit
SHA, or a named specification/ADR/README) — the standard is not "an
exploration process occurred," it is "here is exactly where to look."

**Status: Implemented** (this is a description of this archive's own
construction, verifiable by spot-checking any Evidence block against
its cited source).

### Evidence
- This archive's own template, applied throughout: see `00-INDEX.md`
  §2.

### Historical Notes
None.

### Cross References
`12-CONTRIBUTING.md` (how to extend this without breaking the
discipline).

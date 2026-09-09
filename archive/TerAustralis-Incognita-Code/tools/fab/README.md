# fab — code-defined things you can hold

The first fabrication tooling in the portfolio: executable code in,
printable geometry out, with an independent checker standing between the
two. Nothing here is a mesh a generative model dreamed and nobody can
dimension — every solid is parameters and booleans, which means every
solid can be argued with, regenerated, and checked.

## Node One Vessel

A parametric enclosure for the machine the first companion boots on —
the vessel for the sovereign node the first real-world process needs
(see `transcripts/first-live-session-2026-08-08.md` in the companion's
repository, CrystalArchitect/Clementine-ai-companion
for why that machine is the next step the whole portfolio is waiting on).
Base tray with screw bosses, generous port windows, and NON SOLUS
engraved in the wall; friction-fit lid vented through a hexagonal
lattice that is decoration and airflow in the same geometry.

Defaults fit a Raspberry Pi 5 (85 × 56 mm, M2.5 holes on 58 × 49 mm) —
numbers taken from the published mechanical drawing, not measured from a
board in hand, so verify against yours. Change the `Params` block and
the same code fits any single-board machine. Raspberry Pi is a trademark
of Raspberry Pi Ltd; no affiliation, nominative use only.

### Generate

    pip install bpy                       # headless Blender as a module
    python tools/fab/node_one_vessel.py tools/fab/out

Emits `node-one-vessel-base.stl`, `node-one-vessel-lid.stl`, a combined
exploded `node-one-vessel.glb`, and a render. 1 unit = 1 mm; slicers
will read the STLs at true scale.

### Validate — different library on purpose

    pip install trimesh networkx numpy
    python tools/fab/validate_vessel.py tools/fab/out

The generator does not grade its own work. The checker loads the STLs
with trimesh and verifies what a slicer cares about: watertight,
consistently wound, one connected body, positive volume, stated exterior
dimensions, and that the engraved mark actually exists (probed at the
recess-floor plane, where boolean output actually puts vertices).

Output of the run the committed artifacts came from, 2026-08-08:

    == node-one-vessel-base.stl ==
      watertight   PASS  closed manifold solid
      winding      PASS  faces consistently oriented
      single body  PASS  1 connected body/ies
      volume       PASS  34.8 cm3
      dimensions   PASS  (92.8, 63.8, 34.8) mm vs expected (92.8, 63.8, 34.8) ±0.2
      mark engraved PASS  540 vertices on the recess floor 0.6 mm in
      triangles          3530

    == node-one-vessel-lid.stl ==
      watertight   PASS  closed manifold solid
      winding      PASS  faces consistently oriented
      single body  PASS  1 connected body/ies
      volume       PASS  12.2 cm3
      dimensions   PASS  (92.8, 63.8, 6.4) mm vs expected (92.8, 63.8, 6.4) ±0.2
      triangles          1472

    all checks passed

The checker earned its place on its first day: it caught screw bosses
that touched the floor without joining it (five bodies pretending to be
one part), an arithmetic slip in this file's own expectations, and — in
the other direction — its own first mark-probe looking for vertices in a
band booleans never put vertices in. All three catches are recorded in
the code comments where they happened.

### Print (dreamed until printed)

Belt-Three honesty: everything above is **surveyed geometry** — closed
solids with the stated dimensions, machine-checked. Whether the printed
part fits a real board, holds its self-tappers, friction-fits its lid
and breathes well enough under inference load is **dreamed until
printed**. An unprinted design is a dreamed line about plastic.

Design intent for the first attempt: PLA or PETG, 0.2 mm layers, no
supports (the port windows bridge; the lid prints plate-down), 3
perimeters. Pilot holes are 2.2 mm for M2.5 self-tappers. Print, measure
against your board, adjust `Params`, regenerate — iteration is a number
change, not a redraw.

---

*Honour to Country beneath every wire. Non Solus.*

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059

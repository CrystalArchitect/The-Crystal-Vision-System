# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Independent geometry checks for the Node One Vessel exports.

Deliberately not Blender: the generator must not grade its own work, so
this loads the STLs with trimesh and checks the claims a slicer cares
about — watertight, consistently wound, one body, positive volume, and
the stated exterior dimensions. The expected numbers are restated here
on purpose (independence over DRY); if you change Params in the
generator, change EXPECT below to match, and the diff records that both
moved together.

    pip install trimesh numpy
    python tools/fab/validate_vessel.py [dir_with_stls]

Exit code 0 means every check passed. What passing proves is geometry,
nothing more: fit, strength and airflow stay dreamed until printed.
"""

import sys
from pathlib import Path

import trimesh

# part filename -> (bbox extents in mm, tolerance mm)
# base height = floor 2.4 + standoff 6.0 + board 1.4 + headroom 25.0 = 34.8.
# (The first draft of this table said 33.4 — arithmetic drift, caught by
# the part itself on the first validation run. The restatement policy cuts
# both ways, which is what it is for.)
EXPECT = {
    "node-one-vessel-base.stl": ((92.8, 63.8, 34.8), 0.2),
    "node-one-vessel-lid.stl": ((92.8, 63.8, 6.4), 0.2),
}


def check(path: Path, expect, tol):
    mesh = trimesh.load(path, force="mesh")
    rows = []
    ok = True

    def row(name, passed, detail):
        nonlocal ok
        ok = ok and passed
        rows.append((name, "PASS" if passed else "FAIL", detail))

    row("watertight", mesh.is_watertight, "closed manifold solid")
    row("winding", mesh.is_winding_consistent, "faces consistently oriented")
    bodies = len(mesh.split(only_watertight=False))
    row("single body", bodies == 1, f"{bodies} connected body/ies")
    vol = float(mesh.volume) if mesh.is_watertight else 0.0
    row("volume", vol > 0, f"{vol / 1000.0:.1f} cm3")
    ext = tuple(round(float(v), 2) for v in mesh.extents)
    dims_ok = all(abs(e - x) <= tol for e, x in zip(sorted(ext), sorted(expect)))
    row("dimensions", dims_ok, f"{ext} mm vs expected {expect} ±{tol}")

    # The base carries the NON SOLUS mark, engraved 0.6 mm into the -Y
    # wall. A boolean's output puts vertices only at feature boundaries —
    # the rim on the outer face and the recess floor 0.6 mm in, nothing
    # between — so the honest probe looks AT the recess-floor plane, not
    # the empty air between planes. (The first draft of this check probed
    # the space between and reported a mark that existed as missing;
    # instrumented rebuild found the cut present and the probe blind.
    # A checker can be wrong in both directions; this one now states
    # where it looks and why.)
    if "base" in path.name:
        ymin = float(mesh.bounds[0][1])
        v = mesh.vertices
        floor_band = v[(v[:, 1] > ymin + 0.55) & (v[:, 1] < ymin + 0.65)]
        row("mark engraved", len(floor_band) > 50,
            f"{len(floor_band)} vertices on the recess floor 0.6 mm in")

    rows.append(("triangles", "", f"{len(mesh.faces)}"))

    print(f"\n== {path.name} ==")
    for name, verdict, detail in rows:
        print(f"  {name:<12} {verdict:<5} {detail}")
    return ok


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "tools/fab/out")
    all_ok = True
    for fname, (expect, tol) in EXPECT.items():
        path = out / fname
        if not path.exists():
            print(f"\n== {fname} ==\n  missing        FAIL  not found in {out}/")
            all_ok = False
            continue
        all_ok = check(path, expect, tol) and all_ok
    print(f"\n{'all checks passed' if all_ok else 'CHECKS FAILED'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

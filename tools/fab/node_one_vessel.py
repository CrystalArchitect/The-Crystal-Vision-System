# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Node One Vessel — parametric enclosure generator for the first
companion's machine.

Executable code in, printable geometry out: run under Blender's Python
(the `bpy` module, headless is fine) and it emits two STLs (base tray,
vented lid), a combined GLB, and a render. Every dimension is a named
parameter below — change the board numbers and the same code fits a
different machine, which is the point: the vessel is code, and code is
the one material this project can already fabricate anywhere.

    pip install bpy
    python tools/fab/node_one_vessel.py [output_dir]

Then validate the geometry with the independent checker (different
library on purpose — the generator must not grade its own work):

    python tools/fab/validate_vessel.py <output_dir>

Defaults target a Raspberry Pi 5 (85 x 56 mm board, M2.5 holes on a
58 x 49 mm rectangle inset 3.5 mm from the corners). Those numbers are
from the published mechanical drawing, not from measuring a board in
hand — verify against your board before trusting a print. Raspberry Pi
is a trademark of Raspberry Pi Ltd; this project is not affiliated with
it, this is nominative use only.

Belt-Three honesty, load-bearing: what this script proves is geometry —
watertight solids with the stated dimensions. Whether the printed part
fits a real board, holds its screws, and breathes well enough under
inference load is *dreamed until printed*. An unprinted design is a
dreamed line about plastic. Print, measure, iterate; the parameters
exist so iteration is a number change, not a redraw.

Units: 1 Blender unit = 1 mm. STL is unitless and slicers assume mm,
so exports land at true scale.
"""

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import bpy


# ---------------------------------------------------------------------------
# Parameters — the whole design, in numbers a person can argue with
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Params:
    # The board this vessel is for (defaults: Raspberry Pi 5, from the
    # published drawing — verify against the board in your hand).
    board_x: float = 85.0          # board length, mm
    board_y: float = 56.0          # board width, mm
    hole_pitch_x: float = 58.0     # mounting-hole rectangle, mm
    hole_pitch_y: float = 49.0
    hole_inset: float = 3.5        # hole-centre inset from board corner, mm

    # Vessel shell
    wall: float = 2.4              # side wall thickness, mm (3 perimeters)
    floor: float = 2.4             # base floor thickness, mm
    clearance: float = 1.5         # board-edge to inner-wall gap, mm
    interior_above_board: float = 25.0  # headroom above the board, mm
    board_thickness: float = 1.4   # PCB thickness, mm

    # Standoffs (screw bosses) — board rests here, M2.5 self-tappers bite
    standoff_h: float = 6.0        # keeps the underside connector clear, mm
    standoff_d: float = 6.2        # boss outer diameter, mm
    pilot_d: float = 2.2           # M2.5 self-tap pilot, mm
    pilot_depth: float = 5.0       # blind pilot depth, mm

    # Port windows — coarse on purpose in v0; print, measure, tighten
    portx_w: float = 52.0          # +X short side (USB / Ethernet), mm
    portx_h: float = 16.0
    porty_w: float = 48.0          # +Y long side (power / HDMI), mm
    porty_h: float = 14.0

    # Lid — friction fit, hex-vented
    lid_plate: float = 2.4         # lid plate thickness, mm
    lip_h: float = 4.0             # friction lip depth into the cavity, mm
    lip_wall: float = 1.6          # lip wall thickness, mm
    fit_gap: float = 0.25          # lip-to-wall clearance per side, mm
    vent_across_flats: float = 6.0 # hex vent size, mm
    vent_web: float = 2.6          # web left between vents, mm
    vent_margin: float = 7.0       # no vents this close to the lid edge, mm

    # The mark — shallow engraving on the -Y wall, printable on a vertical
    mark_text: str = "NON SOLUS"
    mark_depth: float = 0.6        # engrave depth, mm
    mark_size: float = 7.0         # cap height, mm

    # Derived
    @property
    def inner_x(self) -> float:
        return self.board_x + 2 * self.clearance

    @property
    def inner_y(self) -> float:
        return self.board_y + 2 * self.clearance

    @property
    def cavity_h(self) -> float:
        return self.standoff_h + self.board_thickness + self.interior_above_board

    @property
    def outer_x(self) -> float:
        return self.inner_x + 2 * self.wall

    @property
    def outer_y(self) -> float:
        return self.inner_y + 2 * self.wall

    @property
    def base_h(self) -> float:
        return self.floor + self.cavity_h


# ---------------------------------------------------------------------------
# Small helpers over bpy — kept dumb and explicit
# ---------------------------------------------------------------------------

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _apply_all(obj):
    with bpy.context.temp_override(object=obj, active_object=obj,
                                   selected_objects=[obj]):
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def box(name, sx, sy, sz, at=(0.0, 0.0, 0.0)):
    """A cuboid of exact dimensions, centred at `at`."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=at)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (sx, sy, sz)
    _apply_all(obj)
    return obj


def cylinder(name, d, h, at=(0.0, 0.0, 0.0), verts=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=d / 2.0,
                                        depth=h, location=at)
    obj = bpy.context.active_object
    obj.name = name
    _apply_all(obj)
    return obj


def hex_prism(name, across_flats, h, at):
    """A hexagonal prism; across-flats is the honest printed size."""
    r = (across_flats / 2.0) / math.cos(math.pi / 6.0)  # flats -> circumradius
    return cylinder(name, 2.0 * r, h, at=at, verts=6)


def join(target, others):
    objs = [target] + list(others)
    with bpy.context.temp_override(active_object=target, selected_objects=objs,
                                   selected_editable_objects=objs):
        bpy.ops.object.join()
    return target


def boolean(target, cutter, op):
    mod = target.modifiers.new(name=op, type='BOOLEAN')
    mod.operation = op
    mod.object = cutter
    try:
        mod.solver = 'EXACT'
    except TypeError:
        pass  # older/newer solver enum — the default will do
    with bpy.context.temp_override(object=target, active_object=target,
                                   selected_objects=[target]):
        bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)
    return target


def text_solid(name, text, size, thickness):
    """Text as a solid mesh slab, for engraving by difference.

    Meshed via the evaluated depsgraph rather than the convert operator:
    headless, the operator can quietly do nothing, the boolean then gets a
    non-mesh object and quietly does nothing either, and the mark simply
    never appears. (That exact silence happened on the first run — the
    validator's mark probe caught it.) This path either meshes or raises.
    """
    bpy.ops.object.text_add()
    src = bpy.context.active_object
    src.data.body = text
    src.data.size = size
    src.data.extrude = thickness / 2.0
    src.data.align_x = 'CENTER'
    src.data.align_y = 'CENTER'
    deps = bpy.context.evaluated_depsgraph_get()
    mesh = bpy.data.meshes.new_from_object(src.evaluated_get(deps))
    if len(mesh.polygons) == 0:
        raise RuntimeError("text meshed to nothing — no silent no-marks")

    # Meshed text arrives visually solid but topologically open: the caps
    # and the extruded sides carry duplicate rim vertices, every rim edge
    # reads as boundary, and the EXACT boolean treats the cutter as not a
    # solid and quietly cuts nothing. Weld the seams shut, then insist.
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bm.to_mesh(mesh)
    bm.free()
    open_edges = sum(1 for e in mesh.edges if e.is_loose)
    boundary = 0
    counts = {}
    for poly in mesh.polygons:
        for a, b in poly.edge_keys:
            k = (a, b) if a < b else (b, a)
            counts[k] = counts.get(k, 0) + 1
    boundary = sum(1 for c in counts.values() if c == 1)
    if boundary or open_edges:
        raise RuntimeError(
            f"text mesh still open after weld ({boundary} boundary edges) — "
            "refusing to hand the boolean a cutter it will silently ignore")

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    bpy.data.objects.remove(src, do_unlink=True)
    return obj


# ---------------------------------------------------------------------------
# The two parts
# ---------------------------------------------------------------------------

def build_base(p: Params):
    """Tray: shell minus cavity, plus bosses, minus pilots, ports, mark."""
    base = box("vessel_base", p.outer_x, p.outer_y, p.base_h,
               at=(0, 0, p.base_h / 2.0))
    cavity = box("cavity", p.inner_x, p.inner_y, p.cavity_h + 1.0,
                 at=(0, 0, p.floor + (p.cavity_h + 1.0) / 2.0))
    boolean(base, cavity, 'DIFFERENCE')

    # Screw bosses at the board's hole pattern (board centred in the cavity).
    # Each boss reaches 0.5 mm down INTO the floor: a union of exactly
    # touching faces leaves disconnected shells (the independent checker
    # caught precisely this — five bodies), an overlap fuses one solid.
    hx, hy = p.hole_pitch_x / 2.0, p.hole_pitch_y / 2.0
    sink = 0.5
    bosses = []
    for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
        bosses.append(cylinder(f"boss_{i}", p.standoff_d, p.standoff_h + sink,
                               at=(sx * hx, sy * hy,
                                   p.floor + (p.standoff_h - sink) / 2.0)))
    cutters = join(bosses[0], bosses[1:])
    boolean(base, cutters, 'UNION')

    pilots = []
    for i, (sx, sy) in enumerate([(1, 1), (1, -1), (-1, 1), (-1, -1)]):
        top = p.floor + p.standoff_h
        pilots.append(cylinder(f"pilot_{i}", p.pilot_d, p.pilot_depth + 0.2,
                               at=(sx * hx, sy * hy,
                                   top - (p.pilot_depth + 0.2) / 2.0 + 0.1),
                               verts=32))
    pilot_cut = join(pilots[0], pilots[1:])
    boolean(base, pilot_cut, 'DIFFERENCE')

    # Port windows: sill at standoff top so the board's edge connectors clear
    sill = p.floor + p.standoff_h
    px = box("port_x", p.wall + 2.0, p.portx_w, p.portx_h,
             at=(p.outer_x / 2.0 - p.wall / 2.0, 0,
                 sill + p.portx_h / 2.0))
    boolean(base, px, 'DIFFERENCE')
    py = box("port_y", p.porty_w, p.wall + 2.0, p.porty_h,
             at=(0, p.outer_y / 2.0 - p.wall / 2.0,
                 sill + p.porty_h / 2.0))
    boolean(base, py, 'DIFFERENCE')

    # The mark, engraved shallow into the -Y wall's outer face
    if p.mark_text:
        mark = text_solid("mark", p.mark_text, p.mark_size, p.mark_depth * 2)
        mark.rotation_euler = (math.pi / 2.0, 0.0, 0.0)
        mark.location = (0, -p.outer_y / 2.0, p.base_h * 0.55)
        _apply_all(mark)
        boolean(base, mark, 'DIFFERENCE')

    return base


def build_lid(p: Params):
    """Plate with a friction lip and a crystal-lattice vent field."""
    z0 = p.base_h  # lid plate sits on the tray's rim
    lid = box("vessel_lid", p.outer_x, p.outer_y, p.lid_plate,
              at=(0, 0, z0 + p.lid_plate / 2.0))

    # The lip overlaps 0.5 mm up into the plate for the same reason the
    # bosses sink into the floor: touching is not joined, overlap is.
    sink = 0.5
    lip_ox = p.inner_x - 2 * p.fit_gap
    lip_oy = p.inner_y - 2 * p.fit_gap
    lip_outer = box("lip_outer", lip_ox, lip_oy, p.lip_h + sink,
                    at=(0, 0, z0 - (p.lip_h - sink) / 2.0))
    lip_inner = box("lip_inner", lip_ox - 2 * p.lip_wall,
                    lip_oy - 2 * p.lip_wall, p.lip_h + 1.0,
                    at=(0, 0, z0 - (p.lip_h + 1.0) / 2.0 + 0.5))
    boolean(lip_outer, lip_inner, 'DIFFERENCE')
    boolean(lid, lip_outer, 'UNION')

    # Hex vent field — the lattice, doing real work as airflow
    pitch = p.vent_across_flats + p.vent_web
    row_h = pitch * math.sqrt(3.0) / 2.0
    span_x = p.outer_x - 2 * p.vent_margin - p.vent_across_flats
    span_y = p.outer_y - 2 * p.vent_margin - p.vent_across_flats
    cols = int(span_x // pitch) + 1
    rows = int(span_y // row_h) + 1
    hexes = []
    for r in range(rows):
        y = -span_y / 2.0 + r * row_h
        offset = (pitch / 2.0) if (r % 2) else 0.0
        for c in range(cols):
            x = -span_x / 2.0 + c * pitch + offset
            if x > span_x / 2.0 + 0.01:
                continue
            hexes.append(hex_prism(f"vent_{r}_{c}", p.vent_across_flats,
                                   p.lid_plate + 2.0,
                                   at=(x, y, z0 + p.lid_plate / 2.0)))
    if hexes:
        vent_cut = join(hexes[0], hexes[1:])
        boolean(lid, vent_cut, 'DIFFERENCE')

    return lid


# ---------------------------------------------------------------------------
# Exports and the record
# ---------------------------------------------------------------------------

def export_stl(obj, path: Path):
    for o in bpy.context.view_layer.objects:
        o.select_set(o is obj)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=str(path), export_selected_objects=True,
                          apply_modifiers=True)


def render_hero(p: Params, path: Path):
    """One honest look at the parts, workbench engine, no glamour."""
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.light = 'STUDIO'
    scene.display.shading.color_type = 'OBJECT'
    for o in bpy.context.view_layer.objects:
        if o.type == 'MESH':
            o.color = (0.55, 0.75, 0.85, 1.0)
    scene.render.resolution_x = 1400
    scene.render.resolution_y = 1000
    scene.render.filepath = str(path)

    cam_data = bpy.data.cameras.new("cam")
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    d = max(p.outer_x, p.outer_y) * 3.1
    cam.location = (d * 0.72, -d * 0.72, d * 0.5)
    target = bpy.data.objects.new("cam_target", None)
    scene.collection.objects.link(target)
    target.location = (0, 0, p.base_h * 0.9)  # between tray and lifted lid
    track = cam.constraints.new(type='TRACK_TO')
    track.target = target
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    scene.camera = cam

    sun_data = bpy.data.lights.new("sun", type='SUN')
    sun = bpy.data.objects.new("sun", sun_data)
    scene.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))

    bpy.ops.render.render(write_still=True)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "tools/fab/out")
    out.mkdir(parents=True, exist_ok=True)
    p = Params()

    reset_scene()
    base = build_base(p)
    lid = build_lid(p)

    # Exploded view for the render and the GLB: lid lifted clear
    lid.location.z += 28.0
    _apply_all(lid)

    export_stl(base, out / "node-one-vessel-base.stl")
    export_stl(lid, out / "node-one-vessel-lid.stl")
    bpy.ops.export_scene.gltf(filepath=str(out / "node-one-vessel.glb"),
                              export_format='GLB')
    render_hero(p, out / "node-one-vessel.png")

    print(f"vessel: outer {p.outer_x:.1f} x {p.outer_y:.1f} mm, "
          f"base {p.base_h:.1f} mm tall, lid plate {p.lid_plate:.1f} mm "
          f"+ {p.lip_h:.1f} mm lip")
    print(f"board: {p.board_x:.0f} x {p.board_y:.0f} mm on "
          f"{p.hole_pitch_x:.0f} x {p.hole_pitch_y:.0f} mm holes, "
          f"bosses {p.standoff_h:.0f} mm, pilots {p.pilot_d:.1f} mm")
    print(f"wrote 2 STL + 1 GLB + 1 PNG to {out}/")


if __name__ == "__main__":
    main()

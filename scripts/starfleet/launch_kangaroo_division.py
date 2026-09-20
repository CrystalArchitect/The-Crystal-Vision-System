#!/usr/bin/env python3
"""Launch Starfleet Australia — Kangaroo Division (hub coordination).

    python3 scripts/starfleet/launch_kangaroo_division.py

Does NOT adopt a Starfleet persona. Does NOT claim MoU / pads / warp.
Vision ≠ Built. Canon: no.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PACK = ROOT / "archive" / "starfleet-au-kangaroo-pack"
REQUIRED = (
    "README.md",
    "01-PITCH-ONE-PAGER.md",
    "02-SPEC-SHEET.md",
    "03-FACTCHECK.md",
    "04-INDUSTRIAL-NODES.md",
    "assets/au-sites-map.png",
    "assets/kangaroo-class-ncc-992-au.jpeg",
)

DIVISION_TOPIC = (
    "STARFLEET AUSTRALIA — KANGAROO DIVISION LAUNCH. "
    "Vision only: AU shipyard + Academy adjacency pitch (NCC-992-AU fiction cover). "
    "Hard no: Starship MoU, warp, ELA-as-live, Core≠TAI collapse, false Elon bonds. "
    "Map each seat's honest role if any. Label science|story|vision. Canon: no. Human publishes."
)


def _check_pack() -> list[str]:
    missing = []
    for rel in REQUIRED:
        if not (PACK / rel).exists():
            missing.append(rel)
    return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch Kangaroo Division")
    parser.add_argument("--skip-chaos", action="store_true")
    parser.add_argument("--skip-align", action="store_true")
    parser.add_argument(
        "--out",
        default="",
        help="chaos ledger path (default under 14_AI_INTERACTIONS/chaos-ledger/)",
    )
    args = parser.parse_args(argv)

    stamp = datetime.now(tz=timezone.utc)
    iso = stamp.strftime("%Y-%m-%d %H:%M UTC")
    print("═══════════════════════════════════════════")
    print("  STARFLEET AUSTRALIA — KANGAROO DIVISION")
    print("  Status: LAUNCH sequence · Canon: no")
    print("═══════════════════════════════════════════")

    missing = _check_pack()
    if missing:
        print("PACK FAIL — missing:")
        for m in missing:
            print(f"  - {m}")
        return 2
    print(f"pack: OK ({PACK.relative_to(ROOT)})")

    map_doc = ROOT / "00_MASTER_INDEX" / "STARFLEET-AU-KANGAROO-DIVISION.md"
    if not map_doc.exists():
        print(f"map missing: {map_doc}")
        return 2
    print(f"map:  {map_doc.relative_to(ROOT)}")

    if not args.skip_align:
        sys.path.insert(0, str(ROOT / "scripts" / "chaos"))
        import align as chaos_align

        drift = chaos_align.audit()
        if drift:
            print("align DRIFT — Division launch holds but Chaos fan-out blocked:")
            for d in drift:
                print(f"  - {d}")
            return 3
        print("align: DRIFT NONE")

    result_meta: dict = {
        "division": "Kangaroo Division",
        "fleet": "Starfleet Australia",
        "callsign_fiction": "NCC-992-AU",
        "launched_at": iso,
        "canon": False,
        "vision": True,
        "hard_nos": [
            "no_starship_mou",
            "no_warp",
            "no_ela_as_live",
            "no_false_elon_bonds",
            "no_starfleet_persona_adoption",
            "kangaroo_class_is_fiction_cover",
        ],
        "pack": str(PACK.relative_to(ROOT)),
    }

    if not args.skip_chaos:
        from crystal_platform.chaos import ChaosEngine
        from crystal_platform.orchestration import build_live_stack

        engine = ChaosEngine(stack=build_live_stack(provider_ids=("local.open",)))
        run = engine.run(DIVISION_TOPIC)
        result_meta["chaos_run_id"] = run.run_id
        result_meta["cross_compare"] = dict(run.cross_compare)
        ledger_dir = ROOT / "14_AI_INTERACTIONS" / "chaos-ledger"
        ledger_dir.mkdir(parents=True, exist_ok=True)
        if args.out:
            out = Path(args.out)
            if not out.is_absolute():
                out = ROOT / out
        else:
            out = ledger_dir / f"{stamp.strftime('%Y%m%dT%H%M%SZ')}-KANGAROO-DIVISION.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(run.markdown(), encoding="utf-8")
        json_path = out.with_suffix(".json")
        json_path.write_text(
            json.dumps(
                {
                    **result_meta,
                    "replies": [
                        {
                            "provider_id": r.provider_id,
                            "status": r.status,
                            "silent": r.silent,
                            "text": r.text,
                        }
                        for r in run.replies
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"chaos: run={run.run_id}")
        print(
            f"  asked={run.cross_compare['seats_asked']} "
            f"ok={run.cross_compare['seats_ok']} "
            f"silent={run.cross_compare['seats_silent']}"
        )
        print(f"  ledger={out.relative_to(ROOT)}")
    else:
        print("chaos: skipped")

    launch_stamp = ROOT / "14_AI_INTERACTIONS" / "2026-09-20-STARFLEET-KANGAROO-DIVISION-LAUNCHED.md"
    launch_stamp.write_text(
        "\n".join(
            [
                "# Starfleet Australia — Kangaroo Division LAUNCHED",
                "",
                "**Canon:** **no**  ",
                f"**When:** {iso}  ",
                "**Layer:** vision / coordination  ",
                "**Map:** [`../00_MASTER_INDEX/STARFLEET-AU-KANGAROO-DIVISION.md`](../00_MASTER_INDEX/STARFLEET-AU-KANGAROO-DIVISION.md)  ",
                "**Pack:** `archive/starfleet-au-kangaroo-pack/`  ",
                "",
                "## Cleared",
                "",
                "- Pack files present",
                "- Hub Division map on disk",
                "- Chaos align clean (if run)",
                "- Persona adoption: **refused** (mythos ≠ authorize)",
                "",
                "## Hard nos held",
                "",
                "- No Starship MoU · no warp · no ELA-as-live · no false Elon bonds",
                "- Kangaroo-class = fiction cover only",
                "",
                f"Chaos run: `{result_meta.get('chaos_run_id', 'n/a')}`",
                "",
                "*Non Solus.* · Kangaroo Division away.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"stamp: {launch_stamp.relative_to(ROOT)}")
    print("───────────────────────────────────────────")
    print("  KANGAROO DIVISION — LAUNCHED (Vision)")
    print("───────────────────────────────────────────")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

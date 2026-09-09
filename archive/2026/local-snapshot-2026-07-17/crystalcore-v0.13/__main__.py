"""
python -m crystalcore           → live status board
python -m crystalcore status    → live status board
python -m crystalcore expose    → full JSON transparency dump
"""
from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = (args[0] if args else "status").lower()
    rest = args[1:] if args and args[0].lower() in ("status", "expose") else args

    if cmd == "expose":
        from .expose import main as expose_main
        return expose_main(rest)
    if cmd in ("status", "-h", "--help") or not args or args[0].startswith("-"):
        from .status import main as status_main
        # bare flags go to status; explicit "status" strips the subcommand
        if cmd == "status":
            return status_main(rest)
        if cmd in ("-h", "--help"):
            print(
                "CrystalCore\n"
                "  python -m crystalcore           live status board\n"
                "  python -m crystalcore status    live status board\n"
                "  python -m crystalcore expose    full JSON dump\n"
            )
            return 0
        return status_main(args)
    # unknown subcommand → status helpfully
    from .status import main as status_main
    return status_main(args)


raise SystemExit(main())

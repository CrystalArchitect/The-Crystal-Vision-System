#!/usr/bin/env python3
"""Cut the two JPEG sizes each volume needs, and write the manifest.

The second heredoc the build README lists as never saved. For every slug in a
catalogue module it writes:

* an **archival** JPEG into ``--archive`` — long edge capped, good quality.
  This is the copy committed to ``vision-plates/<volume>/plates/``.
* a **web** JPEG into ``--web`` — smaller, cheaper. Only the inline build reads
  these; they are not committed.

and records ``native`` (the size as supplied) plus ``web`` (the dimensions the
builders write into the ``width``/``height`` attributes) into the manifest.

Nothing is ever upscaled. A source already under the cap is re-encoded at the
target quality at its own size, which is why several Volume II plates are
identical in both manifest fields.

    python3 resize.py --catalogue plates2 --src /path/to/uploads \\
        --archive archive2 --web web2 --manifest manifest2.json

Volume I used ``--web-max 1320``; Volume II used the 1000 default. Both used the
2400 archival cap. Run this before the builders — they read the manifest, and a
slug missing from it is a ``KeyError`` at render time rather than a clear error.
"""
import argparse
import importlib
import json
import math
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:                                     # pragma: no cover
    raise SystemExit("needs Pillow: pip install Pillow")

HERE = os.path.dirname(os.path.abspath(__file__))
RESAMPLE = Image.Resampling.LANCZOS


def catalogue(name):
    """Return the ``slug -> entry`` mapping from a catalogue module.

    Volume II onwards builds it with ``add()`` into ``P``; Volume I predates
    that and uses ``PLATES`` with no ``src`` key, so it cannot be resized from
    here without one being added.
    """
    sys.path.insert(0, HERE)
    mod = importlib.import_module(name)
    for attr in ("P", "PLATES"):
        if hasattr(mod, attr):
            return getattr(mod, attr)
    raise SystemExit("%s defines neither P nor PLATES" % name)


def fit(size, cap):
    """Scale ``size`` down so its long edge is at most ``cap``. Never up.

    Halves round up, not to even. A 1792×1008 source at the 1000 cap gives a
    short edge of exactly 562.5, and the committed manifests record 563 — so
    ``round()`` would silently disagree with every existing plate at that ratio.
    """
    w, h = size
    if max(w, h) <= cap:
        return w, h
    scale = cap / float(max(w, h))
    return (max(1, int(math.floor(w * scale + 0.5))),
            max(1, int(math.floor(h * scale + 0.5))))


def write(im, size, path, quality):
    out = im if im.size == size else im.resize(size, RESAMPLE)
    out.convert("RGB").save(path, "JPEG", quality=quality, optimize=True,
                            progressive=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalogue", required=True,
                    help="catalogue module, e.g. plates2 (needs a src per entry)")
    ap.add_argument("--src", required=True, help="directory holding the supplied images")
    ap.add_argument("--archive", required=True, help="output directory for committed JPEGs")
    ap.add_argument("--web", required=True, help="output directory for inline-build JPEGs")
    ap.add_argument("--manifest", required=True, help="manifest JSON to write")
    ap.add_argument("--archive-max", type=int, default=2400)
    ap.add_argument("--archive-quality", type=int, default=88)
    ap.add_argument("--web-max", type=int, default=1000)
    ap.add_argument("--web-quality", type=int, default=76)
    args = ap.parse_args()

    plates = catalogue(args.catalogue)
    no_src = [s for s, p in plates.items() if not p.get("src")]
    if no_src:
        raise SystemExit("%d entries have no src: %s"
                         % (len(no_src), ", ".join(sorted(no_src)[:5])))

    for d in (args.archive, args.web):
        os.makedirs(d, exist_ok=True)

    manifest = {}
    for slug, p in plates.items():
        src = os.path.join(args.src, p["src"])
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)   # honour orientation before measuring
            native = im.size
            arch = fit(native, args.archive_max)
            web = fit(native, args.web_max)
            write(im, arch, os.path.join(args.archive, slug + ".jpg"), args.archive_quality)
            write(im, web, os.path.join(args.web, slug + ".jpg"), args.web_quality)
        manifest[slug] = {"native": "%d×%d" % native, "web": list(web)}
        print("%-38s %s -> archive %s, web %s"
              % (slug, "%d×%d" % native, "%d×%d" % arch, "%d×%d" % web))

    with open(args.manifest, "w") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote %s — %d plates" % (args.manifest, len(manifest)))


if __name__ == "__main__":
    main()

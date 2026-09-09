#!/usr/bin/env python3
"""Emit the ``@font-face`` CSS the builders splice in at ``__FONTS__``.

This step used to be a heredoc, which is why a clean clone could not run
``build.py`` or ``build2.py`` at all: both open ``fonts.css`` (inline mode) or
``fonts-linked.css`` (linked mode) at import time, and neither file was
committed. Written out here so the pipeline runs from a checkout.

No network call. The four Latin-subset WOFF2 files are already vendored in
``../fonts/`` under the SIL OFL; this reads them off disk. The original heredoc
fetched them from Google Fonts with a full Chrome UA and deduped by content
hash — that fetch is what produced the vendored files, and it does not need
repeating unless a family changes.

    python3 fonts.py                    # -> fonts.css + fonts-linked.css (fonts/)
    python3 fonts.py --prefix ../fonts/ # volume-2 and any later volume

The prefix is the only thing that differs between volumes: Volume I sits beside
``fonts/``, every volume in a subdirectory reaches ``../fonts/``.
"""
import argparse
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")

# file -> (family, style, weight). Weight ranges are variable fonts served by
# Google Fonts as a single file covering the whole range.
FACES = [
    ("ibm-plex-mono.woff2", "IBM Plex Mono", "normal", "400"),
    ("ibm-plex-sans.woff2", "IBM Plex Sans", "normal", "400 600"),
    ("newsreader-italic.woff2", "Newsreader", "italic", "400"),
    ("newsreader.woff2", "Newsreader", "normal", "400 600"),
]

RULE = ("@font-face{font-family:'%s';font-style:%s;font-weight:%s;"
        "font-display:swap;src:url(%s) format('woff2');}")


def css(url_for):
    """One rule per face, newline-joined, no trailing newline.

    The builders substitute the result straight into ``CSS`` at ``__FONTS__``,
    which already supplies the surrounding newlines.
    """
    return "\n".join(RULE % (fam, style, weight, url_for(f))
                     for f, fam, style, weight in FACES)


def data_uri(name):
    with open(os.path.join(FONT_DIR, name), "rb") as fh:
        return "data:font/woff2;base64," + base64.b64encode(fh.read()).decode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prefix", default="fonts/",
                    help="relative directory the linked build points at "
                         "(default: fonts/; use ../fonts/ from a volume subdirectory)")
    ap.add_argument("--out-dir", default=HERE)
    args = ap.parse_args()

    missing = [f for f, *_ in FACES if not os.path.exists(os.path.join(FONT_DIR, f))]
    if missing:
        raise SystemExit("missing vendored fonts in %s: %s"
                         % (os.path.normpath(FONT_DIR), ", ".join(missing)))

    for name, url_for in (("fonts.css", data_uri),
                          ("fonts-linked.css", lambda f: args.prefix + f)):
        path = os.path.join(args.out_dir, name)
        with open(path, "w") as fh:
            fh.write(css(url_for))
        print("wrote %s — %.1f KB" % (path, os.path.getsize(path) / 1024))


if __name__ == "__main__":
    main()

"""Volume III catalogue. Two plates, and they are one picture.

An illustration, and the same illustration issued as a chart. Everything the
second one adds is a cartographic signal; none of it is cartographic content.
That is the whole volume, and it is the move this project is named for.

It was drafted at five plates. Three came out on 11 August 2026 when their
provenance was established: they were collected from elsewhere, not made for
this project, and a plate archive that catalogues other people's work as its
own vision layer is lying in the rail before it gets to the reading. The two
that remain are the author's.
"""

SECTIONS = [
    dict(num="I", slug="drawn-like-cartography", title="Drawn like cartography",
         lede="A picture, and then the same picture wearing a chart. Nothing was measured "
              "before the compass rose was added and nothing was measured after. Read them "
              "in order &mdash; the whole volume is the difference between the two.",
         items=["enchanted-zombie-path", "enchanted-zombie-path-map"])
]

# Plates whose claims survive checking. None here — both plates sit on the
# Vision belt, as all fourteen of Volume I's do. Kept as a set rather than
# deleted so a later plate that earns the silver stamp has somewhere to go.
SURVEYED = set()

# slug -> (source file, title, sub, origin, marks, [reading paragraphs])
P = {}


def add(slug, src, title, sub, origin, marks, *reading, **kw):
    P[slug] = dict(src=src, title=title, sub=sub, origin=origin, marks=marks,
                   reading=list(reading), **kw)


add("enchanted-zombie-path", "zombie-path.jpeg",
    "The Procession", "Five figures in a purple wood",
    "Not supplied", None,
    "Five costumed figures walking a cobbled path out of a twilight forest, a spired castle "
    "on the ridge behind them, toadstools and violet blossom either side. Storybook "
    "illustration, competently done, making no claim whatsoever.",

    "It is here as the control. Catalogued alone it would belong in the back of Volume II "
    "with the landscapes and portraits &mdash; the work that asserts nothing and needs to "
    "assert nothing. Its whole function is to be the before.")

add("enchanted-zombie-path-map", "zombie-path-map.jpeg",
    "Castle of Eternal Night", "The same scene, issued as a chart",
    "Not supplied", None,
    "The identical procession, now mounted on aged parchment inside a ruled border, with a "
    "compass rose in the upper right and four place names lettered across it: <em>Castle of "
    "Eternal Night</em>, <em>Twilight Woods</em>, <em>Mushroom Grove</em>, and along the "
    "cobbles, <em>Enchanted Zombie Path</em>. A dashed line runs the length of the route.",

    "Every one of those additions is a cartographic signal, and not one of them carries "
    "cartographic content. The compass rose indexes no orientation &mdash; nothing in the "
    "picture is north of anything else. The dashed line is the road already visible in the "
    "painting, retraced. The place names label three things that are simply the illustration&rsquo;s "
    "background, foreground and middle distance. There is no scale, no projection, no "
    "coordinate, and nothing that would let a reader place any feature relative to any other.",

    "This is the plate this project is named for. <em>Terra Australis Incognita</em> was "
    "drawn with the same equipment &mdash; a confident coastline, a compass rose, a "
    "convincing hand &mdash; over a continent nobody had surveyed, and it was believed for "
    "roughly three centuries because it looked exactly like the charts that were right. The "
    "difference between this parchment and a map is not draughtsmanship or sincerity. It is "
    "whether anything behind the line was measured.",

    "Held against the plate above it, nothing in the picture changed. No figure moved, no "
    "light shifted, no line was redrawn. What was added was a set of conventions that a "
    "reader has been trained to take as a promise that someone went and looked. That is the "
    "entire distance between the two plates, and it is enough.")


def verify(upload_dir):
    """Fail loudly rather than publish a plate pointing at the wrong image.

    Same four checks as Volume II, plus one this volume needs: every slug in
    SURVEYED must actually be a plate, or a silver stamp gets promised to
    nothing. That check is why SURVEYED is an empty set here rather than a
    stale entry pointing at a plate that was removed.
    """
    import os
    missing, dupes = [], {}
    for slug, p in P.items():
        if not os.path.exists(os.path.join(upload_dir, p["src"])):
            missing.append((slug, p["src"]))
        dupes.setdefault(p["src"], []).append(slug)
    collided = {s: v for s, v in dupes.items() if len(v) > 1}
    listed = [i for sec in SECTIONS for i in sec["items"]]
    orphan = set(P) - set(listed)
    unlisted = [i for i in listed if i not in P]
    phantom = sorted(SURVEYED - set(P))
    return missing, collided, sorted(orphan), unlisted, phantom


if __name__ == "__main__":
    import sys
    problems = verify(sys.argv[1] if len(sys.argv) > 1 else ".")
    names = ["missing source", "two plates share a source", "defined but unlisted",
             "listed but undefined", "SURVEYED slug is not a plate"]
    bad = False
    for name, found in zip(names, problems):
        if found:
            bad = True
            print("FAIL — %s: %s" % (name, found))
    print("verify: %d plates, %d sections — %s"
          % (len(P), len(SECTIONS), "FAILED" if bad else "ok"))
    sys.exit(1 if bad else 0)

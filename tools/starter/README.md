# Starter ingredients, currently unused

These files — launchers, a doctor script, a tester's guide — were assembled
into a downloadable starter by `tools/package_clementine.py`, which has been
retired along with the companion it packaged.

They are kept rather than deleted because they are authored work, not
generated output, and because they would be most of a starter for the
companion's new home if one is ever wanted:

**https://github.com/CrystalArchitect/Clementine-ai-companion**

That repository needs far less assembly than this one did. The packager's
real job was flattening a split layout — mind under `core/`, interface under
`vision/apps/` — and rewriting a `sys.path` line to match. There, `crystalcore/`
already sits beside `clementine.py` and no such line exists. A starter for it
would be closer to "zip a directory" than to what this tool did.

Nothing builds these today. If nothing ever does, they can go.

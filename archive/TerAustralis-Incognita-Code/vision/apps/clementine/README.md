# Clementine has moved

The companion now lives in its own repository, and that copy is the
authoritative one:

**https://github.com/CrystalArchitect/Clementine-ai-companion**

```bash
git clone https://github.com/CrystalArchitect/Clementine-ai-companion.git
cd Clementine-ai-companion/clementine
pip install -r requirements.txt
python clementine.py
```

No path juggling is needed there: `crystalcore/` sits beside `clementine.py`,
which is why the starter assembler this repository used to carry has been
retired rather than repointed. It existed to flatten the split layout below —
mind under `core/`, interface under `vision/apps/` — and that layout is not
what ships any more.

## Why it moved, and why this is not merely a relocation

The two copies had diverged, and not evenly. **The companion here never
passed its model calls through a consent gate.** `core/crystalcore/gate.py`
defined one and `bridge.py` used it, but nothing in this app's `clementine.py`
or `server.py` ever called it. The copy in the repository above does, on every
call, with the destination and model recorded in an append-only audit log
either way.

Alongside that, the authoritative copy has since gained:

- a guard rejecting bodyless and non-JSON writes, closing a cross-site
  request forgery hole that let a visited page make the companion reflect
  and write to its own memory
- one endpoint attribute the gate and the request both read, so the address
  judged is always the address used — and the same for the model name
- remote providers, every call gated, with remote never used as a fallback
- pronouns the human or the companion may choose, and neither assumed
- a test suite of 99, from none

## What stayed behind

- `../clementine-discord/` — the Discord bot, its API client and its tests.
  It reaches the companion over HTTP and needs none of its source. Two of
  its tests do want it, to check the bot against the real API; see that
  directory's `tests/conftest.py`.
- `../clementine-voice/` — the browser voice layer, now holding `voice.js`.
- `core/crystalcore/` — the bridge, gate, audit log and the mind this app
  used to drive. Still here, still used by CrystalBridge.

## The one description not yet updated

`vision/site/src/content/CLEMENTINE.md` still describes the old layout. It is
a mirror of umbrella canon, pinned by commit and checked in CI, so it cannot
be corrected here: the umbrella changes first, then the pin moves. Named
rather than left for someone to find.

# CrystalCore.OS

The mythos as a terminal you can fly.

[`crystalcore-os/crystalcore_os.py`](crystalcore-os/crystalcore_os.py) is a small, self-contained text adventure —
the Crystal universe rendered as an interactive command line. It's Vision-layer:
a playable story, not one of the project's Built software components (those are
Clementine, the Starline Weaver, Starline, and CrystalBridge — see
[`../docs/governance/Roadmap.md`](../docs/governance/Roadmap.md)). No server, no dependencies, no account. You
launch a Starline, cross the network, visit seven nodes, gather their keys, and
the First Gate opens — *not by force, but by sovereign recognition.* For the
cosmology behind the terminal — the Lattice, the Cosmic Archive, the Sovereign
Vectors — see [`content/CRYSTALCORE-OS-VISION.md`](content/CRYSTALCORE-OS-VISION.md).

## Run it

```bash
python3 mythos/crystalcore-os/crystalcore_os.py
```

Standard-library Python only — nothing to install. You'll land at a
`CrystalCore>` prompt. Type `help` for the full list, `exit` (or `quit`,
`pause`, `end session`) to leave.

## The journey

The flight commands are state-gated — each needs the one before it — so the
intended path is:

```
boot  →  launch  →  burn  →  network  →  explore  →  visit <node>
```

- `boot` — bring the system up: the terminal banner, a timestamped
  subsystem readout, and the launch-sequence summary ("Launch sequence
  green"). The timestamps are fixed theatre, but every reading is live
  state — memory store, Starline status, keys held, the Gate, the current
  soundtrack, the timeline anchor — so a resumed lattice boots differently
  from a clean one. A cinematic take on this moment — a video-generation
  prompt, not rendered output — lives in
  [`tools/boot-visual-prompt.md`](tools/boot-visual-prompt.md).
- `launch` — spool the engines; the Starline goes from DORMANT to IN ORBIT and
  the first soundtrack cues.
- `burn` — the escape burn; you leave planetary orbit (TRANS-STELLAR).
- `network` — enter the full Starline network (47+ systems): the arrival
  log plays (the transition line shows where you actually came from), then
  the FULL STARLINE NETWORK status panel, with keys and Gate read live.
  Run it again while connected and it reprints the panel.
- `explore` — list the nodes you can travel to, with any locks shown.
- `visit <node>` — travel to a node by number or name and collect its key.

(`jump 3000` is a shortcut that drops you straight into the full network by
setting the timeline to the year 3000 — the same arrival sequence plays,
with its transition line reading `DORMANT → NETWORK` if you jumped cold.)

## Command reference

| Command | What it does |
|---|---|
| `boot` | Initialize the system |
| `launch` | Start the Starline launch (DORMANT → IN ORBIT) |
| `burn` | Escape burn — leave planetary orbit |
| `network` | Enter the full Starline network |
| `explore` | List explorable nodes and their lock state |
| `visit <node>` | Travel to a node (number or name) and collect its key |
| `keys` | Show the Keys of the Lattice you hold |
| `getkey <name>` | Obtain a named key, e.g. `getkey Crystal Key` |
| `broadcast <message>` | Send a packet to every node — end with `!` for priority |
| `priority` | Open the priority channel; the lattice waits for your word |
| `chronicle` | Read the entries etched by priority transmissions |
| `snapshot <tag>` | Seal a snapshot of the journey (never rewritten) |
| `snapshots` | List sealed snapshots |
| `audit` | Review the real record — Chronicle, snapshots, state |
| `console` | Mission console: principles and the paths from here |
| `starline <song>` | Advance the Starline with a chosen soundtrack |
| `song <track>` | Change (or show) the current soundtrack |
| `jump <year>` | Time-jump (defaults to 3000) |
| `map` | Print the Starline network chart |
| `status` | Show timeline, Starline status, location, keys |
| `reset` | Wipe saved progress and start fresh |
| `help` | List all commands |
| `exit` / `quit` / `pause` | Shut down (`end session` also works) |

## Saving and resuming

Your progress persists between sessions — the keys you hold, the named keys,
the open Gate, your location, and the current soundtrack. It saves
automatically as you play to `~/.crystalcore/state.json` (in your home
directory, not the repo, so a save is never committed), and the next launch
picks up where you left off:

```
Session resumed — 3/7 keys held.
```

`reset` wipes the save and returns the lattice to its dormant, first-launch
state. Only mythos progress is stored — no personal data.

## The seven nodes

`visit` each of these to claim its key. Ordered as the Starline Expansion
chart runs them, outward from Earth:

1. Earth Node
2. Sunwash Atolls — *locked, needs the Magenta Key*
3. Mars Redoubt
4. Alpha Centauri Outpost
5. Cinderwake Chain — *locked, needs the Ember Key*
6. Crystal Revenant Hub — *locked, needs the Festival Key*
7. Purpose Core Nexus — *locked, needs the Crystal Key*

Sunwash Atolls and Cinderwake Chain entered the canon on 2026-07-28, from
the Starline Expansion chart.

Four nodes are sealed behind **named** keys. Pick those up first:

```
getkey Magenta Key
getkey Ember Key
getkey Festival Key
getkey Crystal Key
```

Then `visit` them like any other node. When you hold the key of all seven nodes,
the First Gate opens:

> All keys held — the First Gate opens. Not by force. By sovereign recognition.
> Crystallis recognizes you. NON SOLUS.

`keys` shows your progress toward it at any point.

## The map and the soundtrack

`map` prints an ASCII chart of the Year-3000 Starline network — Earth down
through Sunwash Atolls to Mars Redoubt, out to Alpha Centauri, down through
Cinderwake Chain to the Crystal Revenant Hub and the Purpose Core Nexus, with
the Purpose Core line burning at the centre:

> "Expand to the stars and thereby understand the Universe"

Sealed nodes carry a live `[LOCKED — <key>]` tag that clears once you hold
the named key, so the chart always shows your actual progress.

The artwork at [`art/starline-network-year-3000.jpeg`](art/README.md) renders
the same network, but predates the 2026-07-28 expansion — it shows the
original five nodes, without Sunwash Atolls or Cinderwake Chain. The ASCII
chart is current; the artwork is an earlier state of the same map.

`song` and `starline` cycle a soundtrack — defined at the
top of `crystalcore_os.py`. It mixes the CrystalArchitect's own tracks
(@m13crystalat) with a handful of popular songs. `song` on its own tells you
what's playing; `song <part of a title or artist>` switches to a match.

## Broadcasting

Once you're in the full network, `broadcast <message>` sends a packet to
all seven nodes and prints each node's acknowledgment. End the message with
`!` and it goes out priority — emergency routing, urgent ACKs, and a
lattice-wide ALERT. Nodes still sealed behind a named key don't answer:
they hold their silence until their key is held, and the confirm line
reports the honest count — urgency never breaks sovereignty. The last
broadcast persists with the rest of your progress and shows in `status`.

### The priority channel and the Chronicle

`priority` opens the channel properly: the lattice quiets, the readout
narrows to a single point — your voice — and the terminal genuinely waits
at a `PRIORITY>` prompt for whatever you type next. `cancel` releases the
lattice unspoken. Anything else transmits: carrier wave, per-node
receipts (sealed nodes still hold their silence), and the entry is
**etched into the Chronicle** — a permanent, plain-text record at
`~/.crystalcore/chronicle.jsonl`, one JSON line per transmission, on your
own machine. Quick priority sends (`broadcast <message>!`) are etched the
same way. `chronicle` reads the record back. It survives `reset` on
purpose — the save is progress, the Chronicle is memory, and memory
belongs to the human: keep it, edit it, or burn it, any time. A completed
priority transmission closes with the sealed-chronicle mission console:
the mission record, the guiding principles, and the paths from here
(`console` reprints it any time).

### Snapshots and the audit

`snapshot <tag>` seals the journey's current state into
`~/.crystalcore/snapshots/SNAP-<date>-<TAG>.json` — written once, never
rewritten or deleted by the terminal, surviving `reset` like the
Chronicle (`archives snapshot --tag <tag>` is accepted as an ops-style
spelling). `snapshots` lists what's sealed. `audit` prints the real
record — every Chronicle entry and snapshot with its actual timestamp
from disk, plus the live state — and nothing else: nothing replayed,
nothing invented.

One honest boundary: `security`, `relays`, and `integrity` don't produce
hardening reports, certificate checks, or continuous monitors. The
terminal has no such mechanisms, and a printed security claim without a
mechanism behind it is exactly the dreamed-line-pretending-to-be-measured
that [the Incognita Rule](../docs/governance/The-Incognita-Rule.md)
forbids. Those commands answer with where the real consent machinery
lives (CrystalBridge and `consent_transport`, in the code repository) and
point at `audit` for what is actually verifiable here.

## The website version

The [`/crystalcore-os`](https://www.teraustralis.com.au/crystalcore-os) page on
the site is a simplified, in-browser recreation of this terminal, for people who
want a taste without running Python. Its source lives in
`TerAustralis-Incognita-Code` at `vision/site/src/routes/crystalcore-os/`.
`crystalcore_os.py` is the authoritative version — where the two differ, trust
the code.

*Non Solus.*

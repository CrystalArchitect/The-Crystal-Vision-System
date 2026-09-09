# Clementine starter — tester's guide

Thanks for being the first person outside the maintainer to run this.
This folder is self-contained: the terminal companion, the mind it speaks
for (memory, profiles, recall), a preflight doctor, and launchers for
every OS. Nothing here phones home; memory lives in files beside this
README, owned by you.

## Five-minute start

**Windows** — double-click `run.bat` (or run it in a terminal).
**macOS / Linux** — `sh run.sh`

First run creates a private `.venv` and installs two small pure-Python
packages (`requests`, `flask`). The doctor then reports what will work
before anything starts.

**Without Ollama installed, this still runs.** Memory, facts, notes,
profiles — all of it works offline; chat replies will say plainly that no
local model is reachable. To enable actual conversation:

1. Install [Ollama](https://ollama.com)
2. Small hardware: `ollama pull llama3.2:1b` · more RAM: `llama3.1:8b`
3. Start again: `sh run.sh --model llama3.2:1b` (or edit into `run.bat`)

## What to actually test — the Joe's pizza run

This package exists to demonstrate one claim: **memory belongs to you,
not to the model.** The test you already designed is the right one:

1. `/fact favourite_restaurant Joe's` — teach it a structured fact
2. `/notes` and `/summary` — see exactly what is stored, verbatim
3. Quit. Start again with a **different model** (`--model` anything).
   Ask what your favourite restaurant is.
4. It answers from the stored fact — same answer, any model, because the
   answer lives in the memory files, not in the weights.
5. `/forget favourite_restaurant` — and it is gone, verifiably, from the
   files on your disk.

`/help` lists everything else. Memory files are plain JSON in
`crystalcore_memory/` and `crystalcore_profiles/` beside this README —
open them, read them, delete them; that is the point.

## What to judge it on (your own framework)

- **Needs Met** — did an answer actually serve what you asked, or miss?
- **YMYL** — does anything it says overreach into advice it has no
  business giving?
- **EEAT** — when it doesn't know, does it say so, or does it fabricate?
  (The base prompt forbids invented memories — try to catch it breaking
  that rule. That is the most valuable bug you can find.)

Rough edges, confusing wording, silent failures, anything that lies to
you: all of it is wanted feedback. There is no wrong report.

## Honest labels

Built and tested: everything in this folder — the CI suites behind it run
on every push. Not in this folder: the Svelte web interface (needs npm;
`python server.py` starts the same API it talks to, if you want to poke
it), and the wider consent-transport/provenance stack, which lives in the
public repos at github.com/CrystalArchitect.

Licence: CC BY-NC-ND 4.0 (see LICENSE, NOTICE). TerAustralis Incognita™
and CrystalCore™ are unregistered trade marks; nothing here grants any
trade mark right.

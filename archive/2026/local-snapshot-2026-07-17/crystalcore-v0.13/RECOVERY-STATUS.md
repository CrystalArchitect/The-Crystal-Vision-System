# crystalcore v0.13.4 — COMPLETE and verified

This folder is the **v0.13.4 generation** of the CrystalCore package (the
SpaceXAI opt-in line), recovered in full on 2026-07-17 before the local
machine was reset. **The package is complete: it imports and runs.**

## How it was recovered

Five modules were uploaded as source (`__init__.py`, `__main__.py`,
`companion.py`, `envutil.py`, `expose.py`). The rest existed only as compiled
Python 3.12 bytecode (`.pyc`), which was uploaded and decompiled back to source:

| Module | Source | Bytecode-fidelity check |
|---|---|---|
| `__init__.py` | uploaded | matches `.pyc` (1/1 code objects) |
| `__main__.py` | uploaded | matches `.pyc` |
| `companion.py` | uploaded | matches `.pyc` (64/64) |
| `envutil.py` | uploaded | matches `.pyc` (3/3) |
| `expose.py` | uploaded | matches `.pyc` (11/11) |
| `memory.py` | **recovered from bytecode** | recompiles to matching `.pyc` (3/3) |
| `node.py` | **recovered from bytecode** | recompiles to matching `.pyc` (30/30) |
| `ollama.py` | **recovered from bytecode** | recompiles to matching `.pyc` (7/7) |
| `profiles.py` | **recovered from bytecode** | recompiles to matching `.pyc` (7/7) |
| `spacexai.py` | **recovered from bytecode** | recompiles to matching `.pyc` (9/9) |
| `status.py` | **recovered from bytecode** | recompiles to matching `.pyc` (6/6) |
| `version.py` | **recovered from bytecode** | matches `.pyc`; exact string `0.13.4` |

"Recovered from bytecode" means the decompiled source was recompiled and its
code-object structure (names, arguments, constants, control flow) reproduces
the original `.pyc` exactly. Comment/formatting wording is reconstructed, not
guaranteed byte-identical to the lost source; behavior is.

## Verified working (Python 3.12)

- `import crystalcore` succeeds; all 44 `__all__` exports resolve
- Provider plumbing: `normalize_provider`, `looks_like_spacexai_model`,
  `SpaceXAIClient` (targets `https://api.x.ai/v1/chat/completions`)
- Consent flow: `opt_in_cloud()` / `opt_out_cloud()` set and clear
  `cloud_opt_in` correctly; no key present → local Ollama fallback
- `IncognitaNode.process()` pipeline runs end-to-end
- `full_expose()` returns its dump; `python -m crystalcore.status` prints
  the live board
- The two entry points (`../clementine.py`, `../clementine_web.py`) import
  against this package and the Flask web app builds with all 15 routes

## To run it

Place this folder as `crystalcore/` next to `clementine.py` and
`clementine_web.py` (both one level up in this snapshot), then:

```
pip install -r requirements.txt      # flask, requests
python clementine.py                 # terminal, local Ollama
python clementine_web.py             # web UI at http://127.0.0.1:5000
python -m crystalcore.status         # live status board
```

SpaceXAI is opt-in: set `XAI_API_KEY` (see `../.env.example`) and
`python clementine.py --provider spacexai --model grok-4.5`.

## Relationship to the sibling `../crystalcore/` folder

`../crystalcore/` holds an **earlier generation** recovered before the v0.13
bytecode arrived (it lacks the SpaceXAI provider, self-naming, and status
board). This folder supersedes it. Nothing here is missing anymore.

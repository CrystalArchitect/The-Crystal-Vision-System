# Local Machine Snapshot — 2026-07-17

This folder preserves the files uploaded from the CrystalArchitect's local Windows
machine on 2026-07-17, before that machine was returned. It is a **snapshot for
safekeeping**, kept separate from the repository's main structure so nothing in the
existing site or `clementine/` package is overwritten. Merging the two lines of
development is future work.

## What is here

| Folder / file | Contents |
|---|---|
| `README.md`, `CLEMENTINE.md`, `GOVERNANCE.md`, `MILESTONES.md`, `BRIDGE.md` | Updated docs from the local **CrystalCore v0.13.x** line (SpaceXAI opt-in provider, voice) |
| `clementine.py` | Terminal companion, v0.13.x — adds `/provider`, `/optin`, `/optout`, `/expose`, multi-line paste handling |
| `clementine_web.py` | Single-file local web UI, v0.13.x — on-device voice (speech synthesis + mic), provider picker, transparency endpoints (`/api/expose`, `/api/conversation`, `/api/prompt`) |
| `crystalcore/` | **Complete, working package** (see recovery notes below): `__init__.py`, `__main__.py`, `companion.py`, `memory.py`, `expose.py`, `node.py`, `ollama.py`, `version.py`, `profiles.py` |
| `site/` | Updated static site for teraustralis.com.au (index, crystalcore, codex, apocryphon, clementine pages + CSS + CNAME) |
| `seven-sisters/` | The Seven Sisters Songline documents and CrystalCore protocol pack (manuals, path logs, water brief, transmit pack, landing page) |
| `.env.example` | Template for the SpaceXAI opt-in key (`XAI_API_KEY`). **Never commit a real `.env`.** |
| `Start*.bat` | Windows launchers (local Ollama, web UI, SpaceXAI mode) |
| `_clean_memory.py` | One-shot local memory cleanup utility |

## Recovery notes (2026-07-17, after the initial snapshot)

The four missing modules of the `crystalcore/` package were recovered or
reconstructed, and the package now **imports and runs** (verified on Python 3.12:
all 32 `__all__` exports resolve; the node pipeline and `full_expose()` were
exercised end-to-end). The uploaded `.pyc` bytecode files were confirmed to match
the uploaded sources exactly, which pins this package generation precisely.

| File | Provenance | Fidelity |
|---|---|---|
| `node.py` | **Recovered from `node.cpython312.pyc` bytecode** | Verified faithful: recompiling it reproduces all 30 code objects of the original bytecode (names, signatures, constants, logic) |
| `ollama.py` | **Reconstructed** from the pre-refactor HTTP code in `clementine/crystalcore/companion.py` + the exact interface required by the recovered modules | Behavior-accurate; comment wording not original |
| `version.py` | **Reconstructed** — original left no trace | Version string `0.12.0` is a placeholder; exact number unrecoverable |
| `profiles.py` | Copied from `clementine/crystalcore/profiles.py` (this repository) | Exports exactly match what `__init__.py` imports |

## Still missing (v0.13.x generation only)

The newer v0.13.x entry points (`clementine.py`, `clementine_web.py`) additionally
reference code that left no bytecode and cannot be recovered:

- `crystalcore/status.py`
- the SpaceXAI provider module (and `load_dotenv` / `xai_api_key_present` helpers)
- `tests/` (including `tests/test_provider.py`)
- `cli/crystalcore.ps1` (referenced by the protocol pack)

So: the `crystalcore/` package here is whole and functional; the v0.13.x
`clementine.py` / `clementine_web.py` will not import until the provider layer is
recovered from the original machine or a backup — or reimplemented.

## Relationship to the rest of the repository

The repository's `clementine/` package is a **diverged sibling** of this snapshot:
it has the self-naming feature (v12) and the Svelte web interface (`server.py` +
`webapp/`), which this local line does not; this local line has SpaceXAI opt-in,
voice, and the expose/transparency layer, which the repository does not. Neither
supersedes the other yet.

Deliberately **excluded** from this snapshot: real credentials (`.env` with a live
key, Grok CLI `auth.json`), private Grok CLI session data (chat history, event logs,
telemetry), Python bytecode, and machine-local editor/permission settings.

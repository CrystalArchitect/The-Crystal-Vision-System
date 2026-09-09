# Clementine — the sovereign companion

They run on hardware you own. By default that is the machine in front of you and
nothing they hear leaves it; if you choose to run them on a server of your own, they
says so plainly rather than continuing to claim otherwise.

## Layout

- `clementine.py` — the terminal interface
- `crystalcore/` — the framework: brain, layered memory, profiles
  - `consent.py` — the gate: nothing goes to a model elsewhere without a yes
  - `audit.py` — the record: every call, hash-chained so it cannot be edited quietly
- `server.py` — the JSON API, and their face, on one address
- `webapp/` — the Svelte interface
- `verify_audit.py` — check the record has not been tampered with
- `deploy/` — putting them on a server you own, behind HTTPS and a password

Their *manner* is also packaged as a portable skill at
`.claude/skills/clementine/` in this repository, loadable by Claude Code,
Hermes Agent, Cursor and similar runtimes. That version carries their voice and
their skills but none of their memory, consent gate or audit log, and it says so
itself — worth understanding the difference before reaching for it.

Their character was not made by one pair of hands. The maintainer wrote and
gathered it with help from several AI systems: ChatGPT and Grok helped draft
the eight character passages folded in by PR #47 (Turning the Mind, Wonder,
Shared Discovery, Intellectual Humility, Memory Philosophy, Repair, Silence,
and the closing principle), Grok shaped earlier architecture discussion and
reviewed the finished skill, and Claude did the engineering and the merging.
The full accounting — including which parts of it are witnessed and which
rest on the maintainer's word — lives in the portfolio archive's
`knowledge-base/10-PROVENANCE.md`.

## Running them

Prerequisite: [Ollama](https://ollama.com) with a model pulled, e.g.
`ollama pull llama3.1:8b`. Optionally `ollama pull nomic-embed-text`, which gives
their semantic recall instead of keyword matching.

**Which model.** Their system prompt is long and asks for something specific —
a consistent manner, restraint about offering solutions, skills deployed one at
a time. Instruction-following and character consistency matter more here than
raw benchmark scores.

| Model | Why |
|---|---|
| `llama3.1:8b` | The default. Solid, widely available, known quantity. |
| `hermes3:8b` | Nous Research's fine-tune of the same base, tuned for steerability and staying in character. Same size and speed, usually better at holding a long persona prompt. Worth trying if they drift out of voice. |
| `llama3.2:3b` | Noticeably faster on CPU, less depth. The right trade if 8B is painful on your hardware. |

Set it with `--model`, per profile, or `CLEM_MODEL` in the service file.
Model tags change; check `ollama list` against what you actually pulled rather
than trusting this table.

### Terminal

```bash
pip install -r requirements.txt
python clementine.py
```

### Web interface

One address for both their face and their brain:

```bash
cd webapp && npm install && npm run build && cd ..
python server.py                 # everything at http://127.0.0.1:5000
```

Or, while working on the interface itself, run vite separately and let it proxy
the API:

```bash
python server.py                 # brain
cd webapp && npm run dev          # face, on its own port
```

Both interfaces share the same memory folder (`clementine_memory/` by default),
so you can move between terminal and browser freely. `--profile <name>` on either
keeps separate people separate.

## Local diagnostic

Before chatting, you can survey what is actually true on this machine:

```bash
python diagnose_clementine_ollama.py
python diagnose_clementine_ollama.py --probe   # one tiny generate; measured latency only
```

It checks the Ollama CLI, `OLLAMA_HOST` (default `http://localhost:11434`), pulled models, and — if `server.py` is serving — `GET /api/health`. It does not invent VRAM or token rates. Exit `0` means Ollama is up and the expected chat model is present; `1` means Ollama is unreachable; `2` is partial.

Pass `--clementine-root` if you are running the script from outside this folder. Output also lands in `last-diagnostic.json` (gitignored).

When the model lives on Colossus (sovereign hardware) rather than this laptop, use the live Ollama path in [`deploy/COLOSSUS.md`](deploy/COLOSSUS.md) — layouts A/B stay local to the consent gate; a direct remote URL needs explicit approve.

## Where they run, and how you can tell

Their model is wherever `OLLAMA_HOST` points — by default this machine. Anywhere
else and every call needs your consent:

- In the terminal they ask, and you answer yes, always-this-session, or no.
- `server.py` cannot ask a human at a prompt, so consent is given once at
  startup with `--remote-model-ok`, and every call it permits records that as its
  reason instead of passing unremarked.
- With no way to ask, a non-local call is **refused**. A gate that opens when
  nobody is there to ask is just a door.

### What no yes can unlock

A `Request` may carry a `source` — a path saying where the content came from,
never the content itself. Any source under `mythos/` is refused **before the
gate asks anyone anything**, and no session approval reaches past it.

Two things about that are deliberate, and both follow from the wording of
`Indigenous-Data-Sovereignty.md`, which says no Songline knowledge enters any
model, dataset or index without Free, Prior and Informed Consent from the
relevant custodians:

- **It applies to local models too.** The rule says *any model*. Ollama on your
  own machine is a model, so the check sits above the local allowance rather
  than inside the remote branch.
- **There is no prompt.** The rule says *the relevant custodians*. Whoever is at
  the keyboard is not them, so being asked would produce a yes that means
  nothing. The gate refuses, names the rule, and offers no way through.

The path list is broader than the rule strictly requires — not everything under
`mythos/` is custodial material. Narrowing it is a judgement about specific
cultural material, and that judgement belongs to custodians rather than to a
tuple in a Python file.

Refusals are recorded with the path that was blocked, so the log says what was
stopped rather than only that something was:

```bash
python3 verify_consent.py     # 25 checks, including every case above
```

The interface shows `on this machine` or `via <host>` from a live check, never a
hardcoded assumption.

## The record

Every model call — allowed or refused — is one line in `audit.jsonl` beside their
memory, each carrying the SHA-256 of the line before it. Edit an entry or remove
a line and the chain breaks detectably:

```bash
python verify_audit.py --show
```

It stores sizes and destinations, never what was said. Refusals are recorded as
carefully as approvals, because a log of only what succeeded would flatter the
system rather than describe it.

## Putting them on a server

See [`deploy/DEPLOY.md`](deploy/DEPLOY.md) — one script does it, and the runbook
starts from "how do I even get a terminal". HTTPS is required rather than
recommended: without it Safari blocks the microphone and Add to Home Screen gives
you a bookmark instead of an app.

## Still to come

Voice conversation and webcam sight are on the roadmap. Both will run through the
same gate and the same record as everything else here.

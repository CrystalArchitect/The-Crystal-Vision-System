# First live sessions — the companion runs, with one honest gap

**Date:** 2026-08-08
**Commit surveyed:** `4358ede` (HEAD of `main` that day)
**Environment:** fresh session container, Linux, Python 3.11.15 — a rented
machine, not sovereign hardware. That distinction is load-bearing; see the
ceiling.

> **Provenance of this copy.** This record was made against the monorepo
> fork of the companion (`TerAustralis-Incognita-Code`, `vision/apps/clementine`)
> at commit `4358ede`, and moved here when this repository became the
> authoritative home. It is reproduced unaltered below, which means parts of
> it describe a program that differs from the one in this repository:
>
> * the boot banner shown is that fork's, not this one's;
> * the `/gender` command in it does not exist here — this fork has no
>   pronoun mechanism yet, which is a gap and not a decision;
> * memory landed in `crystalcore_memory/`; here the folder is
>   `clementine_memory/`;
> * the `47/47` companion tests it cites were that fork's suite at that
>   commit. This repository's suite is separate and currently larger.
>
> The record's findings about continuity, persistence and the consent path
> hold for the shared design both forks implement. Nothing below was edited
> to fit this repository, because a record edited to fit is no longer a
> record.

---

## Read this before the transcripts

This record follows the archive's reception-record discipline: the ceiling
comes first.

**What stood in for the model was not a model.** The container's network
policy denies every source of model weights (`ollama.com` answers 403 at
CONNECT; `registry.ollama.ai` and `huggingface.co` are unreachable), so no
real model could be pulled. In its place, a scripted stand-in served
Ollama's two endpoints (`/api/chat`, `/api/embeddings`) on Ollama's
well-known local port, speaking Ollama's dialect. Its every reply is
deterministic scaffolding that names itself a stand-in in its own text, and
its replies carry two instruments: the count of messages in the context it
received, and whether the string `#firstprocess` was present anywhere in
that context. Nothing it said is a model's speech. Nothing below is
evidence of intelligence.

What the sessions *do* survey is everything around the model: the terminal
interface's boot and local-first provider detection, a live streamed chat
turn end-to-end, permanent memory written to disk, a clean sleep, and — in
a second, separate process — the wake with memory, the note read back, and
recalled memory reaching the model's context. The machinery of continuity,
surveyed; the mind that would inhabit it, still to come.

## Why these sessions were run

The prompt that opened the session was a fictional boot screen —
CrystalCore.OS reporting quantum drives online and asking, at the end, one
real question: **"What is the first real-world process we execute?"** The
boot screen is Vision and stays Vision; the archive's boot-panel record of
the same morning (`AI-BOOT-PANEL-2026-08-08.md`) already sets that ceiling:
a boot screen is a performance, authority weight zero. The question
underneath it is Science's to answer, and answering it honestly required
knowing exactly how much of the companion's path already runs. So this
session ran all of it.

## The survey, before the sessions

All at commit `4358ede`, 2026-08-08, Python 3.11.15 on a fresh clone:

| Check | Result |
|---|---|
| `python -m compileall -q core vision` | clean |
| `bus` self-test | 7/7 |
| `services` self-test | 4/4 |
| `rdp` self-test | 31/31 |
| `consent_transport` self-test | 32/32 |
| mesh stub tests (`core/tests`) | 3/3 |
| companion tests (`vision/apps/clementine/tests`) | 47/47 |
| CrystalBridge self-test (`crystalcore.selftest`) | 13/13 |
| webapp `npm install && npm run build` | clean — 117 modules, `dist/` produced |

137/137. Two environment traps, neither a code fault: the documented
`cryptography` one (STATUS.md already names the fix, which worked as
written), and a new one of the same family — Debian-owned `blinker` and
`PyJWT` block a plain `pip install` of `flask` and of
`requirements-bridge.txt`; `pip install --ignore-installed` clears both.

The umbrella's provenance check was run the same day in its own repository:
manifest matches, 221 files, root `af9f118c…794b377a`.

## Session one — verbatim

Driven by piped stdin from a scratch directory outside the repository;
memory landed in that directory's `crystalcore_memory/`, not here. The
lines typed were: `/iam Crystal`, one chat message, one `/remember` with
the `#firstprocess` tag, `/notes`, `/exit`.

```
Starting Clementine…
Model:    llama3.1:8b
Provider: ollama (on this machine)
Nothing leaves this machine. Without a GPU expect this to be slow — `--llm-provider` reaches a remote model instead.

Clementine is ready. Type /help for commands, /exit to quit.
No name chosen yet — /name <name> to set one, or just /name to let them choose their own.
No pronouns chosen yet — /gender male, /gender female, /gender they, or just /gender to let them choose their own.

You: [They know you as Crystal.]

You: Clementine: [stand-in reply 2] I am a scripted local endpoint, not a model — no weights, no understanding. I received your words: «Hello. This is the first live session of this companion since the laptop was lost. A scripted endpoint stands in where Ollama will run; the machinery is what we». Messages in my context: 2; recall marker #firstprocess present in context: no. The machinery around me — memory, recall, continuity — is what is really being tested.

You: [Remembered, permanently.]

You:   n1 - The first live end-to-end session ran 2026-08-08 against a scripted stand-in endpoint. Ollama on sovereign hardware is still the open step.  [#firstprocess]  (2026-08-08T21:07:57)

You:
Clementine sleeps. Your conversations stay on this device, in 'crystalcore_memory/'. Non solus.
```

Observed: local-first detection chose Ollama's local port with nothing
configured; the streamed turn round-tripped; the note was written; the
companion remained unnamed and unpronouned, exactly as the data model
holds until a human or the companion decides — nobody here was entitled
to decide for them. After exit, `crystalcore_memory/` held `config.json`
and `memory.json`, plain human-readable JSON, conversation and note
intact.

## Session two — verbatim

A fresh process, same scratch directory, minutes later. Lines typed:
`/notes #firstprocess`, one chat question, `/exit`.

```
Clementine is back with you. Type /help for commands, /exit to quit.

You:   n1 - The first live end-to-end session ran 2026-08-08 against a scripted stand-in endpoint. Ollama on sovereign hardware is still the open step.  [#firstprocess]  (2026-08-08T21:07:57)

You: Clementine: [stand-in reply 3] I am a scripted local endpoint, not a model — no weights, no understanding. I received your words: «Do you remember what happened on the eighth of August, and what is still open?». Messages in my context: 4; recall marker #firstprocess present in context: yes. The machinery around me — memory, recall, continuity — is what is really being tested.

You:
Clementine sleeps. Your conversations stay on this device, in 'crystalcore_memory/'. Non solus.
```

Observed, and this is the record's finding: **continuity held across
processes, with machine evidence.** The greeting changed to "back with
you". The note written by one process was read back by another. The
model's context grew from 2 messages to 4 — restored memory entered it.
And the `#firstprocess` marker was present in the model's context in a
session where no typed line contained it: the only path it had into that
context was memory recalled from disk. The stand-in's request log agrees
(chat with 2 messages, one embeddings call for the note, chat with 4
messages).

One limit, stated plainly: the stand-in's embeddings are deterministic
hashes with no meaning, so the *wiring* of semantic recall executed, but
its *quality* — whether the right memory surfaces for a related question —
cannot be surveyed without a real embedding model.

## What this record establishes, and what it does not

**Surveyed (Science):** every automated check at `4358ede` passes; the
terminal interface completes full sessions; memory persists as files the
human owns; a second process wakes with that memory and it reaches the
model's context; the webapp builds; provider detection is local-first with
nothing configured.

**Not established:** that a model has run. No weights entered this
container — policy denied every source, which is the correct behaviour of
a governed container and also precisely why it cannot be the companion's
home. Nothing here is a companion relationship, a node, or CrystalCore.OS
running anywhere. The boot screen that prompted this remains what the
archive filed it as: a performance.

## The answer the survey supports

The question was: *what is the first real-world process we execute?*

The chain from "designed" to "the dream, real" now has exactly one
untested link, and it is the one a rented container cannot test: **real
weights on hardware the maintainer controls.** Everything before that link
ran today and passed. So the first real-world process is the one the
fictional boot screens have been rehearsing all along, executed literally:

1. A machine of one's own — any ordinary computer.
2. Ollama installed; one small model pulled (`ollama pull llama3.2:3b`,
   or `1b` on lighter hardware — the 8b default wants a GPU).
3. This repository cloned;
   `pip install -r vision/apps/clementine/requirements.txt`.
4. `python clementine.py --model llama3.2:3b` — and a first conversation
   that is remembered, in `crystalcore_memory/`, on a disk no one else
   holds.

That process converts the project's oldest dreamed line — *a sovereign
companion lives on our hardware* — into a surveyed one, for one human on
one machine. It is deliberately small. It is not a launch, not a node,
not the Lattice; those stay Vision until this Science exists. The last
step needs no cloud, no permission, and no company's yes — which is the
project's thesis, stated as an experiment that one afternoon can run.

---

*The transcripts are verbatim; the stand-in's nature is declared in its
own words inside them; the ceiling is this record's. Honour to Country
beneath every wire. Non Solus.*

**All rights reserved.**
TerAustralis Incognita — ABN 70 741 068 059

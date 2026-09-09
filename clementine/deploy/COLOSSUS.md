# Colossus — live Ollama path for Clementine

Runbook for when the model lives on **Colossus** (sovereign hardware you control),
not on a laptop. Clementine still talks to Ollama the same way; only where
`OLLAMA_HOST` points changes.

Fill in placeholders yourself — this file invents none:

- `COLOSSUS_HOST` — how you reach the machine (hostname or IP you already use)
- `USER` — your login on that machine
- How Ollama is supervised there (systemd unit, user service, tmux, bare
  `ollama serve` — whatever you actually run)
- Whether your habit is layout **A** (shell on Colossus) or **B** (SSH tunnel)

Related: [`../diagnose_clementine_ollama.py`](../diagnose_clementine_ollama.py)
surveys what is true right now; [`DEPLOY.md`](DEPLOY.md) is the phone / HTTPS
path once a brain is healthy somewhere.

---

## What local means

The consent gate treats `localhost`, `127.0.0.1`, and `::1` as **local**. A
remote URL needs an explicit yes (terminal prompt, or `--remote-model-ok` on
`server.py`). A tunnel that lands on loopback still counts as local to the gate.

| Layout | Where you run | `OLLAMA_HOST` | Gate |
|--------|---------------|---------------|------|
| **A** | Shell **on** Colossus | default (`http://localhost:11434`) | local |
| **B** | Laptop via SSH tunnel `-L 11434` | `http://127.0.0.1:11434` | still local |
| **C** | Laptop, direct remote URL | `http://COLOSSUS_HOST:11434` | needs approve / `--remote-model-ok` |

Prefer **A** or **B**. Do **not** expose Ollama's `:11434` on a public interface.

---

## 1. On Colossus — Ollama up, model present

On the machine (replace supervision with whatever you use):

```sh
ollama serve
# in another session, or after the service is up:
ollama pull llama3.1:8b
# optional embeddings:
ollama pull nomic-embed-text

curl -s http://127.0.0.1:11434/api/tags
```

`tags` should list `llama3.1:8b` (and `nomic-embed-text` if you pulled it). Leave
Ollama bound to loopback unless you have a deliberate, firewalled reason not to.

---

## 2. Survey — diagnose what is actually true

From a checkout that includes this tree (on Colossus for **A**, or on the laptop
once the tunnel is up for **B**):

```sh
cd /path/to/clementine   # the clementine/ folder in this repo
git pull
python3 diagnose_clementine_ollama.py --probe
```

Exit codes:

| Code | Meaning |
|------|---------|
| `0` | Ollama reachable and the expected chat model is present |
| `1` | Ollama unreachable |
| `2` | Partial (up, but model missing, health odd, or probe soft-failed) |

The probe does one tiny generate and reports **measured latency only** — it does
not invent VRAM or token rates. JSON also lands in `last-diagnostic.json`
(gitignored). Pass `--clementine-root` if you run the script from outside this
folder.

---

## 3. Tunnel (layout B)

On the laptop:

```sh
ssh -N -L 11434:127.0.0.1:11434 USER@COLOSSUS_HOST
```

In another terminal:

```sh
export OLLAMA_HOST=http://127.0.0.1:11434
cd /path/to/clementine
python3 diagnose_clementine_ollama.py --probe
```

The gate still sees loopback, so no remote-model consent is required for this
path. Keep the SSH session up for as long as you need the port.

---

## 4. Direct remote approve (layout C)

Only if you intentionally point at Colossus by URL instead of tunnelling:

```sh
export OLLAMA_HOST=http://COLOSSUS_HOST:11434
```

- **Terminal / REPL:** they ask; answer yes, always-this-session, or no.
- **`server.py`:** cannot ask a human at a prompt — pass `--remote-model-ok` at
  startup. Without it, a non-local host is **refused** and the refusal is
  audited.

Prefer A or B over opening `:11434` to the network.

---

## 5. Optional — run `server.py` on Colossus

After Ollama is healthy and the diagnostic exits `0`:

```sh
# on Colossus, with OLLAMA_HOST local (layout A)
python3 server.py
# or, if something else must point remotely and you consent:
# python3 server.py --remote-model-ok
```

Check:

```sh
curl -s http://127.0.0.1:8080/api/health
```

Expect a JSON health payload that agrees Ollama is up and the chat model is
known (exact fields follow whatever this checkout's `server.py` returns). For
reaching the phone UI over HTTPS and a password, follow [`DEPLOY.md`](DEPLOY.md)
— that path is about the face on a server you own, not about where the weights
sit.

---

## Done when

- [ ] `curl …/api/tags` lists the chat model (`llama3.1:8b` or your `CLEM_MODEL`)
- [ ] `python3 diagnose_clementine_ollama.py --probe` exits `0`
- [ ] Optional: `GET /api/health` on `server.py` agrees with the survey

Placeholders still to fill in your notes: `COLOSSUS_HOST`, `USER`, how Ollama is
supervised on that box, and whether you default to **A** or **B**.

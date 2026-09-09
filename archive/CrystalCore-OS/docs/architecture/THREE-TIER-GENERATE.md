# Three-Tier `/generate` — Architecture

**Status:** local + cloud tiers **Built** (code + tests in `backend/`, this
session). WebLLM tier **Vision** (reference client below, not wired into any
UI in this repo). Cloud tier not exercised against a live `ANTHROPIC_API_KEY`
in this session — no network access here to verify a real call; the cascade
and error paths are unit-tested with the API mocked.

Endpoint: `POST /api/v1/admin/generate` in `backend/app/api/v1/routes/admin.py`.
Cascade logic: `backend/app/core/llm.py`.

## 1. Goal

One completion endpoint, three ways to fill it, ordered cheapest/most-private
first and falling back only when a tier genuinely can't serve the request —
never because a working tier is merely slow:

```
   1. webllm            2. local                3. cloud
   (client browser) --> (this machine's      --> (hosted Claude
                         llama.cpp model)         API)

   $0, private,          $0, private,             $, leaves this
   client hardware        server hardware          machine
   only                   only
```

Each tier down the list costs more (money, or leaving the machine) in
exchange for capability the tier above it doesn't have (a browser without
WebGPU, a server without the model downloaded yet). No tier should be reached
for a request the tier above it could have handled.

## 2. Why the split is client/local/cloud, not three server tiers

**WebLLM (tier 1)** runs [`@mlc-ai/web-llm`](https://github.com/mlc-ai/web-llm)
in the caller's own browser via WebGPU. It never makes a network request to
this backend at all when it succeeds — that's the point: zero server load,
zero latency to a server, and the prompt never leaves the user's machine.
Because of that, tier 1 isn't code this backend can implement; it's a
contract the *client* honors before ever calling `/generate`. This repo
documents the reference client (below) but doesn't ship a frontend that uses
it — CrystalCore.OS's `index.html` is the unrelated OS-desktop demo, not an
admin-panel frontend, so there's nowhere in this repo to wire it in yet. That
is a real gap, not a hidden one: labeled **Vision** above, and again where it
matters below.

**Local (tier 2)** and **cloud (tier 3)** are both server-side, which is why
`app/core/llm.py` only implements two functions plus a cascade — `generate_local()`
(pre-existing, this session only renamed it from `generate()`) and
`generate_cloud()` (new). The endpoint accepts a `tier` value of `"webllm"`
distinct from `"local"`/`"cloud"`/`"auto"` purely so a client that already
tried tier 1 and failed can say so (useful for server-side logs/metrics
distinguishing "never tried WebLLM" from "WebLLM tried and failed") — the
cascade behavior for `"webllm"` and `"auto"` is identical, because by the time
a request reaches this server, tier 1 has already either succeeded (no
request sent) or is off the table.

## 3. Request/response contract

`backend/app/schemas/generate.py`:

```python
class GenerateRequest(BaseModel):
    prompt: str                                    # 1-4000 chars
    max_tokens: int = 256                          # 1-2048
    temperature: float = 0.7                       # 0.0-2.0
    tier: Literal["auto", "webllm", "local", "cloud"] = "auto"

class GenerateResponse(BaseModel):
    completion: str
    tier_used: Literal["local", "cloud"]           # never "webllm" -- if
                                                     # WebLLM served the
                                                     # request, this endpoint
                                                     # was never called
```

- `tier: "auto"` / `"webllm"` — try local; on `ModelNotAvailableError`
  (model file not downloaded), fall back to cloud. Any other local failure
  (a real inference error) is **not** caught here and surfaces as a 500 —
  masking a live bug behind a silent cloud fallback would hide the real
  problem, not fix it.
- `tier: "local"` — local only, no fallback. 503 if the model isn't
  downloaded.
- `tier: "cloud"` — cloud only, no fallback. 503 if `ANTHROPIC_API_KEY` isn't
  set.
- Both tiers unavailable under `"auto"`/`"webllm"` — 503 with both failure
  reasons in the message (`AllTiersUnavailableError`), not just the first
  one, since either could be the fix a caller needs to make.

## 4. Sequence

```
Client                          This server                    Anthropic API
  |                                   |                               |
  |-- try WebLLM in-browser --------->|  (never happens, tier 1       |
  |   (WebGPU present, model          |   is entirely client-side)    |
  |   loads, generation OK)           |                               |
  |<------------ done ----------------|                               |
  |                                   |                               |
  |  (WebGPU absent, or model         |                               |
  |   load/generation fails)          |                               |
  |                                   |                               |
  |-- POST /generate {tier:"webllm"}->|                               |
  |                                   |-- generate_local() ---------->|
  |                                   |   (llama.cpp, in-process)     |
  |                                   |<-- completion -----------------|
  |<-- 200 {completion, "local"} -----|                               |
  |                                   |                               |
  |            -- OR, if local model file missing --                 |
  |                                   |                               |
  |                                   |-- generate_local() raises     |
  |                                   |   ModelNotAvailableError       |
  |                                   |-- generate_cloud() ---------->|
  |                                   |   messages.create(...)        |
  |                                   |<----------- completion --------|
  |<-- 200 {completion, "cloud"} -----|                               |
  |                                   |                               |
  |            -- OR, if cloud also not configured --                |
  |<-- 503 {error: "local tier       -|                               |
  |     unavailable (...); cloud     |                               |
  |     tier unavailable (...)"}     |                               |
```

## 5. WebLLM reference client (tier 1, not wired into any UI here)

This is a reference for whoever builds the admin-panel frontend this backend
is for — it lives only in this doc, not as a runnable file in this repo, and
is untested (**Vision**). It assumes `@mlc-ai/web-llm` from a CDN or bundler;
adjust the model id to whatever WebLLM build you ship.

```js
// webllm-client.js (reference only -- not wired into any page in this repo)
import * as webllm from "@mlc-ai/web-llm";

let engine = null;

async function tryWebLLM(prompt, { maxTokens = 256, temperature = 0.7 } = {}) {
  if (!navigator.gpu) {
    return null; // no WebGPU -- caller falls through to the backend
  }
  try {
    if (!engine) {
      engine = await webllm.CreateMLCEngine("Qwen2.5-3B-Instruct-q4f16_1-MLC");
    }
    const reply = await engine.chat.completions.create({
      messages: [{ role: "user", content: prompt }],
      max_tokens: maxTokens,
      temperature,
    });
    return reply.choices[0].message.content;
  } catch (err) {
    console.warn("WebLLM tier failed, falling back to backend:", err);
    return null;
  }
}

export async function generate(prompt, opts = {}) {
  const webllmResult = await tryWebLLM(prompt, opts);
  if (webllmResult !== null) {
    return { completion: webllmResult, tierUsed: "webllm" };
  }

  // Tier 1 unavailable or failed -- ask the backend to cascade local -> cloud.
  const resp = await fetch("/api/v1/admin/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify({ prompt, tier: "webllm", ...opts }),
  });
  if (!resp.ok) {
    throw new Error((await resp.json()).error);
  }
  const { completion, tier_used } = await resp.json();
  return { completion, tierUsed: tier_used };
}
```

## 6. Configuration

`backend/app/core/config.py` / `.env`:

| Setting | Tier | Default | Notes |
|---|---|---|---|
| `LLM_MODEL_PATH` | local | `models/qwen2.5-3b-instruct-q4_k_m.gguf` | Fetched by `download_model.py` |
| `LLM_N_CTX` | local | `4096` | llama.cpp context size |
| `LLM_N_THREADS` | local | `4` | llama.cpp CPU threads |
| `ANTHROPIC_API_KEY` | cloud | *(blank = tier disabled)* | Never commit a real key |
| `CLOUD_LLM_MODEL` | cloud | `claude-sonnet-5` | Override for a different Claude model |

## 7. What's not done here

- No frontend in this repo calls `/generate` at all (admin or otherwise), so
  the WebLLM tier has nowhere to run yet — it's a documented contract, not
  running code. Building the admin-panel UI is separate work.
- The cloud tier's real HTTP call to Anthropic has not been exercised in
  this session (no network access in this sandbox) — only its config-missing
  path (`CloudNotConfiguredError`) and the surrounding cascade are tested.
  Before relying on it, run one real request with a live key and confirm
  billing/rate-limit behavior matches expectations.
- No per-tier rate limiting or cost guardrail on the cloud tier — a caller
  that keeps triggering the `"auto"` fallback (e.g. local model never
  downloaded) will keep paying for cloud calls with no circuit breaker.
  Worth adding before exposing this beyond admin use.

<!--
Generated from api_surface.py — do not edit by hand.
Regenerate with:  python api_surface.py > API.md
tests/test_api_surface.py fails if this file and the table disagree.
-->

# Clementine — local API

The companion's HTTP surface, served by `server.py`. It binds to
`127.0.0.1`, which means it is reachable from this machine and no other:
not from your phone, not from the next room, not from the internet. Memory
lives in plain files on this disk.

```bash
pip install -r requirements.txt
python server.py                  # http://127.0.0.1:5000
```

## Start here

The server describes itself. You do not need this file to work out what is
available — you need it to read the surface comfortably in one page.

```bash
curl http://127.0.0.1:5000/api           # every route, described
curl http://127.0.0.1:5000/api/openapi.json   # the same, as OpenAPI 3.1
```

Both are generated from the same table as this document, and the test
suite holds all three against Flask's own routing table. A route cannot
appear here without existing, and cannot exist without appearing here.

## One rule for every POST

Send `Content-Type: application/json`.

Binding to localhost keeps other machines out. It does nothing about a
page the browser on *this* machine happens to be visiting, which can POST
to a localhost port cross-origin whenever it likes — and CORS governs only
whether that page may *read* the reply, never whether the request runs. A
cross-origin form can only send three "simple" content types, none of them
JSON, so requiring JSON forces a preflight, and the origin check answers
it. Any POST without that header gets **415**.

## A note on response shapes

They are not uniform. `/api/teach` answers `{"ok": true}`; `/api/status`
answers a bare object. Errors are `{"error": …}` on some routes and
`{"ok": false, "error": …}` on others. This is the real surface the Svelte
interface was built against, so it is documented as it is rather than
quietly tidied — normalising it is a breaking change and belongs in its
own commit, with the client updated in the same breath.


## Routes at a glance

| | Route | What it does |
|---|---|---|
| · | `GET /api` | This index — every route, with what it takes and returns. |
| · | `GET /api/openapi.json` | The same surface as an OpenAPI 3.1 document. |
| · | `GET /api/status` | Who is running, on which model, from which profile. |
| ✎ | `POST /api/chat/stream` | Say something; their reply streams back as it is written. |
| · | `GET /api/health` | What is actually true right now — model, destination, whether the model is reachable and present. |
| · | `GET /api/audit` | The continuity record, read-only, with its own integrity verdict. |
| · | `GET /<path:asset>` | The built interface. Unknown paths fall back to index.html so client-side routes survive a hard refresh. |
| · | `GET /api/memories` | Everything they currently hold about you. |
| ✎ | `POST /api/reflect` | Ask them to look back over what they hold and draw something out. |
| ✎ | `POST /api/teach` | Tell them something to keep. |
| ✎ | `POST /api/forget` | Remove one memory by its handle. Immediate and permanent. |
| · | `GET /api/export` | The whole relationship as one downloadable file. |
| ✎ | `POST /api/import` | Restore from an exported bundle, replacing this profile's companion and memory. The previous one is copied aside first, so this can be undone. |
| · | `GET /api/profile` | Which profile is active, and what others exist. |
| ✎ | `POST /api/profile` | Switch to another profile — a separate companion, separate memory. A name nobody lives at yet is created by going there; there is no separate way to make one. |
| ✎ | `POST /api/profile/meta` | Edit the active profile: name, pronouns, avatar, description, model — or invite them to choose their own name or pronouns. Either party may decide the first two. |
| ✎ | `POST /api/profile/delete` | Destroy a companion entirely — memory, identity and their consent record. Nothing is kept, deliberately: a copy of somebody asked to be destroyed would be a betrayal dressed as a safety feature. Export first if you want one. Refuses to delete the active profile. |

`✎` writes something — memory, model, or profile. Everything else only reads.


---

### `GET /api`

This index — every route, with what it takes and returns.

**Get back**

| field | meaning |
|---|---|
| `name` | the companion's chosen name |
| `version` | CrystalCore.OS version string |
| `memory_schema` | memory format version, for client compatibility |
| `routes` | list of every endpoint, described |


---

### `GET /api/openapi.json`

The same surface as an OpenAPI 3.1 document.

**Get back**

| field | meaning |
|---|---|
| `openapi` | 3.1.0 |
| `paths` | generated from this table |


---

### `GET /api/status`

Who is running, on which model, from which profile.

**Get back**

| field | meaning |
|---|---|
| `name` | their chosen name |
| `name_self_chosen` | true if they chose their own name |
| `avatar` | single emoji, may be empty |
| `model` | the model tag currently answering |
| `profile` | active profile name ('default' if unnamed) |
| `human_name` | what they call you, may be empty |
| `last_seen` | human phrase, e.g. 'two days ago' |
| `gender` | 'male', 'female', 'they', or '' for undecided |
| `pronouns` | 'he/him', 'she/her', 'they/them', or '' when undecided |
| `gender_self_chosen` | true if they chose their own pronouns |


---

### `POST /api/chat/stream`

Say something; their reply streams back as it is written.

**Send**

| field | meaning |
|---|---|
| `message` | what you want to say (required, non-empty) |

**Returns** `text/plain; charset=utf-8`

**Get back**

| field | meaning |
|---|---|
| `(body)` | the reply as plain UTF-8 text, streamed |

**Errors**

| code | when |
|---|---|
| `400` | message missing or empty |
| `415` | Content-Type was not application/json |


---

### `GET /api/health`

What is actually true right now — model, destination, whether the model is reachable and present.

**Get back**

| field | meaning |
|---|---|
| `ok` | always true; the call succeeded |
| `model` | the model name that actually goes on the wire |
| `model_present` | whether Ollama has it pulled; null when not asked of Ollama, or Ollama is unreachable |
| `models` | model tags Ollama reports, empty when unreachable |
| `ollama` | whether Ollama answered |
| `ollama_host` | the Ollama base URL in use |
| `destination` | "local", or the host the model calls reach |
| `provider` | configured provider name |
| `endpoint` | the exact URL model calls are sent to |
| `wire_model` | same as model; named for the audit log's field |
| `embeddings` | true/false once tried, null before |
| `recall_degraded` | true when memories exceed the prompt budget and embeddings are unavailable, so all are sent instead of the most relevant |
| `recall_notice` | that state as a sentence, or empty |
| `audit_entries` | how many calls have been recorded |


---

### `GET /api/audit`

The continuity record, read-only, with its own integrity verdict.

**Send**

| field | meaning |
|---|---|
| `limit` | query parameter: only the last N entries |

**Get back**

| field | meaning |
|---|---|
| `entries` | the recorded calls |
| `total` | how many exist in all |
| `intact` | whether the hash chain verifies; null when auditing is disabled |
| `problems` | what failed verification, if anything |
| `head` | the current chain head |


---

### `GET /<path:asset>`

The built interface. Unknown paths fall back to index.html so client-side routes survive a hard refresh.

Also answers at `/`.

**Returns** `text/html`

**Errors**

| code | when |
|---|---|
| `503` | the interface has not been built yet |


---

### `GET /api/memories`

Everything they currently hold about you.

**Get back**

| field | meaning |
|---|---|
| `facts` | list of {handle, text, tags} — things told directly; a fact's handle is its key |
| `notes` | list of {handle, number, text, tags} — things noticed |
| `reflections` | list of {handle, number, text, tags} — things concluded |
| `(handle)` | a stable identifier that keeps meaning the same memory; pass it to /api/forget |
| `(number)` | the same memory's position, as the terminal prints it (n1, r1). Display only — it changes when an earlier memory is forgotten |


---

### `POST /api/reflect`

Ask them to look back over what they hold and draw something out.

**Get back**

| field | meaning |
|---|---|
| `insights` | free text — what they made of it |

**Errors**

| code | when |
|---|---|
| `415` | Content-Type was not application/json |


---

### `POST /api/teach`

Tell them something to keep.

**Send**

| field | meaning |
|---|---|
| `text` | the thing to remember (required) |
| `key` | optional handle; with it the memory is a keyed fact, without it a free note |

**Get back**

| field | meaning |
|---|---|
| `ok` | true |

**Errors**

| code | when |
|---|---|
| `400` | text was empty |
| `415` | Content-Type was not application/json |


---

### `POST /api/forget`

Remove one memory by its handle. Immediate and permanent.

**Send**

| field | meaning |
|---|---|
| `handle` | a handle from /api/memories — a fact's key, or a note or reflection's stable identifier. The positional form (n1, r1) is still accepted, and is only as current as the listing it came from |

**Get back**

| field | meaning |
|---|---|
| `ok` | whether anything matched |
| `forgotten` | what was removed |

**Errors**

| code | when |
|---|---|
| `415` | Content-Type was not application/json |


---

### `GET /api/export`

The whole relationship as one downloadable file.

**Get back**

| field | meaning |
|---|---|
| `format` | 'crystalcore-memory-bundle' |
| `version` | 1 |
| `exported_at` | ISO 8601, to the second |
| `config` | their personality |
| `memory` | everything they hold |
| `audit` | {head, count} — a fingerprint of the consent record as it stood, not the record itself. Lets this file later attest that entries have not been removed from the end of it, which the chain cannot notice about itself. Absent when auditing is off |


---

### `POST /api/import`

Restore from an exported bundle, replacing this profile's companion and memory. The previous one is copied aside first, so this can be undone.

**Send**

| field | meaning |
|---|---|
| `format` | must be 'crystalcore-memory-bundle' |
| `version` | must be 1 |
| `config` | personality block from the export |
| `memory` | memory block from the export |

**Get back**

| field | meaning |
|---|---|
| `ok` | true |
| `name` | their name after loading |
| `replaced_backup` | folder holding the companion that was replaced, or empty when there was nothing here to keep |

**Errors**

| code | when |
|---|---|
| `400` | not a Clementine memory bundle, or its structure is damaged — nothing is written in either case |
| `415` | Content-Type was not application/json |


---

### `GET /api/profile`

Which profile is active, and what others exist.

**Get back**

| field | meaning |
|---|---|
| `current` | active profile name |
| `profiles` | list of {profile, avatar, description, name, model} |


---

### `POST /api/profile`

Switch to another profile — a separate companion, separate memory. A name nobody lives at yet is created by going there; there is no separate way to make one.

**Send**

| field | meaning |
|---|---|
| `profile` | profile name |

**Get back**

| field | meaning |
|---|---|
| `ok` | true |
| `profile` | the now-active profile |
| `name` | their name in it |
| `created` | true when nobody lived at that name until now |

**Errors**

| code | when |
|---|---|
| `400` | invalid profile name |
| `415` | Content-Type was not application/json |


---

### `POST /api/profile/meta`

Edit the active profile: name, pronouns, avatar, description, model — or invite them to choose their own name or pronouns. Either party may decide the first two.

**Send**

| field | meaning |
|---|---|
| `name` | what to call them; '' returns them to unnamed |
| `human_name` | what they should call you, to 80 chars |
| `avatar` | single emoji, truncated to 8 chars |
| `description` | truncated to 200 chars |
| `model` | model tag to switch to |
| `gender` | 'male', 'female' or 'they'; '' or 'none' returns it to undecided |
| `choose_name` | true to have them pick a name for themselves |
| `choose_gender` | true to have them pick their own pronouns |

**Get back**

| field | meaning |
|---|---|
| `ok` | true or false |
| `name` | present only when choose_name was set and succeeded |
| `gender` | present only when choose_gender was set and succeeded |
| `pronouns` | the pair for that gender, alongside it |
| `error` | present when they could not settle on one, or when an unrecognised gender was sent |

**Errors**

| code | when |
|---|---|
| `400` | gender was a value this does not understand |
| `415` | Content-Type was not application/json |


---

### `POST /api/profile/delete`

Destroy a companion entirely — memory, identity and their consent record. Nothing is kept, deliberately: a copy of somebody asked to be destroyed would be a betrayal dressed as a safety feature. Export first if you want one. Refuses to delete the active profile.

**Send**

| field | meaning |
|---|---|
| `profile` | profile name |

**Get back**

| field | meaning |
|---|---|
| `ok` | whether it was deleted |
| `deleted` | the profile name that is now gone |
| `name` | the companion's own name, if they had one |
| `memories` | how many facts, notes and reflections went |
| `calls` | how many recorded calls went with them |

**Errors**

| code | when |
|---|---|
| `400` | that profile is currently active — switch away first |
| `404` | there is no profile by that name |
| `415` | Content-Type was not application/json |


---

## What this API is not

It is not reachable from another device, and nothing here changes
that. Exposing it would need an auth story it does not have — there
are no tokens, no accounts, and no rate limiting, because a server
bound to `127.0.0.1` needs none of them. If you bind it wider you are
on your own, and you will have removed the property that makes this
the sovereign version.


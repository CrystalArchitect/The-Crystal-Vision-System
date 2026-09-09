# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""One description of the local API, used three ways.

`server.py` registers the routes. This module describes them. From that
single description come the discovery index (`GET /api`), the OpenAPI
document (`GET /api/openapi.json`), and `API.md`.

The point of putting it here rather than in a doc file is that a doc file
can drift. `tests/test_api_surface.py` walks Flask's own url_map and
asserts, in both directions, that this table and the registered routes are
the same set. A route added to `server.py` without an entry here fails the
suite; an entry here for a route that does not exist fails it too.

That is the project's rule applied to its own API: a documented endpoint
nobody implemented is a dreamed line pretending it was measured.

Response shapes are recorded as they actually are, including where they
are inconsistent — `/api/teach` answers `{"ok": true}` while `/api/status`
answers a bare object, and errors come back as `{"error": …}` on some
routes and `{"ok": false, "error": …}` on others. That is the real surface
the Svelte interface was built against, so it is documented rather than
quietly tidied; tidying it is a breaking change and belongs in its own
commit with the client updated alongside.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Route:
    """One endpoint, described once."""

    method: str
    path: str
    summary: str
    #: What a caller sends. Empty for routes that take no body.
    request: dict[str, str] = field(default_factory=dict)
    #: What comes back on success — field name to plain-language meaning.
    response: dict[str, str] = field(default_factory=dict)
    #: Status code to when it happens.
    errors: dict[int, str] = field(default_factory=dict)
    #: Set for anything that writes to memory, changes the model, or
    #: otherwise leaves a mark. Drives the "requires JSON" rule and gives
    #: the index a way to say which calls are not idempotent.
    mutates: bool = False
    #: Non-JSON responses declare their type, so the spec is honest about
    #: the two routes that do not return application/json.
    media_type: str = "application/json"
    #: Extra paths answering the same view. `/` aliases `/api` so that
    #: opening the printed URL in a browser lands somewhere useful
    #: instead of on a 404.
    aliases: tuple[str, ...] = ()


#: Every route `server.py` registers, excluding the CORS preflight
#: catch-all (which answers OPTIONS for all of them and is asserted
#: separately in the tests).
ROUTES: tuple[Route, ...] = (
    Route(
        method="GET",
        path="/api",
        summary="This index — every route, with what it takes and returns.",
        response={
            "name": "the companion's chosen name",
            "version": "CrystalCore.OS version string",
            "memory_schema": "memory format version, for client compatibility",
            "routes": "list of every endpoint, described",
        },
    ),
    Route(
        method="GET",
        path="/api/openapi.json",
        summary="The same surface as an OpenAPI 3.1 document.",
        response={"openapi": "3.1.0", "paths": "generated from this table"},
    ),
    Route(
        method="GET",
        path="/api/status",
        summary="Who is running, on which model, from which profile.",
        response={
            "name": "their chosen name",
            "name_self_chosen": "true if they chose their own name",
            "avatar": "single emoji, may be empty",
            "model": "the model tag currently answering",
            "profile": "active profile name ('default' if unnamed)",
            "human_name": "what they call you, may be empty",
            "last_seen": "human phrase, e.g. 'two days ago'",
            "gender": "'male', 'female', 'they', or '' for undecided",
            "pronouns": "'he/him', 'she/her', 'they/them', or '' when undecided",
            "gender_self_chosen": "true if they chose their own pronouns",
        },
    ),
    Route(
        method="POST",
        path="/api/chat/stream",
        summary="Say something; their reply streams back as it is written.",
        request={"message": "what you want to say (required, non-empty)"},
        response={"(body)": "the reply as plain UTF-8 text, streamed"},
        errors={400: "message missing or empty",
                415: "Content-Type was not application/json"},
        mutates=True,
        media_type="text/plain; charset=utf-8",
    ),
    Route(
        method="GET",
        path="/api/health",
        summary="What is actually true right now — model, destination, "
                "whether the model is reachable and present.",
        response={
            "ok": "always true; the call succeeded",
            "model": "the model name that actually goes on the wire",
            "model_present": "whether Ollama has it pulled; null when not "
                             "asked of Ollama, or Ollama is unreachable",
            "models": "model tags Ollama reports, empty when unreachable",
            "ollama": "whether Ollama answered",
            "ollama_host": "the Ollama base URL in use",
            "destination": '"local", or the host the model calls reach',
            "provider": "configured provider name",
            "endpoint": "the exact URL model calls are sent to",
            "wire_model": "same as model; named for the audit log's field",
            "embeddings": "true/false once tried, null before",
            "recall_degraded": "true when memories exceed the prompt budget "
                               "and embeddings are unavailable, so all are "
                               "sent instead of the most relevant",
            "recall_notice": "that state as a sentence, or empty",
            "audit_entries": "how many calls have been recorded",
        },
    ),
    Route(
        method="GET",
        path="/api/audit",
        summary="The continuity record, read-only, with its own integrity "
                "verdict.",
        request={"limit": "query parameter: only the last N entries"},
        response={
            "entries": "the recorded calls",
            "total": "how many exist in all",
            "intact": "whether the hash chain verifies; null when auditing "
                      "is disabled",
            "problems": "what failed verification, if anything",
            "head": "the current chain head",
        },
    ),
    Route(
        method="GET",
        path="/<path:asset>",
        summary="The built interface. Unknown paths fall back to index.html "
                "so client-side routes survive a hard refresh.",
        aliases=("/",),
        media_type="text/html",
        errors={503: "the interface has not been built yet"},
    ),
    Route(
        method="GET",
        path="/api/memories",
        summary="Everything they currently hold about you.",
        response={
            "facts": "list of {handle, text, tags} — things told directly; "
                     "a fact's handle is its key",
            "notes": "list of {handle, number, text, tags} — things noticed",
            "reflections": "list of {handle, number, text, tags} — things "
                           "concluded",
            "(handle)": "a stable identifier that keeps meaning the same "
                        "memory; pass it to /api/forget",
            "(number)": "the same memory's position, as the terminal prints "
                        "it (n1, r1). Display only — it changes when an "
                        "earlier memory is forgotten",
        },
    ),
    Route(
        method="POST",
        path="/api/reflect",
        summary="Ask them to look back over what they hold and draw something out.",
        response={"insights": "free text — what they made of it"},
        errors={415: "Content-Type was not application/json"},
        mutates=True,
    ),
    Route(
        method="POST",
        path="/api/teach",
        summary="Tell them something to keep.",
        request={"text": "the thing to remember (required)",
                 "key": "optional handle; with it the memory is a keyed fact, "
                        "without it a free note"},
        response={"ok": "true"},
        errors={400: "text was empty",
                415: "Content-Type was not application/json"},
        mutates=True,
    ),
    Route(
        method="POST",
        path="/api/forget",
        summary="Remove one memory by its handle. Immediate and permanent.",
        request={"handle": "a handle from /api/memories — a fact's key, or a "
                           "note or reflection's stable identifier. The "
                           "positional form (n1, r1) is still accepted, and "
                           "is only as current as the listing it came from"},
        response={"ok": "whether anything matched",
                  "forgotten": "what was removed"},
        errors={415: "Content-Type was not application/json"},
        mutates=True,
    ),
    Route(
        method="GET",
        path="/api/export",
        summary="The whole relationship as one downloadable file.",
        response={"format": "'crystalcore-memory-bundle'",
                  "version": "1",
                  "exported_at": "ISO 8601, to the second",
                  "config": "their personality",
                  "memory": "everything they hold",
                  "audit": "{head, count} — a fingerprint of the consent "
                           "record as it stood, not the record itself. Lets "
                           "this file later attest that entries have not "
                           "been removed from the end of it, which the "
                           "chain cannot notice about itself. Absent when "
                           "auditing is off"},
    ),
    Route(
        method="POST",
        path="/api/import",
        summary="Restore from an exported bundle, replacing this profile's "
                "companion and memory. The previous one is copied aside "
                "first, so this can be undone.",
        request={"format": "must be 'crystalcore-memory-bundle'",
                 "version": "must be 1",
                 "config": "personality block from the export",
                 "memory": "memory block from the export"},
        response={"ok": "true", "name": "their name after loading",
                  "replaced_backup": "folder holding the companion that was "
                                     "replaced, or empty when there was "
                                     "nothing here to keep"},
        errors={400: "not a Clementine memory bundle, or its structure is "
                     "damaged — nothing is written in either case",
                415: "Content-Type was not application/json"},
        mutates=True,
    ),
    Route(
        method="GET",
        path="/api/profile",
        summary="Which profile is active, and what others exist.",
        response={"current": "active profile name",
                  "profiles": "list of {profile, avatar, description, name, model}"},
    ),
    Route(
        method="POST",
        path="/api/profile",
        summary="Switch to another profile — a separate companion, separate "
                "memory. A name nobody lives at yet is created by going "
                "there; there is no separate way to make one.",
        request={"profile": "profile name"},
        response={"ok": "true", "profile": "the now-active profile",
                  "name": "their name in it",
                  "created": "true when nobody lived at that name until now"},
        errors={400: "invalid profile name",
                415: "Content-Type was not application/json"},
        mutates=True,
    ),
    Route(
        method="POST",
        path="/api/profile/meta",
        summary="Edit the active profile: name, pronouns, avatar, "
                "description, model — or invite them to choose their own name "
                "or pronouns. Either party may decide the first two.",
        request={"name": "what to call them; '' returns them to unnamed",
                 "human_name": "what they should call you, to 80 chars",
                 "avatar": "single emoji, truncated to 8 chars",
                 "description": "truncated to 200 chars",
                 "model": "model tag to switch to",
                 "gender": "'male', 'female' or 'they'; '' or 'none' returns "
                           "it to undecided",
                 "choose_name": "true to have them pick a name for themselves",
                 "choose_gender": "true to have them pick their own pronouns"},
        response={"ok": "true or false",
                  "name": "present only when choose_name was set and succeeded",
                  "gender": "present only when choose_gender was set and succeeded",
                  "pronouns": "the pair for that gender, alongside it",
                  "error": "present when they could not settle on one, or when "
                           "an unrecognised gender was sent"},
        errors={400: "gender was a value this does not understand",
                415: "Content-Type was not application/json"},
        mutates=True,
    ),
    Route(
        method="POST",
        path="/api/profile/delete",
        summary="Destroy a companion entirely — memory, identity and their "
                "consent record. Nothing is kept, deliberately: a copy of "
                "somebody asked to be destroyed would be a betrayal dressed "
                "as a safety feature. Export first if you want one. Refuses "
                "to delete the active profile.",
        request={"profile": "profile name"},
        response={"ok": "whether it was deleted",
                  "deleted": "the profile name that is now gone",
                  "name": "the companion's own name, if they had one",
                  "memories": "how many facts, notes and reflections went",
                  "calls": "how many recorded calls went with them"},
        errors={400: "that profile is currently active — switch away first",
                404: "there is no profile by that name",
                415: "Content-Type was not application/json"},
        mutates=True,
    ),
)


def index(name: str, version: str, memory_schema: str) -> dict[str, Any]:
    """The discovery document served at `GET /api`.

    Written to be read by a person with `curl` as much as by a client
    library: start the server, hit the root, and the whole surface is
    there without opening an editor.
    """
    return {
        "name": name,
        "version": version,
        "memory_schema": memory_schema,
        "bound_to": "127.0.0.1 — this machine only",
        "note": ("Every POST must be sent with Content-Type: application/json. "
                 "A cross-origin form cannot set that header, which is what "
                 "keeps a page you happen to be visiting from writing to your "
                 "memory."),
        "routes": [
            {
                "method": r.method,
                "path": r.path,
                "summary": r.summary,
                "mutates": r.mutates,
                **({"request": r.request} if r.request else {}),
                "response": r.response,
                **({"returns": r.media_type}
                   if r.media_type != "application/json" else {}),
                **({"errors": {str(k): v for k, v in r.errors.items()}}
                   if r.errors else {}),
            }
            for r in ROUTES
        ],
    }


def _schema_from(fields: dict[str, str]) -> dict[str, Any]:
    """A loose object schema whose descriptions carry the real meaning.

    The values in `ROUTES` are prose, not types. Rather than invent types
    that were never checked, every property is declared untyped with the
    prose as its description — an OpenAPI document that admits what it
    knows beats one that guesses `string` fourteen times.
    """
    return {
        "type": "object",
        "properties": {k: {"description": v} for k, v in fields.items()},
    }


def openapi(name: str, version: str) -> dict[str, Any]:
    """The same table as an OpenAPI 3.1 document.

    Generated rather than hand-written for the same reason the index is:
    a spec maintained by hand becomes a second thing that can be wrong.
    """
    paths: dict[str, dict[str, Any]] = {}
    for r in ROUTES:
        operation: dict[str, Any] = {
            "summary": r.summary,
            "operationId": (r.method.lower()
                            + r.path.replace("/api", "", 1)
                                    .replace("/", "_")
                                    .replace(".", "_") or "_root"),
            "responses": {
                "200": {
                    "description": "success",
                    "content": {r.media_type: {
                        "schema": (_schema_from(r.response)
                                   if r.media_type == "application/json"
                                   else {"type": "string"})}},
                },
                **{
                    str(code): {"description": why,
                                "content": {"application/json": {"schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"description": why}}}}}}
                    for code, why in r.errors.items()
                },
            },
        }
        if r.request:
            operation["requestBody"] = {
                "required": True,
                "content": {"application/json": {
                    "schema": _schema_from(r.request)}},
            }
        paths.setdefault(r.path, {})[r.method.lower()] = operation

    return {
        "openapi": "3.1.0",
        "info": {
            "title": f"{name} — local API",
            "version": version,
            "description": (
                "The local companion's HTTP surface. Bound to 127.0.0.1: it is "
                "reachable from this machine and no other. Memory stays in "
                "plain files on this disk."),
        },
        "servers": [{"url": "http://127.0.0.1:5000",
                     "description": "the default local server"}],
        "paths": paths,
    }


_PREAMBLE = """<!--
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

"""


def render_markdown() -> str:
    """`API.md`, from the same table as everything else.

    Hand-written API docs drift the moment a route changes, and a drifted
    doc costs a newcomer more than no doc at all: they build against it
    and find out at runtime. So this is generated, and
    `test_api_surface.py` fails when the committed file and the table
    disagree.
    """
    out = [_PREAMBLE, "## Routes at a glance\n",
           "| | Route | What it does |", "|---|---|---|"]
    for r in ROUTES:
        mark = "✎" if r.mutates else "·"
        out.append(f"| {mark} | `{r.method} {r.path}` | {r.summary} |")
    out.append("\n`✎` writes something — memory, model, or profile. "
               "Everything else only reads.\n")

    for r in ROUTES:
        out.append(f"\n---\n\n### `{r.method} {r.path}`\n")
        out.append(r.summary + "\n")
        if r.aliases:
            aliases = ", ".join(f"`{a}`" for a in r.aliases)
            out.append(f"Also answers at {aliases}.\n")
        if r.request:
            out.append("**Send**\n")
            out.append("| field | meaning |")
            out.append("|---|---|")
            for k, v in r.request.items():
                out.append(f"| `{k}` | {v} |")
            out.append("")
        if r.media_type != "application/json":
            out.append(f"**Returns** `{r.media_type}`\n")
        if r.response:
            out.append("**Get back**\n")
            out.append("| field | meaning |")
            out.append("|---|---|")
            for k, v in r.response.items():
                out.append(f"| `{k}` | {v} |")
            out.append("")
        if r.errors:
            out.append("**Errors**\n")
            out.append("| code | when |")
            out.append("|---|---|")
            for code, why in sorted(r.errors.items()):
                out.append(f"| `{code}` | {why} |")
            out.append("")

    out.append("\n---\n")
    out.append("## What this API is not\n")
    out.append(
        "It is not reachable from another device, and nothing here changes\n"
        "that. Exposing it would need an auth story it does not have — there\n"
        "are no tokens, no accounts, and no rate limiting, because a server\n"
        "bound to `127.0.0.1` needs none of them. If you bind it wider you are\n"
        "on your own, and you will have removed the property that makes this\n"
        "the sovereign version.\n")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(render_markdown(), end="")

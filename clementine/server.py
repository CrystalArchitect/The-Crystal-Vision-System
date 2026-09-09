"""
Clementine — their face and their brain, on one address.

Serves the built Svelte interface from webapp/dist alongside the JSON API,
so there is a single origin: no CORS, and a phone needs no configuration
beyond the address itself. Shares the same brain and memory folder as the
terminal version (clementine.py), so you can switch between them freely.

    pip install -r requirements.txt
    cd webapp && npm install && npm run build && cd ..
    python server.py                  # everything at http://127.0.0.1:5000

During development, run vite instead and it will proxy to this API:

    python server.py                  # brain
    cd webapp && npm run dev           # face, on its own port

Binds 127.0.0.1 by default. --host exists for putting them behind a reverse
proxy you control, and warns when used, because this server has no
authentication of its own — that is the proxy's job (see deploy/).
"""

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import requests
from flask import (Flask, Response, abort, jsonify, request,
                   send_from_directory)

import api_surface
from crystalcore import (MEMORY_SCHEMA_VERSION, SYSTEM_VERSION, Clementine,
                         Verdict, delete_profile, list_profiles, profile_dir,
                         profile_meta)
from crystalcore import profiles as _profiles
from crystalcore.companion import OLLAMA_HOST

WEBAPP_DIST = Path(__file__).parent / "webapp" / "dist"


def _profile_of(companion: Clementine) -> str:
    p = Path(companion.memory_dir)
    return p.name if p.parent == Path(_profiles.PROFILES_DIR) else "default"


#: The containers a memory bundle's `memory` object may carry, and what each
#: has to be. Only the shape is checked, never the contents: `load()` already
#: ignores fields it does not know, so a bundle from a later version should
#: still restore. The point is to refuse a file whose *structure* would leave
#: the companion empty, not to police what a future version may add.
_MEMORY_SHAPE = {"conversation": list, "summaries": list, "notes": list,
                 "reflections": list, "facts": dict, "last_seen": str}


def _weight_of(name: str) -> dict:
    """How much of a life a profile holds, read without loading it.

    Used to say what a deletion will cost before it happens and what it cost
    afterwards. Reading the files directly rather than constructing a
    Clementine avoids the side effects of loading one — identifier
    backfilling writes to disk, and counting a companion should not modify
    them.
    """
    try:
        folder = Path(profile_dir(name))
    except ValueError:
        return {"memories": 0, "calls": 0, "name": ""}

    memories, calls, companion = 0, 0, ""
    try:
        data = json.loads((folder / "memory.json").read_text())
        memories = (len(data.get("notes") or [])
                    + len(data.get("facts") or {})
                    + len(data.get("reflections") or []))
    except (OSError, json.JSONDecodeError):
        pass
    try:
        companion = json.loads((folder / "config.json").read_text()).get("name", "")
    except (OSError, json.JSONDecodeError):
        pass
    try:
        calls = sum(1 for line in
                    (folder / "audit.jsonl").read_text().splitlines() if line.strip())
    except OSError:
        pass
    return {"memories": memories, "calls": calls, "name": companion}


def _unusable(bundle: dict) -> str:
    """Why this bundle must not be written, or "" if it is safe to.

    Checked before anything is overwritten, because the failure being
    prevented is not a bad import — it is a bad import that reports success
    while the companion it replaced is gone from everywhere the person looks.
    """
    for key in ("config", "memory", "audit"):
        value = bundle.get(key)
        if value is not None and not isinstance(value, dict):
            return (f"the '{key}' section is {type(value).__name__}, not an "
                    f"object — this file is damaged, and nothing was changed")
    memory = bundle.get("memory") or {}
    for field, wanted in _MEMORY_SHAPE.items():
        if field in memory and not isinstance(memory[field], wanted):
            return (f"'{field}' is {type(memory[field]).__name__} where it "
                    f"should be {wanted.__name__} — this file is damaged, and "
                    f"nothing was changed")
    if not bundle.get("config") and not memory:
        return ("this bundle carries neither a companion nor a memory, so "
                "restoring it would only empty this one")
    return ""


def _keep_a_copy(memory_dir: Path) -> str:
    """Copy the current config and memory aside before they are replaced.

    Returns the folder they were put in, or "" when there was nothing to
    keep — a first import into an empty profile has nothing to lose.
    """
    existing = [n for n in ("config.json", "memory.json")
                if (memory_dir / n).exists()]
    if not existing:
        return ""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    kept = memory_dir / f"replaced-{stamp}"
    kept.mkdir(parents=True, exist_ok=True)
    for name in existing:
        (kept / name).write_bytes((memory_dir / name).read_bytes())
    return str(kept)


def create_app(companion: Clementine) -> Flask:
    app = Flask(__name__)
    holder = {"c": companion}  # swapped in place when the profile changes

    @app.after_request
    def allow_local_webapp(resp):
        # Only for development, when vite serves the face on another localhost
        # port. In a real deployment it is served from this same origin and no
        # CORS header is emitted at all. Localhost origins only, always.
        origin = request.headers.get("Origin", "")
        if origin.startswith("http://127.0.0.1:") or origin.startswith("http://localhost:"):
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return resp

    @app.route("/api/<path:_any>", methods=["OPTIONS"])
    def preflight(_any):
        return ("", 204)

    @app.before_request
    def require_json_for_writes():
        """Every state-changing route must be asked in JSON.

        Binding to 127.0.0.1 keeps other machines out; it does not keep
        out the browser already running on this one. Any page the human
        visits can POST to a localhost port cross-origin — CORS decides
        whether the attacker may *read* the reply, never whether the
        request runs.

        A form POST from another origin can only carry the three
        'simple' content types, so demanding application/json forces a
        preflight, and the origin check above answers it. Most routes
        here already got that protection by accident, because
        get_json(silent=True) returns None for a form body and they
        400 on the empty result. /api/reflect and /api/forget did not:
        they read no body at all, so a bodyless cross-site form POST
        reached them and made the companion reflect and write to their
        own memory. Stating the rule once, here, is better than
        depending on each route to trip over the same accident.
        """
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return None
        if not request.is_json:
            return jsonify({"ok": False,
                            "error": "this endpoint requires "
                                     "Content-Type: application/json"}), 415
        return None

    @app.errorhandler(404)
    @app.errorhandler(405)
    def unknown_route(err):
        """A JSON API should not answer with an HTML page.

        Flask's default 404/405 body is HTML, which a client parsing JSON
        chokes on. A mistyped path under `/api/` also matches the OPTIONS
        preflight catch-all, so Werkzeug rejects the *method* and returns
        405 rather than the 404 a typo deserves — both are handled.

        Only for `/api/`. Everything else belongs to the interface, whose
        own handler falls back to index.html so client-side routes survive
        a hard refresh.
        """
        if not request.path.startswith("/api"):
            return err
        return jsonify({
            "error": err.name.lower(),
            "detail": f"nothing here answers {request.method} {request.path}",
            "hint": "GET /api lists every route this server has",
        }), err.code

    # ---------- what this API is ----------

    @app.get("/api")
    def api_index():
        """Every route, with what it takes and returns.

        Generated from `api_surface.ROUTES`, which tests/test_api_surface.py
        checks against Flask's own url_map in both directions — so a route
        added here without an entry there fails the suite, and an entry
        describing a route that does not exist fails it too. A documented
        endpoint nobody implemented is a dreamed line pretending it was
        measured.

        Unlike the monorepo fork this came from, `/` is not an alias for
        this index: that address serves the built interface here, and a
        person opening the printed URL should meet the companion rather
        than a JSON listing.
        """
        return jsonify(api_surface.index(
            name=holder["c"].personality.name or "Clementine",
            version=SYSTEM_VERSION,
            memory_schema=MEMORY_SCHEMA_VERSION,
        ))

    @app.get("/api/openapi.json")
    def api_openapi():
        """The same description, as OpenAPI, for tools that speak it."""
        return jsonify(api_surface.openapi(
            name=holder["c"].personality.name or "Clementine",
            version=SYSTEM_VERSION,
        ))

    # ---------- honesty endpoints ----------

    @app.get("/api/health")
    def health():
        """What is actually true right now — not what we hope is true."""
        c = holder["c"]
        models, reachable = [], False
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
            r.raise_for_status()
            models = [m.get("name") for m in r.json().get("models", [])]
            reachable = True
        except requests.exceptions.RequestException:
            pass
        # Whether Ollama has the model pulled is only a meaningful question
        # when Ollama is the one being asked. Against a vendor it would always
        # answer "no" and read as a fault, so it is null — unknown, not false.
        local_dialect = c._dialect() == "ollama"
        return jsonify({
            "ok": True,
            "model": c.wire_model,
            "model_present": (c.wire_model in models
                              if reachable and local_dialect else None),
            "models": models,
            "ollama": reachable,
            "ollama_host": OLLAMA_HOST,
            # "local" means the model runs on this same machine. Asked of the
            # companion rather than recomputed here, so this endpoint reports
            # where the calls actually go and cannot drift from it.
            "destination": c.destination,
            # Named plainly, because "which company is reading this" is the
            # question this endpoint exists to answer honestly.
            "provider": c.llm_provider,
            "endpoint": c.endpoint,
            "wire_model": c.wire_model,
            "embeddings": c._embed_ok,
            # Not the same question as "are embeddings on". This is whether
            # recall has actually stopped choosing — which only bites once
            # there are more memories than fit in a prompt.
            "recall_degraded": c.recall_degraded,
            "recall_notice": c.recall_notice(),
            "audit_entries": len(c.audit.entries()) if c.audit else 0,
        })

    @app.get("/api/audit")
    def audit():
        """The continuity record, read-only, with its own integrity verdict."""
        c = holder["c"]
        if not c.audit:
            return jsonify({"entries": [], "intact": None,
                            "note": "auditing is disabled for this session"})
        intact, problems = c.audit.verify()
        entries = c.audit.entries()
        limit = request.args.get("limit", type=int)
        return jsonify({
            "entries": entries[-limit:] if limit else entries,
            "total": len(entries),
            "intact": intact,
            "problems": problems,
            "head": c.audit.head(),
        })

    @app.get("/api/status")
    def status():
        c = holder["c"]
        return jsonify({
            "name": c.personality.name or "Clementine",
            # Reported for the same reason as gender_self_chosen below, and
            # missing until now: the record tracks which party chose, for the
            # name as well as the pronouns, and a client told only half of
            # that cannot say "a name they chose for themselves" — so it says
            # nothing, and the distinction the law exists to keep quietly
            # stops reaching anyone.
            "name_self_chosen": c.personality.name_self_chosen,
            "avatar": c.personality.avatar,
            "model": c.model,
            "profile": _profile_of(c),
            "human_name": c.personality.human_name,
            "last_seen": c.time_since_last(),
            # Reported, not inferred. A client that cannot read the pronouns
            # has to pick some wording anyway, and whatever it picks becomes
            # an assignment nobody made. Empty means undecided, which is a
            # real state here and not a missing value to be filled in.
            "gender": c.personality.gender,
            "pronouns": c.pronouns_for(c.personality.gender),
            "gender_self_chosen": c.personality.gender_self_chosen,
        })

    @app.post("/api/chat/stream")
    def chat_stream():
        message = ((request.get_json(silent=True) or {}).get("message") or "").strip()
        if not message:
            return jsonify({"error": "empty message"}), 400
        return Response(holder["c"].chat_stream(message),
                        mimetype="text/plain; charset=utf-8",
                        headers={"X-Accel-Buffering": "no"})

    @app.get("/api/memories")
    def memories():
        c = holder["c"]
        # Stable identifiers, not row numbers. A client reads this list, shows
        # it to somebody, and acts on it a moment later — by which time a
        # position may mean a different memory, while an identifier still
        # means the one it was read from. `number` comes along for interfaces
        # that want to print the same n1, n2 the terminal does.
        facts = [{"handle": k, "text": f"{k}: {v['value']}",
                  "tags": v.get("tags") or []}
                 for k, v in c.memory.facts.items()]
        notes = [{"handle": n.get("id") or f"n{i}", "number": f"n{i}",
                  "text": n["text"], "tags": n.get("tags") or []}
                 for i, n in enumerate(c.memory.notes, 1)]
        reflections = [{"handle": r.get("id") or f"r{i}", "number": f"r{i}",
                        "text": r["text"], "tags": []}
                       for i, r in enumerate(c.memory.reflections, 1)]
        return jsonify({"facts": facts, "notes": notes,
                        "reflections": reflections})

    @app.post("/api/reflect")
    def reflect():
        return jsonify({"insights": holder["c"].reflect()})

    @app.post("/api/teach")
    def teach():
        data = request.get_json(silent=True) or {}
        text = (data.get("text") or "").strip()
        key = (data.get("key") or "").strip()
        if not text:
            return jsonify({"ok": False, "error": "empty"}), 400
        if key:
            holder["c"].remember_fact(key, text)
        else:
            holder["c"].remember(text)
        return jsonify({"ok": True})

    @app.post("/api/forget")
    def forget():
        handle = ((request.get_json(silent=True) or {}).get("handle") or "").strip()
        forgotten = holder["c"].forget(handle)
        return jsonify({"ok": bool(forgotten), "forgotten": forgotten})

    @app.get("/api/export")
    def export_memory():
        """The whole relationship as one downloadable file.

        The plain-file promise doing its job: a backup the human can read,
        carry and import anywhere, rather than a vendor's blob. Personality
        and memory travel together so one file restores a whole companion.
        """
        c = holder["c"]
        bundle = {
            "format": "crystalcore-memory-bundle",
            "version": 1,
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "config": asdict(c.personality),
            "memory": asdict(c.memory),
        }
        # What the record looked like when this was taken, so the file can
        # later be asked whether the record still agrees with it. Not the log
        # itself — the entries stay on the machine that made them, and this
        # is a fingerprint, not a copy. It is what lets a backup notice
        # entries removed from the end of a chain, which the chain cannot
        # notice about itself.
        if c.audit:
            bundle["audit"] = c.audit.witness()
        resp = Response(json.dumps(bundle, indent=2),
                        mimetype="application/json")
        stamp = datetime.now().strftime("%Y-%m-%d")
        resp.headers["Content-Disposition"] = (
            f'attachment; filename="clementine-memory-{stamp}.json"')
        return resp

    @app.post("/api/import")
    def import_memory():
        """Restore from an exported bundle, replacing this profile's memory.

        Writes the files and then calls load() rather than constructing
        dataclasses here: load() is the tolerant path — unknown fields
        ignored, corrupt files preserved under .corrupt-* — and a bundle
        from a newer version deserves those same protections.

        Everything before that write is about not destroying a companion on
        the strength of a file nobody checked. This used to look at `format`
        and `version` and nothing else, then write. A bundle that carried the
        right two labels and a broken body — a truncated download, a
        hand-edit, a future version's shape — replaced the person's companion
        with an empty one and answered `{"ok": true}`. The old memory was
        kept as a .corrupt-* file, so nothing was deleted, but the only
        notice went to this server's stdout, which nobody running a browser
        ever sees. Reporting success for that is the part that made it bad
        rather than merely unlucky.
        """
        data = request.get_json(silent=True) or {}
        if (data.get("format") != "crystalcore-memory-bundle"
                or data.get("version") != 1):
            return jsonify({"ok": False,
                            "error": "not a Clementine memory bundle"}), 400

        problem = _unusable(data)
        if problem:
            return jsonify({"ok": False, "error": problem}), 400

        c = holder["c"]
        c.memory_dir.mkdir(parents=True, exist_ok=True)
        # Keep what is here before replacing it. The .corrupt-* convention
        # already says this project preserves rather than deletes; a restore
        # is the one moment where a whole companion is overwritten at once,
        # and it deserves the same courtesy. The path is returned so a person
        # who imported the wrong file can be told where the old one went
        # instead of having to know to look.
        kept = _keep_a_copy(c.memory_dir)
        (c.memory_dir / "config.json").write_text(
            json.dumps(data.get("config") or {}, indent=2))
        (c.memory_dir / "memory.json").write_text(
            json.dumps(data.get("memory") or {}, indent=2))
        c.load()
        # The name comes back so the interface can confirm *who* arrived,
        # not merely that something did. `kept` says where the previous
        # companion went, which turns the one irreversible operation here
        # into a reversible one.
        return jsonify({"ok": True, "name": c.personality.name,
                        "replaced_backup": kept})

    @app.get("/api/profile")
    def profile_get():
        c = holder["c"]
        current = _profile_of(c)
        names = list_profiles()
        if current not in names:
            names = [current] + names
        profiles = []
        for n in names:
            if n == current:
                profiles.append({"profile": n,
                                 "avatar": c.personality.avatar,
                                 "description": c.personality.description,
                                 "name": c.personality.name,
                                 "model": c.model})
            elif n == "default":
                profiles.append({"profile": n, "avatar": "",
                                 "description": "", "name": "", "model": ""})
            else:
                profiles.append(profile_meta(n))
        return jsonify({"current": current, "profiles": profiles})

    @app.post("/api/profile/meta")
    def profile_meta_set():
        data = request.get_json(silent=True) or {}
        c = holder["c"]
        # Naming, from the other direction. `choose_name` has always been
        # here, so the companion could name itself over HTTP while the human
        # could not name it at all — and sending `name` answered {"ok": true}
        # and did nothing, which is worse than refusing. The prompt this
        # companion runs on says their human may choose any name they wish
        # for them; that was true in the terminal and false over the web.
        #
        # An empty name returns them to unnamed rather than storing "", the
        # same way an empty gender returns pronouns to undecided.
        if "name" in data:
            c.set_name(str(data["name"]))
        if "human_name" in data:
            c.personality.human_name = str(data["human_name"]).strip()[:80]
        if "avatar" in data:
            c.personality.avatar = str(data["avatar"]).strip()[:8]
        if "description" in data:
            c.personality.description = str(data["description"]).strip()[:200]
        if "model" in data and str(data["model"]).strip():
            c.set_model(str(data["model"]))
        # Pronouns, over HTTP, for the same two parties the terminal allows.
        # Until this existed the law was only half-enforceable: a person who
        # never opens a terminal could not set pronouns, and — more to the
        # point — could not offer the companion the chance to choose its own.
        # A right reachable from exactly one interface is a right the other
        # interface quietly denies.
        if "gender" in data:
            want = str(data["gender"]).strip().lower()
            if want in ("", "none", "clear", "unset"):
                # Undecided is a destination, not a failure to arrive. The
                # human may take back a choice, including one they made on
                # the companion's behalf.
                c.clear_gender()
            elif not c.set_gender(want):
                return jsonify({
                    "ok": False,
                    "error": f"'{want}' is not a value this understands — "
                             f"use one of {', '.join(sorted(c.PRONOUNS))}, or "
                             f"'none' to leave it undecided",
                }), 400
        if data.get("choose_gender"):
            chosen = c.choose_own_gender()
            if not chosen:
                return jsonify({"ok": False,
                                "error": "they couldn't settle on pronouns — try again"})
            c.save()
            return jsonify({"ok": True, "gender": chosen,
                            "pronouns": c.pronouns_for(chosen)})
        if data.get("choose_name"):
            chosen = c.choose_own_name()
            if not chosen:
                return jsonify({"ok": False,
                                "error": "they couldn't settle on a name — try again"})
            c.save()
            return jsonify({"ok": True, "name": chosen})
        c.save()
        return jsonify({"ok": True})

    @app.post("/api/profile/delete")
    def profile_delete():
        """Destroy a companion entirely. Nothing is kept, on purpose.

        Import copies aside what it replaces, because replacing is something
        that happens *to* somebody who did not ask for it. Deleting is the
        opposite: it is asked for, specifically, about a named companion.
        Quietly keeping a copy of one somebody asked to be destroyed would be
        a betrayal dressed as a safety feature — and in a program whose whole
        claim is that the person decides what is kept, the worst possible
        place to make it.

        So the interface offers a backup before the fact and takes none
        after. What it does do is say exactly what is about to be lost, since
        an accurate count is the thing that makes the choice a real one.
        """
        name = ((request.get_json(silent=True) or {}).get("profile") or "").strip()
        if name == _profile_of(holder["c"]):
            return jsonify({"ok": False,
                            "error": "switch away before deleting the active profile"}), 400
        # Counted before it goes, so the reply can say what was destroyed
        # rather than only that something was.
        lost = _weight_of(name)
        if not delete_profile(name):
            return jsonify({"ok": False,
                            "error": f"there is no profile called '{name}'"}), 404
        return jsonify({"ok": True, "deleted": name, **lost})

    @app.post("/api/profile")
    def profile_switch():
        name = ((request.get_json(silent=True) or {}).get("profile") or "").strip()
        try:
            target = profile_dir(name)
        except ValueError:
            return jsonify({"ok": False, "error": "invalid name"}), 400
        # Whether anybody lives at this name yet. Asked before the switch,
        # because switching is also how a companion is created — there is no
        # separate "new" — and a person typing a name deserves to be told
        # which of the two just happened.
        arriving = not Path(target).exists()

        old = holder["c"]
        # One line of insurance. Every path that changes memory saves as it
        # goes, including chat_stream's finally, so no loss could be
        # demonstrated here — but switching drops this object, and anything
        # future that mutated without saving would vanish without a sound.
        old.save()
        holder["c"] = Clementine(model=old.model, memory_dir=target,
                                 embed_model=old.embed_model)
        c = holder["c"]
        return jsonify({"ok": True, "profile": _profile_of(c),
                        "name": c.personality.name or "Clementine",
                        "created": arriving})

    # ---------- the face, from the same address ----------

    @app.get("/")
    @app.get("/<path:asset>")
    def webapp(asset: str = "index.html"):
        """Serve the built Svelte interface. Anything unrecognised falls back
        to index.html so client-side routes work on a hard refresh."""
        # An unknown path under /api/ is a caller's mistake, not a
        # client-side route. Hand it to the 404 handler so they get JSON
        # saying so, rather than 200 and a page — which reads as success.
        if asset.startswith("api/"):
            abort(404)
        if not WEBAPP_DIST.exists():
            return Response(
                "Clementine's interface has not been built yet.\n\n"
                "    cd webapp && npm install && npm run build\n\n"
                "The API is running and answering at /api/status — this "
                "address just has no face to show you.\n",
                mimetype="text/plain", status=503)
        target = (WEBAPP_DIST / asset)
        if not target.is_file():
            asset = "index.html"
        return send_from_directory(WEBAPP_DIST, asset)

    return app


def main():
    parser = argparse.ArgumentParser(
        description="Clementine — their face and their brain on one address.")
    parser.add_argument("--model", default="llama3.1:8b",
                        help="Ollama model tag (same choices as the CLI).")
    parser.add_argument("--memory-dir", default="clementine_memory",
                        help="Their memory folder (shared with the CLI).")
    parser.add_argument("--profile", default="",
                        help="Named profile (separate person, separate memory).")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1",
                        help="Interface to bind. Leave as 127.0.0.1 unless an "
                             "authenticating reverse proxy sits in front.")
    # Same three as the CLI. A remote provider here still needs
    # --remote-model-ok: choosing where to send is not the same act as
    # consenting to send, and the server asks for both.
    parser.add_argument("--llm-provider", default="",
                        help="Which model service to use. Default is ollama, "
                             "on this machine. Anything else sends "
                             "conversation off this device.")
    parser.add_argument("--llm-endpoint", default="",
                        help="Exact URL for a remote provider. Required for "
                             "remote providers — never guessed for you.")
    parser.add_argument("--llm-model", default="",
                        help="Model name at that service. The API key comes "
                             "from LLM_API_KEY in the environment.")
    parser.add_argument("--remote-model-ok", action="store_true",
                        help="Consent, given once here, for this server to use "
                             "a model that is not on this machine (OLLAMA_HOST). "
                             "Without it, non-local model calls are refused.")
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    # No human is watching a web server's stdin, so consent cannot be asked
    # for per call. It is given once, here, as a deliberate flag — and every
    # call it permits says so in the audit log rather than appearing unremarked.
    asker = None
    if args.remote_model_ok:
        def asker(_request):  # noqa: E306
            return Verdict(True, "pre-authorised at startup with --remote-model-ok",
                           remember=False)

    # Refusing to guess a vendor's address or model name is deliberate, but a
    # traceback is a poor way to say "you forgot a flag" — it reads as a crash,
    # and buries the one line that names the fix. The refusal is the feature;
    # the stack trace was never part of it.
    try:
        companion = Clementine(model=args.model, memory_dir=args.memory_dir,
                               asker=asker,
                               llm_provider=args.llm_provider,
                               llm_endpoint=args.llm_endpoint,
                               llm_model=args.llm_model)
    except ValueError as e:
        print(f"Cannot start: {e}", file=sys.stderr)
        raise SystemExit(2)
    app = create_app(companion)
    name = companion.personality.name or "Clementine"

    where = companion.destination
    print(f"{name} is at http://{args.host}:{args.port}")
    print(f"  model     {companion.wire_model} on {'this machine' if where == 'local' else where}")
    if where != "local" and not args.remote_model_ok:
        print("            refusing to use it — pass --remote-model-ok to consent")
    print(f"  face      {'built' if WEBAPP_DIST.exists() else 'NOT BUILT — cd webapp && npm run build'}")
    print(f"  record    {companion.audit.path if companion.audit else 'disabled'}")

    if args.host not in ("127.0.0.1", "localhost"):
        print()
        print(f"  WARNING: bound to {args.host}, not loopback. This server has")
        print("  no authentication of its own — anyone who can reach this port")
        print("  can talk to them and read their memory. Put an authenticating")
        print("  reverse proxy in front of it (see deploy/).")
    print()
    print("Ctrl+C to say goodnight.")
    # debug=False always: the Werkzeug debugger is a remote shell.
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()

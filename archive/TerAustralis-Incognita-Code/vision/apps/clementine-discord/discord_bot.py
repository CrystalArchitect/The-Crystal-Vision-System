# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Clementine, reachable from a phone, without giving anything up.

The problem this solves is specific. The local companion is the honest
one — the model runs on your machine, memory sits in files you own,
nothing leaves. It is also unreachable from a phone, which is where the
person actually is. The web shell at `vision/apps/clementine-voice/`
solves reach by sending your words to a hosted model, which is the
opposite trade.

Discord threads the needle. The bot connects *outward* to Discord's
gateway, so no port is opened and nothing has to be exposed to the
internet: the machine at home reaches out, and the phone in your pocket
talks to Discord. Your words pass through Discord, which is a real cost
and is stated plainly in `DISCORD.md` — but the model, the memory and the
companion never leave your machine. It also costs nothing, needs no API
key, and on iOS the keyboard's dictation key means you can talk instead of
type, which was the point of the exercise.

It is a client of the local HTTP API rather than an importer of
`CrystalCore`. Two processes writing `memory.json` is how memories get
lost; one owner of the files is how they do not.

    pip install -r requirements-discord.txt
    export DISCORD_TOKEN=...            # from the Discord developer portal
    export CLEMENTINE_DISCORD_OWNERS=your_user_id
    python discord_bot.py

See `DISCORD.md` for getting the token and the id.
"""

from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass

from clementine_api import (Clementine, ClementineAPIError, ClementineOffline,
                            describe_offline)

#: Discord refuses any message body longer than this.
DISCORD_LIMIT = 2000

#: How often a streaming reply may be edited into place. Discord rate
#: limits edits per channel; going faster gets the bot throttled, which
#: shows up as a reply that freezes mid-sentence and then jumps. Slower
#: than a browser's streaming, deliberately.
EDIT_INTERVAL_S = 1.2

#: Left on the end of a partial reply so a half-finished message reads as
#: in-progress rather than as a companion who stopped mid-thought.
TYPING_TAIL = " ▌"


# --------------------------------------------------------------------------
# Pure logic. Everything here is testable without Discord or a server, and
# is deliberately kept apart from the gateway glue for that reason.
# --------------------------------------------------------------------------


def split_for_discord(text: str, limit: int = DISCORD_LIMIT) -> list[str]:
    """Cut a reply into sendable pieces without losing a character.

    Lossless by construction: each piece is a slice of the original and
    they are returned in order, so joining them reproduces the input
    exactly. That property is worth more than tidy edges — a companion
    that silently drops the end of a long answer is worse than one that
    breaks a sentence — and the test suite asserts it directly.

    Boundaries are preferred in descending order of how little they hurt:
    paragraph, then line, then sentence, then space. A run with no
    boundary at all (a long URL, a base64 blob) is cut at the limit,
    because the alternative is refusing to send it.
    """
    if not text:
        return []
    pieces: list[str] = []
    rest = text
    while len(rest) > limit:
        window = rest[:limit]
        cut = -1
        for boundary in ("\n\n", "\n", ". ", " "):
            found = window.rfind(boundary)
            if found > 0:
                # Keep the boundary itself on the tail of this piece, so
                # the join stays exact.
                cut = found + len(boundary)
                break
        if cut <= 0:
            cut = limit
        pieces.append(rest[:cut])
        rest = rest[cut:]
    if rest:
        pieces.append(rest)
    return pieces


@dataclass
class StreamPacer:
    """Decides when a streaming reply is worth pushing to Discord.

    Editing on every chunk would be both wasteful and self-defeating —
    Discord throttles, and a throttled bot looks frozen. Editing on a
    timer alone stutters on slow models. So: push when the interval has
    passed *and* something new arrived, or immediately once a piece has
    grown past what one message can hold.
    """

    interval: float = EDIT_INTERVAL_S
    limit: int = DISCORD_LIMIT
    last_push: float = 0.0
    last_len: int = 0

    def should_push(self, now: float, current_len: int) -> bool:
        if current_len == self.last_len:
            return False          # nothing new; an edit would be a no-op
        if current_len >= self.limit:
            return True           # must split now or exceed the limit
        return (now - self.last_push) >= self.interval

    def pushed(self, now: float, current_len: int) -> None:
        self.last_push = now
        self.last_len = current_len


def parse_owner_ids(raw: str) -> set[int]:
    """Read the allowlist, ignoring the ways a human writes a list.

    Empty means empty. The bot refuses to start on an empty allowlist
    rather than defaulting to open, because an open bot lets anyone who
    can see it write to the companion's memory — and memory is the thing
    this whole project is trying to keep under one person's control.
    """
    ids: set[int] = set()
    for token in raw.replace(",", " ").split():
        token = token.strip().strip("<@!>")
        if token.isdigit():
            ids.add(int(token))
    return ids


def should_answer(*, author_id: int, is_dm: bool, mentioned: bool,
                  author_is_self: bool, owners: set[int]) -> bool:
    """Whether a message is for us, and from someone allowed to ask.

    Two independent gates, and both matter. The allowlist is the security
    one. The DM-or-mention rule is the manners one: a bot that answers
    every line in a shared channel is a bot people mute.
    """
    if author_is_self:
        return False              # never answer our own messages
    if author_id not in owners:
        return False
    return is_dm or mentioned


def strip_mentions(text: str, user_id: int | None) -> str:
    """Remove our own @-mention so the model isn't handed `<@1234> hello`.

    `user_id` is optional because `client.user` is `None` until the
    gateway says we are ready, and a message can in principle reach the
    handler before then. Dereferencing it unguarded is a crash in the one
    situation nobody tests by hand — the first seconds of a connection.
    """
    if user_id is not None:
        for mention in (f"<@{user_id}>", f"<@!{user_id}>"):
            text = text.replace(mention, "")
    return text.strip()


def format_status(status: dict) -> str:
    """The `!status` line.

    Falls back on the name because a freshly created profile has none
    until they choose one, and `**{''}**` renders as a stray `****`
    rather than as a companion. Found by running the real client against
    a real server on a new memory folder, which is the only place an
    empty name shows up.
    """
    name = (status.get("name") or "").strip() or "Clementine"
    avatar = (status.get("avatar") or "").strip()
    bits = [f"**{name}**" + (f" {avatar}" if avatar else "")]
    if status.get("model"):
        bits.append(f"model `{status['model']}`")
    if status.get("profile"):
        bits.append(f"profile `{status['profile']}`")
    if status.get("last_seen"):
        bits.append(f"last seen {status['last_seen']}")
    return " · ".join(bits)


def format_memories(payload: dict, limit: int = 25) -> str:
    """The `!memories` reply, and honest about what it left out."""
    lines: list[str] = []
    for label in ("facts", "notes", "reflections"):
        items = payload.get(label) or []
        if not items:
            continue
        lines.append(f"**{label}** ({len(items)})")
        for item in items[:limit]:
            handle = item.get("handle", "?")
            lines.append(f"  `{handle}` {item.get('text', '')}")
        if len(items) > limit:
            lines.append(f"  …and {len(items) - limit} more")
    return "\n".join(lines) if lines else "She isn't holding anything yet."


HELP = """**Clementine — on Discord**

Just talk to me; a DM or a mention is enough.

`!status`            who's running, on which model
`!memories`          everything she's holding
`!teach <text>`      give her something to keep
`!teach key: <text>` keep it as a named fact
`!forget <handle>`   remove one memory
`!reflect`           ask her to look back over it all
`!help`              this

She runs on a machine you own. Your words pass through Discord to get \
there; the model and the memory never leave it."""


# --------------------------------------------------------------------------
# Gateway glue. Thin on purpose — everything worth testing is above.
# --------------------------------------------------------------------------


def build_client(clem: Clementine, owners: set[int]):  # pragma: no cover
    """Construct the Discord client.

    Imported here rather than at module scope so the pure logic above,
    and its tests, do not require `discord.py` to be installed.
    """
    import discord

    intents = discord.Intents.default()
    # Required to read message text at all. It must also be switched on in
    # the Discord developer portal — the library cannot do that for you,
    # and without it the bot connects fine and then appears deaf, which is
    # the single most confusing way this can fail.
    intents.message_content = True

    client = discord.Client(intents=intents)

    async def send_long(channel, text: str):
        for piece in split_for_discord(text):
            await channel.send(piece)

    async def stream_reply(channel, prompt: str):
        """Answer, editing the message as her words arrive."""
        loop = asyncio.get_running_loop()
        pacer = StreamPacer()
        buffer = ""
        message = await channel.send("…")
        overflow: list[str] = []

        def pump(queue: asyncio.Queue):
            """Run the blocking HTTP stream off the event loop."""
            try:
                for chunk in clem.chat_stream(prompt):
                    loop.call_soon_threadsafe(queue.put_nowait, chunk)
            except Exception as exc:                     # noqa: BLE001
                loop.call_soon_threadsafe(queue.put_nowait, exc)
            finally:
                loop.call_soon_threadsafe(queue.put_nowait, None)

        queue: asyncio.Queue = asyncio.Queue()
        await loop.run_in_executor(None, lambda: None)   # warm the pool
        task = loop.run_in_executor(None, pump, queue)

        failure: Exception | None = None
        while True:
            item = await queue.get()
            if item is None:
                break
            if isinstance(item, Exception):
                failure = item
                break
            buffer += item
            now = loop.time()
            if pacer.should_push(now, len(buffer)):
                pieces = split_for_discord(buffer)
                head = pieces[0]
                if len(pieces) > 1:
                    # The first message is full; freeze it and carry the
                    # remainder into a fresh one.
                    await message.edit(content=head)
                    overflow.append(head)
                    buffer = "".join(pieces[1:])
                    message = await channel.send("…")
                else:
                    await message.edit(content=head + TYPING_TAIL)
                pacer.pushed(now, len(buffer))
        await task

        if failure is not None:
            await message.edit(content=_explain(failure, clem))
            return
        final = split_for_discord(buffer)
        if not final:
            await message.edit(content="*(she said nothing)*")
            return
        await message.edit(content=final[0])
        for piece in final[1:]:
            await channel.send(piece)

    @client.event
    async def on_ready():
        print(f"Connected as {client.user}. Answering "
              f"{len(owners)} allowed user(s).")

    @client.event
    async def on_message(message):
        mentioned = client.user in getattr(message, "mentions", [])
        if not should_answer(
                author_id=message.author.id,
                is_dm=message.guild is None,
                mentioned=mentioned,
                author_is_self=message.author == client.user,
                owners=owners):
            return

        text = strip_mentions(message.content,
                              client.user.id if client.user else None)

        async with message.channel.typing():
            try:
                await _handle(message.channel, text, send_long, stream_reply)
            except (ClementineOffline, ClementineAPIError) as exc:
                await message.channel.send(_explain(exc, clem))

    async def _handle(channel, text, send_long, stream_reply):
        loop = asyncio.get_running_loop()

        def off(fn, *a):
            return loop.run_in_executor(None, fn, *a)

        if text in ("!help", "help", ""):
            return await channel.send(HELP)
        if text == "!status":
            return await channel.send(format_status(await off(clem.status)))
        if text == "!memories":
            return await send_long(channel, format_memories(await off(clem.memories)))
        if text == "!reflect":
            return await send_long(channel, await off(clem.reflect) or "*(nothing came)*")
        if text.startswith("!teach "):
            body = text[len("!teach "):].strip()
            key = ""
            if ":" in body.split("\n")[0]:
                maybe_key, rest = body.split(":", 1)
                # A short leading token before the colon reads as a name
                # for the fact; a long one is just a sentence with a colon
                # in it, and turning that into a handle would be a mess.
                if maybe_key.strip() and len(maybe_key.strip()) <= 40:
                    key, body = maybe_key.strip(), rest.strip()
            await off(clem.teach, body, key)
            return await channel.send(
                f"Kept it{f' as `{key}`' if key else ''}.")
        if text.startswith("!forget "):
            handle = text[len("!forget "):].strip()
            res = await off(clem.forget, handle)
            return await channel.send(
                f"Forgot {res.get('forgotten')}." if res.get("ok")
                else f"Nothing here is called `{handle}`.")
        return await stream_reply(channel, text)

    return client


def _explain(exc: Exception, clem: Clementine) -> str:
    """Turn a failure into something worth reading on a phone."""
    if isinstance(exc, ClementineOffline):
        return describe_offline(clem.base)
    if isinstance(exc, ClementineAPIError):
        return f"She answered with an error ({exc.status}): {exc.body}"
    return f"Something went wrong: {exc}"


def check_report(*, api_ok: bool, api_detail: str, token_present: bool,
                 owners: set[int], gateway: str, gateway_detail: str) -> str:
    """The `--check` output, assembled where it can be tested.

    Written as a checklist because the question it answers — "is this
    working?" — has four independent parts, and a single pass/fail hides
    which one is broken. Each line says what to do about a failure, since
    the person reading it is usually mid-setup rather than debugging.
    """
    def mark(ok):
        return "  ok  " if ok else " FAIL "

    lines = ["Clementine · Discord — check", ""]

    lines.append(f"[{mark(api_ok)}] the companion")
    lines.append(f"          {api_detail}")
    if not api_ok:
        lines.append("          → run `python server.py` on that machine first")

    lines.append(f"[{mark(token_present)}] DISCORD_TOKEN")
    if not token_present:
        lines.append("          → not set. Developer portal → Bot → Reset Token")

    lines.append(f"[{mark(bool(owners))}] allowlist")
    if owners:
        lines.append(f"          {len(owners)} allowed: "
                     + ", ".join(str(o) for o in sorted(owners)))
    else:
        lines.append("          → CLEMENTINE_DISCORD_OWNERS is empty. Discord "
                     "→ Settings → Advanced → Developer Mode,")
        lines.append("            then right-click your name → Copy User ID")

    lines.append(f"[{mark(gateway == 'ok')}] Discord gateway")
    lines.append(f"          {gateway_detail}")
    if gateway == "intent":
        lines.append("          → Developer portal → your app → Bot →")
        lines.append("            turn on MESSAGE CONTENT INTENT, then re-run")
    elif gateway == "token":
        lines.append("          → the token was rejected. Reset it and copy "
                     "the whole thing")
    elif gateway == "network":
        lines.append("          → could not reach Discord. Check the "
                     "machine's connection")
    elif gateway == "skipped":
        # Distinct from a rejected token: nothing was tried, so telling
        # someone to reset a token they never made is a wrong instruction
        # at the exact moment they are following instructions.
        lines.append("          → set DISCORD_TOKEN and run --check again")

    everything = api_ok and token_present and bool(owners) and gateway == "ok"
    lines.append("")
    lines.append("All four green — DM the bot and she'll answer." if everything
                 else "Fix the lines marked FAIL above, then run --check again.")
    return "\n".join(lines)


async def _probe_gateway(token: str) -> tuple[str, str]:  # pragma: no cover
    """Log in, become ready, and disconnect. Returns (code, detail).

    Logging in alone would validate the token but not the intents —
    privileged intents are only rejected during the gateway handshake, and
    a missing MESSAGE CONTENT INTENT is by far the most confusing failure
    (the bot connects happily and then appears deaf). So this goes all the
    way to ready and then closes.
    """
    import discord

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    seen: dict = {}

    @client.event
    async def on_ready():
        seen["user"] = str(client.user)
        seen["guilds"] = len(client.guilds)
        await client.close()

    try:
        await asyncio.wait_for(client.start(token), timeout=45)
    except discord.PrivilegedIntentsRequired:
        return "intent", ("connected, but Discord refused the message-content "
                          "intent — the bot would see your messages with the "
                          "text stripped out")
    except discord.LoginFailure:
        return "token", "Discord rejected the token"
    except asyncio.TimeoutError:
        return "network", "timed out after 45s without becoming ready"
    except Exception as exc:                              # noqa: BLE001
        return "network", f"{type(exc).__name__}: {exc}"
    finally:
        if not client.is_closed():
            await client.close()

    if "user" not in seen:
        return "network", "the connection closed before becoming ready"
    return "ok", (f"connected as {seen['user']}, in {seen['guilds']} server(s); "
                  "message-content intent granted")


def run_check(token: str, owners: set[int], base: str) -> int:  # pragma: no cover
    clem = Clementine(base=base)
    try:
        who = clem.status()
        api_ok, api_detail = True, (
            f"{who.get('name') or 'Clementine'} at {base}, "
            f"model {who.get('model')}")
    except ClementineOffline:
        api_ok, api_detail = False, f"nothing answering at {base}"
    except ClementineAPIError as exc:
        api_ok, api_detail = False, f"{base} answered {exc.status}"

    if token:
        gateway, gateway_detail = asyncio.run(_probe_gateway(token))
    else:
        gateway, gateway_detail = "skipped", "not attempted — no token set"

    print(check_report(api_ok=api_ok, api_detail=api_detail,
                       token_present=bool(token), owners=owners,
                       gateway=gateway, gateway_detail=gateway_detail))
    return 0 if (api_ok and token and owners and gateway == "ok") else 1


def main() -> int:  # pragma: no cover - entry point
    token = os.environ.get("DISCORD_TOKEN", "").strip()
    owners = parse_owner_ids(os.environ.get("CLEMENTINE_DISCORD_OWNERS", ""))
    base = os.environ.get("CLEMENTINE_API", "http://127.0.0.1:5000")

    if "--check" in sys.argv[1:]:
        # Deliberately runs before the refusals below: --check exists to
        # tell you what is missing, so it must not itself refuse to run
        # because something is missing.
        return run_check(token, owners, base)

    if not token:
        print("DISCORD_TOKEN is not set. See DISCORD.md.", file=sys.stderr)
        return 2
    if not owners:
        # Refusing is the whole point: an allowlist that defaults to
        # everyone is not an allowlist, and this bot can write to memory.
        print("CLEMENTINE_DISCORD_OWNERS is not set. Refusing to start: an "
              "open bot lets anyone who can see it write to her memory.\n"
              "Set it to your Discord user id (see DISCORD.md).",
              file=sys.stderr)
        return 2

    clem = Clementine(base=base)
    try:
        who = clem.status()
        print(f"Talking to {who['name']} on {base} (model {who['model']}).")
    except ClementineOffline:
        # A warning, not a refusal: starting the bot before the server is
        # a reasonable order to do things in, and it will connect when the
        # first message arrives.
        print(describe_offline(base), file=sys.stderr)
        print("Starting anyway — she'll answer once that's running.",
              file=sys.stderr)

    build_client(clem, owners).run(token)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

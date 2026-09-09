# Clementine on Discord

Reach the local companion from a phone without giving up what makes her
local.

The trade this project keeps running into: the **local** build is the
honest one — model on your machine, memory in files you own, nothing
leaves — and it is unreachable from a phone. The **web** build reaches
your phone by sending your words to a hosted model, which is the opposite
trade.

Discord threads the needle. The bot connects **outward** to Discord's
gateway, so nothing is exposed and no port is opened: the machine at home
reaches out, and the phone in your pocket talks to Discord. Free, no API
key, and on iOS the keyboard's 🎤 key means you can talk rather than type.

## What this costs you, plainly

| | |
|---|---|
| The model answering | **your machine.** Never leaves. |
| Her memory | **your machine.** Plain files on your disk. |
| Your messages, in transit | **through Discord.** They hold them, on their servers, under their terms. |

So this is not the sovereign path — Discord is a third party and reading
your messages is within their power. It is a deliberate middle: you give
up transport privacy to get reach, and you keep the two things this
project cares most about. If that trade is wrong for you, the terminal
interface on the machine itself gives up nothing.

## Setting it up

**1 · Make the bot**

1. Go to <https://discord.com/developers/applications> → **New Application**.
2. **Bot** in the sidebar → **Reset Token** → copy it. This is a password;
   treat it like one.
3. On the same page, turn on **MESSAGE CONTENT INTENT**. Without it the
   bot connects fine and then appears deaf — it receives your messages
   with the text stripped out. This is the single most confusing way the
   setup can fail.
4. **OAuth2 → URL Generator**: scope `bot`, permissions *Send Messages*
   and *Read Message History*. Open the generated URL to add it to a
   server. (For DM-only use you still need it added to one server first.)

**2 · Find your user id**

In Discord: **Settings → Advanced → Developer Mode** on, then right-click
your own name → **Copy User ID**. It is a long number.

**3 · Run it**

```bash
pip install -r requirements.txt -r requirements-discord.txt

python server.py                      # terminal 1 — the companion

export DISCORD_TOKEN='your-token'     # terminal 2 — the bot
export CLEMENTINE_DISCORD_OWNERS='your-user-id'
python discord_bot.py
```

Then DM the bot. That is the whole thing.

## Confirming it works

```bash
python discord_bot.py --check
```

Four independent things have to be true, and one pass/fail would hide
which one isn't. So it checks them separately and each failure says what
to do:

```
Clementine · Discord — check

[  ok  ] the companion
          Clementine at http://127.0.0.1:5000, model llama3.1:8b
[  ok  ] DISCORD_TOKEN
[  ok  ] allowlist
          1 allowed: 123456789012345678
[  ok  ] Discord gateway
          connected as Clementine#1234, in 1 server(s);
          message-content intent granted

All four green — DM the bot and she'll answer.
```

It logs in, waits to become ready, then disconnects. Going all the way to
ready is the point: **logging in validates the token, but the intents are
only checked during the gateway handshake.** A missing MESSAGE CONTENT
INTENT lets the bot connect happily and then appear deaf, and that is the
failure this exists to catch before you spend an evening on it.

`--check` runs before the bot's own refusals, so it works when nothing is
set up yet — that is when you need it most. Exit code is 0 only when all
four pass.

## The allowlist is not optional

`CLEMENTINE_DISCORD_OWNERS` has no default and the bot **refuses to
start** without it.

This is deliberate. The bot can write to her memory — `!teach`, and
ordinary conversation, both leave marks. A bot that answers anyone who can
see it hands that to strangers. An allowlist that defaults to everyone is
not an allowlist.

Several ids, if you want more than one person:
`CLEMENTINE_DISCORD_OWNERS='123,456'`.

## Talking to her

A DM is enough. In a shared channel, mention her.

| | |
|---|---|
| `!status` | who's running, on which model |
| `!memories` | everything she's holding |
| `!teach <text>` | give her something to keep |
| `!teach key: <text>` | keep it as a named fact |
| `!forget <handle>` | remove one memory |
| `!reflect` | ask her to look back over it all |
| `!help` | the same list |

Replies stream: the message is edited into place as her words arrive,
about once a second. Answers over Discord's 2000-character limit continue
into a second message rather than being cut.

## Settings

| variable | default | |
|---|---|---|
| `DISCORD_TOKEN` | — | required |
| `CLEMENTINE_DISCORD_OWNERS` | — | required; refuses to start without it |
| `CLEMENTINE_API` | `http://127.0.0.1:5000` | where `server.py` is listening |

`CLEMENTINE_API` exists so the bot and the companion can live on different
machines on the same network. That means widening the server past
`127.0.0.1`, which it has no flag for and no auth story behind — if you do
it, you have removed the property that makes this the sovereign version,
and you are on your own.

## Known limits

- **One companion at a time.** Profile switching is a property of the
  server, not of the conversation, so several people talking at once would
  share one profile and step on each other. Owner-only sidesteps this
  rather than solving it. Per-user profiles need the server to hold more
  than one companion, which it does not yet.
- **The machine has to be awake.** No machine, no Clementine. When the
  server is unreachable the bot says which address it tried and that
  `server.py` may not be running, rather than failing silently.
- **A code block split across two messages loses its fence.** Splitting
  prefers paragraph, then line, then sentence, then word boundaries, and
  it never drops a character — but it does not know about Markdown, so a
  fenced block broken across the 2000-character line renders as plain
  text in the second half.
- **Not tested against a live Discord gateway.** Everything below the
  socket is covered: the `on_message` handler is driven end to end by
  `tests/test_discord_handlers.py` — real `discord.Client`, real handler,
  real HTTP client, real Flask app, with only Discord's `Message` and
  `Channel` standing in — and the API client is also exercised against a
  live server. What nobody has done is point it at a real bot token;
  there is no Discord account in the build container. `--check` exists
  precisely because that last step can only be taken on your machine.
- **Voice notes are not transcribed.** Sending an audio message does
  nothing. Use the keyboard's dictation key, which is the phone's own
  speech-to-text and never reaches this code.

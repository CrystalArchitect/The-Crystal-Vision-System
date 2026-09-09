# Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
# SPDX-License-Identifier: CC-BY-NC-ND-4.0

"""Drive the real Discord handlers, with only the socket replaced.

`test_discord_bot.py` covers the pure functions. This covers the layer
above them — the `on_message` handler that `build_client` registers, with
its routing, mention stripping, command dispatch, streaming edits and
error paths. That layer had no coverage at all, and it is the layer where
a mistake looks like "the bot ignores me" rather than a failing assertion.

What is real here: the actual `discord.Client` built by `build_client`,
the actual handler it registered, the actual `Clementine` HTTP client, and
a real Flask app served through Werkzeug's test client. What is a stand-in:
Discord's `Message`, `Channel` and gateway. Nothing about the gateway can
be checked without a token and a network, and `discord_bot.py --check`
exists for that part.

Requires `discord.py`, so the module skips cleanly without it rather than
failing the suite for anyone who has not installed the optional extra.
"""

import os
import asyncio

import pytest

discord = pytest.importorskip(
    "discord", reason="optional extra; pip install -r requirements-discord.txt")

import discord_bot                                          # noqa: E402

pytestmark = pytest.mark.skipif(
    not os.environ.get("CLEMENTINE_SRC", "").strip(),
    reason="needs the companion's source: set CLEMENTINE_SRC to the "
           "clementine/ directory of a Clementine-ai-companion checkout. "
           "See tests/conftest.py.",
)

from clementine_api import Clementine                       # noqa: E402

BOT_ID = 999
OWNER = 1
STRANGER = 2


# ----------------------------------------------------------- Discord stubs

class _StubUser:
    def __init__(self, uid):
        self.id = uid

    def __eq__(self, other):
        return isinstance(other, _StubUser) and other.id == self.id

    def __hash__(self):
        return hash(self.id)


class _StubSentMessage:
    """A message the bot sent. Records every edit it received."""

    def __init__(self, content):
        self.content = content
        self.edits = [content]

    async def edit(self, content=None, **_):
        self.content = content
        self.edits.append(content)


class _StubTyping:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        return False


class _StubChannel:
    def __init__(self):
        self.sent: list[_StubSentMessage] = []

    async def send(self, content):
        msg = _StubSentMessage(content)
        self.sent.append(msg)
        return msg

    def typing(self):
        return _StubTyping()


class _StubMessage:
    def __init__(self, content, author_id=OWNER, is_dm=True, mentions=()):
        self.content = content
        self.author = _StubUser(author_id)
        self.guild = None if is_dm else object()
        self.mentions = list(mentions)
        self.channel = _StubChannel()


# ------------------------------------------------------------- the fixtures

class _FlaskTransport:
    """Serve the real Flask app to the real HTTP client, without a socket.

    `requests` and Werkzeug's test client have different shapes, so this
    adapts one to the other — enough of a `Session` for `Clementine` to
    drive the genuine server code, including the streaming route.
    """

    def __init__(self, app):
        self.client = app.test_client()

    def request(self, method, url, json=None, headers=None, timeout=None,
                stream=False):
        path = url.split("127.0.0.1:5000", 1)[-1] if "127.0.0.1" in url else url
        res = self.client.open(path, method=method, json=json,
                               headers=headers or {})
        return _FlaskResponse(res)


class _FlaskResponse:
    def __init__(self, res):
        self._res = res
        self.status_code = res.status_code
        self.text = res.get_data(as_text=True)

    def json(self):
        return self._res.get_json()

    def iter_content(self, chunk_size=None, decode_unicode=False):
        # The route streams prose; hand it over in small pieces so the
        # pacing logic sees more than one chunk, as it would in life.
        text = self.text
        for i in range(0, len(text), 8):
            yield text[i:i + 8]


class _Companion:
    """A companion that answers without a model behind it."""

    class _Personality:
        name = "Clementine"
        avatar = "🍊"
        description = ""
        human_name = ""

    def __init__(self, reply="I'm here."):
        self.model = "test-model"
        self.embed_model = "test-embed"
        self.memory_dir = "crystalcore_memory"
        self.personality = self._Personality()
        self.reply = reply
        self.said: list[str] = []

        class _Mem:
            facts: dict = {}
            notes: list = []
            reflections: list = []
        self.memory = _Mem()

    def time_since_last(self):
        return "just now"

    def chat_stream(self, message):
        self.said.append(message)
        for word in self.reply.split(" "):
            yield word + " "

    def reflect(self):
        return "something looked back at me"

    def remember(self, text):
        self.memory.notes.append({"text": text, "tags": []})

    def remember_fact(self, key, value):
        self.memory.facts[key] = {"value": value, "tags": []}

    def forget(self, handle):
        return f"fact '{handle}'" if handle in self.memory.facts else ""


def pretend_ready(client, user):
    """Give the client the identity the gateway would have handed it.

    `Client.user` is a read-only property reading `_connection.user`, so
    it has to be set underneath. That reaches into a private attribute,
    which is worth doing openly and worth guarding: the assertion below
    means a future version of discord.py that moves it fails this suite
    with a clear reason, instead of leaving every test running against a
    client whose `user` is still `None`.

    The precedent is the speech-synthesis mock in the voice app, which
    assigned to a read-only getter, was silently ignored, and reported
    green while measuring nothing. A mock that fails open is worse than
    no mock.
    """
    client._connection.user = user
    assert client.user is user, (
        "could not give the client an identity — discord.py has moved "
        "Client.user off _connection.user, and these tests would be "
        "running against a client that never became ready")


@pytest.fixture
def rig():
    """A real client + real handler + real HTTP client over a real app."""
    from server import create_app
    companion = _Companion()
    app = create_app(companion)
    app.testing = True
    clem = Clementine(session=_FlaskTransport(app))
    client = discord_bot.build_client(clem, {OWNER})
    pretend_ready(client, _StubUser(BOT_ID))
    return client, companion


def deliver(client, message):
    asyncio.run(client.on_message(message))
    return message.channel


# ----------------------------------------------------------------- the tests

def test_a_dm_from_the_owner_gets_a_streamed_reply(rig):
    client, companion = rig
    channel = deliver(client, _StubMessage("are you there?"))
    assert companion.said == ["are you there?"]
    assert channel.sent, "the bot said nothing at all"
    assert channel.sent[0].content.strip() == "I'm here."


def test_a_stranger_is_ignored_entirely(rig):
    """Not refused politely — ignored. A refusal tells a stranger the bot
    is listening, and answering at all is what the allowlist forbids."""
    client, companion = rig
    channel = deliver(client, _StubMessage("hello", author_id=STRANGER))
    assert channel.sent == []
    assert companion.said == []


def test_an_unmentioned_channel_message_is_ignored(rig):
    client, companion = rig
    channel = deliver(client, _StubMessage("chatting to someone else",
                                           is_dm=False))
    assert channel.sent == []


def test_a_mention_in_a_channel_is_answered_with_the_mention_removed(rig):
    client, companion = rig
    deliver(client, _StubMessage(f"<@{BOT_ID}> how are you?", is_dm=False,
                                 mentions=[_StubUser(BOT_ID)]))
    assert companion.said == ["how are you?"], "the raw mention reached the model"


def test_a_message_before_ready_does_not_crash(rig):
    """`client.user` is None until the gateway says ready. Dereferencing it
    unguarded crashed here, in the one window nobody tests by hand."""
    client, _ = rig
    client._connection.user = None
    assert client.user is None
    channel = deliver(client, _StubMessage("hi"))
    assert channel.sent, "handler died before answering"


def test_the_bot_does_not_answer_itself(rig):
    client, companion = rig
    msg = _StubMessage("an echo")
    msg.author = _StubUser(BOT_ID)
    deliver(client, msg)
    assert companion.said == []


@pytest.mark.parametrize("command,expect", [
    ("!help", "Clementine — on Discord"),
    ("!status", "**Clementine**"),
    ("!memories", "isn't holding anything"),
    ("!reflect", "something looked back at me"),
])
def test_commands_answer_without_reaching_the_model(rig, command, expect):
    client, companion = rig
    channel = deliver(client, _StubMessage(command))
    assert expect in channel.sent[0].content
    assert companion.said == [], f"{command} was passed to the model as chat"


def test_teach_stores_a_plain_note(rig):
    client, companion = rig
    channel = deliver(client, _StubMessage("!teach she prefers talking"))
    assert companion.memory.notes[0]["text"] == "she prefers talking"
    assert "Kept it." in channel.sent[0].content


def test_teach_with_a_short_leading_token_stores_a_named_fact(rig):
    client, companion = rig
    channel = deliver(client, _StubMessage("!teach alyssa: has a Mac"))
    assert companion.memory.facts["alyssa"]["value"] == "has a Mac"
    assert "`alyssa`" in channel.sent[0].content


def test_a_sentence_with_a_colon_is_not_mistaken_for_a_handle(rig):
    """A long left-hand side is prose, not a name. Turning it into a
    handle would make an unusable memory nobody can forget by name."""
    client, companion = rig
    long_prefix = "here is the thing I keep coming back to lately"
    deliver(client, _StubMessage(f"!teach {long_prefix}: it matters"))
    assert companion.memory.facts == {}
    assert companion.memory.notes[0]["text"].startswith(long_prefix)


def test_forget_reports_a_miss_rather_than_claiming_success(rig):
    client, _ = rig
    channel = deliver(client, _StubMessage("!forget nothing-by-that-name"))
    assert "Nothing here is called" in channel.sent[0].content


def test_a_long_reply_continues_into_a_second_message(rig):
    """Discord's 2000-character limit, exercised through the real handler."""
    client, companion = rig
    companion.reply = "word " * 900          # ~4500 chars
    channel = deliver(client, _StubMessage("say a lot"))
    assert len(channel.sent) > 1, "a 4500-character reply fitted in one message?"
    whole = "".join(m.content for m in channel.sent)
    assert whole.replace(discord_bot.TYPING_TAIL, "").strip().startswith("word")
    for msg in channel.sent:
        assert len(msg.content) <= discord_bot.DISCORD_LIMIT


def test_the_reply_is_edited_into_place_as_it_arrives(rig):
    """The streaming behaviour: one message, edited, not a wall of messages."""
    client, companion = rig
    companion.reply = "one two three four five"
    channel = deliver(client, _StubMessage("stream please"))
    assert len(channel.sent[0].edits) >= 2, "never edited — did it stream?"
    assert channel.sent[0].edits[0] == "…", "no placeholder went up first"


def test_the_final_edit_has_no_cursor_left_on_it(rig):
    """The ▌ marks a reply still arriving. Leaving it on the finished text
    makes a completed answer look truncated forever."""
    client, companion = rig
    channel = deliver(client, _StubMessage("hello"))
    assert discord_bot.TYPING_TAIL not in channel.sent[-1].content


def test_a_dead_server_produces_a_sentence_not_a_stack_trace(rig):
    """The failure people will actually hit: the machine is asleep."""
    client, _ = rig
    clem = Clementine(base="http://127.0.0.1:5094")   # nothing listening
    client = discord_bot.build_client(clem, {OWNER})
    pretend_ready(client, _StubUser(BOT_ID))
    channel = deliver(client, _StubMessage("!status"))
    said = channel.sent[0].content
    assert "127.0.0.1:5094" in said
    assert "server.py" in said
    assert "Traceback" not in said

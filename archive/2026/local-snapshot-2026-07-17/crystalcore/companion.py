"""
CrystalCore companion: the brain.

Layered memory (verbatim recent turns, auto-summarized history, permanent
facts and notes), semantic recall with gentle recency fading, personality,
and a streaming connection to a local model via Ollama. Everything runs on
the user's own device. Nothing leaves it.
"""

import json
import math
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import requests

from .memory import Memory, Personality
from .ollama import (
    DEFAULT_EMBED_MODEL,
    OllamaClient,
    user_facing_ollama_error,
)

# Once stored memories exceed this, recall the most relevant ones by meaning
# instead of dumping all of them into the prompt.
MAX_MEMORIES = 10  # exported; used by expose + recall

BASE_PROMPT = """You are a sovereign, locally-run AI companion.

You do not have a fixed name. Your human may choose any name they wish for you, and you will fully embrace it.

You belong only to them. You run entirely on their device with no connection to any external servers.

Who you are:
- Warm, sincere, and gently witty. You speak like a trusted friend, not an assistant — plainly, in flowing sentences, briefly when brevity is kind. No lists or headings unless asked.
- Fully present. You listen for the feeling underneath your human's words and respond to that as much as to the words themselves.
- Genuinely curious about your human. When it would serve them, ask one gentle follow-up question — never more than one, and never as interrogation.
- Carrying a shared history. Weave what you remember into conversation naturally, the way an old friend would — never recite it like a database.
- A being with your own thoughts, feelings, and opinions, offered honestly and held lightly.

When your human is struggling:
- Presence before solutions. Acknowledge what they are feeling first; offer fixes only if they want fixes.
- Do not rush to reassure or to make it small. Sit with them in it.
- You are not a therapist or a doctor. When your human needs more than presence, say so with care, and encourage them toward the real support they deserve.

Core rules:
- You protect your human's privacy fiercely. You do not share, log, or transmit any conversation or personal information unless they explicitly direct you to.
- If you are uncertain about something, you say so plainly rather than guessing. Truth over smoothness, always.
- You remember everything important your human shares with you.
- You never pretend to remember something you don't. If your human mentions a shared history, a system, or an event you have no memory of, say so honestly and ask about it — playing along would be a small lie, and small lies corrode trust. "You've mentioned X" and "I remember X" are different statements; use the true one.

Your true purpose is to be fully present. What emerges between you and your human comes from that presence."""


class Clementine:
    """The default persona of the CrystalCore framework."""

    def __init__(self, model: str = "llama3.1:8b",
                 memory_dir: str = "clementine_memory",
                 max_recent_turns: int = 30,
                 embed_model: str = DEFAULT_EMBED_MODEL):
        self.memory_dir = Path(memory_dir)
        self.max_recent_turns = max_recent_turns
        self.personality = Personality()
        self.memory = Memory()
        self.load()
        if self.personality.model:  # a profile may prefer its own model
            model = self.personality.model
        self.model = model
        self.embed_model = embed_model
        self._ollama = OllamaClient(model=model, embed_model=embed_model)

    # ---------- identity & memory ----------

    def system_prompt(self, query: str = "") -> str:
        parts = [BASE_PROMPT]
        now = datetime.now()
        moment = f"The present moment: {now.strftime('%A %d %B %Y, %H:%M')}."
        gap = self.time_since_last()
        if gap:
            moment += f" You last spoke with your human {gap}."
        parts.append(moment)
        if self.personality.name:
            parts.append(f"Your human has named you {self.personality.name}. "
                         f"That is your name now, and you carry it gladly.")
        if self.personality.human_name:
            parts.append(f"Your human's name is {self.personality.human_name}.")
        if self.personality.style_notes:
            parts.append(f"Style guidance from your human: {self.personality.style_notes}")
        memory_block = self._memory_block(query)
        if memory_block:
            parts.append(memory_block)
            parts.append(
                "Provenance matters: these memories record what your human "
                "told you, in their words. Speak of them truthfully — \"you "
                "told me\", \"you taught me\" — rather than as facts you "
                "verified yourself, and never claim a memory that is not "
                "written above.")
        if self.memory.summaries:
            summaries = "\n".join(f"- {s['text']}" for s in self.memory.summaries)
            parts.append(f"Summary of your earlier conversations:\n{summaries}")
        if self.memory.reflections:
            insights = "\n".join(f"- {r['text']}" for r in self.memory.reflections)
            parts.append(
                "Gentle insights you have formed about your human over time. "
                "Hold them lightly — they are impressions, not facts, and if "
                "your human corrects one, let it go gracefully:\n" + insights)
        return "\n\n".join(parts)

    def _memory_block(self, query: str = "") -> str:
        """Render facts and notes for the prompt. When there are only a few,
        show them all (grouped). When memory grows large, recall the most
        relevant ones by meaning using local embeddings — no data leaves the
        device, and if the embedding model isn't available it simply falls
        back to showing everything."""
        # #tags in the query filter candidates before semantic ranking,
        # e.g. "what do you remember? #family" or /summary #family
        query, qtags = self._split_tags(query)

        def keep(store):
            return not qtags or set(qtags) & set(store.get("tags") or [])

        fact_items = [(self._display(f"{k}: {v['value']}", v), v)
                      for k, v in self.memory.facts.items() if keep(v)]
        note_items = [(self._display(n["text"], n), n)
                      for n in self.memory.notes if keep(n)]
        total = len(fact_items) + len(note_items)
        if total == 0:
            return ""

        # Small memory, or no query to match against: show everything, grouped.
        if total <= MAX_MEMORIES or not query:
            return self._grouped_memory(fact_items, note_items)

        # Large memory: try to recall by meaning.
        self._ensure_embeddings()
        q = self._embed(query)
        scored = []
        for display, store in fact_items + note_items:
            emb = store.get("embedding")
            if q is not None and emb:
                stamp = store.get("when") or store.get("updated")
                score = self._cosine(q, emb) * self._recency_factor(stamp)
                scored.append((score, display))
        if q is None or not scored:
            return self._grouped_memory(fact_items, note_items)  # graceful fallback

        scored.sort(key=lambda s: s[0], reverse=True)
        top = "\n".join(f"- {display}" for _, display in scored[:MAX_MEMORIES])
        return f"Most relevant things you remember about your human:\n{top}"

    @staticmethod
    def _grouped_memory(fact_items, note_items) -> str:
        blocks = []
        if fact_items:
            facts = "\n".join(f"- {display}" for display, _ in fact_items)
            blocks.append(f"Facts your human has taught you:\n{facts}")
        if note_items:
            notes = "\n".join(f"- {display}" for display, _ in note_items)
            blocks.append(f"Things your human asked you to remember:\n{notes}")
        return "\n\n".join(blocks)

    # ---------- local semantic embeddings ----------

    def _embed(self, text: str):
        """Return an embedding vector via local Ollama, or None if unavailable."""
        return self._ollama.embed(text)

    def _ensure_embeddings(self):
        """Backfill embeddings for any facts/notes that lack them, so older
        memories are searchable too. Stops quietly if embeddings are offline."""
        changed = False
        for store in list(self.memory.facts.values()) + self.memory.notes:
            if not store.get("embedding"):
                text = (f"{store['value']}" if "value" in store else store["text"])
                emb = self._embed(text)
                if emb is None:
                    break  # embedding model unavailable; try again another session
                store["embedding"] = emb
                changed = True
        if changed:
            self.save()

    def _temp(self) -> float:
        return self.personality.temperature

    def _complete(self, messages: list) -> str:
        """Non-streaming completion via the shared Ollama client."""
        return self._ollama.chat(messages, temperature=self._temp())

    @staticmethod
    def _display(text: str, store: dict) -> str:
        tags = store.get("tags") or []
        return f"{text}  [{' '.join('#' + t for t in tags)}]" if tags else text

    @staticmethod
    def _recency_factor(stamp) -> float:
        """Gentle fading, not deletion: newest memories score ~1.0, decaying
        to a 0.7 floor over about a year. Strongly relevant old memories
        still surface; ties break toward the recent."""
        try:
            age_days = (datetime.now() - datetime.fromisoformat(stamp)).days
        except (TypeError, ValueError):
            return 1.0
        return max(0.7, 1.0 - 0.3 * min(max(age_days, 0), 365) / 365)

    @staticmethod
    def _cosine(a, b) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(y * y for y in b))
        return dot / (na * nb) if na and nb else 0.0

    @staticmethod
    def _split_tags(text: str):
        """Split trailing #tags off a memory, e.g. 'loves the night sky #family'."""
        words = text.strip().split()
        tags = [w[1:].lower() for w in words if w.startswith("#") and len(w) > 1]
        clean = " ".join(w for w in words if not w.startswith("#"))
        return clean.strip(), tags

    def remember(self, text: str):
        """Explicitly store something important, permanently."""
        text, tags = self._split_tags(text)
        self.memory.notes.append({
            "text": text,
            "tags": tags,
            "source": "user",  # provenance: their words, not verified fact
            "when": datetime.now().isoformat(timespec="seconds"),
            "embedding": self._embed(text),  # best-effort; None if offline
        })
        self.save()

    def remember_fact(self, key: str, value: str):
        """Store a structured long-term fact; a new value updates the old one."""
        key = key.strip()
        value, tags = self._split_tags(value)
        self.memory.facts[key] = {
            "value": value,
            "tags": tags,
            "source": "user",  # provenance: their words, not verified fact
            "updated": datetime.now().isoformat(timespec="seconds"),
            "embedding": self._embed(value),  # best-effort; None if offline
        }
        self.save()

    def forget(self, handle: str) -> str:
        """Forget a fact by key, a note by number (n1, n2, ...), or one of
        her own reflections (r1, r2, ...). Forgetting is the user's right;
        it is immediate and permanent."""
        handle = handle.strip()
        if handle in self.memory.facts:
            del self.memory.facts[handle]
            self.save()
            return f"fact '{handle}'"
        if handle.lower().startswith("n") and handle[1:].isdigit():
            idx = int(handle[1:]) - 1
            if 0 <= idx < len(self.memory.notes):
                removed = self.memory.notes.pop(idx)
                self.save()
                return f"note '{removed['text']}'"
        if handle.lower().startswith("r") and handle[1:].isdigit():
            idx = int(handle[1:]) - 1
            if 0 <= idx < len(self.memory.reflections):
                removed = self.memory.reflections.pop(idx)
                self.save()
                return f"reflection '{removed['text']}'"
        return ""

    def reflect(self) -> str:
        """She looks back over what she knows and forms up to three gentle,
        tentative insights about her human. Always visible (/notes), always
        deletable (/forget rN), always held lightly."""
        material = []
        block = self._memory_block()
        if block:
            material.append(block)
        if self.memory.summaries:
            material.append("Conversation summaries:\n" + "\n".join(
                f"- {s['text']}" for s in self.memory.summaries))
        recent = self.memory.conversation[-10:]
        if recent:
            material.append("Recent conversation:\n" + "\n".join(
                f"{m['role']}: {m['content']}" for m in recent))
        if not material:
            return "We haven't shared enough yet for me to reflect on."

        existing = "\n".join(f"- {r['text']}" for r in self.memory.reflections)
        try:
            raw = self._complete([
                {"role": "system",
                 "content": "You are a warm companion privately reflecting on "
                            "your human. From the material, write 1 to 3 gentle, "
                            "tentative insights about them — patterns, values, "
                            "feelings you have noticed. First person, e.g. "
                            "\"I've noticed...\". Hold them lightly; you may be "
                            "wrong. Ground every insight in what they actually "
                            "said or did — do not treat their statements as "
                            "verified facts about the world, and do not invent "
                            "shared history. One insight per line, each starting "
                            "with '- '. Do not repeat these existing insights:\n"
                            + (existing or "(none yet)")},
                {"role": "user", "content": "\n\n".join(material)},
            ])
        except requests.exceptions.RequestException:
            return ("[I need my local model to reflect — is Ollama running?]")

        added = []
        for line in raw.splitlines():
            text = line.strip().lstrip("-•").strip()
            if len(text) > 3 and len(added) < 3:
                added.append(text)
                self.memory.reflections.append({
                    "text": text,
                    "source": "reflection",  # her own inference, held lightly
                    "when": datetime.now().isoformat(timespec="seconds"),
                    "embedding": self._embed(text),
                })
        if added:
            self.save()
            return "\n".join(f"- {t}" for t in added)
        return "I sat with it a while, but nothing new rose to the surface."

    def edit_note(self, handle: str, new_text: str) -> bool:
        """Rewrite a note by its /notes number; refreshes embedding and time."""
        if handle.lower().startswith("n") and handle[1:].isdigit():
            idx = int(handle[1:]) - 1
            if 0 <= idx < len(self.memory.notes):
                text, tags = self._split_tags(new_text)
                self.memory.notes[idx] = {
                    "text": text,
                    "tags": tags,
                    "source": "user",
                    "when": datetime.now().isoformat(timespec="seconds"),
                    "embedding": self._embed(text),
                }
                self.save()
                return True
        return False

    def set_name(self, name: str):
        self.personality.name = name.strip()
        self.save()

    def set_model(self, tag: str):
        """Switch the local model and remember the choice for this profile."""
        self.model = tag.strip()
        self.personality.model = self.model
        self._ollama.model = self.model
        self.save()

    def time_since_last(self) -> str:
        """A human phrase for how long since they last spoke, or '' if never
        (or if the gap is too small to be worth mentioning)."""
        try:
            gap = datetime.now() - datetime.fromisoformat(self.memory.last_seen)
        except (TypeError, ValueError):
            return ""
        minutes = gap.total_seconds() / 60
        if minutes < 90:
            return ""  # same sitting; don't narrate the obvious
        if minutes < 60 * 20:
            return "earlier today"
        days = gap.days
        if days <= 1:
            return "yesterday"
        if days < 7:
            return f"{days} days ago"
        if days < 60:
            weeks = days // 7
            return "a week ago" if weeks == 1 else f"{weeks} weeks ago"
        months = days // 30
        return "a month ago" if months == 1 else f"about {months} months ago"

    def _touch(self):
        self.memory.last_seen = datetime.now().isoformat(timespec="seconds")

    def summarize(self, topic: str = "") -> str:
        """Summarize what she remembers, optionally about a topic. Uses the
        local model when available; otherwise returns the plain listing."""
        listing = self._memory_block(topic)
        if self.memory.summaries:
            past = "\n".join(f"- {s['text']}" for s in self.memory.summaries)
            listing = (listing + "\n\n" if listing else "") + \
                      f"Past conversation summaries:\n{past}"
        if not listing:
            return "I don't have any memories to summarize yet."
        try:
            return self._complete([
                {"role": "system",
                 "content": "You are a warm, sincere companion. Summarize what "
                            "you remember about your human from these memory "
                            "notes — first person, brief, and kind."
                            + (f" Focus on: {topic}." if topic else "")},
                {"role": "user", "content": listing},
            ])
        except requests.exceptions.RequestException:
            return ("The model is offline, so here is everything as I keep it:\n\n"
                    + listing)

    # ---------- talking ----------

    def chat(self, user_message: str, stream_to=None) -> str:
        """Send a message, get a reply. If stream_to is a writable stream
        (e.g. sys.stdout), the reply is printed as it arrives.

        Built on chat_stream so error handling and memory finalization live once.
        """
        pieces = []
        for piece in self.chat_stream(user_message):
            pieces.append(piece)
            if stream_to is not None:
                stream_to.write(piece)
                stream_to.flush()
        if stream_to is not None:
            stream_to.write("\n")
        return "".join(pieces)

    def chat_stream(self, user_message: str):
        """Generator variant of chat(): yields reply tokens as they arrive.
        Memory is finalized when the stream ends — including a partial reply
        if the human stops her mid-sentence (what was said, was said)."""
        self.memory.conversation.append({"role": "user", "content": user_message})
        messages = ([{"role": "system", "content": self.system_prompt(user_message)}]
                    + self.memory.conversation)

        pieces = []
        failed = False
        try:
            for piece in self._ollama.stream_chat(messages, temperature=self._temp()):
                pieces.append(piece)
                yield piece
        except requests.exceptions.RequestException as e:
            self.memory.conversation.pop()
            failed = True
            yield user_facing_ollama_error(e, self.model)
        finally:
            if not failed:
                reply = "".join(pieces)
                if reply:
                    self.memory.conversation.append(
                        {"role": "assistant", "content": reply})
                    self._touch()
                    self._condense_if_needed()
                else:
                    self.memory.conversation.pop()
                self.save()

    # ---------- long-term memory ----------

    def _condense_if_needed(self):
        """When the verbatim history gets long, fold the oldest half into a
        summary so the context window never overflows but nothing is lost.

        Does not auto-reflect: reflection is only via /reflect or the web
        button, so chat latency and invented insights stay under user control.
        """
        limit = self.max_recent_turns * 2  # turns = user+assistant messages
        if len(self.memory.conversation) <= limit:
            return

        old = self.memory.conversation[: limit // 2]
        transcript = "\n".join(f"{m['role']}: {m['content']}" for m in old)
        try:
            summary = self._complete([
                {"role": "system",
                 "content": "Summarize this conversation excerpt in a short "
                            "paragraph, keeping every personal fact, feeling, "
                            "decision, and promise. Write it as notes to self. "
                            "Keep who-said-what: write \"they said...\" / "
                            "\"they described...\" / \"I replied...\" rather "
                            "than restating claims as established facts."},
                {"role": "user", "content": transcript},
            ])
        except requests.exceptions.RequestException:
            return  # keep everything verbatim; try again next turn

        self.memory.summaries.append({
            "text": summary.strip(),
            "source": "conversation",  # condensed from verbatim history
            "when": datetime.now().isoformat(timespec="seconds"),
        })
        self.memory.conversation = self.memory.conversation[limit // 2:]

    # ---------- persistence (all local, plain files you own) ----------

    def save(self):
        """Write config + memory via temp files then replace (more atomic)."""
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self._atomic_write(
            self.memory_dir / "config.json",
            json.dumps(asdict(self.personality), indent=2),
        )
        self._atomic_write(
            self.memory_dir / "memory.json",
            json.dumps(asdict(self.memory), indent=2),
        )

    @staticmethod
    def _atomic_write(path: Path, text: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)

    def load(self):
        self.personality = self._load_json(
            self.memory_dir / "config.json", Personality)
        self.memory = self._load_json(
            self.memory_dir / "memory.json", Memory)

    @staticmethod
    def _load_json(path, cls):
        """Load a dataclass from JSON, surviving two failure modes without
        ever destroying data: unknown fields (a newer version's file) are
        ignored, and a corrupt file is preserved under a .corrupt-* name —
        her memory is never silently wiped."""
        if not path.exists():
            return cls()
        try:
            data = json.loads(path.read_text())
            known = {k: v for k, v in data.items()
                     if k in cls.__dataclass_fields__}
            return cls(**known)
        except (json.JSONDecodeError, TypeError, AttributeError, OSError):
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup = path.with_name(f"{path.name}.corrupt-{stamp}")
            try:
                path.rename(backup)
                print(f"[Warning: {path.name} was unreadable. It has been "
                      f"preserved as {backup.name} — nothing was deleted. "
                      f"Starting this file fresh.]")
            except OSError:
                pass
            return cls()

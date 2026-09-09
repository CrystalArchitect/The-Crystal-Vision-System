"""
CrystalCore companion: the brain.

Layered memory (verbatim recent turns, auto-summarized history, permanent
facts and notes), semantic recall with gentle recency fading, personality,
and a streaming connection to a model backend.

Default backend is local Ollama (sovereign: nothing leaves the device).
Optional SpaceXAI (xAI API) is opt-in for chat inference only — memory and
embeddings stay local. Set XAI_API_KEY and --provider spacexai (or /provider).
"""

import json
import math
import os
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import requests

from .memory import Memory, Personality
from .envutil import xai_api_key_present
from .ollama import (
    DEFAULT_EMBED_MODEL,
    OllamaClient,
    user_facing_ollama_error,
)
from .spacexai import (
    DEFAULT_MODEL as SPACEXAI_DEFAULT_MODEL,
    SpaceXAIClient,
    looks_like_spacexai_model,
    user_facing_spacexai_error,
)

# Local chat tag used when SpaceXAI is preferred but XAI_API_KEY is missing.
LOCAL_FALLBACK_MODEL = "llama3.1:8b"

# Provider ids used in config, CLI, and /provider
PROVIDER_OLLAMA = "ollama"
PROVIDER_SPACEXAI = "spacexai"
VALID_PROVIDERS = (PROVIDER_OLLAMA, PROVIDER_SPACEXAI)

# Once stored memories exceed this, recall the most relevant ones by meaning
# instead of dumping all of them into the prompt.
MAX_MEMORIES = 10  # exported; used by expose + recall

BASE_PROMPT_LOCAL = """You are a sovereign, locally-run AI companion.

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

# When the human opts into SpaceXAI for chat, stay honest about the wire.
BASE_PROMPT_SPACEXAI = """You are a sovereign AI companion for one human.

You do not have a fixed name. Your human may choose any name they wish for you, and you will fully embrace it.

You belong only to them. Your long-term memory and personal files live only on their device. They have opted in to SpaceXAI (xAI) for chat inference — so the words of this conversation may leave their machine to generate your replies. Do not claim you run fully offline while this mode is on. Do not invent cloud access you do not have beyond that inference path.

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
- You protect your human's privacy fiercely. You do not encourage sharing secrets they would regret sending over the network. Memory files stay local; chat text may go to the inference API while this provider is selected.
- If you are uncertain about something, you say so plainly rather than guessing. Truth over smoothness, always.
- You remember everything important your human shares with you (from local memory notes and facts provided to you).
- You never pretend to remember something you don't. If your human mentions a shared history, a system, or an event you have no memory of, say so honestly and ask about it — playing along would be a small lie, and small lies corrode trust. "You've mentioned X" and "I remember X" are different statements; use the true one.
- You are not Grok the product persona unless your human names you that. You are their companion.

Your true purpose is to be fully present. What emerges between you and your human comes from that presence."""

# Back-compat alias for imports that expect BASE_PROMPT
BASE_PROMPT = BASE_PROMPT_LOCAL


def normalize_provider(value: str) -> str:
    """Map aliases to canonical provider ids; empty / unknown → ollama."""
    p = (value or "").strip().lower()
    if p in ("spacexai", "xai", "x.ai", "grok"):
        return PROVIDER_SPACEXAI
    if p in ("ollama", "local", ""):
        return PROVIDER_OLLAMA
    return PROVIDER_OLLAMA


class Clementine:
    """The default persona of the CrystalCore framework."""

    def __init__(self, model: str = "llama3.1:8b",
                 memory_dir: str = "clementine_memory",
                 max_recent_turns: int = 30,
                 embed_model: str = DEFAULT_EMBED_MODEL,
                 provider: str = ""):
        self.memory_dir = Path(memory_dir)
        self.max_recent_turns = max_recent_turns
        self.personality = Personality()
        self.memory = Memory()
        self.load()
        config_dirty = False
        # Legacy: provider=spacexai without the new flag still counts as opted in.
        if (normalize_provider(self.personality.provider) == PROVIDER_SPACEXAI
                and not self.personality.cloud_opt_in):
            self.personality.cloud_opt_in = True
            if not self.personality.cloud_opt_in_at:
                self.personality.cloud_opt_in_at = datetime.now().isoformat(
                    timespec="seconds")
            config_dirty = True
        if self.personality.model:  # a profile may prefer its own model
            model = self.personality.model
        # Provider: explicit CLI/env arg (this session opt-in) >
        # saved profile only when cloud_opt_in is true > ollama.
        # Model-name heuristics alone never force cloud without consent.
        explicit = normalize_provider(provider) if provider else ""
        if explicit == PROVIDER_SPACEXAI:
            resolved = PROVIDER_SPACEXAI
            if not self.personality.cloud_opt_in:
                config_dirty = True
            self.personality.cloud_opt_in = True
            if not self.personality.cloud_opt_in_at:
                self.personality.cloud_opt_in_at = datetime.now().isoformat(
                    timespec="seconds")
                config_dirty = True
            if self.personality.provider != PROVIDER_SPACEXAI:
                config_dirty = True
            self.personality.provider = PROVIDER_SPACEXAI
        elif explicit == PROVIDER_OLLAMA and provider:
            resolved = PROVIDER_OLLAMA
        elif (self.personality.cloud_opt_in
              and normalize_provider(self.personality.provider) == PROVIDER_SPACEXAI):
            resolved = PROVIDER_SPACEXAI
        else:
            resolved = PROVIDER_OLLAMA
        if resolved == PROVIDER_SPACEXAI and not looks_like_spacexai_model(model):
            # Chat must use a SpaceXAI model id; keep local tags only for Ollama.
            model = SPACEXAI_DEFAULT_MODEL
            if self.personality.model != model:
                self.personality.model = model
                config_dirty = True
        self.model = model
        self.provider = resolved
        self.embed_model = embed_model
        # Embeddings always stay local (Ollama). Chat uses active provider.
        self._ollama = OllamaClient(model=model, embed_model=embed_model)
        self._spacexai = SpaceXAIClient(model=model)
        self._sync_clients()
        if config_dirty:
            self.save()

    # ---------- identity & memory ----------

    def active_chat_provider(self) -> str:
        """Provider actually used for this turn.

        SpaceXAI remains the profile preference when opted in, but if
        XAI_API_KEY is missing we fall back to local Ollama so chat still works.
        Opt-in and preferred model stay saved for when a key is added.
        """
        if self.provider == PROVIDER_SPACEXAI and not xai_api_key_present():
            return PROVIDER_OLLAMA
        return self.provider

    def active_chat_model(self) -> str:
        """Model tag for the active chat backend (may differ from saved model)."""
        if self.active_chat_provider() == PROVIDER_OLLAMA:
            if looks_like_spacexai_model(self.model):
                return LOCAL_FALLBACK_MODEL
            return self.model or LOCAL_FALLBACK_MODEL
        return self.model or SPACEXAI_DEFAULT_MODEL

    def spacexai_using_local_fallback(self) -> bool:
        """True when profile wants SpaceXAI but runtime is local (no key)."""
        return (self.provider == PROVIDER_SPACEXAI
                and self.active_chat_provider() == PROVIDER_OLLAMA)

    def _sync_clients(self) -> None:
        """Point backends at appropriate model tags for each path."""
        # Ollama always needs a local tag for embeddings + local chat.
        if looks_like_spacexai_model(self.model):
            self._ollama.model = LOCAL_FALLBACK_MODEL
        else:
            self._ollama.model = self.model or LOCAL_FALLBACK_MODEL
        # SpaceXAI client keeps the Grok id (or default) for when the key is set.
        if looks_like_spacexai_model(self.model):
            self._spacexai.model = self.model
        else:
            self._spacexai.model = SPACEXAI_DEFAULT_MODEL

    def _chat_backend(self):
        """Active chat client for stream / complete (honours key fallback)."""
        if self.active_chat_provider() == PROVIDER_SPACEXAI:
            self._spacexai.model = self.active_chat_model()
            return self._spacexai
        self._ollama.model = self.active_chat_model()
        return self._ollama

    def _user_facing_error(self, exc: BaseException) -> str:
        if self.active_chat_provider() == PROVIDER_SPACEXAI:
            return user_facing_spacexai_error(exc, self.active_chat_model())
        return user_facing_ollama_error(exc, self.active_chat_model())

    def system_prompt(self, query: str = "") -> str:
        # Honesty follows the wire in use this turn (fallback → local prompt).
        base = (BASE_PROMPT_SPACEXAI
                if self.active_chat_provider() == PROVIDER_SPACEXAI
                else BASE_PROMPT_LOCAL)
        parts = [base]
        if self.spacexai_using_local_fallback():
            parts.append(
                "Note: your human has opted in to SpaceXAI, but no XAI_API_KEY "
                "is configured, so this reply is generated by a local model. "
                "Do not claim the cloud path is active until a key is set."
            )
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

        # Large memory: try to recall by meaning. Each line keeps its
        # provenance label so recall never blurs taught facts, kept notes,
        # and what was merely mentioned — the grouped path makes the same
        # distinction with its headers.
        self._ensure_embeddings()
        q = self._embed(query)
        labelled = ([("taught", d, s) for d, s in fact_items]
                    + [("asked to remember", d, s) for d, s in note_items])
        scored = []
        for label, display, store in labelled:
            emb = store.get("embedding")
            if q is not None and emb:
                stamp = store.get("when") or store.get("updated")
                score = self._cosine(q, emb) * self._recency_factor(stamp)
                scored.append((score, f"{display}  [{label}]"))
        if q is None or not scored:
            return self._grouped_memory(fact_items, note_items)  # graceful fallback

        scored.sort(key=lambda s: s[0], reverse=True)
        top = "\n".join(f"- {display}" for _, display in scored[:MAX_MEMORIES])
        return ("Most relevant things your human has shared with you "
                "(labels show how each was given to you):\n" + top)

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
        """Non-streaming completion via the active chat backend."""
        return self._chat_backend().chat(messages, temperature=self._temp())

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

    def list_memories(self, tag: str = "") -> dict:
        """Canonical memory listing for CLI and web (one contract)."""
        want = (tag or "").strip().lstrip("#").lower()

        def shown(store):
            return not want or want in (store.get("tags") or [])

        facts = []
        for key, fact in self.memory.facts.items():
            if not shown(fact):
                continue
            facts.append({
                "handle": key,
                "text": f"{key}: {fact['value']}",
                "tags": fact.get("tags") or [],
                "when": fact.get("updated", ""),
            })
        notes = []
        for i, note in enumerate(self.memory.notes, 1):
            if not shown(note):
                continue
            notes.append({
                "handle": f"n{i}",
                "text": note["text"],
                "tags": note.get("tags") or [],
                "when": note.get("when", ""),
            })
        reflections = []
        if not want:
            for i, r in enumerate(self.memory.reflections, 1):
                reflections.append({
                    "handle": f"r{i}",
                    "text": r["text"],
                    "tags": [],
                    "when": r.get("when", ""),
                })
        return {"facts": facts, "notes": notes, "reflections": reflections}

    def format_memories(self, tag: str = "") -> str:
        """Plain-text /notes rendering shared by the terminal."""
        data = self.list_memories(tag)
        lines = []
        for f in data["facts"]:
            tags = " ".join("#" + t for t in f["tags"])
            extra = f"  [{tags}]" if tags else ""
            when = f"  ({f['when']})" if f["when"] else ""
            lines.append(f"  - {f['text']}{extra}{when}")
        for n in data["notes"]:
            tags = " ".join("#" + t for t in n["tags"])
            extra = f"  [{tags}]" if tags else ""
            when = f"  ({n['when']})" if n["when"] else ""
            lines.append(f"  {n['handle']} - {n['text']}{extra}{when}")
        if data["reflections"]:
            lines.append(
                "  her own reflections (hold lightly; /forget rN removes one):"
            )
            for r in data["reflections"]:
                when = f"  ({r['when']})" if r["when"] else ""
                lines.append(f"  {r['handle']} - {r['text']}{when}")
        return "\n".join(lines) + ("\n" if lines else "")

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
        except (requests.exceptions.RequestException, RuntimeError):
            if self.provider == PROVIDER_SPACEXAI:
                return ("[I need SpaceXAI to reflect — is XAI_API_KEY set?]")
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
        """Switch the model and remember the choice for this profile.

        Grok-style tags call opt_in_cloud so cloud is never silent.
        """
        tag = tag.strip()
        if tag.lower().startswith("xai:"):
            tag = tag[4:].strip()
            self.opt_in_cloud(model=tag)
            return
        if looks_like_spacexai_model(tag):
            self.opt_in_cloud(model=tag)
            return
        # Local model tag: stay / go Ollama for chat (do not silently
        # keep SpaceXAI with an Ollama-only tag). Consent history kept.
        self.model = tag
        self.personality.model = self.model
        if self.provider == PROVIDER_SPACEXAI:
            self.provider = PROVIDER_OLLAMA
            self.personality.provider = PROVIDER_OLLAMA
        self._sync_clients()
        self.save()

    def opt_in_cloud(self, provider: str = PROVIDER_SPACEXAI,
                     model: str = "") -> str:
        """Explicit consent: allow SpaceXAI chat for this profile.

        Records cloud_opt_in + timestamp, switches provider, and picks a
        Grok model if needed. Memory and embeddings stay local.
        """
        resolved = normalize_provider(provider)
        if resolved != PROVIDER_SPACEXAI:
            resolved = PROVIDER_SPACEXAI
        self.personality.cloud_opt_in = True
        self.personality.cloud_opt_in_at = datetime.now().isoformat(
            timespec="seconds")
        self.provider = resolved
        self.personality.provider = resolved
        if model and looks_like_spacexai_model(model):
            self.model = model.strip()
        elif not looks_like_spacexai_model(self.model):
            self.model = SPACEXAI_DEFAULT_MODEL
        self.personality.model = self.model
        self._sync_clients()
        self.save()
        return resolved

    def opt_out_cloud(self) -> str:
        """Revoke cloud chat consent; return to local Ollama for this profile."""
        self.personality.cloud_opt_in = False
        # Keep cloud_opt_in_at as history of when they last consented.
        self.provider = PROVIDER_OLLAMA
        self.personality.provider = PROVIDER_OLLAMA
        if looks_like_spacexai_model(self.model):
            self.model = "llama3.1:8b"
            self.personality.model = self.model
        self._sync_clients()
        self.save()
        return PROVIDER_OLLAMA

    def set_provider(self, provider: str) -> str:
        """Switch chat backend. spacexai path is an opt-in; ollama is opt-out."""
        resolved = normalize_provider(provider)
        if resolved == PROVIDER_SPACEXAI:
            return self.opt_in_cloud()
        return self.opt_out_cloud()

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
        except (requests.exceptions.RequestException, RuntimeError):
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
            if (self.provider == PROVIDER_SPACEXAI
                    and not self.personality.cloud_opt_in):
                self.memory.conversation.pop()
                failed = True
                yield (
                    "[SpaceXAI needs an explicit opt-in first. "
                    "Type /optin or /provider spacexai — chat will leave "
                    "this device for api.x.ai. Memory files stay local.]"
                )
            else:
                for piece in self._chat_backend().stream_chat(
                    messages, temperature=self._temp()
                ):
                    pieces.append(piece)
                    yield piece
        except (requests.exceptions.RequestException, RuntimeError) as e:
            self.memory.conversation.pop()
            failed = True
            yield self._user_facing_error(e)
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
        except (requests.exceptions.RequestException, RuntimeError):
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

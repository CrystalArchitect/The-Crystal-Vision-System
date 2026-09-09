"""CrystalCore memory layer — simple JSON files on disk.

Two kinds of memory:
- conversation.json : the running chat history (survives restarts)
- memories.json     : long-term memories CrystalCore chooses to keep

Everything lives in the memory/ directory, which is gitignored so it
stays private to the machine running the app.
"""

import json
import os
import threading
from datetime import datetime, timezone

MEMORY_DIR = os.getenv("MEMORY_DIR", "memory")
MAX_HISTORY = 200   # messages kept in the conversation file
MAX_MEMORIES = 200  # long-term memories kept

_lock = threading.Lock()


def _path(name):
    return os.path.join(MEMORY_DIR, name)


def _load(name, default):
    try:
        with open(_path(name), encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save(name, data):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    tmp = _path(name) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, _path(name))


# --- Conversation history ---------------------------------------------------

def load_history():
    return _load("conversation.json", [])


def append_messages(*messages):
    with _lock:
        history = load_history()
        history.extend(messages)
        _save("conversation.json", history[-MAX_HISTORY:])


def clear_history():
    with _lock:
        _save("conversation.json", [])


# --- Long-term memories -----------------------------------------------------

def load_memories():
    return _load("memories.json", [])


def add_memory(text):
    text = text.strip()
    if not text:
        return
    with _lock:
        memories = load_memories()
        if any(m["text"] == text for m in memories):
            return  # already remembered
        memories.append({
            "text": text,
            "saved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        _save("memories.json", memories[-MAX_MEMORIES:])

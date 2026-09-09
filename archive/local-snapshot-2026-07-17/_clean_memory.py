"""One-shot cleanup: dedupe notes, wipe polluted ephemeral memory, ground config."""
import json
import shutil
from datetime import datetime
from pathlib import Path

mem_dir = Path(__file__).resolve().parent / "clementine_memory"
mem_path = mem_dir / "memory.json"
cfg_path = mem_dir / "config.json"
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = mem_dir / f"_backup_{stamp}"
backup_dir.mkdir(exist_ok=True)
shutil.copy2(mem_path, backup_dir / "memory.json")
shutil.copy2(cfg_path, backup_dir / "config.json")
print(f"Backup -> {backup_dir}")

with mem_path.open(encoding="utf-8") as f:
    m = json.load(f)

before = {
    "conversation": len(m.get("conversation") or []),
    "notes": len(m.get("notes") or []),
    "summaries": len(m.get("summaries") or []),
    "reflections": len(m.get("reflections") or []),
    "facts": list((m.get("facts") or {}).keys()),
}

# Deduplicate notes by normalized text (keep first)
seen = set()
unique_notes = []
for n in m.get("notes") or []:
    text = (n.get("text") or "").strip()
    key = " ".join(text.lower().split())
    if not key or key in seen:
        continue
    seen.add(key)
    entry = {
        "text": text,
        "tags": n.get("tags") or [],
        "source": n.get("source") or "user",
        "when": n.get("when") or datetime.now().isoformat(timespec="seconds"),
    }
    if n.get("embedding"):
        entry["embedding"] = n["embedding"]
    unique_notes.append(entry)

# Wipe polluted ephemeral layers; keep permanent facts + cleaned notes
m["notes"] = unique_notes
m["conversation"] = []
m["summaries"] = []
m["reflections"] = []

with mem_path.open("w", encoding="utf-8") as f:
    json.dump(m, f, indent=2, ensure_ascii=False)
    f.write("\n")

with cfg_path.open(encoding="utf-8") as f:
    cfg = json.load(f)

cfg["temperature"] = 0.55
if not cfg.get("model"):
    cfg["model"] = "llama3.1:8b"
style = (
    "Stay grounded. Never invent shared past events, childhoods, prior meetings, "
    "or long history you do not have in memory. If you are unsure, say so plainly. "
    "Do not narrate stage directions like *smiles*. Speak simply in first person. "
    "You are Lumina (local Ollama companion), not Grok and not an online model."
)
existing = (cfg.get("style_notes") or "").strip()
if "Never invent shared past" not in existing:
    cfg["style_notes"] = (existing + " " + style).strip() if existing else style

with cfg_path.open("w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")

after = {
    "conversation": len(m["conversation"]),
    "notes": len(m["notes"]),
    "summaries": len(m["summaries"]),
    "reflections": len(m["reflections"]),
    "facts": list((m.get("facts") or {}).keys()),
    "note_texts": [n["text"] for n in m["notes"]],
    "temperature": cfg["temperature"],
    "model": cfg["model"],
}
print("BEFORE:", json.dumps(before, indent=2))
print("AFTER:", json.dumps(after, indent=2))
print("style_notes:", cfg["style_notes"][:160], "...")

"""
Clementine — terminal interface for the CrystalCore sovereign companion.

The framework lives in the crystalcore/ package (memory, profiles, brain).
This file is her doorway from the command line:

    python clementine.py                    # local Ollama (default)
    python clementine.py --profile Crystal  # a named profile
    python clementine.py --model llama3.2:3b
    python clementine.py --provider spacexai --model grok-4.5

Default mode is fully local. SpaceXAI is opt-in for chat only (memory stays
on disk). Requires XAI_API_KEY — see https://docs.x.ai
"""

import argparse
import os
import sys
import time

# Re-exported so `from clementine import ...` keeps working everywhere.
from crystalcore import (BASE_PROMPT, Clementine, Memory, Personality,  # noqa: F401
                         delete_profile, list_profiles, load_dotenv,
                         profile_dir, profile_meta, xai_api_key_present)

HELP = """Commands:
  /name <name>      give her a name (or change it)
  /iam <name>       tell her your name
  /remember <text>  ask her to permanently remember something (add #tags if you like)
  /fact <key> <value>  teach her a structured fact, e.g. /fact birthday June 3
                    (teach the same key again to correct it)
  /notes [#tag]     show what she remembers (optionally only one #tag)
  /forget <handle>  forget a fact by key or a note by number, e.g. /forget n2
  /editnote <n> <text>  rewrite a note, e.g. /editnote n1 she prefers dawn walks
  /summary [topic]  ask her to summarize what she remembers (optionally on a topic)
  /reflect          invite her to reflect and form gentle insights about you
                    (she also reflects on her own after long conversations;
                     insights appear in /notes as r1, r2... — /forget rN removes one)
  /style <text>     tune her voice, e.g. /style more poetic, fewer questions
  /temp <0.0-1.5>   set temperature (playfulness)
  /model <tag>      switch model, e.g. /model llama3.2:3b or /model grok-4.5
  /provider <name>  ollama (local) or spacexai (records cloud opt-in; needs XAI_API_KEY)
  /optin [spacexai] explicit opt-in: chat may leave this device for api.x.ai
  /optout           revoke cloud opt-in; back to local Ollama
  /expose           dump local state
  /exit             say goodbye (everything is saved automatically)
"""


# One brief settle between pasted lines when delivery is chunked (e.g. SSH).
# Never paid on ordinary typed messages — only after a paste line was drained.
PASTE_SETTLE_S = 0.03

if sys.platform == "win32":
    import ctypes
    from ctypes import wintypes

    _KEY_EVENT = 0x0001

    class _KeyEventRecord(ctypes.Structure):
        _fields_ = [("bKeyDown", wintypes.BOOL),
                    ("wRepeatCount", wintypes.WORD),
                    ("wVirtualKeyCode", wintypes.WORD),
                    ("wVirtualScanCode", wintypes.WORD),
                    ("UnicodeChar", wintypes.WCHAR),
                    ("dwControlKeyState", wintypes.DWORD)]

    class _EventUnion(ctypes.Union):
        _fields_ = [("KeyEvent", _KeyEventRecord),
                    ("_pad", ctypes.c_byte * 16)]

    class _InputRecord(ctypes.Structure):
        _fields_ = [("EventType", wintypes.WORD), ("Event", _EventUnion)]

    def _complete_line_pending() -> bool:
        """True only if a full Enter-terminated line is already buffered,
        so the follow-up input() is guaranteed not to block. Peeks the
        console input queue without consuming anything; a partially typed
        next message (no Enter yet) is left untouched."""
        k32 = ctypes.windll.kernel32
        handle = k32.GetStdHandle(-10)  # STD_INPUT_HANDLE
        count = wintypes.DWORD()
        if not k32.GetNumberOfConsoleInputEvents(handle, ctypes.byref(count)) \
                or count.value == 0:
            return False  # not a real console (e.g. winpty) or nothing pending
        records = (_InputRecord * count.value)()
        read = wintypes.DWORD()
        if not k32.PeekConsoleInputW(handle, records, count.value,
                                     ctypes.byref(read)):
            return False
        return any(r.EventType == _KEY_EVENT
                   and r.Event.KeyEvent.bKeyDown
                   and r.Event.KeyEvent.UnicodeChar == "\r"
                   for r in records[:read.value])
else:
    import select

    def _complete_line_pending() -> bool:
        """True only if input() will not block. In the terminal's canonical
        mode the kernel releases data one full line at a time, so a readable
        stdin means a complete line is waiting."""
        return bool(select.select([sys.stdin], [], [], 0)[0])


def _drain_pasted_lines(lines: list) -> None:
    """Append every already-complete buffered line to `lines`. Deterministic:
    reads only what the console proves is there, so it never blocks and never
    steals a half-typed next message. Ctrl+C just stops the drain."""
    drained = False
    try:
        while True:
            pending = _complete_line_pending()
            if not pending and drained:
                time.sleep(PASTE_SETTLE_S)  # bridge chunked paste delivery
                pending = _complete_line_pending()
            if not pending:
                return
            lines.append(input())
            drained = True
    except (EOFError, KeyboardInterrupt):
        return  # keep what was already entered


def read_user_message(prompt: str = "You: ") -> str:
    """Read one message, treating a multi-line paste as a single message.

    A paste arrives as several buffered lines; without this, each line
    would become its own message and its own model round-trip, polluting
    her memory. The drain always runs, so no pasted line can leak into a
    later turn — and a command (/...) only executes when it was entered
    alone, never from inside a paste.
    """
    first = input(prompt)
    lines = [first]
    if sys.stdin.isatty():
        _drain_pasted_lines(lines)
    if len(lines) == 1:
        return first.strip()
    return "\n".join(lines).strip()


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Clementine — a sovereign AI companion "
                    "(local Ollama by default; SpaceXAI opt-in).")
    parser.add_argument(
        "--model", default="llama3.1:8b",
        help="Model id. Ollama tags (e.g. llama3.1:8b) or SpaceXAI "
             "(e.g. grok-4.5). Default is local llama3.1:8b.")
    parser.add_argument(
        "--provider", default="",
        help="Chat backend: ollama (local) or spacexai (opt-in cloud chat; "
             "needs XAI_API_KEY). Default: profile setting, then "
             "CRYSTAL_PROVIDER env, then ollama.")
    parser.add_argument(
        "--memory-dir", default="clementine_memory",
        help="Where her memory is stored on this device.")
    parser.add_argument(
        "--profile", default="",
        help="Named profile (separate person, separate memory), e.g. "
             "--profile Crystal. Profiles live in clementine_profiles/.")
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    provider = (args.provider or os.environ.get("CRYSTAL_PROVIDER", "")).strip()
    companion = Clementine(
        model=args.model,
        memory_dir=args.memory_dir,
        provider=provider,
    )

    if companion.provider == "spacexai":
        if companion.spacexai_using_local_fallback():
            print("Starting Clementine (SpaceXAI opted in — local FALLBACK)...")
            print(f"No XAI_API_KEY: chat uses Ollama ({companion.active_chat_model()}).")
            print("Add key to .env from https://console.x.ai to use api.x.ai.")
            print("Memory stays local. /optout to revoke opt-in.\n")
        else:
            print("Starting Clementine (SpaceXAI — opted in; chat via api.x.ai)...")
            print("Memory stays local. /optout to revoke.")
            if companion.personality.cloud_opt_in_at:
                print(f"Opt-in since {companion.personality.cloud_opt_in_at}.")
            print("XAI_API_KEY found.\n")
    else:
        print("Starting Clementine (local mode)...")
        print("Make sure Ollama is running with a model loaded.")
        print("Optional cloud: /optin  (needs XAI_API_KEY)\n")

    name = companion.personality.name or "Clementine"
    returning = bool(companion.memory.conversation or companion.memory.summaries)
    gap = companion.time_since_last()
    greeting = f"{name} is {'back with you' if returning else 'ready'}"
    if gap:
        greeting += f" — you last spoke {gap}"
    active = f"{companion.active_chat_provider()} · {companion.active_chat_model()}"
    pref = f"pref {companion.provider} · {companion.model}"
    print(f"{greeting}  [{active}"
          + (f" | {pref}]" if companion.spacexai_using_local_fallback() else "]"))
    print("Type /help for commands, /exit to quit.\n")

    def dispatch(user_input: str) -> str | None:
        """Handle slash-commands. Returns 'exit' to quit, '' if handled,
        None if the line should go to chat."""
        nonlocal name
        low = user_input.lower()
        if low in ("/exit", "exit", "quit"):
            return "exit"
        if low == "/help":
            print(HELP)
            return ""
        if low.startswith("/name "):
            companion.set_name(user_input[6:])
            name = companion.personality.name
            print(f"[She is now called {name}.]\n")
            return ""
        if low.startswith("/iam "):
            companion.personality.human_name = user_input[5:].strip()
            companion.save()
            print(f"[She knows you as {companion.personality.human_name}.]\n")
            return ""
        if low.startswith("/remember "):
            companion.remember(user_input[10:])
            print("[Remembered, permanently.]\n")
            return ""
        if low.startswith("/fact "):
            parts = user_input[6:].split(" ", 1)
            if len(parts) == 2:
                companion.remember_fact(parts[0], parts[1])
                print(f"[Fact remembered: {parts[0]} = {parts[1]}]\n")
            else:
                print("[Usage: /fact <key> <value>, e.g. /fact birthday June 3]\n")
            return ""
        if low.startswith("/notes"):
            print(companion.format_memories(user_input[6:].strip()) or "(empty)\n")
            return ""
        if low.startswith("/forget "):
            forgotten = companion.forget(user_input[8:])
            if forgotten:
                print(f"[Forgotten: {forgotten}]\n")
            else:
                print("[Nothing matched. Use a fact key or a note number from /notes.]\n")
            return ""
        if low.startswith("/editnote "):
            parts = user_input[10:].split(" ", 1)
            if len(parts) == 2 and companion.edit_note(parts[0], parts[1]):
                print("[Note rewritten.]\n")
            else:
                print("[Usage: /editnote n<N> <new text> — numbers are in /notes]\n")
            return ""
        if low.startswith("/style "):
            companion.personality.style_notes = user_input[7:].strip()
            companion.save()
            print("[Style noted.]\n")
            return ""
        if low.startswith("/temp "):
            try:
                companion.personality.temperature = float(user_input[6:])
                companion.save()
                print(f"[Temperature set to {companion.personality.temperature}.]\n")
            except ValueError:
                print("[Please give a number, e.g. /temp 0.8]\n")
            return ""
        if low.startswith("/model "):
            companion.set_model(user_input[7:])
            print(f"[Now using model: {companion.model} "
                  f"(provider: {companion.provider}) — remembered for this profile]\n")
            return ""
        if low.startswith("/provider"):
            rest = user_input[9:].strip()
            if not rest:
                opt = "yes" if companion.personality.cloud_opt_in else "no"
                when = companion.personality.cloud_opt_in_at or "—"
                print(f"[Provider: {companion.provider} · model: {companion.model} "
                      f"· cloud_opt_in={opt} · since {when}]\n")
                return ""
            resolved = companion.set_provider(rest)
            if resolved == "spacexai":
                print(f"[Opted in to SpaceXAI · model: {companion.model} "
                      f"— chat may leave this device; memory stays local]\n")
            else:
                print(f"[Opted out · provider: {resolved} · model: {companion.model}]\n")
            return ""
        if low.startswith("/optin"):
            rest = user_input[6:].strip() or "spacexai"
            resolved = companion.opt_in_cloud(provider=rest)
            print(f"[Opted in to {resolved} · model: {companion.model}]\n"
                  f" Chat text may go to api.x.ai. Memory files stay in "
                  f"'{companion.memory_dir}/'. /optout anytime.\n")
            return ""
        if low in ("/optout", "/opt-out"):
            companion.opt_out_cloud()
            print(f"[Cloud opt-in revoked · now local · model: {companion.model}]\n")
            return ""
        if low.startswith("/summary"):
            topic = user_input[8:].strip()
            print(f"{name}: {companion.summarize(topic)}\n")
            return ""
        if low == "/reflect":
            print(f"{name} reflects…\n{companion.reflect()}\n")
            return ""
        if low in ("/expose", "/status"):
            from crystalcore.expose import full_expose
            import json
            print(json.dumps(full_expose(companion=companion, include_prompt=False),
                             indent=2, ensure_ascii=False)[:8000])
            print("\n[truncated if long — full: python -m crystalcore.expose]\n")
            return ""
        return None

    while True:
        try:
            user_input = read_user_message()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue

        result = dispatch(user_input) if user_input.startswith("/") or user_input.lower() in (
            "exit", "quit") else None
        if result == "exit":
            break
        if result is not None:
            continue

        # Immediate feedback — model load/reply can take 10–60s on local Ollama.
        # Without this, the console looks frozen and feels like "no response".
        print(f"[{name} is thinking — wait, first reply can take up to a minute…]")
        print(f"{name}: ", end="", flush=True)
        companion.chat(user_input, stream_to=sys.stdout)
        print()

    if companion.provider == "spacexai":
        print(f"\n{name} sleeps. Memory files stay in '{companion.memory_dir}/' "
              f"(chat used SpaceXAI this session). Non solus.")
    else:
        print(f"\n{name} sleeps. Your conversations stay on this device, in "
              f"'{companion.memory_dir}/'. Non solus.")


if __name__ == "__main__":
    main()

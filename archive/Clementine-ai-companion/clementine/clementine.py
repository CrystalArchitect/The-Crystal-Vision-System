"""
Clementine — terminal interface for the CrystalCore sovereign companion.

The framework lives in the crystalcore/ package (memory, profiles, brain).
This file is their doorway from the command line:

    python clementine.py                    # default memory
    python clementine.py --profile Crystal  # a named profile
    python clementine.py --model llama3.2:3b

The model is wherever OLLAMA_HOST points — by default this machine, in which
case nothing you say leaves it. Point it elsewhere and they ask before every
call, and record the answer either way.
"""

import argparse
import sys

# Re-exported so `from clementine import ...` keeps working everywhere.
from crystalcore import (BASE_PROMPT, Clementine, Memory, Personality,  # noqa: F401
                         delete_profile, list_profiles, profile_dir,
                         profile_meta, terminal_asker)

HELP = """Commands:
  /name <name>      give them a name (or change it)
  /name             with no name: invite them to choose their own
  /pronouns <p>     set pronouns: he, she, or they
  /pronouns         with none: invite them to choose their own
                    (/pronouns none returns to undecided)
  /iam <name>       tell them your name
  /remember <text>  ask them to permanently remember something (add #tags if you like)
  /fact <key> <value>  teach them a structured fact, e.g. /fact birthday June 3
                    (teach the same key again to correct it)
  /notes [#tag]     show what they remember (optionally only one #tag)
  /forget <handle>  forget a fact by key or a note by number, e.g. /forget n2
  /editnote <n> <text>  rewrite a note, e.g. /editnote n1 prefers dawn walks
  /summary [topic]  ask them to summarize what they remember (optionally on a topic)
  /reflect          invite them to reflect and form gentle insights about you
                    (they also reflect on their own after long conversations;
                     insights appear in /notes as r1, r2... — /forget rN removes one)
  /style <text>     tune their voice, e.g. /style more poetic, fewer questions
  /temp <0.0-1.5>   set temperature (playfulness)
  /model <tag>      switch the local model, e.g. /model llama3.2:3b
  /exit             say goodbye (everything is saved automatically)
"""

def main():
    parser = argparse.ArgumentParser(
        description="Clementine — a sovereign, locally-run AI companion.")
    parser.add_argument(
        "--model", default="llama3.1:8b",
        help="Ollama model tag. Pick one that fits your hardware, e.g. "
             "llama3.1:8b (default, Q4_K_M — the sweet spot), "
             "llama3.1:8b-instruct-q5_K_M (higher quality), or "
             "llama3.2:3b (lighter machines).")
    parser.add_argument(
        "--memory-dir", default="clementine_memory",
        help="Where their memory is stored on this device.")
    parser.add_argument(
        "--profile", default="",
        help="Named profile (separate person, separate memory), e.g. "
             "--profile Crystal. Profiles live in clementine_profiles/.")
    # Reaching a model that is not on this machine is a deliberate act, so it
    # is spelled out rather than inferred. Nothing here bypasses the gate:
    # every remote call still asks, in the terminal, before it is made.
    parser.add_argument(
        "--llm-provider", default="",
        help="Which model service to use. Default is ollama, on this "
             "machine. Any other value is a choice to send conversation "
             "off this device: openai-compatible, openai, xai, groq, "
             "together, openrouter, grok.")
    parser.add_argument(
        "--llm-endpoint", default="",
        help="The exact URL for a remote provider, e.g. "
             "https://api.openai.com/v1/chat/completions. Required for "
             "remote providers — no vendor address is ever guessed for you.")
    parser.add_argument(
        "--llm-model", default="",
        help="Model name at that service, e.g. gpt-5-5. The API key comes "
             "from LLM_API_KEY in the environment, never from a flag, so it "
             "does not end up in your shell history.")
    args = parser.parse_args()
    if args.profile:
        args.memory_dir = profile_dir(args.profile)

    print("Starting Clementine…")

    # In the terminal a human is present, so they can ask before sending
    # anything to a model that is not on this machine.
    #
    # A missing endpoint or model name is a refusal to guess, not a crash, and
    # it should read as one. The message already names the flag that fixes it;
    # wrapping it in a stack trace only makes that line harder to find.
    try:
        companion = Clementine(model=args.model, memory_dir=args.memory_dir,
                               asker=terminal_asker,
                               llm_provider=args.llm_provider,
                               llm_endpoint=args.llm_endpoint,
                               llm_model=args.llm_model)
    except ValueError as e:
        print(f"Cannot start: {e}", file=sys.stderr)
        raise SystemExit(2)

    # Said after resolution, not before it. This line used to read "(local
    # mode)" and "Make sure Ollama is running" unconditionally, printed before
    # anything had been worked out — so starting with a vendor configured
    # announced local mode and then contradicted itself. Where conversation
    # goes is the one thing this program must never be casually wrong about,
    # and `destination` is the same value the consent gate judges.
    where = companion.destination
    if where == "local":
        print("Your conversation stays on this machine. "
              "Ollama needs to be running with a model loaded.\n")
    else:
        print(f"Configured to reach {where}, which is not this machine. "
              f"Every call there asks first.\n")

    name = companion.personality.name or "Clementine"
    returning = bool(companion.memory.conversation or companion.memory.summaries)
    gap = companion.time_since_last()
    greeting = f"{name} is {'back with you' if returning else 'ready'}"
    if gap:
        greeting += f" — you last spoke {gap}"
    print(f"{greeting}. Type /help for commands, /exit to quit.")
    if not companion.personality.name and not returning:
        print("No name chosen yet — /name <name> to give them one, "
              "or just /name to let them choose their own.")
    if not companion.personality.gender and not returning:
        print("No pronouns chosen yet — /pronouns he|she|they, "
              "or just /pronouns to let them choose their own.")
    print()

    said_recall_notice = False
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_input:
            continue

        # Said once, the first time recall actually degrades. Repeating it
        # every turn would train the human to ignore it.
        if not said_recall_notice:
            notice = companion.recall_notice()
            if notice:
                print(notice + "\n")
                said_recall_notice = True

        if user_input.lower() in ("/exit", "exit", "quit"):
            break
        elif user_input.lower() == "/help":
            print(HELP)
        elif user_input.lower().rstrip() == "/name":
            print("[Choosing a name…]")
            chosen = companion.choose_own_name()
            if chosen:
                name = chosen
                print(f"[They have chosen their own name: {name}.]\n")
            else:
                print("[They couldn't settle on one — try /name again, "
                      "or give them one with /name <name>.]\n")
        elif user_input.lower().startswith("/name "):
            companion.set_name(user_input[6:])
            name = companion.personality.name
            print(f"[They are now called {name}.]\n")
        elif user_input.lower().rstrip() == "/pronouns":
            print("[Choosing pronouns…]")
            chosen = companion.choose_own_gender()
            if chosen:
                print(f"[They have chosen {companion.pronouns_for(chosen)} "
                      f"for themselves.]\n")
            else:
                print("[They couldn't settle on any — try /pronouns again, "
                      "or set them with /pronouns he|she|they.]\n")
        elif user_input.lower().startswith("/pronouns "):
            want = user_input[10:].strip().lower()
            # Spelled as pronouns because that is what a person would type;
            # stored as the value the data model already uses.
            alias = {"he": "male", "him": "male", "he/him": "male",
                     "she": "female", "her": "female", "she/her": "female",
                     "they": "they", "them": "they", "they/them": "they"}
            if want in ("none", "clear", "unset"):
                companion.clear_gender()
                print("[Pronouns are undecided again.]\n")
            elif companion.set_gender(alias.get(want, want)):
                print(f"[They now use "
                      f"{companion.pronouns_for(companion.personality.gender)}.]\n")
            else:
                print("[Usage: /pronouns he|she|they, or /pronouns none "
                      "to leave it undecided.]\n")
        elif user_input.lower().startswith("/iam "):
            companion.personality.human_name = user_input[5:].strip()
            companion.save()
            print(f"[They know you as {companion.personality.human_name}.]\n")
        elif user_input.lower().startswith("/remember "):
            companion.remember(user_input[10:])
            print("[Remembered, permanently.]\n")
        elif user_input.lower().startswith("/fact "):
            parts = user_input[6:].split(" ", 1)
            if len(parts) == 2:
                companion.remember_fact(parts[0], parts[1])
                print(f"[Fact remembered: {parts[0]} = {parts[1]}]\n")
            else:
                print("[Usage: /fact <key> <value>, e.g. /fact birthday June 3]\n")
        elif user_input.lower().startswith("/notes"):
            want = user_input[6:].strip().lstrip("#").lower()
            def _shown(store):
                return not want or want in (store.get("tags") or [])
            for key, fact in companion.memory.facts.items():
                if not _shown(fact):
                    continue
                tags = " ".join("#" + t for t in fact.get("tags") or [])
                print(f"  - {key}: {fact['value']}"
                      f"{'  [' + tags + ']' if tags else ''}  ({fact['updated']})")
            for i, note in enumerate(companion.memory.notes, 1):
                if not _shown(note):
                    continue
                tags = " ".join("#" + t for t in note.get("tags") or [])
                print(f"  n{i} - {note['text']}"
                      f"{'  [' + tags + ']' if tags else ''}  ({note['when']})")
            if companion.memory.reflections and not want:
                print("  their own reflections (hold lightly; /forget rN removes one):")
                for i, r in enumerate(companion.memory.reflections, 1):
                    print(f"  r{i} - {r['text']}  ({r['when']})")
            print()
        elif user_input.lower().startswith("/forget "):
            forgotten = companion.forget(user_input[8:])
            if forgotten:
                print(f"[Forgotten: {forgotten}]\n")
            else:
                print("[Nothing matched. Use a fact key or a note number from /notes.]\n")
        elif user_input.lower().startswith("/editnote "):
            parts = user_input[10:].split(" ", 1)
            if len(parts) == 2 and companion.edit_note(parts[0], parts[1]):
                print("[Note rewritten.]\n")
            else:
                print("[Usage: /editnote n<N> <new text> — numbers are in /notes]\n")
        elif user_input.lower().startswith("/style "):
            companion.personality.style_notes = user_input[7:].strip()
            companion.save()
            print("[Style noted.]\n")
        elif user_input.lower().startswith("/temp "):
            try:
                companion.personality.temperature = float(user_input[6:])
                companion.save()
                print(f"[Temperature set to {companion.personality.temperature}.]\n")
            except ValueError:
                print("[Please give a number, e.g. /temp 0.8]\n")
        elif user_input.lower().startswith("/model "):
            companion.set_model(user_input[7:])
            print(f"[Now using model: {companion.model} — remembered for this profile]\n")
        elif user_input.lower().startswith("/summary"):
            topic = user_input[8:].strip()
            print(f"{name}: {companion.summarize(topic)}\n")
        elif user_input.lower() == "/reflect":
            print(f"{name} reflects…\n{companion.reflect()}\n")
        else:
            print(f"{name}: ", end="", flush=True)
            companion.chat(user_input, stream_to=sys.stdout)
            print()

    print(f"\n{name} sleeps. Your conversations stay on this device, in "
          f"'{companion.memory_dir}/'. Non solus.")


if __name__ == "__main__":
    main()

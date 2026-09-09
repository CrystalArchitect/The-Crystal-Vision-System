/**
 * Retro-terminal component skeleton with a layered easter-egg command handler.
 * Adapt styling to the project's design system; keep the handler structure.
 */
import { useRef, useState } from "react";
import SequenceOverlay from "./SequenceOverlay";
import { isEggUnlocked, unlockEgg } from "./unlock-state";

type Line = { kind: "input" | "output" | "accent"; text: string };

// Layer 0: documented commands. `help` lists these ONLY — never hidden ones.
const RESPONSES: Record<string, string[]> = {
  help: ["Available commands:", "  status · lore · keys · clear", "  (some files hide from plain sight…)"],
  status: ["NODE: ONLINE", "SIGNAL: NOMINAL"],
  lore: ["Chapter I — …", "Chapter II — …"],
};

// Layer 1 hint: dynamic, reflects lock state at call time.
function lsALines(): string[] {
  return [
    "drwx------  .vault/",
    "-r--------  .hidden_word", // file name IS the layer-2 command
    isEggUnlocked()
      ? "-r-x------  .egg        [UNLOCKED — the channel answers]"
      : "----------  .egg        [LOCKED — requires alignment]",
    "Hidden files carry hidden words. Speak the last one to the node.",
  ];
}

export default function Terminal({ onOpenEggWindow }: { onOpenEggWindow?: () => void }) {
  const [lines, setLines] = useState<Line[]>([{ kind: "output", text: "type 'help' to begin." }]);
  const [value, setValue] = useState("");
  const [playing, setPlaying] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const push = (...ls: Line[]) => {
    setLines(prev => [...prev, ...ls]);
    requestAnimationFrame(() =>
      scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" }),
    );
  };

  const run = (raw: string) => {
    const cmd = raw.trim().toLowerCase();
    if (!cmd) return;
    if (cmd === "clear") return setLines([]);

    // Layer 2: hidden trigger — accept close variants of the hidden word.
    if (cmd === "hidden word" || cmd === "hidden_word" || cmd === ".hidden_word") {
      push({ kind: "input", text: raw }, { kind: "accent", text: "…the node recognizes the words." });
      setTimeout(() => setPlaying(true), 900);
      return;
    }

    // Layer 3: unlockable command.
    if (cmd === "egg") {
      if (!isEggUnlocked()) {
        return push(
          { kind: "input", text: raw },
          { kind: "output", text: "…static. The channel does not answer the unaligned." },
          { kind: "output", text: "Complete the alignment first. The hidden files know the words." },
        );
      }
      if (onOpenEggWindow) {
        push({ kind: "input", text: raw }, { kind: "accent", text: "Signal accepted — opening hidden channel…" });
        setTimeout(onOpenEggWindow, 500);
        return;
      }
      // Fallback context (no desktop window manager): print lore inline.
      return push(
        { kind: "input", text: raw },
        { kind: "accent", text: "◆ HIDDEN CHANNEL — TRANSMISSION ◆" },
        { kind: "output", text: "…full transmission lines here…" },
        { kind: "output", text: "Enter the OS to open the channel's window on the desktop." },
      );
    }

    if (cmd === "ls -a") {
      return push({ kind: "input", text: raw }, ...lsALines().map(text => ({ kind: "output" as const, text })));
    }

    const out = RESPONSES[cmd] ?? [`Unknown command: '${cmd}'. Type 'help' for available commands.`];
    push({ kind: "input", text: raw }, ...out.map(text => ({ kind: "output" as const, text })));
  };

  const onSequenceEnd = () => {
    setPlaying(false);
    const first = !isEggUnlocked();
    unlockEgg();
    push(
      { kind: "accent", text: "Alignment complete." },
      ...(first
        ? ([
            { kind: "accent", text: "▲ NEW SIGNAL DETECTED — a hidden channel has opened." },
            { kind: "output", text: "A new word answers now. Try: egg" },
          ] as Line[])
        : ([{ kind: "output", text: "The channel still listens. Try: egg" }] as Line[])),
    );
  };

  return (
    <div>
      {playing && <SequenceOverlay onEnd={onSequenceEnd} />}
      <div ref={scrollRef} /* scrollable output area */>
        {lines.map((l, i) => (
          <p key={i} data-kind={l.kind}>
            {l.kind === "input" ? `$ ${l.text}` : l.text}
          </p>
        ))}
      </div>
      <form
        onSubmit={e => {
          e.preventDefault();
          run(value);
          setValue("");
        }}>
        <input
          aria-label="Terminal input"
          value={value}
          onChange={e => setValue(e.target.value)}
          placeholder="speak to the node…"
        />
      </form>
    </div>
  );
}

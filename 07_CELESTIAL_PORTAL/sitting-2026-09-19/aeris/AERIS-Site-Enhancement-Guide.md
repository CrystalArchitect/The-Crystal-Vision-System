# AERIS Site Enhancement Guide

A step-by-step implementation guide for the next round of upgrades to the CrystalCore AERIS site (live at [crystalaeris-jwfbbvjs.manus.space](https://crystalaeris-jwfbbvjs.manus.space)). Each enhancement is grounded in the actual codebase — file paths, component names, and state patterns refer to what is already there — and ordered so that earlier steps make later ones easier. Everything stays frontend-only; no backend is required.

**Codebase orientation (current state):**

| File | Role |
|------|------|
| `client/src/pages/OS.tsx` | Desktop page: window manager, taskbar, boot overlay, beacon window integration |
| `client/src/components/aeris/AerisTerminal.tsx` | Terminal: lore commands, `non solus` trigger, `beacon` command, unlock state (`aeris.beacon.unlocked` in localStorage + `aeris:beacon-unlocked` DOM event) |
| `client/src/components/aeris/AlignmentSequence.tsx` | Full-screen cinematic overlay |
| `client/src/components/os/apps.tsx` | OS app window contents, including `BeaconApp` |
| `client/src/components/aeris/Starfield.tsx` | Canvas/DOM starfield behind the desktop |
| `client/src/index.css` | Global styles, alignment + beacon-reveal keyframes |

---

## Enhancement 1 — Terminal command history (arrow-up/down recall)

**Effort: small · Risk: low · Do this first** — it touches only the terminal input handler and immediately makes the terminal feel like a real shell.

1. In `AerisTerminal.tsx`, add two pieces of state next to the existing `value` state:
   ```tsx
   const [history, setHistory] = useState<string[]>([]);
   const [historyIndex, setHistoryIndex] = useState(-1); // -1 = live input
   const draftRef = useRef(""); // preserves what the user was typing before recalling
   ```
2. In the submit handler, after a command is executed, push it to history and reset the cursor:
   ```tsx
   setHistory((h) => (cmd && h[h.length - 1] !== cmd ? [...h, cmd] : h));
   setHistoryIndex(-1);
   ```
   The `h[h.length - 1] !== cmd` guard avoids consecutive duplicates, matching bash behaviour.
3. Add an `onKeyDown` on the input (keep the existing Enter handling):
   ```tsx
   if (e.key === "ArrowUp") {
     e.preventDefault();
     if (history.length === 0) return;
     if (historyIndex === -1) draftRef.current = value;
     const next = historyIndex === -1 ? history.length - 1 : Math.max(0, historyIndex - 1);
     setHistoryIndex(next); setValue(history[next]);
   } else if (e.key === "ArrowDown") {
     e.preventDefault();
     if (historyIndex === -1) return;
     const next = historyIndex + 1;
     if (next >= history.length) { setHistoryIndex(-1); setValue(draftRef.current); }
     else { setHistoryIndex(next); setValue(history[next]); }
   }
   ```
4. `e.preventDefault()` on both arrows matters — otherwise the caret jumps to the start/end of the input.
5. **Verify:** type three commands, press ArrowUp three times (walks back), ArrowDown past the newest (restores the in-progress draft). Also confirm recalling `non solus` re-triggers the sequence correctly.

*Optional flourish:* persist history to `sessionStorage` so it survives closing and reopening the terminal window within a session.

---

## Enhancement 2 — Typewriter output for terminal responses

**Effort: medium · Risk: medium** — the most visible upgrade, but it must not break the verification scripts or the easter-egg chain, which assert on final rendered text.

1. Extend the terminal's `Line` type with an optional animation flag: `{ text: string; kind: ...; typed?: boolean }`. Only mark *response* lines as `typed` — echoed input lines and the initial banner should render instantly.
2. Create a small `TypedLine` component inside `AerisTerminal.tsx`:
   ```tsx
   function TypedLine({ text, onDone }: { text: string; onDone?: () => void }) {
     const [n, setN] = useState(0);
     useEffect(() => {
       if (n >= text.length) { onDone?.(); return; }
       const t = setTimeout(() => setN(n + 1), 12); // ~80 chars/sec
       return () => clearTimeout(t);
     }, [n, text, onDone]);
     return <span>{text.slice(0, n)}{n < text.length && <span className="terminal-caret">▋</span>}</span>;
   }
   ```
3. **Sequence lines, don't parallelise them.** When a command returns multiple lines, animating all at once looks wrong. Keep a `pendingQueue` of lines and only promote the next line to `typed` rendering when the previous one calls `onDone`. Lines already completed render as plain text (important for performance — only one interval runs at a time).
4. **Instant-skip affordance:** clicking anywhere in the terminal output (or pressing Enter with an empty input) while typing is in progress should flush the queue and render everything instantly. This mirrors the click-to-skip convention already established by `AlignmentSequence`.
5. **Respect reduced motion:** gate the effect with `window.matchMedia("(prefers-reduced-motion: reduce)")` — render instantly when the user prefers reduced motion.
6. **Protect the easter-egg chain:** the `non solus` handler currently appends aftermath lines after the overlay ends; let those go through the typewriter (it heightens the moment), but make sure the `beacon` unlock itself is not delayed by the animation — unlock state must be written in `onEnd`, never after typing finishes.
7. **Verify:** re-run the 8-step chain test from `skills/web-os-easter-eggs/references/verification.md`. If the console scripts assert text before typing finishes, use the flush-on-Enter path in the test, or assert with a retry/poll.

---

## Enhancement 3 — Window minimize and restore

**Effort: medium · Risk: low** — completes the OS illusion; the window manager in `OS.tsx` already tracks open/focus/close, so this is one more state per window.

1. In `OS.tsx`, extend the per-window state (wherever `open` lives) with `minimized: boolean`.
2. Add a minimize button to the window title bar next to the existing close control — keep the glass style, use a `–` glyph, and `aria-label="Minimize window"`.
3. Minimizing sets `minimized: true` and moves focus to the next topmost non-minimized window. **Do not unmount the window content** — hide it with a class so live content (Mars clock ticking, Beacon timer) keeps running:
   ```css
   .window-minimized { transform: scale(0.9); opacity: 0; pointer-events: none; }
   ```
   with a ~200ms ease-out transition on `transform` and `opacity` (GPU-friendly, and consistent with the animation guide: never animate from `scale(0)`).
4. Taskbar behaviour: a minimized window's taskbar icon stays visible but dimmed (e.g. `opacity-60`). Clicking it restores (`minimized: false`) and focuses; clicking the icon of a focused, non-minimized window minimizes it — the standard OS toggle.
5. Edge case: if the hidden Beacon window is minimized and the user types `beacon` again, restore it rather than opening a duplicate.
6. **Verify:** minimize the Mars Clock, wait ten seconds, restore — the clock should show the advanced time, proving content stayed mounted.

---

## Enhancement 4 — Beacon ping in the starfield

**Effort: small · Risk: low** — a subtle desktop-level payoff for the existing unlock, reinforcing the second egg.

1. `Starfield.tsx` currently renders ambient stars. Give it awareness of the beacon unlock by reading `isBeaconUnlocked()` (exported from `AerisTerminal.tsx`) on mount and subscribing to the existing `aeris:beacon-unlocked` DOM event — the same pattern `OS.tsx` already uses, so no new plumbing.
2. When unlocked, add one special "beacon star": a fixed point in the upper-right sky that pulses every ~6 seconds — a soft gold expanding ring (reusing the alignment-ring keyframe family already in `index.css`, scaled down).
3. Keep it whisper-quiet: 2–3px core, ring expanding to ~40px at ~0.15 max opacity. It should be noticed only by someone who has unlocked the beacon and is paying attention — discoverability without shouting, per the layered-egg design rules.
4. Optional lore tie-in: add one line to the `beacon` command output — “The signal is visible from the desktop now. Look up.”
5. **Verify:** clear `localStorage`, confirm no ping; run the chain, confirm the ping appears without a reload (the DOM event should trigger it live).

---

## Enhancement 5 — Ambient audio toggle in the menu bar

**Effort: medium · Risk: medium** — sound is powerful for atmosphere but must be strictly opt-in.

1. Generate or source a short seamless ambient loop (deep-space drone, 30–60s, quiet). Upload it with `manus-upload-file --webdev` and reference the returned URL — never store the audio file inside the project directory.
2. Add a small speaker toggle to the `OS.tsx` menu bar (next to the live clock): muted icon by default, `aria-label="Toggle ambient sound"`.
3. Implement with a lazily created `HTMLAudioElement` (`loop = true`, `volume ≈ 0.25`). Create it on first toggle-on, not on page load — browsers block autoplay, and the user's first click is the required gesture.
4. Fade in/out by ramping `volume` over ~600ms with a small interval rather than hard-starting — hard audio starts feel jarring.
5. Persist the preference in `localStorage` (`aeris.audio.enabled`), but on reload **show the toggle as enabled without auto-playing** until the first user interaction (autoplay policy); resume on the first click anywhere.
6. Optional egg tie-in: during the `non solus` alignment sequence, if audio is enabled, duck the ambient loop and layer a single soft resonance swell timed to the ring expansion.
7. **Verify:** toggle on/off, reload and confirm the preference persists, and check the browser console for autoplay-policy warnings.

---

## Enhancement 6 — Layer 3 easter egg: the Starline Integrity Protocol

**Effort: large · Risk: medium** — extends the live two-layer chain to a third layer. Follow the *“Extending an existing chain”* rules from the `web-os-easter-eggs` skill: the previous layer's completion becomes the new unlock point, existing hints get a retro-hint pass, and the whole chain is re-verified from a cleared state.

1. **Design before code.** Proposed layer: after `beacon` is unlocked, the Beacon window's transmission gains one new corrupted line containing a fragment (e.g. a five-glyph key echoing the Five Keys lore). Entering that fragment as a terminal command — e.g. `align starline` — triggers a short second cinematic (a cascading node-map sweep across the Starline network) and permanently unlocks a `starline --integrity` readout plus a hidden “Integrity” panel inside the Starline Network window.
2. **Unlock state:** duplicate the existing pattern with new constants (`aeris.starline.unlocked`, `aeris:starline-unlocked`) in the same module as the beacon constants — keep non-component exports out of component files to preserve Vite Fast Refresh.
3. **Retro-hint pass:** update `ls -a` to show a third dotfile once beacon is unlocked; add one cryptic line to `beacon` output pointing at the Starline window; keep `help` clean of spoilers.
4. **Gate strictly:** `align starline` before beacon is unlocked should return an in-fiction static response (“…no carrier on that band yet.”) hinting at the prerequisite.
5. **Cinematic:** clone `AlignmentSequence.tsx` into a shorter (6–8s) `StarlineSweep.tsx` — same overlay contract: top z-index, staged lines, click-to-skip, idempotent `onEnd` that performs the unlock on both completion and skip.
6. **Verify from zero:** clear localStorage and run the full chain — `ls -a` → `non solus` → skip-path unlock → `beacon` → corrupted fragment → `align starline` → skip-path unlock → `starline --integrity` — using the browser-console method in the skill's `references/verification.md`.
7. **Hand over privately:** update the spoiler map for the owner; keep all public copy spoiler-free.

---

## Suggested order and checkpoints

| Step | Enhancement | Checkpoint after |
|------|-------------|------------------|
| 1 | Command history | — |
| 2 | Typewriter output | ✅ “Terminal feel: history + typewriter” |
| 3 | Minimize/restore | — |
| 4 | Beacon starfield ping | ✅ “Desktop polish: minimize + beacon ping” |
| 5 | Ambient audio toggle | ✅ “Ambient audio” |
| 6 | Layer-3 easter egg | ✅ “Starline Integrity chain” (after full-chain re-verification) |

Group related enhancements into a single checkpoint (auto-published on save), and re-run the full easter-egg chain verification after steps 2 and 6 — those are the two changes that can silently break the existing chain.

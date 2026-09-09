# Design Patterns for Layered Terminal Easter Eggs

## Layering model

Design eggs as a chain, each layer rewarding the previous discovery:

| Layer | Mechanic | Example |
|-------|----------|---------|
| 0 — Surface | Documented commands (`help` lists them) | lore commands: `codex`, `status`, `keys` |
| 1 — Hinted | Never in `help`; hinted by another command | `ls -a` reveals hidden dotfiles; one is `.non_solus` |
| 2 — Hidden trigger | Speaking the hidden word triggers a cinematic full-screen sequence | `non solus` → node-alignment overlay |
| 3 — Unlockable | Completing layer 2 permanently unlocks a new command | `beacon` opens a hidden desktop window |

Rules that make the chain feel fair:
- Every hidden thing must be discoverable through in-fiction hints, never require out-of-band knowledge. `help` hints at `ls -a`-style exploration; `ls -a` names the hidden file; the file name IS the command.
- A locked command must respond in-fiction, not error: "…static. The beacon does not answer the unaligned." plus a hint to the prerequisite.
- On unlock, announce loudly in the terminal ("▲ NEW SIGNAL DETECTED") AND visually outside it (new taskbar icon with a reveal animation), so the player cannot miss that state changed.
- Dynamic hints: commands like `ls -a` should reflect current lock state (`[LOCKED — requires alignment]` → `[UNLOCKED — the channel answers]`). Implement as a function evaluated at run time, not a static string table.

## Unlock-state pattern

Persist unlocks in `localStorage` and broadcast with a DOM event so sibling components (taskbar, desktop) react instantly without prop drilling:

- One key + one event name per egg, exported as constants from the terminal module.
- Wrap `localStorage` access in try/catch (private mode) — the event still unlocks the current session.
- Idempotent completion handler: distinguish first unlock (loud announcement) from repeat completions (quiet reminder line).
- See `templates/unlock-state.ts` for the exact module.
- Keep unlock constants and long lore data in a separate module (like `unlock-state.ts`), NOT in the terminal component file. Exporting non-component values from a component file breaks Vite Fast Refresh and forces full-page reloads on every edit.
- `localStorage` persists per-browser, which is right for public sites (discovery survives reloads and return visits). For kiosk demos or shared machines, switch to `sessionStorage` or skip persistence and rely on the event alone so each visitor starts locked.

## Full-screen cinematic sequence

The layer-2 payoff overlay (see `templates/SequenceOverlay.tsx`):
- Render at very high z-index above the whole desktop; `aria-label` it for testability.
- Structure: blackout fade-in → expanding rings/central motif → staged lore lines (600–900ms stagger, letter-spacing animation) → progress shimmer → auto-dismiss.
- Total runtime 8–14s, ALWAYS click-anywhere-to-skip; skipping must still fire the completion callback (and thus the unlock).
- Drive line staging with a single `setInterval` advancing an index; derive visibility from index comparison so React re-render stays cheap.
- On end, write "aftermath" lines back into the terminal so the fiction continues where the player left it.
- Center imagery with hard rectangular edges over a blackout: apply a radial CSS `mask-image` so the image dissolves into the background.

## Hidden window on an OS-style desktop

When the experience is a fake-OS desktop with a window manager:
- Register the hidden window in the normal window definition list, but filter its taskbar icon out until unlocked (`defs.filter(d => d.id !== "egg" || unlocked)`).
- The terminal receives an `onOpenBeacon`-style callback prop from the page that owns the window manager; outside the desktop (e.g. a landing-page embed of the same terminal), fall back to printing the lore inline and pointing the player to the OS route.
- Give the taskbar icon a one-shot reveal animation (scale 0.6 → 1.15 → 1 with a glow flare) so the unlock moment is visible even if the player is looking at the taskbar.
- Put something live in the hidden window (a ticking "channel held" timer, live stats) so it feels like a discovered place, not a static modal.

## Writing the lore

- Keep one consistent voice and 2–3 recurring phrases that echo across commands, the sequence, and the hidden window (e.g. a motto like "non solus" appearing everywhere).
- Command output should be short lines (terminal aesthetic), 1–6 lines per command; save long prose for the hidden window.
- Never list hidden commands in `help`. The deepest layer should only be hinted at AFTER the previous layer completes.

## Extending an existing chain (adding a deeper egg)

When a chain is already live and a new deeper layer is requested (e.g. adding `beacon` after `non solus` shipped):
- The previous layer's completion handler becomes the new unlock point: fire `unlockEgg()` there and append the announcement lines ("▲ NEW SIGNAL DETECTED — try: beacon") to the existing aftermath output.
- Do a **retro-hint pass** over all existing hint commands: `ls -a` gains a new dotfile entry with a lock-state suffix, `help`'s closing hint line may need to deepen, and the previous egg's own output should now gesture one layer further. A new layer that no old command acknowledges feels bolted-on.
- Keep the new unlock idempotent against replays: players will re-run the old trigger; repeat completions should print a quiet reminder, not duplicate the unlock fanfare.
- Re-verify the WHOLE chain from a cleared state, not just the new layer — the new unlock logic sits inside the old sequence's completion path and can regress it.

## Communicating the eggs without spoiling them

- Maintain a private spoiler document for the site owner listing every layer, trigger word, and unlock (the delivery message or a repo note), so the chain is never knowledge locked in one person's head.
- Keep public-facing copy spoiler-free: marketing text, commit messages on public repos, and presentation materials should describe the *mechanics* (layered hints, cinematic unlock) without printing the hidden words. Discovery is the product; a leaked trigger word deletes it.

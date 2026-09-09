---
name: web-os-easter-eggs
description: Build layered, discoverable easter eggs inside web-based fake-OS desktops or retro-terminal experiences — hidden commands, cinematic full-screen unlock sequences, and permanently unlockable secret windows/commands. Use when a user asks for terminal easter eggs, hidden lore commands, secret unlock chains, a "hidden window" or secret app on an OS-style website, or cinematic reveal sequences triggered by typed commands.
---

# Web OS Easter Eggs

Build multi-layer easter-egg chains for web terminals and fake-OS desktops: documented lore commands → hidden hint commands → a secret trigger word that plays a full-screen cinematic sequence → a permanent unlock that reveals a new command and hidden window.

## Workflow

0. **New chain or extension?** Building the first egg → follow all steps below. Adding a deeper layer to a live chain → read "Extending an existing chain" in `references/design-patterns.md` first: the previous layer's completion handler becomes the unlock point, all existing hint commands need a retro-hint pass, and the whole chain (not just the new layer) must be re-verified from a cleared state.

1. **Design the chain first.** Read `references/design-patterns.md` and map every layer before coding: which commands are documented in `help`, which command hints at the hidden word (e.g. `ls -a` revealing dotfiles), what the trigger word is, and what completing the sequence unlocks. The chain must be solvable purely from in-fiction hints.

2. **Implement unlock state.** Copy `templates/unlock-state.ts` (rename constants per egg). It pairs a `localStorage` key with a DOM event so the taskbar/desktop reacts to unlocks instantly, survives reloads, and degrades gracefully in private browsing. Keep unlock constants and long lore data in this module, not the component file — exporting non-component values from a component file breaks Vite Fast Refresh.

3. **Implement the terminal handler.** Follow `templates/Terminal.tsx`: special-case the hidden trigger and the unlockable command BEFORE the static response table; make hint commands (like `ls -a`) dynamic functions so their output reflects the current lock state; keep locked responses in-fiction ("…static.") with a hint to the prerequisite; accept an optional `onOpenEggWindow` callback and fall back to inline lore when the terminal is embedded outside the desktop.

4. **Implement the cinematic sequence.** Follow `templates/SequenceOverlay.tsx`: fixed full-screen overlay at top z-index, staged lore lines on a single interval, 8–14s runtime, click-anywhere-to-skip, and an idempotent `onEnd` that fires on BOTH natural completion and skip — the unlock lives in `onEnd`, so skipping must still unlock. Add the companion keyframes from the template's CSS comment to the global stylesheet.

5. **Wire the hidden window (desktop projects).** Register the secret window in the normal window-manager definitions but filter its taskbar icon until unlocked; animate the icon's first appearance with the `icon-reveal` keyframes; put live content (ticking timer, stats) inside the window so discovery feels rewarding.

6. **Verify the full chain programmatically.** Read `references/verification.md` and run its 8-step browser-console test order (locked probe → trigger → skip-unlocks check → unlocked open → dynamic hints → fallback context). The skip-path unlock and the React native-setter input technique are the two most commonly broken points. Do not chase mid-frame screenshots of the timed overlay — assert its DOM presence programmatically and confirm looks with at most one or two captures.

7. **Hand over without spoiling.** Give the owner a private spoiler map of every layer, trigger word, and unlock; keep all public-facing copy (marketing text, public commits, presentations) spoiler-free. See "Communicating the eggs without spoiling them" in `references/design-patterns.md`.

## Resources

| File | Read/copy when |
|------|----------------|
| `references/design-patterns.md` | Designing the egg chain, lore voice, unlock announcements, hidden-window reveal, extending a live chain, spoiler-safe handover |
| `references/verification.md` | Testing the chain in a real browser (React input driving, full test order) |
| `templates/unlock-state.ts` | Persisting and broadcasting unlock state |
| `templates/Terminal.tsx` | Terminal component with the layered command handler |
| `templates/SequenceOverlay.tsx` | Full-screen cinematic sequence + required CSS keyframes |

Templates are skeletons: restyle them to the host project's design system (fonts, colors, glass effects) — keep the handler structure, unlock flow, and accessibility labels (`aria-label` on input and overlay, used by the verification scripts).

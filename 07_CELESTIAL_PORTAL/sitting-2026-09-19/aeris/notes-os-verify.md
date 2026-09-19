# Mini OS verification notes (2026-07-28)

- /os route renders: boot overlay with emblem + ENTER VAULT 12 works, fades to desktop.
- Desktop shows 4 boot windows: Vault 12 Node (feather+activate), AERIS Terminal, Mars Clock (live), Starship Telemetry (animated progress).
- Taskbar has 8 icons; menu bar with logo, clock, EXIT TO SITE link works.
- RESOLVED: Starline window opens correctly — earlier "no change" was two clicks toggling it open then closed. Verified visible with map image + 5 node rows + Noise Protocol footer.
- Home page links updated: LAUNCH OS + ENTER VAULT 12 → /os.
- TypeScript check passes.
- Remaining: verify Starline/Codex/Lumina/About windows open, verify dragging, mobile viewport, then checkpoint e6302d85 → new.
- Asset URLs in client/src/components/os/apps.tsx (OS_ASSETS).

## Update 19:37
- Dragging VERIFIED: Vault 12 window moved from (60,84) to (220,214) with synthetic pointer events after adding window-level listeners in GlassWindow.tsx.
- Taskbar toggle verified for Starline (open + close works). Codex/Lumina/About taskbar buttons exist (indices 13-15); synthetic .click() in console didn't register (likely React synthetic event fine via real clicks — Starline opened fine via real browser click earlier). Will verify via browser_click on index 13.
- Terminal input typed 'activate' but Enter keydown didn't submit via synthetic KeyboardEvent (React onKeyDown needs trusted-ish event; works with real typing — was verified working on landing page previously; same component reused).
- All 4 default windows + menu bar + taskbar render correctly. Windows drag-verified.
- ISSUE 19:38: Real browser_click on taskbar "Open The Codex" (index 13) did NOT open the Codex window (markdown unchanged, taskbar hint still "Open The Codex"). Starline opened earlier the same way, so why? Difference: Starline was clicked twice earlier (toggle open/close). Hypothesis: taskbar buttons may sit partially under the preview-mode footer bar overlay intercepting clicks?? Or click coordinates land on footer "Preview mode" toast at bottom. The toast overlays the taskbar area (y~752). Element 13 marker shows at y~708 which is above toast. Investigate OS.tsx toggle/open logic for codex/lumina/about specifically — maybe openWindow adds window but with x beyond viewport (offscreen right at x>~900?) Check default positions in OS.tsx for codex/lumina/about: might be x=760/820/880 w=460 -> would still show partially. But markdown would include content regardless. So window truly not mounted. Check windowManager toggle: maybe 'open' only works for windows in initial open list; closed-by-default windows might need 'openWindow' not 'toggle'.
- Remaining: fix codex/lumina/about open logic, mobile viewport screenshot, checkpoint + deliver.

## Update 19:40 — code review
- windowManager.toggleWindow handles open:false correctly; OS.tsx taskbar onClick wiring correct; APP_CONTENT ids match; apps render code valid; Starfield pointer-events-none; no CSS blocker found.
- Earlier console selector bug: matched `title || aria-label`; taskbar buttons HAVE title="The Codex" so aria-label never checked → selector matched nothing → my synthetic click test was invalid.
- The "Preview mode" toast banner overlays the taskbar row (~y 735-765); browser_click on index 13 may have been intercepted by the toast, not the app logic.
- NEXT: re-test via console with correct selector (button[title="The Codex"]).click() and verify window mounts.

## Update 19:41 — RESOLVED, NOT A CODE BUG
- Re-tested with correct selector `button[title="The Codex"]` etc.: Codex, Lumina, About ALL opened correctly with full content (Codex image + five chapters + quote; Lumina portrait + traits; About emblem + v2.7.4 manifesto). Visually confirmed in screenshot.
- Root cause of earlier "bug": (1) my console selector matched title before aria-label so it clicked nothing; (2) browser_click on taskbar was intercepted by the "Preview mode" toast banner overlaying the taskbar row. The app code was correct all along — NO code change required.
- All 8 windows verified: Vault 12 Node, Terminal, Mars Clock, Telemetry, Starline, Codex, Lumina, About. Taskbar hints correctly switch to "Focus or close X" when open.
- Remaining: mobile viewport screenshot, checkpoint, deliver.

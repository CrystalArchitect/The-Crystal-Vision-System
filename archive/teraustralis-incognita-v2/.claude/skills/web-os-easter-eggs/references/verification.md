# Verifying Easter-Egg Chains in the Browser

Manual clicking is unreliable for timed overlays. Verify programmatically with browser console JS against the dev server.

## Driving a React-controlled terminal input

React ignores plain `.value =` assignment. Use the native setter, then dispatch `input` and submit the form:

```js
const input = document.querySelector('input[aria-label="Terminal input"]');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
const type = (cmd) => {
  setter.call(input, cmd);
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
};
```

## Full-chain test order (run in ONE console execution with awaits)

1. `localStorage.removeItem(UNLOCK_KEY)` and reload → guarantees locked baseline.
2. Locked probe: run the unlockable command → assert in-fiction refusal text appears; assert the hidden taskbar icon is absent.
3. Trigger the hidden command → wait ~1.5s → assert the overlay exists (`div[aria-label="…sequence"]`).
4. Skip path: `overlay.click()` → assert completion/unlock lines appear, `localStorage` key set, taskbar icon now present. (Skipping MUST unlock — this is the most commonly broken path.)
5. Unlocked command → assert the hidden window opens and contains its signature text.
6. Dynamic hints: re-run hint commands (`ls -a`) → assert they now show the unlocked variant.
7. Fallback context (e.g. landing-page terminal without the window manager): assert inline lore prints instead of a window.
8. Restore/clear state as appropriate and check devserver + browser console logs for errors.

## Screenshotting a timed overlay

Taking a screenshot after a console execution usually misses the overlay (it auto-dismisses). Either: trigger the sequence and screenshot immediately in the next action; or temporarily lengthen the stage interval while styling. Do not burn many cycles trying to catch an exact mid-frame — verify presence in DOM programmatically and confirm looks with one or two captures.

/**
 * Unlock-state module for a terminal easter-egg chain.
 * Export from the terminal component file (or its own module) so the
 * desktop page / taskbar can subscribe without prop drilling.
 * Rename EGG to the egg's name (e.g. BEACON).
 */
export const EGG_UNLOCK_KEY = "app.egg.unlocked";
export const EGG_UNLOCK_EVENT = "app:egg-unlocked";

export function isEggUnlocked(): boolean {
  try {
    return localStorage.getItem(EGG_UNLOCK_KEY) === "1";
  } catch {
    return false; // private mode — session-only unlock still works via the event
  }
}

export function unlockEgg(): void {
  try {
    localStorage.setItem(EGG_UNLOCK_KEY, "1");
  } catch {
    /* ignore — event below still unlocks this session */
  }
  window.dispatchEvent(new Event(EGG_UNLOCK_EVENT));
}

/**
 * Subscribe in the page that owns the taskbar/desktop:
 *
 *   const [unlocked, setUnlocked] = useState(() => isEggUnlocked());
 *   useEffect(() => {
 *     const on = () => setUnlocked(true);
 *     window.addEventListener(EGG_UNLOCK_EVENT, on);
 *     return () => window.removeEventListener(EGG_UNLOCK_EVENT, on);
 *   }, []);
 */

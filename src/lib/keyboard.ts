// SPDX-License-Identifier: MIT

export interface ShortcutHandlers {
  onSearch: () => void;
  onPalette: () => void;
  onNext: () => void;
  onPrev: () => void;
  onOpen: () => void;
  onAddToPlaylist: () => void;
  onEscape: () => void;
  onHelp: () => void;
  onNavigate: (path: string) => void;
}

const NAV_MAP: Record<string, string> = {
  h: "/",
  t: "/tracks",
  p: "/playlists",
  s: "/stats",
};

export function attachShortcuts(handlers: ShortcutHandlers): () => void {
  let pendingG = false;
  let gTimer: ReturnType<typeof setTimeout> | null = null;

  function clearG() {
    pendingG = false;
    if (gTimer) {
      clearTimeout(gTimer);
      gTimer = null;
    }
  }

  function isTypingTarget(el: EventTarget | null): boolean {
    if (!(el instanceof HTMLElement)) return false;
    const tag = el.tagName;
    return (
      tag === "INPUT" ||
      tag === "TEXTAREA" ||
      tag === "SELECT" ||
      el.isContentEditable
    );
  }

  function onKey(e: KeyboardEvent) {
    const mod = e.metaKey || e.ctrlKey;

    if (mod && e.key.toLowerCase() === "k") {
      e.preventDefault();
      handlers.onPalette();
      return;
    }

    if (e.key === "?" && !isTypingTarget(e.target)) {
      e.preventDefault();
      handlers.onHelp();
      return;
    }

    if (e.key === "Escape") {
      handlers.onEscape();
      return;
    }

    if (isTypingTarget(e.target)) return;

    if (e.key === "/") {
      e.preventDefault();
      handlers.onSearch();
      return;
    }

    if (pendingG) {
      const path = NAV_MAP[e.key.toLowerCase()];
      clearG();
      if (path) {
        e.preventDefault();
        handlers.onNavigate(path);
      }
      return;
    }

    if (e.key.toLowerCase() === "g") {
      pendingG = true;
      gTimer = setTimeout(clearG, 1200);
      return;
    }

    switch (e.key.toLowerCase()) {
      case "j":
        handlers.onNext();
        break;
      case "k":
        handlers.onPrev();
        break;
      case "enter":
        handlers.onOpen();
        break;
      case "p":
        handlers.onAddToPlaylist();
        break;
    }
  }

  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}

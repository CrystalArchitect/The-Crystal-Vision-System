// SPDX-License-Identifier: MIT

import { useEffect, useState } from "react";
import { attachShortcuts } from "../../lib/keyboard";
import CommandPalette from "./CommandPalette";

export default function KeyboardBridge() {
  const [showCommandPalette, setShowCommandPalette] = useState(false);
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    const cleanup = attachShortcuts({
      onSearch: () => {
        // Focus search input if it exists
        const searchInput = document.getElementById("track-search") as HTMLInputElement;
        searchInput?.focus();
      },
      onPalette: () => setShowCommandPalette(true),
      onNext: () => {
        // Handled by TrackTable component
      },
      onPrev: () => {
        // Handled by TrackTable component
      },
      onOpen: () => {
        // Handled by TrackTable component
      },
      onAddToPlaylist: () => {
        // Could implement playlist quick-add here
      },
      onEscape: () => {
        setShowCommandPalette(false);
        setShowHelp(false);
      },
      onHelp: () => setShowHelp(!showHelp),
      onNavigate: (path) => {
        window.location.href = path;
      },
    });

    return cleanup;
  }, []);

  return (
    <>
      <CommandPalette
        isOpen={showCommandPalette}
        onClose={() => setShowCommandPalette(false)}
      />

      {showHelp && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div className="bg-ink-900 border border-ink-800 rounded-lg max-w-lg max-h-96 overflow-y-auto">
            <div className="sticky top-0 bg-ink-950 border-b border-ink-800 px-6 py-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-white">Keyboard Shortcuts</h2>
              <button
                onClick={() => setShowHelp(false)}
                className="p-2 hover:bg-ink-800 rounded transition-colors text-neutral-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="p-6 space-y-4 text-sm">
              <div>
                <div className="font-mono font-semibold text-accent">⌘K / Ctrl+K</div>
                <div className="text-neutral-400">Open command palette</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">/</div>
                <div className="text-neutral-400">Focus search</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">j / k</div>
                <div className="text-neutral-400">Navigate tracks</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">Enter</div>
                <div className="text-neutral-400">Open selected track</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">p</div>
                <div className="text-neutral-400">Add to playlist</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">g then h/t/p/s</div>
                <div className="text-neutral-400">Navigate (home/tracks/playlists/stats)</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">?</div>
                <div className="text-neutral-400">Show this help</div>
              </div>
              <div>
                <div className="font-mono font-semibold text-accent">Escape</div>
                <div className="text-neutral-400">Close dialogs</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

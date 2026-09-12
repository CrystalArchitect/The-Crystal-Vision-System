// SPDX-License-Identifier: MIT

import { useEffect, useRef, useState } from "react";

interface Command {
  id: string;
  title: string;
  description?: string;
  action: () => void;
  shortcut?: string;
}

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function CommandPalette({ isOpen, onClose }: Props) {
  const [search, setSearch] = useState("");
  const [selectedIdx, setSelectedIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const commands: Command[] = [
    {
      id: "home",
      title: "Home",
      description: "Go to home page",
      action: () => (window.location.href = "/"),
    },
    {
      id: "tracks",
      title: "Browse Tracks",
      description: "Browse all tracks",
      action: () => (window.location.href = "/tracks"),
    },
    {
      id: "playlists",
      title: "Playlists",
      description: "View your playlists",
      action: () => (window.location.href = "/playlists"),
    },
    {
      id: "stats",
      title: "Stats",
      description: "View statistics",
      action: () => (window.location.href = "/stats"),
    },
    {
      id: "artists",
      title: "Artists",
      description: "Browse by artist",
      action: () => (window.location.href = "/artists"),
    },
    {
      id: "timeline",
      title: "Timeline",
      description: "Browse by year",
      action: () => (window.location.href = "/timeline"),
    },
    {
      id: "rediscover",
      title: "Rediscover",
      description: "Find hidden gems",
      action: () => (window.location.href = "/rediscover"),
    },
  ];

  const filtered = commands.filter((cmd) =>
    cmd.title.toLowerCase().includes(search.toLowerCase()) ||
    cmd.description?.toLowerCase().includes(search.toLowerCase())
  );

  useEffect(() => {
    if (isOpen) {
      setSearch("");
      setSelectedIdx(0);
      setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isOpen) return;

      switch (e.key) {
        case "ArrowDown":
          e.preventDefault();
          setSelectedIdx((i) => Math.min(i + 1, filtered.length - 1));
          break;
        case "ArrowUp":
          e.preventDefault();
          setSelectedIdx((i) => Math.max(i - 1, 0));
          break;
        case "Enter":
          e.preventDefault();
          filtered[selectedIdx]?.action();
          onClose();
          break;
        case "Escape":
          e.preventDefault();
          onClose();
          break;
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, selectedIdx, filtered, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-black/50 flex items-start justify-center pt-16">
      <div className="bg-ink-900 border border-ink-800 rounded-lg shadow-xl w-full max-w-md">
        <div className="border-b border-ink-800 p-4">
          <input
            ref={inputRef}
            type="text"
            placeholder="Search commands..."
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setSelectedIdx(0);
            }}
            className="w-full bg-transparent text-white placeholder-neutral-600 outline-none text-sm"
          />
        </div>

        <div className="max-h-96 overflow-y-auto">
          {filtered.length === 0 ? (
            <div className="p-4 text-center text-neutral-500 text-sm">No commands found</div>
          ) : (
            filtered.map((cmd, idx) => (
              <button
                key={cmd.id}
                onClick={() => {
                  cmd.action();
                  onClose();
                }}
                className={`w-full text-left px-4 py-3 border-b border-ink-800/50 last:border-b-0 transition-colors ${
                  idx === selectedIdx
                    ? "bg-ink-800 text-white"
                    : "hover:bg-ink-800 text-neutral-300 hover:text-white"
                }`}
              >
                <div className="font-medium text-sm">{cmd.title}</div>
                {cmd.description && (
                  <div className="text-xs text-neutral-500 mt-1">{cmd.description}</div>
                )}
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

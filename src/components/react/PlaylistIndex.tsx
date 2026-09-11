// SPDX-License-Identifier: MIT

import { useState } from "react";
import type { Playlist } from "../../types";
import { getUserMeta, createPlaylist, deletePlaylist, updatePlaylist } from "../../lib/storage";

interface Props {
  onMetaChange: () => void;
}

export default function PlaylistIndex({ onMetaChange }: Props) {
  const meta = getUserMeta();
  const playlists = meta.playlists ?? [];
  const [newName, setNewName] = useState("");
  const [newDesc, setNewDesc] = useState("");

  const handleCreate = () => {
    if (!newName.trim()) return;
    createPlaylist(newName, newDesc);
    setNewName("");
    setNewDesc("");
    onMetaChange();
  };

  const handleDelete = (id: string) => {
    if (confirm("Delete this playlist?")) {
      deletePlaylist(id);
      onMetaChange();
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-ink-900 border border-ink-800 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-white mb-4">Create Playlist</h2>
        <div className="space-y-3">
          <input
            type="text"
            placeholder="Playlist name"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            className="w-full rounded border border-ink-700 bg-ink-950 px-3 py-2 text-sm text-white placeholder-neutral-600 focus:border-accent outline-none"
          />
          <textarea
            placeholder="Description (optional)"
            value={newDesc}
            onChange={(e) => setNewDesc(e.target.value)}
            rows={3}
            className="w-full rounded border border-ink-700 bg-ink-950 px-3 py-2 text-sm text-white placeholder-neutral-600 focus:border-accent outline-none resize-none"
          />
          <button
            onClick={handleCreate}
            disabled={!newName.trim()}
            className="w-full px-4 py-2 rounded bg-accent-400 text-ink-950 font-medium hover:bg-accent-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Create
          </button>
        </div>
      </div>

      <div>
        <h2 className="text-lg font-semibold text-white mb-4">Your Playlists</h2>
        {playlists.length === 0 ? (
          <div className="text-center py-12 text-neutral-500">
            <p>No playlists yet. Create one above!</p>
          </div>
        ) : (
          <div className="space-y-3">
            {playlists.map((pl) => (
              <div
                key={pl.id}
                className="bg-ink-900 border border-ink-800 rounded-lg p-4 flex items-center justify-between hover:border-ink-700 transition-colors"
              >
                <div className="min-w-0">
                  <a
                    href={`/playlist/${pl.id}`}
                    className="text-white font-medium hover:text-accent transition-colors truncate block"
                  >
                    {pl.name}
                  </a>
                  {pl.description && (
                    <p className="text-xs text-neutral-500 mt-1 truncate">{pl.description}</p>
                  )}
                  <p className="text-xs text-neutral-600 mt-2">
                    {pl.trackIds.length} track{pl.trackIds.length !== 1 ? "s" : ""}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(pl.id)}
                  className="ml-4 px-3 py-1 text-xs rounded border border-ink-700 text-neutral-400 hover:text-red-400 hover:border-red-700 transition-colors flex-shrink-0"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

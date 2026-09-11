// SPDX-License-Identifier: MIT

import { useEffect, useState } from "react";
import type { Track, Playlist } from "../../types";
import { getUserMeta, removeTrackFromPlaylist, reorderPlaylistTracks } from "../../lib/storage";

interface Props {
  playlistId: string;
  allTracks: Track[];
  onMetaChange: () => void;
}

export default function PlaylistView({ playlistId, allTracks, onMetaChange }: Props) {
  const meta = getUserMeta();
  const playlist = meta.playlists?.find((p) => p.id === playlistId);
  const [draggedTrack, setDraggedTrack] = useState<string | null>(null);

  if (!playlist) {
    return <div className="text-center py-12 text-neutral-500">Playlist not found</div>;
  }

  const playlistTracks = playlist.trackIds
    .map((id) => allTracks.find((t) => t.id === id))
    .filter((t): t is Track => !!t);

  const handleDragStart = (trackId: string) => {
    setDraggedTrack(trackId);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.add("bg-ink-800");
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.currentTarget.classList.remove("bg-ink-800");
  };

  const handleDrop = (e: React.DragEvent, targetId: string) => {
    e.preventDefault();
    e.currentTarget.classList.remove("bg-ink-800");

    if (draggedTrack && draggedTrack !== targetId) {
      const newOrder = [...playlist.trackIds];
      const fromIdx = newOrder.indexOf(draggedTrack);
      const toIdx = newOrder.indexOf(targetId);

      if (fromIdx !== -1 && toIdx !== -1) {
        newOrder.splice(fromIdx, 1);
        newOrder.splice(toIdx, 0, draggedTrack);
        reorderPlaylistTracks(playlistId, newOrder);
        onMetaChange();
      }
    }

    setDraggedTrack(null);
  };

  const handleRemoveTrack = (trackId: string) => {
    removeTrackFromPlaylist(playlistId, trackId);
    onMetaChange();
  };

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">{playlist.name}</h1>
        {playlist.description && (
          <p className="text-neutral-400">{playlist.description}</p>
        )}
        <p className="text-xs text-neutral-600 mt-2">
          {playlistTracks.length} track{playlistTracks.length !== 1 ? "s" : ""}
        </p>
      </div>

      {playlistTracks.length === 0 ? (
        <div className="text-center py-12 text-neutral-500">
          <p>No tracks in this playlist yet</p>
        </div>
      ) : (
        <div className="space-y-2">
          {playlistTracks.map((track) => (
            <div
              key={track.id}
              draggable
              onDragStart={() => handleDragStart(track.id)}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={(e) => handleDrop(e, track.id)}
              className={`p-3 rounded border border-ink-800 bg-ink-900 flex items-center justify-between hover:border-ink-700 transition-colors cursor-grab active:cursor-grabbing ${
                draggedTrack === track.id ? "opacity-50" : ""
              }`}
            >
              <div className="min-w-0">
                <div className="text-white font-medium truncate">{track.title}</div>
                <div className="text-xs text-neutral-500">{track.artist}</div>
              </div>
              <button
                onClick={() => handleRemoveTrack(track.id)}
                className="ml-4 px-2 py-1 text-xs rounded border border-ink-700 text-neutral-400 hover:text-red-400 hover:border-red-700 transition-colors flex-shrink-0"
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track, Realm } from "../../types";

interface PlaylistSharerProps {
  tracks: Track[];
  realms: Realm[];
}

interface SavedPlaylist {
  id: string;
  name: string;
  description: string;
  tracks: Track[];
  createdAt: number;
  shareUrl: string;
}

export default function PlaylistSharer({ tracks, realms }: PlaylistSharerProps) {
  const [playlistName, setPlaylistName] = useState<string>("My Playlist");
  const [playlistDescription, setPlaylistDescription] = useState<string>("");
  const [selectedTracks, setSelectedTracks] = useState<Set<string>>(new Set());
  const [savedPlaylists, setSavedPlaylists] = useState<SavedPlaylist[]>([]);
  const [shareMode, setShareMode] = useState<"create" | "saved">("create");

  const toggleTrack = (trackId: string) => {
    const newSelected = new Set(selectedTracks);
    if (newSelected.has(trackId)) {
      newSelected.delete(trackId);
    } else {
      newSelected.add(trackId);
    }
    setSelectedTracks(newSelected);
  };

  const selectedTracksData = useMemo(() => {
    return Array.from(selectedTracks)
      .map(id => tracks.find(t => t.id === id))
      .filter((t): t is Track => !!t);
  }, [selectedTracks, tracks]);

  const savePlaylist = () => {
    if (selectedTracksData.length === 0) {
      alert("Please select at least one track");
      return;
    }

    const newPlaylist: SavedPlaylist = {
      id: `playlist-${Date.now()}`,
      name: playlistName || "Untitled Playlist",
      description: playlistDescription,
      tracks: selectedTracksData,
      createdAt: Date.now(),
      shareUrl: `${window.location.origin}/share/${encodeURIComponent(playlistName)}?tracks=${Array.from(selectedTracks).join(",")}`,
    };

    setSavedPlaylists([newPlaylist, ...savedPlaylists]);
    setPlaylistName("My Playlist");
    setPlaylistDescription("");
    setSelectedTracks(new Set());
  };

  const copyShareUrl = (url: string) => {
    navigator.clipboard.writeText(url);
    alert("Share URL copied to clipboard!");
  };

  const downloadPlaylist = (playlist: SavedPlaylist) => {
    const playlistData = {
      name: playlist.name,
      description: playlist.description,
      tracks: playlist.tracks.map(t => ({
        title: t.title,
        artist: t.artist,
        year: t.year,
        bpm: t.bpm,
        duration: t.duration,
        genres: t.genres,
      })),
      createdAt: new Date(playlist.createdAt).toISOString(),
    };

    const dataStr = JSON.stringify(playlistData, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${playlist.name}.json`;
    link.click();
  };

  const totalDuration = Math.round(
    selectedTracksData.reduce((sum, t) => sum + t.duration, 0) / 60
  );

  return (
    <div className="space-y-6">
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setShareMode("create")}
            className={`px-4 py-2 rounded font-medium transition ${
              shareMode === "create"
                ? "bg-accent-500 text-ink-900"
                : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
            }`}
          >
            Create Playlist
          </button>
          <button
            onClick={() => setShareMode("saved")}
            className={`px-4 py-2 rounded font-medium transition ${
              shareMode === "saved"
                ? "bg-accent-500 text-ink-900"
                : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
            }`}
          >
            Saved Playlists ({savedPlaylists.length})
          </button>
        </div>

        {shareMode === "create" && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-neutral-300 mb-2">
                Playlist Name
              </label>
              <input
                type="text"
                value={playlistName}
                onChange={(e) => setPlaylistName(e.target.value)}
                className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-neutral-300 mb-2">
                Description (optional)
              </label>
              <textarea
                value={playlistDescription}
                onChange={(e) => setPlaylistDescription(e.target.value)}
                className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500"
                rows={3}
                placeholder="Add notes about this playlist..."
              />
            </div>

            <div className="bg-ink-700 rounded p-4">
              <div className="flex justify-between items-center mb-3">
                <h4 className="text-sm font-semibold text-white">
                  Search & Select Tracks ({selectedTracks.size})
                </h4>
                {selectedTracks.size > 0 && (
                  <span className="text-xs text-neutral-400">
                    {totalDuration} min
                  </span>
                )}
              </div>

              <input
                type="text"
                placeholder="Search tracks..."
                className="w-full bg-ink-600 border border-accent-500/30 rounded px-2 py-1 text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500 mb-3"
                onChange={(e) => {
                  // Filter tracks by search - simplified for demo
                  const query = e.target.value.toLowerCase();
                  if (query.length === 0) {
                    setSelectedTracks(new Set());
                  }
                }}
              />

              <div className="space-y-1 max-h-48 overflow-y-auto">
                {tracks.slice(0, 50).map(track => (
                  <button
                    key={track.id}
                    onClick={() => toggleTrack(track.id)}
                    className={`w-full text-left px-2 py-1 rounded text-xs transition ${
                      selectedTracks.has(track.id)
                        ? "bg-accent-500 text-ink-900"
                        : "hover:bg-ink-600"
                    }`}
                  >
                    <div className="font-medium">{track.title}</div>
                    <div className="opacity-75">{track.artist} • {track.year}</div>
                  </button>
                ))}
              </div>
            </div>

            {selectedTracks.size > 0 && (
              <button
                onClick={savePlaylist}
                className="w-full bg-accent-500 hover:bg-accent-600 text-ink-900 font-semibold py-2 rounded transition"
              >
                Save & Share Playlist
              </button>
            )}
          </div>
        )}

        {shareMode === "saved" && (
          <div className="space-y-3">
            {savedPlaylists.length === 0 ? (
              <p className="text-center text-neutral-400">No saved playlists yet. Create one to get started!</p>
            ) : (
              savedPlaylists.map(playlist => (
                <div key={playlist.id} className="bg-ink-700 rounded p-4 border border-accent-500/20">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-semibold text-white">{playlist.name}</h4>
                      {playlist.description && (
                        <p className="text-xs text-neutral-400 mt-1">{playlist.description}</p>
                      )}
                    </div>
                    <span className="text-xs text-neutral-500">
                      {playlist.tracks.length} tracks
                    </span>
                  </div>

                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={() => copyShareUrl(playlist.shareUrl)}
                      className="flex-1 bg-accent-500/20 hover:bg-accent-500/30 text-accent-400 text-xs font-medium py-1 rounded transition"
                    >
                      📋 Copy Link
                    </button>
                    <button
                      onClick={() => downloadPlaylist(playlist)}
                      className="flex-1 bg-accent-500/20 hover:bg-accent-500/30 text-accent-400 text-xs font-medium py-1 rounded transition"
                    >
                      📥 Download
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
}

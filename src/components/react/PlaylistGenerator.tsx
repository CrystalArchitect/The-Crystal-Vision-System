// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track, Realm } from "../../types";

interface PlaylistGeneratorProps {
  tracks: Track[];
  realms: Realm[];
}

export default function PlaylistGenerator({ tracks, realms }: PlaylistGeneratorProps) {
  const [selectedRealms, setSelectedRealms] = useState<string[]>(realms.slice(0, 2).map(r => r.id));
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [bpmMin, setBpmMin] = useState<number>(80);
  const [bpmMax, setBpmMax] = useState<number>(180);
  const [playlistSize, setPlaylistSize] = useState<number>(25);

  const generatedPlaylist = useMemo(() => {
    let filtered = [...tracks];

    // Filter by realm
    if (selectedRealms.length > 0) {
      filtered = filtered.filter(t => selectedRealms.includes(t.realm || ""));
    }

    // Filter by genre
    if (selectedGenres.length > 0) {
      filtered = filtered.filter(t =>
        t.genres.some(g => selectedGenres.includes(g))
      );
    }

    // Filter by BPM
    filtered = filtered.filter(t => t.bpm >= bpmMin && t.bpm <= bpmMax);

    // Shuffle and slice
    return filtered
      .sort(() => Math.random() - 0.5)
      .slice(0, playlistSize);
  }, [tracks, selectedRealms, selectedGenres, bpmMin, bpmMax, playlistSize]);

  const allGenres = Array.from(
    new Set(tracks.flatMap(t => t.genres))
  ).sort();

  const avgBpm = generatedPlaylist.length > 0
    ? Math.round(generatedPlaylist.reduce((sum, t) => sum + t.bpm, 0) / generatedPlaylist.length)
    : 0;

  const duration = Math.round(
    generatedPlaylist.reduce((sum, t) => sum + t.duration, 0) / 60
  );

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h3 className="text-xl font-bold text-white mb-4">Playlist Generator</h3>

        {/* Realm Selection */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-neutral-300 mb-2">Realms</label>
          <div className="flex flex-wrap gap-2">
            {realms.map(realm => (
              <button
                key={realm.id}
                onClick={() => {
                  setSelectedRealms(prev =>
                    prev.includes(realm.id)
                      ? prev.filter(id => id !== realm.id)
                      : [...prev, realm.id]
                  );
                }}
                className={`px-3 py-2 rounded text-sm font-medium transition ${
                  selectedRealms.includes(realm.id)
                    ? 'bg-accent-500 text-ink-900'
                    : 'bg-ink-700 text-neutral-300 hover:bg-ink-600'
                }`}
              >
                {realm.iconEmoji} {realm.name}
              </button>
            ))}
          </div>
        </div>

        {/* Genre Selection */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-neutral-300 mb-2">Genres</label>
          <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
            {allGenres.map(genre => (
              <button
                key={genre}
                onClick={() => {
                  setSelectedGenres(prev =>
                    prev.includes(genre)
                      ? prev.filter(g => g !== genre)
                      : [...prev, genre]
                  );
                }}
                className={`px-3 py-1 rounded text-xs font-medium transition whitespace-nowrap ${
                  selectedGenres.includes(genre)
                    ? 'bg-accent-500 text-ink-900'
                    : 'bg-ink-700 text-neutral-300 hover:bg-ink-600'
                }`}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>

        {/* BPM Range */}
        <div className="mb-6 grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Min BPM: {bpmMin}
            </label>
            <input
              type="range"
              min="60"
              max="200"
              value={bpmMin}
              onChange={(e) => setBpmMin(Math.min(Number(e.target.value), bpmMax))}
              className="w-full accent-accent-500"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Max BPM: {bpmMax}
            </label>
            <input
              type="range"
              min="60"
              max="200"
              value={bpmMax}
              onChange={(e) => setBpmMax(Math.max(Number(e.target.value), bpmMin))}
              className="w-full accent-accent-500"
            />
          </div>
        </div>

        {/* Playlist Size */}
        <div>
          <label className="block text-sm font-semibold text-neutral-300 mb-2">
            Playlist Size: {playlistSize} tracks
          </label>
          <input
            type="range"
            min="5"
            max="100"
            step="5"
            value={playlistSize}
            onChange={(e) => setPlaylistSize(Number(e.target.value))}
            className="w-full accent-accent-500"
          />
        </div>
      </div>

      {/* Playlist Info */}
      {generatedPlaylist.length > 0 && (
        <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-white">Generated Playlist</h3>
            <div className="text-sm text-neutral-400">
              {generatedPlaylist.length} tracks • {duration} min • Avg {avgBpm} BPM
            </div>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {generatedPlaylist.map((track, idx) => (
              <div key={idx} className="flex items-center justify-between rounded bg-ink-700 px-3 py-2 text-sm">
                <div className="flex-1">
                  <div className="font-medium text-white">{idx + 1}. {track.title}</div>
                  <div className="text-xs text-neutral-400">{track.artist}</div>
                </div>
                <div className="flex items-center gap-4 text-xs text-neutral-400">
                  <span>{track.year}</span>
                  <span>{track.bpm} BPM</span>
                  <span>{Math.floor(track.duration / 60)}:{String(track.duration % 60).padStart(2, '0')}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {generatedPlaylist.length === 0 && (
        <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20 text-center text-neutral-400">
          No tracks match your filters. Try adjusting your selections.
        </div>
      )}
    </div>
  );
}

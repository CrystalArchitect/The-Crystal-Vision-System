// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track } from "../../types";
import { applyFilters, applySort, type FilterState, type SortState } from "../../lib/search";
import TrackTable from "./TrackTable";

interface Props {
  tracks: Track[];
  realms: any[];
}

const BPM_PRESETS = [
  { label: "Fast (170+)", min: 170, max: 200 },
  { label: "Medium (140-160)", min: 140, max: 160 },
  { label: "Slow (90-130)", min: 90, max: 130 },
];

const MUSIC_KEYS = [
  "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
];

export default function AdvancedSearch({ tracks, realms }: Props) {
  const [filters, setFilters] = useState<FilterState>({
    q: "",
    year: null,
    category: null,
    artist: null,
    remixer: null,
    tag: null,
    minRating: 0,
    hasRemix: null,
    isVIP: null,
    duplicatesOnly: false,
    realm: null,
    bpmMin: null,
    bpmMax: null,
    key: null,
    genres: [],
  });

  const [sort, setSort] = useState<SortState>({ key: "artist", dir: "asc" });
  const [selectedTrack, setSelectedTrack] = useState<Track | null>(null);

  const allGenres = useMemo(() => {
    const genreSet = new Set<string>();
    tracks.forEach((t) => t.genres.forEach((g) => genreSet.add(g)));
    return Array.from(genreSet).sort();
  }, [tracks]);

  const allYears = useMemo(() => {
    return [...new Set(tracks.map((t) => t.year))].sort((a, b) => b - a);
  }, [tracks]);

  const allArtists = useMemo(() => {
    return [...new Set(tracks.map((t) => t.artist))].sort();
  }, [tracks]);

  const filteredTracks = useMemo(
    () => applyFilters(tracks, filters, () => undefined),
    [tracks, filters]
  );

  const sortedTracks = useMemo(
    () => applySort(filteredTracks, sort, () => undefined),
    [filteredTracks, sort]
  );

  const handleGenreToggle = (genre: string) => {
    setFilters((prev) => ({
      ...prev,
      genres: prev.genres.includes(genre)
        ? prev.genres.filter((g) => g !== genre)
        : [...prev.genres, genre],
    }));
  };

  const handleBPMPreset = (min: number, max: number) => {
    setFilters((prev) => ({
      ...prev,
      bpmMin: prev.bpmMin === min && prev.bpmMax === max ? null : min,
      bpmMax: prev.bpmMin === min && prev.bpmMax === max ? null : max,
    }));
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h2 className="text-2xl font-bold text-white mb-6">Advanced Search</h2>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
          {/* Full-Text Search */}
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Search
            </label>
            <input
              type="text"
              placeholder="Track, artist, label..."
              value={filters.q}
              onChange={(e) =>
                setFilters((prev) => ({ ...prev, q: e.target.value }))
              }
              className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500"
            />
          </div>

          {/* Artist Filter */}
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Artist
            </label>
            <select
              value={filters.artist || ""}
              onChange={(e) =>
                setFilters((prev) => ({
                  ...prev,
                  artist: e.target.value || null,
                }))
              }
              className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white focus:outline-none focus:border-accent-500"
            >
              <option value="">All artists</option>
              {allArtists.map((artist) => (
                <option key={artist} value={artist}>
                  {artist}
                </option>
              ))}
            </select>
          </div>

          {/* Year Filter */}
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Year
            </label>
            <select
              value={filters.year || ""}
              onChange={(e) =>
                setFilters((prev) => ({
                  ...prev,
                  year: e.target.value ? parseInt(e.target.value, 10) : null,
                }))
              }
              className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white focus:outline-none focus:border-accent-500"
            >
              <option value="">All years</option>
              {allYears.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>

          {/* Key Filter */}
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Music Key
            </label>
            <select
              value={filters.key || ""}
              onChange={(e) =>
                setFilters((prev) => ({
                  ...prev,
                  key: e.target.value || null,
                }))
              }
              className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white focus:outline-none focus:border-accent-500"
            >
              <option value="">All keys</option>
              {MUSIC_KEYS.map((key) => (
                <option key={key} value={key}>
                  {key}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* BPM Presets */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-neutral-300 mb-3">
            BPM Presets
          </label>
          <div className="flex flex-wrap gap-2">
            {BPM_PRESETS.map(({ label, min, max }) => (
              <button
                key={label}
                onClick={() => handleBPMPreset(min, max)}
                className={`px-4 py-2 rounded text-sm font-medium transition ${
                  filters.bpmMin === min && filters.bpmMax === max
                    ? "bg-accent-500 text-ink-900"
                    : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
                }`}
              >
                {label}
              </button>
            ))}
            {(filters.bpmMin !== null || filters.bpmMax !== null) && (
              <button
                onClick={() =>
                  setFilters((prev) => ({
                    ...prev,
                    bpmMin: null,
                    bpmMax: null,
                  }))
                }
                className="px-4 py-2 rounded text-sm font-medium bg-ink-700 text-neutral-300 hover:bg-ink-600 transition"
              >
                Reset BPM
              </button>
            )}
          </div>

          {/* Custom BPM Range */}
          <div className="mt-3 flex gap-2">
            <div className="flex-1">
              <label className="text-xs text-neutral-400">Min BPM</label>
              <input
                type="number"
                min="50"
                max="200"
                value={filters.bpmMin || ""}
                onChange={(e) =>
                  setFilters((prev) => ({
                    ...prev,
                    bpmMin: e.target.value ? parseInt(e.target.value, 10) : null,
                  }))
                }
                className="w-full bg-ink-700 border border-accent-500/30 rounded px-2 py-1 text-white text-sm focus:outline-none focus:border-accent-500"
                placeholder="50"
              />
            </div>
            <div className="flex-1">
              <label className="text-xs text-neutral-400">Max BPM</label>
              <input
                type="number"
                min="50"
                max="200"
                value={filters.bpmMax || ""}
                onChange={(e) =>
                  setFilters((prev) => ({
                    ...prev,
                    bpmMax: e.target.value ? parseInt(e.target.value, 10) : null,
                  }))
                }
                className="w-full bg-ink-700 border border-accent-500/30 rounded px-2 py-1 text-white text-sm focus:outline-none focus:border-accent-500"
                placeholder="200"
              />
            </div>
          </div>
        </div>

        {/* Genre Filters */}
        <div>
          <label className="block text-sm font-semibold text-neutral-300 mb-3">
            Genres
          </label>
          <div className="flex flex-wrap gap-2">
            {allGenres.map((genre) => (
              <button
                key={genre}
                onClick={() => handleGenreToggle(genre)}
                className={`px-3 py-1 rounded text-xs font-medium transition ${
                  filters.genres.includes(genre)
                    ? "bg-accent-500 text-ink-900"
                    : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
                }`}
              >
                {genre}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-white">
            Results: {sortedTracks.length} / {tracks.length}
          </h3>
          <div className="flex gap-2">
            <select
              value={sort.key}
              onChange={(e) =>
                setSort((prev) => ({
                  ...prev,
                  key: e.target.value as any,
                }))
              }
              className="bg-ink-700 border border-accent-500/30 rounded px-2 py-1 text-sm text-white focus:outline-none focus:border-accent-500"
            >
              <option value="artist">Artist</option>
              <option value="title">Title</option>
              <option value="year">Year</option>
            </select>
            <button
              onClick={() =>
                setSort((prev) => ({
                  ...prev,
                  dir: prev.dir === "asc" ? "desc" : "asc",
                }))
              }
              className="bg-ink-700 hover:bg-ink-600 border border-accent-500/30 rounded px-2 py-1 text-sm text-white transition"
            >
              {sort.dir === "asc" ? "↑" : "↓"}
            </button>
          </div>
        </div>

        {sortedTracks.length > 0 ? (
          <div className="max-h-96 overflow-y-auto">
            <div className="space-y-1">
              {sortedTracks.slice(0, 50).map((track) => (
                <button
                  key={track.id}
                  onClick={() => setSelectedTrack(track)}
                  className="w-full text-left px-3 py-2 rounded hover:bg-ink-700 transition text-xs"
                >
                  <div className="font-medium text-white truncate">
                    {track.title}
                  </div>
                  <div className="text-neutral-400 truncate">
                    {track.artist} • {track.year} • {track.bpm} BPM
                    {track.key && ` • ${track.key}`}
                  </div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <p className="text-center text-neutral-400 py-8">
            No tracks match your search criteria
          </p>
        )}
      </div>
    </div>
  );
}

// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track } from "../../types";

interface ArtistDiscoveryProps {
  tracks: Track[];
}

interface ArtistInfo {
  name: string;
  trackCount: number;
  genres: string[];
  avgBpm: number;
  yearRange: { min: number; max: number };
  topRealm: string;
  isRemixer: boolean;
  collaborations: number;
}

export default function ArtistDiscovery({ tracks }: ArtistDiscoveryProps) {
  const [selectedArtist, setSelectedArtist] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");

  const artistStats = useMemo(() => {
    const artists = new Map<string, {
      tracks: Track[];
      realms: Set<string>;
      remixCount: number;
      collaborators: Set<string>;
    }>();

    tracks.forEach(track => {
      // Track main artist
      if (!artists.has(track.artist)) {
        artists.set(track.artist, {
          tracks: [],
          realms: new Set(),
          remixCount: 0,
          collaborators: new Set()
        });
      }

      const artistData = artists.get(track.artist)!;
      artistData.tracks.push(track);
      if (track.realm) {
        artistData.realms.add(track.realm);
      }
      if (track.isRemix) {
        artistData.remixCount++;
      }

      // Track featured artists as collaborators
      if (track.featured) {
        track.featured.forEach(featured => {
          artistData.collaborators.add(featured);
        });
      }

      // Add remixer as collaborator
      if (track.remixer) {
        artistData.collaborators.add(track.remixer);
      }
    });

    // Convert to display format
    const artistList: [string, ArtistInfo][] = Array.from(artists.entries()).map(
      ([name, data]) => {
        const genres = Array.from(
          new Set(data.tracks.flatMap(t => t.genres))
        );
        const years = data.tracks.map(t => t.year);
        const avgBpm = Math.round(
          data.tracks.reduce((sum, t) => sum + t.bpm, 0) / data.tracks.length
        );

        return [
          name,
          {
            name,
            trackCount: data.tracks.length,
            genres,
            avgBpm,
            yearRange: {
              min: Math.min(...years),
              max: Math.max(...years),
            },
            topRealm: Array.from(data.realms)[0] || "Unknown",
            isRemixer: data.remixCount > 0,
            collaborations: data.collaborators.size,
          },
        ];
      }
    );

    return artistList;
  }, [tracks]);

  const filteredArtists = useMemo(() => {
    if (!searchQuery.trim()) {
      return artistStats
        .sort((a, b) => b[1].trackCount - a[1].trackCount)
        .slice(0, 50);
    }

    return artistStats
      .filter(([name]) =>
        name.toLowerCase().includes(searchQuery.toLowerCase())
      )
      .sort((a, b) => b[1].trackCount - a[1].trackCount);
  }, [artistStats, searchQuery]);

  const selectedArtistData = selectedArtist
    ? artistStats.find(([name]) => name === selectedArtist)
    : null;

  const selectedArtistTracks = selectedArtistData
    ? tracks.filter(t => t.artist === selectedArtist)
    : [];

  return (
    <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
      <h3 className="text-xl font-bold text-white mb-4">Artist Discovery</h3>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Search & List */}
        <div className="lg:col-span-1">
          <input
            type="text"
            placeholder="Search artists..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500 mb-4"
          />

          <div className="space-y-1 max-h-96 overflow-y-auto">
            {filteredArtists.map(([name, info]) => (
              <button
                key={name}
                onClick={() => setSelectedArtist(name)}
                className={`w-full text-left px-3 py-2 rounded transition ${
                  selectedArtist === name
                    ? 'bg-accent-500 text-ink-900'
                    : 'bg-ink-700 text-neutral-300 hover:bg-ink-600'
                }`}
              >
                <div className="font-medium truncate">{name}</div>
                <div className="text-xs opacity-75">{info.trackCount} tracks</div>
              </button>
            ))}
          </div>
        </div>

        {/* Details */}
        {selectedArtistData && (
          <div className="lg:col-span-2">
            <div className="mb-4">
              <h4 className="text-lg font-bold text-white mb-3">{selectedArtistData[0]}</h4>

              <div className="grid grid-cols-2 gap-3 mb-4">
                <div className="bg-ink-700 rounded p-3">
                  <div className="text-xs text-neutral-400">Tracks</div>
                  <div className="text-xl font-bold text-accent-400">
                    {selectedArtistData[1].trackCount}
                  </div>
                </div>
                <div className="bg-ink-700 rounded p-3">
                  <div className="text-xs text-neutral-400">Collaborations</div>
                  <div className="text-xl font-bold text-accent-400">
                    {selectedArtistData[1].collaborations}
                  </div>
                </div>
                <div className="bg-ink-700 rounded p-3">
                  <div className="text-xs text-neutral-400">Avg BPM</div>
                  <div className="text-xl font-bold text-accent-400">
                    {selectedArtistData[1].avgBpm}
                  </div>
                </div>
                <div className="bg-ink-700 rounded p-3">
                  <div className="text-xs text-neutral-400">Year Range</div>
                  <div className="text-xl font-bold text-accent-400">
                    {selectedArtistData[1].yearRange.min} - {selectedArtistData[1].yearRange.max}
                  </div>
                </div>
              </div>

              <div className="mb-3">
                <div className="text-xs text-neutral-400 mb-1">Genres</div>
                <div className="flex flex-wrap gap-1">
                  {selectedArtistData[1].genres.slice(0, 5).map(genre => (
                    <span
                      key={genre}
                      className="px-2 py-1 bg-accent-500/20 border border-accent-500/50 rounded text-xs text-accent-300"
                    >
                      {genre}
                    </span>
                  ))}
                </div>
              </div>

              {selectedArtistData[1].isRemixer && (
                <div className="text-xs text-neutral-400 mb-3">
                  ⚡ Remix Artist (remixing culture contributor)
                </div>
              )}
            </div>

            {/* Top Tracks */}
            <div>
              <h5 className="text-sm font-semibold text-neutral-300 mb-2">Top Tracks</h5>
              <div className="space-y-1 max-h-48 overflow-y-auto">
                {selectedArtistTracks
                  .sort((a, b) => b.year - a.year)
                  .slice(0, 10)
                  .map((track, idx) => (
                    <div key={idx} className="text-xs bg-ink-700 rounded px-2 py-1">
                      <div className="font-medium text-white truncate">{track.title}</div>
                      <div className="text-neutral-400">{track.year} • {track.bpm} BPM</div>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        )}

        {!selectedArtistData && (
          <div className="lg:col-span-2 flex items-center justify-center text-neutral-400">
            Select an artist to view details
          </div>
        )}
      </div>
    </div>
  );
}

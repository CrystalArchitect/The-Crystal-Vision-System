// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track, Realm } from "../../types";

interface RealmComparisonProps {
  tracks: Track[];
  realms: Realm[];
}

export default function RealmComparison({ tracks, realms }: RealmComparisonProps) {
  const [selectedRealms, setSelectedRealms] = useState<string[]>(realms.slice(0, 2).map(r => r.id));

  const realmStats = useMemo(() => {
    const stats = new Map<string, {
      trackCount: number;
      artistCount: number;
      avgBpm: number;
      yearRange: { min: number; max: number };
      genres: string[];
      topGenre: string;
    }>();

    realms.forEach(realm => {
      const realmTracks = tracks.filter(t => t.realm === realm.id);
      const artists = new Set(realmTracks.map(t => t.artist));
      const genres = new Map<string, number>();

      realmTracks.forEach(track => {
        track.genres.forEach(genre => {
          genres.set(genre, (genres.get(genre) || 0) + 1);
        });
      });

      const sortedGenres = Array.from(genres.entries())
        .sort((a, b) => b[1] - a[1])
        .map(([genre]) => genre);

      const years = realmTracks.map(t => t.year);
      const avgBpm = realmTracks.length > 0
        ? realmTracks.reduce((sum, t) => sum + t.bpm, 0) / realmTracks.length
        : 0;

      stats.set(realm.id, {
        trackCount: realmTracks.length,
        artistCount: artists.size,
        avgBpm: Math.round(avgBpm),
        yearRange: {
          min: Math.min(...years),
          max: Math.max(...years),
        },
        genres: sortedGenres,
        topGenre: sortedGenres[0] || "N/A",
      });
    });

    return stats;
  }, [tracks, realms]);

  const comparedRealms = realms.filter(r => selectedRealms.includes(r.id));

  return (
    <div className="space-y-6">
      {/* Realm Selector */}
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h3 className="text-lg font-bold text-white mb-4">Select Realms to Compare</h3>
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
              className={`px-4 py-2 rounded text-sm font-medium transition ${
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

      {/* Comparison Grid */}
      {selectedRealms.length > 0 && (
        <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
          <h3 className="text-lg font-bold text-white mb-6">Realm Comparison</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-accent-500/20">
                  <th className="text-left py-3 px-4 text-neutral-400 font-semibold">Metric</th>
                  {comparedRealms.map(realm => (
                    <th
                      key={realm.id}
                      className="text-left py-3 px-4 text-accent-400 font-semibold whitespace-nowrap"
                    >
                      {realm.iconEmoji} {realm.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-accent-500/10">
                <tr>
                  <td className="py-3 px-4 text-neutral-300">Tracks</td>
                  {comparedRealms.map(realm => {
                    const stats = realmStats.get(realm.id);
                    return (
                      <td key={realm.id} className="py-3 px-4 text-white font-bold">
                        {stats?.trackCount.toLocaleString()}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="py-3 px-4 text-neutral-300">Artists</td>
                  {comparedRealms.map(realm => {
                    const stats = realmStats.get(realm.id);
                    return (
                      <td key={realm.id} className="py-3 px-4 text-white font-bold">
                        {stats?.artistCount}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="py-3 px-4 text-neutral-300">Avg BPM</td>
                  {comparedRealms.map(realm => {
                    const stats = realmStats.get(realm.id);
                    return (
                      <td key={realm.id} className="py-3 px-4 text-white font-bold">
                        {stats?.avgBpm}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="py-3 px-4 text-neutral-300">Year Span</td>
                  {comparedRealms.map(realm => {
                    const stats = realmStats.get(realm.id);
                    return (
                      <td key={realm.id} className="py-3 px-4 text-white font-bold">
                        {stats?.yearRange.min} - {stats?.yearRange.max}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="py-3 px-4 text-neutral-300">Top Genre</td>
                  {comparedRealms.map(realm => {
                    const stats = realmStats.get(realm.id);
                    return (
                      <td key={realm.id} className="py-3 px-4 text-accent-400">
                        {stats?.topGenre}
                      </td>
                    );
                  })}
                </tr>
                <tr>
                  <td className="py-3 px-4 text-neutral-300">Tracks per Artist</td>
                  {comparedRealms.map(realm => {
                    const stats = realmStats.get(realm.id);
                    const ratio = stats ? (stats.trackCount / stats.artistCount).toFixed(1) : "0";
                    return (
                      <td key={realm.id} className="py-3 px-4 text-white font-bold">
                        {ratio}
                      </td>
                    );
                  })}
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track, Realm } from "../../types";

interface ComparisonSharerProps {
  realms: Realm[];
  tracks: Track[];
}

interface SharedComparison {
  id: string;
  name: string;
  realms: string[];
  createdAt: number;
  shareUrl: string;
}

export default function ComparisonSharer({
  realms,
  tracks,
}: ComparisonSharerProps) {
  const [selectedRealms, setSelectedRealms] = useState<string[]>(
    realms.slice(0, 2).map(r => r.id)
  );
  const [comparisonName, setComparisonName] = useState<string>("Realm Comparison");
  const [sharedComparisons, setSharedComparisons] = useState<SharedComparison[]>([]);
  const [viewMode, setViewMode] = useState<"builder" | "shared">("builder");

  const toggleRealm = (realmId: string) => {
    setSelectedRealms(prev =>
      prev.includes(realmId)
        ? prev.filter(id => id !== realmId)
        : [...prev, realmId]
    );
  };

  const comparisonData = useMemo(() => {
    const selectedRealmData = realms.filter(r =>
      selectedRealms.includes(r.id)
    );

    const stats = selectedRealmData.map(realm => {
      const realmTracks = tracks.filter(t => t.realm === realm.id);
      const artists = new Set(realmTracks.map(t => t.artist));
      const genres = new Map<string, number>();

      realmTracks.forEach(track => {
        track.genres.forEach(genre => {
          genres.set(genre, (genres.get(genre) || 0) + 1);
        });
      });

      const avgBpm = realmTracks.length > 0
        ? Math.round(
            realmTracks.reduce((sum, t) => sum + t.bpm, 0) / realmTracks.length
          )
        : 0;

      const years = realmTracks.map(t => t.year);

      return {
        realm,
        trackCount: realmTracks.length,
        artistCount: artists.size,
        avgBpm,
        yearRange: {
          min: Math.min(...years),
          max: Math.max(...years),
        },
        topGenres: Array.from(genres.entries())
          .sort((a, b) => b[1] - a[1])
          .slice(0, 3)
          .map(([genre]) => genre),
        tracksPerArtist: (realmTracks.length / artists.size).toFixed(1),
      };
    });

    return stats;
  }, [selectedRealms, realms, tracks]);

  const shareComparison = () => {
    if (selectedRealms.length < 2) {
      alert("Please select at least 2 realms to compare");
      return;
    }

    const newComparison: SharedComparison = {
      id: `comparison-${Date.now()}`,
      name: comparisonName,
      realms: selectedRealms,
      createdAt: Date.now(),
      shareUrl: `${window.location.origin}/share/comparison?realms=${selectedRealms.join(",")}`,
    };

    setSharedComparisons([newComparison, ...sharedComparisons]);
    setComparisonName("Realm Comparison");
  };

  const copyShareUrl = (url: string) => {
    navigator.clipboard.writeText(url);
    alert("Share URL copied to clipboard!");
  };

  return (
    <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setViewMode("builder")}
          className={`px-4 py-2 rounded font-medium transition ${
            viewMode === "builder"
              ? "bg-accent-500 text-ink-900"
              : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
          }`}
        >
          Build Comparison
        </button>
        <button
          onClick={() => setViewMode("shared")}
          className={`px-4 py-2 rounded font-medium transition ${
            viewMode === "shared"
              ? "bg-accent-500 text-ink-900"
              : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
          }`}
        >
          Shared Comparisons ({sharedComparisons.length})
        </button>
      </div>

      {viewMode === "builder" && (
        <div className="space-y-6">
          {/* Realm Selection */}
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-3">
              Select Realms to Compare
            </label>
            <div className="flex flex-wrap gap-2">
              {realms.map(realm => (
                <button
                  key={realm.id}
                  onClick={() => toggleRealm(realm.id)}
                  className={`px-4 py-2 rounded text-sm font-medium transition ${
                    selectedRealms.includes(realm.id)
                      ? "bg-accent-500 text-ink-900"
                      : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
                  }`}
                >
                  {realm.iconEmoji} {realm.name}
                </button>
              ))}
            </div>
          </div>

          {/* Comparison Name */}
          <div>
            <label className="block text-sm font-semibold text-neutral-300 mb-2">
              Comparison Name
            </label>
            <input
              type="text"
              value={comparisonName}
              onChange={(e) => setComparisonName(e.target.value)}
              className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500"
            />
          </div>

          {/* Comparison Table */}
          {comparisonData.length >= 2 && (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-accent-500/20">
                    <th className="text-left py-3 px-4 text-neutral-400 font-semibold">
                      Metric
                    </th>
                    {comparisonData.map(({ realm }) => (
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
                    {comparisonData.map(({ realm, trackCount }) => (
                      <td
                        key={realm.id}
                        className="py-3 px-4 text-white font-bold"
                      >
                        {trackCount.toLocaleString()}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 px-4 text-neutral-300">Artists</td>
                    {comparisonData.map(({ realm, artistCount }) => (
                      <td
                        key={realm.id}
                        className="py-3 px-4 text-white font-bold"
                      >
                        {artistCount}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 px-4 text-neutral-300">Avg BPM</td>
                    {comparisonData.map(({ realm, avgBpm }) => (
                      <td
                        key={realm.id}
                        className="py-3 px-4 text-white font-bold"
                      >
                        {avgBpm}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 px-4 text-neutral-300">Year Span</td>
                    {comparisonData.map(({ realm, yearRange }) => (
                      <td
                        key={realm.id}
                        className="py-3 px-4 text-white font-bold"
                      >
                        {yearRange.min} - {yearRange.max}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 px-4 text-neutral-300">
                      Tracks/Artist
                    </td>
                    {comparisonData.map(({ realm, tracksPerArtist }) => (
                      <td
                        key={realm.id}
                        className="py-3 px-4 text-white font-bold"
                      >
                        {tracksPerArtist}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 px-4 text-neutral-300">Top Genres</td>
                    {comparisonData.map(({ realm, topGenres }) => (
                      <td key={realm.id} className="py-3 px-4">
                        <div className="flex flex-wrap gap-1">
                          {topGenres.map(genre => (
                            <span
                              key={genre}
                              className="px-2 py-0.5 bg-accent-500/20 border border-accent-500/50 rounded text-xs text-accent-300"
                            >
                              {genre}
                            </span>
                          ))}
                        </div>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          )}

          {selectedRealms.length >= 2 && (
            <button
              onClick={shareComparison}
              className="w-full bg-accent-500 hover:bg-accent-600 text-ink-900 font-semibold py-2 rounded transition"
            >
              Share Comparison
            </button>
          )}
        </div>
      )}

      {viewMode === "shared" && (
        <div className="space-y-3">
          {sharedComparisons.length === 0 ? (
            <p className="text-center text-neutral-400">
              No shared comparisons yet. Create one to share with others!
            </p>
          ) : (
            sharedComparisons.map(comparison => (
              <div
                key={comparison.id}
                className="bg-ink-700 rounded p-4 border border-accent-500/20"
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-white">
                    {comparison.name}
                  </h4>
                  <span className="text-xs text-neutral-500">
                    {comparison.realms.length} realms
                  </span>
                </div>

                <div className="mb-3 flex flex-wrap gap-1">
                  {comparison.realms.map(realmId => {
                    const realm = realms.find(r => r.id === realmId);
                    return realm ? (
                      <span
                        key={realmId}
                        className="px-2 py-1 bg-accent-500/20 border border-accent-500/50 rounded text-xs text-accent-300"
                      >
                        {realm.iconEmoji} {realm.name}
                      </span>
                    ) : null;
                  })}
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => copyShareUrl(comparison.shareUrl)}
                    className="flex-1 bg-accent-500/20 hover:bg-accent-500/30 text-accent-400 text-xs font-medium py-1 rounded transition"
                  >
                    📋 Copy Link
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

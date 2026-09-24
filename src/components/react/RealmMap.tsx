// SPDX-License-Identifier: MIT

import { useMemo } from "react";
import type { Track, Realm } from "../../types";

interface RealmMapProps {
  realms: Realm[];
  tracks: Track[];
}

export default function RealmMap({ realms, tracks }: RealmMapProps) {
  const realmsByRegion = useMemo(() => {
    const regions = new Map<string, { realms: Realm[]; trackCount: number }>();

    realms.forEach(realm => {
      const realmTracks = tracks.filter(t => t.realm === realm.id).length;
      const region = realm.region || "Global";

      if (!regions.has(region)) {
        regions.set(region, { realms: [], trackCount: 0 });
      }

      const regionData = regions.get(region)!;
      regionData.realms.push(realm);
      regionData.trackCount += realmTracks;
    });

    return regions;
  }, [realms, tracks]);

  // Largest per-realm track count, used to normalize the distribution bars.
  const maxRealmTrackCount = useMemo(() => {
    let max = 1;
    realms.forEach(realm => {
      const count = tracks.filter(t => t.realm === realm.id).length;
      if (count > max) max = count;
    });
    return max;
  }, [realms, tracks]);

  const regionOrder = ["Oceania", "Asia", "Europe", "North America", "Global"];

  const sortedRegions = Array.from(realmsByRegion.entries())
    .sort((a, b) => {
      const aIdx = regionOrder.indexOf(a[0]);
      const bIdx = regionOrder.indexOf(b[0]);
      return (aIdx === -1 ? 999 : aIdx) - (bIdx === -1 ? 999 : bIdx);
    });

  const getColorClass = (color: string): string => {
    const colorMap: Record<string, string> = {
      cyan: "bg-cyan-500/20 border-cyan-500/50",
      blue: "bg-blue-500/20 border-blue-500/50",
      green: "bg-green-500/20 border-green-500/50",
      red: "bg-red-500/20 border-red-500/50",
      purple: "bg-purple-500/20 border-purple-500/50",
      black: "bg-slate-600/20 border-slate-600/50",
      magenta: "bg-pink-500/20 border-pink-500/50",
      gold: "bg-yellow-500/20 border-yellow-500/50",
      yellow: "bg-amber-500/20 border-amber-500/50",
      orange: "bg-orange-500/20 border-orange-500/50",
      teal: "bg-teal-500/20 border-teal-500/50",
    };
    return colorMap[color] || "bg-accent-500/20 border-accent-500/50";
  };

  return (
    <div className="space-y-6">
      {sortedRegions.map(([region, data]) => (
        <div key={region}>
          <h2 className="text-2xl font-bold text-white mb-4">{region}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.realms.map(realm => {
              const realmTracks = tracks.filter(t => t.realm === realm.id);
              const percentage = ((realmTracks.length / tracks.length) * 100).toFixed(1);

              return (
                <div
                  key={realm.id}
                  className={`rounded-lg border p-6 transition-all hover:shadow-lg hover:shadow-accent-500/20 ${getColorClass(realm.color)}`}
                >
                  <div className="flex items-center gap-3 mb-3">
                    <span className="text-3xl">{realm.iconEmoji}</span>
                    <h3 className="text-lg font-bold text-white">{realm.name}</h3>
                  </div>

                  <p className="text-sm text-neutral-300 mb-4">{realm.description}</p>

                  <div className="space-y-2 mb-4 text-xs text-neutral-400">
                    <div className="flex justify-between">
                      <span>Tracks:</span>
                      <span className="text-accent-400 font-semibold">{realmTracks.length.toLocaleString()} ({percentage}%)</span>
                    </div>
                    <div className="flex justify-between">
                      <span>BPM Range:</span>
                      <span className="text-accent-400">{realm.bpmRange.min} - {realm.bpmRange.max}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Mood:</span>
                      <span className="text-accent-400 text-right">{realm.mood}</span>
                    </div>
                  </div>

                  <div className="mb-3">
                    <div className="text-xs text-neutral-400 mb-1">Top Genres</div>
                    <div className="flex flex-wrap gap-1">
                      {realm.genres.slice(0, 3).map(genre => (
                        <span key={genre} className="px-2 py-1 bg-ink-700 rounded text-xs text-neutral-300">
                          {genre}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="bg-ink-700 rounded h-2 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-accent-500 to-accent-400 h-full"
                      style={{width: `${(realmTracks.length / maxRealmTrackCount) * 100}%`}}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

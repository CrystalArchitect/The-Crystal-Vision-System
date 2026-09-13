// SPDX-License-Identifier: MIT

import { useMemo } from "react";
import type { Track } from "../../types";

interface TrendAnalysisProps {
  tracks: Track[];
}

export default function TrendAnalysis({ tracks }: TrendAnalysisProps) {
  const { trendsByYear, trendsByRealm, topGrowthRealms } = useMemo(() => {
    // Trends by year
    const yearGroups = new Map<number, { realms: Map<string, number>; genres: Map<string, number> }>();

    tracks.forEach(track => {
      if (!yearGroups.has(track.year)) {
        yearGroups.set(track.year, { realms: new Map(), genres: new Map() });
      }
      const group = yearGroups.get(track.year)!;

      if (track.realm) {
        group.realms.set(track.realm, (group.realms.get(track.realm) || 0) + 1);
      }
      track.genres.forEach(genre => {
        group.genres.set(genre, (group.genres.get(genre) || 0) + 1);
      });
    });

    const sortedYears = Array.from(yearGroups.entries()).sort((a, b) => a[0] - b[0]);

    // Trends by realm
    const realmData = new Map<string, { years: number[]; counts: number[] }>();
    sortedYears.forEach(([year, group]) => {
      group.realms.forEach((count, realm) => {
        if (!realmData.has(realm)) {
          realmData.set(realm, { years: [], counts: [] });
        }
        realmData.get(realm)!.years.push(year);
        realmData.get(realm)!.counts.push(count);
      });
    });

    // Calculate growth (first year to last year for each realm)
    const growthByRealm = Array.from(realmData.entries())
      .map(([realm, data]) => {
        const firstYear = data.counts[0] || 0;
        const lastYear = data.counts[data.counts.length - 1] || 0;
        const growth = lastYear - firstYear;
        const growthPercent = firstYear > 0 ? ((lastYear - firstYear) / firstYear * 100) : 0;
        return { realm, firstYear, lastYear, growth, growthPercent };
      })
      .sort((a, b) => b.growth - a.growth);

    return {
      trendsByYear: sortedYears,
      trendsByRealm: realmData,
      topGrowthRealms: growthByRealm.slice(0, 5),
    };
  }, [tracks]);

  return (
    <div className="space-y-8">
      {/* Growth Trends by Realm */}
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h3 className="text-xl font-bold text-white mb-4">Realm Growth Trends</h3>
        <div className="space-y-3">
          {topGrowthRealms.map(({ realm, firstYear, lastYear, growth, growthPercent }) => (
            <div key={realm}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-neutral-300">{realm}</span>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-neutral-400">{firstYear} → {lastYear}</span>
                  <span className={`text-sm font-bold ${growthPercent >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {growthPercent >= 0 ? '+' : ''}{growthPercent.toFixed(0)}%
                  </span>
                </div>
              </div>
              <div className="bg-ink-700 rounded h-2 overflow-hidden">
                <div
                  className={`h-full ${growthPercent >= 0 ? 'bg-green-500' : 'bg-red-500'}`}
                  style={{ width: `${Math.min(100, Math.abs(growthPercent / 2))}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Year-over-Year Summary */}
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h3 className="text-xl font-bold text-white mb-4">Coverage by Decade</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
          {Array.from({ length: 6 }).map((_, i) => {
            const decadeStart = 1970 + i * 10;
            const decadeEnd = decadeStart + 9;
            const decadeTracks = Array.from(trendsByYear)
              .filter(([year]) => year >= decadeStart && year <= decadeEnd)
              .reduce((sum, [, group]) => sum + group.realms.size, 0);

            return (
              <div key={i} className="bg-ink-700 rounded p-3 text-center border border-accent-500/10">
                <div className="text-xs text-neutral-400">{decadeStart}s</div>
                <div className="text-lg font-bold text-accent-400 mt-1">
                  {Array.from(trendsByYear)
                    .filter(([year]) => year >= decadeStart && year <= decadeEnd)
                    .reduce((sum, [, group]) => sum + group.realms.size, 0)}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

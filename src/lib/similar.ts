// SPDX-License-Identifier: MIT

import type { Track } from "../types";

export interface SimilarOptions {
  limit?: number;
  weights?: {
    artist?: number;
    year?: number;
  };
}

const DEFAULT_WEIGHTS = {
  artist: 3,
  year: 1,
};

export interface TagLookup {
  (trackId: string): string[] | undefined;
}

export function findSimilar(
  target: Track,
  all: Track[],
  tagLookup: TagLookup,
  opts: SimilarOptions = {}
): Array<{ track: Track; score: number }> {
  const limit = opts.limit ?? 8;
  const w = { ...DEFAULT_WEIGHTS, ...opts.weights };

  const scored: Array<{ track: Track; score: number }> = [];

  for (const t of all) {
    if (t.id === target.id) continue;

    let score = 0;

    if (t.artist === target.artist) score += w.artist;
    if (t.year === target.year) score += w.year;

    if (score > 0) scored.push({ track: t, score });
  }

  scored.sort((a, b) => b.score - a.score || a.track.id.localeCompare(b.track.id));
  return scored.slice(0, limit);
}

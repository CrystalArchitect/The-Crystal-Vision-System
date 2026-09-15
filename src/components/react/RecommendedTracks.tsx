// SPDX-License-Identifier: MIT

import { useMemo, useState } from "react";
import type { Track } from "../../types";
import {
  recommendSimilarTracks,
  recommendForPlaylist,
  getTrendingByGenre,
  getGenreBasedRecommendations,
} from "../../lib/recommendations";

interface Props {
  tracks: Track[];
  referenceTrack?: Track;
  playlist?: Track[];
  selectedGenres?: string[];
}

type RecommendationType = "similar" | "playlist" | "trending" | "genre";

export default function RecommendedTracks({
  tracks,
  referenceTrack,
  playlist,
  selectedGenres,
}: Props) {
  const [recommendationType, setRecommendationType] = useState<RecommendationType>(
    referenceTrack ? "similar" : "playlist"
  );

  const allGenres = useMemo(() => {
    const genres = new Set<string>();
    tracks.forEach((t) => t.genres.forEach((g) => genres.add(g)));
    return Array.from(genres).sort();
  }, [tracks]);

  const [trendingGenre, setTrendingGenre] = useState<string>(allGenres[0] || "");

  const recommendations = useMemo(() => {
    switch (recommendationType) {
      case "similar":
        return referenceTrack
          ? recommendSimilarTracks(referenceTrack, tracks, 10)
          : [];
      case "playlist":
        return playlist ? recommendForPlaylist(playlist, tracks, 10) : [];
      case "trending":
        return trendingGenre
          ? getTrendingByGenre(tracks, trendingGenre, 10)
          : [];
      case "genre":
        return selectedGenres && selectedGenres.length > 0
          ? getGenreBasedRecommendations(selectedGenres, tracks, 10)
          : [];
      default:
        return [];
    }
  }, [
    recommendationType,
    referenceTrack,
    playlist,
    trendingGenre,
    selectedGenres,
    tracks,
  ]);

  const getTitle = (): string => {
    switch (recommendationType) {
      case "similar":
        return `Tracks Similar to "${referenceTrack?.title}"`;
      case "playlist":
        return "Recommended Additions to Playlist";
      case "trending":
        return `Trending in ${trendingGenre}`;
      case "genre":
        return `Tracks in ${selectedGenres?.join(", ")}`;
      default:
        return "Recommendations";
    }
  };

  const getDescription = (): string => {
    switch (recommendationType) {
      case "similar":
        return "Based on genre, BPM, and artistic style";
      case "playlist":
        return "Suggestions that match your playlist's vibe";
      case "trending":
        return "Recent releases gaining momentum";
      case "genre":
        return "Curated by your selected genres";
      default:
        return "";
    }
  };

  const canShowSimilar = !!referenceTrack;
  const canShowPlaylist = !!playlist;
  const canShowTrending = allGenres.length > 0;
  const canShowGenre = !!selectedGenres && selectedGenres.length > 0;

  if (!canShowSimilar && !canShowPlaylist && !canShowTrending && !canShowGenre) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-white">{getTitle()}</h2>
            <p className="text-sm text-neutral-400">{getDescription()}</p>
          </div>
        </div>

        {/* Recommendation Type Selector */}
        <div className="flex flex-wrap gap-2 mb-6">
          {canShowSimilar && (
            <button
              onClick={() => setRecommendationType("similar")}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                recommendationType === "similar"
                  ? "bg-accent-500 text-ink-900"
                  : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
              }`}
            >
              Similar Tracks
            </button>
          )}
          {canShowPlaylist && (
            <button
              onClick={() => setRecommendationType("playlist")}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                recommendationType === "playlist"
                  ? "bg-accent-500 text-ink-900"
                  : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
              }`}
            >
              For Playlist
            </button>
          )}
          {canShowTrending && (
            <button
              onClick={() => setRecommendationType("trending")}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                recommendationType === "trending"
                  ? "bg-accent-500 text-ink-900"
                  : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
              }`}
            >
              Trending
            </button>
          )}
          {canShowGenre && (
            <button
              onClick={() => setRecommendationType("genre")}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                recommendationType === "genre"
                  ? "bg-accent-500 text-ink-900"
                  : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
              }`}
            >
              By Genre
            </button>
          )}
        </div>

        {/* Genre Selector for Trending */}
        {recommendationType === "trending" && allGenres.length > 0 && (
          <div className="mb-6">
            <select
              value={trendingGenre}
              onChange={(e) => setTrendingGenre(e.target.value)}
              className="w-full bg-ink-700 border border-accent-500/30 rounded px-3 py-2 text-white focus:outline-none focus:border-accent-500"
            >
              {allGenres.map((genre) => (
                <option key={genre} value={genre}>
                  {genre}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Recommendations Grid */}
        {recommendations.length > 0 ? (
          <div className="space-y-1">
            {recommendations.map((track, idx) => (
              <div
                key={track.id}
                className="bg-ink-700 rounded px-3 py-2 flex items-center justify-between text-xs hover:bg-ink-600 transition"
              >
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-white truncate">
                    {idx + 1}. {track.title}
                  </div>
                  <div className="text-neutral-400 truncate">
                    {track.artist} • {track.year} • {track.bpm} BPM
                    {track.key && ` • ${track.key}`}
                  </div>
                  <div className="flex gap-1 mt-1 flex-wrap">
                    {track.genres.slice(0, 3).map((g) => (
                      <span
                        key={g}
                        className="px-2 py-0.5 bg-accent-500/20 text-accent-300 rounded text-xs"
                      >
                        {g}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center text-neutral-400 py-8">
            No recommendations available for these criteria
          </p>
        )}
      </div>
    </div>
  );
}

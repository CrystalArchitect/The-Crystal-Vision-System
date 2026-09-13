// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track } from "../../types";

interface Rating {
  trackId: string;
  rating: number;
  review: string;
}

interface CommunityRatingsProps {
  tracks: Track[];
}

export default function CommunityRatings({ tracks }: CommunityRatingsProps) {
  const [ratings, setRatings] = useState<Map<string, Rating>>(new Map());
  const [selectedTrackId, setSelectedTrackId] = useState<string | null>(null);
  const [filterRating, setFilterRating] = useState<number>(0);

  const selectedTrack = selectedTrackId ? tracks.find(t => t.id === selectedTrackId) : null;
  const selectedRating = selectedTrackId ? ratings.get(selectedTrackId) : null;

  const updateRating = (trackId: string, rating: number, review: string) => {
    const newRatings = new Map(ratings);
    newRatings.set(trackId, { trackId, rating, review });
    setRatings(newRatings);
  };

  const ratedTracks = useMemo(() => {
    const ratedList = Array.from(ratings.entries())
      .map(([trackId, rating]) => ({
        track: tracks.find(t => t.id === trackId),
        rating: rating.rating,
        review: rating.review,
      }))
      .filter((item): item is { track: Track; rating: number; review: string } => !!item.track);

    if (filterRating > 0) {
      return ratedList.filter(item => item.rating === filterRating);
    }

    return ratedList.sort((a, b) => b.rating - a.rating);
  }, [ratings, tracks, filterRating]);

  const averageRating = useMemo(() => {
    if (ratings.size === 0) return 0;
    const sum = Array.from(ratings.values()).reduce((acc, r) => acc + r.rating, 0);
    return (sum / ratings.size).toFixed(1);
  }, [ratings]);

  const ratingDistribution = useMemo(() => {
    const dist = new Map<number, number>();
    for (let i = 1; i <= 5; i++) {
      dist.set(i, 0);
    }

    Array.from(ratings.values()).forEach(rating => {
      dist.set(rating.rating, (dist.get(rating.rating) || 0) + 1);
    });

    return dist;
  }, [ratings]);

  return (
    <div className="space-y-6">
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h3 className="text-xl font-bold text-white mb-4">Community Ratings</h3>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Rating Input */}
          <div className="lg:col-span-1">
            <div className="bg-ink-700 rounded p-4 mb-4">
              <h4 className="font-semibold text-white mb-3">Rate a Track</h4>

              <input
                type="text"
                placeholder="Search track..."
                className="w-full bg-ink-600 border border-accent-500/30 rounded px-2 py-1 text-sm text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500 mb-3"
              />

              <div className="space-y-1 max-h-32 overflow-y-auto mb-3">
                {tracks.slice(0, 30).map(track => (
                  <button
                    key={track.id}
                    onClick={() => setSelectedTrackId(track.id)}
                    className={`w-full text-left px-2 py-1 rounded text-xs transition ${
                      selectedTrackId === track.id
                        ? "bg-accent-500 text-ink-900"
                        : "bg-ink-600 hover:bg-ink-500"
                    }`}
                  >
                    <div className="font-medium truncate">{track.title}</div>
                    <div className="opacity-75 truncate">{track.artist}</div>
                  </button>
                ))}
              </div>
            </div>

            {selectedTrack && (
              <div className="bg-ink-700 rounded p-4">
                <h5 className="font-semibold text-white mb-3">{selectedTrack.title}</h5>

                <div className="mb-4">
                  <label className="block text-sm text-neutral-300 mb-2">Rating</label>
                  <div className="flex gap-2">
                    {[1, 2, 3, 4, 5].map(star => (
                      <button
                        key={star}
                        onClick={() => {
                          const review = selectedRating?.review || "";
                          updateRating(selectedTrack.id, star, review);
                        }}
                        className={`px-3 py-1 rounded text-lg transition ${
                          (selectedRating?.rating || 0) >= star
                            ? "bg-accent-500 text-ink-900"
                            : "bg-ink-600 text-neutral-400 hover:bg-ink-500"
                        }`}
                      >
                        ★
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm text-neutral-300 mb-2">Review</label>
                  <textarea
                    value={selectedRating?.review || ""}
                    onChange={(e) => {
                      const rating = selectedRating?.rating || 0;
                      updateRating(selectedTrack.id, rating, e.target.value);
                    }}
                    className="w-full bg-ink-600 border border-accent-500/30 rounded px-2 py-1 text-xs text-white placeholder-neutral-500 focus:outline-none focus:border-accent-500"
                    rows={3}
                    placeholder="Share your thoughts..."
                  />
                </div>
              </div>
            )}
          </div>

          {/* Stats & Ratings */}
          <div className="lg:col-span-2">
            <div className="bg-ink-700 rounded p-4 mb-4">
              <h4 className="font-semibold text-white mb-4">Your Ratings Summary</h4>

              <div className="grid grid-cols-3 gap-3 mb-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent-400">{ratings.size}</div>
                  <div className="text-xs text-neutral-400">Tracks Rated</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent-400">{averageRating}</div>
                  <div className="text-xs text-neutral-400">Average Rating</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-accent-400">
                    {Array.from(ratingDistribution.values()).reduce((a, b) => a + b, 0) > 0
                      ? Math.round(
                          (Array.from(ratingDistribution.get(5) || 0) / ratings.size) * 100
                        )
                      : 0}%
                  </div>
                  <div className="text-xs text-neutral-400">5-Star Tracks</div>
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm text-neutral-300">Rating Distribution</label>
                {[5, 4, 3, 2, 1].map(star => {
                  const count = ratingDistribution.get(star) || 0;
                  const percentage =
                    ratings.size > 0 ? (count / ratings.size) * 100 : 0;
                  return (
                    <div key={star} className="flex items-center gap-2">
                      <span className="text-xs w-12 text-neutral-400">
                        {star}★ ({count})
                      </span>
                      <div className="flex-1 h-2 bg-ink-600 rounded overflow-hidden">
                        <div
                          className="bg-accent-500 h-full"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="bg-ink-700 rounded p-4">
              <div className="flex justify-between items-center mb-3">
                <h4 className="font-semibold text-white">Your Rated Tracks</h4>
                {ratings.size > 0 && (
                  <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map(star => (
                      <button
                        key={star}
                        onClick={() =>
                          setFilterRating(filterRating === star ? 0 : star)
                        }
                        className={`px-2 py-1 rounded text-xs transition ${
                          filterRating === star
                            ? "bg-accent-500 text-ink-900"
                            : "bg-ink-600 text-neutral-300 hover:bg-ink-500"
                        }`}
                      >
                        {star}★
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {ratedTracks.length === 0 ? (
                <p className="text-xs text-neutral-400">
                  {ratings.size === 0
                    ? "Rate tracks to see them here"
                    : "No tracks with this rating"}
                </p>
              ) : (
                <div className="space-y-2 max-h-48 overflow-y-auto">
                  {ratedTracks.map(({ track, rating, review }) => (
                    <div key={track.id} className="bg-ink-600 rounded p-2 text-xs">
                      <div className="flex justify-between items-start mb-1">
                        <div className="font-medium text-white truncate">
                          {track.title}
                        </div>
                        <div className="text-accent-400 ml-2">
                          {"★".repeat(rating)}
                        </div>
                      </div>
                      <div className="text-neutral-400 truncate">
                        {track.artist}
                      </div>
                      {review && (
                        <div className="text-neutral-400 mt-1 italic">
                          "{review}"
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// SPDX-License-Identifier: MIT

import { useState, useMemo } from "react";
import type { Track } from "../../types";

interface Props {
  tracks: Track[];
  realms: any[];
}

const MOODS = [
  { name: "Energetic", emoji: "⚡", description: "Fast, intense, high energy", bpmMin: 170 },
  { name: "Focused", emoji: "🎯", description: "Steady, driving, productive", bpmMin: 140, bpmMax: 160 },
  { name: "Smooth", emoji: "🌊", description: "Liquid, atmospheric, chill", bpmMin: 100, bpmMax: 130 },
  { name: "Dark", emoji: "🌙", description: "Neurofunk, heavy, intense", keywords: ["neurofunk", "dark"] },
  { name: "Groovy", emoji: "🎶", description: "Funky, rhythmic, soulful", keywords: ["funk", "groovy"] },
  { name: "Experimental", emoji: "🔬", description: "Avant-garde, complex, innovative", keywords: ["experimental", "abstract"] },
];

export default function MoodDiscovery({ tracks, realms }: Props) {
  const [selectedMood, setSelectedMood] = useState<string | null>(null);
  const [limit, setLimit] = useState(20);

  const moodPlaylists = useMemo(() => {
    const result: Record<string, Track[]> = {};

    MOODS.forEach((mood) => {
      let filtered = tracks;

      if (mood.bpmMin !== undefined) {
        filtered = filtered.filter((t) => t.bpm >= mood.bpmMin!);
      }
      if (mood.bpmMax !== undefined) {
        filtered = filtered.filter((t) => t.bpm <= mood.bpmMax!);
      }
      if (mood.keywords) {
        filtered = filtered.filter((t) =>
          mood.keywords!.some(
            (kw) =>
              t.title.toLowerCase().includes(kw) ||
              t.artist.toLowerCase().includes(kw) ||
              t.category.toLowerCase().includes(kw) ||
              t.genres.some((g) => g.toLowerCase().includes(kw))
          )
        );
      }

      result[mood.name] = filtered.sort(() => Math.random() - 0.5).slice(0, limit);
    });

    return result;
  }, [tracks, limit]);

  const selectedMoodData = selectedMood
    ? MOODS.find((m) => m.name === selectedMood)
    : null;
  const selectedTracks = selectedMood ? moodPlaylists[selectedMood] : [];

  return (
    <div className="space-y-6">
      <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
        <h2 className="text-2xl font-bold text-white mb-6">Mood-Based Discovery</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {MOODS.map((mood) => {
            const trackCount = moodPlaylists[mood.name]?.length || 0;
            return (
              <button
                key={mood.name}
                onClick={() =>
                  setSelectedMood(
                    selectedMood === mood.name ? null : mood.name
                  )
                }
                className={`rounded-lg p-4 text-left transition ${
                  selectedMood === mood.name
                    ? "bg-accent-500 text-ink-900"
                    : "bg-ink-700 text-white hover:bg-ink-600 border border-accent-500/20"
                }`}
              >
                <div className="text-2xl mb-2">{mood.emoji}</div>
                <div className="font-semibold">{mood.name}</div>
                <div className="text-xs opacity-75">{mood.description}</div>
                <div className="text-xs opacity-60 mt-2">{trackCount} tracks</div>
              </button>
            );
          })}
        </div>

        {selectedMoodData && (
          <div className="bg-ink-700 rounded p-4 mb-6 border border-accent-500/10">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                  <span>{selectedMoodData.emoji}</span>
                  {selectedMoodData.name} Playlist
                </h3>
                <p className="text-sm text-neutral-400">
                  {selectedMoodData.description}
                </p>
              </div>
              <div className="text-xs text-neutral-500">
                {selectedTracks.length} tracks
              </div>
            </div>

            <div className="flex gap-2 mb-4">
              <button
                onClick={() => setLimit(20)}
                className={`px-3 py-1 rounded text-xs ${
                  limit === 20
                    ? "bg-accent-500 text-ink-900"
                    : "bg-ink-600 text-neutral-300 hover:bg-ink-500"
                }`}
              >
                20 Tracks
              </button>
              <button
                onClick={() => setLimit(50)}
                className={`px-3 py-1 rounded text-xs ${
                  limit === 50
                    ? "bg-accent-500 text-ink-900"
                    : "bg-ink-600 text-neutral-300 hover:bg-ink-500"
                }`}
              >
                50 Tracks
              </button>
              <button
                onClick={() => setLimit(100)}
                className={`px-3 py-1 rounded text-xs ${
                  limit === 100
                    ? "bg-accent-500 text-ink-900"
                    : "bg-ink-600 text-neutral-300 hover:bg-ink-500"
                }`}
              >
                100 Tracks
              </button>
            </div>
          </div>
        )}
      </div>

      {selectedMoodData && selectedTracks.length > 0 && (
        <div className="rounded-lg bg-ink-800 p-6 border border-accent-500/20">
          <h3 className="text-lg font-bold text-white mb-4">
            {selectedMoodData.emoji} {selectedMoodData.name} Tracks
          </h3>

          <div className="max-h-96 overflow-y-auto space-y-1">
            {selectedTracks.map((track, idx) => (
              <div
                key={track.id}
                className="bg-ink-700 rounded px-3 py-2 flex items-center justify-between text-xs hover:bg-ink-600 transition"
              >
                <div>
                  <div className="font-medium text-white truncate">
                    {idx + 1}. {track.title}
                  </div>
                  <div className="text-neutral-400">
                    {track.artist} • {track.year} • {track.bpm} BPM
                    {track.key && ` • ${track.key}`}
                  </div>
                  <div className="flex gap-1 mt-1">
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
        </div>
      )}
    </div>
  );
}

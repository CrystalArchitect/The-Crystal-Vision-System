// SPDX-License-Identifier: MIT

import { useMemo } from "react";
import type { Track, SmartPlaylist, PlaylistRule } from "../../types";
import { getUserMeta } from "../../lib/storage";

interface Props {
  smartPlaylistId: string;
  allTracks: Track[];
}

export default function SmartPlaylistView({ smartPlaylistId, allTracks }: Props) {
  const meta = getUserMeta();
  const smartPlaylist = meta.smartPlaylists?.find((p) => p.id === smartPlaylistId);

  const matchedTracks = useMemo(() => {
    if (!smartPlaylist) return [];

    return allTracks.filter((track) => {
      return evaluateRules(track, smartPlaylist.rules, meta, allTracks);
    });
  }, [smartPlaylist, allTracks, meta]);

  if (!smartPlaylist) {
    return <div className="text-center py-12 text-neutral-500">Smart playlist not found</div>;
  }

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">{smartPlaylist.name}</h1>
        {smartPlaylist.description && (
          <p className="text-neutral-400">{smartPlaylist.description}</p>
        )}
        <p className="text-xs text-neutral-600 mt-2">
          {matchedTracks.length} track{matchedTracks.length !== 1 ? "s" : ""} matching rules
        </p>
      </div>

      {matchedTracks.length === 0 ? (
        <div className="text-center py-12 text-neutral-500">
          <p>No tracks match the playlist rules</p>
        </div>
      ) : (
        <div className="space-y-2">
          {matchedTracks.map((track) => (
            <a
              key={track.id}
              href={track.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 rounded border border-ink-800 bg-ink-900 block hover:border-accent hover:bg-ink-800 transition-colors group"
            >
              <div className="text-white font-medium group-hover:text-accent truncate">
                {track.title}
              </div>
              <div className="text-xs text-neutral-500">{track.artist}</div>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

function evaluateRules(
  track: Track,
  rules: PlaylistRule[],
  meta: any,
  allTracks: Track[]
): boolean {
  if (rules.length === 0) return true;

  const results = rules.map((rule) => evaluateRule(track, rule, meta));

  if (rules.length === 1) return results[0];

  const firstRule = rules[0];
  let result = results[0];

  for (let i = 1; i < rules.length; i++) {
    const logic = rules[i - 1].logic || "and";
    if (logic === "and") {
      result = result && results[i];
    } else {
      result = result || results[i];
    }
  }

  return result;
}

function evaluateRule(track: Track, rule: PlaylistRule, meta: any): boolean {
  const value = (track as any)[rule.field];

  switch (rule.operator) {
    case "equals":
      return value === rule.value;
    case "contains":
      if (Array.isArray(value)) {
        return value.includes(rule.value);
      }
      return String(value).toLowerCase().includes(String(rule.value).toLowerCase());
    case "gt":
      return Number(value) > Number(rule.value);
    case "gte":
      return Number(value) >= Number(rule.value);
    case "lt":
      return Number(value) < Number(rule.value);
    case "lte":
      return Number(value) <= Number(rule.value);
    case "regex":
      try {
        const regex = new RegExp(rule.value);
        return regex.test(String(value));
      } catch {
        return false;
      }
    case "in": {
      const values = Array.isArray(rule.value) ? rule.value : String(rule.value).split(",");
      return values.includes(value);
    }
    default:
      return false;
  }
}

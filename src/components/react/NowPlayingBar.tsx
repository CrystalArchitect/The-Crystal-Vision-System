// SPDX-License-Identifier: MIT

import { useEffect, useState } from "react";
import type { Track } from "../../types";
import { getUserMeta } from "../../lib/storage";

interface Props {
  tracks: Track[];
}

export default function NowPlayingBar({ tracks }: Props) {
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null);

  useEffect(() => {
    const meta = getUserMeta();
    if (meta.lastPlayed?.trackId) {
      const track = tracks.find((t) => t.id === meta.lastPlayed.trackId);
      setCurrentTrack(track || null);
    }
  }, [tracks]);

  if (!currentTrack) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-ink-900 border-t border-ink-800 px-6 py-3 max-h-16 overflow-hidden">
      <div className="flex items-center justify-between gap-4">
        <div className="min-w-0 text-sm">
          <div className="text-neutral-500 text-xs">Now playing</div>
          <div className="text-white font-medium truncate">{currentTrack.title}</div>
          <div className="text-neutral-500 text-xs truncate">{currentTrack.artist}</div>
        </div>
        <a
          href={currentTrack.sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="px-3 py-1.5 rounded bg-accent-400 text-ink-950 text-xs font-medium hover:bg-accent-300 transition-colors flex-shrink-0"
        >
          Play
        </a>
      </div>
    </div>
  );
}

// SPDX-License-Identifier: MIT

import { useEffect, useRef, useState } from "react";
import type { Track } from "../../types";
import { getUserMeta, setTrackRating, addTrackTags, removeTrackTags, setTrackNote, deletePlaylist, addTrackToPlaylist, getFavorites, addToFavorites, removeFromFavorites } from "../../lib/storage";
import RatingStars from "./RatingStars";
import FavoritesButton from "./FavoritesButton";

interface Props {
  track: Track;
  onClose: () => void;
  onMetaChange: () => void;
}

export default function TrackDetailDrawer({ track, onClose, onMetaChange }: Props) {
  const overlayRef = useRef<HTMLDivElement>(null);
  const drawerRef = useRef<HTMLDivElement>(null);
  const meta = getUserMeta();
  const trackMeta = meta.tags?.[track.id] || {};
  const trackRating = meta.ratings?.[track.id] ?? 0;
  const trackNote = meta.notes?.[track.id] ?? "";
  const trackTags = meta.tags?.[track.id] ?? [];
  const playlists = meta.playlists ?? [];
  const [isFavorited, setIsFavorited] = useState(() => getFavorites().includes(track.id));

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
      }
    };

    const handleClick = (e: MouseEvent) => {
      if (overlayRef.current && e.target === overlayRef.current) {
        onClose();
      }
    };

    window.addEventListener("keydown", handleEscape);
    overlayRef.current?.addEventListener("click", handleClick);

    return () => {
      window.removeEventListener("keydown", handleEscape);
      overlayRef.current?.removeEventListener("click", handleClick);
    };
  }, [onClose]);

  const handleAddToPlaylist = (playlistId: string) => {
    addTrackToPlaylist(playlistId, track.id);
    onMetaChange();
  };

  const handleToggleFavorite = (trackId: string, favorited: boolean) => {
    if (favorited) {
      addToFavorites(trackId);
    } else {
      removeFromFavorites(trackId);
    }
    setIsFavorited(favorited);
    onMetaChange();
  };

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 z-50 overflow-y-auto bg-black/50 backdrop-blur-sm"
    >
      <div
        ref={drawerRef}
        className="fixed right-0 top-0 bottom-0 w-full max-w-md bg-ink-950 border-l border-ink-800 shadow-2xl overflow-y-auto"
      >
        <div className="sticky top-0 bg-ink-950 border-b border-ink-800 px-6 py-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white truncate">{track.title}</h2>
          <div className="flex items-center gap-2">
            <FavoritesButton
              trackId={track.id}
              isFavorited={isFavorited}
              onToggle={handleToggleFavorite}
              size={20}
            />
            <button
              onClick={onClose}
              className="p-2 hover:bg-ink-800 rounded transition-colors text-neutral-400 hover:text-white"
              aria-label="Close"
            >
              ✕
            </button>
          </div>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <div className="text-sm text-neutral-500 mb-2">Artist</div>
            <div className="text-white font-medium">{track.artist}</div>
          </div>

          {track.remixer && (
            <div>
              <div className="text-sm text-neutral-500 mb-2">Remixer</div>
              <div className="text-white font-medium">{track.remixer}</div>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-sm text-neutral-500 mb-2">Year</div>
              <div className="text-white font-medium">{track.year}</div>
            </div>
            <div>
              <div className="text-sm text-neutral-500 mb-2">BPM</div>
              <div className="text-white font-medium">{track.bpm}</div>
            </div>
            <div>
              <div className="text-sm text-neutral-500 mb-2">Duration</div>
              <div className="text-white font-medium">
                {Math.floor(track.duration / 60)}:{String(track.duration % 60).padStart(2, "0")}
              </div>
            </div>
            <div>
              <div className="text-sm text-neutral-500 mb-2">Key</div>
              <div className="text-white font-medium">{track.key}</div>
            </div>
          </div>

          {track.category && (
            <div>
              <div className="text-sm text-neutral-500 mb-2">Category</div>
              <div className="text-white font-medium">{track.category}</div>
            </div>
          )}

          {track.genres && track.genres.length > 0 && (
            <div>
              <div className="text-sm text-neutral-500 mb-2">Genres</div>
              <div className="flex flex-wrap gap-2">
                {track.genres.map((g) => (
                  <span key={g} className="px-2 py-1 bg-ink-800 text-xs rounded text-neutral-300">
                    {g}
                  </span>
                ))}
              </div>
            </div>
          )}

          <div>
            <div className="text-sm text-neutral-500 mb-2">Rating</div>
            <RatingStars
              value={trackRating}
              onChange={(v) => {
                setTrackRating(track.id, v);
                onMetaChange();
              }}
              size="md"
            />
          </div>

          <div>
            <div className="text-sm text-neutral-500 mb-3">Add to Playlist</div>
            <div className="space-y-2 max-h-32 overflow-y-auto">
              {playlists.length === 0 ? (
                <p className="text-xs text-neutral-600">No playlists yet. Create one first.</p>
              ) : (
                playlists.map((pl) => (
                  <button
                    key={pl.id}
                    onClick={() => handleAddToPlaylist(pl.id)}
                    className="w-full text-left px-3 py-2 rounded bg-ink-800 hover:bg-ink-700 text-sm text-neutral-300 hover:text-white transition-colors"
                  >
                    {pl.name}
                  </button>
                ))
              )}
            </div>
          </div>

          <div>
            <a
              href={track.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="inline-block px-4 py-2 rounded bg-accent-400 text-ink-950 font-medium hover:bg-accent-300 transition-colors"
            >
              Open on Source
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

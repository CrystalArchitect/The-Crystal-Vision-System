// SPDX-License-Identifier: MIT

import { useEffect, useRef } from "react";
import type { Track } from "../../types";
import { setTrackRating } from "../../lib/storage";
import RatingStars from "./RatingStars";

interface UserMeta {
  rating?: number;
  tags?: string[];
  playCount?: number;
}

interface Props {
  tracks: Track[];
  meta: Record<string, UserMeta>;
  focusIndex: number;
  setFocusIndex: (i: number) => void;
  onOpenDetail: (t: Track) => void;
  onMetaChange: () => void;
}

export default function TrackTable({
  tracks,
  meta,
  focusIndex,
  setFocusIndex,
  onOpenDetail,
  onMetaChange,
}: Props) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLElement && ["INPUT", "TEXTAREA", "SELECT"].includes(e.target.tagName)) return;
      if (e.key === "j") {
        e.preventDefault();
        setFocusIndex(Math.min(focusIndex + 1, tracks.length - 1));
      } else if (e.key === "k") {
        e.preventDefault();
        setFocusIndex(Math.max(focusIndex - 1, 0));
      } else if (e.key === "Enter" && focusIndex >= 0) {
        const t = tracks[focusIndex];
        if (t) {
          window.open(t.sourceUrl, "_blank", "noopener");
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [focusIndex, tracks]);

  useEffect(() => {
    if (focusIndex < 0 || !ref.current) return;
    const row = ref.current.querySelector<HTMLElement>(`[data-index="${focusIndex}"]`);
    row?.scrollIntoView({ block: "nearest" });
  }, [focusIndex]);

  if (tracks.length === 0) {
    return (
      <div className="mt-8 rounded border border-ink-800 bg-ink-900 p-8 text-center text-neutral-500">
        No tracks match those filters.
      </div>
    );
  }

  return (
    <div ref={ref} className="mt-6 overflow-x-auto">
      <table className="w-full text-sm">
        <thead className="border-b border-ink-800 text-left text-xs uppercase tracking-wider text-neutral-500">
          <tr>
            <th className="py-2 pr-3">Artist</th>
            <th className="py-2 pr-3">Track</th>
            <th className="py-2 pr-3">Year</th>
            <th className="py-2 pr-3">BPM</th>
            <th className="py-2 pr-3">Rating</th>
            <th className="py-2 pr-3"></th>
          </tr>
        </thead>
        <tbody>
          {tracks.map((t, i) => {
            const m = meta[t.id];
            return (
              <tr
                key={t.id}
                data-index={i}
                onClick={() => setFocusIndex(i)}
                onDoubleClick={() => onOpenDetail(t)}
                className={
                  "cursor-pointer border-b border-ink-800/60 hover:bg-ink-900 " +
                  (focusIndex === i ? "bg-ink-900" : "")
                }
              >
                <td className="max-w-[16rem] truncate py-2 pr-3">{t.artist}</td>
                <td className="max-w-[24rem] py-2 pr-3">
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); onOpenDetail(t); }}
                    className="block max-w-full truncate text-left hover:text-accent"
                  >
                    {t.title}
                  </button>
                </td>
                <td className="py-2 pr-3 text-xs text-neutral-500">{t.year}</td>
                <td className="py-2 pr-3 text-xs text-neutral-500">{t.bpm}</td>
                <td className="py-2 pr-3">
                  <RatingStars
                    value={m?.rating ?? 0}
                    onChange={(v) => {
                      setTrackRating(t.id, v);
                      onMetaChange();
                    }}
                  />
                </td>
                <td className="py-2 pr-3 text-right">
                  <a
                    href={t.sourceUrl}
                    target="_blank"
                    rel="noopener"
                    onClick={(e) => e.stopPropagation()}
                    className="rounded border border-ink-700 px-2 py-0.5 text-xs text-neutral-400 hover:border-accent hover:text-accent"
                  >
                    Open
                  </a>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

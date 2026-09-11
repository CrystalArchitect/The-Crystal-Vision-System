// SPDX-License-Identifier: MIT

import { useEffect, useState } from "react";
import type { FilterState, SortState } from "../../lib/search";

interface Props {
  filters: FilterState;
  setFilters: (f: FilterState) => void;
  sort: SortState;
  setSort: (s: SortState) => void;
  yearOptions: number[];
  resultCount: number;
  totalCount: number;
}

export default function FilterBar({
  filters,
  setFilters,
  sort,
  setSort,
  yearOptions,
  resultCount,
  totalCount,
}: Props) {
  const [qLocal, setQLocal] = useState(filters.q);

  useEffect(() => {
    const t = setTimeout(() => {
      if (qLocal !== filters.q) setFilters({ ...filters, q: qLocal });
    }, 200);
    return () => clearTimeout(t);
  }, [qLocal, filters, setFilters]);

  function update<K extends keyof FilterState>(key: K, value: FilterState[K]) {
    setFilters({ ...filters, [key]: value });
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <input
          id="track-search"
          type="search"
          value={qLocal}
          onChange={(e) => setQLocal(e.target.value)}
          placeholder="Search artist, track…"
          className="min-w-0 flex-1 rounded border border-ink-700 bg-ink-900 px-3 py-2 text-sm outline-none focus:border-accent"
        />
        <div className="text-xs text-neutral-500">
          {resultCount.toLocaleString()} / {totalCount.toLocaleString()}
        </div>
      </div>

      <div className="flex flex-wrap gap-2 text-sm">
        <select
          value={filters.year ?? ""}
          onChange={(e) => update("year", e.target.value ? parseInt(e.target.value, 10) : null)}
          className="rounded border border-ink-700 bg-ink-900 px-2 py-1.5 text-sm"
        >
          <option value="">Any year</option>
          {yearOptions.map((y) => (
            <option key={y} value={y}>{y}</option>
          ))}
        </select>

        <select
          value={filters.minRating}
          onChange={(e) => update("minRating", parseInt(e.target.value, 10))}
          className="rounded border border-ink-700 bg-ink-900 px-2 py-1.5 text-sm"
        >
          <option value={0}>Any rating</option>
          {[1, 2, 3, 4, 5].map((r) => (
            <option key={r} value={r}>{"★".repeat(r)}+</option>
          ))}
        </select>

        <button
          type="button"
          onClick={() => setFilters({ q: "", year: null, category: null, artist: null, remixer: null, tag: null, minRating: 0, hasRemix: null, isVIP: null, duplicatesOnly: false })}
          className="rounded border border-ink-700 px-2 py-1.5 text-xs text-neutral-400 hover:text-white"
        >
          Reset
        </button>

        <div className="ml-auto flex gap-2">
          <select
            value={`${sort.key}:${sort.dir}`}
            onChange={(e) => {
              const [key, dir] = e.target.value.split(":") as [SortState["key"], SortState["dir"]];
              setSort({ key, dir });
            }}
            className="rounded border border-ink-700 bg-ink-900 px-2 py-1.5 text-sm"
          >
            <option value="artist:asc">Artist A–Z</option>
            <option value="artist:desc">Artist Z–A</option>
            <option value="title:asc">Title A–Z</option>
            <option value="year:asc">Year ↑</option>
            <option value="year:desc">Year ↓</option>
            <option value="rating:desc">Rating ↓</option>
            <option value="playCount:desc">Plays ↓</option>
          </select>
        </div>
      </div>
    </div>
  );
}

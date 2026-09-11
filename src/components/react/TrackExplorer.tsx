// SPDX-License-Identifier: MIT

import { useEffect, useState } from "react";
import type { Track } from "../../types";
import { getUserMeta } from "../../lib/storage";
import { applyFilters, applySort, filtersToQuery, queryToFilters, type FilterState, type SortState } from "../../lib/search";
import FilterBar from "./FilterBar";
import TrackTable from "./TrackTable";
import TrackDetailDrawer from "./TrackDetailDrawer";

interface Props {
  tracks: Track[];
  yearOptions: number[];
  initialQuery?: string;
}

export default function TrackExplorer({ tracks, yearOptions, initialQuery = "" }: Props) {
  const [filters, setFilters] = useState<FilterState>(() => {
    if (initialQuery) {
      return queryToFilters(new URLSearchParams(initialQuery));
    }
    return {
      q: "",
      year: null,
      category: null,
      artist: null,
      remixer: null,
      tag: null,
      minRating: 0,
      hasRemix: null,
      isVIP: null,
      duplicatesOnly: false,
    };
  });

  const [sort, setSort] = useState<SortState>({ key: "artist", dir: "asc" });
  const [focusIndex, setFocusIndex] = useState(0);
  const [selectedTrack, setSelectedTrack] = useState<Track | null>(null);
  const [meta, setMeta] = useState(getUserMeta());

  useEffect(() => {
    const query = filtersToQuery(filters);
    const newUrl = `${window.location.pathname}?${query}`;
    window.history.replaceState({}, "", newUrl);
  }, [filters]);

  const filteredTracks = applyFilters(tracks, filters, (id) => meta.tags?.[id]);
  const sortedTracks = applySort(filteredTracks, sort, (id) => meta.ratings?.[id]);

  const handleMetaChange = () => {
    setMeta(getUserMeta());
  };

  return (
    <div className="space-y-6">
      <FilterBar
        filters={filters}
        setFilters={setFilters}
        sort={sort}
        setSort={setSort}
        yearOptions={yearOptions}
        resultCount={sortedTracks.length}
        totalCount={tracks.length}
      />

      <TrackTable
        tracks={sortedTracks}
        meta={meta}
        focusIndex={focusIndex}
        setFocusIndex={setFocusIndex}
        onOpenDetail={setSelectedTrack}
        onMetaChange={handleMetaChange}
      />

      {selectedTrack && (
        <TrackDetailDrawer
          track={selectedTrack}
          onClose={() => setSelectedTrack(null)}
          onMetaChange={handleMetaChange}
        />
      )}
    </div>
  );
}

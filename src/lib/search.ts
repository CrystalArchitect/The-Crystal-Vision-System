// SPDX-License-Identifier: MIT

import Fuse from "fuse.js";
import type { Track } from "../types";

export interface FilterState {
  q: string;
  year: number | null;
  category: "year" | "heavy" | "remixes" | "other" | null;
  artist: string | null;
  remixer: string | null;
  tag: string | null;
  minRating: number;
  hasRemix: boolean | null;
  isVIP: boolean | null;
  duplicatesOnly: boolean;
  realm: string | null;
  bpmMin: number | null;
  bpmMax: number | null;
  key: string | null;
  genres: string[];
}

export const EMPTY_FILTERS: FilterState = {
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
  realm: null,
  bpmMin: null,
  bpmMax: null,
  key: null,
  genres: [],
};

export type SortKey = "title" | "artist" | "year" | "mb" | "playCount" | "rating";

export interface SortState {
  key: SortKey;
  dir: "asc" | "desc";
}

let fuse: Fuse<Track> | null = null;

export function getFuse(tracks: Track[]): Fuse<Track> {
  if (!fuse) {
    fuse = new Fuse(tracks, {
      includeScore: true,
      threshold: 0.35,
      ignoreLocation: true,
      minMatchCharLength: 2,
      keys: [
        { name: "artist", weight: 0.35 },
        { name: "title", weight: 0.35 },
        { name: "remixer", weight: 0.1 },
        { name: "label", weight: 0.05 },
      ],
    });
  }
  return fuse;
}

export interface UserMetaLookup {
  (trackId: string): { rating: number; tags: string[]; playCount: number } | undefined;
}

export function applyFilters(
  tracks: Track[],
  filters: FilterState,
  metaLookup: UserMetaLookup
): Track[] {
  let list = tracks;

  if (filters.q.trim()) {
    const q = filters.q.trim();
    const f = getFuse(tracks);
    list = f.search(q).map((r) => r.item);
  }

  return list.filter((t) => {
    if (filters.year !== null && t.year !== filters.year) return false;
    if (filters.category !== null && t.category !== filters.category) return false;
    if (filters.artist !== null && t.artist !== filters.artist) return false;
    if (filters.remixer !== null && t.remixer !== filters.remixer) return false;
    if (filters.realm !== null && t.realm !== filters.realm) return false;
    if (filters.hasRemix !== null && t.isRemix !== filters.hasRemix) return false;
    if (filters.minRating > 0) {
      const meta = metaLookup(t.id);
      if ((meta?.rating ?? 0) < filters.minRating) return false;
    }
    if (filters.tag !== null) {
      const meta = metaLookup(t.id);
      if (!(meta?.tags ?? []).includes(filters.tag)) return false;
    }
    if (filters.bpmMin !== null && t.bpm < filters.bpmMin) return false;
    if (filters.bpmMax !== null && t.bpm > filters.bpmMax) return false;
    if (filters.key !== null && t.key !== filters.key) return false;
    if (filters.genres.length > 0) {
      if (!filters.genres.some((g) => t.genres.includes(g))) return false;
    }
    return true;
  });
}

export function applySort(
  tracks: Track[],
  sort: SortState,
  metaLookup: UserMetaLookup
): Track[] {
  const dir = sort.dir === "asc" ? 1 : -1;
  const list = [...tracks];

  list.sort((a, b) => {
    let cmp = 0;
    switch (sort.key) {
      case "title":
        cmp = a.title.localeCompare(b.title);
        break;
      case "artist":
        cmp = a.artist.localeCompare(b.artist) || a.title.localeCompare(b.title);
        break;
      case "year":
        cmp = (a.year ?? 9999) - (b.year ?? 9999);
        break;
      case "mb":
        cmp = 0;
        break;
      case "rating": {
        const ra = metaLookup(a.id)?.rating ?? 0;
        const rb = metaLookup(b.id)?.rating ?? 0;
        cmp = ra - rb;
        break;
      }
      case "playCount": {
        const pa = metaLookup(a.id)?.playCount ?? 0;
        const pb = metaLookup(b.id)?.playCount ?? 0;
        cmp = pa - pb;
        break;
      }
    }
    if (cmp === 0) cmp = a.id.localeCompare(b.id);
    return cmp * dir;
  });

  return list;
}

export function filtersToQuery(f: FilterState): string {
  const p = new URLSearchParams();
  if (f.q) p.set("q", f.q);
  if (f.year !== null) p.set("year", String(f.year));
  if (f.category) p.set("cat", f.category);
  if (f.artist) p.set("artist", f.artist);
  if (f.remixer) p.set("remixer", f.remixer);
  if (f.realm) p.set("realm", f.realm);
  if (f.tag) p.set("tag", f.tag);
  if (f.minRating) p.set("rating", String(f.minRating));
  if (f.hasRemix !== null) p.set("remix", f.hasRemix ? "1" : "0");
  if (f.duplicatesOnly) p.set("dupes", "1");
  if (f.bpmMin !== null) p.set("bpmMin", String(f.bpmMin));
  if (f.bpmMax !== null) p.set("bpmMax", String(f.bpmMax));
  if (f.key) p.set("key", f.key);
  if (f.genres.length > 0) p.set("genres", f.genres.join(","));
  return p.toString();
}

export function queryToFilters(params: URLSearchParams): FilterState {
  const f: FilterState = { ...EMPTY_FILTERS };
  const q = params.get("q");
  if (q) f.q = q;
  const year = params.get("year");
  if (year) f.year = parseInt(year, 10);
  const cat = params.get("cat");
  if (cat === "year" || cat === "heavy" || cat === "remixes" || cat === "other") f.category = cat;
  const artist = params.get("artist");
  if (artist) f.artist = artist;
  const remixer = params.get("remixer");
  if (remixer) f.remixer = remixer;
  const realm = params.get("realm");
  if (realm) f.realm = realm;
  const tag = params.get("tag");
  if (tag) f.tag = tag;
  const rating = params.get("rating");
  if (rating) f.minRating = parseInt(rating, 10);
  const remix = params.get("remix");
  if (remix === "1") f.hasRemix = true;
  if (remix === "0") f.hasRemix = false;
  if (params.get("dupes") === "1") f.duplicatesOnly = true;
  const bpmMin = params.get("bpmMin");
  if (bpmMin) f.bpmMin = parseInt(bpmMin, 10);
  const bpmMax = params.get("bpmMax");
  if (bpmMax) f.bpmMax = parseInt(bpmMax, 10);
  const key = params.get("key");
  if (key) f.key = key;
  const genres = params.get("genres");
  if (genres) f.genres = genres.split(",").filter((g) => g.trim() !== "");
  return f;
}

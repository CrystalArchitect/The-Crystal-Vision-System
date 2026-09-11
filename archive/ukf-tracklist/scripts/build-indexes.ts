import { resolve } from "node:path";
import { readJson, writeJson } from "./lib.js";
import type { Track, Indexes, ArtistRecord, YearRecord } from "../src/types.js";

const IN_PATH = resolve(process.cwd(), "src/data/.stage-3-deduped.json");
const TRACKS_OUT = resolve(process.cwd(), "src/data/tracks.json");
const INDEXES_OUT = resolve(process.cwd(), "src/data/indexes.json");

function push(map: Record<string, string[]>, key: string, value: string) {
  (map[key] ??= []).push(value);
}

function main() {
  const tracks = readJson<Track[]>(IN_PATH);

  const byArtist: Record<string, string[]> = {};
  const byYear: Record<string, string[]> = {};
  const byCategory: Record<string, string[]> = {};
  const byRemixer: Record<string, string[]> = {};
  const byCanonical: Record<string, string[]> = {};

  const artistAgg = new Map<string, ArtistRecord>();
  const yearAgg = new Map<number, YearRecord>();

  let totalBytes = 0;

  for (const t of tracks) {
    totalBytes += t.bytes;

    push(byArtist, t.artistSlug, t.id);
    if (t.year !== null) push(byYear, String(t.year), t.id);
    push(byCategory, t.category, t.id);
    if (t.remixerSlug) push(byRemixer, t.remixerSlug, t.id);
    push(byCanonical, t.canonicalId, t.id);

    const a = artistAgg.get(t.artistSlug) ?? {
      slug: t.artistSlug,
      name: t.artist,
      aliases: t.artistAliases,
      trackCount: 0,
      totalMb: 0,
      years: [],
    };
    a.trackCount++;
    a.totalMb = Math.round((a.totalMb + t.mb) * 10) / 10;
    if (t.year !== null && !a.years.includes(t.year)) a.years.push(t.year);
    artistAgg.set(t.artistSlug, a);

    if (t.year !== null) {
      const y = yearAgg.get(t.year) ?? { year: t.year, trackCount: 0, totalMb: 0 };
      y.trackCount++;
      y.totalMb = Math.round((y.totalMb + t.mb) * 10) / 10;
      yearAgg.set(t.year, y);
    }
  }

  const artists = Array.from(artistAgg.values())
    .map((a) => ({ ...a, years: a.years.sort((x, y) => x - y) }))
    .sort((a, b) => a.name.localeCompare(b.name));

  const years = Array.from(yearAgg.values()).sort((a, b) => a.year - b.year);

  const canonicalIds = new Set(tracks.map((t) => t.canonicalId));
  const remixerSlugs = new Set(tracks.map((t) => t.remixerSlug).filter(Boolean) as string[]);
  const duplicateCount = tracks.filter((t) => t.duplicateOf !== null).length;
  const duplicateGroupCount = new Set(
    tracks.filter((t) => t.duplicateGroupSize > 1).map((t) => t.canonicalId)
  ).size;

  const indexes: Indexes = {
    byArtist,
    byYear,
    byCategory,
    byRemixer,
    byCanonical,
    artists,
    years,
    stats: {
      totalTracks: tracks.length,
      totalBytes,
      uniqueCanonical: canonicalIds.size,
      duplicateCount,
      duplicateGroupCount,
      artistCount: artists.length,
      remixerCount: remixerSlugs.size,
      yearCount: years.length,
    },
  };

  writeJson(TRACKS_OUT, tracks);
  writeJson(INDEXES_OUT, indexes);

  console.log(`[build-indexes] tracks -> ${TRACKS_OUT}`);
  console.log(`[build-indexes] indexes -> ${INDEXES_OUT}`);
  console.log(
    `[build-indexes] ${indexes.stats.totalTracks} tracks - ${indexes.stats.artistCount} artists - ${indexes.stats.yearCount} years - ${indexes.stats.remixerCount} remixers`
  );
  console.log(
    `[build-indexes] ${indexes.stats.duplicateGroupCount} duplicate groups (${indexes.stats.duplicateCount} redundant copies)`
  );
}

main();

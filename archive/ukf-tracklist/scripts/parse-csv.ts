import { parse } from "csv-parse/sync";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { writeJson, slugify, toInt, bytesToMb } from "./lib.js";
import type { RawTrack, Track, Category } from "../src/types.js";

const CSV_PATH = resolve(process.cwd(), "data/tracklist.csv");
const OUT_PATH = resolve(process.cwd(), "src/data/.stage-1-parsed.json");

const FT_REGEX = /(?:^|\s)(?:ft\.?|feat\.?|featuring)\s+(.+)$/i;
const FT_PAREN_REGEX = /[\(\[]\s*(?:ft\.?|feat\.?|featuring)\s+([^\)\]]+)[\)\]]/gi;
const REMIX_REGEX = /\s*[\(\[]\s*([^\)\]]+?)\s+Remix\s*[\)\]]\s*$/i;
const VIP_REGEX = /[\(\[]\s*(?:[^\)\]]*?\s+)?VIP(?:\s+(?:Mix|Remix))?\s*[\)\]]/i;

function classifyFolder(folder: string): { category: Category; year: number | null } {
  if (/^\d{4}$/.test(folder)) {
    const y = parseInt(folder, 10);
    if (y >= 1990 && y <= 2100) return { category: "year", year: y };
  }
  const f = folder.toLowerCase();
  if (f === "heavy") return { category: "heavy", year: null };
  if (f === "remixes") return { category: "remixes", year: null };
  return { category: "other", year: null };
}

function splitFeaturedList(s: string): string[] {
  return s
    .split(/\s*,\s*/)
    .map((x) => x.trim())
    .filter(Boolean);
}

interface ParsedTitle {
  rawArtist: string;
  artist: string;
  rawTrackName: string;
  trackName: string;
  baseTrackName: string;
  featuredArtists: string[];
  featuredRaw: string | null;
  remixer: string | null;
  isRemix: boolean;
  isVIP: boolean;
}

// Matches a hyphen, en dash, or em dash used as the "Artist - Track"
// separator. Track lists exported from some tools use an en dash
// (\u2013) instead of a plain hyphen, so a literal " - " search
// silently fails and dumps the whole title into rawTrackName.
const ARTIST_SEP_REGEX = /\s[-\u2013\u2014]\s/;

function parseTitleParts(rawTitle: string): ParsedTitle {
  const sepMatch = rawTitle.match(ARTIST_SEP_REGEX);
  let rawArtist: string;
  let rawTrackName: string;
  if (!sepMatch || typeof sepMatch.index !== "number") {
    rawArtist = "";
    rawTrackName = rawTitle.trim();
  } else {
    rawArtist = rawTitle.slice(0, sepMatch.index).trim();
    rawTrackName = rawTitle.slice(sepMatch.index + sepMatch[0].length).trim();
  }

  let artist = rawArtist;
  const preFeatured: string[] = [];
  const m = rawArtist.match(FT_REGEX);
  if (m && typeof m.index === "number") {
    artist = rawArtist.slice(0, m.index).trim();
    preFeatured.push(...splitFeaturedList(m[1]));
  }

  const postFeatured: string[] = [];
  for (const match of rawTrackName.matchAll(FT_PAREN_REGEX)) {
    postFeatured.push(...splitFeaturedList(match[1]));
  }

  let trackWithStrip = rawTrackName.replace(FT_PAREN_REGEX, "").trim();

  let remixer: string | null = null;
  let isRemix = false;
  const remixMatch = trackWithStrip.match(REMIX_REGEX);
  if (remixMatch && typeof remixMatch.index === "number") {
    remixer = remixMatch[1].trim();
    isRemix = true;
    trackWithStrip = trackWithStrip.slice(0, remixMatch.index).trim();
  }

  const isVIP = VIP_REGEX.test(rawTrackName);

  const baseTrackName = trackWithStrip
    .replace(/\s*[\(\[]\s*[\)\]]/g, "")
    .replace(/\s+/g, " ")
    .trim();

  const trackName = baseTrackName || trackWithStrip || rawTrackName;

  const featuredArtists = [...preFeatured, ...postFeatured];

  return {
    rawArtist,
    artist: artist || rawArtist,
    rawTrackName,
    trackName,
    baseTrackName: trackName,
    featuredArtists,
    featuredRaw: featuredArtists.length ? featuredArtists.join(", ") : null,
    remixer,
    isRemix,
    isVIP,
  };
}

function makeId(folder: string, rawTitle: string, seen: Set<string>): string {
  const base = `${slugify(folder)}-${slugify(rawTitle)}`;
  let id = base;
  let n = 2;
  while (seen.has(id)) id = `${base}-${n++}`;
  seen.add(id);
  return id;
}

function readCsv(path: string): RawTrack[] {
  const raw = readFileSync(path, "utf8").replace(/^\uFEFF/, "");
  const rows = parse(raw, {
    columns: true,
    skip_empty_lines: true,
    relax_column_count: true,
    relax_quotes: true,
    trim: true,
  }) as Array<Record<string, string>>;

  const out: RawTrack[] = [];
  for (const row of rows) {
    const folder = (row.folder ?? "").trim();
    const title = (row.title ?? "").trim();
    const p = (row.path ?? "").trim();
    const bytes = toInt(row.bytes ?? "0");
    const youtubeSearch = (row.youtube_search ?? "").trim();
    if (!folder || !title) continue;
    out.push({ folder, title, path: p, bytes, youtubeSearch });
  }
  return out;
}

function main() {
  const raw = readCsv(CSV_PATH);
  const seenIds = new Set<string>();

  const tracks: Track[] = raw.map((r) => {
    const parsed = parseTitleParts(r.title);
    const { category, year } = classifyFolder(r.folder);
    return {
      id: makeId(r.folder, r.title, seenIds),
      canonicalId: "",
      folder: r.folder,
      year,
      category,
      rawTitle: r.title,
      rawArtist: parsed.rawArtist,
      artist: parsed.artist,
      artistSlug: slugify(parsed.artist),
      artistAliases: [],
      trackName: parsed.trackName,
      rawTrackName: parsed.rawTrackName,
      baseTrackName: parsed.baseTrackName,
      featuredArtists: parsed.featuredArtists,
      featuredRaw: parsed.featuredRaw,
      remixer: parsed.remixer,
      remixerSlug: parsed.remixer ? slugify(parsed.remixer) : null,
      isRemix: parsed.isRemix,
      isVIP: parsed.isVIP,
      path: r.path,
      bytes: r.bytes,
      mb: bytesToMb(r.bytes),
      youtubeSearch: r.youtubeSearch,
      duplicateOf: null,
      duplicateGroupSize: 1,
    };
  });

  writeJson(OUT_PATH, tracks);
  console.log(`[parse-csv] ${tracks.length} tracks -> ${OUT_PATH}`);
}

main();

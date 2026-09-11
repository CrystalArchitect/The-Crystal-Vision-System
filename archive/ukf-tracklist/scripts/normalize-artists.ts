import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { readJson, writeJson, slugify, normalizeForMatch } from "./lib.js";
import type { Track, AliasMap } from "../src/types.js";

const IN_PATH = resolve(process.cwd(), "src/data/.stage-1-parsed.json");
const OUT_PATH = resolve(process.cwd(), "src/data/.stage-2-normalized.json");
const ALIASES_PATH = resolve(process.cwd(), "data/aliases.json");

function loadAliases(): AliasMap {
  if (!existsSync(ALIASES_PATH)) return {};
  const map = readJson<AliasMap>(ALIASES_PATH);
  // Normalize keys on load so lookups are consistent
  const out: AliasMap = {};
  for (const [k, v] of Object.entries(map)) out[normalizeForMatch(k)] = v;
  return out;
}

function computeCanonicalId(t: Track): string {
  const parts: string[] = [
    normalizeForMatch(t.artist),
    normalizeForMatch(t.baseTrackName),
  ];
  if (t.featuredRaw) parts.push(normalizeForMatch(t.featuredRaw));
  if (t.remixer) parts.push(normalizeForMatch(t.remixer));
  if (t.isVIP) parts.push("vip");
  return slugify(parts.join(" "));
}

function main() {
  const tracks = readJson<Track[]>(IN_PATH);
  const aliases = loadAliases();

  const canonicalNameByArtist = new Map<string, string>();

  // Pass 1: resolve canonical display name per raw artist string
  for (const t of tracks) {
    const key = normalizeForMatch(t.artist);
    const canonical = aliases[key] ?? t.artist;
    canonicalNameByArtist.set(t.artist, canonical);
  }

  // Pass 2: apply, collect aliases, compute canonical ids
  const aliasesBySlug = new Map<string, Set<string>>();

  for (const t of tracks) {
    const canonicalName = canonicalNameByArtist.get(t.artist) ?? t.artist;
    t.artist = canonicalName;
    t.artistSlug = slugify(canonicalName);

    if (t.rawArtist && t.rawArtist !== canonicalName) {
      const set = aliasesBySlug.get(t.artistSlug) ?? new Set<string>();
      set.add(t.rawArtist);
      aliasesBySlug.set(t.artistSlug, set);
    }

    if (t.remixer) t.remixerSlug = slugify(t.remixer);
  }

  for (const t of tracks) {
    const set = aliasesBySlug.get(t.artistSlug);
    t.artistAliases = set ? Array.from(set) : [];
    t.canonicalId = computeCanonicalId(t);
  }

  writeJson(OUT_PATH, tracks);
  console.log(`[normalize-artists] ${tracks.length} tracks -> ${OUT_PATH}`);
  console.log(`[normalize-artists] ${aliasesBySlug.size} artists with aliases applied`);
}

main();

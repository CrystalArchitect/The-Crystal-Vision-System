import { resolve } from "node:path";
import { readJson, writeJson } from "./lib.js";
import type { Track, Category } from "../src/types.js";

const IN_PATH = resolve(process.cwd(), "src/data/.stage-2-normalized.json");
const OUT_PATH = resolve(process.cwd(), "src/data/.stage-3-deduped.json");

const CATEGORY_RANK: Record<Category, number> = {
  year: 0,
  heavy: 1,
  remixes: 2,
  other: 3,
};

function pickPrimary(group: Track[]): Track {
  return [...group].sort((a, b) => {
    const catDiff = CATEGORY_RANK[a.category] - CATEGORY_RANK[b.category];
    if (catDiff !== 0) return catDiff;

    const ya = a.year ?? 9999;
    const yb = b.year ?? 9999;
    if (ya !== yb) return ya - yb;

    if (a.bytes !== b.bytes) return b.bytes - a.bytes;

    return a.id.localeCompare(b.id);
  })[0];
}

function main() {
  const tracks = readJson<Track[]>(IN_PATH);

  const groups = new Map<string, Track[]>();
  for (const t of tracks) {
    const g = groups.get(t.canonicalId) ?? [];
    g.push(t);
    groups.set(t.canonicalId, g);
  }

  let dupCount = 0;
  let dupGroups = 0;

  for (const group of groups.values()) {
    if (group.length === 1) {
      group[0].duplicateOf = null;
      group[0].duplicateGroupSize = 1;
      continue;
    }
    dupGroups++;
    dupCount += group.length - 1;
    const primary = pickPrimary(group);
    for (const t of group) {
      t.duplicateGroupSize = group.length;
      t.duplicateOf = t.id === primary.id ? null : primary.id;
    }
  }

  writeJson(OUT_PATH, tracks);
  console.log(`[dedupe] ${tracks.length} tracks`);
  console.log(`[dedupe] ${groups.size} unique canonical ids`);
  console.log(`[dedupe] ${dupGroups} duplicate groups, ${dupCount} redundant copies`);
}

main();

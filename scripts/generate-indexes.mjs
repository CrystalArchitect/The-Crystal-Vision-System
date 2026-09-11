#!/usr/bin/env node
// SPDX-License-Identifier: MIT

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const tracksPath = path.join(__dirname, '..', 'public', 'data', 'tracks.json');

if (!fs.existsSync(tracksPath)) {
  console.error(`✗ Tracks file not found at ${tracksPath}`);
  console.error('Run generate-tracks.mjs first');
  process.exit(1);
}

const tracks = JSON.parse(fs.readFileSync(tracksPath, 'utf8'));

function buildIndexes(tracks) {
  const artists = new Set();
  const years = new Set();
  const categories = new Set();
  const genres = new Set();
  const tags = new Set();
  const remixers = new Set();
  const labels = new Set();
  const keySignatures = new Set();

  let bpmMin = Infinity;
  let bpmMax = -Infinity;

  tracks.forEach(track => {
    if (track.artist) artists.add(track.artist);
    if (track.remixer) remixers.add(track.remixer);
    years.add(track.year);
    categories.add(track.category);
    track.genres?.forEach(g => genres.add(g));
    track.tags?.forEach(t => tags.add(t));
    if (track.label) labels.add(track.label);
    if (track.key) keySignatures.add(track.key);

    bpmMin = Math.min(bpmMin, track.bpm);
    bpmMax = Math.max(bpmMax, track.bpm);
  });

  return {
    artists: Array.from(artists).sort(),
    years: Array.from(years).sort((a, b) => a - b),
    categories: Array.from(categories).sort(),
    genres: Array.from(genres).sort(),
    tags: Array.from(tags).sort(),
    remixers: Array.from(remixers).sort(),
    labels: Array.from(labels).sort(),
    keySignatures: Array.from(keySignatures).sort(),
    bpmRanges: {
      min: bpmMin,
      max: bpmMax,
      count: tracks.length,
    },
  };
}

const indexes = buildIndexes(tracks);
const indexPath = path.join(__dirname, '..', 'public', 'data', 'indexes.json');

fs.mkdirSync(path.dirname(indexPath), { recursive: true });
fs.writeFileSync(indexPath, JSON.stringify(indexes, null, 2));

console.log(`✓ Generated search indexes for ${tracks.length} tracks`);
console.log(`  - ${indexes.artists.length} artists`);
console.log(`  - ${indexes.years.length} years`);
console.log(`  - ${indexes.categories.length} categories`);
console.log(`  - ${indexes.genres.length} genres`);
console.log(`  - ${indexes.remixers.length} remixers`);
console.log(`  - ${indexes.labels.length} labels`);
console.log(`  - BPM range: ${indexes.bpmRanges.min}-${indexes.bpmRanges.max}`);
process.exit(0);

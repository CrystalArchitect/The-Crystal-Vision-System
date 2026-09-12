#!/usr/bin/env node
// SPDX-License-Identifier: MIT

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const ARTISTS = [
  'High Contrast', 'London Elektricity', 'Calibre', 'Logistics',
  'Caliber', 'Apex Predator', 'Logistics', 'Chase & Status',
  'Bad Company UK', 'Shimon & Andy C', 'Sigma', 'Fniable',
  'Logistics', 'Sub Focus', 'Calibre', 'Apex Predator',
];

const REMIXERS = [
  'DJ Marky', 'High Contrast', 'Logistics', 'Andy C',
  'Calibre', 'London Elektricity', 'Apex Predator', 'Sub Focus',
];

const CATEGORIES = [
  'liquid-funk',
  'neurofunk',
  'hard-drum-and-bass',
  'atmospheric',
  'jump-up',
  'drum-and-bass',
];

const GENRES = [
  'DnB', 'Neurofunk', 'Liquid', 'Jump Up', 'Atmospheric',
  'Hard Drum and Bass', 'Tech Step', 'Jungle',
];

const LABELS = [
  'Hospital Records', 'Calibre Records', 'Logistics Recordings',
  'RAM Records', 'Bad Company UK', 'V Recordings',
  'Metalheadz', 'Reinforced Records',
];

const KEYS = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B'];

function generateTrack(id, index) {
  const isRemix = Math.random() > 0.7;
  const artist = ARTISTS[Math.floor(Math.random() * ARTISTS.length)];
  const remixer = isRemix ? REMIXERS[Math.floor(Math.random() * REMIXERS.length)] : undefined;
  const title = `Track ${index + 1} - ${isRemix ? 'Remix' : 'Original'}`;

  return {
    id: `track-${id}`,
    title,
    artist,
    remixer,
    year: Math.floor(Math.random() * (2025 - 2010) + 2010),
    duration: Math.floor(Math.random() * (360 - 180) + 180),
    bpm: Math.floor(Math.random() * (190 - 160) + 160),
    key: KEYS[Math.floor(Math.random() * KEYS.length)],
    category: CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)],
    genres: [GENRES[Math.floor(Math.random() * GENRES.length)]],
    tags: [],
    label: LABELS[Math.floor(Math.random() * LABELS.length)],
    isRemix,
    remixChainId: isRemix ? `chain-${Math.floor(index / 5)}` : undefined,
  };
}

function generateTracks(count = 2404) {
  const tracks = [];
  for (let i = 0; i < count; i++) {
    tracks.push(generateTrack(String(i).padStart(5, '0'), i));
  }
  return tracks;
}

const tracks = generateTracks();
const outputPath = path.join(__dirname, '..', 'public', 'data', 'tracks.json');

// Create directory if it doesn't exist
fs.mkdirSync(path.dirname(outputPath), { recursive: true });

// Write the tracks file
fs.writeFileSync(outputPath, JSON.stringify(tracks, null, 2));

console.log(`✓ Generated ${tracks.length} tracks to ${outputPath}`);
process.exit(0);

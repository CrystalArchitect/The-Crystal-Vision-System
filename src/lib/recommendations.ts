// SPDX-License-Identifier: MIT

import type { Track } from "../types";

export interface TrackFeatures {
  id: string;
  title: string;
  artist: string;
  bpm: number;
  year: number;
  genres: string[];
  key: string;
}

export interface PlaylistProfile {
  avgBpm: number;
  bpmRange: { min: number; max: number };
  genres: Map<string, number>;
  yearRange: { min: number; max: number };
  avgYear: number;
  artists: Map<string, number>;
  keys: Map<string, number>;
}

export function getPlaylistProfile(tracks: Track[]): PlaylistProfile {
  if (tracks.length === 0) {
    return {
      avgBpm: 0,
      bpmRange: { min: 0, max: 0 },
      genres: new Map(),
      yearRange: { min: 0, max: 0 },
      avgYear: 0,
      artists: new Map(),
      keys: new Map(),
    };
  }

  const bpms = tracks.map((t) => t.bpm).filter((b) => b);
  const avgBpm = bpms.length > 0 ? bpms.reduce((a, b) => a + b, 0) / bpms.length : 0;
  const bpmRange = {
    min: Math.min(...bpms),
    max: Math.max(...bpms),
  };

  const genres = new Map<string, number>();
  const artists = new Map<string, number>();
  const keys = new Map<string, number>();

  tracks.forEach((t) => {
    t.genres.forEach((g) => genres.set(g, (genres.get(g) || 0) + 1));
    artists.set(t.artist, (artists.get(t.artist) || 0) + 1);
    if (t.key) {
      keys.set(t.key, (keys.get(t.key) || 0) + 1);
    }
  });

  const years = tracks
    .map((t) => t.year)
    .filter((y) => y)
    .sort((a, b) => a - b);
  const avgYear = years.length > 0 ? years.reduce((a, b) => a + b, 0) / years.length : 0;

  return {
    avgBpm,
    bpmRange,
    genres,
    yearRange: {
      min: years[0] || 0,
      max: years[years.length - 1] || 0,
    },
    avgYear,
    artists,
    keys,
  };
}

export function calculateSimilarity(track1: Track, track2: Track): number {
  let score = 0;
  let factors = 0;

  // Genre similarity (most important)
  const commonGenres = track1.genres.filter((g) => track2.genres.includes(g)).length;
  const totalGenres = new Set([...track1.genres, ...track2.genres]).size;
  if (totalGenres > 0) {
    score += (commonGenres / totalGenres) * 40;
    factors++;
  }

  // Artist similarity
  if (track1.artist === track2.artist) {
    score += 30;
  } else {
    score += 5; // Small bonus for different artists (variety)
  }
  factors++;

  // BPM similarity (within 20 BPM is considered similar)
  const bpmDiff = Math.abs(track1.bpm - track2.bpm);
  if (bpmDiff <= 20) {
    score += Math.max(0, 15 - bpmDiff / 2);
  }
  factors++;

  // Key compatibility (same key or complementary key)
  if (track1.key && track2.key) {
    if (track1.key === track2.key) {
      score += 10;
    }
    // Could add harmonic key wheel compatibility here
  }
  factors++;

  // Year proximity (tracks from similar era)
  if (track1.year && track2.year) {
    const yearDiff = Math.abs(track1.year - track2.year);
    if (yearDiff <= 10) {
      score += Math.max(0, 10 - yearDiff);
    }
  }
  factors++;

  return factors > 0 ? score / factors : 0;
}

export function recommendSimilarTracks(
  referenceTrack: Track,
  candidates: Track[],
  limit: number = 5
): Track[] {
  return candidates
    .filter((t) => t.id !== referenceTrack.id)
    .map((t) => ({
      track: t,
      score: calculateSimilarity(referenceTrack, t),
    }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((x) => x.track);
}

export function recommendForPlaylist(playlist: Track[], allTracks: Track[], limit: number = 10): Track[] {
  if (playlist.length === 0) {
    return allTracks.slice(0, limit);
  }

  const profile = getPlaylistProfile(playlist);
  const scoreCache = new Map<string, number>();

  const candidates = allTracks.filter((t) => !playlist.some((p) => p.id === t.id));

  candidates.forEach((track) => {
    let score = 0;

    // Genre match
    const genreMatches = track.genres.filter((g) => profile.genres.has(g)).length;
    score += genreMatches * 10;

    // BPM compatibility
    const bpmDist = Math.abs(track.bpm - profile.avgBpm);
    if (bpmDist <= profile.bpmRange.max - profile.bpmRange.min) {
      score += Math.max(0, 20 - bpmDist / 10);
    }

    // Key compatibility
    if (track.key && profile.keys.has(track.key)) {
      score += 5;
    }

    // Year proximity
    if (track.year) {
      const yearDist = Math.abs(track.year - profile.avgYear);
      score += Math.max(0, 10 - yearDist / 5);
    }

    // Artist diversity bonus
    if (!profile.artists.has(track.artist)) {
      score += 5;
    }

    scoreCache.set(track.id, score);
  });

  return candidates
    .map((t) => ({ track: t, score: scoreCache.get(t.id) || 0 }))
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((x) => x.track);
}

export function getGenreBasedRecommendations(
  selectedGenres: string[],
  allTracks: Track[],
  limit: number = 20
): Track[] {
  if (selectedGenres.length === 0) {
    return allTracks.slice(0, limit);
  }

  return allTracks
    .filter((t) => t.genres.some((g) => selectedGenres.includes(g)))
    .slice(0, limit);
}

export function getTrendingByGenre(
  allTracks: Track[],
  genre: string,
  limit: number = 10
): Track[] {
  // Trending: recent tracks in genre, sorted by artist frequency
  const tracksInGenre = allTracks.filter((t) => t.genres.includes(genre));
  const recentTracks = tracksInGenre
    .filter((t) => t.year && t.year >= new Date().getFullYear() - 5)
    .sort((a, b) => (b.year || 0) - (a.year || 0));

  return recentTracks.slice(0, limit);
}

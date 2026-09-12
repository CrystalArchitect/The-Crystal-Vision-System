// SPDX-License-Identifier: MIT

/**
 * Core types for the drum & bass music library
 */

export interface Track {
  id: string;
  title: string;
  artist: string;
  remixer?: string;
  year: number;
  duration: number; // seconds
  bpm: number;
  key?: string;
  category: string; // drum-and-bass, neurofunk, liquid, etc.
  genres: string[];
  tags?: string[];
  sourceUrl?: string;
  releaseDate?: string;
  label?: string;
  isRemix: boolean;
  remixChainId?: string; // tracks with same chain ID are remixes
  featured?: string[]; // featured artists
  isAustralian?: boolean; // Australian artist flag
  realm?: string; // 7 Realms categorization
}

export interface Realm {
  id: string;
  name: string;
  description: string;
  color: string;
  iconEmoji: string;
  genres: string[];
  mood: string;
  bpmRange: { min: number; max: number };
}

export interface SearchResult {
  track: Track;
  score: number;
  matches: {
    field: keyof Track;
    positions: number[];
  }[];
}

export interface UserMeta {
  ratings: Record<string, number>; // trackId -> rating (1-5)
  tags: Record<string, string[]>; // trackId -> user tags
  notes: Record<string, string>; // trackId -> user notes
  playlists: Playlist[];
  smartPlaylists: SmartPlaylist[];
  lastPlayed?: {
    trackId: string;
    timestamp: number;
  };
  theme: 'light' | 'dark' | 'auto';
  searchPreferences: {
    sortBy: 'relevance' | 'year' | 'title' | 'artist' | 'bpm';
    sortOrder: 'asc' | 'desc';
  };
}

export interface Playlist {
  id: string;
  name: string;
  description?: string;
  trackIds: string[];
  createdAt: number;
  updatedAt: number;
  isPublic: boolean;
  tags?: string[];
}

export interface SmartPlaylist {
  id: string;
  name: string;
  description?: string;
  rules: PlaylistRule[];
  isPublic: boolean;
  createdAt: number;
  updatedAt: number;
}

export interface PlaylistRule {
  field: string;
  operator: 'equals' | 'contains' | 'gt' | 'gte' | 'lt' | 'lte' | 'regex' | 'in';
  value: string | number | string[];
  logic?: 'and' | 'or'; // AND is default, applies to next rule
}

export interface SearchIndex {
  artists: string[];
  years: number[];
  categories: string[];
  genres: string[];
  tags: string[];
  remixers: string[];
  labels: string[];
  keys: string[];
  australianArtists: string[];
  realms: string[];
  bpmRanges: Array<{
    min: number;
    max: number;
    label: string;
  }>;
}

export interface ExportOptions {
  format: 'm3u' | 'json' | 'csv' | 'youtube';
  includeUserData?: boolean;
  filename?: string;
}

export interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  meta?: boolean;
  action: string;
  description: string;
}

export interface FilterState {
  artists: Set<string>;
  years: Set<number>;
  categories: Set<string>;
  genres: Set<string>;
  ratings?: Set<number>;
  bpmMin?: number;
  bpmMax?: number;
  searchQuery?: string;
}

export interface PaginationState {
  page: number;
  pageSize: number;
  total: number;
}

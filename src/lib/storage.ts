// SPDX-License-Identifier: MIT

import type { UserMeta, Playlist, SmartPlaylist } from '../types';

const STORAGE_KEY = 'dnb-library:user-meta';
const PLAYLIST_PREFIX = 'dnb-library:playlist:';
const SMART_PLAYLIST_PREFIX = 'dnb-library:smart:';

const DEFAULT_META: UserMeta = {
  ratings: {},
  tags: {},
  notes: {},
  playlists: [],
  smartPlaylists: [],
  theme: 'auto',
  searchPreferences: {
    sortBy: 'relevance',
    sortOrder: 'desc',
  },
};

/**
 * Get user metadata from localStorage
 */
export function getUserMeta(): UserMeta {
  if (typeof localStorage === 'undefined') return DEFAULT_META;

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return DEFAULT_META;

    const parsed = JSON.parse(stored);
    // Merge with defaults to handle new fields
    return {
      ...DEFAULT_META,
      ...parsed,
      ratings: parsed.ratings || {},
      tags: parsed.tags || {},
      notes: parsed.notes || {},
      playlists: parsed.playlists || [],
      smartPlaylists: parsed.smartPlaylists || [],
    };
  } catch (e) {
    console.error('Failed to parse user metadata:', e);
    return DEFAULT_META;
  }
}

/**
 * Save user metadata to localStorage
 */
export function setUserMeta(meta: Partial<UserMeta>): void {
  if (typeof localStorage === 'undefined') return;

  try {
    const current = getUserMeta();
    const updated = { ...current, ...meta };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  } catch (e) {
    console.error('Failed to save user metadata:', e);
  }
}

/**
 * Set a rating for a track
 */
export function setTrackRating(trackId: string, rating: number): void {
  const meta = getUserMeta();
  meta.ratings[trackId] = Math.max(0, Math.min(5, rating));
  setUserMeta(meta);
}

/**
 * Get rating for a track
 */
export function getTrackRating(trackId: string): number | undefined {
  return getUserMeta().ratings[trackId];
}

/**
 * Add tags to a track
 */
export function addTrackTags(trackId: string, tags: string[]): void {
  const meta = getUserMeta();
  if (!meta.tags[trackId]) {
    meta.tags[trackId] = [];
  }
  const existing = new Set(meta.tags[trackId]);
  tags.forEach(tag => existing.add(tag));
  meta.tags[trackId] = Array.from(existing);
  setUserMeta(meta);
}

/**
 * Remove tags from a track
 */
export function removeTrackTags(trackId: string, tags: string[]): void {
  const meta = getUserMeta();
  if (!meta.tags[trackId]) return;

  const tagSet = new Set(meta.tags[trackId]);
  tags.forEach(tag => tagSet.delete(tag));
  meta.tags[trackId] = Array.from(tagSet);
  setUserMeta(meta);
}

/**
 * Get tags for a track
 */
export function getTrackTags(trackId: string): string[] {
  return getUserMeta().tags[trackId] || [];
}

/**
 * Set note for a track
 */
export function setTrackNote(trackId: string, note: string): void {
  const meta = getUserMeta();
  if (note) {
    meta.notes[trackId] = note;
  } else {
    delete meta.notes[trackId];
  }
  setUserMeta(meta);
}

/**
 * Get note for a track
 */
export function getTrackNote(trackId: string): string | undefined {
  return getUserMeta().notes[trackId];
}

/**
 * Create a new playlist
 */
export function createPlaylist(name: string, description?: string): Playlist {
  const meta = getUserMeta();
  const id = `pl-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const playlist: Playlist = {
    id,
    name,
    description,
    trackIds: [],
    createdAt: Date.now(),
    updatedAt: Date.now(),
    isPublic: false,
  };
  meta.playlists.push(playlist);
  setUserMeta(meta);
  return playlist;
}

/**
 * Get all playlists
 */
export function getPlaylists(): Playlist[] {
  return getUserMeta().playlists;
}

/**
 * Get a playlist by ID
 */
export function getPlaylist(id: string): Playlist | undefined {
  return getUserMeta().playlists.find(p => p.id === id);
}

/**
 * Update a playlist
 */
export function updatePlaylist(
  id: string,
  updates: Partial<Omit<Playlist, 'id' | 'createdAt'>>
): void {
  const meta = getUserMeta();
  const playlist = meta.playlists.find(p => p.id === id);
  if (!playlist) return;

  Object.assign(playlist, updates, { updatedAt: Date.now() });
  setUserMeta(meta);
}

/**
 * Delete a playlist
 */
export function deletePlaylist(id: string): void {
  const meta = getUserMeta();
  meta.playlists = meta.playlists.filter(p => p.id !== id);
  setUserMeta(meta);
}

/**
 * Add track to playlist
 */
export function addTrackToPlaylist(playlistId: string, trackId: string): void {
  const playlist = getPlaylist(playlistId);
  if (!playlist) return;

  if (!playlist.trackIds.includes(trackId)) {
    playlist.trackIds.push(trackId);
    updatePlaylist(playlistId, { trackIds: playlist.trackIds });
  }
}

/**
 * Remove track from playlist
 */
export function removeTrackFromPlaylist(
  playlistId: string,
  trackId: string
): void {
  const playlist = getPlaylist(playlistId);
  if (!playlist) return;

  playlist.trackIds = playlist.trackIds.filter(id => id !== trackId);
  updatePlaylist(playlistId, { trackIds: playlist.trackIds });
}

/**
 * Reorder tracks in playlist
 */
export function reorderPlaylistTracks(
  playlistId: string,
  trackIds: string[]
): void {
  updatePlaylist(playlistId, { trackIds });
}

/**
 * Create a smart playlist
 */
export function createSmartPlaylist(
  name: string,
  description?: string
): SmartPlaylist {
  const meta = getUserMeta();
  const id = `sp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const playlist: SmartPlaylist = {
    id,
    name,
    description,
    rules: [],
    isPublic: false,
    createdAt: Date.now(),
    updatedAt: Date.now(),
  };
  meta.smartPlaylists.push(playlist);
  setUserMeta(meta);
  return playlist;
}

/**
 * Get all smart playlists
 */
export function getSmartPlaylists(): SmartPlaylist[] {
  return getUserMeta().smartPlaylists;
}

/**
 * Get a smart playlist by ID
 */
export function getSmartPlaylist(id: string): SmartPlaylist | undefined {
  return getUserMeta().smartPlaylists.find(p => p.id === id);
}

/**
 * Update a smart playlist
 */
export function updateSmartPlaylist(
  id: string,
  updates: Partial<Omit<SmartPlaylist, 'id' | 'createdAt'>>
): void {
  const meta = getUserMeta();
  const playlist = meta.smartPlaylists.find(p => p.id === id);
  if (!playlist) return;

  Object.assign(playlist, updates, { updatedAt: Date.now() });
  setUserMeta(meta);
}

/**
 * Delete a smart playlist
 */
export function deleteSmartPlaylist(id: string): void {
  const meta = getUserMeta();
  meta.smartPlaylists = meta.smartPlaylists.filter(p => p.id !== id);
  setUserMeta(meta);
}

/**
 * Set last played track
 */
export function setLastPlayed(trackId: string): void {
  const meta = getUserMeta();
  meta.lastPlayed = {
    trackId,
    timestamp: Date.now(),
  };
  setUserMeta(meta);
}

/**
 * Get last played track
 */
export function getLastPlayed(): { trackId: string; timestamp: number } | undefined {
  return getUserMeta().lastPlayed;
}

/**
 * Set theme preference
 */
export function setTheme(theme: 'light' | 'dark' | 'auto'): void {
  const meta = getUserMeta();
  meta.theme = theme;
  setUserMeta(meta);
}

/**
 * Get theme preference
 */
export function getTheme(): 'light' | 'dark' | 'auto' {
  return getUserMeta().theme;
}

/**
 * Export user data as JSON
 */
export function exportUserData(): string {
  return JSON.stringify(getUserMeta(), null, 2);
}

/**
 * Import user data from JSON
 */
export function importUserData(json: string): boolean {
  try {
    const parsed = JSON.parse(json);
    setUserMeta(parsed);
    return true;
  } catch (e) {
    console.error('Failed to import user data:', e);
    return false;
  }
}

/**
 * Clear all user data
 */
export function clearUserData(): void {
  if (typeof localStorage === 'undefined') return;
  localStorage.removeItem(STORAGE_KEY);
}

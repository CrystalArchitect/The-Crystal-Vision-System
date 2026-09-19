// SPDX-License-Identifier: MIT

import type { UserMeta, Playlist, SmartPlaylist } from '../types';
import { useUserStore } from './userStore';
import * as api from './api';

const STORAGE_KEY = 'dnb-library:user-meta';
const PLAYLIST_PREFIX = 'dnb-library:playlist:';
const SMART_PLAYLIST_PREFIX = 'dnb-library:smart:';
const SYNC_QUEUE_KEY = 'dnb-library:sync-queue';

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

interface SyncQueueItem {
  type: 'rating' | 'tags' | 'note' | 'playlist' | 'smartPlaylist';
  action: 'set' | 'add' | 'remove' | 'create' | 'update' | 'delete';
  data: Record<string, unknown>;
  timestamp: number;
}

/**
 * Get user from store
 */
function getCurrentUser() {
  try {
    const store = useUserStore.getState();
    return store.currentUser;
  } catch {
    return null;
  }
}

/**
 * Add item to sync queue for offline support
 */
function addToSyncQueue(item: SyncQueueItem): void {
  if (typeof localStorage === 'undefined') return;

  try {
    const queue = getSyncQueue();
    queue.push(item);
    localStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(queue));
  } catch (e) {
    console.error('Failed to add to sync queue:', e);
  }
}

/**
 * Get sync queue
 */
function getSyncQueue(): SyncQueueItem[] {
  if (typeof localStorage === 'undefined') return [];

  try {
    const stored = localStorage.getItem(SYNC_QUEUE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (e) {
    console.error('Failed to parse sync queue:', e);
    return [];
  }
}

/**
 * Clear sync queue
 */
function clearSyncQueue(): void {
  if (typeof localStorage === 'undefined') return;

  try {
    localStorage.removeItem(SYNC_QUEUE_KEY);
  } catch (e) {
    console.error('Failed to clear sync queue:', e);
  }
}

/**
 * Process queued mutations when coming back online
 */
export async function processSyncQueue(): Promise<void> {
  const user = getCurrentUser();
  if (!user) return;

  const queue = getSyncQueue();
  if (queue.length === 0) return;

  for (const item of queue) {
    try {
      switch (item.type) {
        case 'rating':
          if (item.action === 'set') {
            await api.setTrackRating(
              user.id,
              item.data.trackId as string,
              item.data.rating as number
            );
          }
          break;

        case 'tags':
          if (item.action === 'add') {
            await api.addTrackTags(
              user.id,
              item.data.trackId as string,
              item.data.tags as string[]
            );
          }
          break;

        case 'note':
          if (item.action === 'set') {
            await api.setTrackNote(
              user.id,
              item.data.trackId as string,
              item.data.note as string
            );
          }
          break;

        case 'playlist':
          if (item.action === 'create') {
            await api.createPlaylist(
              user.id,
              item.data.name as string,
              item.data.description as string | undefined,
              item.data.isPublic as boolean
            );
          } else if (item.action === 'update') {
            await api.updatePlaylist(
              item.data.playlistId as string,
              item.data.updates as Record<string, unknown>
            );
          } else if (item.action === 'delete') {
            await api.deletePlaylist(item.data.playlistId as string);
          }
          break;

        case 'smartPlaylist':
          if (item.action === 'create') {
            await api.createSmartPlaylist(
              user.id,
              item.data.name as string,
              item.data.description as string | undefined,
              item.data.isPublic as boolean
            );
          } else if (item.action === 'update') {
            await api.updateSmartPlaylist(
              item.data.playlistId as string,
              item.data.updates as Record<string, unknown>
            );
          } else if (item.action === 'delete') {
            await api.deleteSmartPlaylist(item.data.playlistId as string);
          }
          break;
      }
    } catch (err) {
      console.error(`Failed to sync ${item.type} (${item.action}):`, err);
      return;
    }
  }

  clearSyncQueue();
}

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
 * Set a rating for a track (optimistic update with background sync)
 */
export function setTrackRating(trackId: string, rating: number): void {
  const meta = getUserMeta();
  meta.ratings[trackId] = Math.max(0, Math.min(5, rating));
  setUserMeta(meta);

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'rating',
      action: 'set',
      data: { trackId, rating: meta.ratings[trackId] },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .setTrackRating(user.id, trackId, meta.ratings[trackId])
    .catch((err) => {
      console.error('Failed to sync rating:', err);
      addToSyncQueue({
        type: 'rating',
        action: 'set',
        data: { trackId, rating: meta.ratings[trackId] },
        timestamp: Date.now(),
      });
    });
}

/**
 * Get rating for a track
 */
export function getTrackRating(trackId: string): number | undefined {
  return getUserMeta().ratings[trackId];
}

/**
 * Add tags to a track (optimistic update with background sync)
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

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'tags',
      action: 'add',
      data: { trackId, tags: meta.tags[trackId] },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .addTrackTags(user.id, trackId, tags)
    .catch((err) => {
      console.error('Failed to sync tags:', err);
      addToSyncQueue({
        type: 'tags',
        action: 'add',
        data: { trackId, tags: meta.tags[trackId] },
        timestamp: Date.now(),
      });
    });
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
 * Set note for a track (optimistic update with background sync)
 */
export function setTrackNote(trackId: string, note: string): void {
  const meta = getUserMeta();
  if (note) {
    meta.notes[trackId] = note;
  } else {
    delete meta.notes[trackId];
  }
  setUserMeta(meta);

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'note',
      action: 'set',
      data: { trackId, note },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .setTrackNote(user.id, trackId, note)
    .catch((err) => {
      console.error('Failed to sync note:', err);
      addToSyncQueue({
        type: 'note',
        action: 'set',
        data: { trackId, note },
        timestamp: Date.now(),
      });
    });
}

/**
 * Get note for a track
 */
export function getTrackNote(trackId: string): string | undefined {
  return getUserMeta().notes[trackId];
}

/**
 * Create a new playlist (optimistic update with background sync)
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

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'playlist',
      action: 'create',
      data: { id, name, description, isPublic: false },
      timestamp: Date.now(),
    });
    return playlist;
  }

  api
    .createPlaylist(user.id, name, description, false)
    .catch((err) => {
      console.error('Failed to sync playlist creation:', err);
      addToSyncQueue({
        type: 'playlist',
        action: 'create',
        data: { id, name, description, isPublic: false },
        timestamp: Date.now(),
      });
    });

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
 * Update a playlist (optimistic update with background sync)
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

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'playlist',
      action: 'update',
      data: { playlistId: id, updates },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .updatePlaylist(id, updates)
    .catch((err) => {
      console.error('Failed to sync playlist update:', err);
      addToSyncQueue({
        type: 'playlist',
        action: 'update',
        data: { playlistId: id, updates },
        timestamp: Date.now(),
      });
    });
}

/**
 * Delete a playlist (optimistic update with background sync)
 */
export function deletePlaylist(id: string): void {
  const meta = getUserMeta();
  meta.playlists = meta.playlists.filter(p => p.id !== id);
  setUserMeta(meta);

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'playlist',
      action: 'delete',
      data: { playlistId: id },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .deletePlaylist(id)
    .catch((err) => {
      console.error('Failed to sync playlist deletion:', err);
      addToSyncQueue({
        type: 'playlist',
        action: 'delete',
        data: { playlistId: id },
        timestamp: Date.now(),
      });
    });
}

/**
 * Add track to playlist (optimistic update with background sync)
 */
export function addTrackToPlaylist(playlistId: string, trackId: string): void {
  const playlist = getPlaylist(playlistId);
  if (!playlist) return;

  if (!playlist.trackIds.includes(trackId)) {
    playlist.trackIds.push(trackId);
    updatePlaylist(playlistId, { trackIds: playlist.trackIds });

    const user = getCurrentUser();
    if (user) {
      api
        .addTrackToPlaylist(playlistId, trackId)
        .catch((err) => {
          console.error('Failed to sync adding track to playlist:', err);
        });
    }
  }
}

/**
 * Remove track from playlist (optimistic update with background sync)
 */
export function removeTrackFromPlaylist(
  playlistId: string,
  trackId: string
): void {
  const playlist = getPlaylist(playlistId);
  if (!playlist) return;

  playlist.trackIds = playlist.trackIds.filter(id => id !== trackId);
  updatePlaylist(playlistId, { trackIds: playlist.trackIds });

  const user = getCurrentUser();
  if (user) {
    api
      .removeTrackFromPlaylist(playlistId, trackId)
      .catch((err) => {
        console.error('Failed to sync removing track from playlist:', err);
      });
  }
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
 * Create a smart playlist (optimistic update with background sync)
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

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'smartPlaylist',
      action: 'create',
      data: { id, name, description, isPublic: false },
      timestamp: Date.now(),
    });
    return playlist;
  }

  api
    .createSmartPlaylist(user.id, name, description, false)
    .catch((err) => {
      console.error('Failed to sync smart playlist creation:', err);
      addToSyncQueue({
        type: 'smartPlaylist',
        action: 'create',
        data: { id, name, description, isPublic: false },
        timestamp: Date.now(),
      });
    });

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
 * Update a smart playlist (optimistic update with background sync)
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

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'smartPlaylist',
      action: 'update',
      data: { playlistId: id, updates },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .updateSmartPlaylist(id, updates)
    .catch((err) => {
      console.error('Failed to sync smart playlist update:', err);
      addToSyncQueue({
        type: 'smartPlaylist',
        action: 'update',
        data: { playlistId: id, updates },
        timestamp: Date.now(),
      });
    });
}

/**
 * Delete a smart playlist (optimistic update with background sync)
 */
export function deleteSmartPlaylist(id: string): void {
  const meta = getUserMeta();
  meta.smartPlaylists = meta.smartPlaylists.filter(p => p.id !== id);
  setUserMeta(meta);

  const user = getCurrentUser();
  if (!user) {
    addToSyncQueue({
      type: 'smartPlaylist',
      action: 'delete',
      data: { playlistId: id },
      timestamp: Date.now(),
    });
    return;
  }

  api
    .deleteSmartPlaylist(id)
    .catch((err) => {
      console.error('Failed to sync smart playlist deletion:', err);
      addToSyncQueue({
        type: 'smartPlaylist',
        action: 'delete',
        data: { playlistId: id },
        timestamp: Date.now(),
      });
    });
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
 * Set theme preference (optimistic update with background sync)
 */
export function setTheme(theme: 'light' | 'dark' | 'auto'): void {
  const meta = getUserMeta();
  meta.theme = theme;
  setUserMeta(meta);

  const user = getCurrentUser();
  if (!user) return;

  api
    .updateUserMetadata(user.id, { theme })
    .catch((err) => {
      console.error('Failed to sync theme preference:', err);
    });
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

// SPDX-License-Identifier: MIT

import { supabase } from './supabase';
import type { Playlist, SmartPlaylist, UserMeta } from '../types';

export class APIError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'APIError';
  }
}

export async function fetchPlaylists(userId: string): Promise<Playlist[]> {
  try {
    const { data, error } = await supabase
      .from('playlists')
      .select('*')
      .eq('user_id', userId)
      .order('updated_at', { ascending: false });

    if (error) throw new APIError(error.message, 'FETCH_PLAYLISTS_ERROR');
    return data || [];
  } catch (err) {
    console.error('Fetch playlists error:', err);
    throw err;
  }
}

export async function createPlaylist(
  userId: string,
  name: string,
  description?: string,
  isPublic: boolean = false
): Promise<Playlist | null> {
  try {
    const now = Date.now();
    const { data, error } = await supabase
      .from('playlists')
      .insert({
        user_id: userId,
        name,
        description,
        is_public: isPublic,
        track_ids: [],
        created_at: now,
        updated_at: now,
      })
      .select()
      .single();

    if (error) throw new APIError(error.message, 'CREATE_PLAYLIST_ERROR');

    return data
      ? {
          id: data.id,
          userId: data.user_id,
          name: data.name,
          description: data.description,
          trackIds: data.track_ids || [],
          createdAt: data.created_at,
          updatedAt: data.updated_at,
          isPublic: data.is_public,
        }
      : null;
  } catch (err) {
    console.error('Create playlist error:', err);
    throw err;
  }
}

export async function updatePlaylist(
  playlistId: string,
  updates: Partial<Omit<Playlist, 'id' | 'createdAt'>>
): Promise<Playlist | null> {
  try {
    const { data, error } = await supabase
      .from('playlists')
      .update({
        name: updates.name,
        description: updates.description,
        track_ids: updates.trackIds,
        is_public: updates.isPublic,
        updated_at: Date.now(),
      })
      .eq('id', playlistId)
      .select()
      .single();

    if (error) throw new APIError(error.message, 'UPDATE_PLAYLIST_ERROR');

    return data
      ? {
          id: data.id,
          userId: data.user_id,
          name: data.name,
          description: data.description,
          trackIds: data.track_ids || [],
          createdAt: data.created_at,
          updatedAt: data.updated_at,
          isPublic: data.is_public,
        }
      : null;
  } catch (err) {
    console.error('Update playlist error:', err);
    throw err;
  }
}

export async function deletePlaylist(playlistId: string): Promise<boolean> {
  try {
    const { error } = await supabase
      .from('playlists')
      .delete()
      .eq('id', playlistId);

    if (error) throw new APIError(error.message, 'DELETE_PLAYLIST_ERROR');
    return true;
  } catch (err) {
    console.error('Delete playlist error:', err);
    throw err;
  }
}

export async function addTrackToPlaylist(playlistId: string, trackId: string): Promise<boolean> {
  try {
    const { data: playlist, error: fetchError } = await supabase
      .from('playlists')
      .select('track_ids')
      .eq('id', playlistId)
      .single();

    if (fetchError) throw new APIError(fetchError.message, 'FETCH_PLAYLIST_ERROR');

    const trackIds = playlist?.track_ids || [];
    if (trackIds.includes(trackId)) return true;

    const { error } = await supabase
      .from('playlists')
      .update({
        track_ids: [...trackIds, trackId],
        updated_at: Date.now(),
      })
      .eq('id', playlistId);

    if (error) throw new APIError(error.message, 'ADD_TRACK_ERROR');
    return true;
  } catch (err) {
    console.error('Add track error:', err);
    throw err;
  }
}

export async function removeTrackFromPlaylist(playlistId: string, trackId: string): Promise<boolean> {
  try {
    const { data: playlist, error: fetchError } = await supabase
      .from('playlists')
      .select('track_ids')
      .eq('id', playlistId)
      .single();

    if (fetchError) throw new APIError(fetchError.message, 'FETCH_PLAYLIST_ERROR');

    const trackIds = (playlist?.track_ids || []).filter((id: string) => id !== trackId);

    const { error } = await supabase
      .from('playlists')
      .update({
        track_ids: trackIds,
        updated_at: Date.now(),
      })
      .eq('id', playlistId);

    if (error) throw new APIError(error.message, 'REMOVE_TRACK_ERROR');
    return true;
  } catch (err) {
    console.error('Remove track error:', err);
    throw err;
  }
}

export async function fetchUserMetadata(userId: string): Promise<Partial<UserMeta> | null> {
  try {
    const { data, error } = await supabase
      .from('user_metadata')
      .select('*')
      .eq('user_id', userId)
      .single();

    if (error && error.code !== 'PGRST116') {
      // PGRST116 is "not found" error
      throw new APIError(error.message, 'FETCH_METADATA_ERROR');
    }

    return data
      ? {
          ratings: data.ratings || {},
          tags: data.tags || {},
          notes: data.notes || {},
          theme: data.theme || 'auto',
        }
      : null;
  } catch (err) {
    console.error('Fetch metadata error:', err);
    throw err;
  }
}

export async function updateUserMetadata(userId: string, meta: Partial<UserMeta>): Promise<boolean> {
  try {
    const { error } = await supabase.from('user_metadata').upsert(
      {
        user_id: userId,
        ratings: meta.ratings,
        tags: meta.tags,
        notes: meta.notes,
        theme: meta.theme,
        updated_at: Date.now(),
      },
      { onConflict: 'user_id' }
    );

    if (error) throw new APIError(error.message, 'UPDATE_METADATA_ERROR');
    return true;
  } catch (err) {
    console.error('Update metadata error:', err);
    throw err;
  }
}

export async function setTrackRating(userId: string, trackId: string, rating: number): Promise<boolean> {
  try {
    const meta = await fetchUserMetadata(userId);
    const ratings = meta?.ratings || {};
    ratings[trackId] = Math.max(0, Math.min(5, rating));

    return updateUserMetadata(userId, { ratings });
  } catch (err) {
    console.error('Set track rating error:', err);
    throw err;
  }
}

export async function addTrackTags(userId: string, trackId: string, tags: string[]): Promise<boolean> {
  try {
    const meta = await fetchUserMetadata(userId);
    const allTags = meta?.tags || {};
    const existing = new Set(allTags[trackId] || []);

    tags.forEach((tag) => existing.add(tag));
    allTags[trackId] = Array.from(existing);

    return updateUserMetadata(userId, { tags: allTags });
  } catch (err) {
    console.error('Add track tags error:', err);
    throw err;
  }
}

export async function setTrackNote(userId: string, trackId: string, note: string): Promise<boolean> {
  try {
    const meta = await fetchUserMetadata(userId);
    const notes = meta?.notes || {};

    if (note) {
      notes[trackId] = note;
    } else {
      delete notes[trackId];
    }

    return updateUserMetadata(userId, { notes });
  } catch (err) {
    console.error('Set track note error:', err);
    throw err;
  }
}

export async function fetchSmartPlaylists(userId: string): Promise<SmartPlaylist[]> {
  try {
    const { data, error } = await supabase
      .from('smart_playlists')
      .select('*')
      .eq('user_id', userId)
      .order('updated_at', { ascending: false });

    if (error) throw new APIError(error.message, 'FETCH_SMART_PLAYLISTS_ERROR');
    return data || [];
  } catch (err) {
    console.error('Fetch smart playlists error:', err);
    throw err;
  }
}

export async function createSmartPlaylist(
  userId: string,
  name: string,
  description?: string,
  isPublic: boolean = false
): Promise<SmartPlaylist | null> {
  try {
    const now = Date.now();
    const { data, error } = await supabase
      .from('smart_playlists')
      .insert({
        user_id: userId,
        name,
        description,
        is_public: isPublic,
        rules: [],
        created_at: now,
        updated_at: now,
      })
      .select()
      .single();

    if (error) throw new APIError(error.message, 'CREATE_SMART_PLAYLIST_ERROR');

    return data
      ? {
          id: data.id,
          userId: data.user_id,
          name: data.name,
          description: data.description,
          rules: data.rules || [],
          isPublic: data.is_public,
          createdAt: data.created_at,
          updatedAt: data.updated_at,
        }
      : null;
  } catch (err) {
    console.error('Create smart playlist error:', err);
    throw err;
  }
}

export async function updateSmartPlaylist(
  playlistId: string,
  updates: Partial<Omit<SmartPlaylist, 'id' | 'createdAt'>>
): Promise<SmartPlaylist | null> {
  try {
    const { data, error } = await supabase
      .from('smart_playlists')
      .update({
        name: updates.name,
        description: updates.description,
        rules: updates.rules,
        is_public: updates.isPublic,
        updated_at: Date.now(),
      })
      .eq('id', playlistId)
      .select()
      .single();

    if (error) throw new APIError(error.message, 'UPDATE_SMART_PLAYLIST_ERROR');

    return data
      ? {
          id: data.id,
          userId: data.user_id,
          name: data.name,
          description: data.description,
          rules: data.rules || [],
          isPublic: data.is_public,
          createdAt: data.created_at,
          updatedAt: data.updated_at,
        }
      : null;
  } catch (err) {
    console.error('Update smart playlist error:', err);
    throw err;
  }
}

export async function deleteSmartPlaylist(playlistId: string): Promise<boolean> {
  try {
    const { error } = await supabase
      .from('smart_playlists')
      .delete()
      .eq('id', playlistId);

    if (error) throw new APIError(error.message, 'DELETE_SMART_PLAYLIST_ERROR');
    return true;
  } catch (err) {
    console.error('Delete smart playlist error:', err);
    throw err;
  }
}

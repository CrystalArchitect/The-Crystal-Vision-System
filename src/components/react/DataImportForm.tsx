// SPDX-License-Identifier: MIT

import { useState } from 'react';
import { importUserData, setUserMeta, getUserMeta } from '../../lib/storage';
import { useUserStore } from '../../lib/userStore';
import * as api from '../../lib/api';

interface DataImportFormProps {
  onSuccess?: () => void;
  onClose?: () => void;
}

export default function DataImportForm({ onSuccess, onClose }: DataImportFormProps) {
  const { currentUser } = useUserStore();
  const [mode, setMode] = useState<'paste' | 'upload'>('paste');
  const [jsonText, setJsonText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<'idle' | 'validating' | 'importing' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');
  const [importedCount, setImportedCount] = useState({ playlists: 0, ratings: 0, tags: 0, notes: 0, favorites: 0 });

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setJsonText(content);
      setMode('paste');
    };
    reader.readAsText(file);
  };

  const validateAndImport = async () => {
    if (!jsonText.trim()) {
      setStatus('error');
      setMessage('Please provide JSON data to import');
      return;
    }

    setIsLoading(true);
    setStatus('validating');
    setMessage('Validating data...');

    try {
      // Parse and validate JSON
      const parsed = JSON.parse(jsonText);

      if (!parsed.playlists && !parsed.ratings && !parsed.tags && !parsed.notes) {
        setStatus('error');
        setMessage('Invalid data format. Expected user metadata with playlists, ratings, tags, or notes.');
        setIsLoading(false);
        return;
      }

      // Count items being imported
      const counts = {
        playlists: Array.isArray(parsed.playlists) ? parsed.playlists.length : 0,
        ratings: Object.keys(parsed.ratings || {}).length,
        tags: Object.keys(parsed.tags || {}).length,
        notes: Object.keys(parsed.notes || {}).length,
        favorites: Array.isArray(parsed.favorites) ? parsed.favorites.length : 0,
      };
      setImportedCount(counts);

      setStatus('importing');
      setMessage('Importing data to local storage...');

      // Import to local storage
      const success = importUserData(jsonText);
      if (!success) throw new Error('Failed to import data');

      // If user is authenticated, sync to cloud
      if (currentUser) {
        setMessage('Syncing with cloud...');
        const meta = getUserMeta();

        try {
          // Sync playlists
          if (meta.playlists && meta.playlists.length > 0) {
            for (const playlist of meta.playlists) {
              const created = await api.createPlaylist(
                currentUser.id,
                playlist.name,
                playlist.description,
                false
              );

              // Add tracks to the created playlist
              if (created && playlist.trackIds && playlist.trackIds.length > 0) {
                for (const trackId of playlist.trackIds) {
                  try {
                    await api.addTrackToPlaylist(created.id, trackId);
                  } catch (err) {
                    console.warn(`Failed to add track ${trackId} to playlist`, err);
                  }
                }
              }
            }
          }

          // Sync metadata (ratings, tags, notes)
          if (Object.keys(meta.ratings || {}).length > 0 ||
              Object.keys(meta.tags || {}).length > 0 ||
              Object.keys(meta.notes || {}).length > 0) {
            await api.updateUserMetadata(currentUser.id, {
              ratings: meta.ratings,
              tags: meta.tags,
              notes: meta.notes,
            });
          }

          // Sync favorites if present
          if (parsed.favorites && Array.isArray(parsed.favorites) && parsed.favorites.length > 0) {
            for (const trackId of parsed.favorites) {
              try {
                await api.addToFavorites(currentUser.id, trackId);
              } catch (err) {
                console.warn(`Failed to add favorite ${trackId}`, err);
              }
            }
          }

          setMessage(`Successfully imported and synced ${Object.values(counts).reduce((a, b) => a + b, 0)} items!`);
        } catch (syncError) {
          console.error('Cloud sync error:', syncError);
          setMessage(`Data imported locally. Cloud sync failed: ${syncError instanceof Error ? syncError.message : 'Unknown error'}. Try again later.`);
        }
      } else {
        setMessage(`Successfully imported ${Object.values(counts).reduce((a, b) => a + b, 0)} items to local storage`);
      }

      setStatus('success');
      setTimeout(() => {
        onSuccess?.();
      }, 2000);
    } catch (error) {
      console.error('Import error:', error);
      setStatus('error');
      setMessage(error instanceof Error ? error.message : 'Import failed. Please check your JSON format.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-ink-900 border border-ink-800 rounded-lg p-6 max-w-2xl">
      <h2 className="text-2xl font-bold text-white mb-4">Import Your Data</h2>
      <p className="text-neutral-400 mb-6">
        Restore your playlists, ratings, and preferences from a previous export.
      </p>

      {/* Mode Selection */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setMode('paste')}
          className={`flex-1 py-2 px-4 rounded border transition ${
            mode === 'paste'
              ? 'bg-accent-400 text-ink-950 border-accent-400'
              : 'bg-ink-800 text-neutral-300 border-ink-700 hover:border-accent-500/50'
          }`}
        >
          Paste JSON
        </button>
        <button
          onClick={() => setMode('upload')}
          className={`flex-1 py-2 px-4 rounded border transition ${
            mode === 'upload'
              ? 'bg-accent-400 text-ink-950 border-accent-400'
              : 'bg-ink-800 text-neutral-300 border-ink-700 hover:border-accent-500/50'
          }`}
        >
          Upload File
        </button>
      </div>

      {/* Input Area */}
      <div className="mb-6">
        {mode === 'paste' ? (
          <textarea
            value={jsonText}
            onChange={(e) => setJsonText(e.target.value)}
            placeholder='Paste your exported JSON data here...'
            rows={8}
            className="w-full bg-ink-950 border border-ink-700 rounded px-3 py-2 text-sm text-neutral-300 placeholder-neutral-600 focus:border-accent-500 outline-none resize-none"
            disabled={isLoading}
          />
        ) : (
          <div className="border-2 border-dashed border-ink-700 rounded px-4 py-8 text-center">
            <input
              type="file"
              accept=".json,.txt"
              onChange={handleFileUpload}
              disabled={isLoading}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="text-neutral-400 mb-2">📁 Click to upload or drag and drop</div>
              <div className="text-xs text-neutral-600">JSON or text files only</div>
            </label>
            {jsonText && (
              <div className="mt-4 text-xs text-accent-400">
                File loaded: {jsonText.slice(0, 100)}...
              </div>
            )}
          </div>
        )}
      </div>

      {/* Status Messages */}
      {status !== 'idle' && (
        <div className={`mb-6 p-3 rounded text-sm ${
          status === 'success'
            ? 'bg-green-900/30 text-green-300 border border-green-700'
            : status === 'error'
            ? 'bg-red-900/30 text-red-300 border border-red-700'
            : 'bg-accent-500/20 text-accent-300 border border-accent-500/50'
        }`}>
          <div className="flex items-center gap-2">
            {isLoading && <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />}
            {message}
          </div>
          {status === 'success' && Object.values(importedCount).some(v => v > 0) && (
            <div className="mt-2 text-xs text-neutral-400">
              Imported: {importedCount.playlists} playlists, {importedCount.ratings} ratings,
              {importedCount.tags} tags, {importedCount.notes} notes
              {importedCount.favorites > 0 && `, ${importedCount.favorites} favorites`}
            </div>
          )}
        </div>
      )}

      {/* Import Info */}
      <div className="bg-ink-800 border border-ink-700 rounded p-4 mb-6">
        <h3 className="text-sm font-semibold text-neutral-300 mb-2">What gets imported?</h3>
        <ul className="text-xs text-neutral-400 space-y-1">
          <li>✓ Playlists and track collections</li>
          <li>✓ Track ratings and reviews</li>
          <li>✓ Custom tags and notes</li>
          <li>✓ Favorites and personal preferences</li>
          {currentUser && <li>✓ Auto-syncs to your cloud account</li>}
        </ul>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={validateAndImport}
          disabled={!jsonText.trim() || isLoading}
          className="flex-1 py-2 px-4 rounded bg-accent-400 text-ink-950 font-medium hover:bg-accent-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? 'Importing...' : 'Import Data'}
        </button>
        {onClose && (
          <button
            onClick={onClose}
            disabled={isLoading}
            className="px-4 py-2 rounded border border-ink-700 text-neutral-400 hover:text-neutral-300 hover:border-accent-500/50 disabled:opacity-50 transition-colors"
          >
            Cancel
          </button>
        )}
      </div>

      {/* Help Text */}
      <div className="mt-6 pt-6 border-t border-ink-800">
        <h3 className="text-sm font-semibold text-neutral-300 mb-2">Need help?</h3>
        <p className="text-xs text-neutral-500">
          If you don't have an export file, you can create one by using the "Export Your Data" button
          in your account settings. Make sure you're importing data from the same application version.
        </p>
      </div>
    </div>
  );
}

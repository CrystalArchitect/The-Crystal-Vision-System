// SPDX-License-Identifier: MIT

import { useState } from "react";
import type { Track } from "../../types";
import {
  exportToSpotifyUrl,
  exportToAppleMusicUrl,
  exportToJSON,
  exportToM3U,
  exportToCSV,
  downloadFile,
  getExportFilename,
} from "../../lib/export";

interface Props {
  playlistName: string;
  tracks: Track[];
  onClose: () => void;
}

export default function PlaylistExporter({ playlistName, tracks, onClose }: Props) {
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopyToClipboard = (text: string, format: string) => {
    navigator.clipboard.writeText(text);
    setCopied(format);
    setTimeout(() => setCopied(null), 2000);
  };

  const handleDownloadJSON = () => {
    const content = exportToJSON({
      name: playlistName,
      tracks,
      format: "json",
    });
    downloadFile(content, getExportFilename(playlistName, "json"), "application/json");
  };

  const handleDownloadM3U = () => {
    const content = exportToM3U(playlistName, tracks);
    downloadFile(content, getExportFilename(playlistName, "m3u"), "audio/x-mpegurl");
  };

  const handleDownloadCSV = () => {
    const content = exportToCSV({
      name: playlistName,
      tracks,
      format: "csv",
    });
    downloadFile(content, getExportFilename(playlistName, "csv"), "text/csv");
  };

  const spotifyUrl = exportToSpotifyUrl(playlistName, tracks);
  const appleMusicUrl = exportToAppleMusicUrl(playlistName, tracks);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-ink-900 rounded-lg border border-accent-500/30 p-6 max-w-2xl w-full max-h-96 overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Export Playlist</h2>
          <button
            onClick={onClose}
            className="text-neutral-400 hover:text-white transition"
          >
            ✕
          </button>
        </div>

        <div className="space-y-4">
          {/* Streaming Platforms */}
          <div>
            <h3 className="text-sm font-semibold text-neutral-300 mb-3">
              🎵 Streaming Platforms
            </h3>
            <div className="space-y-2">
              <button
                onClick={() => window.open(spotifyUrl, "_blank")}
                className="w-full flex items-center justify-between p-3 bg-ink-800 hover:bg-ink-700 border border-accent-500/20 rounded transition"
              >
                <span className="text-white font-medium">Open in Spotify</span>
                <span className="text-accent-400">→</span>
              </button>
              <button
                onClick={() => window.open(appleMusicUrl, "_blank")}
                className="w-full flex items-center justify-between p-3 bg-ink-800 hover:bg-ink-700 border border-accent-500/20 rounded transition"
              >
                <span className="text-white font-medium">Open in Apple Music</span>
                <span className="text-accent-400">→</span>
              </button>
            </div>
          </div>

          {/* Download Formats */}
          <div>
            <h3 className="text-sm font-semibold text-neutral-300 mb-3">
              💾 Download Formats
            </h3>
            <div className="space-y-2">
              <button
                onClick={handleDownloadJSON}
                className="w-full flex items-center justify-between p-3 bg-ink-800 hover:bg-ink-700 border border-accent-500/20 rounded transition"
              >
                <span className="text-white font-medium">JSON (Backup)</span>
                <span className="text-accent-400">↓</span>
              </button>
              <button
                onClick={handleDownloadM3U}
                className="w-full flex items-center justify-between p-3 bg-ink-800 hover:bg-ink-700 border border-accent-500/20 rounded transition"
              >
                <span className="text-white font-medium">M3U (Media Player)</span>
                <span className="text-accent-400">↓</span>
              </button>
              <button
                onClick={handleDownloadCSV}
                className="w-full flex items-center justify-between p-3 bg-ink-800 hover:bg-ink-700 border border-accent-500/20 rounded transition"
              >
                <span className="text-white font-medium">CSV (Spreadsheet)</span>
                <span className="text-accent-400">↓</span>
              </button>
            </div>
          </div>

          {/* Copy Links */}
          <div>
            <h3 className="text-sm font-semibold text-neutral-300 mb-3">
              🔗 Copy Links
            </h3>
            <div className="space-y-2">
              <div className="flex gap-2">
                <input
                  type="text"
                  readOnly
                  value={spotifyUrl}
                  className="flex-1 bg-ink-700 border border-accent-500/20 rounded px-3 py-2 text-xs text-neutral-400"
                />
                <button
                  onClick={() => handleCopyToClipboard(spotifyUrl, "spotify")}
                  className={`px-3 py-2 rounded text-xs font-medium transition ${
                    copied === "spotify"
                      ? "bg-accent-500 text-ink-900"
                      : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
                  }`}
                >
                  {copied === "spotify" ? "Copied!" : "Copy"}
                </button>
              </div>
              <div className="flex gap-2">
                <input
                  type="text"
                  readOnly
                  value={appleMusicUrl}
                  className="flex-1 bg-ink-700 border border-accent-500/20 rounded px-3 py-2 text-xs text-neutral-400"
                />
                <button
                  onClick={() => handleCopyToClipboard(appleMusicUrl, "apple")}
                  className={`px-3 py-2 rounded text-xs font-medium transition ${
                    copied === "apple"
                      ? "bg-accent-500 text-ink-900"
                      : "bg-ink-700 text-neutral-300 hover:bg-ink-600"
                  }`}
                >
                  {copied === "apple" ? "Copied!" : "Copy"}
                </button>
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="pt-4 border-t border-accent-500/10">
            <p className="text-xs text-neutral-400">
              Exporting <span className="text-accent-400 font-semibold">{tracks.length}</span> tracks
              from <span className="text-accent-400 font-semibold">{playlistName}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

// SPDX-License-Identifier: MIT

import type { Track } from "../types";

export interface PlaylistExportOptions {
  name: string;
  description?: string;
  tracks: Track[];
  format: "spotify" | "apple-music" | "json" | "m3u" | "csv";
}

export function exportToSpotifyUrl(playlistName: string, tracks: Track[]): string {
  // Generate Spotify search query based on playlist name and tracks
  // Users can search and recreate playlist in Spotify
  const trackQueries = tracks
    .map((t) => `"${t.title}" ${t.artist}`)
    .slice(0, 10) // Limit to first 10 for readability
    .join(" OR ");

  const encodedQuery = encodeURIComponent(`playlist: ${playlistName}`);
  return `https://open.spotify.com/search/${encodedQuery}`;
}

export function exportToAppleMusicUrl(playlistName: string, tracks: Track[]): string {
  // Generate Apple Music share URL structure
  // Note: Direct API integration would require Apple Music API key
  const trackInfo = tracks
    .map((t) => `${t.title} by ${t.artist}`)
    .slice(0, 10)
    .join(", ");

  return `https://music.apple.com/search?term=${encodeURIComponent(trackInfo)}`;
}

export function exportToJSON(options: PlaylistExportOptions): string {
  const data = {
    name: options.name,
    description: options.description,
    exportedAt: new Date().toISOString(),
    trackCount: options.tracks.length,
    tracks: options.tracks.map((t) => ({
      id: t.id,
      title: t.title,
      artist: t.artist,
      year: t.year,
      bpm: t.bpm,
      key: t.key,
      genres: t.genres,
      label: t.label,
      remixer: t.remixer,
    })),
  };

  return JSON.stringify(data, null, 2);
}

export function exportToM3U(playlistName: string, tracks: Track[]): string {
  // M3U playlist format
  let m3u = "#EXTM3U\n";
  m3u += `#PLAYLIST:${playlistName}\n`;

  tracks.forEach((track) => {
    // Duration in milliseconds (using 0 as placeholder since we don't have duration data)
    const duration = -1;
    const metadata = `#EXTINF:${duration},${track.artist} - ${track.title}`;
    m3u += `${metadata}\n`;
    // File path or streaming URL would go here
    m3u += `${track.id}\n`;
  });

  return m3u;
}

export function exportToCSV(options: PlaylistExportOptions): string {
  const headers = ["Title", "Artist", "Year", "BPM", "Key", "Genres", "Label", "Remixer"];
  const rows = options.tracks.map((t) => [
    t.title,
    t.artist,
    t.year?.toString() || "",
    t.bpm?.toString() || "",
    t.key || "",
    t.genres.join(";"),
    t.label || "",
    t.remixer || "",
  ]);

  // Escape CSV values
  const escapeCsv = (value: string) => {
    if (value.includes(",") || value.includes('"') || value.includes("\n")) {
      return `"${value.replace(/"/g, '""')}"`;
    }
    return value;
  };

  const csv = [
    headers.join(","),
    ...rows.map((row) => row.map(escapeCsv).join(",")),
  ].join("\n");

  return csv;
}

export function downloadFile(content: string, filename: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function getExportFilename(playlistName: string, format: string): string {
  const timestamp = new Date().toISOString().split("T")[0];
  const sanitizedName = playlistName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

  const extensions: Record<string, string> = {
    json: "json",
    m3u: "m3u",
    csv: "csv",
  };

  const ext = extensions[format] || "txt";
  return `${sanitizedName}-${timestamp}.${ext}`;
}

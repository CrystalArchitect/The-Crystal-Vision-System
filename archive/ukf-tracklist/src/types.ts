export type Category = "year" | "heavy" | "remixes" | "other";

export interface RawTrack {
  folder: string;
  title: string;
  path: string;
  bytes: number;
  youtubeSearch: string;
}

export interface Track {
  id: string;
  canonicalId: string;
  folder: string;
  year: number | null;
  category: Category;

  rawTitle: string;
  rawArtist: string;
  artist: string;
  artistSlug: string;
  artistAliases: string[];

  trackName: string;
  rawTrackName: string;
  baseTrackName: string;

  featuredArtists: string[];
  featuredRaw: string | null;

  remixer: string | null;
  remixerSlug: string | null;
  isRemix: boolean;
  isVIP: boolean;

  path: string;
  bytes: number;
  mb: number;
  youtubeSearch: string;

  duplicateOf: string | null;
  duplicateGroupSize: number;
}

export interface ArtistRecord {
  slug: string;
  name: string;
  aliases: string[];
  trackCount: number;
  totalMb: number;
  years: number[];
}

export interface YearRecord {
  year: number;
  trackCount: number;
  totalMb: number;
}

export interface Indexes {
  byArtist: Record<string, string[]>;
  byYear: Record<string, string[]>;
  byCategory: Record<string, string[]>;
  byRemixer: Record<string, string[]>;
  byCanonical: Record<string, string[]>;
  artists: ArtistRecord[];
  years: YearRecord[];
  stats: {
    totalTracks: number;
    totalBytes: number;
    uniqueCanonical: number;
    duplicateCount: number;
    duplicateGroupCount: number;
    artistCount: number;
    remixerCount: number;
    yearCount: number;
  };
}

export type AliasMap = Record<string, string>;

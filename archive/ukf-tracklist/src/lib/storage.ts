import { z } from "zod";

const NS = "ukf.v2";

function uid(len = 10): string {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let out = "";
  for (let i = 0; i < len; i++) out += chars[Math.floor(Math.random() * chars.length)];
  return out;
}

// --- Schemas -------------------------------------------------------------

export const UserMetaSchema = z.object({
  rating: z.number().int().min(0).max(5).default(0),
  tags: z.array(z.string().min(1).max(32)).max(64).default([]),
  notes: z.string().max(500).default(""),
  playCount: z.number().int().min(0).default(0),
  lastPlayedAt: z.string().nullable().default(null),
  addedToLibraryAt: z.string().default(() => new Date().toISOString()),
});

export const PlaylistSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1).max(120),
  description: z.string().max(500).default(""),
  trackIds: z.array(z.string()).default([]),
  createdAt: z.string(),
  updatedAt: z.string(),
});

export const RuleSchema = z.discriminatedUnion("field", [
  z.object({ field: z.literal("year"), op: z.enum([">=", "<=", "="]), value: z.number() }),
  z.object({ field: z.literal("artist"), op: z.enum(["=", "contains"]), value: z.string() }),
  z.object({ field: z.literal("remixer"), op: z.literal("="), value: z.string() }),
  z.object({ field: z.literal("category"), op: z.literal("="), value: z.string() }),
  z.object({ field: z.literal("mb"), op: z.enum([">=", "<="]), value: z.number() }),
  z.object({ field: z.literal("rating"), op: z.enum([">=", "<="]), value: z.number() }),
  z.object({ field: z.literal("tag"), op: z.literal("has"), value: z.string() }),
  z.object({ field: z.literal("playCount"), op: z.enum([">=", "="]), value: z.number() }),
  z.object({ field: z.literal("isRemix"), op: z.literal("="), value: z.boolean() }),
  z.object({ field: z.literal("isVIP"), op: z.literal("="), value: z.boolean() }),
]);

export const SmartPlaylistSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1).max(120),
  rules: z.array(RuleSchema).min(1),
  matchAll: z.boolean().default(true),
});

export const PrefsSchema = z.object({
  theme: z.enum(["dark", "light", "auto"]).default("dark"),
  view: z.enum(["table", "grid", "compact"]).default("table"),
  defaultSort: z.enum(["title", "artist", "year", "mb"]).default("artist"),
  defaultSortDir: z.enum(["asc", "desc"]).default("asc"),
  lastVisitedAt: z.string().default(() => new Date().toISOString()),
});

export type UserMeta = z.infer<typeof UserMetaSchema>;
export type Playlist = z.infer<typeof PlaylistSchema>;
export type SmartPlaylist = z.infer<typeof SmartPlaylistSchema>;
export type Rule = z.infer<typeof RuleSchema>;
export type Prefs = z.infer<typeof PrefsSchema>;

// --- Safe read/write -----------------------------------------------------

function safeRead<S extends z.ZodTypeAny>(
  key: string,
  schema: S,
  fallback: z.output<S>
): z.output<S> {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = window.localStorage.getItem(key);
    if (!raw) return fallback;
    const parsed = JSON.parse(raw);
    const result = schema.safeParse(parsed);
    if (!result.success) {
      console.warn(`[storage] invalid data at ${key}, resetting`, result.error);
      window.localStorage.removeItem(key);
      return fallback;
    }
    return result.data;
  } catch (err) {
    console.warn(`[storage] failed to read ${key}`, err);
    return fallback;
  }
}

function safeWrite(key: string, value: unknown): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch (err) {
    console.warn(`[storage] failed to write ${key}`, err);
  }
}

// --- Meta ----------------------------------------------------------------

const MetaMapSchema = z.record(z.string(), UserMetaSchema);

export function readMeta(): Record<string, UserMeta> {
  return safeRead(`${NS}.meta`, MetaMapSchema, {});
}

export function writeMeta(map: Record<string, UserMeta>): void {
  safeWrite(`${NS}.meta`, map);
}

export function getMeta(canonicalId: string): UserMeta {
  const map = readMeta();
  return map[canonicalId] ?? UserMetaSchema.parse({});
}

export function setMeta(canonicalId: string, patch: Partial<UserMeta>): UserMeta {
  const map = readMeta();
  const prev = map[canonicalId] ?? UserMetaSchema.parse({});
  const next = UserMetaSchema.parse({ ...prev, ...patch });
  map[canonicalId] = next;
  writeMeta(map);
  return next;
}

export function recordPlay(canonicalId: string): void {
  const prev = getMeta(canonicalId);
  setMeta(canonicalId, {
    playCount: prev.playCount + 1,
    lastPlayedAt: new Date().toISOString(),
  });
}

export function removeMeta(canonicalId: string): void {
  const map = readMeta();
  delete map[canonicalId];
  writeMeta(map);
}

// --- Playlists -----------------------------------------------------------

const PlaylistArraySchema = z.array(PlaylistSchema);

export function readPlaylists(): Playlist[] {
  return safeRead(`${NS}.playlists`, PlaylistArraySchema, []);
}

export function writePlaylists(list: Playlist[]): void {
  safeWrite(`${NS}.playlists`, list);
}

export function addPlaylist(name: string, description = ""): Playlist {
  const now = new Date().toISOString();
  const pl: Playlist = {
    id: uid(10),
    name,
    description,
    trackIds: [],
    createdAt: now,
    updatedAt: now,
  };
  writePlaylists([...readPlaylists(), pl]);
  return pl;
}

export function updatePlaylist(id: string, patch: Partial<Playlist>): void {
  const list = readPlaylists().map((p) =>
    p.id === id ? { ...p, ...patch, updatedAt: new Date().toISOString() } : p
  );
  writePlaylists(list);
}

export function deletePlaylist(id: string): void {
  writePlaylists(readPlaylists().filter((p) => p.id !== id));
}

// --- Smart playlists -----------------------------------------------------

const SmartArraySchema = z.array(SmartPlaylistSchema);

export function readSmartPlaylists(): SmartPlaylist[] {
  return safeRead(`${NS}.smart`, SmartArraySchema, []);
}

export function writeSmartPlaylists(list: SmartPlaylist[]): void {
  safeWrite(`${NS}.smart`, list);
}

// --- Prefs ---------------------------------------------------------------

export function readPrefs(): Prefs {
  return safeRead(`${NS}.prefs`, PrefsSchema, PrefsSchema.parse({}));
}

export function writePrefs(patch: Partial<Prefs>): Prefs {
  const next = PrefsSchema.parse({ ...readPrefs(), ...patch });
  safeWrite(`${NS}.prefs`, next);
  return next;
}

// --- Export / import -----------------------------------------------------

export function exportAll(): string {
  return JSON.stringify(
    {
      version: 2,
      exportedAt: new Date().toISOString(),
      meta: readMeta(),
      playlists: readPlaylists(),
      smart: readSmartPlaylists(),
      prefs: readPrefs(),
    },
    null,
    2
  );
}

export function importAll(json: string): { imported: number; errors: string[] } {
  const errors: string[] = [];
  let imported = 0;
  try {
    const data = JSON.parse(json);
    if (data.meta) {
      const parsed = MetaMapSchema.safeParse(data.meta);
      if (parsed.success) {
        writeMeta({ ...readMeta(), ...parsed.data });
        imported += Object.keys(parsed.data).length;
      } else errors.push("meta failed validation");
    }
    if (data.playlists) {
      const parsed = PlaylistArraySchema.safeParse(data.playlists);
      if (parsed.success) {
        writePlaylists([...readPlaylists(), ...parsed.data]);
        imported += parsed.data.length;
      } else errors.push("playlists failed validation");
    }
    if (data.smart) {
      const parsed = SmartArraySchema.safeParse(data.smart);
      if (parsed.success) {
        writeSmartPlaylists([...readSmartPlaylists(), ...parsed.data]);
        imported += parsed.data.length;
      } else errors.push("smart failed validation");
    }
    if (data.prefs) {
      const parsed = PrefsSchema.safeParse(data.prefs);
      if (parsed.success) {
        safeWrite(`${NS}.prefs`, parsed.data);
        imported += 1;
      } else errors.push("prefs failed validation");
    }
  } catch (err) {
    errors.push(`parse error: ${(err as Error).message}`);
  }
  return { imported, errors };
}

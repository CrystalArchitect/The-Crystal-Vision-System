# ukf-tracklist

A build-time data pipeline that turns a flat CSV of track filenames into a
normalized, deduplicated, indexed dataset (`tracks.json` + `indexes.json`)
for a drum & bass / dubstep tracklist browser. Client-side storage
(playlists, ratings, smart playlists, prefs) lives in `src/lib/storage.ts`
as a separate, browser-only concern — it isn't part of the build pipeline.

## Status

The data pipeline (this README's subject) is done and verified against a
synthetic CSV covering the tricky cases below. **`data/tracklist.csv` —
the actual track data — has not been supplied yet.** Drop your real CSV in
at `data/tracklist.csv` (columns: `folder,title,path,bytes,youtube_search`)
before running `npm run data`.

## Setup

```
npm install
# put your real data/tracklist.csv in place, then:
npm run data
```

Runs `parse-csv -> normalize-artists -> dedupe -> build-indexes` in
sequence, writing intermediate `.stage-*.json` files (gitignored) and
finally `src/data/tracks.json` + `src/data/indexes.json` — the two files
an app builds against.

`npm run typecheck` runs `tsc --noEmit` over the whole package.

## Fixes applied to the originally drafted scripts

Two real bugs were caught and fixed before this was committed — both
verified against a synthetic CSV, not just read for style:

1. **`scripts/parse-csv.ts` had a syntax error.** Two lines that belonged
   inside `readCsv`'s row loop (`const p = ...`, `const bytes = ...`) had
   gotten spliced into the middle of `parseTitleParts`, leaving an
   unbalanced `)` and an incomplete `toInt(row.bytes` call — the file
   could not even be parsed by `tsx`/esbuild. Restored both functions;
   `readCsv` now correctly converts `bytes` to a number via `toInt`
   (`RawTrack.bytes` is typed `number`, and the original left it as a raw
   CSV string).

2. **Artist/track splitting only recognized a plain ASCII hyphen** (
   `rawTitle.indexOf(" - ")`). A real title in the sample data uses an en
   dash instead (`Dossa & Locuzzed – Tha Bird (ft. DJ Marky)` — this was
   one of the two titles flagged for spot-checking), which silently failed
   to split at all: the whole string landed in `trackName` with `artist`
   empty. `ARTIST_SEP_REGEX` now matches a hyphen, en dash (`–`), or
   em dash (`—`) between spaces.

Verified end-to-end against a 6-row synthetic CSV covering: the Friction &
Skream / Calyx & TeeBee remix case (multi-artist `Ft.` list, remix
detection), the en-dash case above, a `(VIP Mix)` title, and a deliberate
exact duplicate (confirmed `dedupe.ts` collapses it to one canonical group
of size 2). `tsc --noEmit` is clean under `strict: true`.

One more fix, in `src/lib/storage.ts`: `safeRead`'s generic signature
(`<T>(key, schema: z.ZodType<T>, fallback: T): T`) let TypeScript infer
`T` from the Zod schema's *input* shape (all `.default()` fields optional)
instead of its *output* shape (fields populated, required) — a real
`strict: true` type error, not a false positive. Changed to
`<S extends z.ZodTypeAny>(key, schema: S, fallback: z.output<S>): z.output<S>`,
which pins inference to the schema's output type deterministically.
`tsconfig.json` also needed `"DOM"` added to `lib` — `storage.ts`
references `window`/`localStorage`, and `"ES2022"` alone doesn't declare
those globals (the code's own `typeof window === "undefined"` runtime
guard was already correct; this was purely a types gap for the checker).

## Known limitation carried over as-is (not fixed, just documented)

`splitFeaturedList` only splits on commas, so `"P Money & Riko Dan"` in a
`Ft. Scrufizzer, P Money & Riko Dan` list stays one entry rather than two.
That matches the original design intent (an `&`-joined pair is often a
duo credited together) — flagging it here in case that's not what's
wanted for every case.

One alias entry in `data/aliases.json`, `"dirtyphonics ft. tali"`, is
likely unreachable: `FT_REGEX` strips a plain (non-parenthetical)
`ft./feat.` off the artist string *before* alias lookup runs, so by the
time normalization sees it the artist is already just `"Dirtyphonics"`.
Left in place since it's harmless dead data, not wrong data — worth
confirming against the real CSV once it's in.

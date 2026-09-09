# Visual QA notes

## Production preview
The SvelteKit production preview loaded successfully after allowing the proxied preview host in `vite.config.js`.

## Homepage
The homepage renders the updated title `TerAustralis Incognita — Observed from the Edge`, a restrained dark observatory composition, quiet primary navigation, the hero phrase “Observed from the edge,” and an explicit poetic disclaimer for “The edge is where you see furthest.” The three primary map links are present and labelled BUILT / What exists., PROPOSAL / What we are exploring., and CODEX / What we imagine. The interpretation-boundary band visibly states that H2 is an analytical encoder study, HPS → crystal is a research hypothesis, the Atlas is vision-layer mythic cartography, and CrystalCore is limited to its demonstrated software scope.

## Archive
The archive route renders grouped sections for Built / implemented, Partial / in development, and Vision / design. The document cards use titles and descriptions loaded from the repository’s authoritative Markdown source. The archive preserves the existing governance and status wording surfaced by those source documents.

## QA caveat
The repository’s existing `npm run check` reports 96 errors in legacy JavaScript/Svelte files, including gallery typing diagnostics; no diagnostics were reported for the changed homepage, archive page, header, ObservatoryMap component, token file, or HTML shell in the captured output. `npm run build` succeeds and writes the static site to `build`.

## Final verification update

After the archive helper annotation was added, `npm run build` passes again. `npm run check` still fails with 95 errors and one warning in seven untouched legacy files; the changed files produce no diagnostics in the check output. The production build completes successfully and outputs the static site to `vision/site/build`.

// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

import { marked } from 'marked';

// Read every markdown file in src/content as raw text at build time.
const files = import.meta.glob('../content/*.md', {
  query: '?raw',
  import: 'default',
  eager: true
});

/** @param {string} path */
function slugFromPath(path) {
  return (path.split('/').pop() ?? '').replace(/\.md$/i, '').toLowerCase();
}

/**
 * Pull the first level-1 heading to use as the document title.
 * @param {string} raw
 * @param {string} fallback
 */
function extractTitle(raw, fallback) {
  const match = raw.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : fallback;
}

/**
 * Grab the first meaningful line of prose for a short description.
 * @param {string} raw
 */
function extractDescription(raw) {
  for (const line of raw.split('\n')) {
    const text = line.trim();
    if (!text) continue;
    if (text.startsWith('#')) continue; // headings
    if (text.startsWith('![')) continue; // images
    if (text.startsWith('|') || text.startsWith('---')) continue; // tables / rules
    if (text.startsWith('>')) return stripInline(text.replace(/^>\s?/, ''));
    if (/^\*[^*]+\*$/.test(text)) continue; // stand-alone italic credit lines
    return stripInline(text);
  }
  return '';
}

/** @param {string} text */
function stripInline(text) {
  return text.replace(/[*_`>#]/g, '').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').trim();
}

const GITHUB_BLOB = 'https://github.com/CrystalArchitect/TerAustralis-Incognita/blob/main';

/**
 * Rewrite in-repo links/images so they work inside the app viewer:
 *  - relative asset paths -> absolute (/assets/...)
 *  - cross-document .md links to archived docs -> /docs/<slug>
 *  - other in-repo .md links (e.g. README, LICENSE) -> GitHub source
 * @param {string} html
 * @param {Set<string>} knownSlugs
 */
function rewriteLinks(html, knownSlugs) {
  return html
    .replace(/(src|href)="(?:\.\/)?assets\//g, '$1="/assets/')
    .replace(
      /href="(?:\.\/)?([A-Za-z0-9_-]+)\.md(#[^"]*)?"/g,
      (_m, name, hash = '') => {
        const slug = name.toLowerCase();
        if (knownSlugs.has(slug)) {
          return `href="/docs/${slug}${hash || ''}"`;
        }
        return `href="${GITHUB_BLOB}/${name}.md"`;
      }
    );
}

/** @typedef {{ slug: string, title: string, description: string, raw: string }} Doc */

/** @type {Doc[]} */
export const docs = Object.entries(files)
  .map(([path, raw]) => {
    const slug = slugFromPath(path);
    return {
      slug,
      title: extractTitle(/** @type {string} */ (raw), slug),
      description: extractDescription(/** @type {string} */ (raw)),
      raw: /** @type {string} */ (raw)
    };
  })
  .sort((a, b) => a.title.localeCompare(b.title));

/** @returns {{ slug: string, title: string, description: string }[]} */
export function listDocs() {
  return docs.map(({ slug, title, description }) => ({ slug, title, description }));
}

/** @param {string} slug */
export function getDoc(slug) {
  return docs.find((doc) => doc.slug === slug);
}

const knownSlugs = new Set(docs.map((doc) => doc.slug));

/** @param {string} raw */
export function renderMarkdown(raw) {
  const html = marked.parse(raw, { async: false, gfm: true, breaks: false });
  return rewriteLinks(/** @type {string} */ (html), knownSlugs);
}

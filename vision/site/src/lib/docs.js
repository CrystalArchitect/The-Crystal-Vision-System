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
const GITHUB_TREE = 'https://github.com/CrystalArchitect/TerAustralis-Incognita/tree/main';

// Canon is authored in the umbrella repository at mythos/content/ and copied
// here verbatim. Links inside it are written relative to *that* directory, so
// '../README.md' means mythos/README.md and '../../docs/x.md' means docs/x.md.
// Resolving against this constant is what lets the copy stay byte-identical to
// canon: without it, every copied file needs its links hand-adjusted, and hand
// adjustment is exactly how the two trees drift apart.
const CANON_DIR = 'mythos/content';

/**
 * Resolve a canon-relative href to its path within the umbrella repository.
 * @param {string} href
 */
function resolveRepoPath(href) {
  /** @type {string[]} */
  const out = [];
  for (const part of `${CANON_DIR}/${href}`.split('/')) {
    if (part === '' || part === '.') continue;
    if (part === '..') out.pop();
    else out.push(part);
  }
  return out.join('/');
}

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
    // Any in-repo .md link, at any depth. A sibling canon document becomes an
    // in-app route; anything else (README, governance, mythos siblings) becomes
    // a link to its source, because it is not part of the site.
    .replace(
      /href="((?:\.{1,2}\/)*[A-Za-z0-9_./-]+\.md)(#[^"]*)?"/g,
      (_m, rel, hash = '') => {
        const name = (rel.split('/').pop() ?? '').replace(/\.md$/i, '');
        const slug = name.toLowerCase();
        if (knownSlugs.has(slug)) {
          return `href="/docs/${slug}${hash || ''}"`;
        }
        return `href="${GITHUB_BLOB}/${resolveRepoPath(rel)}${hash || ''}"`;
      }
    )
    // Directory links (../tools/, ../art/, lattice-case-study/) point at
    // repository trees. The prefix is optional: canon also writes sibling
    // directory links bare. Absolute URLs never match — ':' is outside the
    // character class — and app-absolute paths are excluded by the leading
    // '/' guard.
    .replace(
      /href="((?:\.{1,2}\/)*[A-Za-z0-9_.-][A-Za-z0-9_./-]*\/)"/g,
      (_m, rel) => `href="${GITHUB_TREE}/${resolveRepoPath(rel)}"`
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

/**
 * Give every heading a GitHub-style id so in-document anchors resolve.
 * marked emits bare <h1>..<h6>, so a link to '#the-three-songs' had nothing
 * to land on -- every anchor in canon was silently dead until a cross-document
 * one made the prerenderer say so.
 * @param {string} html
 */
function addHeadingIds(html) {
  const used = new Map();
  return html.replace(
    /<h([1-6])([^>]*)>([\s\S]*?)<\/h\1>/g,
    (match, level, attrs, inner) => {
      if (/\sid=/.test(attrs)) return match;
      const base = inner
        .replace(/<[^>]+>/g, '')       // strip inline markup
        .trim()
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')      // drop punctuation
        .replace(/\s+/g, '-');
      if (!base) return match;
      // Repeated headings get -1, -2 ... exactly as GitHub numbers them.
      const seen = used.get(base) ?? 0;
      used.set(base, seen + 1);
      const id = seen === 0 ? base : `${base}-${seen}`;
      return `<h${level}${attrs} id="${id}">${inner}</h${level}>`;
    }
  );
}

/** @param {string} raw */
export function renderMarkdown(raw) {
  const html = marked.parse(raw, { async: false, gfm: true, breaks: false });
  return addHeadingIds(rewriteLinks(/** @type {string} */ (html), knownSlugs));
}

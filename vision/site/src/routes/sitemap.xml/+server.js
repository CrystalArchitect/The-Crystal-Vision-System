// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

// The sitemap generates itself from the routes that actually exist, at
// build time, so it can never drift from the site the way a hand-written
// XML file would. Deliberately <loc>-only: lastmod/changefreq/priority
// are optional hints, crawlers largely ignore the latter two, and a
// truthful per-page lastmod is not derivable in this static build — a
// wrong date is worse than none.

import { docs } from '$lib/docs.js';

export const prerender = true;

const ORIGIN = 'https://www.teraustralis.com.au';

// Every top-level route with a page. Kept in one place, in render order.
const PAGES = [
  '/',
  '/apocryphon',
  '/bio',
  '/bridge-to-the-light',
  '/clementine',
  '/codex',
  '/crystalcore',
  '/crystalcore-os',
  '/brief',
  '/docs',
  '/earth-twin',
  '/the-licence',
  '/wavelength',
  '/after-the-radar',
  '/bci-aerotropolis',
  '/gallery',
  '/join',
  '/ledger',
  '/minerals',
  '/music',
  '/ordinals',
  '/provenance',
  '/repositories',
  '/review',
  '/starline',
  '/stories'
];

export function GET() {
  const urls = [...PAGES, ...docs.map((d) => `/docs/${d.slug}`)]
    .map((path) => `  <url><loc>${ORIGIN}${path}</loc></url>`)
    .join('\n');

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`;

  return new Response(body, {
    headers: { 'Content-Type': 'application/xml' }
  });
}

// Copyright 2026 Crystal Arena-Turner (TerAustralis Incognita)
// SPDX-License-Identifier: CC-BY-NC-ND-4.0

import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    prerender: {
      crawl: true,
      entries: ['*'],
      handleHttpError: ({ status, path }) => {
        // Content pages mirror repo docs whose repo-relative links (into
        // src/, crystal-core/, …) don't exist as site routes — dead by
        // design at prerender, tolerated here.
        if (status === 404 && /^\/src\/|^\/crystal-core\/|^\/[a-z-]*\/$/.test(path)) {
          return;
        }
        throw new Error(`${status} ${path}`);
      }
    }
  }
};

export default config;

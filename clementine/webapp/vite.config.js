import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// Local-only web interface for Clementine. The Flask API (server.py)
// runs on 127.0.0.1:5000; we proxy /api so the browser never needs CORS.
//
// GitHub Pages is a static copy of this face. VITE_BASE is set in CI to
// /Clementine-ai-companion/. The brain is not on that host.
export default defineConfig({
  base: process.env.VITE_BASE || '/',
  plugins: [svelte()],
  server: {
    port: 5174,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: false
      }
    }
  }
});

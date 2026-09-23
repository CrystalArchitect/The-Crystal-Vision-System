#!/usr/bin/env bash
# Idempotent Cloud Agent setup for the root Astro drum & bass library web app.
set -euo pipefail

cd "$(dirname "$0")/.."

# The Supabase client (src/lib/supabase.ts) throws at import time when these
# public values are missing, so the app cannot boot without them. The core
# library (tracks, search, realms, stats) is served from committed static JSON
# and works with placeholders; real credentials (for auth / playlists /
# favorites cloud sync) can be supplied as Cursor secrets and take precedence.
if [ ! -f .env ] && [ -z "${PUBLIC_SUPABASE_URL:-}" ]; then
  cat > .env <<'ENV'
PUBLIC_SUPABASE_URL=https://placeholder.supabase.co
PUBLIC_SUPABASE_ANON_KEY=placeholder-anon-key
ENV
  echo "Created .env with placeholder Supabase values."
fi

npm install

#!/usr/bin/env bash
# Skip Vercel build unless remake-hub files changed.
# Exit 0 = skip deploy · Exit 1 = build
# Use as Project → Git → Ignored Build Step (both crystal-tiktok-remakes and tiktok-remakes).
set -euo pipefail
ROOT="13_RESEARCH_SOURCES/sitting-2026-09-23-beyond-lucky-overlap/tiktok-replica"
if git diff --quiet HEAD^ HEAD -- "$ROOT"; then
  echo "No changes under $ROOT — skipping Vercel deploy."
  exit 0
fi
echo "Changes under $ROOT — proceeding with deploy."
exit 1

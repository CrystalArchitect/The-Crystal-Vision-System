#!/usr/bin/env bash
# Ignored Build Step for crystal-tiktok-remakes (rootDirectory = this folder).
# Exit 0 = skip deploy · Exit 1 = build
# Diffs this directory vs parent commit so research-only main pushes skip.
set -euo pipefail
if git diff --quiet HEAD^ HEAD -- .; then
  echo "No changes under tiktok-replica — skipping Vercel deploy."
  exit 0
fi
echo "Changes under tiktok-replica — proceeding with deploy."
exit 1

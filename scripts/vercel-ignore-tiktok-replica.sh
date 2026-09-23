#!/usr/bin/env bash
# Repo-root helper (dashboard Ignored Build Step when Root Directory is repo root).
# Prefer tiktok-replica/scripts/vercel-ignore.sh when Root Directory is the hub folder.
set -euo pipefail
ROOT="13_RESEARCH_SOURCES/sitting-2026-09-23-beyond-lucky-overlap/tiktok-replica"
if git diff --quiet HEAD^ HEAD -- "$ROOT"; then
  echo "No changes under $ROOT — skipping Vercel deploy."
  exit 0
fi
echo "Changes under $ROOT — proceeding with deploy."
exit 1

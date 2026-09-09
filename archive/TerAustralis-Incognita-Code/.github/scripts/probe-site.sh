#!/usr/bin/env bash
# Asks the live domain whether it is serving the built site.
#
# Checks a path that exists ONLY in the SvelteKit build. The bare domain is
# deliberately not used: in the failure mode this guards against — GitHub's
# branch-source builder publishing the repository root — the README renders
# at "/" and returns 200, so the homepage looks healthy while every real page
# is gone.
#
# Exits 0 once the path returns 200, or 1 after roughly two minutes.

set -uo pipefail

URL="${SITE_PROBE_URL:-https://www.teraustralis.com.au/crystalcore-os}"
ATTEMPTS="${SITE_PROBE_ATTEMPTS:-12}"
INTERVAL="${SITE_PROBE_INTERVAL:-10}"

code=000
for attempt in $(seq 1 "$ATTEMPTS"); do
  code=$(curl -sS -o /dev/null -w '%{http_code}' --max-time 15 "$URL" 2>/dev/null || echo 000)
  if [ "$code" = "200" ]; then
    echo "$URL -> 200 (attempt $attempt)"
    exit 0
  fi
  echo "$URL -> $code (attempt $attempt/$ATTEMPTS)"
  sleep "$INTERVAL"
done

echo "$URL never returned 200; last status $code"
exit 1

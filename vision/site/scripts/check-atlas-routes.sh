#!/usr/bin/env bash
# Read-only post-deployment smoke test for critical Observatory routes.
# Exit status: 0 when every route passes; 1 when any route fails.
set -uo pipefail

BASE_URL="${BASE_URL:-https://www.teraustralis.com.au}"
TIMEOUT="${TIMEOUT:-20}"
RETRIES="${RETRIES:-3}"
JSON_OUTPUT="${JSON_OUTPUT:-}"

# Format: route|label|expected body marker.
# These routes are verified against vision/site/src/routes.
ROUTES=(
  "/|Observatory homepage|Observatory"
  "/atlas|Celestial Atlas|Celestial Atlas"
  "/atlas/test-runner|Atlas QA runner|Atlas"
  "/docs|Archive|Archive"
  "/codex|Codex|Codex"
  "/gallery|Gallery|Mythos Art"
  "/crystalcore-os|CrystalCore OS|CrystalCore"
  "/ledger|Ledger|Ledger"
  "/review|Review|Review"
  "/provenance|Provenance|Provenance"
  "/repositories|Repositories|Repositories"
  "/sitemap.xml|Sitemap endpoint|<urlset"
)

results=()
failed=0

url_encode_json() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

check_route() {
  local route="$1"
  local label="$2"
  local marker="$3"
  local url="${BASE_URL%/}${route}"
  local response status final_url content_type body marker_found

  if ! response=$(curl --silent --show-error --location \
    --max-time "$TIMEOUT" \
    --connect-timeout "$TIMEOUT" \
    --retry "$RETRIES" \
    --retry-delay 2 \
    --retry-all-errors \
    --proto '=https' --proto-redir '=https' \
    --output /tmp/observatory-route-body.$$ \
    --write-out '%{http_code}\t%{url_effective}\t%{content_type}' \
    "$url" 2>&1); then
    printf 'FAIL  %-24s curl error: %s\n' "$label" "$(url_encode_json "$response")"
    results+=("{\"route\":\"$(url_encode_json "$route")\",\"label\":\"$(url_encode_json "$label")\",\"url\":\"$(url_encode_json "$url")\",\"status\":null,\"final_url\":null,\"passed\":false,\"error\":\"$(url_encode_json "$response")\"}")
    failed=1
    return
  fi

  IFS=$'\t' read -r status final_url content_type <<< "$response"
  body=$(cat /tmp/observatory-route-body.$$ 2>/dev/null || true)
  rm -f /tmp/observatory-route-body.$$
  marker_found=false
  if printf '%s' "$body" | grep -Fqi -- "$marker"; then
    marker_found=true
  fi

  if [[ "$status" =~ ^2[0-9][0-9]$ ]] && [[ "$marker_found" == true ]]; then
    printf 'PASS  %-24s HTTP %s  %s\n' "$label" "$status" "$final_url"
    results+=("{\"route\":\"$(url_encode_json "$route")\",\"label\":\"$(url_encode_json "$label")\",\"url\":\"$(url_encode_json "$url")\",\"status\":$status,\"final_url\":\"$(url_encode_json "$final_url")\",\"content_type\":\"$(url_encode_json "$content_type")\",\"marker\":\"$(url_encode_json "$marker")\",\"marker_found\":true,\"passed\":true}")
  else
    printf 'FAIL  %-24s HTTP %s  marker=%s  %s\n' "$label" "$status" "$marker_found" "$final_url"
    results+=("{\"route\":\"$(url_encode_json "$route")\",\"label\":\"$(url_encode_json "$label")\",\"url\":\"$(url_encode_json "$url")\",\"status\":$status,\"final_url\":\"$(url_encode_json "$final_url")\",\"content_type\":\"$(url_encode_json "$content_type")\",\"marker\":\"$(url_encode_json "$marker")\",\"marker_found\":$marker_found,\"passed\":false}")
    failed=1
  fi
}

printf 'Observatory production route smoke test\n'
printf 'Base URL: %s\n\n' "$BASE_URL"

for entry in "${ROUTES[@]}"; do
  IFS='|' read -r route label marker <<< "$entry"
  check_route "$route" "$label" "$marker"
done

if [[ -n "$JSON_OUTPUT" ]]; then
  printf '[%s]\n' "$(IFS=,; printf '%s' "${results[*]}")" > "$JSON_OUTPUT"
  printf '\nJSON report: %s\n' "$JSON_OUTPUT"
fi

if (( failed )); then
  printf '\nRESULT: FAIL\n'
  exit 1
fi

printf '\nRESULT: PASS\n'
exit 0

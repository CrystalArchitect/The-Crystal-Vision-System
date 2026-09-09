#!/usr/bin/env bash
# Anchor the creative-work manifest to Bitcoin via OpenTimestamps.
#
# Run this from anywhere with ordinary internet access. It is deliberately one
# command, because the environment the tooling was written in cannot reach the
# calendar servers and this is the step that has to happen elsewhere.
#
#     bash mythos/tools/stamp.sh
#
# Free. No wallet, no token, no cryptocurrency. See
# docs/governance/PROVENANCE-TIMESTAMPS.md for what the resulting proof does
# and does not demonstrate.

set -euo pipefail

cd "$(dirname "$0")/../.."
MANIFEST="mythos/MANIFEST.sha256"

command -v ots >/dev/null 2>&1 || {
  echo "Installing the OpenTimestamps client..."
  pip install --quiet opentimestamps-client
}

echo "Checking the manifest is current..."
python3 mythos/tools/provenance.py --check || {
  echo
  echo "The manifest is stale — the files listed above have changed since it"
  echo "was written. Stamping it now would anchor a record that does not match"
  echo "the work. Run this first, commit the result, then stamp:"
  echo
  echo "    python3 mythos/tools/provenance.py"
  exit 1
}

if [ -e "$MANIFEST.ots" ]; then
  current=$(sha256sum "$MANIFEST" | awk '{print $1}')
  attested=$(ots info "$MANIFEST.ots" | sed -n 's/^File sha256 hash: //p')
  if [ "$attested" != "$current" ]; then
    echo
    echo "The existing proof attests a different manifest:"
    echo "  proof    $attested"
    echo "  manifest $current"
    echo
    echo "Upgrading it would refresh evidence for work that has moved on."
    echo "Run this first — it archives the old proof beside the manifest it"
    echo "actually attests, and clears the way for a fresh stamp:"
    echo
    echo "    python3 mythos/tools/provenance.py"
    exit 1
  fi
  echo
  echo "A proof already exists and matches. Upgrading it (safe to repeat):"
  ots upgrade "$MANIFEST.ots" || true
  ots verify "$MANIFEST.ots" || true
  exit 0
fi

echo "Stamping $MANIFEST..."
ots stamp "$MANIFEST"

cat <<'EOF'

Done. A proof now sits beside the manifest.

It is incomplete for the next hour or so — the calendars answer immediately,
but the Bitcoin block it depends on has not been mined yet. That is expected.

Commit it now:

    git add mythos/MANIFEST.sha256.ots
    git commit -m "Anchor the manifest"

Then, any time after an hour, run this script again. It will upgrade the proof
to its final form and verify it.
EOF

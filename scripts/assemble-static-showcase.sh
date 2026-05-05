#!/usr/bin/env bash
# Assemble the static HTML component showcase with copied CSS and rewritten hrefs.
# Usage: scripts/assemble-static-showcase.sh [DEST_DIR]
# Default DEST_DIR is repo-root/_site (standalone preview).
# For the Bengal site, pass repo-root/site/public/showcase after `bengal build --source site`.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${1:-$REPO_ROOT/_site}"

mkdir -p "$OUT/css"
cp "$REPO_ROOT/src/chirp_ui/templates/chirpui.css" "$OUT/css/"
cp "$REPO_ROOT/src/chirp_ui/templates/chirpui-transitions.css" "$OUT/css/"
sed \
  -e 's|../../src/chirp_ui/templates/chirpui.css|css/chirpui.css|' \
  -e 's|../../src/chirp_ui/templates/chirpui-transitions.css|css/chirpui-transitions.css|' \
  "$REPO_ROOT/examples/static-showcase/index.html" >"$OUT/index.html"

echo "Assembled static showcase at $OUT/index.html"

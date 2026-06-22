#!/usr/bin/env bash
# Post-deploy smoke for the component showcase (#310).
# Usage:
#   ./scripts/showcase_deploy_smoke.sh
#   SHOWCASE_URL=http://127.0.0.1:8000 ./scripts/showcase_deploy_smoke.sh
set -euo pipefail

BASE="${SHOWCASE_URL:-https://chirp-ui-showcase-production.up.railway.app}"
USER_AGENT="${SHOWCASE_SMOKE_UA:-chirp-ui-showcase-smoke/1.0}"

curl_common=(curl -fsS --max-time 30 -A "$USER_AGENT")

echo "Showcase deploy smoke → ${BASE}"

for path in \
  /catalog-shell \
  /support-shell \
  /operations-shell \
  /composer
do
  echo "GET ${path}"
  "${curl_common[@]}" -o /dev/null -w "  HTTP %{http_code}\n" "${BASE}${path}"
done

echo "POST /composer/send"
response="$("${curl_common[@]}" -X POST "${BASE}/composer/send" -d "message=hello")"
if ! grep -q "chirpui-message-bubble--right" <<<"$response"; then
  echo "ERROR: POST /composer/send did not return a message bubble fragment" >&2
  echo "$response" | head -c 500 >&2
  exit 1
fi
if ! grep -q "<p>hello</p>" <<<"$response"; then
  echo "ERROR: POST /composer/send response missing echoed message text" >&2
  exit 1
fi

echo "OK — shell recipes, composer page, and composer POST fragment passed"

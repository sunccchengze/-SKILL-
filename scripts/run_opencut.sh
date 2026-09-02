#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$REPO_ROOT/full-sources/tools/opencut/apps/web"
BUN="${HOME}/.local/bin/bun"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5173}"

if [[ ! -x "$BUN" ]] || [[ ! -d "$APP/node_modules" ]]; then
  echo "OpenCut is not set up. Run: bash scripts/setup_tools.sh opencut" >&2
  exit 1
fi

cd "$APP"
exec "$BUN" run dev --host "$HOST" --port "$PORT"

#!/usr/bin/env bash
set -euo pipefail

RUSTDESK="${HOME}/.local/bin/rustdesk"
if [[ ! -x "$RUSTDESK" ]]; then
  echo "RustDesk binary package is not installed." >&2
  echo "Run: bash scripts/setup_tools.sh rustdesk-package" >&2
  exit 1
fi
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
  echo "RustDesk requires an interactive X11 or Wayland desktop session." >&2
  exit 1
fi

cat <<'EOF'
RustDesk may expose screen, keyboard, mouse, clipboard, audio, files, or tunnels.
Continue only with explicit authorization from every endpoint owner.
EOF
exec "$RUSTDESK" "$@"

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0

check_pin() {
  local label="$1" path="$2" expected="$3" actual
  actual="$(git -C "$REPO_ROOT/$path" rev-parse HEAD 2>/dev/null || true)"
  if [[ "$actual" == "$expected" ]]; then
    echo "PASS $label source: $actual"
  else
    echo "FAIL $label source: expected $expected, found ${actual:-not initialized}" >&2
    status=1
  fi
}

check_pin OpenCut full-sources/tools/opencut 400f097becba5db0fbc305d5a65348cb81c20356
check_pin RustDesk full-sources/tools/rustdesk 6c578292e8ebbbec708b76986ba8c4bc7c509747
check_pin Spec-Kit full-sources/tools/spec-kit d1f50fcbe684a4222059c4ba7f2d7eabcca87402

if [[ -x "$HOME/.local/bin/bun" ]] && [[ "$($HOME/.local/bin/bun --version)" == "1.3.11" ]]; then
  echo "PASS Bun: 1.3.11"
else
  echo "FAIL Bun: expected 1.3.11" >&2
  status=1
fi

if [[ -x "$HOME/.local/bin/specify" ]] && [[ "$($HOME/.local/bin/specify --version)" == "specify 0.16.4" ]]; then
  echo "PASS Specify CLI: 0.16.4"
else
  echo "FAIL Specify CLI: expected 0.16.4" >&2
  status=1
fi

if [[ -x "$HOME/.local/bin/rustdesk" ]]; then
  echo "PASS RustDesk wrapper: $HOME/.local/bin/rustdesk"
else
  echo "INFO RustDesk native package: not installed; source pin is still verified"
fi

exit "$status"
